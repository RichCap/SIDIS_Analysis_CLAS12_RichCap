#!/usr/bin/env run-groovy

import org.jlab.jnp.hipo4.io.HipoReader
import org.jlab.jnp.hipo4.data.Bank
import org.jlab.jnp.hipo4.data.Event
import org.jlab.jnp.hipo4.data.SchemaFactory
import groovyx.gpars.GParsPool
import org.jlab.clas.physics.LorentzVector
import org.jlab.jroot.ROOTFile
import uconn.utils.pid.Candidate.Level
import uconn.utils.pid.stefan.ElectronCandidate
import uconn.utils.pid.stefan.PionCandidate
import my.Sugar
// import clasqa.QADB

long StartTime = System.nanoTime()

Sugar.enable()

def isinb = ! ( args[0].contains('outb') || args[0].contains('torus+1') )
def ismc  = args[0].contains("gemc")

def suff = isinb ? 'inb' : 'outb'
if(ismc) suff += '.mc'
else suff += '.qa'

def outname = args[0].split("/")[-1]

// def ff = new ROOTFile("MC_Gen_sidis_epip_richcap.${suff}.new5.${outname}.root")

// // Updated on 4/16/2025: Running over files with different background merging settings (used 45nA instead of 50nA), so changed names of file outputs (no other changes were made to how the code runs)
// def ff = new ROOTFile("MC_Gen_sidis_epip_richcap.${suff}.new5.45nA.${outname}.root")

// Updated on 12/17/2025: new6 does not differentiate between the background merging settings for the baseline file names (must see individual HIPO files for such distinctions)
def ff = new ROOTFile("MC_Gen_sidis_epip_richcap.${suff}.new6.${outname}.root")

// // Added 'Num_Pions' as of 7/29/2024 (as part of version 'new5' - name used to match the reconstructed files)
// def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:beamCharge:Num_Pions/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Hx:Hy')

// Added parent PIDs of both particles as of 12/17/2025 (with 'new6' version)
def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:beamCharge:Num_Pions/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Hx:Hy:Par_PID_el/I:Par_PID_pip/I')

int Multiple_Pions_Per_Electron = 0
int Total_Events_Found = 0

def beam = LorentzVector.withPID(11,0,0,10.6041)

def Q2_cut_Count   = 0
def Q2_nocut_Count = 0
def Q2_SIDIS_Count = 0


// Tolerances for float comparisons (tune as needed)
final double ABS_TOL = 1e-6
final double REL_TOL = 1e-4

// Helper: robust float compare (absolute + relative)
boolean nearlyEqual(double a, double b, double absTol, double relTol) {
    double diff = Math.abs(a - b)
    if (diff <= absTol) return true
    double scale = Math.max(Math.abs(a), Math.abs(b))
    return diff <= relTol * scale
}

// Finds the LUND particle matching the provided PID and momentum and returns the PID of its parent particle.
// Returns 0 if no matching particle is found.
Integer findParentPIDFromLund(def lund_in, int pid_in, float px_in, float py_in, float pz_in, double absTol, double relTol) {

    int nrows_lund = lund_in.getRows()

    for (int i = 0; i < nrows_lund; i++) {

        // Pull candidate from MC::Lund at row i
        int   pid_lund = lund_in.getInt("pid",  i)
        float px_lund  = lund_in.getFloat("px", i)
        float py_lund  = lund_in.getFloat("py", i)
        float pz_lund  = lund_in.getFloat("pz", i)

        // Compare with values you already extracted from the other bank
        boolean pidOK = (pid_lund == pid_in)
        boolean pxOK   = nearlyEqual(px_lund, px_in, absTol, relTol)
        boolean pyOK   = nearlyEqual(py_lund, py_in, absTol, relTol)
        boolean pzOK   = nearlyEqual(pz_lund, pz_in, absTol, relTol)

        // If this row does not match, continue searching
        if (!(pidOK && pxOK && pyOK && pzOK)) { continue }

        // ---- Match found ----
        int parentIndex = lund_in.getByte("parent", i)  // 'parent' is type 'B'

        // Defensive check on parent index
        if (parentIndex < 0 || parentIndex >= nrows_lund) {
            System.out.println("WARNING - Matched particle found, but parent index is invalid: ${parentIndex}")
            return 0
        }

        int parentPID = lund_in.getInt("pid", parentIndex)

        // System.out.println("Matched LUND row = ${i}")
        // System.out.println("parentPID = ${parentPID}")

        return parentPID
    }

    // ---- No match found ----
    System.out.println("ERROR - No matching particle found in LUND bank.")
    System.out.println("Target Particle = (pid,px,py,pz)=(${pid_in},${px_in},${py_in},${pz_in})")

    return 0
}


GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    // QADB qa = new QADB()

    def reader = new HipoReader()
    reader.open(fname)
    def event = new Event()
    def factory = reader.getSchemaFactory()
    def banks = ['MC::Header', 'REC::Event', 'MC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator', 'MC::Lund'].collect{new Bank(factory.getSchema(it))}

    while(reader.hasNext()){
        reader.nextEvent(event)
        banks.each{event.read(it)}

        if(banks.every()){
            def (runb, evb, partb, ecb, ccb, trajb, scb, lund) = banks

            def run = runb.getInt("run",   0)
            def evn = runb.getInt("event", 0)
            def pid = partb.getInt("pid",  0)
            
            def beamCharge = evb.getFloat("beamCharge", 0)
            
            if(pid == 11){ // Is an electron
                
                int pionCount = 0 // Counter for pions (helps control double-counted electrons)
                
                def ex  = partb.getFloat("px", 0)
                def ey  = partb.getFloat("py", 0)
                def ez  = partb.getFloat("pz", 0)
                def ele = LorentzVector.withPID(pid, ex, ey, ez)
                def Q2  = -(beam - ele).mass2()
                
                // System.out.println("Finding electron Parent:");
                int parentPID_el = findParentPIDFromLund(lund, pid, ex, ey, ez, ABS_TOL, REL_TOL);
                // System.out.println("parentPID_el = ${parentPID_el}");

                if(Q2 > 1.5){ Q2_cut_Count += 1;}
                else{ Q2_nocut_Count += 1;}
                
                for(int ipart = 1; ipart < partb.getRows(); ipart++){
                    def pid_pip = partb.getInt("pid", ipart)
                    
                    if(pid_pip == 211){ // Is a Pi+
                        
                        pionCount += 1;                                         // Increment pion counter
                        Total_Events_Found += 1;                                // Increment "total event" counter
                        if(pionCount != 1){ Multiple_Pions_Per_Electron += 1; } // Increment "number of double-counted electron" counter

                        if(Q2 > 1.5){ Q2_SIDIS_Count += 1; }
                        
                        def px = partb.getFloat("px", ipart)
                        def py = partb.getFloat("py", ipart)
                        def pz = partb.getFloat("pz", ipart)
                        def pip0 = LorentzVector.withPID(pid_pip, px, py, pz)
                        
                        // System.out.println("Finding pi+ pion Parent:");
                        int parentPID_pi = findParentPIDFromLund(lund, pid_pip, px, py, pz, ABS_TOL, REL_TOL);
                        // System.out.println("parentPID_pi = ${parentPID_pi}");

                        // Coordinate of the matched hit (cm) - for Valerii's cuts (done in python)
                        float Hx = ecb.getFloat("hx", 0)
                        float Hy = ecb.getFloat("hy", 0)

                        // // Spherical Momentum Coordinates
                        def elPhi = (180/3.1415926)*ele.phi()
                        def pipPhi = (180/3.1415926)*pip0.phi()

                        // Electron Sectors (From Angle)
                        def esec_a = 0
                        if(elPhi >=  -30 && elPhi <   30){esec_a = 1}
                        if(elPhi >=   30 && elPhi <   90){esec_a = 2}
                        if(elPhi >=   90 && elPhi <  150){esec_a = 3}
                        if(elPhi >=  150 || elPhi < -150){esec_a = 4}
                        if(elPhi >=  -90 && elPhi <  -30){esec_a = 5}
                        if(elPhi >= -150 && elPhi <  -90){esec_a = 6}

                        // Pi+ Sectors (From Angle)
                        def pipsec_a = 0
                        if(pipPhi >=  -45 && pipPhi <   15){pipsec_a = 1}
                        if(pipPhi >=   15 && pipPhi <   75){pipsec_a = 2}
                        if(pipPhi >=   75 && pipPhi <  135){pipsec_a = 3}
                        if(pipPhi >=  135 || pipPhi < -165){pipsec_a = 4}
                        if(pipPhi >= -105 && pipPhi <  -45){pipsec_a = 5}
                        if(pipPhi >= -165 && pipPhi < -105){pipsec_a = 6}
                        
                        tt.fill(evn, run,  beamCharge, pionCount,
                                 ex, ey,   ez, px, py, pz,
                             esec_a, pipsec_a, Hx, Hy,
                             parentPID_el, parentPID_pi)
                    }
                }
            }
        }
    }

    reader.close()
}
}

System.out.println("");

System.out.println("Total number of events found                                = " + Total_Events_Found);
System.out.println("");

System.out.println("Number of times that Multiple Pions were found per Electron = " + Multiple_Pions_Per_Electron);
System.out.println("");

System.out.println("Total number of generated events found with Q2 > 1.5        = " + Q2_cut_Count);
System.out.println("Total number of generated events found with Q2 < 1.5        = " + Q2_nocut_Count);
System.out.println("Total number of   SIDIS   events found with Q2 > 1.5        = " + Q2_SIDIS_Count);
System.out.println("");

long RunTime = (System.nanoTime() - StartTime)/1000000000;

if(RunTime > 60){
    RunTime = RunTime/60;
    System.out.println("This code's runtime (in min) is: ");
}
else{
    System.out.println("This code's runtime (in sec) is: ");
}

System.out.println(RunTime);


tt.write()
ff.close()
