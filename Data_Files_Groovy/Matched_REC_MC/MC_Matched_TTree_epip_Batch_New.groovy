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
// import uconn.utils.pid.stefan.ElectronCandidate.Cut
import uconn.utils.pid.stefan.PionCandidate
// import uconn.utils.pid.stefan.PionCandidate.Cut
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
// Using Bank Matching
branches_string += ':ex_gen_Bank:ey_gen_Bank:ez_gen_Bank:eE_gen_Bank:PID_el_Bank:'
branches_string += 'pipx_gen_Bank:pipy_gen_Bank:pipz_gen_Bank:pipE_gen_Bank:PID_pip_Bank:'
branches_string += 'el_Bank_Match_Quality:pip_Bank_Match_Quality:'
branches_string += 'Par_PID_el_Bank/I:Par_PID_pip_Bank/I'

// Reconstructed PID Cut variations:
    // Electrons
branches_string += ':Full_norm_el/I:Full_tight_el/I:Full_mid_el/I:Full_loose_el/I'
branches_string += ':DC_VERTEX_norm_el/I:DC_VERTEX_tight_el/I:DC_VERTEX_mid_el/I:DC_VERTEX_loose_el/I'
branches_string += ':DC_FIDUCIAL_REG_norm_el/I:DC_FIDUCIAL_REG_tight_el/I:DC_FIDUCIAL_REG_mid_el/I:DC_FIDUCIAL_REG_loose_el/I'
branches_string += ':DC_FIDUCIAL_REG3_norm_el/I:DC_FIDUCIAL_REG3_tight_el/I:DC_FIDUCIAL_REG3_mid_el/I:DC_FIDUCIAL_REG3_loose_el/I'
branches_string += ':DC_FIDUCIAL_REG2_norm_el/I:DC_FIDUCIAL_REG2_tight_el/I:DC_FIDUCIAL_REG2_mid_el/I:DC_FIDUCIAL_REG2_loose_el/I'
branches_string += ':DC_FIDUCIAL_REG1_norm_el/I:DC_FIDUCIAL_REG1_tight_el/I:DC_FIDUCIAL_REG1_mid_el/I:DC_FIDUCIAL_REG1_loose_el/I'
branches_string += ':EC_FIDUCIAL_norm_el/I:EC_FIDUCIAL_tight_el/I:EC_FIDUCIAL_mid_el/I:EC_FIDUCIAL_loose_el/I'
branches_string += ':EC_SAMPLING_norm_el/I:EC_SAMPLING_tight_el/I:EC_SAMPLING_mid_el/I:EC_SAMPLING_loose_el/I'
branches_string += ':EC_OUTER_VS_INNER_norm_el/I:EC_OUTER_VS_INNER_tight_el/I:EC_OUTER_VS_INNER_mid_el/I:EC_OUTER_VS_INNER_loose_el/I'
branches_string += ':CC_NPHE_norm_el/I:PID_norm_el/I'
    // Pi+ Pions
branches_string += ':Full_norm_pip/I:Full_tight_pip/I:Full_mid_pip/I:Full_loose_pip/I'
branches_string += ':DELTA_VZ_norm_pip/I:DELTA_VZ_tight_pip/I:DELTA_VZ_mid_pip/I:DELTA_VZ_loose_pip/I'
branches_string += ':DC_FIDUCIAL_REG_norm_pip/I:DC_FIDUCIAL_REG_tight_pip/I:DC_FIDUCIAL_REG_mid_pip/I:DC_FIDUCIAL_REG_loose_pip/I'
branches_string += ':DC_FIDUCIAL_REG3_norm_pip/I:DC_FIDUCIAL_REG3_tight_pip/I:DC_FIDUCIAL_REG3_mid_pip/I:DC_FIDUCIAL_REG3_loose_pip/I'
branches_string += ':DC_FIDUCIAL_REG2_norm_pip/I:DC_FIDUCIAL_REG2_tight_pip/I:DC_FIDUCIAL_REG2_mid_pip/I:DC_FIDUCIAL_REG2_loose_pip/I'
branches_string += ':DC_FIDUCIAL_REG1_norm_pip/I:DC_FIDUCIAL_REG1_tight_pip/I:DC_FIDUCIAL_REG1_mid_pip/I:DC_FIDUCIAL_REG1_loose_pip/I'
branches_string += ':CHI2PID_CUT_norm_pip/I:CHI2PID_CUT_tight_pip/I:CHI2PID_CUT_mid_pip/I:CHI2PID_CUT_loose_pip/I'
branches_string += ':FORWARD_norm_pip/I:PID_norm_pip/I'

// Additional Variables for PID Cuts:
branches_string += ':pcal_energy:ecin_energy:ecout_energy:ele_DC_vertex_vz' // Electrons
branches_string += ':pip_chi2pid:pip_dvz'                                   // Pi+ Pions

// Updated on 12/17/2025 (new feature): add independent generated-match branches for additional matching criteria configurations
    // Second update on 12/22/2025: Added PID cut branches and some of the missing variables to be able to manipulate them again in the ROOT output files
def tt = ff.makeTree('h22', 'title', branches_string)

// If print_extra_info = 1, then extra information will be printed while running this program (do not do unless trying to test certain information - will run less efficiently)
// Let print_extra_info = 0 to run normally
print_extra_info = 0

def num_of_failed_ele = 0
def num_of_failed_pip = 0


def num_of_total_matched  = 0
def num_of_true_matched   = 0
def num_of_strict_matched = 0

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


// Helper: Converts booleans into integers (1 == true, 0 == false)
Integer ConvertBoolean(boolean bool) {
    if(bool) { return 1;}
    else {     return 0;}
}

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


def matchBasedonHIPObanks(def RecMatch_in, def MCpart_in, def lund_in, def rec_index, double absTol, double relTol) {

    int pid_matched     = 0;
    float matched_x_gen = 0;
    float matched_y_gen = 0;
    float matched_z_gen = 0;
    float matched_E_gen = 0;
    int parentPID       = 0;
    float quality_match = RecMatch_in.getFloat("quality", rec_index);
    def gen_index       = RecMatch_in.getShort("mcindex", rec_index);
    if(gen_index < 0){
        // System.out.println("UnMatched Particle")
        return [
            pid_matched    : pid_matched,
            matched_x_gen  : matched_x_gen,
            matched_y_gen  : matched_y_gen,
            matched_z_gen  : matched_z_gen,
            matched_E_gen  : matched_E_gen,
            parentPID      : parentPID,
            quality_match  : quality_match
        ]
    }
    
    pid_matched         = MCpart_in.getInt("pid",  gen_index);
    matched_x_gen       = MCpart_in.getFloat("px", gen_index);
    matched_y_gen       = MCpart_in.getFloat("py", gen_index);
    matched_z_gen       = MCpart_in.getFloat("pz", gen_index);
    def matched_vec_gen = LorentzVector.withPID(pid_matched, matched_x_gen, matched_y_gen, matched_z_gen);
    matched_E_gen       = matched_vec_gen.e();
    parentPID           = findParentPIDFromLund(lund_in, pid_matched, matched_x_gen, matched_y_gen, matched_z_gen, absTol, relTol);
    return [
        pid_matched    : pid_matched,
        matched_x_gen  : matched_x_gen,
        matched_y_gen  : matched_y_gen,
        matched_z_gen  : matched_z_gen,
        matched_E_gen  : matched_E_gen,
        parentPID      : parentPID,
        quality_match  : quality_match
    ]
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



// ------------------------------------------------------------
// Custom Electron PID Cuts
// ------------------------------------------------------------

def Custom_EC_OUTER_VS_INNER(def eleCan_In, def cutLevel_In) {
    def pcal_energy  = eleCan_In.pcal_energy;
    if(pcal_energy==null) { return false; }
    final double edep_tight = 0.06, edep_medium = 0.07, edep_loose = 0.09;
    double edep = edep_medium;
    if(cutLevel_In == "loose"){ edep = edep_loose; }
    if(cutLevel_In == "tight"){ edep = edep_tight; }
    return pcal_energy > edep;
}

def Custom_EC_SAMPLING(def eleCan_In, def cutLevel_In) {
    def pcal_sector  = eleCan_In.getPCALsector();
    def partp        = eleCan_In.p;
    def pcal_energy  = eleCan_In.pcal_energy;
    def ecin_energy  = eleCan_In.ecin_energy;
    def ecout_energy = eleCan_In.ecout_energy;
    if(pcal_sector==null || partp==null || pcal_energy==null || ecin_energy==null || ecout_energy==null) { return false; }
    
    double[][] ecal_e_sampl_mu   = [ [  0.2531,  0.2550,  0.2514,  0.2494,  0.2528,  0.2521 ],
                                     [ -0.6502, -0.7472, -0.7674, -0.4913, -0.3988, -0.703  ],
                                     [  4.939,   5.350,   5.102,   6.440,   6.149,   4.957  ] ] as double[][];
    double[][] ecal_e_sampl_sigm = [ [  2.726e-3, 4.157e-3, 5.222e-3, 5.398e-3, 8.453e-3, 6.533e-3 ],
                                     [  1.062,    0.859,    0.5564,   0.6576,   0.3242,   0.4423   ],
                                     [ -4.089,   -3.318,   -2.078,   -2.565,   -0.8223,  -1.274    ] ] as double[][];

    double sigma_range = 3.5;
    if(cutLevel_In == "loose"){ sigma_range = 4.0; }
    if(cutLevel_In == "tight"){ sigma_range = 3.0; }

    double ectotal_energy = pcal_energy + ecin_energy + ecout_energy;
    int isec = pcal_sector-1;
    double mean = ecal_e_sampl_mu[0][isec] + ecal_e_sampl_mu[1][isec]/1000*Math.pow(partp-ecal_e_sampl_mu[2][isec],2);
    double sigma = ecal_e_sampl_sigm[0][isec] + ecal_e_sampl_sigm[1][isec]/(10*(partp-ecal_e_sampl_sigm[2][isec]));
    double upper_lim_total = mean + sigma_range * sigma;
    double lower_lim_total = mean - sigma_range * sigma;

    boolean pass_band = ectotal_energy/partp <= upper_lim_total && ectotal_energy/partp >= lower_lim_total;
    boolean pass_triangle = false;

    if(partp < 4.5) { pass_triangle = true; }
    else { pass_triangle = ecin_energy/partp > (0.2 -  pcal_energy/partp); }

    return pass_band && pass_triangle;
}

def Custom_EC_FIDUCIAL(def eleCan_In, def cutLevel_In) {
    def pcal_sector = eleCan_In.getPCALsector();
    def lv          = eleCan_In.pcal_lv;
    def lw          = eleCan_In.pcal_lw;
    
    if(pcal_sector==null || lv==null || lw==null) { return false; }

    // Cut using the natural directions of the scintillator bars/ fibers:
    double[] min_v_tight_inb   = [19.0, 19.0, 19.0, 19.0, 19.0, 19.0] as double[];
    double[] min_v_med_inb     = [14.0, 14.0, 14.0, 14.0, 14.0, 14.0] as double[];
    double[] min_v_loose_inb   = [9.0,  9.0,  9.0,  9.0,  9.0,  9.0 ] as double[];
    double[] min_v_loosest_inb = [5.0,  5.0,  5.0,  5.0,  5.0,  5.0 ] as double[];
        
    double[] max_v_tight_inb   = [400, 400, 400, 400, 400, 400] as double[];
    double[] max_v_med_inb     = [400, 400, 400, 400, 400, 400] as double[];
    double[] max_v_loose_inb   = [400, 400, 400, 400, 400, 400] as double[];
    double[] max_v_loosest_inb = [400, 400, 400, 400, 400, 400] as double[];
        
    double[] min_w_tight_inb   = [19.0, 19.0, 19.0, 19.0, 19.0, 19.0] as double[];
    double[] min_w_med_inb     = [14.0, 14.0, 14.0, 14.0, 14.0, 14.0] as double[];
    double[] min_w_loose_inb   = [9.0,  9.0,  9.0,  9.0,  9.0,  9.0 ] as double[];
    double[] min_w_loosest_inb = [5.0,  5.0,  5.0,  5.0,  5.0,  5.0 ] as double[];
        
    double[] max_w_tight_inb   = [400, 400, 400, 400, 400, 400] as double[];
    double[] max_w_med_inb     = [400, 400, 400, 400, 400, 400] as double[];
    double[] max_w_loose_inb   = [400, 400, 400, 400, 400, 400] as double[];
    double[] max_w_loosest_inb = [400, 400, 400, 400, 400, 400] as double[];

    int isec = pcal_sector - 1;
    double min_v = min_v_loose_inb[isec];
    double max_v = max_v_loose_inb[isec];
    double min_w = min_w_loose_inb[isec];
    double max_w = max_w_loose_inb[isec];

    // if(lvl == Level.MEDIUM) {
    if(cutLevel_In == "tight") {
        min_v = min_v_med_inb[isec];
        max_v = max_v_med_inb[isec];
        min_w = min_w_med_inb[isec];
        max_w = max_w_med_inb[isec];
    // } else if(lvl == Level.TIGHT) {
    } else if(cutLevel_In == "tighter") {
        min_v = min_v_tight_inb[isec];
        max_v = max_v_tight_inb[isec];
        min_w = min_w_tight_inb[isec];
        max_w = max_w_tight_inb[isec];
    // } else if(lvl == Level.LOOSEST) {
    } else if(cutLevel_In == "loose") {
        min_v = min_v_loosest_inb[isec];
        max_v = max_v_loosest_inb[isec];
        min_w = min_w_loosest_inb[isec];
        max_w = max_w_loosest_inb[isec];
    }

    return lv > min_v && lv < max_v && lw > min_w && lw < max_w;
}


// def Custom_DC_FIDUCIAL_REG(def eleCan_In, def cutLevel_In, def region, boolean isinbending=isinb) {
def Custom_DC_FIDUCIAL_REG(def eleCan_In, def cutLevel_In, def region) {
    boolean isinbending = true;
    def dc_sector = eleCan_In.getDCsector();
    def x         = eleCan_In.getDC1x(); // traj_x1
    def y         = eleCan_In.getDC1y(); // traj_y1
    if(region == 2){
        x         = eleCan_In.traj_x2; // traj_x2
        y         = eleCan_In.traj_y2; // traj_y2
    }
    if(region == 3){
        x         = eleCan_In.traj_x3; // traj_x3
        y         = eleCan_In.traj_y3; // traj_y3
    }
    def partpid   = eleCan_In.pid; // Should always be 11 for electron

    if(dc_sector==null || x==null || y==null || partpid==null) { return false; }
    
    // new cut parameters for the linear cut based on x and y coordinates (inbending field):
    // replace it in the function: bool DC_fiducial_cut_XY(int j, int region)
    // (optimized for electrons, do not use it for hadrons)
    double[][][][] maxparams_in = [
        [   [[-14.563,0.60032],[-19.6768,0.58729],[-22.2531,0.544896]],[[-12.7486,0.587631],[-18.8093,0.571584],[-19.077,0.519895]],
            [[-11.3481,0.536385],[-18.8912,0.58099],[-18.8584,0.515956]],[[-10.7248,0.52678],[-18.2058,0.559429],[-22.0058,0.53808]],
            [[-16.9644,0.688637],[-17.1012,0.543961],[-21.3974,0.495489]],[[-13.4454,0.594051],[-19.4173,0.58875],[-22.8771,0.558029]]
        ],
        [   [[-6.2928,0.541828],[-16.7759,0.57962],[-32.5232,0.599023]],[[-6.3996,0.543619],[-16.7429,0.578472],[-32.5408,0.600826]],
            [[-5.49712,0.53463],[-16.1294,0.576928],[-32.5171,0.597735]],[[-6.4374,0.54839],[-16.9511,0.582143],[-33.0501,0.59995]],
            [[-5.30128,0.529377],[-16.1229,0.579019],[-30.7768,0.593861]],[[-5.89201,0.541124],[-16.1245,0.575001],[-32.2617,0.601506]]
        ],
        [   [[-6.3618,0.546384],[-17.0277,0.582344],[-34.9276,0.612875]],[[-6.36432,0.546268],[-15.8404,0.574102],[-33.0627,0.599142]],
            [[-6.34357,0.548411],[-16.0496,0.575913],[-34.8535,0.610211]],[[-5.8568,0.541784],[-16.1124,0.576473],[-32.8547,0.599033]],
            [[-5.91941,0.536801],[-15.726,0.575211],[-34.0964,0.606777]],[[-5.55498,0.536609],[-15.9853,0.579705],[-33.4886,0.606439]]
        ],
        [   [[-12.594,0.613062],[-18.4504,0.588136],[-16.3157,0.529461]],[[-12.3417,0.61231],[-18.1498,0.590748],[-13.8106,0.52335]],
            [[-12.1761,0.609307],[-15.919,0.572156],[-13.0598,0.5194]],[[-12.5467,0.612645],[-16.2129,0.572974],[-12.8611,0.51252]],
            [[-13.0976,0.615928],[-16.9233,0.580972],[-13.0906,0.519738]],[[-12.884,0.622133],[-17.2566,0.585572],[-12.1874,0.510124]]
        ],
        [   [[-6.51157,0.545763],[-16.4246,0.583603],[-32.2001,0.60425]],[[-6.21169,0.541872],[-16.8484,0.591172],[-31.7785,0.606234]],
            [[-5.89452,0.54464],[-16.612,0.591506],[-29.9143,0.589656]],[[-6.68908,0.553374],[-16.2993,0.585165],[-30.252,0.59519]],
            [[-6.17185,0.540496],[-16.7197,0.591664],[-31.619,0.608306]],[[-5.7526,0.541761],[-16.2054,0.587326],[-31.3653,0.604081]]
        ],
        [   [[-11.8798,0.62389],[-20.2212,0.610786],[-16.4137,0.51337]],[[-12.0817,0.631621],[-20.7511,0.610844],[-16.9407,0.522958]],
            [[-9.72746,0.605471],[-20.4903,0.622337],[-15.3363,0.520589]],[[-12.4566,0.627481],[-20.238,0.606098],[-20.7651,0.56974]],
            [[-11.6712,0.622265],[-18.2649,0.591062],[-19.2569,0.580894]],[[-12.0943,0.630674],[-22.4432,0.633366],[-17.2197,0.537965]]
        ]
    ] as double[][][][];
    double[][][][] minparams_in = [
        [   [[12.2692,-0.583057],[17.6233,-0.605722],[19.7018,-0.518429]],[[12.1191,-0.582662],[16.8692,-0.56719],[20.9153,-0.534871]],
            [[11.4562,-0.53549],[19.3201,-0.590815],[20.1025,-0.511234]],[[13.202,-0.563346],[20.3542,-0.575843],[23.6495,-0.54525]],
            [[12.0907,-0.547413],[17.1319,-0.537551],[17.861,-0.493782]],[[13.2856,-0.594915],[18.5707,-0.597428],[21.6804,-0.552287]]
        ],
        [   [[5.35616,-0.531295],[16.9702,-0.583819],[36.3388,-0.612192]],[[6.41665,-0.543249],[17.3455,-0.584322],[37.1294,-0.61791]],
            [[6.86336,-0.550492],[17.2747,-0.575263],[39.6389,-0.625934]],[[6.82938,-0.558897],[17.8618,-0.599931],[39.3376,-0.631517]],
            [[6.05547,-0.54347],[15.7765,-0.569165],[35.6589,-0.611349]],[[6.3468,-0.544882],[16.7144,-0.578363],[38.2501,-0.617055]]
        ],
        [   [[6.70668,-0.558853],[17.0627,-0.587751],[36.1194,-0.617417]],[[6.3848,-0.542992],[16.6355,-0.581708],[34.6781,-0.609794]],
            [[6.36802,-0.539521],[15.9829,-0.569165],[32.5691,-0.59588]],[[5.94912,-0.546191],[18.0321,-0.601764],[36.5238,-0.619185]],
            [[5.65108,-0.541684],[15.5009,-0.567131],[34.0489,-0.602048]],[[6.71064,-0.547956],[16.4449,-0.577051],[34.4375,-0.602515]]
        ],
        [   [[12.4734,-0.608063],[16.1064,-0.575034],[16.0751,-0.536452]],[[12.1936,-0.6034],[15.9302,-0.571271],[14.2791,-0.520157]],
            [[12.216,-0.600017],[14.8741,-0.56304],[11.1766,-0.498955]],[[12.7941,-0.616044],[17.1516,-0.583616],[11.6077,-0.500028]],
            [[12.7448,-0.611315],[16.2814,-0.572461],[13.1033,-0.506663]],[[12.7949,-0.612051],[16.1565,-0.569143],[12.9295,-0.504203]]
        ],
        [   [[7.19022,-0.562083],[16.5946,-0.591266],[31.9033,-0.589167]],[[7.80002,-0.571429],[17.8587,-0.595543],[36.5772,-0.630136]],
            [[7.96121,-0.569485],[17.8085,-0.592936],[37.553,-0.632848]],[[7.52041,-0.566112],[17.3385,-0.603462],[33.7712,-0.606047]],
            [[7.35796,-0.562782],[15.2865,-0.57433],[29.8283,-0.574685]],[[7.80003,-0.571429],[16.1751,-0.583286],[39.1972,-0.642803]]
        ],
        [   [[13.4466,-0.633911],[22.0097,-0.62205],[18.8862,-0.519652]],[[13.0534,-0.626648],[20.2994,-0.60581],[19.3973,-0.573994]],
            [[12.547,-0.62145],[18.9322,-0.596491],[16.2331,-0.546036]],[[14.5339,-0.64585],[20.0211,-0.608462],[19.0405,-0.563914]],
            [[12.7388,-0.617954],[21.1677,-0.621012],[15.4502,-0.525165]],[[13.4019,-0.63075],[16.6584,-0.554797],[19.0302,-0.55004]]
        ]
    ] as double[][][][];
    // //double maxparams_out[6][6][3][2] =
    // double[][][][] maxparams_out = [
    //     [   [[-9.86221, 0.565985],[-16.4397, 0.569087],[-29.7787, 0.586842]],
    //         [[-10.2065, 0.565541],[-16.5554, 0.571394],[-28.933, 0.582078]],
    //         [[-8.48034, 0.550706],[-16.4397, 0.569087],[-27.1037, 0.563767]],
    //         [[-6.77188, 0.53062],[-16.4397, 0.569087],[-30.485, 0.587534]],
    //         [[-8.00705, 0.543502],[-16.4038, 0.571178],[-27.7934, 0.573472]],
    //         [[-10.3328, 0.571942],[-16.69, 0.575252],[-30.8177, 0.592418]]
    //     ],
    //     [   [[-5.43811, 0.550931],[-17.1906, 0.57936],[-18.552, 0.546789]],
    //         [[-5.46281, 0.549659],[-18.0351, 0.588876],[-17.6981, 0.549803]],
    //         [[-3.26087, 0.531677],[-16.3762, 0.578005],[-17.6831, 0.55049]],
    //         [[-4.5985, 0.542017],[-17.2735, 0.581566],[-16.7013, 0.538853]],
    //         [[-6.83053, 0.561019],[-16.5082, 0.579816],[-18.0846, 0.553592]],
    //         [[-5.67358, 0.5558],[-18.8196, 0.594965],[-19.4333, 0.560965]]
    //     ],
    //     [   [[-12.6317, 0.611023],[-16.5644, 0.578978],[-11.5882, 0.496324]],
    //         [[-12.8886, 0.614807],[-17.0847, 0.584072],[-14.9561, 0.532125]],
    //         [[-11.4504, 0.600574],[-16.3862, 0.57885],[-12.3309, 0.515431]],
    //         [[-12.2256, 0.609801],[-16.2134, 0.574306],[-12.7661, 0.515787]],
    //         [[-12.6311, 0.611069],[-16.2486, 0.577577],[-12.6783, 0.519597]],
    //         [[-12.6937, 0.615423],[-16.1427, 0.57847],[-11.5156, 0.509458]]
    //     ],
    //     [   [[-5.95834, 0.538479],[-15.8909, 0.570164],[-30.2922, 0.586335]],
    //         [[-6.15277, 0.542134],[-16.1129, 0.573794],[-31.6024, 0.592681]],
    //         [[-6.12341, 0.542023],[-16.1611, 0.575971],[-29.8604, 0.581528]],
    //         [[-6.37691, 0.546536],[-16.8501, 0.580239],[-30.0623, 0.580497]],
    //         [[-5.96605, 0.537402],[-15.7154, 0.5704],[-31.2955, 0.594146]],
    //         [[-5.86704, 0.539556],[-16.2268, 0.580945],[-31.2345, 0.590849]]
    //     ],
    //     [   [[-11.7796, 0.614043],[-19.0763, 0.595015],[-18.804, 0.559538]],
    //         [[-12.4399, 0.623126],[-19.1733, 0.600646],[-17.675, 0.557016]],
    //         [[-10.4158, 0.605483],[-18.0044, 0.595497],[-17.5441, 0.556504]],
    //         [[-12.1552, 0.617782],[-19.7134, 0.603519],[-17.3756, 0.549676]],
    //         [[-11.3901, 0.612121],[-18.2429, 0.596796],[-10.0097, 0.482578]],
    //         [[-12.5004, 0.626384],[-19.9266, 0.60993],[-16.4668, 0.543148]]
    //     ],
    //     [   [[-5.60572, 0.537153],[-16.3196, 0.582537],[-32.4336, 0.601487]],
    //         [[-5.52369, 0.532985],[-15.2055, 0.568935],[-31.9046, 0.600079]],
    //         [[-5.78558, 0.546316],[-16.3328, 0.583765],[-36.0074, 0.617008]],
    //         [[-5.82321, 0.542839],[-15.9551, 0.580441],[-31.4304, 0.597132]],
    //         [[-5.36526, 0.535923],[-15.9219, 0.586886],[-30.4245, 0.599613]],
    //         [[-5.14766, 0.53037],[-14.1986, 0.561504],[-31.7548, 0.60233]]
    //     ]
    // ] as double[][][][];
    // //double minparams_out[6][6][3][2] =
    // double[][][][] minparams_out = [
    //     [   [[8.07831, -0.548881],[16.4382, -0.569075],[33.7768, -0.607402]],
    //         [[8.51057, -0.551773],[16.7782, -0.571381],[32.2613, -0.600686]],
    //         [[8.5232, -0.552628],[16.4274, -0.56775],[31.1516, -0.584708]],
    //         [[7.98845, -0.544571],[16.4381, -0.569077],[31.8093, -0.595237]],
    //         [[7.46705, -0.538557],[16.7414, -0.573345],[31.1888, -0.586751]],
    //         [[7.82627, -0.538957],[16.2409, -0.565872],[32.1089, -0.596846]]
    //     ],
    //     [   [[7.1519, -0.563678],[16.1038, -0.571795],[20.0449, -0.559802]],
    //         [[6.38228, -0.553174],[16.4526, -0.576382],[19.3523, -0.556484]],
    //         [[7.11359, -0.561586],[17.2815, -0.578095],[14.9667, -0.53314]],
    //         [[5.89053, -0.556406],[17.4946, -0.585038],[17.3607, -0.545739]],
    //         [[7.08253, -0.562099],[15.1516, -0.569192],[16.9665, -0.545949]],
    //         [[5.53089, -0.546315],[16.4962, -0.574014],[17.9593, -0.545788]]
    //     ],
    //     [   [[12.4879, -0.610527],[16.7782, -0.575065],[11.7704, -0.511182]],
    //         [[12.1931, -0.604779],[15.6443, -0.560967],[12.7304, -0.515606]],
    //         [[12.206, -0.602999],[16.5979, -0.573274],[12.3971, -0.513795]],
    //         [[11.5538, -0.604186],[16.6974, -0.576753],[12.7385, -0.517811]],
    //         [[12.9718, -0.611968],[17.7233, -0.583943],[10.6601, -0.49233]],
    //         [[12.2966, -0.607592],[15.923, -0.564133],[13.9314, -0.525363]]
    //     ],
    //     [   [[5.92493, -0.539308],[17.4444, -0.586183],[31.6974, -0.591988]],
    //         [[5.467, -0.525876],[16.0649, -0.570869],[30.5937, -0.590071]],
    //         [[5.67798, -0.531096],[16.5072, -0.57205],[30.7922, -0.586727]],
    //         [[6.85795, -0.558336],[14.9425, -0.545596],[31.3159, -0.592865]],
    //         [[6.0155, -0.545283],[16.0649, -0.570869],[30.6644, -0.587002]],
    //         [[6.18343, -0.539055],[17.4516, -0.583221],[32.6264, -0.594317]]
    //     ],
    //     [   [[12.9118, -0.618907],[19.7061, -0.60171],[18.9352, -0.559461]],
    //         [[13.0612, -0.618743],[19.0954, -0.595406],[19.7019, -0.568119]],
    //         [[12.4007, -0.613459],[17.544, -0.581147],[12.8175, -0.511017]],
    //         [[13.3144, -0.625596],[18.9225, -0.594001],[15.1524, -0.530046]],
    //         [[13.101, -0.620887],[18.5616, -0.595279],[14.8807, -0.533111]],
    //         [[12.2964, -0.613529],[19.0686, -0.595276],[19.2596, -0.562706]]
    //     ],
    //     [   [[5.34118, -0.530584],[16.3015, -0.585185],[38.7808, -0.641362]],
    //         [[6.68051, -0.548747],[16.4236, -0.583598],[38.4718, -0.630423]],
    //         [[6.87, -0.552602],[16.4285, -0.57977],[36.8889, -0.624053]],
    //         [[7.15338, -0.565067],[16.9387, -0.595922],[37.2398, -0.624177]],
    //         [[6.06995, -0.550001],[15.7376, -0.577755],[32.6004, -0.601595]],
    //         [[6.20459, -0.543148],[14.6326, -0.561623],[39.2154, -0.631762]]
    //     ]
    // ] as double[][][][];

    // double[][][][] minparams = isinbending ? minparams_in : minparams_out;
    // double[][][][] maxparams = isinbending ? maxparams_in : maxparams_out;

    double[][][][] minparams = minparams_in;
    double[][][][] maxparams = maxparams_in;

    double X = x;
    double Y = y;

    double X_new = X * Math.cos(Math.toRadians(-60*(dc_sector-1))) - Y * Math.sin(Math.toRadians(-60*(dc_sector-1)));
    Y = X * Math.sin(Math.toRadians(-60*(dc_sector-1))) + Y * Math.cos(Math.toRadians(-60*(dc_sector-1)));
    X = X_new;

    int pid = 0;

    switch (partpid){
    case 11:
        pid = 0;
        break;
    case 2212:
        pid = 1;
        break;
    case 211:
        pid = 2;
        break;
    case -211:
        pid = 3;
        break;
    case 321:
        pid = 4;
        break;
    case -321:
        pid = 5;
        break;
    default:
        return false;
    }
    //if(inbending == true) pid = 0; // use only for electrons in inbending case
    double calc_min = minparams[pid][dc_sector - 1][region-1][0] + minparams[pid][dc_sector - 1][region-1][1] * X;
    double calc_max = maxparams[pid][dc_sector - 1][region-1][0] + maxparams[pid][dc_sector - 1][region-1][1] * X;
    double region_scale = 0.5;
    if(region == 2){ region_scale = 0.505; }
    if(region == 3){ region_scale = 0.495; }
    
    if(cutLevel_In == 'loose') {
        calc_min = calc_min + (-region_scale * ( 0.6 * region));
        calc_max = calc_max + ( region_scale * ( 0.6 * region));
    }
    if(cutLevel_In == 'tight') {
        calc_min = calc_min + (-region_scale * (-0.6 * region));
        calc_max = calc_max + ( region_scale * (-0.6 * region));
    }

    return (Y > calc_min) && (Y < calc_max);
}

def Custom_DC_VERTEX(def eleCan_In, def cutLevel_In) {
    boolean isinbending = true;
    def pcal_sector     = eleCan_In.getPCALsector();
    def partvz          = eleCan_In.vz;

    if(pcal_sector==null || partvz==null ) { return false; }

    double[] vz_min_sect_inb  = [-13d, -13d, -13d, -13d, -13d, -13d];
    double[] vz_max_sect_inb  = [ 12d,  12d,  12d,  12d,  12d,  12d];
    double[] vz_min_sect_outb = [-20d, -20d, -20d, -20d, -20d, -20d];
    double[] vz_max_sect_outb = [ 12d,  12d,  12d,  12d,  12d,  12d];

    double level_var = 0d;
    if(cutLevel_In == 'loose') { level_var = -0.5d; }
    if(cutLevel_In == 'tight') { level_var =  0.5d; }

    int isec = pcal_sector - 1;
    double vz_min = (isinbending ? vz_min_sect_inb[isec]  : vz_min_sect_outb[isec]) + level_var;
    double vz_max = (isinbending ? vz_max_sect_inb[isec]  : vz_max_sect_outb[isec]) - level_var;

    return (partvz > vz_min) && (partvz < vz_max);
}



// ------------------------------------------------------------
// Custom Pi+ Pion PID Cuts
// ------------------------------------------------------------
def Custom_CHI2PID_CUT_pip(def pipCan_In, def cutLevel_In) {
    def p       = pipCan_In.p;
    int pid     = pipCan_In.pid; 
    def chi2pid = pipCan_In.chi2pid;

    if(p==null || pid==null || chi2pid==null ) { return false; }
    
    boolean isstrict = false;
    double coef;
    if(pid==211) coef = 0.88;
    else if(pid==-211) coef = 0.93;
    else if(pid==2212) return Math.abs(chi2pid)<2.64;
    else return false;

    if(cutLevel_In == 'loose') { coef = coef + 0.02;}
    if(cutLevel_In == 'tight') { coef = coef - 0.02;}
        
    boolean chi2cut = false;
    if(isstrict) {
        if(p<2.44)     chi2cut = chi2pid < 3*coef;
        else if(p<4.6) chi2cut = chi2pid <   coef*( 0.00869 + 14.98587*Math.exp(-p/1.18236) + 1.81751*Math.exp(-p/4.86394));
        else           chi2cut = chi2pid <   coef*(-1.14099 + 24.14992*Math.exp(-p/1.36554) + 2.66876*Math.exp(-p/6.80522));
    } else {
        if(p<2.44)     chi2cut = chi2pid < 3*coef;
        else           chi2cut = chi2pid <   coef*( 0.00869 + 14.98587*Math.exp(-p/1.18236) + 1.81751*Math.exp(-p/4.86394));
    }

    return chi2cut && chi2pid>coef*-3;
}

def Custom_DC_FIDUCIAL_REG_pip(def pipCan_In, def cutLevel_In, def region) {
    boolean isinbending = true;
    def dc_sector = pipCan_In.getDCsector();
    def trajx     = pipCan_In.getDC1x(); // traj_x1
    def trajy     = pipCan_In.getDC1y(); // traj_y1
    def trajz     = pipCan_In.getDC1z(); // traj_z1
    if(region == 2) {
        trajx     = pipCan_In.traj_x2; // traj_x2
        trajy     = pipCan_In.traj_y2; // traj_y2
        trajz     = pipCan_In.traj_z2; // traj_z2
    }
    if(region == 3) {
        trajx     = pipCan_In.traj_x3; // traj_x3
        trajy     = pipCan_In.traj_y3; // traj_y3
        trajz     = pipCan_In.traj_z3; // traj_z3
    }
    int partpid   = pipCan_In.pid;

    if(dc_sector==null || trajx==null || trajy==null || trajz==null || partpid==null) { return false; }
    
    // new cut parameters for the polynomial cut based on the local theta and phi coordinates (inbending field):
    // replace it in the function: bool DC_fiducial_cut_theta_phi(int j, int region)
    // (optimized for pi+ and pi-, not optimized for Kaons yet)
    double[][][][] maxparams_in = [
        [   [[-37.5489,27.4543,-1.11484,0.00522935],[-29.7228,26.7512,-1.52592,0.0122397],[-20.3559,23.1586,-1.47441,0.0133898]],
            [[-36.2719,25.1427,-0.817973,0.00233912],[-28.2118,25.0664,-1.29748,0.00947493],[-20.6015,22.9639,-1.39759,0.012069]],
            [[-34.1013,25.9343,-1.23555,0.00959955],[-24.0285,22.9346,-1.165,0.00846331],[-8.04969,12.5436,-0.268326,9.03561e-11]],
            [[-48.5546,36.1076,-2.07362,0.0161268],[-24.7284,22.9355,-1.12754,0.00796403],[-22.5292,24.1624,-1.52361,0.0137042]],
            [[-40.4295,30.8386,-1.77195,0.0156563],[-26.7149,23.5322,-1.1011,0.00715825],[-10.9822,13.8127,-0.312534,1.32292e-05]],
            [[-38.1396,28.0524,-1.19166,0.00613986],[-26.1238,24.3235,-1.28254,0.00950751],[-19.0376,22.042,-1.32482,0.0113948]]
        ],
        [   [[-1.67037e-08,12.8334,-0.820443,0.00818882],[-6.23823,14.8659,-0.776403,0.00624484],[-5.75713,11.4787,-0.227124,6.61281e-10]],
            [[-6.09637e-07,12.7972,-0.813133,0.00808401],[-5.51055,13.9682,-0.639287,0.00441366],[-7.90046,12.5383,-0.271117,1.86929e-10]],
            [[-2.84217e-14,13.0836,-0.864047,0.00869759],[-6.78639,15.3367,-0.827197,0.00677168],[-4.8928,11.1884,-0.221965,1.51263e-10]],
            [[-3.8595e-09,12.9673,-0.841224,0.0083938],[-4.01784,12.9989,-0.557548,0.00367493],[-1.95023,9.69687,-0.157901,5.33239e-09]],
            [[-6.43496e-10,12.9804,-0.850651,0.00863353],[-5.10299,13.9958,-0.671087,0.00489619],[-6.03313,11.7973,-0.249435,1.2754e-11]],
            [[-2.94932e-10,13.1054,-0.859032,0.00848181],[-6.05945,14.7331,-0.742818,0.00558374],[-5.63811,11.6686,-0.247509,2.33147e-13]]
        ],
        [   [[-2.68279e-07,12.99,-0.846226,0.00845788],[-14.6317,19.3874,-1.09244,0.00899541],[-38.1915,29.8688,-1.59229,0.0120089]],
            [[-0.996514,13.9379,-0.964686,0.00982941],[-15.9613,20.2461,-1.16106,0.00955431],[-35.9455,29.0996,-1.586,0.0122175]],
            [[-1.14284e-07,13.6015,-0.966952,0.0101523],[-15.5288,20.3045,-1.20523,0.0102808],[-34.2682,26.4216,-1.20609,0.0078434]],
            [[-1.70075e-08,13.0005,-0.832325,0.00817159],[-7.66776,15.4526,-0.779727,0.00585967],[-26.8035,23.9995,-1.2322,0.00942061]],
            [[-9.53804e-10,13.2563,-0.898206,0.00917629],[-6.85083,14.8485,-0.722803,0.0053221],[-39.3606,31.5412,-1.83015,0.0148302]],
            [[-7.66835e-07,13.937,-1.05153,0.0118223],[-9.7913,16.925,-0.913158,0.00712552],[-27.722,23.9412,-1.1314,0.00761088]]
        ],
        [   [[-22.1832,20.4134,-0.764848,0.00310923],[-31.0844,28.2369,-1.715,0.0145145],[-9.52175,18.7932,-1.38896,0.0150233]],
            [[-21.5849,20.2457,-0.762109,0.00305359],[-19.5601,21.5945,-1.18955,0.00939109],[-1.57084,13.3989,-0.823161,0.00795227]],
            [[-16.052,16.6264,-0.444308,2.82701e-06],[-13.8291,18.6541,-1.01549,0.00825776],[-1.92223e-05,13.0305,-0.881089,0.00925281]],
            [[-19.821,18.4301,-0.516168,2.17199e-10],[-30.6295,28.0989,-1.71897,0.0146585],[-9.23709,17.1589,-1.03955,0.00943673]],
            [[-16.1795,16.7121,-0.448883,1.53774e-11],[-23.6418,24.5748,-1.48652,0.01254],[-4.2626e-09,12.899,-0.845374,0.00872171]],
            [[-9.74791,15.0287,-0.531727,0.00192371],[-41.0848,33.1802,-1.97671,0.0158148],[-4.12428,14.3361,-0.820483,0.00725632]]
        ],
        [   [[-1.05499e-08,12.7347,-0.800158,0.00789171],[-3.78358,13.3272,-0.620589,0.0043452],[-31.0947,26.2276,-1.33783,0.00961276]],
            [[-3.20108e-05,13.2084,-0.89232,0.00907651],[-11.5913,18.4403,-1.08132,0.00895511],[-26.4998,23.4434,-1.09015,0.00695521]],
            [[-1.54979e-07,13.3849,-0.912541,0.00919697],[-4.77271,14.366,-0.750675,0.00582608],[-31.7881,27.2978,-1.49603,0.0115217]],
            [[-8.46957e-07,13.135,-0.863007,0.00850261],[-5.91254,14.7345,-0.748863,0.00564354],[-27.2818,24.4544,-1.24541,0.009006]],
            [[-8.97242e-09,12.8923,-0.825914,0.00815967],[-6.91507,16.0014,-0.917916,0.00756705],[-18.1359,18.5543,-0.695074,0.00311518]],
            [[-2.50141e-08,13.1356,-0.864227,0.00854005],[-6.62648,15.5703,-0.861224,0.00697927],[-19.9356,18.969,-0.647219,0.00209364]]
        ],
        [   [[-31.056,26.1595,-1.20596,0.00643836],[-44.4944,36.2986,-2.35276,0.020162],[-12.2855,21.0109,-1.61628,0.0172125]],
            [[-27.3898,25.1282,-1.2366,0.00728902],[-24.9794,23.2357,-1.09342,0.00656412],[-16.9519,23.8236,-1.78734,0.017541]],
            [[-28.7906,26.9219,-1.49542,0.0104976],[-22.0922,23.6046,-1.37835,0.0110503],[-5.24383,16.5267,-1.15701,0.0113067]],
            [[-3.92728,12.0692,-0.372323,0.0011559],[-23.5702,22.3459,-1.04378,0.00649998],[-17.3561,24.4119,-1.93535,0.0204532]],
            [[-30.442,26.0012,-1.2191,0.00674908],[-54.5014,42.354,-2.8256,0.0242569],[-0.751452,13.9234,-0.958253,0.00952713]],
            [[-31.216,26.1169,-1.20087,0.00650951],[-31.0314,28.4075,-1.70479,0.0137299],[-13.8981,22.326,-1.72999,0.0176742]]
        ]
    ] as double[][][][];
    double[][][][] minparams_in = [
        [   [[45.6964,-33.9555,1.83632,-0.0133721],[16.3132,-19.1709,0.95922,-0.00719164],[17.4745,-21.3091,1.29658,-0.0114378]],
            [[34.063,-25.5129,0.992129,-0.00445872],[22.4188,-23.1898,1.33328,-0.011079],[15.558,-20.779,1.32969,-0.0122892]],
            [[28.8399,-21.4732,0.662977,-0.00227941],[15.2776,-18.4944,0.917128,-0.00703012],[25.9277,-26.2555,1.70407,-0.0154587]],
            [[43.4091,-32.329,1.78095,-0.0143066],[34.8052,-27.7186,1.43403,-0.0108989],[26.384,-24.813,1.4364,-0.0123938]],
            [[42.094,-32.8674,2.12321,-0.0208007],[39.6248,-33.4591,2.1938,-0.0196953],[17.5854,-17.6921,0.617536,-0.00282672]],
            [[24.4957,-19.3118,0.481099,-6.0729e-07],[22.7714,-23.2117,1.31478,-0.0107808],[16.2955,-21.0448,1.33876,-0.0123879]]
        ],
        [   [[2.01913e-05,-13.2206,0.868885,-0.00845047],[6.86331,-15.0105,0.765473,-0.00602765],[5.15884,-11.18,0.21433,-1.79763e-09]],
            [[3.24593,-15.5188,1.12128,-0.011555],[8.61633,-16.3281,0.913374,-0.00783236],[4.51456,-11.0507,0.243113,-0.000607925]],
            [[0.905676,-13.3623,0.85485,-0.00835569],[6.87062,-14.5731,0.694399,-0.00526577],[3.8283,-10.4277,0.178245,-4.2334e-10]],
            [[5.54817e-07,-12.6609,0.744683,-0.00664861],[6.25817,-14.6969,0.728253,-0.00543273],[6.01169,-11.8105,0.251251,-3.71394e-10]],
            [[9.30801e-09,-13.3207,0.888792,-0.00873133],[8.41797,-16.4985,0.956897,-0.00841779],[4.36256,-10.8341,0.202655,-3.44186e-09]],
            [[0.27863,-13.1208,0.833431,-0.0079631],[7.38412,-15.4188,0.82054,-0.00681735],[4.48567,-10.7376,0.190611,-9.77392e-10]]
        ],
        [   [[1.59369e-06,-13.8294,0.990918,-0.0103128],[20.1273,-23.853,1.58449,-0.0145959],[40.8152,-32.8944,2.00731,-0.0171007]],
            [[1.4334,-14.5452,1.04379,-0.0106791],[19.9242,-23.3894,1.5036,-0.0134429],[45.1348,-34.9897,2.11238,-0.0175613]],
            [[4.48276e-06,-12.6688,0.757818,-0.006981],[10.2525,-16.9056,0.909637,-0.00739798],[33.2958,-27.7763,1.53467,-0.0123488]],
            [[3.817e-06,-13.2285,0.856439,-0.0081744],[12.5356,-19.0801,1.1686,-0.0102758],[37.3388,-29.7344,1.64296,-0.0130658]],
            [[3.64842e-07,-14.1631,1.0771,-0.0118569],[9.85442,-17.8198,1.12641,-0.010627],[34.7,-28.5335,1.57226,-0.0124004]],
            [[0.828721,-13.6429,0.895665,-0.00866683],[10.8176,-18.0919,1.11147,-0.010183],[29.9288,-24.3389,1.08973,-0.00703934]]
        ],
        [   [[15.8302,-16.9632,0.53561,-0.00136216],[32.8002,-29.2569,1.79783,-0.015324],[1.98393,-13.0099,0.70788,-0.00615153]],
            [[16.0367,-16.5901,0.470678,-0.000728065],[32.4005,-29.7403,1.92286,-0.0171968],[2.39707,-13.6612,0.816883,-0.00770837]],
            [[22.0623,-21.6319,1.02811,-0.00680893],[32.7467,-29.6099,1.87839,-0.0164223],[1.19902e-08,-12.972,0.863127,-0.00884759]],
            [[21.5883,-21.198,0.957819,-0.00575361],[25.7387,-25.4963,1.5428,-0.0131855],[6.06479,-16.6311,1.16092,-0.0117194]],
            [[19.6915,-19.1751,0.704086,-0.00288768],[28.6596,-27.3351,1.70309,-0.0148193],[5.30096e-08,-11.8562,0.621373,-0.00541869]],
            [[20.6594,-19.8704,0.786033,-0.00394155],[20.7612,-22.3774,1.27116,-0.0104109],[2.56196,-14.4159,0.98009,-0.0100214]]
        ],
        [   [[6.84429e-08,-11.7778,0.558372,-0.00403519],[5.88119,-14.1561,0.630592,-0.00400605],[22.9399,-21.6066,0.97379,-0.00604844]],
            [[5.49686,-16.3382,1.10037,-0.0105049],[9.25791,-16.8955,0.947447,-0.00774283],[19.4826,-18.4694,0.587601,-0.00147216]],
            [[0.148482,-12.4191,0.691879,-0.00595948],[6.95863,-15.5624,0.862069,-0.00725014],[16.6631,-16.746,0.461105,-0.000520762]],
            [[2.64705e-10,-11.8828,0.574528,-0.00419463],[5.45746,-13.9134,0.602948,-0.00360009],[31.3252,-27.342,1.51348,-0.0115756]],
            [[3.46769,-15.3338,1.02031,-0.00951104],[0.368693,-11.8657,0.574108,-0.0044343],[39.7957,-32.8529,2.02652,-0.016978]],
            [[0.00207118,-12.0447,0.602167,-0.00447581],[3.03476,-12.9176,0.603586,-0.00440659],[32.0315,-26.8451,1.37417,-0.00966969]]
        ],
        [   [[56.9355,-42.3826,2.61014,-0.0202986],[28.8989,-27.1772,1.63996,-0.0136625],[4.30155,-15.1455,0.995784,-0.0100192]],
            [[13.4916,-17.1287,0.681434,-0.0031646],[32.246,-29.0499,1.77696,-0.0148718],[2.22052,-9.65178,0.133616,-9.0964e-05]],
            [[41.8686,-33.5132,1.92542,-0.0142307],[0.0645903,-9.74163,0.217245,-2.22987e-05],[9.58895e-09,-13.2013,0.926579,-0.00993616]],
            [[34.8087,-28.1804,1.3547,-0.00784213],[31.3059,-28.7057,1.76134,-0.0146575],[8.66833,-17.8896,1.20937,-0.0116248]],
            [[42.0802,-33.525,1.91492,-0.0140721],[36.8805,-31.3893,1.91131,-0.0157056],[6.11008,-17.0626,1.24276,-0.0127673]],
            [[39.6762,-31.6354,1.73354,-0.0123964],[30.2451,-27.8243,1.67413,-0.0138583],[4.78902,-14.9558,0.912758,-0.00855026]]
        ]
    ] as double[][][][];
    // //fitted values outbending
    // double[][][][] maxparams_out = [
    //     [   [[-3.69457, 12.3755, -0.41328, 0.00129631],[-54.3237, 40.3308, -2.39952, 0.0181339],[-39.8661, 27.1428, -0.907303, 0.00220974]],
    //         [[-37.6199, 26.2865, -0.826366, 0.000862203],[-72.4212, 54.7953, -4.04856, 0.0373308],[-21.1791, 17.0759, -0.391795, 0.00151085]],
    //         [[-0.421685, 10.482, -0.272111, 8.69408e-05],[-43.3635, 32.746, -1.6541, 0.0101454],[-62.6387, 41.1869, -1.97298, 0.0107022]],
    //         [[-42.0766, 29.6387, -0.993426, 1.97101e-09],[-44.7036, 33.0587, -1.64131, 0.0099416],[-47.2703, 32.6109, -1.46533, 0.00817871]],
    //         [[-22.2035, 20.6894, -0.689051, 0.000592423],[-74.6572, 54.7065, -3.83999, 0.0351952],[-38.9183, 25.7212, -0.711499, 2.5796e-12]],
    //         [[-52.078, 45.571, -3.71942, 0.0376577],[-65.4047, 49.1723, -3.36623, 0.0288435],[-53.9611, 35.9294, -1.58589, 0.00772417]]
    //     ],
    //     [   [[-2.20312e-07, 13.0916, -0.864184, 0.0086342],[-6.44026e-08, 12.056, -0.675801, 0.00643464],[-20.2596, 23.5977, -1.545, 0.0141047]],
    //         [[-4.42537e-05, 10.2799, -0.322454, 0.00154825],[-1.63659e-07, 11.0228, -0.451412, 0.00308633],[-8.5382, 15.6903, -0.785315, 0.00602734]],
    //         [[-2.32088, 11.6343, -0.363509, 0.000902217],[-0.301128, 12.0319, -0.643794, 0.00581994],[-22.4378, 25.2772, -1.73656, 0.0164181]],
    //         [[-7.40627, 13.601, -0.382439, 2.45262e-05],[-5.50415e-08, 11.9792, -0.652368, 0.00597647],[-15.1608, 20.6455, -1.33827, 0.0127123]],
    //         [[-0.203913, 10.7032, -0.322123, 0.000691162],[-1.73184e-07, 10.735, -0.379993, 0.00196037],[-0.155443, 10.1794, -0.249841, 6.24278e-05]],
    //         [[-1.87352e-07, 12.4226, -0.730141, 0.0068049],[-1.40236e-07, 12.5356, -0.750615, 0.00719921],[-16.8681, 21.8555, -1.43078, 0.0131935]]
    //     ],
    //     [   [[-8.89326e-08, 10.0681, -0.240869, 9.9612e-12],[-15.2705, 21.635, -1.55291, 0.0166645],[-10.5976, 17.9928, -1.08432, 0.00950807]],
    //         [[-0.00389562, 10.2092, -0.254082, 4.15737e-06],[-9.16032e-11, 10.527, -0.334641, 0.00129061],[-9.63013e-07, 11.0668, -0.42453, 0.0022955]],
    //         [[-2.40163e-06, 13.4151, -0.949883, 0.0107662],[-1.60937e-07, 10.5128, -0.35046, 0.00173787],[-29.2647, 30.1252, -2.20552, 0.0213809]],
    //         [[-2.69733e-08, 11.7703, -0.589854, 0.00482124],[-3.77564e-08, 11.3764, -0.527037, 0.00416671],[-4.85047, 13.7737, -0.650441, 0.0047428]],
    //         [[-3.90816e-07, 12.2683, -0.692591, 0.00625884],[-9.70203e-10, 11.0335, -0.438323, 0.00275342],[-2.54193, 13.5404, -0.76861, 0.00684486]],
    //         [[-3.23439e-10, 10.7412, -0.348557, 0.00113794],[-1.79623, 11.7499, -0.449432, 0.00247294],[-13.1393, 19.4689, -1.17148, 0.00984086]]
    //     ],
    //     [   [[-5.07611e-08, 11.7796, -0.516966, 0.00295389],[-4.87018, 12.2727, -0.322719, 9.12315e-06],[-35.9369, 31.015, -1.95133, 0.0169834]],
    //         [[-1.32385e-07, 11.6454, -0.495467, 0.00272602],[-2.70664, 12.0151, -0.434014, 0.00203292],[-8.97137, 15.0453, -0.646138, 0.00429196]],
    //         [[-7.92247e-09, 12.5189, -0.682231, 0.00539531],[-0.0942499, 10.3465, -0.280521, 0.000405358],[-19.7485, 21.7919, -1.24334, 0.0105088]],
    //         [[-8.50093e-11, 10.739, -0.302295, 5.6862e-11],[-0.184771, 10.4358, -0.285869, 0.000389546],[-21.9469, 24.9675, -1.77893, 0.0183075]],
    //         [[-4.34589, 12.5902, -0.362849, 4.996e-15],[-0.000684493, 10.6055, -0.332363, 0.00104632],[-21.328, 22.0864, -1.20993, 0.00989151]],
    //         [[-0.0202168, 12.0097, -0.539165, 0.00299034],[-0.5239, 10.7167, -0.309141, 0.000535617],[-10.0299, 16.3179, -0.812315, 0.00617078]]
    //     ],
    //     [   [[-0.169908, 10.902, -0.353938, 0.00100715],[-3.2818, 13.2193, -0.65495, 0.00515117],[-0.013532, 8.51331, -0.070239, 1.755e-05]],
    //         [[-8.51985e-08, 11.6512, -0.56808, 0.00453582],[-1.2381e-07, 10.6653, -0.368149, 0.00181989],[-9.30287e-08, 10.0352, -0.254321, 0.000417053]],
    //         [[-0.150407, 10.6338, -0.308676, 0.000481694],[-0.00186321, 10.4259, -0.303092, 0.00073092],[-21.3328, 28.0803, -2.37912, 0.025101]],
    //         [[-14.4411, 19.817, -1.13705, 0.00894685],[-6.25263e-09, 11.7414, -0.586098, 0.00478932],[-5.49193, 16.1248, -1.11306, 0.0115644]],
    //         [[-1.54761, 12.0015, -0.462506, 0.00204729],[-5.72883, 14.9638, -0.795325, 0.00616222],[-50.229, 45.8456, -3.88803, 0.0414729]],
    //         [[-40.7531, 33.6269, -2.03771, 0.01609],[-1.33363e-09, 11.9894, -0.614358, 0.004924],[-27.2506, 29.2602, -2.1426, 0.0203235]]
    //     ],
    //     [   [[-1.62999e-10, 14.0422, -1.03609, 0.0107179],[-6.71565, 15.6964, -0.887791, 0.00740777],[-38.9148, 32.9935, -2.09023, 0.0177295]],
    //         [[-1.09078e-05, 13.4131, -0.878092, 0.00825152],[-15.0102, 21.6968, -1.4935, 0.0138851],[-19.5261, 20.3932, -0.969464, 0.00661531]],
    //         [[-1.39619e-08, 12.3593, -0.618488, 0.00415536],[-5.38271e-07, 11.5631, -0.512607, 0.00334452],[-23.0902, 24.7093, -1.57315, 0.0140132]],
    //         [[-1.73908e-08, 12.0348, -0.591608, 0.00423834],[-8.35134, 17.3066, -1.11555, 0.010407],[-2.74909e-07, 9.59202, -0.216455, 0.000527479]],
    //         [[-0.0449157, 10.5243, -0.334389, 0.00134555],[-0.0143489, 10.0993, -0.2434, 1.57595e-10],[-22.3661, 23.2499, -1.32946, 0.0108047]],
    //         [[-5.83731e-07, 14.5234, -1.14022, 0.0122177],[-1.4586e-08, 11.6946, -0.520935, 0.00324975],[-12.4252, 16.3216, -0.652566, 0.00365791]]
    //     ]
    // ] as double[][][][];
    // double[][][][] minparams_out = [
    //     [   [[3.73672, -12.3584,0.390616, -0.000795415],[51.644, -37.8546,1.99228, -0.0119973],[32.3551, -22.9742,0.624096, -4.30811e-05]],
    //         [[6.11614, -13.6358,0.491668, -0.0018637],[47.5098, -35.902,1.97535, -0.0134876],[82.9536, -58.2741,4.12662, -0.0378612]],
    //         [[0.000950108, -7.99619,0.000506416, -0.0020788],[64.0688, -47.8642,3.16007, -0.025878],[70.0064, -50.3249,3.38975, -0.029639]],
    //         [[37.0145, -35.0316,2.61892, -0.0250306],[14.5954, -15.6554,0.426733, -0.000879865],[28.9035, -21.5279,0.610475, -0.00087271]],
    //         [[5.65685, -13.3347,0.400781, -1.46612e-11],[67.3504, -50.152,3.33677, -0.0270726],[47.0772, -32.1506,1.38851, -0.00719898]],
    //         [[8.95987, -15.1646,0.585477, -0.00246174],[41.6154, -29.7967,1.1817, -0.00403765],[61.1631, -41.6465,2.32522, -0.0175271]]
    //     ],
    //     [   [[8.80954e-10, -11.0364,0.413853, -0.00210254],[6.50072e-08, -11.2505,0.501571, -0.00380973],[10.9643, -17.4701,0.989297, -0.00860789]],
    //         [[2.33292e-08, -11.2353,0.470728, -0.00309666],[2.29373e-07, -11.2458,0.50218, -0.00383969],[29.5429, -29.9965,2.19166, -0.021366]],
    //         [[1.61826e-08, -11.861,0.577321, -0.00433276],[2.9436e-07, -11.5738,0.581015, -0.00503307],[19.5142, -23.451,1.58724, -0.0151339]],
    //         [[2.07231e-09, -12.7453,0.751184, -0.00664181],[1.77802e-07, -11.4574,0.537367, -0.00422656],[12.5683, -18.4632,1.05475, -0.00892182]],
    //         [[7.6216e-08, -13.9769,1.01051, -0.0107372],[1.33092e-08, -11.9128,0.628521, -0.00550105],[13.5537, -20.1708,1.32578, -0.0123213]],
    //         [[9.25941, -19.658,1.51566, -0.0157124],[6.25983e-10, -11.6806,0.599263, -0.00532588],[17.0479, -22.0046,1.47474, -0.0140475]]
    //     ],
    //     [   [[4.65436e-08, -11.1925,0.466196, -0.00308992],[18.4968, -22.5122,1.4594, -0.0135962],[18.9488, -23.3348,1.57414, -0.0146183]],
    //         [[3.67722e-08, -10.9985,0.428395, -0.00257574],[16.3745, -21.0105,1.3093, -0.0119156],[11.4404, -18.6679,1.15919, -0.010306]],
    //         [[1.46846e-08, -10.865,0.398638, -0.00212392],[20.7337, -23.3738,1.46852, -0.0130115],[28.2098, -28.9406,2.05908, -0.0197782]],
    //         [[0.237058, -10.4694,0.271985, -1.08731e-07],[2.32759, -11.9354,0.469887, -0.00291497],[13.287, -20.8621,1.49656, -0.0148999]],
    //         [[0.000149907, -10.4632,0.294713, -0.000431947],[6.96663, -15.3946,0.845078, -0.00724722],[11.0939, -17.4733,0.944239, -0.00747728]],
    //         [[3.10006e-08, -10.1416,0.247764, -1.36913e-11],[5.41915, -14.6085,0.795369, -0.00684375],[5.89127, -13.0881,0.453024, -0.0020325]]
    //     ],
    //     [   [[4.16588e-09, -12.9305,0.749425, -0.00611725],[5.65263, -14.1661,0.637395, -0.00400239],[4.66325, -12.9519,0.565753, -0.00442033]],
    //         [[8.0428e-08, -13.1625,0.836744, -0.00778246],[12.3243, -18.8718,1.11103, -0.00917354],[7.20312, -16.0935,0.987223, -0.00930883]],
    //         [[0.00147165, -10.4992,0.280542, -1.79846e-06],[3.20232, -11.6892,0.350774, -0.00101099],[8.14117e-08, -10.9813,0.524839, -0.00507885]],
    //         [[0.470888, -13.5446,0.820782, -0.00768941],[3.9697, -13.0821,0.540847, -0.00303209],[3.44817, -12.3932,0.533804, -0.00414144]],
    //         [[1.05038e-08, -10.6539,0.297078, -6.04694e-05],[15.0983, -21.1791,1.38383, -0.0124058],[17.3666, -20.3986,1.16663, -0.0102393]],
    //         [[8.49365e-07, -13.765,0.964056, -0.00956575],[9.38084, -16.7385,0.904339, -0.00707907],[12.1048, -17.3704,0.91318, -0.00757461]]
    //     ],
    //     [   [[10.6378, -19.5017,1.45275, -0.017057],[1.24368e-08, -10.5134,0.338985, -0.00143696],[37.3291, -35.1606,2.60092, -0.0242728]],
    //         [[19.1614, -24.0851,1.73932, -0.0185466],[14.1293, -19.8382,1.21613, -0.0107037],[20.9629, -24.0839,1.60283, -0.015173]],
    //         [[0.000450804, -8.15062,0.0103867, -2.00709e-05],[5.72496, -14.338,0.717819, -0.00567964],[16.9428, -21.8075,1.4216, -0.0131736]],
    //         [[6.15991e-10, -11.5278,0.536105, -0.00402223],[2.17842e-07, -10.5338,0.327427, -0.0010898],[20.7387, -24.3028,1.65004, -0.0155857]],
    //         [[0.650351, -10.6177,0.275393, -6.4664e-08],[8.05811, -16.1558,0.913735, -0.00788487],[0.308897, -10.2816,0.275186, -0.000561299]],
    //         [[0.427836, -10.168,0.240458, -5.90042e-06],[2.30661, -12.8686,0.664796, -0.00562626],[0.00499667, -11.6585,0.62597, -0.00619261]]
    //     ],
    //     [   [[9.01249e-07, -11.8437,0.494125, -0.00223452],[14.3941, -21.2365,1.46048, -0.0137349],[13.7095, -15.4704,0.408961, -0.000312145]],
    //         [[0.000251044, -11.3084,0.438545, -0.0020791],[0.00847078, -12.6769,0.804431, -0.00836705],[1.09388, -9.66797,0.175278, -1.8721e-11]],
    //         [[4.04693e-10, -11.9001,0.585913, -0.00440376],[5.05178, -12.1514,0.31134, -0.000112735],[30.8105, -28.0795,1.73625, -0.0151639]],
    //         [[3.86607e-11, -13.471,0.889111, -0.0083617],[8.86591e-09, -9.25745,0.163052, -6.08491e-12],[27.1358, -24.3255,1.23326, -0.00891886]],
    //         [[0.196086, -11.7392,0.480055, -0.00224614],[0.18667, -10.5859,0.287231, -6.53153e-06],[14.8865, -17.1338,0.653576, -0.00333176]],
    //         [[2.7955e-07, -13.1311,0.848222, -0.00812719],[29.5508, -32.9514,2.77917, -0.0291596],[59.7514, -47.3033,3.54495, -0.0341802]]
    //     ]
    // ] as double[][][][];
    
    // double[][][][] minparams = isinbending ? minparams_in : minparams_out;
    // double[][][][] maxparams = isinbending ? maxparams_in : maxparams_out;
    double[][][][] minparams = minparams_in;
    double[][][][] maxparams = maxparams_in;
        
    double trajr = Math.sqrt(Math.pow(trajx,2) + Math.pow(trajy,2) + Math.pow(trajz,2));
    double theta_DCr = Math.toDegrees(Math.acos(trajz/trajr));
    double phi_DCr_raw = Math.toDegrees(Math.atan2(trajy/trajr, trajx/trajr));

    double phi_DCr = 5000;

    if (dc_sector == 1) phi_DCr = phi_DCr_raw;
    if (dc_sector == 2) phi_DCr = phi_DCr_raw - 60;
    if (dc_sector == 3) phi_DCr = phi_DCr_raw - 120;
    if (dc_sector == 4 && phi_DCr_raw > 0) phi_DCr = phi_DCr_raw - 180;
    if (dc_sector == 4 && phi_DCr_raw < 0) phi_DCr = phi_DCr_raw + 180;
    if (dc_sector == 5) phi_DCr = phi_DCr_raw + 120;
    if (dc_sector == 6) phi_DCr = phi_DCr_raw + 60;

    int pid = 0;

    switch (partpid){
        case 11:
            pid = 0;
            break;
        case 2212:
            pid = 1;
            break;
        case 211:
            pid = 2;
            break;
        case -211:
            pid = 3;
            break;
        case 321:
            pid = 4;
            break;
        case -321:
            pid = 5;
            break;
        default:
            return false;
    }
    double calc_phi_min = minparams[pid][dc_sector-1][region-1][0] + minparams[pid][dc_sector-1][region-1][1] * Math.log(theta_DCr) + minparams[pid][dc_sector-1][region-1][2] * theta_DCr + minparams[pid][dc_sector-1][region-1][3] * theta_DCr * theta_DCr;
    double calc_phi_max = maxparams[pid][dc_sector-1][region-1][0] + maxparams[pid][dc_sector-1][region-1][1] * Math.log(theta_DCr) + maxparams[pid][dc_sector-1][region-1][2] * theta_DCr + maxparams[pid][dc_sector-1][region-1][3] * theta_DCr * theta_DCr;
    
    double region_scale = 0.5;
    if(region == 2){ region_scale = 0.505; }
    if(region == 3){ region_scale = 0.495; }
    
    if(cutLevel_In == 'loose') {
        calc_phi_min = calc_phi_min + (-region_scale * ( 0.6 * region));
        calc_phi_max = calc_phi_max + ( region_scale * ( 0.6 * region));
    }
    if(cutLevel_In == 'tight') {
        calc_phi_min = calc_phi_min + (-region_scale * (-0.6 * region));
        calc_phi_max = calc_phi_max + ( region_scale * (-0.6 * region));
    }
    return (phi_DCr > calc_phi_min) && (phi_DCr < calc_phi_max);
}

def Custom_DELTA_VZ_pip(def pipCan_In, def cutLevel_In) {
    def dvz = pipCan_In.dvz;
    if(dvz==null) { return false; }
    double level_cut = 20;
    if(cutLevel_In == 'loose') { level_cut = 22;}
    if(cutLevel_In == 'tight') { level_cut = 18;}
    return ((dvz > -level_cut) && (dvz < level_cut));
}


// ------------------------------------------------------------
// Custom electron detector (individual) wrapper
// ------------------------------------------------------------
def isElectronCustom(def eleCan_in, def cutLevel = "norm", def cut_return = "All") {

    boolean passCut = true;

    // Not impacted by 'cutLevel'
    if(cut_return == "PID"               || cut_return == "All" ) { passCut = passCut && eleCan_in.iselectron(ElectronCandidate.Cut.PID); }
    if(cut_return == "CC_NPHE"           || cut_return == "All" ) { passCut = passCut && eleCan_in.iselectron(ElectronCandidate.Cut.CC_NPHE); }
    
    // Cuts with different levels
    
    if(cut_return == "EC_OUTER_VS_INNER" || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.EC_OUTER_VS_INNER)); }
        else { passCut = (passCut && Custom_EC_OUTER_VS_INNER(eleCan_in, cutLevel)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "EC_SAMPLING"       || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.EC_SAMPLING)); }
        else { passCut = (passCut && Custom_EC_SAMPLING(eleCan_in, cutLevel)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "EC_FIDUCIAL"       || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.EC_FIDUCIAL)); }
        else { passCut = (passCut && Custom_EC_FIDUCIAL(eleCan_in, cutLevel)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG1"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.DC_FIDUCIAL_REG1)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG(eleCan_in, cutLevel, 1)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG2"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.DC_FIDUCIAL_REG2)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG(eleCan_in, cutLevel, 2)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG3"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.DC_FIDUCIAL_REG3)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG(eleCan_in, cutLevel, 3)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_VERTEX"         || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.DC_VERTEX)); }
        else { passCut = (passCut && Custom_DC_VERTEX(eleCan_in, cutLevel)); }
    }
    return passCut;
}

// ------------------------------------------------------------
// Custom pi+ pion detector (individual) wrapper
// ------------------------------------------------------------
def isPipCustom(def pipCan_in, def cutLevel = "norm", def cut_return = "All") {

    boolean passCut = true;

    // Not impacted by 'cutLevel'
    if(cut_return == "PID"               || cut_return == "All" ) { passCut = passCut && pipCan_in.ispip(PionCandidate.Cut.PID); }
    if(cut_return == "FORWARD"           || cut_return == "All" ) { passCut = passCut && pipCan_in.ispip(PionCandidate.Cut.FORWARD); }
    
    // Cuts with different levels
    
    if(cut_return == "CHI2PID_CUT"       || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.CHI2PID_CUT)); }
        else { passCut = (passCut && Custom_CHI2PID_CUT_pip(pipCan_in, cutLevel)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG1"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.DC_FIDUCIAL_REG1)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_pip(pipCan_in, cutLevel, 1)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG2"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.DC_FIDUCIAL_REG2)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_pip(pipCan_in, cutLevel, 2)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG3"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.DC_FIDUCIAL_REG3)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_pip(pipCan_in, cutLevel, 3)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DELTA_VZ"          || cut_return == "All" ) { 
        if(cutLevel == "norm"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.DELTA_VZ)); }
        else { passCut = (passCut && Custom_DELTA_VZ_pip(pipCan_in, cutLevel)); }
    }
    return passCut;
}

// ------------------------------------------------------------
// Custom electron detector (full) wrapper
// ------------------------------------------------------------
def isElectronFull(def eleCan){
    boolean PID_norm                = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "PID");
    boolean CC_NPHE_norm            = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "CC_NPHE");

    boolean EC_OUTER_VS_INNER_loose = isElectronCustom(eleCan, cutLevel = "loose", cut_return = "EC_OUTER_VS_INNER");
    boolean EC_OUTER_VS_INNER_mid   = isElectronCustom(eleCan, cutLevel = "mid",   cut_return = "EC_OUTER_VS_INNER");
    boolean EC_OUTER_VS_INNER_tight = isElectronCustom(eleCan, cutLevel = "tight", cut_return = "EC_OUTER_VS_INNER");
    boolean EC_OUTER_VS_INNER_norm  = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "EC_OUTER_VS_INNER");

    boolean EC_SAMPLING_loose       = isElectronCustom(eleCan, cutLevel = "loose", cut_return = "EC_SAMPLING");
    boolean EC_SAMPLING_mid         = isElectronCustom(eleCan, cutLevel = "mid",   cut_return = "EC_SAMPLING");
    boolean EC_SAMPLING_tight       = isElectronCustom(eleCan, cutLevel = "tight", cut_return = "EC_SAMPLING");
    boolean EC_SAMPLING_norm        = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "EC_SAMPLING");

    boolean EC_FIDUCIAL_loose       = isElectronCustom(eleCan, cutLevel = "loose", cut_return = "EC_FIDUCIAL");
    boolean EC_FIDUCIAL_mid         = isElectronCustom(eleCan, cutLevel = "mid",   cut_return = "EC_FIDUCIAL");
    boolean EC_FIDUCIAL_tight       = isElectronCustom(eleCan, cutLevel = "tight", cut_return = "EC_FIDUCIAL");
    boolean EC_FIDUCIAL_norm        = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "EC_FIDUCIAL");

    boolean DC_FIDUCIAL_REG1_loose  = isElectronCustom(eleCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_mid    = isElectronCustom(eleCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_tight  = isElectronCustom(eleCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_norm   = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "DC_FIDUCIAL_REG1");

    boolean DC_FIDUCIAL_REG2_loose  = isElectronCustom(eleCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_mid    = isElectronCustom(eleCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_tight  = isElectronCustom(eleCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_norm   = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "DC_FIDUCIAL_REG2");

    boolean DC_FIDUCIAL_REG3_loose  = isElectronCustom(eleCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_mid    = isElectronCustom(eleCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_tight  = isElectronCustom(eleCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_norm   = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "DC_FIDUCIAL_REG3");

    boolean DC_FIDUCIAL_REG_loose   = (DC_FIDUCIAL_REG1_loose && DC_FIDUCIAL_REG2_loose && DC_FIDUCIAL_REG3_loose);
    boolean DC_FIDUCIAL_REG_mid     = (DC_FIDUCIAL_REG1_mid   && DC_FIDUCIAL_REG2_mid   && DC_FIDUCIAL_REG3_mid);
    boolean DC_FIDUCIAL_REG_tight   = (DC_FIDUCIAL_REG1_tight && DC_FIDUCIAL_REG2_tight && DC_FIDUCIAL_REG3_tight);
    boolean DC_FIDUCIAL_REG_norm    = (DC_FIDUCIAL_REG1_norm  && DC_FIDUCIAL_REG2_norm  && DC_FIDUCIAL_REG3_norm);

    boolean DC_VERTEX_loose         = isElectronCustom(eleCan, cutLevel = "loose", cut_return = "DC_VERTEX");
    boolean DC_VERTEX_mid           = isElectronCustom(eleCan, cutLevel = "mid",   cut_return = "DC_VERTEX");
    boolean DC_VERTEX_tight         = isElectronCustom(eleCan, cutLevel = "tight", cut_return = "DC_VERTEX");
    boolean DC_VERTEX_norm          = isElectronCustom(eleCan, cutLevel = "norm",  cut_return = "DC_VERTEX");

    boolean Full_loose = (PID_norm && CC_NPHE_norm && EC_OUTER_VS_INNER_loose && EC_SAMPLING_loose && EC_FIDUCIAL_loose && DC_FIDUCIAL_REG1_loose && DC_FIDUCIAL_REG2_loose && DC_FIDUCIAL_REG3_loose && DC_FIDUCIAL_REG_loose && DC_VERTEX_loose);
    boolean Full_mid   = (PID_norm && CC_NPHE_norm && EC_OUTER_VS_INNER_mid   && EC_SAMPLING_mid   && EC_FIDUCIAL_mid   && DC_FIDUCIAL_REG1_mid   && DC_FIDUCIAL_REG2_mid   && DC_FIDUCIAL_REG3_mid   && DC_FIDUCIAL_REG_mid   && DC_VERTEX_mid);
    boolean Full_tight = (PID_norm && CC_NPHE_norm && EC_OUTER_VS_INNER_tight && EC_SAMPLING_tight && EC_FIDUCIAL_tight && DC_FIDUCIAL_REG1_tight && DC_FIDUCIAL_REG2_tight && DC_FIDUCIAL_REG3_tight && DC_FIDUCIAL_REG_tight && DC_VERTEX_tight);
    boolean Full_norm  = (PID_norm && CC_NPHE_norm && EC_OUTER_VS_INNER_norm  && EC_SAMPLING_norm  && EC_FIDUCIAL_norm  && DC_FIDUCIAL_REG1_norm  && DC_FIDUCIAL_REG2_norm  && DC_FIDUCIAL_REG3_norm  && DC_FIDUCIAL_REG_norm  && DC_VERTEX_norm);

    if( !( (Full_mid == Full_norm) && (Full_norm == eleCan.iselectron()) ) ) {
        System.out.println("");
        System.out.println("ERROR: My Custom Electron (mid) Cuts do not match the normal cut returns...");
    }

    return [
        Full_norm               : Full_norm,
        Full_tight              : Full_tight,
        Full_mid                : Full_mid,
        Full_loose              : Full_loose,
        DC_VERTEX_norm          : DC_VERTEX_norm,
        DC_VERTEX_tight         : DC_VERTEX_tight,
        DC_VERTEX_mid           : DC_VERTEX_mid,
        DC_VERTEX_loose         : DC_VERTEX_loose,
        DC_FIDUCIAL_REG_norm    : DC_FIDUCIAL_REG_norm,
        DC_FIDUCIAL_REG_tight   : DC_FIDUCIAL_REG_tight,
        DC_FIDUCIAL_REG_mid     : DC_FIDUCIAL_REG_mid,
        DC_FIDUCIAL_REG_loose   : DC_FIDUCIAL_REG_loose,
        DC_FIDUCIAL_REG3_norm   : DC_FIDUCIAL_REG3_norm,
        DC_FIDUCIAL_REG3_tight  : DC_FIDUCIAL_REG3_tight,
        DC_FIDUCIAL_REG3_mid    : DC_FIDUCIAL_REG3_mid,
        DC_FIDUCIAL_REG3_loose  : DC_FIDUCIAL_REG3_loose,
        DC_FIDUCIAL_REG2_norm   : DC_FIDUCIAL_REG2_norm,
        DC_FIDUCIAL_REG2_tight  : DC_FIDUCIAL_REG2_tight,
        DC_FIDUCIAL_REG2_mid    : DC_FIDUCIAL_REG2_mid,
        DC_FIDUCIAL_REG2_loose  : DC_FIDUCIAL_REG2_loose,
        DC_FIDUCIAL_REG1_norm   : DC_FIDUCIAL_REG1_norm,
        DC_FIDUCIAL_REG1_tight  : DC_FIDUCIAL_REG1_tight,
        DC_FIDUCIAL_REG1_mid    : DC_FIDUCIAL_REG1_mid,
        DC_FIDUCIAL_REG1_loose  : DC_FIDUCIAL_REG1_loose,
        EC_FIDUCIAL_norm        : EC_FIDUCIAL_norm,
        EC_FIDUCIAL_tight       : EC_FIDUCIAL_tight,
        EC_FIDUCIAL_mid         : EC_FIDUCIAL_mid,
        EC_FIDUCIAL_loose       : EC_FIDUCIAL_loose,
        EC_SAMPLING_norm        : EC_SAMPLING_norm,
        EC_SAMPLING_tight       : EC_SAMPLING_tight,
        EC_SAMPLING_mid         : EC_SAMPLING_mid,
        EC_SAMPLING_loose       : EC_SAMPLING_loose,
        EC_OUTER_VS_INNER_norm  : EC_OUTER_VS_INNER_norm,
        EC_OUTER_VS_INNER_tight : EC_OUTER_VS_INNER_tight,
        EC_OUTER_VS_INNER_mid   : EC_OUTER_VS_INNER_mid,
        EC_OUTER_VS_INNER_loose : EC_OUTER_VS_INNER_loose,
        CC_NPHE_norm            : CC_NPHE_norm,
        PID_norm                : PID_norm
    ];
}

// ------------------------------------------------------------
// Custom pi+ pion detector (full) wrapper
// ------------------------------------------------------------
def isPipFull(def pipCan){
    boolean PID_norm                = isPipCustom(pipCan, "norm",  "PID");
    boolean FORWARD_norm            = isPipCustom(pipCan, "norm",  "FORWARD");
    
    boolean CHI2PID_CUT_loose       = isPipCustom(pipCan, "loose", "CHI2PID_CUT");
    boolean CHI2PID_CUT_mid         = isPipCustom(pipCan, "mid",   "CHI2PID_CUT");
    boolean CHI2PID_CUT_tight       = isPipCustom(pipCan, "tight", "CHI2PID_CUT");
    boolean CHI2PID_CUT_norm        = isPipCustom(pipCan, "norm",  "CHI2PID_CUT");

    boolean DC_FIDUCIAL_REG1_loose  = isPipCustom(pipCan, "loose", "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_mid    = isPipCustom(pipCan, "mid",   "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_tight  = isPipCustom(pipCan, "tight", "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_norm   = isPipCustom(pipCan, "norm",  "DC_FIDUCIAL_REG1");

    boolean DC_FIDUCIAL_REG2_loose  = isPipCustom(pipCan, "loose", "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_mid    = isPipCustom(pipCan, "mid",   "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_tight  = isPipCustom(pipCan, "tight", "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_norm   = isPipCustom(pipCan, "norm",  "DC_FIDUCIAL_REG2");

    boolean DC_FIDUCIAL_REG3_loose  = isPipCustom(pipCan, "loose", "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_mid    = isPipCustom(pipCan, "mid",   "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_tight  = isPipCustom(pipCan, "tight", "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_norm   = isPipCustom(pipCan, "norm",  "DC_FIDUCIAL_REG3");

    boolean DC_FIDUCIAL_REG_loose   = (DC_FIDUCIAL_REG1_loose && DC_FIDUCIAL_REG2_loose && DC_FIDUCIAL_REG3_loose);
    boolean DC_FIDUCIAL_REG_mid     = (DC_FIDUCIAL_REG1_mid   && DC_FIDUCIAL_REG2_mid   && DC_FIDUCIAL_REG3_mid);
    boolean DC_FIDUCIAL_REG_tight   = (DC_FIDUCIAL_REG1_tight && DC_FIDUCIAL_REG2_tight && DC_FIDUCIAL_REG3_tight);
    boolean DC_FIDUCIAL_REG_norm    = (DC_FIDUCIAL_REG1_norm  && DC_FIDUCIAL_REG2_norm  && DC_FIDUCIAL_REG3_norm);

    boolean DELTA_VZ_loose          = isPipCustom(pipCan, "loose", "DELTA_VZ");
    boolean DELTA_VZ_mid            = isPipCustom(pipCan, "mid",   "DELTA_VZ");
    boolean DELTA_VZ_tight          = isPipCustom(pipCan, "tight", "DELTA_VZ");
    boolean DELTA_VZ_norm           = isPipCustom(pipCan, "norm",  "DELTA_VZ");

    boolean Full_loose = (PID_norm && FORWARD_norm && CHI2PID_CUT_loose && DC_FIDUCIAL_REG1_loose && DC_FIDUCIAL_REG2_loose && DC_FIDUCIAL_REG3_loose && DC_FIDUCIAL_REG_loose && DELTA_VZ_loose);
    boolean Full_mid   = (PID_norm && FORWARD_norm && CHI2PID_CUT_mid   && DC_FIDUCIAL_REG1_mid   && DC_FIDUCIAL_REG2_mid   && DC_FIDUCIAL_REG3_mid   && DC_FIDUCIAL_REG_mid   && DELTA_VZ_mid);
    boolean Full_tight = (PID_norm && FORWARD_norm && CHI2PID_CUT_tight && DC_FIDUCIAL_REG1_tight && DC_FIDUCIAL_REG2_tight && DC_FIDUCIAL_REG3_tight && DC_FIDUCIAL_REG_tight && DELTA_VZ_tight)
    boolean Full_norm  = (PID_norm && FORWARD_norm && CHI2PID_CUT_norm  && DC_FIDUCIAL_REG1_norm  && DC_FIDUCIAL_REG2_norm  && DC_FIDUCIAL_REG3_norm  && DC_FIDUCIAL_REG_norm  && DELTA_VZ_norm);

    if( !( (Full_mid == Full_norm) && (Full_norm == pipCan.ispip()) ) ) {
        System.out.println("");
        System.out.println("ERROR: My Custom Pi+ (mid) Cuts do not match the normal cut returns...");
    }

    return [
        Full_norm              : Full_norm,
        Full_tight             : Full_tight,
        Full_mid               : Full_mid,
        Full_loose             : Full_loose,

        DELTA_VZ_norm          : DELTA_VZ_norm,
        DELTA_VZ_tight         : DELTA_VZ_tight,
        DELTA_VZ_mid           : DELTA_VZ_mid,
        DELTA_VZ_loose         : DELTA_VZ_loose,

        DC_FIDUCIAL_REG_norm   : DC_FIDUCIAL_REG_norm,
        DC_FIDUCIAL_REG_tight  : DC_FIDUCIAL_REG_tight,
        DC_FIDUCIAL_REG_mid    : DC_FIDUCIAL_REG_mid,
        DC_FIDUCIAL_REG_loose  : DC_FIDUCIAL_REG_loose,

        DC_FIDUCIAL_REG3_norm  : DC_FIDUCIAL_REG3_norm,
        DC_FIDUCIAL_REG3_tight : DC_FIDUCIAL_REG3_tight,
        DC_FIDUCIAL_REG3_mid   : DC_FIDUCIAL_REG3_mid,
        DC_FIDUCIAL_REG3_loose : DC_FIDUCIAL_REG3_loose,

        DC_FIDUCIAL_REG2_norm  : DC_FIDUCIAL_REG2_norm,
        DC_FIDUCIAL_REG2_tight : DC_FIDUCIAL_REG2_tight,
        DC_FIDUCIAL_REG2_mid   : DC_FIDUCIAL_REG2_mid,
        DC_FIDUCIAL_REG2_loose : DC_FIDUCIAL_REG2_loose,

        DC_FIDUCIAL_REG1_norm  : DC_FIDUCIAL_REG1_norm,
        DC_FIDUCIAL_REG1_tight : DC_FIDUCIAL_REG1_tight,
        DC_FIDUCIAL_REG1_mid   : DC_FIDUCIAL_REG1_mid,
        DC_FIDUCIAL_REG1_loose : DC_FIDUCIAL_REG1_loose,

        CHI2PID_CUT_norm       : CHI2PID_CUT_norm,
        CHI2PID_CUT_tight      : CHI2PID_CUT_tight,
        CHI2PID_CUT_mid        : CHI2PID_CUT_mid,
        CHI2PID_CUT_loose      : CHI2PID_CUT_loose,

        FORWARD_norm           : FORWARD_norm,
        PID_norm               : PID_norm
    ];
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
    def schemas     = ['RUN::config', 'REC::Event', 'REC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator', 'MC::Particle', 'MC::Lund', 'MC::RecMatch'].collect{factory.getSchema(it)}
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

            def (runb, evb, partb, ecb, ccb, trajb, scb, MCpart, lund, RecMatch) = banks
            
            def run            = runb.getInt("run",   0)
            def evn            = runb.getInt("event", 0)
            
            def canele         = ElectronCandidate.getElectronCandidate(0, partb, ecb, ccb, trajb, isinb)
            def ele            = canele.getLorentzVector()
            
            def beamCharge     = evb.getFloat("beamCharge", 0)
            
            def electron_PIDs  = isElectronFull(canele);

            num_of_rec_ele_candidates += 1;
            //==================================================//
            //==========//   Electron (REC) Found   //==========//
            //==================================================//
            if(electron_PIDs.Full_norm || electron_PIDs.Full_tight || electron_PIDs.Full_mid || electron_PIDs.Full_loose || canele.iselectron()){
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

                    def pip_pion_PIDs  = isPipFull(canpip);
                    //==================================================//
                    //==========//   Pi+ Pion (REC) Found   //==========//
                    //==================================================//
                    if(pip_pion_PIDs.Full_norm || pip_pion_PIDs.Full_tight || pip_pion_PIDs.Full_mid || pip_pion_PIDs.Full_loose || canpip.ispip()){
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

                        def match_bankE = matchBasedonHIPObanks(RecMatch, MCpart, lund,     0, ABS_TOL, REL_TOL) // Electron Bank Matching
                        def match_bankP = matchBasedonHIPObanks(RecMatch, MCpart, lund, ipart, ABS_TOL, REL_TOL) // pi+ Pion Bank Matching

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
                            num_of_total_matched += 1;
                            if(canpip.ispip() && canele.iselectron()){ num_of_true_matched += 1; }   // Made to count the difference caused by the (normal) cut variation
                            if(electron_PIDs.Full_tight && pip_pion_PIDs.Full_tight){ num_of_strict_matched += 1; } // Made to count the difference caused by the (strict) cut variation
                            
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
                                match_P10T4.parentPID_el,      match_P10T4.parentPID_pi,

                                // Using Bank Matching
                                match_bankE.matched_x_gen,     match_bankE.matched_y_gen,     match_bankE.matched_z_gen,     match_bankE.matched_E_gen,     match_bankE.pid_matched,
                                match_bankP.matched_x_gen,     match_bankP.matched_y_gen,     match_bankP.matched_z_gen,     match_bankP.matched_E_gen,     match_bankP.pid_matched,
                                match_bankE.quality_match,     match_bankP.quality_match,     match_bankE.parentPID,         match_bankP.parentPID,

                                // Electron PID Cuts
                                ConvertBoolean(electron_PIDs.Full_norm),              ConvertBoolean(electron_PIDs.Full_tight),              ConvertBoolean(electron_PIDs.Full_mid),              ConvertBoolean(electron_PIDs.Full_loose),
                                ConvertBoolean(electron_PIDs.DC_VERTEX_norm),         ConvertBoolean(electron_PIDs.DC_VERTEX_tight),         ConvertBoolean(electron_PIDs.DC_VERTEX_mid),         ConvertBoolean(electron_PIDs.DC_VERTEX_loose),
                                ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG_norm),   ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG_tight),   ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG_mid),   ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG_loose),
                                ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG3_norm),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG3_tight),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG3_mid),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG3_loose),
                                ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG2_norm),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG2_tight),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG2_mid),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG2_loose),
                                ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG1_norm),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG1_tight),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG1_mid),  ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG1_loose),
                                ConvertBoolean(electron_PIDs.EC_FIDUCIAL_norm),       ConvertBoolean(electron_PIDs.EC_FIDUCIAL_tight),       ConvertBoolean(electron_PIDs.EC_FIDUCIAL_mid),       ConvertBoolean(electron_PIDs.EC_FIDUCIAL_loose),
                                ConvertBoolean(electron_PIDs.EC_SAMPLING_norm),       ConvertBoolean(electron_PIDs.EC_SAMPLING_tight),       ConvertBoolean(electron_PIDs.EC_SAMPLING_mid),       ConvertBoolean(electron_PIDs.EC_SAMPLING_loose),
                                ConvertBoolean(electron_PIDs.EC_OUTER_VS_INNER_norm), ConvertBoolean(electron_PIDs.EC_OUTER_VS_INNER_tight), ConvertBoolean(electron_PIDs.EC_OUTER_VS_INNER_mid), ConvertBoolean(electron_PIDs.EC_OUTER_VS_INNER_loose),
                                ConvertBoolean(electron_PIDs.CC_NPHE_norm),           ConvertBoolean(electron_PIDs.PID_norm),
                                
                                // Pi+ Pion PID Cuts
                                ConvertBoolean(pip_pion_PIDs.Full_norm),              ConvertBoolean(pip_pion_PIDs.Full_tight),              ConvertBoolean(pip_pion_PIDs.Full_mid),              ConvertBoolean(pip_pion_PIDs.Full_loose),
                                ConvertBoolean(pip_pion_PIDs.DELTA_VZ_norm),          ConvertBoolean(pip_pion_PIDs.DELTA_VZ_tight),          ConvertBoolean(pip_pion_PIDs.DELTA_VZ_mid),          ConvertBoolean(pip_pion_PIDs.DELTA_VZ_loose),
                                ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG_norm),   ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG_tight),   ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG_mid),   ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG_loose),
                                ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG3_norm),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG3_tight),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG3_mid),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG3_loose),
                                ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG2_norm),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG2_tight),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG2_mid),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG2_loose),
                                ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG1_norm),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG1_tight),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG1_mid),  ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG1_loose),
                                ConvertBoolean(pip_pion_PIDs.CHI2PID_CUT_norm),       ConvertBoolean(pip_pion_PIDs.CHI2PID_CUT_tight),       ConvertBoolean(pip_pion_PIDs.CHI2PID_CUT_mid),       ConvertBoolean(pip_pion_PIDs.CHI2PID_CUT_loose),
                                ConvertBoolean(pip_pion_PIDs.FORWARD_norm),           ConvertBoolean(pip_pion_PIDs.PID_norm),

                                // Extra Variables for the electron PID refinement cuts:
                                canele.pcal_energy,                   canele.ecin_energy,                    canele.ecout_energy,                 canele.vz,
                                // Extra Variables for the pi+ pion PID refinement cuts:
                                canpip.chi2pid,                       canpip.dvz

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
System.out.println("True number of completly matched events (i.e., those that would have survived the normal PID cuts) = " + num_of_true_matched);
System.out.println("Number of completly matched events with the strictess PID cuts = " + num_of_strict_matched);

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

