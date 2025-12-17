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
import uconn.utils.pid.stefan.ProtonCandidate
import my.Sugar
// import clasqa.QADB

long StartTime = System.nanoTime()

Sugar.enable()


def beam   = LorentzVector.withPID(11,  0,0,10.6041)
def target = LorentzVector.withPID(2212,0,0,0)

def isinb = ! ( args[0].contains('outb') || args[0].contains('torus+1') )
def ismc  = args[0].contains("gemc")

def suff = isinb ? 'inb' : 'outb'
if(ismc) suff += '.mc'
else suff += '.qa'

def outname = args[0].split("/")[-1]

// As of 7/25/2024:
def ff = new ROOTFile("Data_sidis_epip_richcap.${suff}.wProton.new5.${outname}.root")

// DC hits had to be separated into 3 values per particle per event (each layer is hit and stored separately within each event) - Updated on 7/25/2024
    // Added/renamed several variables to do this
    // Removed detector/layer info now that it is built into the other variables
    // Runs with 'new5'
    // Also added "Num_Pions" to help control events where the electron is counted twice (in case that is a previously overlooked issue)
def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:beamCharge:ex:ey:ez:pipx:pipy:pipz:prox:proy:proz:esec/I:pipsec/I:Num_Pions/I:Hx:Hy:Hx_pip:Hy_pip:V_PCal:W_PCal:U_PCal:ele_x_DC_6:ele_y_DC_6:ele_z_DC_6:ele_x_DC_18:ele_y_DC_18:ele_z_DC_18:ele_x_DC_36:ele_y_DC_36:ele_z_DC_36:pip_x_DC_6:pip_y_DC_6:pip_z_DC_6:pip_x_DC_18:pip_y_DC_18:pip_z_DC_18:pip_x_DC_36:pip_y_DC_36:pip_z_DC_36')

int event_count = 0;

int Multiple_Pions_Per_Electron = 0

GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    // QADB qa = new QADB()

    def reader = new HipoReader()
    reader.open(fname)
    def event = new Event()
    def factory = reader.getSchemaFactory()
    def banks = ['RUN::config','REC::Event','REC::Particle','REC::Calorimeter','REC::Cherenkov','REC::Traj','REC::Scintillator'].collect{new Bank(factory.getSchema(it))}

    while(reader.hasNext()){
        reader.nextEvent(event)
        banks.each{event.read(it)}

        if(banks.every()){
            def (runb,evb,partb,ecb,ccb,trajb,scb) = banks

            def run = runb.getInt("run",  0)
            def evn = runb.getInt("event",0)
            
            // def skipqadb = false//true
            // // Running with QADB requirements despite it not being fully updated for Pass 2 yet (still using Pass 1 requirements to my knowledge - was like this in all prior runs before 6/6/2024)
            // // Remove this note when QADB is updated
            // if(ismc || skipqadb || qa.OkForAsymmetry(run, evn)){
            def skipqadb = true // Skipping as of 7/2/2024 as I couldn't get the QADB to load (also it hasn't been updated for Pass 2 anyway)
            if(ismc || skipqadb){
                
                def canele = ElectronCandidate.getElectronCandidate(0, partb, ecb, ccb, trajb, isinb)
                def ele    = canele.getLorentzVector()
                
                def beamCharge = evb.getFloat("beamCharge", 0)

                if(canele.iselectron()){ // A electron has been found
                    
                    int pionCount = 0 // Counter for pions (helps control double-counted electrons)

                    // Check for the presence of a proton (for Harut's Vector Meson Cuts)
                    boolean hasProton = false
                    def proV = null // Declare proV to store the proton Lorentz vector
                    for (int ipart_proton = 1; ipart_proton < partb.getRows(); ipart_proton++) {
                        def canpro = ProtonCandidate.getProtonCandidate(ipart_proton, partb, trajb, isinb)
                        if(canpro.isproton()){
                            hasProton = true
                            proV = canpro.getLorentzVector() // Get the Lorentz vector of the proton
                            break
                        }
                    }
                    // Skip to the next event if no proton is found
                    if(!hasProton){
                        continue
                    }
                    
                    
                    for(int ipart = 1; ipart < partb.getRows(); ipart++){
                        def canpip = PionCandidate.getPionCandidate(ipart, partb, trajb, isinb)
                        
                        if(canpip.ispip()){ // After this 'if' statement, the event being added to the ntuple is known to have at least one electron AND pi+ pion
                            
                            pionCount += 1; // Increment pion counter
                            
                            def pip0 = canpip.getLorentzVector()
                            
                            // Cartesian Momentum Coordinates
                            def ex   = ele.px(),  ey   = ele.py(),  ez   = ele.pz()
                            def px   = pip0.px(), py   = pip0.py(), pz   = pip0.pz()
                            def prox = proV.px(), proy = proV.py(), proz = proV.pz()
                            
                            // Sectors (From Detector)
                            def esec = canele.getPCALsector(), pipsec = canpip.getDCsector()
                            
                            // Coordinate of the matched hit (PCAL) [cm] - for Valerii's cuts (done in python) - Based on Electron
                            float Hx = ecb.getFloat("hx", 0)
                            float Hy = ecb.getFloat("hy", 0)
                            
                            // For other valerii cuts
                            // int detector_PCal = ecb.getInt("detector", 0)
                            // int layer_PCal    = ecb.getInt("layer",    0)
                            float V_PCal = ecb.getFloat("lv", 0)
                            float W_PCal = ecb.getFloat("lw", 0)
                            float U_PCal = ecb.getFloat("lu", 0)
                            
                            float ele_x_DC_6  = Float.NaN, ele_y_DC_6  = Float.NaN, ele_z_DC_6  = Float.NaN
                            float ele_x_DC_18 = Float.NaN, ele_y_DC_18 = Float.NaN, ele_z_DC_18 = Float.NaN
                            float ele_x_DC_36 = Float.NaN, ele_y_DC_36 = Float.NaN, ele_z_DC_36 = Float.NaN
                            for(int ii_el = 0; ii_el < trajb.getRows(); ii_el++) {
                                // Check conditions: pindex is 0 and detector is 6
                                if(trajb.getShort("pindex", ii_el) == 0 && trajb.getByte("detector", ii_el) == 6){
                                    // Process based on layer value
                                    if(trajb.getByte("layer", ii_el) == 6) {
                                        ele_x_DC_6  = trajb.getFloat("x", ii_el)
                                        ele_y_DC_6  = trajb.getFloat("y", ii_el)
                                        ele_z_DC_6  = trajb.getFloat("z", ii_el)
                                    } else if(trajb.getByte("layer", ii_el) == 18) {
                                        ele_x_DC_18 = trajb.getFloat("x", ii_el)
                                        ele_y_DC_18 = trajb.getFloat("y", ii_el)
                                        ele_z_DC_18 = trajb.getFloat("z", ii_el)
                                    } else if(trajb.getByte("layer", ii_el) == 36) {
                                        ele_x_DC_36 = trajb.getFloat("x", ii_el)
                                        ele_y_DC_36 = trajb.getFloat("y", ii_el)
                                        ele_z_DC_36 = trajb.getFloat("z", ii_el)
                                    }
                                }
                            }
                            
                            float Hx_pip = Float.NaN, Hy_pip = Float.NaN
                            // Coordinate of the matched hit (PCAL) [cm] - for fiducial cuts - Based on Pion
                            for(int jj = 0; jj < ecb.getRows(); jj++){
                                // Extracting hx and hy from 'ecb' bank for the pion by looping through the bank
                                if((ecb.getShort("pindex", jj) == ipart) && (ecb.getByte("detector", jj) == 7) && (ecb.getByte("layer", jj) == 1)){
                                    Hx_pip = ecb.getFloat("hx", jj)
                                    Hy_pip = ecb.getFloat("hy", jj)
                                    break // Exit the loop once the matching entry is found
                                }
                            }
                            float pip_x_DC_6  = Float.NaN, pip_y_DC_6  = Float.NaN, pip_z_DC_6  = Float.NaN
                            float pip_x_DC_18 = Float.NaN, pip_y_DC_18 = Float.NaN, pip_z_DC_18 = Float.NaN
                            float pip_x_DC_36 = Float.NaN, pip_y_DC_36 = Float.NaN, pip_z_DC_36 = Float.NaN
                            for(int ii_pip = 0; ii_pip < trajb.getRows(); ii_pip++) {
                                // Check conditions: pindex matches ipart and detector is 6
                                if(trajb.getShort("pindex", ii_pip) == ipart && trajb.getByte("detector", ii_pip) == 6){
                                    // Process based on layer value
                                    if(trajb.getByte("layer", ii_pip) == 6) {
                                        pip_x_DC_6  = trajb.getFloat("x", ii_pip)
                                        pip_y_DC_6  = trajb.getFloat("y", ii_pip)
                                        pip_z_DC_6  = trajb.getFloat("z", ii_pip)
                                    } else if(trajb.getByte("layer", ii_pip) == 18) {
                                        pip_x_DC_18 = trajb.getFloat("x", ii_pip)
                                        pip_y_DC_18 = trajb.getFloat("y", ii_pip)
                                        pip_z_DC_18 = trajb.getFloat("z", ii_pip)
                                    } else if(trajb.getByte("layer", ii_pip) == 36) {
                                        pip_x_DC_36 = trajb.getFloat("x", ii_pip)
                                        pip_y_DC_36 = trajb.getFloat("y", ii_pip)
                                        pip_z_DC_36 = trajb.getFloat("z", ii_pip)
                                    }
                                }
                            }
                            
                            tt.fill(evn,      run,      beamCharge,        ex, ey, ez,        px, py, pz,  prox, proy, proz, 
                                    esec,     pipsec,   pionCount,         Hx, Hy, Hx_pip,    Hy_pip,
                                    V_PCal,             W_PCal,            U_PCal, 
                                    ele_x_DC_6,         ele_y_DC_6,        ele_z_DC_6,
                                    ele_x_DC_18,        ele_y_DC_18,       ele_z_DC_18,
                                    ele_x_DC_36,        ele_y_DC_36,       ele_z_DC_36,
                                    pip_x_DC_6,         pip_y_DC_6,        pip_z_DC_6,
                                    pip_x_DC_18,        pip_y_DC_18,       pip_z_DC_18,
                                    pip_x_DC_36,        pip_y_DC_36,       pip_z_DC_36)

                            if(pionCount > 1){
                                Multiple_Pions_Per_Electron += 1
                            }
                            event_count += 1;

                        }
                    }
                }
            }
        }
    }

    reader.close()
}
}


System.out.println("");


System.out.println("Total number of events found: ");
System.out.println(event_count);
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

System.out.println("");


tt.write()
ff.close()
