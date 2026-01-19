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

// As of 1/18/2025:
def ff = new ROOTFile("Data_sidis_epip_richcap.${suff}.new7.${outname}.root")

// DC hits had to be separated into 3 values per particle per event (each layer is hit and stored separately within each event) - Updated on 7/25/2024
    // Added/renamed several variables to do this
    // Removed detector/layer info now that it is built into the other variables
    // Runs with 'new5'
    // Also added "Num_Pions" to help control events where the electron is counted twice (in case that is a previously overlooked issue)
def branches_string = 'event/I:runN/I:beamCharge:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Num_Pions/I:Hx:Hy:Hx_pip:Hy_pip:V_PCal:W_PCal:U_PCal:ele_x_DC_6:ele_y_DC_6:ele_z_DC_6:ele_x_DC_18:ele_y_DC_18:ele_z_DC_18:ele_x_DC_36:ele_y_DC_36:ele_z_DC_36:pip_x_DC_6:pip_y_DC_6:pip_z_DC_6:pip_x_DC_18:pip_y_DC_18:pip_z_DC_18:pip_x_DC_36:pip_y_DC_36:pip_z_DC_36'

// // Included on 12/22/2025 for '.new6.' files
// // Reconstructed PID Cut variations:
//     // Electrons
// branches_string += ':Full_norm_el/I:Full_tight_el/I:Full_mid_el/I:Full_loose_el/I'
// branches_string += ':DC_VERTEX_norm_el/I:DC_VERTEX_tight_el/I:DC_VERTEX_mid_el/I:DC_VERTEX_loose_el/I'
// branches_string += ':DC_FIDUCIAL_REG_norm_el/I:DC_FIDUCIAL_REG_tight_el/I:DC_FIDUCIAL_REG_mid_el/I:DC_FIDUCIAL_REG_loose_el/I'
// branches_string += ':DC_FIDUCIAL_REG3_norm_el/I:DC_FIDUCIAL_REG3_tight_el/I:DC_FIDUCIAL_REG3_mid_el/I:DC_FIDUCIAL_REG3_loose_el/I'
// branches_string += ':DC_FIDUCIAL_REG2_norm_el/I:DC_FIDUCIAL_REG2_tight_el/I:DC_FIDUCIAL_REG2_mid_el/I:DC_FIDUCIAL_REG2_loose_el/I'
// branches_string += ':DC_FIDUCIAL_REG1_norm_el/I:DC_FIDUCIAL_REG1_tight_el/I:DC_FIDUCIAL_REG1_mid_el/I:DC_FIDUCIAL_REG1_loose_el/I'
// branches_string += ':EC_FIDUCIAL_norm_el/I:EC_FIDUCIAL_tight_el/I:EC_FIDUCIAL_mid_el/I:EC_FIDUCIAL_loose_el/I'
// branches_string += ':EC_SAMPLING_norm_el/I:EC_SAMPLING_tight_el/I:EC_SAMPLING_mid_el/I:EC_SAMPLING_loose_el/I'
// branches_string += ':EC_OUTER_VS_INNER_norm_el/I:EC_OUTER_VS_INNER_tight_el/I:EC_OUTER_VS_INNER_mid_el/I:EC_OUTER_VS_INNER_loose_el/I'
// branches_string += ':CC_NPHE_norm_el/I:PID_norm_el/I'
//     // Pi+ Pions
// branches_string += ':Full_norm_pip/I:Full_tight_pip/I:Full_mid_pip/I:Full_loose_pip/I'
// branches_string += ':DELTA_VZ_norm_pip/I:DELTA_VZ_tight_pip/I:DELTA_VZ_mid_pip/I:DELTA_VZ_loose_pip/I'
// branches_string += ':DC_FIDUCIAL_REG_norm_pip/I:DC_FIDUCIAL_REG_tight_pip/I:DC_FIDUCIAL_REG_mid_pip/I:DC_FIDUCIAL_REG_loose_pip/I'
// branches_string += ':DC_FIDUCIAL_REG3_norm_pip/I:DC_FIDUCIAL_REG3_tight_pip/I:DC_FIDUCIAL_REG3_mid_pip/I:DC_FIDUCIAL_REG3_loose_pip/I'
// branches_string += ':DC_FIDUCIAL_REG2_norm_pip/I:DC_FIDUCIAL_REG2_tight_pip/I:DC_FIDUCIAL_REG2_mid_pip/I:DC_FIDUCIAL_REG2_loose_pip/I'
// branches_string += ':DC_FIDUCIAL_REG1_norm_pip/I:DC_FIDUCIAL_REG1_tight_pip/I:DC_FIDUCIAL_REG1_mid_pip/I:DC_FIDUCIAL_REG1_loose_pip/I'
// branches_string += ':CHI2PID_CUT_norm_pip/I:CHI2PID_CUT_tight_pip/I:CHI2PID_CUT_mid_pip/I:CHI2PID_CUT_loose_pip/I'
// branches_string += ':FORWARD_norm_pip/I:PID_norm_pip/I'
// // Additional Variables for PID Cuts:
// branches_string += ':pcal_energy:ecin_energy:ecout_energy:ele_DC_vertex_vz' // Electrons
// branches_string += ':pip_chi2pid:pip_dvz'                                   // Pi+ Pions


// Added as of 1/18/2026
// Electrons (from isElectronFull)
branches_string += ':EC_OUTER_VS_INNER_loose_el/I:EC_OUTER_VS_INNER_mid_el/I:EC_OUTER_VS_INNER_tight_el/I:EC_OUTER_VS_INNER_pass1_el/I'
branches_string += ':EC_SAMPLING_BAND_loose_el/I:EC_SAMPLING_BAND_mid_el/I:EC_SAMPLING_BAND_tight_el/I'
branches_string += ':EC_SAMPLING_TRIANGLE_mid_el/I'
branches_string += ':EC_SAMPLING_THRESHOLD_loose_el/I:EC_SAMPLING_THRESHOLD_mid_el/I:EC_SAMPLING_THRESHOLD_tight_el/I'
branches_string += ':EC_SAMPLING_pass2_el/I:EC_SAMPLING_pass1_el/I'
branches_string += ':EC_FIDUCIAL_loose_el/I:EC_FIDUCIAL_mid_el/I:EC_FIDUCIAL_tight_el/I:EC_FIDUCIAL_pass1_el/I'
branches_string += ':DC_FIDUCIAL_REG1_loose_el/I:DC_FIDUCIAL_REG1_mid_el/I:DC_FIDUCIAL_REG1_tight_el/I:DC_FIDUCIAL_REG1_pass1_el/I'
branches_string += ':DC_FIDUCIAL_REG2_loose_el/I:DC_FIDUCIAL_REG2_mid_el/I:DC_FIDUCIAL_REG2_tight_el/I:DC_FIDUCIAL_REG2_pass1_el/I'
branches_string += ':DC_FIDUCIAL_REG3_loose_el/I:DC_FIDUCIAL_REG3_mid_el/I:DC_FIDUCIAL_REG3_tight_el/I:DC_FIDUCIAL_REG3_pass1_el/I'
branches_string += ':DC_VERTEX_loose_el/I:DC_VERTEX_mid_el/I:DC_VERTEX_tight_el/I:DC_VERTEX_pass1_el/I'
branches_string += ':Min_PID_check_el/I:Full_default_el/I:Full_pass1_el/I'
// Extra variables used in the Electron PID refinement cuts (that were not already included in the initial `branches_string`)
branches_string += ':DC_Edge_R1e:DC_Edge_R2e:DC_Edge_R3e'
branches_string += ':Electron_Vz'
branches_string += ':PCAL_energy:ECin_energy:ECoutenergy'

// Pi+ (from isPipFull)
branches_string += ':CHI2PID_CUT_loose_pip/I:CHI2PID_CUT_mid_pip/I:CHI2PID_CUT_tight_pip/I:CHI2PID_CUT_pass1_pip/I'
branches_string += ':DC_FIDUCIAL_REG1_loose_pip/I:DC_FIDUCIAL_REG1_mid_pip/I:DC_FIDUCIAL_REG1_tight_pip/I:DC_FIDUCIAL_REG1_pass1_pip/I'
branches_string += ':DC_FIDUCIAL_REG2_loose_pip/I:DC_FIDUCIAL_REG2_mid_pip/I:DC_FIDUCIAL_REG2_tight_pip/I:DC_FIDUCIAL_REG2_pass1_pip/I'
branches_string += ':DC_FIDUCIAL_REG3_loose_pip/I:DC_FIDUCIAL_REG3_mid_pip/I:DC_FIDUCIAL_REG3_tight_pip/I:DC_FIDUCIAL_REG3_pass1_pip/I'
branches_string += ':DELTA_VZ_loose_pip/I:DELTA_VZ_mid_pip/I:DELTA_VZ_tight_pip/I:DELTA_VZ_pass1_pip/I'
branches_string += ':Min_PID_check_pip/I:Full_default_pip/I:Full_pass1_pip/I'
// Extra variables used in the Pion PID refinement cuts (that were not already included in the initial `branches_string`)
branches_string += ':DC_Edge_R1p:DC_Edge_R2p:DC_Edge_R3p'
branches_string += ':PID_chi2pip:PionDeltaVz'

def tt = ff.makeTree('h22', 'title', branches_string)

int event_count = 0;
int true_events = 0;
int pass1_cuts  = 0;
int DC_count    = 0;

int Multiple_Pions_Per_Electron = 0


// Helper: Converts booleans into integers (1 == true, 0 == false)
Integer ConvertBoolean(boolean bool) {
    if(bool) { return 1;}
    else {     return 0;}
}

// ============================================================
// Minimal DC-edge-only "candidate" object
// - Purpose: store DC edge values for regions 1..3
// - Adds PID in the same spirit as the other candidate classes
// - Does NOT modify/pass-through those classes at all
// ============================================================
class DCEdgeCandidate {
    int     ipart   = -1;
    Integer pid     = null;
    Double  edge_r1 = null;
    Double  edge_r2 = null;
    Double  edge_r3 = null;
    DCEdgeCandidate(int ipart_In) { ipart = ipart_In; }

    // Mirror the ElectronCandidate behavior: accept Number, store Integer (or null)
    void setPID(Number pid_In) { this.pid = (pid_In == null) ? null : pid_In.intValue(); }
    Integer getPID() { return pid; }
    Double getEdge(int region) {
        if((region == 1)) { return edge_r1; }
        if((region == 2)) { return edge_r2; }
        if((region == 3)) { return edge_r3; }
        return null;
    }
    // Builder: extract PID from recbank + DC edges from trajbank
    static DCEdgeCandidate getDCEdgeCandidate(int ipart_In, Bank recbank_In, Bank trajbank_In) {
        DCEdgeCandidate dcEdgeCan = new DCEdgeCandidate(ipart_In);
        // PID (same idea as upstream candidate builder)
        if((recbank_In != null)) { dcEdgeCan.setPID(recbank_In.getInt("pid", ipart_In)); }
        // DC edges
        if((trajbank_In == null)) { return dcEdgeCan; }
        int nrows = trajbank_In.getRows();
        for(int ir = 0; ir < nrows; ir++) {
            if((trajbank_In.getShort("pindex", ir) != (short)ipart_In)) { continue; }
            // if((trajbank_In.getByte("detector", ir) != DetectorType.DC.getDetectorId())) { continue; }  // DC detector ID should be 6
            if((trajbank_In.getByte("detector", ir) != 6)) { continue; }
            int layer = (int)trajbank_In.getByte("layer", ir);
            // Region 1: layer 6
            if((layer == 6))  { dcEdgeCan.edge_r1 = (double)trajbank_In.getFloat("edge", ir); }
            // Region 2: layer 18
            if((layer == 18)) { dcEdgeCan.edge_r2 = (double)trajbank_In.getFloat("edge", ir); }
            // Region 3: layer 36
            if((layer == 36)) { dcEdgeCan.edge_r3 = (double)trajbank_In.getFloat("edge", ir); }
        }
        return dcEdgeCan;
    }
}

// ------------------------------------------------------------
// Custom Electron PID Cuts
// ------------------------------------------------------------

def Custom_EC_OUTER_VS_INNER(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true; } // Turns off this cut
    def pcal_energy  = eleCan_In.pcal_energy;
    if(pcal_energy==null) { return false; }
    // final double edep_tight = 0.06, edep_medium = 0.07, edep_loose = 0.09; // For PASS 1
    final double edep_tight = 0.05, edep_medium = 0.06, edep_loose = 0.07, edep_loosest = 0.08; // For PASS 2
    double edep = edep_medium;
    if(cutLevel_In == "loose"){   edep = edep_loose; }
    if(cutLevel_In == "tight"){   edep = edep_tight; }
    if(cutLevel_In == "loosest"){ edep = edep_loosest; }
    return pcal_energy > edep;
}

def Custom_EC_SAMPLING(def eleCan_In, def cutLevel_In) { // This was built for Pass 1 (not Pass 2) — Replaced with `Custom_EC_SAMPLING_PASS2` and its composite functions
    if(cutLevel_In == "off") { return true; } // Turns off this cut
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

// ============================================================
// Pass-2 replacement for Custom_EC_SAMPLING (Fall2018 INB DATA)
// - Splits the sampling-fraction logic into 3 independent cuts:
//   (A) pass_band      : total SF band cut on (Ecal_total / p)
//   (B) pass_triangle  : partial SF “triangle” cut in (PCAL/p) vs (ECIN/p)
//   (C) pass_threshold : PCAL/p > threshold
// Can call the three parts individually, or call the wrapper.
// ============================================================

// (A) Total SF band cut
def Custom_EC_SAMPLING_PASS2_BAND(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true; } // Turns off this cut
    def pcal_sector  = eleCan_In.getPCALsector();
    def partp        = eleCan_In.p;
    def pcal_energy  = eleCan_In.pcal_energy;
    def ecin_energy  = eleCan_In.ecin_energy;
    def ecout_energy = eleCan_In.ecout_energy;
    if((pcal_sector==null) || (partp==null) || (pcal_energy==null) || (ecin_energy==null) || (ecout_energy==null)) { return false; }
    if((partp <= 0.0)) { return false; }

    // fall2018 inb: total SF parameters (array entries represent sectors 1..6)
    double[] p0mean_inb  = [ 0.111767,    0.116619,    0.114606,    0.116586,    0.118251,    0.117391    ] as double[];
    double[] p1mean_inb  = [-0.0281943,   0.0662751,  -0.0896597,   0.181465,    0.085993,    0.0186504   ] as double[];
    double[] p2mean_inb  = [ 0.00711137,  0.00633334,  0.00912098,  0.00652068,  0.00416682,  0.00622289  ] as double[];
    double[] p3mean_inb  = [-0.000878776,-0.000780257,-0.00108891,-0.000645957,-0.000485189,-0.000829729 ] as double[];

    double[] p0sigma_inb = [-0.00497609,  0.0259435,  0.0296159,   0.0161445,   0.0239166,   0.0244309   ] as double[];
    double[] p1sigma_inb = [ 0.0275006,  -0.000805156,-0.00449379,  0.0099462,   0.00192551,  0.00258059  ] as double[];
    double[] p2sigma_inb = [ 0.00253641, -0.00386759, -0.00469883, -0.00182968, -0.00355973, -0.00398967 ] as double[];
    double[] p3sigma_inb = [-0.000173549, 0.00030325,  0.000380195, 0.00012328,  0.000302528, 0.000340911] as double[];

    double sigma_range = 3.5;
    if((cutLevel_In == "loose")) { sigma_range = 4.0; }
    if((cutLevel_In == "tight")) { sigma_range = 3.0; }

    int isec = pcal_sector - 1;
    if((isec < 0) || (isec > 5)) { return false; }

    double ectotal_energy = pcal_energy + ecin_energy + ecout_energy;

    double partp2 = partp*partp;

    double mean  = p0mean_inb[isec]*(1.0 + partp/Math.sqrt(partp2 + p1mean_inb[isec])) + p2mean_inb[isec]*partp + p3mean_inb[isec]*partp2;

    double sigma = p0sigma_inb[isec] + p1sigma_inb[isec]/Math.sqrt(partp) + p2sigma_inb[isec]*partp + p3sigma_inb[isec]*partp2;

    double upper_lim_total = mean + sigma_range * sigma;
    double lower_lim_total = mean - sigma_range * sigma;

    boolean pass_band = ((ectotal_energy/partp) <= upper_lim_total);
    pass_band = pass_band && ((ectotal_energy/partp) >= lower_lim_total);

    return pass_band;
}

// (B) Partial SF “triangle” cut
//     (PCAL/p) > (p1 - p0*(ECIN/p))
def Custom_EC_SAMPLING_PASS2_TRIANGLE(def eleCan_In, def cutLevel_In) {
    if((cutLevel_In == "off") || (cutLevel_In == "loose") || (cutLevel_In == "loosest") ) { return true; } // This cut does not offer an easy way to vary it definitionally — will just treat the loose/tight comparison as being an "on" or "off" cut
    def pcal_sector  = eleCan_In.getPCALsector();
    def partp        = eleCan_In.p;
    def pcal_energy  = eleCan_In.pcal_energy;
    def ecin_energy  = eleCan_In.ecin_energy;
    if((pcal_sector==null) || (partp==null) || (pcal_energy==null) || (ecin_energy==null)) { return false; }
    if((partp <= 0.0)) { return false; }

    // fall2018 inb: triangle parameters (array entries are momentum bins)
    double[][] p0_inb = [
        [ 1.41582, 1.39934, 1.41204, 1.46385, 1.55892, 1.55892, 1.55892, 1.55892 ],  // sec1
        [ 1.44726, 1.44245, 1.47269, 1.53225, 1.61465, 1.61465, 1.61465, 1.61465 ],  // sec2
        [ 1.38589, 1.3908,  1.42501, 1.48177, 1.57636, 1.57636, 1.57636, 1.57636 ],  // sec3
        [ 1.38631, 1.38107, 1.39757, 1.44579, 1.54154, 1.54154, 1.54154, 1.54154 ],  // sec4
        [ 1.50251, 1.52408, 1.52996, 1.49583, 1.39339, 1.39339, 1.39339, 1.39339 ],  // sec5
        [ 1.51312, 1.52784, 1.57519, 1.67332, 1.85128, 1.85128, 1.85128, 1.85128 ]   // sec6
    ] as double[][];

    double[][] p1_inb = [
        [ 0.212225, 0.215542, 0.217,    0.218279, 0.219881, 0.219881, 0.219881, 0.219881 ],  // sec1
        [ 0.221991, 0.225772, 0.227888, 0.229099, 0.228898, 0.228898, 0.228898, 0.228898 ],  // sec2
        [ 0.221492, 0.225738, 0.227955, 0.228604, 0.22836,  0.22836,  0.22836,  0.22836  ],  // sec3
        [ 0.215784, 0.221511, 0.224982, 0.227812, 0.231076, 0.231076, 0.231076, 0.231076 ],  // sec4
        [ 0.22202,  0.227163, 0.228794, 0.226487, 0.218168, 0.218168, 0.218168, 0.218168 ],  // sec5
        [ 0.223651, 0.228082, 0.2305,   0.23241,  0.234238, 0.234238, 0.234238, 0.234238 ]   // sec6
    ] as double[][];

    int isec = pcal_sector - 1;
    if((isec < 0) || (isec > 5)) { return false; }

    int p_bin = 0;
    if((partp <= 3.0))                      { p_bin = 0; }
    if((partp > 3.0) && (partp <= 4.0))     { p_bin = 1; }
    if((partp > 4.0) && (partp <= 5.0))     { p_bin = 2; }
    if((partp > 5.0) && (partp <= 6.0))     { p_bin = 3; }
    if((partp > 6.0) && (partp <= 7.0))     { p_bin = 4; }
    if((partp > 7.0) && (partp <= 8.0))     { p_bin = 5; }
    if((partp > 8.0) && (partp <= 9.0))     { p_bin = 6; }
    if((partp > 9.0))                       { p_bin = 7; }

    double sf_pcal = pcal_energy/partp;
    double sf_ecin = ecin_energy/partp;

    double p0 = p0_inb[isec][p_bin];
    double p1 = p1_inb[isec][p_bin];

    boolean pass_triangle = (sf_pcal > (p1 - p0*sf_ecin));

    return pass_triangle;
}

// (C) PCAL/p threshold cut
def Custom_EC_SAMPLING_PASS2_THRESHOLD(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true; } // Turns off this cut
    def partp       = eleCan_In.p;
    def pcal_energy = eleCan_In.pcal_energy;
    if((partp==null) || (pcal_energy==null)) { return false; }
    if((partp <= 0.0)) { return false; }
    double min_threshold = 0.05;
    if(cutLevel_In == "loose"){ min_threshold = 0.045; }
    if(cutLevel_In == "tight"){ min_threshold = 0.065; }
    boolean pass_threshold = ((pcal_energy/partp) > min_threshold);
    return pass_threshold;
}

// Wrapper: “full Pass-2 sampling”
def Custom_EC_SAMPLING_PASS2(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true; } // Turns off this cut
    boolean pass_band      = Custom_EC_SAMPLING_PASS2_BAND(eleCan_In, cutLevel_In);
    boolean pass_triangle  = Custom_EC_SAMPLING_PASS2_TRIANGLE(eleCan_In, cutLevel_In);
    boolean pass_threshold = Custom_EC_SAMPLING_PASS2_THRESHOLD(eleCan_In, cutLevel_In);

    return pass_band && pass_triangle && pass_threshold;
}

def Custom_EC_FIDUCIAL(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true; } // Turns off this cut
    def pcal_sector = eleCan_In.getPCALsector();
    def lv          = eleCan_In.pcal_lv;
    def lw          = eleCan_In.pcal_lw;
    
    if(pcal_sector==null || lv==null || lw==null) { return false; }

    // Cut using the natural directions of the scintillator bars/ fibers:
    double[] min_v_tight_inb   = [19.0, 19.0, 19.0, 19.0, 19.0, 19.0] as double[];
    double[] min_v_med_inb     = [14.0, 14.0, 14.0, 14.0, 14.0, 14.0] as double[];
    // double[] min_v_loose_inb   = [9.0,  9.0,  9.0,  9.0,  9.0,  9.0 ] as double[]; // This is the default electron cut for PASS 1 beam-spin asymmetry measurements
    double[] min_v_loose_inb   = [9.0,  9.0,  9.0, 13.5,  9.0,  9.0 ] as double[]; // In PASS 2: "Since the PCAL is approximately 1 bar wider than the other calorimeter regions and since a proper cluster formation requires at least 1 bar (4.5 cm) distance to the edge, the loosest cut is defined as 2 bars (9.0 cm). The bar after this cut is completely reconstructed, with a moderate drop of the sampling fraction, which is identical for data and MC. Only for the v coordinate in sector 4, this cut is increased to 13.5 cm, due to a bar with a dead PMT for lower v values, leading to reconstruction problems for lower v values." — https://clasweb.jlab.org/wiki/images/c/cf/Fiducial_PID_RGA_pass2.pdf
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

    // if(lvl == Level.MEDIUM) { \\ In PASS 2: This is the default cut (3 bars + 0.5cm)
    // if(cutLevel_In == "tight") {
    min_v = min_v_med_inb[isec];
    max_v = max_v_med_inb[isec];
    min_w = min_w_med_inb[isec];
    max_w = max_w_med_inb[isec];
    // } else if(lvl == Level.TIGHT) {
    // } else 
    if(cutLevel_In == "tighter" || cutLevel_In == "tight") {
        min_v = min_v_tight_inb[isec];
        max_v = max_v_tight_inb[isec];
        min_w = min_w_tight_inb[isec];
        max_w = max_w_tight_inb[isec];
    // } else if(lvl == Level.LOOSEST) {
    } else if(cutLevel_In == "loose") {
        min_v = min_v_loose_inb[isec];
        max_v = max_v_loose_inb[isec];
        min_w = min_w_loose_inb[isec];
        max_w = max_w_loose_inb[isec];
    } else if(cutLevel_In == "loosest") {
        min_v = min_v_loosest_inb[isec];
        max_v = max_v_loosest_inb[isec];
        min_w = min_w_loosest_inb[isec];
        max_w = max_w_loosest_inb[isec];
    }

    return lv > min_v && lv < max_v && lw > min_w && lw < max_w;
}

def Custom_DC_FIDUCIAL_REG(def eleCan_In, def cutLevel_In, def region) { // Made for PASS 1
    if(cutLevel_In == "off") { return true; } // Turns off this cut
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
    // See MC clasdis file version for the Outbending cuts

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
    if(cutLevel_In == "off") { return true; } // Turns off this cut
    boolean isinbending = true;
    def pcal_sector     = eleCan_In.getPCALsector();
    def partvz          = eleCan_In.vz;

    if(pcal_sector==null || partvz==null ) { return false; }

    // These were for Pass 1
    // double[] vz_min_sect_inb  = [-13d, -13d, -13d, -13d, -13d, -13d];
    // double[] vz_max_sect_inb  = [ 12d,  12d,  12d,  12d,  12d,  12d];
    // double[] vz_min_sect_outb = [-20d, -20d, -20d, -20d, -20d, -20d];
    // double[] vz_max_sect_outb = [ 12d,  12d,  12d,  12d,  12d,  12d];
    // Below is updated for Pass 2
    double[] vz_min_sect_inb  = [-8d,  -8d,  -8d,  -8d,  -8d,  -8d];
    double[] vz_max_sect_inb  = [ 2d,   2d,   2d,   2d,   2d,   2d];
    double[] vz_min_sect_outb = [-11d, -11d, -11d, -11d, -11d, -11d];
    double[] vz_max_sect_outb = [ 1d,   1d,   1d,   1d,   1d,   1d];

    double level_var = 0d;
    if(cutLevel_In == 'loose') { level_var = -1.5d; }
    if(cutLevel_In == 'tight') { level_var =  1.0d; }

    int isec = pcal_sector - 1;
    double vz_min = (isinbending ? vz_min_sect_inb[isec]  : vz_min_sect_outb[isec]) + level_var;
    double vz_max = (isinbending ? vz_max_sect_inb[isec]  : vz_max_sect_outb[isec]) - level_var;

    return (partvz > vz_min) && (partvz < vz_max);
}

// ============================================================
// Pass-2 version of Custom_DC_FIDUCIAL_REG(eleCan_In, cutLevel_In, region)
// - Implements the Pass-2 DC edge cuts (inb/outb) from https://clasweb.jlab.org/wiki/images/c/cf/Fiducial_PID_RGA_pass2.pdf
// - Uses `DCEdgeCan_In` instead of `eleCan_In` or `pipCan_In` since this cut can/should be applied to both particles
// ============================================================
def Custom_DC_FIDUCIAL_REG_PASS2(def DCEdgeCan_In, def cutLevel_In, def region) {
    if(cutLevel_In == "off") { return true; } // Turns off this cut
    if((region == null)) { return false; }
    if((region != 1) && (region != 2) && (region != 3)) { return false; }
    def part_pid = DCEdgeCan_In.getPID();
    // def edge1    = DCEdgeCan_In.getEdge(1);
    // def edge2    = DCEdgeCan_In.getEdge(2);
    // def edge3    = DCEdgeCan_In.getEdge(3);
    def edge_val = DCEdgeCan_In.getEdge(region);

    if((part_pid == null) || (edge_val == null) ) { return false; }

    // --- Pass-2 DC edge cuts (arrays represent regions 1..3) ---
    double[] DCedge_ele_inb  = [5.0, 5.0, 10.0] as double[];
    double[] DCedge_prot_inb = [2.5, 2.5, 9.0 ] as double[];
    double[] DCedge_pip_inb  = [2.5, 2.5, 9.0 ] as double[];
    double[] DCedge_pim_inb  = [3.5, 3.0, 7.0 ] as double[];
    double[] DCedge_Kp_inb   = [2.5, 2.0, 9.0 ] as double[];
    double[] DCedge_Km_inb   = [3.5, 2.5, 5.0 ] as double[];

    double[] DCedge_ele_outb  = [3.0, 3.0, 10.0] as double[];
    double[] DCedge_prot_outb = [3.5, 3.0, 7.0 ] as double[];
    double[] DCedge_pip_outb  = [3.5, 2.5, 6.5 ] as double[];
    double[] DCedge_pim_outb  = [2.5, 2.5, 10.0] as double[];
    double[] DCedge_Kp_outb   = [3.5, 2.5, 6.5 ] as double[];
    double[] DCedge_Km_outb   = [2.5, 2.5, 10.0] as double[];
    double edge_cut = 0.0;
    int regIdx = region - 1;
    boolean outbending = false; // This script is for Inbending files only
    // --- Choose edge_cut based on bending, region, pid (same logic as colleague) ---
    if((outbending == false) && (part_pid == 11))    { edge_cut = DCedge_ele_inb[regIdx]; }
    if((outbending == false) && (part_pid == 2212))  { edge_cut = DCedge_prot_inb[regIdx]; }
    if((outbending == false) && (part_pid == 211))   { edge_cut = DCedge_pip_inb[regIdx]; }
    if((outbending == false) && (part_pid == -211))  { edge_cut = DCedge_pim_inb[regIdx]; }
    if((outbending == false) && (part_pid == 321))   { edge_cut = DCedge_Kp_inb[regIdx]; }
    if((outbending == false) && (part_pid == -321))  { edge_cut = DCedge_Km_inb[regIdx]; }

    if((outbending == true) && (part_pid == 11))     { edge_cut = DCedge_ele_outb[regIdx]; }
    if((outbending == true) && (part_pid == 2212))   { edge_cut = DCedge_prot_outb[regIdx]; }
    if((outbending == true) && (part_pid == 211))    { edge_cut = DCedge_pip_outb[regIdx]; }
    if((outbending == true) && (part_pid == -211))   { edge_cut = DCedge_pim_outb[regIdx]; }
    if((outbending == true) && (part_pid == 321))    { edge_cut = DCedge_Kp_outb[regIdx]; }
    if((outbending == true) && (part_pid == -321))   { edge_cut = DCedge_Km_outb[regIdx]; }

    if(cutLevel_In == 'loose') { 
        edge_cut = edge_cut - 1.0;
        if(part_pid == 11){ edge_cut = edge_cut - 0.5; }
    }
    if(cutLevel_In == 'tight') { 
        edge_cut = edge_cut + 1.0;
        if(part_pid == 11){ edge_cut = edge_cut + 0.5; }
    }
    if((edge_val > edge_cut)) { return true; }
    return false;
}


// ------------------------------------------------------------
// Custom Pi+ Pion PID Cuts
// ------------------------------------------------------------
def Custom_CHI2PID_CUT_pip(def pipCan_In, def cutLevel_In) {  // Made for Pass 1 but has no (generic) Pass 2 update (still needed, so will keep the same)
    if(cutLevel_In == "off") { return true; } // Turns off this cut
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

def Custom_DC_FIDUCIAL_REG_pip(def pipCan_In, def cutLevel_In, def region) { // Made for PASS 1 (See `Custom_DC_FIDUCIAL_REG_PASS2` as the replacement)
    if(cutLevel_In == "off") { return true; } // Turns off this cut
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
    // See MC clasdis file version for the Outbending cuts
    
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
def isElectronCustom(def eleCan_in, def DCEdgeCan_In, def cutLevel = "norm", def cut_return = "All") {

    boolean passCut = true;

    // Not impacted by 'cutLevel'
    if(cut_return == "PID"               || cut_return == "All" ) { passCut = passCut && eleCan_in.iselectron(ElectronCandidate.Cut.PID); }
    if(cut_return == "CC_NPHE"           || cut_return == "All" ) { passCut = passCut && eleCan_in.iselectron(ElectronCandidate.Cut.CC_NPHE); }
    
    if(cutLevel == "off"){ return passCut; } // cutLevel = off --> just the PID cuts without refinements
    // Cuts with different levels
    
    if(cut_return == "EC_OUTER_VS_INNER" || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.EC_OUTER_VS_INNER)); }
        else { passCut = (passCut && Custom_EC_OUTER_VS_INNER(eleCan_in, cutLevel)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "EC_SAMPLING_BAND") {      passCut = (passCut && Custom_EC_SAMPLING_PASS2_BAND(eleCan_in, cutLevel)); }
    if(cut_return == "EC_SAMPLING_TRIANGLE") {  passCut = (passCut && Custom_EC_SAMPLING_PASS2_TRIANGLE(eleCan_in, cutLevel)); }
    if(cut_return == "EC_SAMPLING_THRESHOLD") { passCut = (passCut && Custom_EC_SAMPLING_PASS2_THRESHOLD(eleCan_in, cutLevel)); }
    if(!passCut){return passCut;}

    if(cut_return == "EC_SAMPLING"       || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.EC_SAMPLING)); }
        else { passCut = (passCut && Custom_EC_SAMPLING_PASS2(eleCan_in, cutLevel)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "EC_FIDUCIAL"       || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.EC_FIDUCIAL)); }
        else { passCut = (passCut && Custom_EC_FIDUCIAL(eleCan_in, cutLevel)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG1"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.DC_FIDUCIAL_REG1)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan_In, cutLevel, 1)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG2"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.DC_FIDUCIAL_REG2)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan_In, cutLevel, 2)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG3"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.DC_FIDUCIAL_REG3)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan_In, cutLevel, 3)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_VERTEX"         || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && eleCan_in.iselectron(ElectronCandidate.Cut.DC_VERTEX)); }
        else { passCut = (passCut && Custom_DC_VERTEX(eleCan_in, cutLevel)); }
    }
    return passCut;
}

// ------------------------------------------------------------
// Custom pi+ pion detector (individual) wrapper
// ------------------------------------------------------------
def isPipCustom(def pipCan_in, def DCEdgeCan_In, def cutLevel = "norm", def cut_return = "All") {

    boolean passCut = true;

    // Not impacted by 'cutLevel'
    if(cut_return == "PID"               || cut_return == "All" ) { passCut = passCut && pipCan_in.ispip(PionCandidate.Cut.PID); }
    if(cut_return == "FORWARD"           || cut_return == "All" ) { passCut = passCut && pipCan_in.ispip(PionCandidate.Cut.FORWARD); }
    
    if(cutLevel == "off"){ return passCut; } // cutLevel = off --> just the PID cuts without refinements
    // Cuts with different levels
    
    if(cut_return == "CHI2PID_CUT"       || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.CHI2PID_CUT)); }
        else { passCut = (passCut && Custom_CHI2PID_CUT_pip(pipCan_in, cutLevel)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG1"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.DC_FIDUCIAL_REG1)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan_In, cutLevel, 1)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG2"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.DC_FIDUCIAL_REG2)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan_In, cutLevel, 2)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DC_FIDUCIAL_REG3"  || cut_return == "DC_FIDUCIAL_REG" || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.DC_FIDUCIAL_REG3)); }
        else { passCut = (passCut && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan_In, cutLevel, 3)); }
    }
    if(!passCut){return passCut;}

    if(cut_return == "DELTA_VZ"          || cut_return == "All" ) { 
        if(cutLevel == "pass1"){ passCut = (passCut && pipCan_in.ispip(PionCandidate.Cut.DELTA_VZ)); }
        else { passCut = (passCut && Custom_DELTA_VZ_pip(pipCan_in, cutLevel)); }
    }
    return passCut;
}

// ------------------------------------------------------------
// Custom electron detector (full) wrapper
// ------------------------------------------------------------
def isElectronFull(def eleCan, def DCEdgeCan){
    boolean PID_norm                    = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "norm",  cut_return = "PID");
    boolean CC_NPHE_norm                = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "norm",  cut_return = "CC_NPHE");

    // cutLevel = "mid" is the default for the pass 2 refinement cuts

    boolean EC_OUTER_VS_INNER_loose     = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "loose", cut_return = "EC_OUTER_VS_INNER");
    boolean EC_OUTER_VS_INNER_mid       = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "EC_OUTER_VS_INNER");
    boolean EC_OUTER_VS_INNER_tight     = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "tight", cut_return = "EC_OUTER_VS_INNER");
    boolean EC_OUTER_VS_INNER_pass1     = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "pass1", cut_return = "EC_OUTER_VS_INNER");

    boolean EC_SAMPLING_BAND_loose      = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "loose", cut_return = "EC_SAMPLING_BAND");
    boolean EC_SAMPLING_BAND_mid        = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "EC_SAMPLING_BAND");
    boolean EC_SAMPLING_BAND_tight      = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "tight", cut_return = "EC_SAMPLING_BAND");
    boolean EC_SAMPLING_TRIANGLE_mid    = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "EC_SAMPLING_TRIANGLE"); // Does not have variations (just 'on' or 'off')
    boolean EC_SAMPLING_THRESHOLD_loose = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "loose", cut_return = "EC_SAMPLING_THRESHOLD");
    boolean EC_SAMPLING_THRESHOLD_mid   = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "EC_SAMPLING_THRESHOLD");
    boolean EC_SAMPLING_THRESHOLD_tight = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "tight", cut_return = "EC_SAMPLING_THRESHOLD");
    boolean EC_SAMPLING_pass2           = (EC_SAMPLING_BAND_mid && EC_SAMPLING_TRIANGLE_mid && EC_SAMPLING_THRESHOLD_mid);
    boolean EC_SAMPLING_pass1           = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "pass1", cut_return = "EC_SAMPLING");

    boolean EC_FIDUCIAL_loose           = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "loose", cut_return = "EC_FIDUCIAL");
    boolean EC_FIDUCIAL_mid             = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "EC_FIDUCIAL");
    boolean EC_FIDUCIAL_tight           = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "tight", cut_return = "EC_FIDUCIAL");
    boolean EC_FIDUCIAL_pass1           = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "pass1", cut_return = "EC_FIDUCIAL");

    boolean DC_FIDUCIAL_REG1_loose      = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_mid        = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_tight      = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_pass1      = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "pass1", cut_return = "DC_FIDUCIAL_REG1");

    boolean DC_FIDUCIAL_REG2_loose      = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_mid        = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_tight      = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_pass1      = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "pass1", cut_return = "DC_FIDUCIAL_REG2");

    boolean DC_FIDUCIAL_REG3_loose     = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_mid       = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_tight     = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_pass1     = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "pass1", cut_return = "DC_FIDUCIAL_REG3");

    boolean DC_VERTEX_loose            = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "loose", cut_return = "DC_VERTEX");
    boolean DC_VERTEX_mid              = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "mid",   cut_return = "DC_VERTEX");
    boolean DC_VERTEX_tight            = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "tight", cut_return = "DC_VERTEX");
    boolean DC_VERTEX_pass1            = isElectronCustom(eleCan, DCEdgeCan, cutLevel = "pass1", cut_return = "DC_VERTEX");

    boolean Min_PID_check = (PID_norm      && CC_NPHE_norm);
    boolean Full_default  = (Min_PID_check && EC_OUTER_VS_INNER_mid   && EC_SAMPLING_pass2 && EC_FIDUCIAL_mid   && DC_FIDUCIAL_REG1_mid   && DC_FIDUCIAL_REG2_mid   && DC_FIDUCIAL_REG3_mid   && DC_VERTEX_mid);
    boolean Full_pass1    = (Min_PID_check && EC_OUTER_VS_INNER_pass1 && EC_SAMPLING_pass1 && EC_FIDUCIAL_pass1 && DC_FIDUCIAL_REG1_pass1 && DC_FIDUCIAL_REG2_pass1 && DC_FIDUCIAL_REG3_pass1 && DC_VERTEX_pass1);

    def DC_Edge_R1e = DCEdgeCan.getEdge(1);
    def DC_Edge_R2e = DCEdgeCan.getEdge(2);
    def DC_Edge_R3e = DCEdgeCan.getEdge(3);
    def Electron_Vz = eleCan.vz;
    def PCAL_energy = eleCan.pcal_energy;
    def ECin_energy = eleCan.ecin_energy;
    def ECoutenergy = eleCan.ecout_energy;

    return [
        EC_OUTER_VS_INNER_loose       : EC_OUTER_VS_INNER_loose,
        EC_OUTER_VS_INNER_mid         : EC_OUTER_VS_INNER_mid,
        EC_OUTER_VS_INNER_tight       : EC_OUTER_VS_INNER_tight,
        EC_OUTER_VS_INNER_pass1       : EC_OUTER_VS_INNER_pass1,
        EC_SAMPLING_BAND_loose        : EC_SAMPLING_BAND_loose,
        EC_SAMPLING_BAND_mid          : EC_SAMPLING_BAND_mid,
        EC_SAMPLING_BAND_tight        : EC_SAMPLING_BAND_tight,
        EC_SAMPLING_TRIANGLE_mid      : EC_SAMPLING_TRIANGLE_mid,
        EC_SAMPLING_THRESHOLD_loose   : EC_SAMPLING_THRESHOLD_loose,
        EC_SAMPLING_THRESHOLD_mid     : EC_SAMPLING_THRESHOLD_mid,
        EC_SAMPLING_THRESHOLD_tight   : EC_SAMPLING_THRESHOLD_tight,
        EC_SAMPLING_pass2             : EC_SAMPLING_pass2,
        EC_SAMPLING_pass1             : EC_SAMPLING_pass1,
        EC_FIDUCIAL_loose             : EC_FIDUCIAL_loose,
        EC_FIDUCIAL_mid               : EC_FIDUCIAL_mid,
        EC_FIDUCIAL_tight             : EC_FIDUCIAL_tight,
        EC_FIDUCIAL_pass1             : EC_FIDUCIAL_pass1,
        DC_FIDUCIAL_REG1_loose        : DC_FIDUCIAL_REG1_loose,
        DC_FIDUCIAL_REG1_mid          : DC_FIDUCIAL_REG1_mid,
        DC_FIDUCIAL_REG1_tight        : DC_FIDUCIAL_REG1_tight,
        DC_FIDUCIAL_REG1_pass1        : DC_FIDUCIAL_REG1_pass1,
        DC_FIDUCIAL_REG2_loose        : DC_FIDUCIAL_REG2_loose,
        DC_FIDUCIAL_REG2_mid          : DC_FIDUCIAL_REG2_mid,
        DC_FIDUCIAL_REG2_tight        : DC_FIDUCIAL_REG2_tight,
        DC_FIDUCIAL_REG2_pass1        : DC_FIDUCIAL_REG2_pass1,
        DC_FIDUCIAL_REG3_loose        : DC_FIDUCIAL_REG3_loose,
        DC_FIDUCIAL_REG3_mid          : DC_FIDUCIAL_REG3_mid,
        DC_FIDUCIAL_REG3_tight        : DC_FIDUCIAL_REG3_tight,
        DC_FIDUCIAL_REG3_pass1        : DC_FIDUCIAL_REG3_pass1,
        DC_VERTEX_loose               : DC_VERTEX_loose,
        DC_VERTEX_mid                 : DC_VERTEX_mid,
        DC_VERTEX_tight               : DC_VERTEX_tight,
        DC_VERTEX_pass1               : DC_VERTEX_pass1,
        Min_PID_check                 : Min_PID_check,
        Full_default                  : Full_default,
        Full_pass1                    : Full_pass1,
        DC_Edge_R1e                   : DC_Edge_R1e,
        DC_Edge_R2e                   : DC_Edge_R2e,
        DC_Edge_R3e                   : DC_Edge_R3e,
        Electron_Vz                   : Electron_Vz,
        PCAL_energy                   : PCAL_energy,
        ECin_energy                   : ECin_energy,
        ECoutenergy                   : ECoutenergy
    ];
}

// ------------------------------------------------------------
// Custom pi+ pion detector (full) wrapper
// ------------------------------------------------------------
def isPipFull(def pipCan, def DCEdgeCan){
    boolean PID_norm                = isPipCustom(pipCan, DCEdgeCan, "norm",  "PID");
    boolean FORWARD_norm            = isPipCustom(pipCan, DCEdgeCan, "norm",  "FORWARD");
    
    boolean CHI2PID_CUT_loose       = isPipCustom(pipCan, DCEdgeCan, "loose", "CHI2PID_CUT");
    boolean CHI2PID_CUT_mid         = isPipCustom(pipCan, DCEdgeCan, "mid",   "CHI2PID_CUT");
    boolean CHI2PID_CUT_tight       = isPipCustom(pipCan, DCEdgeCan, "tight", "CHI2PID_CUT");
    boolean CHI2PID_CUT_pass1       = isPipCustom(pipCan, DCEdgeCan, "pass1", "CHI2PID_CUT");

    boolean DC_FIDUCIAL_REG1_loose  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_mid    = isPipCustom(pipCan, DCEdgeCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_tight  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG1");
    boolean DC_FIDUCIAL_REG1_pass1  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "pass1", cut_return = "DC_FIDUCIAL_REG1");

    boolean DC_FIDUCIAL_REG2_loose  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_mid    = isPipCustom(pipCan, DCEdgeCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_tight  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG2");
    boolean DC_FIDUCIAL_REG2_pass1  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "pass1", cut_return = "DC_FIDUCIAL_REG2");

    boolean DC_FIDUCIAL_REG3_loose  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "loose", cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_mid    = isPipCustom(pipCan, DCEdgeCan, cutLevel = "mid",   cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_tight  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "tight", cut_return = "DC_FIDUCIAL_REG3");
    boolean DC_FIDUCIAL_REG3_pass1  = isPipCustom(pipCan, DCEdgeCan, cutLevel = "pass1", cut_return = "DC_FIDUCIAL_REG3");

    boolean DELTA_VZ_loose          = isPipCustom(pipCan, DCEdgeCan, "loose", "DELTA_VZ");
    boolean DELTA_VZ_mid            = isPipCustom(pipCan, DCEdgeCan, "mid",   "DELTA_VZ");
    boolean DELTA_VZ_tight          = isPipCustom(pipCan, DCEdgeCan, "tight", "DELTA_VZ");
    boolean DELTA_VZ_pass1          = isPipCustom(pipCan, DCEdgeCan, "pass1", "DELTA_VZ");

    boolean Min_PID_check = (PID_norm      && FORWARD_norm);
    boolean Full_default  = (Min_PID_check && CHI2PID_CUT_mid   && DELTA_VZ_mid   && DC_FIDUCIAL_REG1_mid   && DC_FIDUCIAL_REG2_mid   && DC_FIDUCIAL_REG3_mid);
    boolean Full_pass1    = (Min_PID_check && CHI2PID_CUT_pass1 && DELTA_VZ_pass1 && DC_FIDUCIAL_REG1_pass1 && DC_FIDUCIAL_REG2_pass1 && DC_FIDUCIAL_REG3_pass1);

    def DC_Edge_R1p = DCEdgeCan.getEdge(1);
    def DC_Edge_R2p = DCEdgeCan.getEdge(2);
    def DC_Edge_R3p = DCEdgeCan.getEdge(3);
    def PID_chi2pip = pipCan.chi2pid;
    def PionDeltaVz = pipCan.dvz;

    return [
        CHI2PID_CUT_loose             : CHI2PID_CUT_loose,
        CHI2PID_CUT_mid               : CHI2PID_CUT_mid,
        CHI2PID_CUT_tight             : CHI2PID_CUT_tight,
        CHI2PID_CUT_pass1             : CHI2PID_CUT_pass1,
        DC_FIDUCIAL_REG1_loose        : DC_FIDUCIAL_REG1_loose,
        DC_FIDUCIAL_REG1_mid          : DC_FIDUCIAL_REG1_mid,
        DC_FIDUCIAL_REG1_tight        : DC_FIDUCIAL_REG1_tight,
        DC_FIDUCIAL_REG1_pass1        : DC_FIDUCIAL_REG1_pass1,
        DC_FIDUCIAL_REG2_loose        : DC_FIDUCIAL_REG2_loose,
        DC_FIDUCIAL_REG2_mid          : DC_FIDUCIAL_REG2_mid,
        DC_FIDUCIAL_REG2_tight        : DC_FIDUCIAL_REG2_tight,
        DC_FIDUCIAL_REG2_pass1        : DC_FIDUCIAL_REG2_pass1,
        DC_FIDUCIAL_REG3_loose        : DC_FIDUCIAL_REG3_loose,
        DC_FIDUCIAL_REG3_mid          : DC_FIDUCIAL_REG3_mid,
        DC_FIDUCIAL_REG3_tight        : DC_FIDUCIAL_REG3_tight,
        DC_FIDUCIAL_REG3_pass1        : DC_FIDUCIAL_REG3_pass1,
        DELTA_VZ_loose                : DELTA_VZ_loose,
        DELTA_VZ_mid                  : DELTA_VZ_mid,
        DELTA_VZ_tight                : DELTA_VZ_tight,
        DELTA_VZ_pass1                : DELTA_VZ_pass1,
        Min_PID_check                 : Min_PID_check,
        Full_default                  : Full_default,
        Full_pass1                    : Full_pass1,
        DC_Edge_R1p                   : DC_Edge_R1p,
        DC_Edge_R2p                   : DC_Edge_R2p,
        DC_Edge_R3p                   : DC_Edge_R3p,
        PID_chi2pip                   : PID_chi2pip,
        PionDeltaVz                   : PionDeltaVz
    ];
}


GParsPool.withPool(2) {
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
            
            def skipqadb = false // Reusing the QADB as of 12/16/2025
            if(ismc || skipqadb || qa.pass(run, evn)){

                def canele = ElectronCandidate.getElectronCandidate(0, partb, ecb, ccb, trajb, isinb)
                def ele    = canele.getLorentzVector()
                def DC_ele = DCEdgeCandidate.getDCEdgeCandidate(0, partb, trajb)
                def beamCharge = evb.getFloat("beamCharge", 0)
                def electron_PIDs = isElectronFull(canele, DC_ele);

                if(electron_PIDs.Min_PID_check){ // A electron has been found (no refinement cuts added)
                    // elec_total_found += 1;
                    int pionCount = 0 // Counter for pions (helps control double-counted electrons)
                    
                    for(int ipart = 1; ipart < partb.getRows(); ipart++){
                        def canpip = PionCandidate.getPionCandidate(ipart,     partb, trajb, isinb)
                        def DC_pip = DCEdgeCandidate.getDCEdgeCandidate(ipart, partb, trajb)
                        def pip_pion_PIDs  = isPipFull(canpip, DC_pip);
                        if(pip_pion_PIDs.Min_PID_check){
                            // After this 'if' statement, the event being added to the ntuple is known to have at least one electron AND pi+ pion
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
                            
                            tt.fill(evn,      run,      beamCharge,        ex, ey, ez,        px, py, pz,
                                    esec,     pipsec,   pionCount,         Hx, Hy, Hx_pip,    Hy_pip,
                                    V_PCal,             W_PCal,            U_PCal, 
                                    ele_x_DC_6,         ele_y_DC_6,        ele_z_DC_6,
                                    ele_x_DC_18,        ele_y_DC_18,       ele_z_DC_18,
                                    ele_x_DC_36,        ele_y_DC_36,       ele_z_DC_36,
                                    pip_x_DC_6,         pip_y_DC_6,        pip_z_DC_6,
                                    pip_x_DC_18,        pip_y_DC_18,       pip_z_DC_18,
                                    pip_x_DC_36,        pip_y_DC_36,       pip_z_DC_36, 
                                   
                                    // Electron PID Refinement Cuts
                                    ConvertBoolean(electron_PIDs.EC_OUTER_VS_INNER_loose),      ConvertBoolean(electron_PIDs.EC_OUTER_VS_INNER_mid),        ConvertBoolean(electron_PIDs.EC_OUTER_VS_INNER_tight),      ConvertBoolean(electron_PIDs.EC_OUTER_VS_INNER_pass1),
                                    ConvertBoolean(electron_PIDs.EC_SAMPLING_BAND_loose),       ConvertBoolean(electron_PIDs.EC_SAMPLING_BAND_mid),         ConvertBoolean(electron_PIDs.EC_SAMPLING_BAND_tight),       ConvertBoolean(electron_PIDs.EC_SAMPLING_TRIANGLE_mid),
                                    ConvertBoolean(electron_PIDs.EC_SAMPLING_THRESHOLD_loose),  ConvertBoolean(electron_PIDs.EC_SAMPLING_THRESHOLD_mid),    ConvertBoolean(electron_PIDs.EC_SAMPLING_THRESHOLD_tight),  ConvertBoolean(electron_PIDs.EC_SAMPLING_pass2),            ConvertBoolean(electron_PIDs.EC_SAMPLING_pass1),
                                    ConvertBoolean(electron_PIDs.EC_FIDUCIAL_loose),            ConvertBoolean(electron_PIDs.EC_FIDUCIAL_mid),              ConvertBoolean(electron_PIDs.EC_FIDUCIAL_tight),            ConvertBoolean(electron_PIDs.EC_FIDUCIAL_pass1),
                                    ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG1_loose),       ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG1_mid),         ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG1_tight),       ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG1_pass1),
                                    ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG2_loose),       ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG2_mid),         ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG2_tight),       ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG2_pass1),
                                    ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG3_loose),       ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG3_mid),         ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG3_tight),       ConvertBoolean(electron_PIDs.DC_FIDUCIAL_REG3_pass1),
                                    ConvertBoolean(electron_PIDs.DC_VERTEX_loose),              ConvertBoolean(electron_PIDs.DC_VERTEX_mid),                ConvertBoolean(electron_PIDs.DC_VERTEX_tight),              ConvertBoolean(electron_PIDs.DC_VERTEX_pass1),
                                    // Combined PID Refinement Cut Booleans:
                                    ConvertBoolean(electron_PIDs.Min_PID_check),                ConvertBoolean(electron_PIDs.Full_default),                 ConvertBoolean(electron_PIDs.Full_pass1),
                                    // Extra Variables for the PID refinement cuts:
                                    electron_PIDs.DC_Edge_R1e, electron_PIDs.DC_Edge_R2e,       electron_PIDs.DC_Edge_R3e, electron_PIDs.Electron_Vz,       electron_PIDs.PCAL_energy, electron_PIDs.ECin_energy,       electron_PIDs.ECoutenergy,

                                    // Pi+ Pion PID Refinement Cuts
                                    ConvertBoolean(pip_pion_PIDs.CHI2PID_CUT_loose),            ConvertBoolean(pip_pion_PIDs.CHI2PID_CUT_mid),              ConvertBoolean(pip_pion_PIDs.CHI2PID_CUT_tight),            ConvertBoolean(pip_pion_PIDs.CHI2PID_CUT_pass1),
                                    ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG1_loose),       ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG1_mid),         ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG1_tight),       ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG1_pass1),
                                    ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG2_loose),       ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG2_mid),         ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG2_tight),       ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG2_pass1),
                                    ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG3_loose),       ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG3_mid),         ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG3_tight),       ConvertBoolean(pip_pion_PIDs.DC_FIDUCIAL_REG3_pass1),
                                    ConvertBoolean(pip_pion_PIDs.DELTA_VZ_loose),               ConvertBoolean(pip_pion_PIDs.DELTA_VZ_mid),                 ConvertBoolean(pip_pion_PIDs.DELTA_VZ_tight),               ConvertBoolean(pip_pion_PIDs.DELTA_VZ_pass1),
                                    // Combined PID Refinement Cut Booleans:
                                    ConvertBoolean(pip_pion_PIDs.Min_PID_check),                ConvertBoolean(pip_pion_PIDs.Full_default),                 ConvertBoolean(pip_pion_PIDs.Full_pass1),
                                    // Extra Variables for the PID refinement cuts:
                                    pip_pion_PIDs.DC_Edge_R1p, pip_pion_PIDs.DC_Edge_R2p,       pip_pion_PIDs.DC_Edge_R3p, pip_pion_PIDs.PID_chi2pip,       pip_pion_PIDs.PionDeltaVz)

                            if(pionCount > 1){ Multiple_Pions_Per_Electron += 1; }
                            if(pip_pion_PIDs.Full_default && electron_PIDs.Full_default){ true_events += 1; } // Made to count the difference caused by the Pass 2 PID refinement cuts
                            if(electron_PIDs.Full_pass1 && pip_pion_PIDs.Full_pass1){ pass1_cuts += 1; }      // Made to count the difference caused by the Pass 1 PID refinement cuts (i.e., the outdated cuts)
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
System.out.println("Total number of events found: " + event_count);
System.out.println("True number of events (i.e., those that would have survived the Pass 2 PID cuts) = " + true_events);
System.out.println("Total number of events that survived the original Pass 1 PID cuts = " + pass1_cuts);
System.out.println("");

System.out.println("Number of times that Multiple Pions were found per Electron = " + Multiple_Pions_Per_Electron);
System.out.println("");

long RunTime = (System.nanoTime() - StartTime)/1000000000;

if(RunTime > 60){
    RunTime = RunTime/60;
    if(RunTime > 60){
        RunTime = RunTime/60;
        System.out.println("This code's runtime (in hours) is: ");
    }
    else { System.out.println("This code's runtime (in min) is: "); }
}
else{ System.out.println("This code's runtime (in sec) is: "); }

System.out.println(RunTime);
System.out.println("");

tt.write()
ff.close()
