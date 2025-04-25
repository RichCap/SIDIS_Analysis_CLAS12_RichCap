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

// def ff = new ROOTFile("MC_Gen_sidis_epip_richcap.${suff}.wProton.new5.${outname}.root")

// Updated on 4/22/2025: Running over files with different background merging settings (used 45nA instead of 50nA), so changed names of file outputs (no other changes were made to how the code runs)
    // On 4/23/2025: Also removed the clasqa.QADB to be in line with the other groovy scripts (will add back later when rerunning all files)
def ff = new ROOTFile("MC_Gen_sidis_epip_richcap.${suff}.wProton.new5.45nA.${outname}.root")

// Added 'Num_Pions' and Proton info as of 7/29/2024 (as part of version 'wProton.new5' - name used to match the reconstructed files)
def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:beamCharge:Num_Pions/I:ex:ey:ez:pipx:pipy:pipz:prox:proy:proz:esec/I:pipsec/I:Hx:Hy')

int Multiple_Pions_Per_Electron = 0
int Total_Events_Found = 0

GParsPool.withPool 2,{
    args.eachParallel{fname->
        println(fname)
        // QADB qa = new QADB()

        def reader = new HipoReader()
        reader.open(fname)
        def event = new Event()
        def factory = reader.getSchemaFactory()
        def banks = ['MC::Header', 'REC::Event', 'MC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator'].collect{new Bank(factory.getSchema(it))}

        while(reader.hasNext()){
            reader.nextEvent(event)
            banks.each{event.read(it)}

            if(banks.every()){
                def (runb, evb, partb, ecb, ccb, trajb, scb) = banks

                def run = runb.getInt("run",   0)
                def evn = runb.getInt("event", 0)
                def pid = partb.getInt("pid",  0)

                def beamCharge = evb.getFloat("beamCharge", 0)

                if(pid == 11){ // Is an electron

                    int pionCount = 0 // Counter for pions (helps control double-counted electrons)

                    // Check for the presence of a proton (for Harut's Vector Meson Cuts)
                    boolean hasProton = false
                    // def proV = null // Declare proV to store the proton Lorentz vector
                    def prox = null
                    def proy = null
                    def proz = null
                    for (int ipart_proton = 1; ipart_proton < partb.getRows(); ipart_proton++){
                        def pid_pro = partb.getInt("pid", ipart_proton)
                        if(pid_pro == 2212){
                            hasProton = true
                            prox = partb.getFloat("px", ipart_proton)
                            proy = partb.getFloat("py", ipart_proton)
                            proz = partb.getFloat("pz", ipart_proton)
                            // proV = LorentzVector.withPID(pid_pro, prox, proy, proz) // Get the Lorentz vector of the proton
                            // Lorentz vector for proton is not in use due to not keeping the proton sector info
                            break
                        }
                    }
                    // Skip to the next event if no proton is found
                    if(!hasProton){
                        continue
                    }

                    for(int ipart = 1; ipart < partb.getRows(); ipart++){
                        def pid_pip = partb.getInt("pid", ipart)

                        if(pid_pip == 211){ // Is a Pi+

                            pionCount += 1;                       // Increment pion counter
                            Total_Events_Found += 1;              // Increment "total event" counter
                            if(pionCount != 1){
                                Multiple_Pions_Per_Electron += 1; // Increment "number of double-counted electron" counter
                            }

                            def ex = partb.getFloat("px", 0)
                            def ey = partb.getFloat("py", 0)
                            def ez = partb.getFloat("pz", 0)
                            def ele = LorentzVector.withPID(pid, ex, ey, ez)

                            def px = partb.getFloat("px", ipart)
                            def py = partb.getFloat("py", ipart)
                            def pz = partb.getFloat("pz", ipart)
                            def pip0 = LorentzVector.withPID(pid_pip, px, py, pz)

                            // Coordinate of the matched hit (cm) - for Valerii's cuts (done in python)
                            float Hx = ecb.getFloat("hx", 0)
                            float Hy = ecb.getFloat("hy", 0)

                            // Spherical Momentum Coordinates
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

                            tt.fill(evn, run, beamCharge, pionCount,
                                    ex,  ey,  ez, px, py, pz,  prox, proy, proz,
                                esec_a, pipsec_a, Hx, Hy)
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
