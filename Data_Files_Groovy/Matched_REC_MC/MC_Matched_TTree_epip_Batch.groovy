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

import org.jlab.clas.pdg.PDGDatabase;
import org.jlab.clas.pdg.PDGParticle;


long StartTime = System.nanoTime()

Sugar.enable()


def isinb = ! ( args[0].contains('outb') || args[0].contains('torus+1') )
def ismc = args[0].contains("gemc")

def suff = isinb ? 'inb' : 'outb'
if(ismc) suff += '.mc'
else suff += '.qa'

def outname = args[0].split("/")[-1]
// New Naming convension as of 7-18-2022 (same as Test_Rules_New_5)
def ff = new ROOTFile("MC_Matching_sidis_epip_richcap.${suff}.${outname}.root")



// // Test_Rules_New_5 --> added code to check phi matches for edge cases (i.e., if Phi_rec = -179˚ and Phi_gen = +179˚, these particles should be considered as matches)
// def ff = new ROOTFile("MC_Matched_sidis_epip_richcap_Test_Rules_New_5.${suff}.${outname}.root")



// Update as of 6-17-2022 --> Prior versions were erased from the volite folder. Remade with additional information regarding the number of GENERATED events (i.e., how many events would be included if the reconstruction correctly identified every possible SIDIS event in the Monte Carlo - variable named 'SIDIS_GEN')
// SIDIS_GEN will increase over time, so only the maximum value will represent the 'true' number of Generated SIDIS events



// def tt = ff.makeTree('h22','title','event/I:runN/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Hx:Hy:ex_gen:ey_gen:ez_gen:eE_gen:PID_el:pipx_gen:pipy_gen:pipz_gen:pipE_gen:PID_pip:ex_2_gen:ey_2_gen:ez_2_gen:eE_2_gen:PID_2_el:pipx_2_gen:pipy_2_gen:pipz_2_gen:pipE_2_gen:PID_2_pip:Possible_ele/I:Possible_pip/I')
def tt = ff.makeTree('h22','title','event/I:runN/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Hx:Hy:ex_gen:ey_gen:ez_gen:eE_gen:PID_el:pipx_gen:pipy_gen:pipz_gen:pipE_gen:PID_pip:ex_2_gen:ey_2_gen:ez_2_gen:eE_2_gen:PID_2_el:pipx_2_gen:pipy_2_gen:pipz_2_gen:pipE_2_gen:PID_2_pip:Possible_ele/I:Possible_pip/I:SIDIS_GEN/I')



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

GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    QADB qa = new QADB()
    

    def reader = new HipoReader()
    reader.open(fname)
    def event = new Event()
    def factory = reader.getSchemaFactory()
    
    
    def schemas = ['RUN::config', 'REC::Event', 'REC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator', 'MC::Header', 'MC::Particle'].collect{factory.getSchema(it)}
    def banks = schemas.collect{new Bank(it)}
    
    // For counting the number of generated events using the same methods as were used in the GEN files for acceptance corrections
    def banks_gen = ['MC::Header', 'REC::Event', 'MC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator'].collect{new Bank(factory.getSchema(it))}

    
    //==============================================//
    //==========//   Event Loop Start   //==========//
    //==============================================//
    while(reader.hasNext()) {
        reader.nextEvent(event)

        
        
        //===================================================================================================//
        //==========//   Getting Current Number of Generated Events as of the given event loop   //==========//
        banks_gen.each{event.read(it)}
        if(banks_gen.every()) {
            def (runb_gen, evb_gen, partb_gen, ecb_gen, ccb_gen, trajb_gen, scb_gen) = banks_gen
            def pid_el_gen = partb_gen.getInt("pid", 0)
            if(pid_el_gen == 11){
                // There is a generated electron
                for(int ipart = 1; ipart < partb_gen.getRows(); ipart++){
                    def pid_pip_gen = partb_gen.getInt("pid", ipart)
                    if(pid_pip_gen == 211){
                        // There is a generated Pi+
                        num_of_gen_sidis_events += 1
                    }
                }
            }
        }
        //==========//   Getting Current Number of Generated Events as of the given event loop   //==========//
        //===================================================================================================//
        
        
        
        def yesbs = schemas.collect{event.scan(it.getGroup(), it.getItem()) > 0}
        
        if(yesbs.every()){
            
            banks.each{event.read(it)}

            def (runb, evb, partb, ecb, ccb, trajb, scb, MChead, MCpart) = banks
            
            def run = runb.getInt("run", 0)
            def evn = runb.getInt("event", 0)
            
            def canele = ElectronCandidate.getElectronCandidate(0, partb, ecb, ccb, trajb, isinb)
            def ele = canele.getLorentzVector()
            
            
            //==================================================//
            //==========//   Electron (REC) Found   //==========//
            //==================================================//
            if(canele.iselectron()){
                // A RECONSTRUCTED electron has been found
                
                
                // These lists are to make sure that the same generated particles are not matched to multiple reconstructed particles
                // Applies mainly to the pi+ pion as the same electron should be matched several times while searching for the pions
                // The electron list is included in case the electron is matched to different particles within the same event (room for future improvement to remove unnecessary searching later)
                def list_of_matched_particles_gen_pip = []
                def list_of_matched_particles_gen_ele = []


                //=====================================================//
                //==========//   Start of Pi+ (REC) Loop   //==========//
                //=====================================================//
                for(int ipart = 1; ipart < partb.getRows(); ipart++){
                    
                    def canpip = PionCandidate.getPionCandidate(ipart, partb, trajb, isinb)
                    
                    
                    //==================================================//
                    //==========//   Pi+ Pion (REC) Found   //==========//
                    //==================================================//
                    if(canpip.ispip()){
                        // A RECONSTRUCTED pi+ particle has been found with the given electron
                        // After this 'if' statement, the event being added to the ntuple is known to have at least one RECONSTRUCTED electron AND pi+ pion

                        def pip0 = canpip.getLorentzVector()
                        
                        
                        //========================================================//
                        //==========// Reconstructed Info to be Saved //==========//
                        
                        // Cartesian Momentum Coordinates
                        def ex = ele.px(), ey = ele.py(), ez = ele.pz()
                        def pipx = pip0.px(), pipy = pip0.py(), pipz = pip0.pz()
                        
                        // Sectors (From Detector)
                        def esec = canele.getPCALsector(), pipsec = canpip.getDCsector()
                        
                        // Coordinate of the matched hit (cm) - for Valerii's Fiducial Cuts (done in python)
                        float Hx = ecb.getFloat("hx", 0)
                        float Hy = ecb.getFloat("hy", 0)
                        
                        //==========// Reconstructed Info to be Saved //==========//
                        //========================================================//
                        
                        
                        // Spherical Momentum Coordinates
                        def el = ele.p()
                        def elth = (180/3.1415926)*ele.theta()
                        def elPhi = (180/3.1415926)*ele.phi()
                        def pip = pip0.p()
                        def pipth = (180/3.1415926)*pip0.theta()
                        def pipPhi = (180/3.1415926)*pip0.phi()
                        
                        
                        
                        
                        // After this line, a proper reconstructed ep->epi+X SIDIS event has been found. The following lines will aim to match these particles to their generated counterparts
                        if(print_extra_info == 1){
                            
                            System.out.println("For event: " + evn);
                            System.out.println("Number of (gen) rows: " + MCpart.getRows());

                        }
                        
                        
                        // Below are the main angular matching criteria for both particles
                        def Phi_Ele_Criteria = 10;
                        def Theta_Ele_Criteria = 6;
                        def Phi_Pip_Criteria = 10;
                        def Theta_Pip_Criteria = 6;
                        
                        
                        def Best_ele_Match = 1000;
                        def Best_pip_Match = 1000;
                        
                        def Next_Best_ele_Match = 1000;
                        def Next_Best_pip_Match = 1000;
                        
                        def num_of_possible_ele_matches = 0
                        def pid_matched_el = 0
                        def matched_el_x_gen = 0
                        def matched_el_y_gen = 0
                        def matched_el_z_gen = 0
                        def matched_el_E_gen = 0
                        
                        def num_of_possible_pip_matches = 0
                        def pid_matched_pip = 0
                        def matched_pip_x_gen = 0
                        def matched_pip_y_gen = 0
                        def matched_pip_z_gen = 0
                        def matched_pip_E_gen = 0
                        
                        
                        def pid_other_matched_el = 0
                        def other_matched_el_x_gen = 0
                        def other_matched_el_y_gen = 0
                        def other_matched_el_z_gen = 0
                        def other_matched_el_E_gen = 0
                        
                        def pid_other_matched_pip = 0
                        def other_matched_pip_x_gen = 0
                        def other_matched_pip_y_gen = 0
                        def other_matched_pip_z_gen = 0
                        def other_matched_pip_E_gen = 0
                        
                        def current_match_pip = []
                        def current_2nd_match_pip = []
                        def current_match_ele = []
                        def current_2nd_match_ele = []
                        
                        
                        //====================================================================================================//
                        //----------------------------------------------------------------------------------------------------//
                        //==========||==========||==========// Matching to Generated Loop //==========||==========||==========//
                        //----------------------------------------------------------------------------------------------------//
                        //====================================================================================================//
                        for(int ii_MCpart = 0; ii_MCpart < MCpart.getRows(); ii_MCpart++){
                            // This loop is to go through each particle in the event to find the generated match for the reconstucted particles above
                            
                            def pid_unmatched = MCpart.getInt("pid", ii_MCpart)
                            def unmatched_x_gen = MCpart.getFloat("px", ii_MCpart)
                            def unmatched_y_gen = MCpart.getFloat("py", ii_MCpart)
                            def unmatched_z_gen = MCpart.getFloat("pz", ii_MCpart)
                            def unmatched_vec_gen = LorentzVector.withPID(pid_unmatched, unmatched_x_gen, unmatched_y_gen, unmatched_z_gen)
                            
                            
                            
                            
                            
                            
                            if(print_extra_info == 1){
                                System.out.println("Particle in row " + ii_MCpart + " has PID= " + pid_unmatched);
                            }
                            
                            def unmatched_p = unmatched_vec_gen.p()
                            def unmatched_th = (180/3.1415926)*unmatched_vec_gen.theta()
                            def unmatched_Phi = (180/3.1415926)*unmatched_vec_gen.phi()
                            def unmatched_charge_gen = (PDGDatabase.getParticleById(pid_unmatched)).charge()
                            
                            
                            //------------------------------------------------------------------------------------------------------//
                            //==========||==========||==========// ELECTRON MATCHING CONDITIONS //==========||==========||==========//
                            //------------------------------------------------------------------------------------------------------//
                            if(unmatched_charge_gen == -1){ //=====// Condition 1: Charge is matched for the Electron //=====//
                                
                                //===============// (Other) Matching Conditions for Electron //===============//

                                def Delta_el_p = Math.abs(el - unmatched_p);
                                def Delta_el_th = Math.abs(elth - unmatched_th);
                                def Delta_el_Phi = Math.abs(elPhi - unmatched_Phi);
                                
                                
                                // These lines are to account for the phi-distribution's natural discontinuity (i.e., The maximum difference between phi angles is 180˚. Beyond that, the angles become smaller when measured in the opposite direction. Since phi is naturally measured from ±180˚, a measurement of -179˚ and +179˚ should only be 2˚ apart, not 358˚)
                                if(Delta_el_Phi > 180){
                                    Delta_el_Phi += -360;
                                    Delta_el_Phi = Math.abs(Delta_el_Phi);
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

                                            pid_other_matched_el = pid_matched_el;
                                            other_matched_el_x_gen = matched_el_x_gen;
                                            other_matched_el_y_gen = matched_el_y_gen;
                                            other_matched_el_z_gen = matched_el_z_gen;
                                            other_matched_el_E_gen = matched_el_E_gen;

                                            current_2nd_match_ele = current_match_ele

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

                                        pid_matched_el = pid_unmatched;
                                        matched_el_x_gen = unmatched_x_gen;
                                        matched_el_y_gen = unmatched_y_gen;
                                        matched_el_z_gen = unmatched_z_gen;
                                        matched_el_E_gen = unmatched_vec_gen.e();
                                        
                                        current_match_ele = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]
                                        //  current_match_ele = ["row of match", "PID of match candidate", "Theta angle of match candidate", "Phi angle of match candidate"]

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
                                    
                                    pid_other_matched_el = pid_unmatched;
                                    other_matched_el_x_gen = unmatched_x_gen;
                                    other_matched_el_y_gen = unmatched_y_gen;
                                    other_matched_el_z_gen = unmatched_z_gen;
                                    other_matched_el_E_gen = unmatched_vec_gen.e();
                                    
                                    current_2nd_match_ele = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]
                                    
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

                                    
                                    def Delta_pip_p = Math.abs(pip - unmatched_p);
                                    def Delta_pip_th = Math.abs(pipth - unmatched_th);
                                    def Delta_pip_Phi = Math.abs(pipPhi - unmatched_Phi);
                                    
                                    
                                    // These lines are to account for the phi-distribution's natural discontinuity (i.e., The maximum difference between phi angles is 180˚. Beyond that, the angles become smaller when measured in the opposite direction. Since phi is naturally measured from ±180˚, a measurement of -179˚ and +179˚ should only be 2˚ apart, not 358˚)
                                    if(Delta_pip_Phi > 180){
                                        Delta_pip_Phi += -360;
                                        Delta_pip_Phi = Math.abs(Delta_pip_Phi);
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

                                                pid_other_matched_pip = pid_matched_pip;
                                                other_matched_pip_x_gen = matched_pip_x_gen;
                                                other_matched_pip_y_gen = matched_pip_y_gen;
                                                other_matched_pip_z_gen = matched_pip_z_gen;
                                                other_matched_pip_E_gen = matched_pip_E_gen;

                                                current_2nd_match_pip = current_match_pip

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

                                            pid_matched_pip = pid_unmatched;
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

                                        pid_other_matched_pip = pid_unmatched;
                                        other_matched_pip_x_gen = unmatched_x_gen;
                                        other_matched_pip_y_gen = unmatched_y_gen;
                                        other_matched_pip_z_gen = unmatched_z_gen;
                                        other_matched_pip_E_gen = unmatched_vec_gen.e();

                                        current_2nd_match_pip = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]

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
                                System.out.println("Run Number is: " + run);
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

                        tt.fill(evn, run, ex, ey, ez, pipx, pipy, pipz,
                            esec, pipsec, Hx, Hy,
                            matched_el_x_gen, matched_el_y_gen, matched_el_z_gen, matched_el_E_gen, pid_matched_el,
                            matched_pip_x_gen, matched_pip_y_gen, matched_pip_z_gen, matched_pip_E_gen, pid_matched_pip,
                            other_matched_el_x_gen, other_matched_el_y_gen, other_matched_el_z_gen, other_matched_el_E_gen, pid_other_matched_el,
                            other_matched_pip_x_gen, other_matched_pip_y_gen, other_matched_pip_z_gen, other_matched_pip_E_gen, pid_other_matched_pip,
                            num_of_possible_ele_matches, num_of_possible_pip_matches, num_of_gen_sidis_events)
                        

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
        
        
    }
    //============================================//
    //==========//   Event Loop End   //==========//
    //============================================//

    reader.close()
    
}
}



System.out.println("");

System.out.println("Total number of completly matched events = " + num_of_total_matched);

System.out.println("Total number of failed Electron matches = " + num_of_failed_ele);
System.out.println("Total number of failed Pi+ Pion matches = " + num_of_failed_pip);

System.out.println("Number of times the reconstructed particles are matched to the same generated particle = " + num_of_double_matches);

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

