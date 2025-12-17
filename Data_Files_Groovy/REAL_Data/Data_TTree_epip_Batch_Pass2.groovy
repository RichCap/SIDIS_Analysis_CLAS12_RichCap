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
import clasqa.QADB

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


// // As of 7/25/2024:
// def ff = new ROOTFile("Data_sidis_epip_richcap.${suff}.new5.${outname}.root")

// As of 12/16/2025:
def ff = new ROOTFile("Data_sidis_epip_richcap.${suff}.new6.${outname}.root")


// DC hits had to be separated into 3 values per particle per event (each layer is hit and stored separately within each event) - Updated on 7/25/2024
    // Added/renamed several variables to do this
    // Removed detector/layer info now that it is built into the other variables
    // Runs with 'new5'
    // Also added "Num_Pions" to help control events where the electron is counted twice (in case that is a previously overlooked issue)
def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:beamCharge:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Num_Pions/I:Hx:Hy:Hx_pip:Hy_pip:V_PCal:W_PCal:U_PCal:ele_x_DC_6:ele_y_DC_6:ele_z_DC_6:ele_x_DC_18:ele_y_DC_18:ele_z_DC_18:ele_x_DC_36:ele_y_DC_36:ele_z_DC_36:pip_x_DC_6:pip_y_DC_6:pip_z_DC_6:pip_x_DC_18:pip_y_DC_18:pip_z_DC_18:pip_x_DC_36:pip_y_DC_36:pip_z_DC_36')

int event_count = 0;
int DC_count = 0;

int Multiple_Pions_Per_Electron = 0

GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    QADB qa = new QADB("latest")
    qa.checkForDefect('TotalOutlier')     // these choices match the criteria of `OkForAsymmetry`
    qa.checkForDefect('TerminalOutlier')
    qa.checkForDefect('MarginalOutlier')
    qa.checkForDefect('SectorLoss')
    qa.checkForDefect('Misc')
    [ // list of runs with `Misc` defect that are allowed by `OkForAsymmetry`
      5046, 5047, 5051, 5128, 5129, 5130, 5158, 5159,
      5160, 5163, 5165, 5166, 5167, 5168, 5169, 5180,
      5181, 5182, 5183, 5400, 5448, 5495, 5496, 5505,
      5567, 5610, 5617, 5621, 5623, 6736, 6737, 6738,
      6739, 6740, 6741, 6742, 6743, 6744, 6746, 6747,
      6748, 6749, 6750, 6751, 6753, 6754, 6755, 6756,
      6757
    ].each{ run -> qa.allowMiscBit(run) }
    // after this, just use `qa.pass(run, evn)` for each event (instead of `qa.OkForAsymmetry(run, evn)`)


    def reader = new HipoReader()
    reader.open(fname)
    def event = new Event()
    def factory = reader.getSchemaFactory()
    def banks = ['RUN::config','REC::Event','REC::Particle','REC::Calorimeter','REC::Cherenkov','REC::Traj','REC::Scintillator'].collect{new Bank(factory.getSchema(it))}
    
    // int elec_total_found  = 0;
    // int elec_num_current  = 0;
    // int elec_events_found = 0;

    while(reader.hasNext()){
        reader.nextEvent(event)
        banks.each{event.read(it)}

        if(banks.every()){
            def (runb,evb,partb,ecb,ccb,trajb,scb) = banks

            def run = runb.getInt("run",  0)
            def evn = runb.getInt("event",0)
            
            // // Running with QADB requirements despite it not being fully updated for Pass 2 yet (still using Pass 1 requirements to my knowledge - was like this in all prior runs before 6/6/2024)
            // // Remove this note when QADB is updated
            // if(ismc || skipqadb || qa.OkForAsymmetry(run, evn)){
            // def skipqadb = true // Skipping as of 7/2/2024 as I couldn't get the QADB to load (also it hasn't been updated for Pass 2 anyway)
            // if(ismc || skipqadb){
            def skipqadb = false // Reusing the QADB as of 12/16/2025
            if(ismc || skipqadb || qa.pass(run, evn)){

                def canele = ElectronCandidate.getElectronCandidate(0, partb, ecb, ccb, trajb, isinb)
                def ele    = canele.getLorentzVector()
                
                def beamCharge = evb.getFloat("beamCharge", 0)

                if(canele.iselectron()){ // A electron has been found
                    // elec_total_found += 1;
                    
                    int pionCount = 0 // Counter for pions (helps control double-counted electrons)
                    
                    for(int ipart = 1; ipart < partb.getRows(); ipart++){
                        def canpip = PionCandidate.getPionCandidate(ipart, partb, trajb, isinb)
                        
                        if(canpip.ispip()){ // After this 'if' statement, the event being added to the ntuple is known to have at least one electron AND pi+ pion
                            // if(elec_total_found   != elec_num_current){
                            //     elec_events_found += 1;
                            //     elec_num_current   = elec_total_found;
                            // }
                            pionCount += 1; // Increment pion counter
                            
                            def pip0 = canpip.getLorentzVector()
                            
                            // Cartesian Momentum Coordinates
                            def ex = ele.px(),  ey = ele.py(),  ez = ele.pz()
                            def px = pip0.px(), py = pip0.py(), pz = pip0.pz()
                            
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

//                             // Coordinate of the matched hit (Drift Chamber) [cm] - for fiducial cuts - Based on Electron
//                             float ele_x_DC = trajb.getFloat("x", 0)
//                             float ele_y_DC = trajb.getFloat("y", 0)
//                             float ele_z_DC = trajb.getFloat("z", 0)
//                             // Drift Chamber layer
//                             int layer_ele_DC    = trajb.getInt("layer",    0)
//                             // Drift Chamber detector (DC = 6)
//                             int detector_ele_DC = trajb.getInt("detector", 0)
//                             // Coordinate of the matched hit (PCAL) [cm] - for fiducial cuts - Based on Pion
//                             float Hx_pip = ecb.getFloat("hx", ipart)
//                             float Hy_pip = ecb.getFloat("hy", ipart)
//                             // Coordinate of the matched hit (Drift Chamber) [cm] - for fiducial cuts - Based on Pion
//                             float pip_x_DC = trajb.getFloat("x", ipart)
//                             float pip_y_DC = trajb.getFloat("y", ipart)
//                             float pip_z_DC = trajb.getFloat("z", ipart)
//                             // Drift Chamber layer
//                             int layer_pip_DC    = trajb.getInt("layer",    ipart)
//                             // Drift Chamber detector (DC = 6)
//                             int detector_pip_DC = trajb.getInt("detector", ipart)

    //                         // Coordinate of the matched hit (Drift Chamber) [cm] - for fiducial cuts - Based on Pion
    //                         // Called Hx_pip/Hy_pip/Hz_pip for similar referencing to the Hx/Hy/Hz for the PCAL despite the banks/meanings being slightly different (same use - different definition/bank)
    //                         float Hx_pip = trajb.getFloat("x", ipart)
    //                         float Hy_pip = trajb.getFloat("y", ipart)
    //                         float Hz_pip = trajb.getFloat("z", ipart)
    //                         // Drift Chamber layer
    //                         int layer_DC    = trajb.getInt("layer",    ipart)
    //                         // Drift Chamber detector (DC = 6)
    //                         int detector_DC = trajb.getInt("detector", ipart)
                            
                            // if(detector_DC != 6){
                            //     System.out.println("detector_DC != 6");
                            //     System.out.println("Current Total DC:");
                            //     System.out.println(DC_count);
                            //     System.out.println("detector_DC:");
                            //     System.out.println(detector_DC);
                            //     System.out.println("");
                            // }
                            // else{
                            //     DC_count += 1;
                            // }
                            // if(detector_pip_DC == 6){
                            //     DC_count += 1;
                            //     // System.out.println("detector_DC = " + detector_DC);
                            //     // System.out.println("layer_DC    = " + layer_DC);
                            //     // System.out.println("DC_count    = " + DC_count);
                            //     // System.out.println("");
                            // }
//                             else{
//                                 System.out.println("detector_DC != 6");
//                                 System.out.println("detector_DC = " + detector_DC);
//                                 System.out.println("layer_DC    = " + layer_DC);
//                                 System.out.println("DC_count    = " + DC_count);
//                                 System.out.println("");
//                             }
                            
                            // tt.fill(evn, run, ex, ey, ez, px, py, pz,
                            //     esec, pipsec, Hx, Hy, elec_events_found)
                            
                            tt.fill(evn,      run,      beamCharge,        ex, ey, ez,        px, py, pz,
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
                            
                            // Removed on 7/25/2024
                            // tt.fill(evn,     run,    ex,           ey,              ez,           px, py, pz,
                            //         esec,    pipsec, V_PCal,       W_PCal,          U_PCal,
                            //         Hx,      Hy,     ele_x_DC,     ele_y_DC,        ele_z_DC,
                            //         Hx_pip,  Hy_pip, pip_x_DC,     pip_y_DC,        pip_z_DC,
                            //         detector_ele_DC, layer_ele_DC, detector_pip_DC, layer_pip_DC, beamCharge)
                            
                            // tt.fill(evn,    run,    ex,     ey, ez, px, py, pz,
                            //         esec,   pipsec, Hx,     Hy, Hx_pip, Hy_pip, Hz_pip, 
                            //         V_PCal, W_PCal, U_PCal, detector_DC,  layer_DC, beamCharge)
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

// System.out.println("Total Pions in DC:");
// System.out.println(DC_count);
// System.out.println("");

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
