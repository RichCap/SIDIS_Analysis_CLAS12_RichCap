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

// // As of 4/16/2025: Running with files that used a different background merging setting (used 45nA instead of 50nA as was done for all prior runs)
//     // Change is only to the output file names - No other changes were made to the internal workings of the script itself
// def ff = new ROOTFile("MC_Matching_sidis_epip_richcap.${suff}.new5.45nA.${outname}.root")

// // // Test_Rules_New_5 --> added code to check phi matches for edge cases (i.e., if Phi_rec = -179˚ and Phi_gen = +179˚, these particles should be considered as matches)
// // def ff = new ROOTFile("MC_Matched_sidis_epip_richcap_Test_Rules_New_5.${suff}.${outname}.root")

// // As of 6/10/2024: Removed second best match info and all of the event count information (i.e., Possible_ele, Possible_pip, and SIDIS_GEN)
// // // Also added Hx_pip, Hy_pip, Hz_pip and layer_DC
// // def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Hx:Hy:Hx_pip:Hy_pip:Hz_pip:layer_DC/I:beamCharge:ex_gen:ey_gen:ez_gen:eE_gen:PID_el:pipx_gen:pipy_gen:pipz_gen:pipE_gen:PID_pip')

// // // Added 'V_PCal', 'W_PCal', 'U_PCal', and 'detector_DC' on 6/12/2024
// // def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Hx:Hy:Hx_pip:Hy_pip:Hz_pip:V_PCal:W_PCal:U_PCal:detector_DC/I:layer_DC/I:beamCharge:ex_gen:ey_gen:ez_gen:eE_gen:PID_el:pipx_gen:pipy_gen:pipz_gen:pipE_gen:PID_pip')

// // // Made the PCal and DC hits, as well as the detector/layer variables unique to each particle on 7/1/2024
// //     // Added/renamed several variables to do this (runs with 'new4')
// // def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:V_PCal:W_PCal:U_PCal:Hx:Hy:ele_x_DC:ele_y_DC:ele_z_DC:Hx_pip:Hy_pip:pip_x_DC:pip_y_DC:pip_z_DC:detector_ele_DC/I:layer_ele_DC/I:detector_pip_DC/I:layer_pip_DC/I:beamCharge:ex_gen:ey_gen:ez_gen:eE_gen:PID_el:pipx_gen:pipy_gen:pipz_gen:pipE_gen:PID_pip')

// // DC hits had to be separated into 3 values per particle per event (each layer is hit and stored separately within each event) - Updated on 7/24/2024
//     // Added/renamed several variables to do this
//     // Removed detector/layer info now that it is built into the other variables
//     // Runs with 'new5'
//     // Also added "Num_Pions" to help control events where the electron is counted twice (in case that is a previously overlooked issue)
// def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:beamCharge:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Num_Pions/I:Hx:Hy:Hx_pip:Hy_pip:V_PCal:W_PCal:U_PCal:ele_x_DC_6:ele_y_DC_6:ele_z_DC_6:ele_x_DC_18:ele_y_DC_18:ele_z_DC_18:ele_x_DC_36:ele_y_DC_36:ele_z_DC_36:pip_x_DC_6:pip_y_DC_6:pip_z_DC_6:pip_x_DC_18:pip_y_DC_18:pip_z_DC_18:pip_x_DC_36:pip_y_DC_36:pip_z_DC_36:ex_gen:ey_gen:ez_gen:eE_gen:PID_el:pipx_gen:pipy_gen:pipz_gen:pipE_gen:PID_pip')

// Updated on 12/17/2025: new6 does not differentiate between the background merging settings for the baseline file names (must see individual HIPO files for such distinctions)
def ff = new ROOTFile("MC_Matching_sidis_epip_richcap.${suff}.new6.${outname}.root")

def branches_string = 'event/I:runN/I:beamCharge:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Num_Pions/I:Hx:Hy:Hx_pip:Hy_pip:V_PCal:W_PCal:U_PCal:ele_x_DC_6:ele_y_DC_6:ele_z_DC_6:ele_x_DC_18:ele_y_DC_18:ele_z_DC_18:ele_x_DC_36:ele_y_DC_36:ele_z_DC_36:pip_x_DC_6:pip_y_DC_6:pip_z_DC_6:pip_x_DC_18:pip_y_DC_18:pip_z_DC_18:pip_x_DC_36:pip_y_DC_36:pip_z_DC_36:ex_gen:ey_gen:ez_gen:eE_gen:PID_el:pipx_gen:pipy_gen:pipz_gen:pipE_gen:PID_pip:Par_PID_el/I:Par_PID_pip/I'
// Additional independent matching criteria branches
// Phi=12, Theta=6
branches_string += ':ex_gen_P12T6:ey_gen_P12T6:ez_gen_P12T6:eE_gen_P12T6:PID_el_P12T6:'
branches_string += 'pipx_gen_P12T6:pipy_gen_P12T6:pipz_gen_P12T6:pipE_gen_P12T6:PID_pip_P12T6:'
branches_string += 'Par_PID_el_P12T6/I:Par_PID_pip_P12T6/I'
// Phi=8, Theta=6
branches_string += ':ex_gen_P8T6:ey_gen_P8T6:ez_gen_P8T6:eE_gen_P8T6:PID_el_P8T6:'
branches_string += 'pipx_gen_P8T6:pipy_gen_P8T6:pipz_gen_P8T6:pipE_gen_P8T6:PID_pip_P8T6:'
branches_string += 'Par_PID_el_P8T6/I:Par_PID_pip_P8T6/I'
// Phi=10, Theta=8
branches_string += ':ex_gen_P10T8:ey_gen_P10T8:ez_gen_P10T8:eE_gen_P10T8:PID_el_P10T8:'
branches_string += 'pipx_gen_P10T8:pipy_gen_P10T8:pipz_gen_P10T8:pipE_gen_P10T8:PID_pip_P10T8:'
branches_string += 'Par_PID_el_P10T8/I:Par_PID_pip_P10T8/I'
// Phi=10, Theta=4
branches_string += ':ex_gen_P10T4:ey_gen_P10T4:ez_gen_P10T4:eE_gen_P10T4:PID_el_P10T4:'
branches_string += 'pipx_gen_P10T4:pipy_gen_P10T4:pipz_gen_P10T4:pipE_gen_P10T4:PID_pip_P10T4:'
branches_string += 'Par_PID_el_P10T4/I:Par_PID_pip_P10T4/I'
// Updated on 12/17/2025 (new feature): add independent generated-match branches for additional matching criteria configurations
def tt = ff.makeTree('h22', 'title', branches_string)

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

// Runs the "Matching to Generated Loop" once for a given (Phi,Theta) criteria set.
// Returns a Map containing the matched gen kinematics + PIDs + parent PIDs + current match bookkeeping.
def matchToGenerated(def MCpart,           def lund,  def list_of_matched_particles_gen_pip,
                     def el,               def elth,  def elPhi,
                     def pip,              def pipth, def pipPhi,
                     def Phi_Ele_Criteria, def Theta_Ele_Criteria,
                     def Phi_Pip_Criteria, def Theta_Pip_Criteria,
                     def print_extra_info,
                     double ABS_TOL, double REL_TOL) {

    def Best_ele_Match = 1000
    def Best_pip_Match = 1000

    def Next_Best_ele_Match = 1000
    def Next_Best_pip_Match = 1000

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

    for(int ii_MCpart = 0; ii_MCpart < MCpart.getRows(); ii_MCpart++){

        def pid_unmatched     = MCpart.getInt("pid",  ii_MCpart)
        def unmatched_x_gen   = MCpart.getFloat("px", ii_MCpart)
        def unmatched_y_gen   = MCpart.getFloat("py", ii_MCpart)
        def unmatched_z_gen   = MCpart.getFloat("pz", ii_MCpart)
        def unmatched_vec_gen = LorentzVector.withPID(pid_unmatched, unmatched_x_gen, unmatched_y_gen, unmatched_z_gen)

        if(print_extra_info == 1){ System.out.println("Particle in row " + ii_MCpart + " has PID= " + pid_unmatched); }

        def unmatched_p   = unmatched_vec_gen.p()
        def unmatched_th  = (180/3.1415926)*unmatched_vec_gen.theta()
        def unmatched_Phi = (180/3.1415926)*unmatched_vec_gen.phi()
        def unmatched_charge_gen = (PDGDatabase.getParticleById(pid_unmatched)).charge()

        //------------------------------------------------------------------------------------------------------//
        //==========||==========||==========// ELECTRON MATCHING CONDITIONS //==========||==========||==========//
        //------------------------------------------------------------------------------------------------------//
        if(unmatched_charge_gen == -1){

            def Delta_el_p   = Math.abs(el    - unmatched_p);
            def Delta_el_th  = Math.abs(elth  - unmatched_th);
            def Delta_el_Phi = Math.abs(elPhi - unmatched_Phi);

            if(Delta_el_Phi > 180){ Delta_el_Phi = Math.abs(Delta_el_Phi-360); }

            def Total_Quality_of_Match = ((Math.abs(Delta_el_th))/(Math.abs(elth))) + ((Math.abs(Delta_el_Phi))/(Math.abs(elPhi)));

            if(Delta_el_Phi < Phi_Ele_Criteria && Delta_el_th < Theta_Ele_Criteria){

                num_of_possible_ele_matches += 1;

                if(Best_ele_Match > Total_Quality_of_Match){

                    if((Total_Quality_of_Match < Next_Best_ele_Match) && (Next_Best_ele_Match != 1000) && (Best_ele_Match != 1000)){

                        Next_Best_ele_Match = Best_ele_Match;

                        pid_other_matched_el   = pid_matched_el;
                        other_matched_el_x_gen = matched_el_x_gen;
                        other_matched_el_y_gen = matched_el_y_gen;
                        other_matched_el_z_gen = matched_el_z_gen;
                        other_matched_el_E_gen = matched_el_E_gen;

                        current_2nd_match_ele  = current_match_ele
                    }

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
                }
            }

            if((Total_Quality_of_Match > Best_ele_Match && Total_Quality_of_Match < Next_Best_ele_Match) || Next_Best_ele_Match == 1000){

                Next_Best_ele_Match = Total_Quality_of_Match;

                pid_other_matched_el   = pid_unmatched;
                other_matched_el_x_gen = unmatched_x_gen;
                other_matched_el_y_gen = unmatched_y_gen;
                other_matched_el_z_gen = unmatched_z_gen;
                other_matched_el_E_gen = unmatched_vec_gen.e();

                current_2nd_match_ele  = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]
            }
        }
        //------------------------------------------------------------------------------------------------------//
        //==========||==========||==========// ELECTRON MATCHING CONDITIONS //==========||==========||==========//
        //------------------------------------------------------------------------------------------------------//


        //------------------------------------------------------------------------------------------------------//
        //==========||==========||==========// PI+ PION MATCHING CONDITIONS //==========||==========||==========//
        //------------------------------------------------------------------------------------------------------//
        if(unmatched_charge_gen == 1){

            if((list_of_matched_particles_gen_pip.isEmpty()) || (list_of_matched_particles_gen_pip.contains([ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]) == false)){

                def Delta_pip_p   = Math.abs(pip    - unmatched_p);
                def Delta_pip_th  = Math.abs(pipth  - unmatched_th);
                def Delta_pip_Phi = Math.abs(pipPhi - unmatched_Phi);

                if(Delta_pip_Phi > 180){ Delta_pip_Phi = Math.abs(Delta_pip_Phi-360); }

                def Total_Quality_of_Match = ((Math.abs(Delta_pip_th))/(Math.abs(pipth))) + ((Math.abs(Delta_pip_Phi))/(Math.abs(pipPhi)));

                if(Delta_pip_Phi < Phi_Pip_Criteria && Delta_pip_th < Theta_Pip_Criteria){

                    num_of_possible_pip_matches += 1;

                    if(Best_pip_Match > Total_Quality_of_Match){

                        if((Total_Quality_of_Match < Next_Best_pip_Match) && (Next_Best_pip_Match != 1000) && (Best_pip_Match != 1000)){

                            Next_Best_pip_Match = Best_pip_Match;

                            pid_other_matched_pip   = pid_matched_pip;
                            other_matched_pip_x_gen = matched_pip_x_gen;
                            other_matched_pip_y_gen = matched_pip_y_gen;
                            other_matched_pip_z_gen = matched_pip_z_gen;
                            other_matched_pip_E_gen = matched_pip_E_gen;

                            current_2nd_match_pip   = current_match_pip
                        }

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
                    }
                }

                if((Total_Quality_of_Match > Best_pip_Match && Total_Quality_of_Match < Next_Best_pip_Match) || Next_Best_pip_Match == 1000){

                    Next_Best_pip_Match = Total_Quality_of_Match;

                    pid_other_matched_pip   = pid_unmatched;
                    other_matched_pip_x_gen = unmatched_x_gen;
                    other_matched_pip_y_gen = unmatched_y_gen;
                    other_matched_pip_z_gen = unmatched_z_gen;
                    other_matched_pip_E_gen = unmatched_vec_gen.e();

                    current_2nd_match_pip   = [ii_MCpart, pid_unmatched, unmatched_th, unmatched_Phi]
                }
            }
        }
        //------------------------------------------------------------------------------------------------------//
        //==========||==========||==========// PI+ PION MATCHING CONDITIONS //==========||==========||==========//
        //------------------------------------------------------------------------------------------------------//
    }

    int parentPID_el = 0
    int parentPID_pi = 0
    if(pid_matched_el  != 0){ parentPID_el = findParentPIDFromLund(lund, pid_matched_el,  matched_el_x_gen,  matched_el_y_gen,  matched_el_z_gen,  ABS_TOL, REL_TOL); }
    if(pid_matched_pip != 0){ parentPID_pi = findParentPIDFromLund(lund, pid_matched_pip, matched_pip_x_gen, matched_pip_y_gen, matched_pip_z_gen, ABS_TOL, REL_TOL); }

    return [
        pid_matched_el    : pid_matched_el,
        matched_el_x_gen  : matched_el_x_gen,
        matched_el_y_gen  : matched_el_y_gen,
        matched_el_z_gen  : matched_el_z_gen,
        matched_el_E_gen  : matched_el_E_gen,

        pid_matched_pip   : pid_matched_pip,
        matched_pip_x_gen : matched_pip_x_gen,
        matched_pip_y_gen : matched_pip_y_gen,
        matched_pip_z_gen : matched_pip_z_gen,
        matched_pip_E_gen : matched_pip_E_gen,

        parentPID_el      : parentPID_el,
        parentPID_pi      : parentPID_pi,

        current_match_ele : current_match_ele,
        current_match_pip : current_match_pip
    ]
}


GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    // QADB qa = new QADB()
    
    def reader    = new HipoReader()
    reader.open(fname)
    def event     = new Event()
    def factory   = reader.getSchemaFactory()
    
    // For counting the number of generated events using the same methods as were used in the GEN files for acceptance corrections
    def schemas     = ['RUN::config', 'REC::Event', 'REC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator', 'MC::Particle', 'MC::Lund'].collect{factory.getSchema(it)}
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
        if(event.hasBanks(schemas_gen)){
            banks_gen.each{event.read(it)}
            def (evb_gen, partb_gen, ecb_gen, ccb_gen, trajb_gen, scb_gen) = banks_gen
            def pid_el_gen = partb_gen.getInt("pid", 0)
            if(pid_el_gen == 11){ // There is a generated electron
                for(int ipart = 1; ipart < partb_gen.getRows(); ipart++){
                    def pid_pip_gen = partb_gen.getInt("pid", ipart)
                    if(pid_pip_gen == 211){ num_of_gen_sidis_events += 1 } // There is a generated Pi+
                }
            }
        }
        //==========//   Getting Current Number of Generated Events as of the given event loop   //==========//
        //===================================================================================================//
        
        if(event.hasBanks(schemas)){
            
            banks.each{event.read(it)}

            def (runb, evb, partb, ecb, ccb, trajb, scb, MCpart, lund) = banks
            
            def run            = runb.getInt("run",   0)
            def evn            = runb.getInt("event", 0)
            
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
                // The electron list is included in case the electron is matched to different particles within the same event
                // Independent per-criteria matched-gen bookkeeping lists (so each criteria behaves like a separate run)
                def list_of_matched_particles_gen_pip       = []   // default (P10T6)
                def list_of_matched_particles_gen_pip_P12T6 = []
                def list_of_matched_particles_gen_pip_P8T6  = []
                def list_of_matched_particles_gen_pip_P10T8 = []
                def list_of_matched_particles_gen_pip_P10T4 = []
                
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
                        pionCount += 1;

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
                        float V_PCal = ecb.getFloat("lv", 0)
                        float W_PCal = ecb.getFloat("lw", 0)
                        float U_PCal = ecb.getFloat("lu", 0)
                        
                        // Coordinate of the matched hit (Drift Chamber) [cm] - for fiducial cuts - Based on Electron - for layers 6, 18, and 36 (i.e., regions 1, 2, and 3)
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
                        
                        // // Drift Chamber layer
                        // // Drift Chamber detector (DC = 6)
                        
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

                        //========================================================================================//
                        //==========//   Matching to Generated Loop (run 5 independent criteria sets) //==========//
                        //========================================================================================//

                        // Default (existing behavior): Phi=10, Theta=6
                        def match_default = matchToGenerated(MCpart, lund, list_of_matched_particles_gen_pip,     el, elth, elPhi, pip, pipth, pipPhi, 10, 6, 10, 6, print_extra_info, ABS_TOL, REL_TOL)

                        // Additional criteria sets (independent branch sets)
                        def match_P12T6 = matchToGenerated(MCpart, lund, list_of_matched_particles_gen_pip_P12T6, el, elth, elPhi, pip, pipth, pipPhi, 12, 6, 12, 6, print_extra_info, ABS_TOL, REL_TOL)

                        def match_P8T6  = matchToGenerated(MCpart, lund, list_of_matched_particles_gen_pip_P8T6,  el, elth, elPhi, pip, pipth, pipPhi, 8,  6,  8, 6, print_extra_info, ABS_TOL, REL_TOL)

                        def match_P10T8 = matchToGenerated(MCpart, lund, list_of_matched_particles_gen_pip_P10T8, el, elth, elPhi, pip, pipth, pipPhi, 10, 8, 10, 8, print_extra_info, ABS_TOL, REL_TOL)

                        def match_P10T4 = matchToGenerated(MCpart, lund, list_of_matched_particles_gen_pip_P10T4, el, elth, elPhi, pip, pipth, pipPhi, 10, 4, 10, 4, print_extra_info, ABS_TOL, REL_TOL)

                        // Unpack default matches into the existing variable names (preserves downstream behavior)
                        def pid_matched_el   = match_default.pid_matched_el
                        def matched_el_x_gen = match_default.matched_el_x_gen
                        def matched_el_y_gen = match_default.matched_el_y_gen
                        def matched_el_z_gen = match_default.matched_el_z_gen
                        def matched_el_E_gen = match_default.matched_el_E_gen

                        def pid_matched_pip   = match_default.pid_matched_pip
                        def matched_pip_x_gen = match_default.matched_pip_x_gen
                        def matched_pip_y_gen = match_default.matched_pip_y_gen
                        def matched_pip_z_gen = match_default.matched_pip_z_gen
                        def matched_pip_E_gen = match_default.matched_pip_E_gen

                        def current_match_ele = match_default.current_match_ele
                        def current_match_pip = match_default.current_match_pip

                        int parentPID_el = match_default.parentPID_el
                        int parentPID_pi = match_default.parentPID_pi

                        //========================================================//
                        //====================// Print Info //====================//
                        //========================================================//
                        
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
                                if(print_extra_info == 1){ System.out.println("Failure to match either particle"); }
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
                        
                        //========================================================//
                        //====================// Print Info //====================//
                        //========================================================//

                        // Update per-criteria lists (so each criteria behaves like a separate run)
                        list_of_matched_particles_gen_pip.add(current_match_pip)
                        list_of_matched_particles_gen_pip_P12T6.add(match_P12T6.current_match_pip)
                        list_of_matched_particles_gen_pip_P8T6.add(match_P8T6.current_match_pip)
                        list_of_matched_particles_gen_pip_P10T8.add(match_P10T8.current_match_pip)
                        list_of_matched_particles_gen_pip_P10T4.add(match_P10T4.current_match_pip)
                        
                        if(list_of_matched_particles_gen_ele.isEmpty()){ list_of_matched_particles_gen_ele.add(current_match_ele) }
                        else{
                            if((list_of_matched_particles_gen_ele.contains(current_match_ele) == false) && print_extra_info == 1){
                                System.out.println("Multiple electrons have been matched to the same event");
                                System.out.println("Event Number is: " + evn);
                                System.out.println("Run Number is: " + run);
                                System.out.println("The list of electrons are: " + list_of_matched_particles_gen_ele);
                            }
                        }

                        // Fill tree:
                        // - default criteria fills existing branches
                        // - additional criteria fill their new, independent branches
                        tt.fill(evn,      run,      beamCharge,        ex, ey, ez,        pipx, pipy, pipz,
                                esec,     pipsec,   pionCount,         Hx, Hy, Hx_pip,    Hy_pip,
                                V_PCal,             W_PCal,            U_PCal,
                                ele_x_DC_6,         ele_y_DC_6,        ele_z_DC_6,
                                ele_x_DC_18,        ele_y_DC_18,       ele_z_DC_18,
                                ele_x_DC_36,        ele_y_DC_36,       ele_z_DC_36,
                                pip_x_DC_6,         pip_y_DC_6,        pip_z_DC_6,
                                pip_x_DC_18,        pip_y_DC_18,       pip_z_DC_18,
                                pip_x_DC_36,        pip_y_DC_36,       pip_z_DC_36,
                                
                                // Default (P10T6)
                                matched_el_x_gen,   matched_el_y_gen,  matched_el_z_gen,  matched_el_E_gen,  pid_matched_el,
                                matched_pip_x_gen,  matched_pip_y_gen, matched_pip_z_gen, matched_pip_E_gen, pid_matched_pip,
                                parentPID_el,       parentPID_pi,
                                
                                // Phi=12, Theta=6
                                match_P12T6.matched_el_x_gen,  match_P12T6.matched_el_y_gen,  match_P12T6.matched_el_z_gen,  match_P12T6.matched_el_E_gen,  match_P12T6.pid_matched_el,
                                match_P12T6.matched_pip_x_gen, match_P12T6.matched_pip_y_gen, match_P12T6.matched_pip_z_gen, match_P12T6.matched_pip_E_gen, match_P12T6.pid_matched_pip,
                                match_P12T6.parentPID_el,      match_P12T6.parentPID_pi,
                                
                                // Phi=8, Theta=6
                                match_P8T6.matched_el_x_gen,   match_P8T6.matched_el_y_gen,   match_P8T6.matched_el_z_gen,   match_P8T6.matched_el_E_gen,   match_P8T6.pid_matched_el,
                                match_P8T6.matched_pip_x_gen,  match_P8T6.matched_pip_y_gen,  match_P8T6.matched_pip_z_gen,  match_P8T6.matched_pip_E_gen,  match_P8T6.pid_matched_pip,
                                match_P8T6.parentPID_el,       match_P8T6.parentPID_pi,
                                
                                // Phi=10, Theta=8
                                match_P10T8.matched_el_x_gen,  match_P10T8.matched_el_y_gen,  match_P10T8.matched_el_z_gen,  match_P10T8.matched_el_E_gen,  match_P10T8.pid_matched_el,
                                match_P10T8.matched_pip_x_gen, match_P10T8.matched_pip_y_gen, match_P10T8.matched_pip_z_gen, match_P10T8.matched_pip_E_gen, match_P10T8.pid_matched_pip,
                                match_P10T8.parentPID_el,      match_P10T8.parentPID_pi,
                                
                                // Phi=10, Theta=4
                                match_P10T4.matched_el_x_gen,  match_P10T4.matched_el_y_gen,  match_P10T4.matched_el_z_gen,  match_P10T4.matched_el_E_gen,  match_P10T4.pid_matched_el,
                                match_P10T4.matched_pip_x_gen, match_P10T4.matched_pip_y_gen, match_P10T4.matched_pip_z_gen, match_P10T4.matched_pip_E_gen, match_P10T4.pid_matched_pip,
                                match_P10T4.parentPID_el,      match_P10T4.parentPID_pi
                        )
                        
                        if(pionCount > 1){ Multiple_Pions_Per_Electron += 1 }

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
        else{ num_of_yesbs_fail += 1; }
        
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

