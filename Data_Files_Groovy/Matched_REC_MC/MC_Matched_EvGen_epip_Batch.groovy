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

import org.jlab.clas.pdg.PDGDatabase;
import org.jlab.clas.pdg.PDGParticle;


long StartTime = System.nanoTime()

Sugar.enable()


def isinb = ! ( args[0].contains('outb') || args[0].contains('torus+1') )
def ismc  = args[0].contains("gemc")

def suff  = isinb ? 'inb' : 'outb'
if(ismc) suff += '.mc'
else suff += '.qa'

def outname = args[0].split("/")[-1]

// As of 4/16/2025: Running with files that used a different background merging setting (used 45nA instead of 50nA as was done for all prior runs)
    // Change is only to the output file names - No other changes were made to the internal workings of the script itself
def ff = new ROOTFile("MC_Matching_sidis_epip_richcap.${suff}.new5.45nA.${outname}.root")

// // Test_Rules_New_5 --> added code to check phi matches for edge cases (i.e., if Phi_rec = -179˚ and Phi_gen = +179˚, these particles should be considered as matches)
// def ff = new ROOTFile("MC_Matched_sidis_epip_richcap_Test_Rules_New_5.${suff}.${outname}.root")

// Update as of 6-17-2022 --> Prior versions were erased from the volite folder. Remade with additional information regarding the number of GENERATED events (i.e., how many events would be included if the reconstruction correctly identified every possible SIDIS event in the Monte Carlo - variable named 'SIDIS_GEN')
// SIDIS_GEN will increase over time, so only the maximum value will represent the 'true' number of Generated SIDIS events

// As of 6/10/2024: Removed second best match info and all of the event count information (i.e., Possible_ele, Possible_pip, and SIDIS_GEN)
// // Also added Hx_pip, Hy_pip, Hz_pip and layer_DC

// // Added 'V_PCal', 'W_PCal', 'U_PCal', and 'detector_DC' on 6/12/2024

// // Made the PCal and DC hits, as well as the detector/layer variables unique to each particle on 7/1/2024
//     // Added/renamed several variables to do this (runs with 'new4')

// DC hits had to be separated into 3 values per particle per event (each layer is hit and stored separately within each event) - Updated on 7/24/2024
    // Added/renamed several variables to do this
    // Removed detector/layer info now that it is built into the other variables
    // Runs with 'new5'
    // Also added "Num_Pions" to help control events where the electron is counted twice (in case that is a previously overlooked issue)

// Added 'gStatus' and 'weight' as of 9/12/2025 (EvGen specific variables refering to the radiative state of the photon (0 for non-rad, 55 for ISR, and 56 for FSR) and the variable event weight)
def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:beamCharge:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Num_Pions/I:Hx:Hy:Hx_pip:Hy_pip:V_PCal:W_PCal:U_PCal:ele_x_DC_6:ele_y_DC_6:ele_z_DC_6:ele_x_DC_18:ele_y_DC_18:ele_z_DC_18:ele_x_DC_36:ele_y_DC_36:ele_z_DC_36:pip_x_DC_6:pip_y_DC_6:pip_z_DC_6:pip_x_DC_18:pip_y_DC_18:pip_z_DC_18:pip_x_DC_36:pip_y_DC_36:pip_z_DC_36:ex_gen:ey_gen:ez_gen:eE_gen:PID_el:pipx_gen:pipy_gen:pipz_gen:pipE_gen:PID_pip:gStatus:weight')

// If print_extra_info = 1, then extra information will be printed while running this program (do not do unless trying to test certain information - will run less efficiently)
// Let print_extra_info = 0 to run normally
print_extra_info = 0

def num_of_failed_ele = 0
def num_of_failed_pip = 0


def num_of_total_matched = 0

// num_of_double_matches = number of times both reconstucted particles are matched to the same generated particle
def num_of_double_matches = 0

// num_of_gen_sidis_events = number of generated events 
def num_of_gen_sidis_events = 0

def num_of_yesbs_fail = 0
def num_of_rec_ele_candidates = 0
def num_of_rec_pip_candidates = 0
def num_of_rec_ele_found = 0
def num_of_rec_pip_found = 0

def Multiple_Pions_Per_Electron = 0

GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    // QADB qa = new QADB()
    
    def reader    = new HipoReader()
    reader.open(fname)
    def event     = new Event()
    def factory   = reader.getSchemaFactory()
    
    // def schemas   = ['RUN::config', 'REC::Event', 'REC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator', 'MC::Header', 'MC::Particle'].collect{factory.getSchema(it)}
    // def banks     = schemas.collect{new Bank(it)}
    // // For counting the number of generated events using the same methods as were used in the GEN files for acceptance corrections
    // def banks_gen = ['MC::Header',  'REC::Event', 'MC::Particle',  'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator'].collect{new Bank(factory.getSchema(it))}
    
    def schemas     = ['RUN::config', 'REC::Event', 'REC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator', 'MC::Particle', 'MC::Event'].collect{factory.getSchema(it)}
    def banks       = schemas.collect{new Bank(it)}

    def schemas_gen = ['REC::Event', 'MC::Particle',  'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator'].collect{factory.getSchema(it)}
    def banks_gen   = schemas_gen.collect{new Bank(it)}

    //==============================================//
    //==========//   Event Loop Start   //==========//
    //==============================================//
    while(reader.hasNext()) {
        reader.nextEvent(event)

        //===================================================================================================//
        //==========//   Getting Current Number of Generated Events as of the given event loop   //==========//
        // banks_gen.each{event.read(it)}
        // if(banks_gen.every()) {
        if(event.hasBanks(schemas_gen)){
            banks_gen.each{event.read(it)}
            
            // def (runb_gen, evb_gen, partb_gen, ecb_gen, ccb_gen, trajb_gen, scb_gen) = banks_gen
            def (evb_gen, partb_gen, ecb_gen, ccb_gen, trajb_gen, scb_gen) = banks_gen
            def pid_el_gen     = partb_gen.getInt("pid",     0)
            if(pid_el_gen == 11){
                // There is a generated electron
                for(int ipart = 1; ipart < partb_gen.getRows(); ipart++){
                    def pid_pip_gen = partb_gen.getInt("pid", ipart)
                    if(pid_pip_gen == 211){ // There is a generated Pi+
                        num_of_gen_sidis_events += 1
                    }
                }
            }
        }
        //==========//   Getting Current Number of Generated Events as of the given event loop   //==========//
        //===================================================================================================//
        
        // def yesbs = schemas.collect{event.scan(it.getGroup(), it.getItem()) > 0}
        // if(yesbs.every()){
        // if(true){
        if(event.hasBanks(schemas)){
            
            banks.each{event.read(it)}

            // def (runb, evb, partb, ecb, ccb, trajb, scb, MChead, MCpart) = banks
            def (runb, evb, partb, ecb, ccb, trajb, scb, MCpart, mcE) = banks
            
            def run            = runb.getInt("run",      0)
            def evn            = runb.getInt("event",    0)
            def Rad            = mcE.getInt("processid", 0)
            def wgt            = mcE.getFloat("weight",  0)
            
            if(print_extra_info == 1){
                System.out.println("processid = " + Rad);
                System.out.println("weight = " + wgt);
            }
            
            def canele         = ElectronCandidate.getElectronCandidate(0, partb, ecb, ccb, trajb, isinb)
            def ele            = canele.getLorentzVector()
            
            def beamCharge     = evb.getFloat("beamCharge", 0)
            
            num_of_rec_ele_candidates += 1;
            //==================================================//
            //==========//   Electron (REC) Found   //==========//
            //==================================================//
            if(canele.iselectron()){
                // A RECONSTRUCTED electron has been found
                num_of_rec_ele_found += 1;
                
                // These lists are to make sure that the same generated particles are not matched to multiple reconstructed particles
                // Applies mainly to the pi+ pion as the same electron should be matched several times while searching for the pions
                // The electron list is included in case the electron is matched to different particles within the same event (room for future improvement to remove unnecessary searching later)
                def list_of_matched_particles_gen_pip = []
                def list_of_matched_particles_gen_ele = []
                
                int pionCount = 0 // Counter for pions (helps control double-counted electrons)
                
                //=====================================================//
                //==========//   Start of Pi+ (REC) Loop   //==========//
                //=====================================================//
                for(int ipart = 1; ipart < partb.getRows(); ipart++){
                    
                    def canpip = PionCandidate.getPionCandidate(ipart, partb, trajb, isinb)
                    num_of_rec_pip_candidates += 1;

                    //==================================================//
                    //==========//   Pi+ Pion (REC) Found   //==========//
                    //==================================================//
                    if(canpip.ispip()){
                        // A RECONSTRUCTED pi+ particle has been found with the given electron
                        // After this 'if' statement, the event being added to the ntuple is known to have at least one RECONSTRUCTED electron AND pi+ pion
                        num_of_rec_pip_found += 1;
                        pionCount += 1; // Increment pion counter

                        def pip0 = canpip.getLorentzVector()

                        //========================================================//
                        //==========// Reconstructed Info to be Saved //==========//
                        
                        // Cartesian Momentum Coordinates
                        def ex   = ele.px(),    ey = ele.py(),    ez = ele.pz()
                        def pipx = pip0.px(), pipy = pip0.py(), pipz = pip0.pz()
                        
                        // Sectors (From Detector)
                        def esec = canele.getPCALsector(),    pipsec = canpip.getDCsector()
                        
                        // Coordinate of the matched hit (PCAL) [cm] - for Valerii's cuts (done in python) - Based on Electron
                        float Hx = ecb.getFloat("hx", 0)
                        float Hy = ecb.getFloat("hy", 0)
                        
                        // For other valerii cuts
                        // int detector_PCal = ecb.getInt("detector", 0)
                        // int layer_PCal    = ecb.getInt("layer",    0)
                        float V_PCal = ecb.getFloat("lv", 0)
                        float W_PCal = ecb.getFloat("lw", 0)
                        float U_PCal = ecb.getFloat("lu", 0)
                        
                        
                        // Coordinate of the matched hit (Drift Chamber) [cm] - for fiducial cuts - Based on Electron - for layers 6, 18, and 36 (i.e., regions 1, 2, and 3)
                        // float ele_x_DC_6  = canele.getDC1x()
                        // float ele_y_DC_6  = canele.getDC1y()
                        // float ele_z_DC_6  = canele.getDC1z()
                        // // Note regarding why getDC() functions aren't used: Only getDC1x(), getDC1y(), getDC1z() exist. The other layers do not have defined functions to retrieve them
                        // float ele_x_DC_18 = canele.getDC2x()
                        // float ele_y_DC_18 = canele.getDC2y()
                        // float ele_z_DC_18 = canele.getDC2z()
                        // float ele_x_DC_36 = canele.getDC3x()
                        // float ele_y_DC_36 = canele.getDC3y()
                        // float ele_z_DC_36 = canele.getDC3z()
                        
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
                        
                        // float ele_x_DC = trajb.getFloat("x", 0)
                        // float ele_y_DC = trajb.getFloat("y", 0)
                        // float ele_z_DC = trajb.getFloat("z", 0)
                        // // Drift Chamber layer
                        // int layer_ele_DC    = trajb.getInt("layer",    0)
                        // // Drift Chamber detector (DC = 6)
                        // int detector_ele_DC = trajb.getInt("detector", 0)
                        
                        
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
                        
                        // Coordinate of the matched hit (Drift Chamber) [cm] - for fiducial cuts - Based on Pion
                        // float pip_x_DC_6  = canpip.getDC1x()
                        // float pip_y_DC_6  = canpip.getDC1y()
                        // float pip_z_DC_6  = canpip.getDC1z()
                        // // Note regarding why getDC() functions aren't used: Only getDC1x(), getDC1y(), getDC1z() exist. The other layers do not have defined functions to retrieve them
                        // float pip_x_DC_18 = canpip.getDC2x()
                        // float pip_y_DC_18 = canpip.getDC2y()
                        // float pip_z_DC_18 = canpip.getDC2z()
                        // float pip_x_DC_36 = canpip.getDC3x()
                        // float pip_y_DC_36 = canpip.getDC3y()
                        // float pip_z_DC_36 = canpip.getDC3z()
                        
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
                        
                        // // Coordinate of the matched hit (PCAL) [cm] - for fiducial cuts - Based on Pion
                        // float Hx_pip = ecb.getFloat("hx", ipart)
                        // float Hy_pip = ecb.getFloat("hy", ipart)
                        // // Coordinate of the matched hit (Drift Chamber) [cm] - for fiducial cuts - Based on Pion
                        // float pip_x_DC = trajb.getFloat("x", ipart)
                        // float pip_y_DC = trajb.getFloat("y", ipart)
                        // float pip_z_DC = trajb.getFloat("z", ipart)
                        // // Drift Chamber layer
                        // int layer_pip_DC    = trajb.getInt("layer",    ipart)
                        // // Drift Chamber detector (DC = 6)
                        // int detector_pip_DC = trajb.getInt("detector", ipart)

                        // // Coordinate of the matched hit (Drift Chamber) [cm] - for fiducial cuts - Based on Pion
                        // // Called Hx_pip/Hy_pip/Hz_pip for similar referencing to the Hx/Hy/Hz for the PCAL despite the banks/meanings being slightly different (same use - different definition/bank)
                        // float Hx_pip = trajb.getFloat("x", ipart)
                        // float Hy_pip = trajb.getFloat("y", ipart)
                        // float Hz_pip = trajb.getFloat("z", ipart)
                        // // Drift Chamber layer
                        // int layer_DC    = trajb.getInt("layer",    ipart)
                        // // Drift Chamber detector (DC = 6)
                        // int detector_DC = trajb.getInt("detector", ipart)
                        
                        //==========// Reconstructed Info to be Saved //==========//
                        //========================================================//
                        
                        // Spherical Momentum Coordinates
                        def el     = ele.p()
                        def elth   = (180/3.1415926)*ele.theta()
                        def elPhi  = (180/3.1415926)*ele.phi()
                        def pip    = pip0.p()
                        def pipth  = (180/3.1415926)*pip0.theta()
                        def pipPhi = (180/3.1415926)*pip0.phi()
                        
                        // After this line, a proper reconstructed ep->epi+X SIDIS event has been found. The following lines will aim to match these particles to their generated counterparts
                        if(print_extra_info == 1){
                            System.out.println("For event: " + evn);
                            System.out.println("Number of (gen) rows: " + MCpart.getRows());
                        }
                        
                        // Below are the main angular matching criteria for both particles
                        def Phi_Ele_Criteria   = 10;
                        def Theta_Ele_Criteria = 6;
                        def Phi_Pip_Criteria   = 10;
                        def Theta_Pip_Criteria = 6;
                        
                        def Best_ele_Match = 1000;
                        def Best_pip_Match = 1000;
                        
                        def Next_Best_ele_Match = 1000;
                        def Next_Best_pip_Match = 1000;
                        
                        def num_of_possible_ele_matches = 0
                        def pid_matched_el   = 0
                        def matched_el_x_gen = 0
                        def matched_el_y_gen = 0
                        def matched_el_z_gen = 0
                        def matched_el_E_gen = 0
                        
                        def num_of_possible_pip_matches = 0
                        def pid_matched_pip   = 0
                        def matched_pip_x_gen = 0
                        def matched_pip_y_gen = 0
                        def matched_pip_z_gen = 0
                        def matched_pip_E_gen = 0
                        
                        def pid_other_matched_el   = 0
                        def other_matched_el_x_gen = 0
                        def other_matched_el_y_gen = 0
                        def other_matched_el_z_gen = 0
                        def other_matched_el_E_gen = 0
                        
                        def pid_other_matched_pip   = 0
                        def other_matched_pip_x_gen = 0
                        def other_matched_pip_y_gen = 0
                        def other_matched_pip_z_gen = 0
                        def other_matched_pip_E_gen = 0
                        
                        def current_match_pip     = []
                        def current_2nd_match_pip = []
                        def current_match_ele     = []
                        def current_2nd_match_ele = []
                        
                        //====================================================================================================//
                        //----------------------------------------------------------------------------------------------------//
                        //==========||==========||==========// Matching to Generated Loop //==========||==========||==========//
                        //----------------------------------------------------------------------------------------------------//
                        //====================================================================================================//
                        for(int ii_MCpart = 0; ii_MCpart < MCpart.getRows(); ii_MCpart++){
                            // This loop is to go through each particle in the event to find the generated match for the reconstucted particles above
                            
                            def pid_unmatched     = MCpart.getInt("pid",  ii_MCpart)
                            def unmatched_x_gen   = MCpart.getFloat("px", ii_MCpart)
                            def unmatched_y_gen   = MCpart.getFloat("py", ii_MCpart)
                            def unmatched_z_gen   = MCpart.getFloat("pz", ii_MCpart)
                            def unmatched_vec_gen = LorentzVector.withPID(pid_unmatched, unmatched_x_gen, unmatched_y_gen, unmatched_z_gen)
                            
                            if(print_extra_info == 1){
                                System.out.println("Particle in row " + ii_MCpart + " has PID= " + pid_unmatched);
                            }
                            
                            def unmatched_p   = unmatched_vec_gen.p()
                            def unmatched_th  = (180/3.1415926)*unmatched_vec_gen.theta()
                            def unmatched_Phi = (180/3.1415926)*unmatched_vec_gen.phi()
                            def unmatched_charge_gen = (PDGDatabase.getParticleById(pid_unmatched)).charge()
                            
                            //------------------------------------------------------------------------------------------------------//
                            //==========||==========||==========// ELECTRON MATCHING CONDITIONS //==========||==========||==========//
                            //------------------------------------------------------------------------------------------------------//
                            if(unmatched_charge_gen == -1){ //=====// Condition 1: Charge is matched for the Electron //=====//
                                
                                //===============// (Other) Matching Conditions for Electron //===============//

                                def Delta_el_p   = Math.abs(el    - unmatched_p);
                                def Delta_el_th  = Math.abs(elth  - unmatched_th);
                                def Delta_el_Phi = Math.abs(elPhi - unmatched_Phi);
                                
                                // These lines are to account for the phi-distribution's natural discontinuity (i.e., The maximum difference between phi angles is 180˚. Beyond that, the angles become smaller when measured in the opposite direction. Since phi is naturally measured from ±180˚, a measurement of -179˚ and +179˚ should only be 2˚ apart, not 358˚)
                                if(Delta_el_Phi > 180){
                                    Delta_el_Phi += -360;
                                    Delta_el_Phi  = Math.abs(Delta_el_Phi);
                                }
                                
                                // def Total_Quality_of_Match = Delta_el_th + Delta_el_Phi;
                                
                                // Used for rules 3:
                                // def Total_Quality_of_Match = ((Math.abs(Delta_el_p))/(Math.abs(el))) + ((Math.abs(Delta_el_th))/(Math.abs(elth))) + ((Math.abs(Delta_el_Phi))/(Math.abs(elPhi)));
                                
                                // Used for rules 4: (also with better 2nd match recording)
                                def Total_Quality_of_Match = ((Math.abs(Delta_el_th))/(Math.abs(elth))) + ((Math.abs(Delta_el_Phi))/(Math.abs(elPhi)));
                                                                
                                //=========================================//
                                //=====// Primary Matching Criteria //=====//
                                //=========================================//
                                
                                // if(Delta_el_th < 2 && Delta_el_Phi < 6){
                                // if(Delta_el_th < 5 && Delta_el_Phi < 9){ // Testing an increased matching criteria range
                                // if(Delta_el_th < 6 && Delta_el_Phi < 10){ // Testing an increased matching criteria range (TEST 2)
                                
                                if(Delta_el_Phi < Phi_Ele_Criteria && Delta_el_th < Theta_Ele_Criteria){ // Matching Criteria (defined above)
                                    // Particle can be matched to the Electron
                                    num_of_possible_ele_matches += 1;
                                    if(Best_ele_Match > Total_Quality_of_Match){
                                        // These lines were added on 4-26-2022 (Not run before "Rules_3")
                                        // Check to see if this match is replacing a better match, or is the first (good) match
                                        //========================================//
                                        //=====// Secondary Particle Match //=====//
                                        //========================================//
                                        if((Total_Quality_of_Match < Next_Best_ele_Match) && (Next_Best_ele_Match != 1000) && (Best_ele_Match != 1000)){
                                            // Replace next best match with the match that is currently about to be replaced
                                            Next_Best_ele_Match = Best_ele_Match;

                                            pid_other_matched_el   = pid_matched_el;
                                            other_matched_el_x_gen = matched_el_x_gen;
                                            other_matched_el_y_gen = matched_el_y_gen;
                                            other_matched_el_z_gen = matched_el_z_gen;
                                            other_matched_el_E_gen = matched_el_E_gen;

                                            current_2nd_match_ele  = current_match_ele
                                        }
                                        //========================================//
                                        //=====// Secondary Particle Match //=====//
                                        //========================================//
                                        
                                        //======================================//
                                        //=====// Primary Particle Match //=====//
                                        //======================================//
                                        
                                        // Current match is the closest one to the reconstructed
                                        Best_ele_Match = Total_Quality_of_Match;

                                        if(pid_matched_el == 11 && pid_matched_el != pid_unmatched && print_extra_info == 1){
                                            System.out.println("Particle that is not an electron is considered a better match than an identified electron."); 
                                        }

                                        pid_matched_el    = pid_unmatched;
                                        matched_el_x_gen  = unmatched_x_gen;
                                        matched_el_y_gen  = unmatched_y_gen;
                                        matched_el_z_gen  = unmatched_z_gen;
                                        matched_el_E_gen  = unmatched_vec_gen.e();
                                        
                                        current_match_ele = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]
                                        // current_match_ele = ["row of match", "PID of match candidate", "Theta angle of match candidate", "Phi angle of match candidate"]

                                        //======================================//
                                        //=====// Primary Particle Match //=====//
                                        //======================================//
                                    }
                                }
                                
                                //========================================//
                                //=====// Secondary Particle Match //=====//
                                //========================================//
                                
                                if((Total_Quality_of_Match > Best_ele_Match && Total_Quality_of_Match < Next_Best_ele_Match) || Next_Best_ele_Match == 1000){
                                    // Always have a 'next best' result (must still have the correct charge)
                                    Next_Best_ele_Match = Total_Quality_of_Match;
                                    
                                    pid_other_matched_el   = pid_unmatched;
                                    other_matched_el_x_gen = unmatched_x_gen;
                                    other_matched_el_y_gen = unmatched_y_gen;
                                    other_matched_el_z_gen = unmatched_z_gen;
                                    other_matched_el_E_gen = unmatched_vec_gen.e();
                                    
                                    current_2nd_match_ele  = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]   
                                }
                                //===============// (Other) Matching Conditions for Electron //===============//
                            }
                            //------------------------------------------------------------------------------------------------------//
                            //==========||==========||==========// ELECTRON MATCHING CONDITIONS //==========||==========||==========//
                            //------------------------------------------------------------------------------------------------------//
                            
                            
                            //------------------------------------------------------------------------------------------------------//
                            //==========||==========||==========// PI+ PION MATCHING CONDITIONS //==========||==========||==========//
                            //------------------------------------------------------------------------------------------------------//
                            if(unmatched_charge_gen == 1){ //=====// Condition 1: Charge is matched for the Pi+ Pion //=====//
                                
                                //=====// Condition 2: Particle has not already been matched //=====//
                                if((list_of_matched_particles_gen_pip.isEmpty()) || (list_of_matched_particles_gen_pip.contains([ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]) == false)){
                                    // Condition above: WILL check the generated particle if there has not been another pion added to the dataframe for this event yet
                                                    //  Will NOT check this particle if it had previously been matched to a different reconstructed pion
                                    
                                    //===============// (Other) Matching Conditions for Pi+ Pion //===============//

                                    def Delta_pip_p   = Math.abs(pip    - unmatched_p);
                                    def Delta_pip_th  = Math.abs(pipth  - unmatched_th);
                                    def Delta_pip_Phi = Math.abs(pipPhi - unmatched_Phi);
                                    
                                    // These lines are to account for the phi-distribution's natural discontinuity (i.e., The maximum difference between phi angles is 180˚. Beyond that, the angles become smaller when measured in the opposite direction. Since phi is naturally measured from ±180˚, a measurement of -179˚ and +179˚ should only be 2˚ apart, not 358˚)
                                    if(Delta_pip_Phi > 180){
                                        Delta_pip_Phi += -360;
                                        Delta_pip_Phi  = Math.abs(Delta_pip_Phi);
                                    }

                                    // def Total_Quality_of_Match = Delta_pip_th + Delta_pip_Phi;
                                    
                                    // Used for rules 3:
                                    // def Total_Quality_of_Match = ((Math.abs(Delta_pip_p))/(Math.abs(pip))) + ((Math.abs(Delta_pip_th))/(Math.abs(pipth))) + ((Math.abs(Delta_pip_Phi))/(Math.abs(pipPhi)));
                                    
                                    // Used for rules 4: (also with better 2nd match recording)
                                    def Total_Quality_of_Match = ((Math.abs(Delta_pip_th))/(Math.abs(pipth))) + ((Math.abs(Delta_pip_Phi))/(Math.abs(pipPhi)));
                                    
                                    // if(Delta_pip_th < 2 && Delta_pip_Phi < 6){
                                    // if(Delta_pip_th < 5 && Delta_pip_Phi < 9){ // Testing an increased matching criteria range
                                    // if(Delta_pip_th < 6 && Delta_pip_Phi < 10){ // Testing an increased matching criteria range (TEST 2)
                                        
                                    if(Delta_pip_Phi < Phi_Pip_Criteria && Delta_pip_th < Theta_Pip_Criteria){ // Matching Criteria (defined above)
                                        // Particle can be matched to the Pi+ Pion
                                        
                                        num_of_possible_pip_matches += 1;

                                        if(Best_pip_Match > Total_Quality_of_Match){
                                            // These lines were added on 4-26-2022 (Not run before "Rules_3")
                                            // Check to see if this match is replacing a better match, or is the first (good) match
                                            //========================================//
                                            //=====// Secondary Particle Match //=====//
                                            //========================================//
                                            if((Total_Quality_of_Match < Next_Best_pip_Match) && (Next_Best_pip_Match != 1000) && (Best_pip_Match != 1000)){
                                                // Replace next best match with the match that is currently about to be replaced
                                                Next_Best_pip_Match = Best_pip_Match;

                                                pid_other_matched_pip   = pid_matched_pip;
                                                other_matched_pip_x_gen = matched_pip_x_gen;
                                                other_matched_pip_y_gen = matched_pip_y_gen;
                                                other_matched_pip_z_gen = matched_pip_z_gen;
                                                other_matched_pip_E_gen = matched_pip_E_gen;

                                                current_2nd_match_pip   = current_match_pip
                                            }
                                            //========================================//
                                            //=====// Secondary Particle Match //=====//
                                            //========================================//

                                            //======================================//
                                            //=====// Primary Particle Match //=====//
                                            //======================================//

                                            // Current match is the closest one to the reconstructed
                                            Best_pip_Match = Total_Quality_of_Match;

                                            if(pid_matched_pip == 211 && pid_matched_pip != pid_unmatched && print_extra_info == 1){
                                                System.out.println("Particle that is not a pi+ pion is considered a better match than an identified pi+ pion."); 
                                            }
                                            pid_matched_pip   = pid_unmatched;
                                            matched_pip_x_gen = unmatched_x_gen;
                                            matched_pip_y_gen = unmatched_y_gen;
                                            matched_pip_z_gen = unmatched_z_gen;
                                            matched_pip_E_gen = unmatched_vec_gen.e();

                                            current_match_pip = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]
                                            //  current_match_pip = ["row of match", "PID of match candidate", "Theta angle of match candidate", "Phi angle of match candidate"]
                                        }
                                    }
                                    if((Total_Quality_of_Match > Best_pip_Match && Total_Quality_of_Match < Next_Best_pip_Match) || Next_Best_pip_Match == 1000){
                                        // Always have a 'next best' result (must still have the correct charge)                                    
                                        Next_Best_pip_Match = Total_Quality_of_Match;

                                        pid_other_matched_pip   = pid_unmatched;
                                        other_matched_pip_x_gen = unmatched_x_gen;
                                        other_matched_pip_y_gen = unmatched_y_gen;
                                        other_matched_pip_z_gen = unmatched_z_gen;
                                        other_matched_pip_E_gen = unmatched_vec_gen.e();

                                        current_2nd_match_pip   = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]
                                    }
                                    //===============// (Other) Matching Conditions for Pi+ Pion //===============//
                                }
                            }
                            //------------------------------------------------------------------------------------------------------//
                            //==========||==========||==========// PI+ PION MATCHING CONDITIONS //==========||==========||==========//
                            //------------------------------------------------------------------------------------------------------//
                        }
                        //==========================================================================================================//
                        //----------------------------------------------------------------------------------------------------------//
                        //==========||==========||==========// Matching to Generated Loop (END) //==========||==========||==========//
                        //----------------------------------------------------------------------------------------------------------//
                        //==========================================================================================================//
                            
                        
                        
                        //--------------------------------------------------------//
                        //====================// Print Info //====================//
                        //--------------------------------------------------------//
                            
                        //==========// Checking to see if particles were matched (Start) //==========//
                        if(pid_matched_el == 0 && matched_el_x_gen == 0 && matched_el_y_gen == 0 && matched_el_z_gen == 0){
                            num_of_failed_ele += 1
                            if(print_extra_info == 1){
                                System.out.println("FAILED to match the electron. (Failure Number: " + num_of_failed_ele + ")");
                                System.out.println("Event Number is: " + evn);
                                System.out.println("Run Number is: "   + run);
                            }
                        }
                        
                        if(pid_matched_pip == 0 && matched_pip_x_gen == 0 && matched_pip_y_gen == 0 && matched_pip_z_gen == 0){
                            num_of_failed_pip += 1
                            if(print_extra_info == 1){
                                System.out.println("FAILED to match the pi+ pion. (Failure Number: " + num_of_failed_pip + ")");
                                System.out.println("Event Number is: " + evn);
                                System.out.println("Run Number is: " + run);
                            }
                        }
                        
                        //=====// Found a matched particle //=====//
                        if(pid_matched_el != 0 && matched_el_x_gen != 0 && matched_el_y_gen != 0 && matched_el_z_gen != 0 && pid_matched_pip != 0 && matched_pip_x_gen != 0 && matched_pip_y_gen != 0 && matched_pip_z_gen != 0){
                            num_of_total_matched += 1
                        }
                        //=====// Found a matched particle //=====//
                        
                        //==========// Checking to see if particles were matched (End) //==========//
                        
                        //===============// Matching Both Particles at the same time //===============//

                        if(pid_matched_el == pid_matched_pip && matched_el_x_gen == matched_pip_x_gen && matched_el_y_gen == matched_pip_y_gen && matched_el_z_gen == matched_pip_z_gen){
                            if(pid_matched_el == 0 && matched_el_x_gen == 0 && matched_el_y_gen == 0 && matched_el_z_gen == 0){
                                if(print_extra_info == 1){
                                    System.out.println("Failure to match either particle");
                                }
                            }
                            else{
                                num_of_double_matches += 1
                                
                                if(print_extra_info == 1){
                                    System.out.println("Rare case of both particles being matched at the same time has been found");
                                    System.out.println("Event Number is: " + evn);
                                    System.out.println("Run Number is: " + run);
                                }
                            }
                        }
                        //===============// Matching Both Particles at the same time //===============//
                        
                        //--------------------------------------------------------//
                        //====================// Print Info //====================//
                        //--------------------------------------------------------//
                        
                        list_of_matched_particles_gen_pip.add(current_match_pip)
                        
                        if(list_of_matched_particles_gen_ele.isEmpty()){
                            list_of_matched_particles_gen_ele.add(current_match_ele)
                        }
                        else{
                            if((list_of_matched_particles_gen_ele.contains(current_match_ele) == false) && print_extra_info == 1){
                                System.out.println("Multiple electrons have been matched to the same event");
                                System.out.println("Event Number is: " + evn);
                                System.out.println("Run Number is: " + run);
                                System.out.println("The list of electrons are: " + list_of_matched_particles_gen_ele);
                                
                            }
                            
                        }




                        tt.fill(evn,      run,      beamCharge,        ex, ey, ez,        pipx, pipy, pipz,
                                esec,     pipsec,   pionCount,         Hx, Hy, Hx_pip,    Hy_pip,
                                V_PCal,             W_PCal,            U_PCal, 
                                ele_x_DC_6,         ele_y_DC_6,        ele_z_DC_6,
                                ele_x_DC_18,        ele_y_DC_18,       ele_z_DC_18,
                                ele_x_DC_36,        ele_y_DC_36,       ele_z_DC_36,
                                pip_x_DC_6,         pip_y_DC_6,        pip_z_DC_6,
                                pip_x_DC_18,        pip_y_DC_18,       pip_z_DC_18,
                                pip_x_DC_36,        pip_y_DC_36,       pip_z_DC_36,
                                matched_el_x_gen,   matched_el_y_gen,  matched_el_z_gen,  matched_el_E_gen,  pid_matched_el,
                                matched_pip_x_gen,  matched_pip_y_gen, matched_pip_z_gen, matched_pip_E_gen, pid_matched_pip,
                                Rad, wgt)
                        
                        if(pionCount > 1){
                            Multiple_Pions_Per_Electron += 1
                        }

                        // Removed on 7/24/2024
                        // tt.fill(evn,     run,      ex,                ey,                ez,                pipx, pipy, pipz,
                        //         esec,    pipsec,   V_PCal,            W_PCal,            U_PCal,
                        //         Hx,      Hy,       ele_x_DC,          ele_y_DC,          ele_z_DC,
                        //         Hx_pip,  Hy_pip,   pip_x_DC,          pip_y_DC,          pip_z_DC,
                        //         detector_ele_DC,   layer_ele_DC,      detector_pip_DC,   layer_pip_DC,      beamCharge,
                        //         matched_el_x_gen,  matched_el_y_gen,  matched_el_z_gen,  matched_el_E_gen,  pid_matched_el,
                        //         matched_pip_x_gen, matched_pip_y_gen, matched_pip_z_gen, matched_pip_E_gen, pid_matched_pip)
                        
                        // Removed on 6/6/2024
                        // tt.fill(evn, run, ex, ey, ez, pipx, pipy, pipz,
                        //     esec, pipsec, Hx, Hy,
                        //     matched_el_x_gen,  matched_el_y_gen,  matched_el_z_gen,  matched_el_E_gen,  pid_matched_el,
                        //     matched_pip_x_gen, matched_pip_y_gen, matched_pip_z_gen, matched_pip_E_gen, pid_matched_pip,
                        //     other_matched_el_x_gen,  other_matched_el_y_gen,  other_matched_el_z_gen,  other_matched_el_E_gen,  pid_other_matched_el,
                        //     other_matched_pip_x_gen, other_matched_pip_y_gen, other_matched_pip_z_gen, other_matched_pip_E_gen, pid_other_matched_pip,
                        //     num_of_possible_ele_matches, num_of_possible_pip_matches, num_of_gen_sidis_events, beamCharge)
                        // Removed on 7/1/2024
                        // tt.fill(evn, run, ex,  ey, ez, pipx, pipy, pipz,
                        //     esec, pipsec, Hx,  Hy, Hx_pip, Hy_pip, Hz_pip, 
                        //     V_PCal,   W_PCal,  U_PCal,             detector_DC,       layer_DC,          beamCharge,
                        //     matched_el_x_gen,  matched_el_y_gen,   matched_el_z_gen,  matched_el_E_gen,  pid_matched_el,
                        //     matched_pip_x_gen, matched_pip_y_gen,  matched_pip_z_gen, matched_pip_E_gen, pid_matched_pip)
                        
                        // if(pid_matched_el  != 0 && pid_matched_el  != 11  && pid_matched_el  != -321 && pid_matched_el  != -211){
                        //     System.out.println("Incorrect Electron PID");
                        //     System.out.println("Matched PID_el  = " + pid_matched_el);
                        // }
                        // if(pid_matched_pip != 0 && pid_matched_pip != 211 && pid_matched_pip != 2212 && pid_matched_pip !=  321 && pid_matched_pip != -11){
                        //     System.out.println("Incorrect Pi+ Pion PID");
                        //     System.out.println("Matched PID_pip = " + pid_matched_pip);
                        // }
                        // if((pid_matched_el != 0 && pid_matched_el  != 11) || (pid_matched_pip != 0 && pid_matched_pip != 211)){
                        //     System.out.println("");
                        // }
                    }
                    //==================================================//
                    //==========//   Pi+ Pion (REC) Found   //==========//
                    //==================================================//
                    
                }
                //===================================================//
                //==========//   End of Pi+ (REC) Loop   //==========//
                //===================================================//
                
            }
            //==================================================//
            //==========//   Electron (REC) Found   //==========//
            //==================================================//
            
        }
        else{
            num_of_yesbs_fail += 1;
            // System.out.println("yesbs.every() Failed");
        }
        
    }
    //============================================//
    //==========//   Event Loop End   //==========//
    //============================================//

    reader.close()
    
}
}

System.out.println("");

System.out.println("Total number of completly matched events = " + num_of_total_matched);

System.out.println("Total number of failed Electron matches  = " + num_of_failed_ele);
System.out.println("Total number of failed Pi+ Pion matches  = " + num_of_failed_pip);

System.out.println("Number of times the reconstructed particles are matched to the same generated particle = " + num_of_double_matches);

System.out.println("");

System.out.println("Total number of generated events = " + num_of_gen_sidis_events);

System.out.println("Number of Reconstructed Electron candidates = " + num_of_rec_ele_candidates);
System.out.println("Number of Reconstructed Electron found      = " + num_of_rec_ele_found);
System.out.println("Number of Reconstructed Pi+ Pion candidates = " + num_of_rec_pip_candidates);
System.out.println("Number of Reconstructed Pi+ Pion found      = " + num_of_rec_pip_found);
System.out.println("");
System.out.println("Number of times that Multiple Pions were found per Electron = " + Multiple_Pions_Per_Electron);
System.out.println("");
System.out.println("Total number of failed yesbs.every() conditions  = " + num_of_yesbs_fail);

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

