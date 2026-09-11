#!/usr/bin/env run-groovy
// Chapter 3 HIPO TTree job.
// One REAL nSidis HIPO file in, one ROOT file with a single h22 TTree out.
// Intended to be launched with run_groovy_scripts_with_emails.py --source data --script-path this file.
// Do not run this script on a machine that does not contain the HIPO inputs.
//
// h22 row kinds:
//   0 — PID trigger electron (particle 0)
//   1 — e-pi+ pair in a PID-electron event
//   2 — charge>0 hadron in a PID-electron event
// Optional cut combinations are applied later in plot_Chapter3_HIPO_hists.py.

import org.jlab.jnp.hipo4.io.HipoReader
import org.jlab.jnp.hipo4.data.Bank
import org.jlab.jnp.hipo4.data.Event
import org.jlab.jroot.ROOTFile
import uconn.utils.pid.stefan.ElectronCandidate
import uconn.utils.pid.stefan.PionCandidate
import clasqa.QADB
import my.Sugar

Sugar.enable()

def hipoPath = args[0]
def isinb = ! ( hipoPath.contains('outb') || hipoPath.contains('torus+1') )
def ismc  = hipoPath.contains("gemc")
def hipoName = hipoPath.split("/")[-1]

def farmChapter3Work  = new File("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Chapter3_Figures")
def farmChapter3WorkB = new File("/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Data_Files_Groovy/Chapter3_Figures")
def farmChapter3 = farmChapter3Work.exists() ? farmChapter3Work : farmChapter3WorkB
def chapter3Dir = null
try {
    def loc = getClass().protectionDomain?.codeSource?.location
    if(loc != null){
        File scriptFile
        try { scriptFile = new File(loc.toURI()) } catch(Exception e1){ scriptFile = new File(loc.getPath()) }
        if(scriptFile.isFile()){ chapter3Dir = scriptFile.getParentFile() }
        else if(scriptFile.isDirectory()){ chapter3Dir = scriptFile }
    }
} catch(Exception e){}
if(chapter3Dir == null || !new File(chapter3Dir, "plot_Chapter3_HIPO_hists.py").exists()){
    def sibling = new File("plot_Chapter3_HIPO_hists.py")
    if(sibling.exists()){ chapter3Dir = sibling.getAbsoluteFile().getParentFile() }
}
if(chapter3Dir == null || !new File(chapter3Dir, "plot_Chapter3_HIPO_hists.py").exists()){
    def parentSibling = new File("..", "plot_Chapter3_HIPO_hists.py")
    if(parentSibling.exists()){ chapter3Dir = parentSibling.getAbsoluteFile().getParentFile() }
}
if(chapter3Dir == null || !new File(chapter3Dir, "plot_Chapter3_HIPO_hists.py").exists()){
    chapter3Dir = farmChapter3
}

def outDirEnv = System.getenv("CHAPTER3_HIPO_OUTDIR")
def outDir = (outDirEnv != null && outDirEnv.trim() != "") ? outDirEnv.trim() : new File(chapter3Dir, "job_outputs").getAbsolutePath()
new File(outDir).mkdirs()
def rootName = "${outDir}/Chapter3_HIPO_hists_${hipoName}.root"

class DCEdgeCandidate {
    int     ipart   = -1
    Integer pid     = null
    Double  edge_r1 = null
    Double  edge_r2 = null
    Double  edge_r3 = null
    DCEdgeCandidate(int ipart_In) { ipart = ipart_In }
    Integer getPID() { return pid }
    Double getEdge(int region) {
        if(region == 1) { return edge_r1 }
        if(region == 2) { return edge_r2 }
        if(region == 3) { return edge_r3 }
        return null
    }
    static DCEdgeCandidate getDCEdgeCandidate(int ipart_In, Bank recbank_In, Bank trajbank_In) {
        DCEdgeCandidate dcEdgeCan = new DCEdgeCandidate(ipart_In)
        if(recbank_In != null) {
            dcEdgeCan.pid = recbank_In.getInt("pid", ipart_In)
        }
        if(trajbank_In == null) { return dcEdgeCan }
        int nrows = trajbank_In.getRows()
        for(int ir = 0; ir < nrows; ir++) {
            if(trajbank_In.getShort("pindex", ir) != (short)ipart_In) { continue }
            if(trajbank_In.getByte("detector", ir) != 6) { continue }
            int layer = (int)trajbank_In.getByte("layer", ir)
            if(layer == 6)  { dcEdgeCan.edge_r1 = (double)trajbank_In.getFloat("edge", ir) }
            if(layer == 18) { dcEdgeCan.edge_r2 = (double)trajbank_In.getFloat("edge", ir) }
            if(layer == 36) { dcEdgeCan.edge_r3 = (double)trajbank_In.getFloat("edge", ir) }
        }
        return dcEdgeCan
    }
}

float fval(def v) {
    if(v == null) { return Float.NaN }
    return (float) v
}

int particle_status(Bank partb, int ipart) {
    try {
        return (int) partb.getShort("status", ipart)
    } catch(Exception e) {
        return partb.getInt("status", ipart)
    }
}

double[] rotate_dc(double x, double y, double z, int sector){
    double angle = Math.toRadians(60.0) * (sector - 1)
    double yrot = y * Math.cos(angle) - x * Math.sin(angle)
    double xrot = y * Math.sin(angle) + x * Math.cos(angle)
    double tilt = -25.0 / 57.2958
    xrot = Math.sin(tilt) * z + Math.cos(tilt) * xrot
    return [xrot, yrot] as double[]
}

double htcc_nphe(Bank ccb){
    double nphe = 0.0
    if(ccb == null){ return nphe }
    for(int ii = 0; ii < ccb.getRows(); ii++){
        if(ccb.getShort("pindex", ii) == 0){
            nphe += (double) ccb.getFloat("nphe", ii)
        }
    }
    return nphe
}

def Custom_EC_OUTER_VS_INNER(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true }
    def pcal_energy = eleCan_In.pcal_energy
    if(pcal_energy==null) { return false }
    final double edep_tight = 0.05, edep_medium = 0.06, edep_loose = 0.07, edep_loosest = 0.08
    double edep = edep_medium
    if(cutLevel_In == "loose"){   edep = edep_loose }
    if(cutLevel_In == "tight"){   edep = edep_tight }
    if(cutLevel_In == "loosest"){ edep = edep_loosest }
    return pcal_energy > edep
}

def Custom_EC_SAMPLING_PASS2_BAND(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true }
    def pcal_sector  = eleCan_In.getPCALsector()
    def partp        = eleCan_In.p
    def pcal_energy  = eleCan_In.pcal_energy
    def ecin_energy  = eleCan_In.ecin_energy
    def ecout_energy = eleCan_In.ecout_energy
    if((pcal_sector==null) || (partp==null) || (pcal_energy==null) || (ecin_energy==null) || (ecout_energy==null)) { return false }
    if((partp <= 0.0)) { return false }
    double[] p0mean_inb  = [ 0.111767,    0.116619,    0.114606,    0.116586,    0.118251,    0.117391    ] as double[]
    double[] p1mean_inb  = [-0.0281943,   0.0662751,  -0.0896597,   0.181465,    0.085993,    0.0186504   ] as double[]
    double[] p2mean_inb  = [ 0.00711137,  0.00633334,  0.00912098,  0.00652068,  0.00416682,  0.00622289  ] as double[]
    double[] p3mean_inb  = [-0.000878776,-0.000780257,-0.00108891,-0.000645957,-0.000485189,-0.000829729 ] as double[]
    double[] p0sigma_inb = [-0.00497609,  0.0259435,  0.0296159,   0.0161445,   0.0239166,   0.0244309   ] as double[]
    double[] p1sigma_inb = [ 0.0275006,  -0.000805156,-0.00449379,  0.0099462,   0.00192551,  0.00258059  ] as double[]
    double[] p2sigma_inb = [ 0.00253641, -0.00386759, -0.00469883, -0.00182968, -0.00355973, -0.00398967 ] as double[]
    double[] p3sigma_inb = [-0.000173549, 0.00030325,  0.000380195, 0.00012328,  0.000302528, 0.000340911] as double[]
    double sigma_range = 3.5
    if((cutLevel_In == "loose")) { sigma_range = 4.0 }
    if((cutLevel_In == "tight")) { sigma_range = 3.0 }
    int isec = pcal_sector - 1
    if((isec < 0) || (isec > 5)) { return false }
    double ectotal_energy = pcal_energy + ecin_energy + ecout_energy
    double partp2 = partp*partp
    double mean  = p0mean_inb[isec]*(1.0 + partp/Math.sqrt(partp2 + p1mean_inb[isec])) + p2mean_inb[isec]*partp + p3mean_inb[isec]*partp2
    double sigma = p0sigma_inb[isec] + p1sigma_inb[isec]/Math.sqrt(partp) + p2sigma_inb[isec]*partp + p3sigma_inb[isec]*partp2
    double upper_lim_total = mean + sigma_range * sigma
    double lower_lim_total = mean - sigma_range * sigma
    return ((ectotal_energy/partp) <= upper_lim_total) && ((ectotal_energy/partp) >= lower_lim_total)
}

def Custom_EC_SAMPLING_PASS2_TRIANGLE(def eleCan_In, def cutLevel_In) {
    if((cutLevel_In == "off") || (cutLevel_In == "loose") || (cutLevel_In == "loosest") ) { return true }
    def pcal_sector  = eleCan_In.getPCALsector()
    def partp        = eleCan_In.p
    def pcal_energy  = eleCan_In.pcal_energy
    def ecin_energy  = eleCan_In.ecin_energy
    if((pcal_sector==null) || (partp==null) || (pcal_energy==null) || (ecin_energy==null)) { return false }
    if((partp <= 0.0)) { return false }
    double[][] p0_inb = [
        [ 1.41582, 1.39934, 1.41204, 1.46385, 1.55892, 1.55892, 1.55892, 1.55892 ],
        [ 1.44726, 1.44245, 1.47269, 1.53225, 1.61465, 1.61465, 1.61465, 1.61465 ],
        [ 1.38589, 1.3908,  1.42501, 1.48177, 1.57636, 1.57636, 1.57636, 1.57636 ],
        [ 1.38631, 1.38107, 1.39757, 1.44579, 1.54154, 1.54154, 1.54154, 1.54154 ],
        [ 1.50251, 1.52408, 1.52996, 1.49583, 1.39339, 1.39339, 1.39339, 1.39339 ],
        [ 1.51312, 1.52784, 1.57519, 1.67332, 1.85128, 1.85128, 1.85128, 1.85128 ]
    ] as double[][]
    double[][] p1_inb = [
        [ 0.212225, 0.215542, 0.217,    0.218279, 0.219881, 0.219881, 0.219881, 0.219881 ],
        [ 0.221991, 0.225772, 0.227888, 0.229099, 0.228898, 0.228898, 0.228898, 0.228898 ],
        [ 0.221492, 0.225738, 0.227955, 0.228604, 0.22836,  0.22836,  0.22836,  0.22836  ],
        [ 0.215784, 0.221511, 0.224982, 0.227812, 0.231076, 0.231076, 0.231076, 0.231076 ],
        [ 0.22202,  0.227163, 0.228794, 0.226487, 0.218168, 0.218168, 0.218168, 0.218168 ],
        [ 0.223651, 0.228082, 0.2305,   0.23241,  0.234238, 0.234238, 0.234238, 0.234238 ]
    ] as double[][]
    int isec = pcal_sector - 1
    if((isec < 0) || (isec > 5)) { return false }
    int p_bin = 0
    if((partp <= 3.0))                      { p_bin = 0 }
    if((partp > 3.0) && (partp <= 4.0))     { p_bin = 1 }
    if((partp > 4.0) && (partp <= 5.0))     { p_bin = 2 }
    if((partp > 5.0) && (partp <= 6.0))     { p_bin = 3 }
    if((partp > 6.0) && (partp <= 7.0))     { p_bin = 4 }
    if((partp > 7.0) && (partp <= 8.0))     { p_bin = 5 }
    if((partp > 8.0) && (partp <= 9.0))     { p_bin = 6 }
    if((partp > 9.0))                       { p_bin = 7 }
    return ((pcal_energy/partp) > (p1_inb[isec][p_bin] - p0_inb[isec][p_bin]*(ecin_energy/partp)))
}

def Custom_EC_SAMPLING_PASS2_THRESHOLD(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true }
    def partp       = eleCan_In.p
    def pcal_energy = eleCan_In.pcal_energy
    if((partp==null) || (pcal_energy==null)) { return false }
    if((partp <= 0.0)) { return false }
    double min_threshold = 0.05
    if(cutLevel_In == "loose"){ min_threshold = 0.045 }
    if(cutLevel_In == "tight"){ min_threshold = 0.065 }
    return ((pcal_energy/partp) > min_threshold)
}

def Custom_EC_SAMPLING_PASS2(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true }
    return Custom_EC_SAMPLING_PASS2_BAND(eleCan_In, cutLevel_In) && Custom_EC_SAMPLING_PASS2_TRIANGLE(eleCan_In, cutLevel_In) && Custom_EC_SAMPLING_PASS2_THRESHOLD(eleCan_In, cutLevel_In)
}

def Custom_EC_FIDUCIAL(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true }
    def pcal_sector = eleCan_In.getPCALsector()
    def lv          = eleCan_In.pcal_lv
    def lw          = eleCan_In.pcal_lw
    if(pcal_sector==null || lv==null || lw==null) { return false }
    double[] min_v_tight_inb   = [19.0, 19.0, 19.0, 19.0, 19.0, 19.0] as double[]
    double[] min_v_med_inb     = [14.0, 14.0, 14.0, 14.0, 14.0, 14.0] as double[]
    double[] min_v_loose_inb   = [9.0,  9.0,  9.0, 13.5,  9.0,  9.0 ] as double[]
    double[] min_v_loosest_inb = [5.0,  5.0,  5.0,  5.0,  5.0,  5.0 ] as double[]
    double[] max_v_inb         = [400, 400, 400, 400, 400, 400] as double[]
    double[] min_w_tight_inb   = [19.0, 19.0, 19.0, 19.0, 19.0, 19.0] as double[]
    double[] min_w_med_inb     = [14.0, 14.0, 14.0, 14.0, 14.0, 14.0] as double[]
    double[] min_w_loose_inb   = [9.0,  9.0,  9.0,  9.0,  9.0,  9.0 ] as double[]
    double[] min_w_loosest_inb = [5.0,  5.0,  5.0,  5.0,  5.0,  5.0 ] as double[]
    int isec = pcal_sector - 1
    double min_v = min_v_med_inb[isec]
    double max_v = max_v_inb[isec]
    double min_w = min_w_med_inb[isec]
    double max_w = max_v_inb[isec]
    if(cutLevel_In == "tighter" || cutLevel_In == "tight") {
        min_v = min_v_tight_inb[isec]; min_w = min_w_tight_inb[isec]
    } else if(cutLevel_In == "loose") {
        min_v = min_v_loose_inb[isec]; min_w = min_w_loose_inb[isec]
    } else if(cutLevel_In == "loosest") {
        min_v = min_v_loosest_inb[isec]; min_w = min_w_loosest_inb[isec]
    }
    return lv > min_v && lv < max_v && lw > min_w && lw < max_w
}

def Custom_DC_VERTEX(def eleCan_In, def cutLevel_In) {
    if(cutLevel_In == "off") { return true }
    def pcal_sector = eleCan_In.getPCALsector()
    def partvz      = eleCan_In.vz
    if(pcal_sector==null || partvz==null ) { return false }
    double[] vz_min_sect_inb = [-8d, -8d, -8d, -8d, -8d, -8d]
    double[] vz_max_sect_inb = [ 2d,  2d,  2d,  2d,  2d,  2d]
    double level_var = 0d
    if(cutLevel_In == 'loose') { level_var = -1.5d }
    if(cutLevel_In == 'tight') { level_var =  1.0d }
    int isec = pcal_sector - 1
    return (partvz > (vz_min_sect_inb[isec] + level_var)) && (partvz < (vz_max_sect_inb[isec] - level_var))
}

def Custom_DC_FIDUCIAL_REG_PASS2(def DCEdgeCan_In, def cutLevel_In, def region) {
    if(cutLevel_In == "off") { return true }
    if((region == null) || ((region != 1) && (region != 2) && (region != 3))) { return false }
    def part_pid = DCEdgeCan_In.getPID()
    def edge_val = DCEdgeCan_In.getEdge(region)
    if((part_pid == null) || (edge_val == null) ) { return false }
    double[] DCedge_ele_inb  = [5.0, 5.0, 10.0] as double[]
    double[] DCedge_pip_inb  = [2.5, 2.5, 9.0 ] as double[]
    int regIdx = region - 1
    double edge_cut = 0.0
    if(part_pid == 11)  { edge_cut = DCedge_ele_inb[regIdx] }
    if(part_pid == 211) { edge_cut = DCedge_pip_inb[regIdx] }
    if(cutLevel_In == 'loose') {
        edge_cut = edge_cut - 1.0
        if(part_pid == 11){ edge_cut = edge_cut - 0.5 }
    }
    if(cutLevel_In == 'tight') {
        edge_cut = edge_cut + 1.0
        if(part_pid == 11){ edge_cut = edge_cut + 0.5 }
    }
    return (edge_val > edge_cut)
}

boolean Baseline_Acceptable_Electron(def eleCan_In, def DCEdgeCan_In){
    if(eleCan_In.pcal_energy==null) {     return false }
    if(eleCan_In.getPCALsector()==null) { return false }
    if(eleCan_In.ecin_energy==null) {     return false }
    if(eleCan_In.ecout_energy==null) {    return false }
    def partp = eleCan_In.p
    if(partp==null || partp <= 0.0) {     return false }
    if(eleCan_In.pcal_lv==null) {         return false }
    if(eleCan_In.pcal_lw==null) {         return false }
    if(eleCan_In.vz==null) {              return false }
    if(DCEdgeCan_In.getEdge(1)==null) {   return false }
    if(DCEdgeCan_In.getEdge(2)==null) {   return false }
    if(DCEdgeCan_In.getEdge(3)==null) {   return false }
    return true
}

int all_electron_flag(def eleCan, def DCEdgeCan){
    if(!Baseline_Acceptable_Electron(eleCan, DCEdgeCan)) { return 0 }
    boolean ok = eleCan.iselectron(ElectronCandidate.Cut.PID)
    ok = ok && eleCan.iselectron(ElectronCandidate.Cut.CC_NPHE)
    ok = ok && Custom_EC_OUTER_VS_INNER(eleCan, "mid")
    ok = ok && Custom_EC_SAMPLING_PASS2(eleCan, "mid")
    ok = ok && Custom_EC_FIDUCIAL(eleCan, "mid")
    ok = ok && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan, "mid", 1)
    ok = ok && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan, "mid", 2)
    ok = ok && Custom_DC_FIDUCIAL_REG_PASS2(DCEdgeCan, "mid", 3)
    ok = ok && Custom_DC_VERTEX(eleCan, "mid")
    return ok ? 1 : 0
}

float pcal_hit_coord(Bank ecb, int ipart, String coord){
    for(int jj = 0; jj < ecb.getRows(); jj++){
        if((ecb.getShort("pindex", jj) == ipart) && (ecb.getByte("detector", jj) == 7) && (ecb.getByte("layer", jj) == 1)){
            return ecb.getFloat(coord, jj)
        }
    }
    return Float.NaN
}

def ff = new ROOTFile(rootName)
def branches_string = 'kind/I:nphe:pcal_energy:el_p:sftot:esec/I:vz:e_edge1:e_edge2:e_edge3:xrot1:yrot1:xrot2:yrot2:xrot3:yrot3:pip_status/I:pip_chi2pid:p_edge1:p_edge2:p_edge3:had_p:had_beta:had_status/I:had_chi2pid:h_edge1:h_edge2:h_edge3:all_electron/I:el_chi2pid:pip_p:dvz:Hx:Hy:V_PCal:W_PCal'
def tt = ff.makeTree('h22', 'title', branches_string)

float nanf = Float.NaN
int   nani = -1

QADB qa = new QADB("latest")
qa.checkForDefect('TotalOutlier')
qa.checkForDefect('TerminalOutlier')
qa.checkForDefect('MarginalOutlier')
qa.checkForDefect('SectorLoss')
qa.checkForDefect('Misc')
[5046, 5047, 5051, 5128, 5129, 5130, 5158, 5159, 5160, 5163, 5165, 5166, 5167, 5168, 5169, 5180, 5181, 5182, 5183, 5400, 5448, 5495, 5496, 5505, 5567, 5610, 5617, 5621, 5623, 6736, 6737, 6738, 6739, 6740, 6741, 6742, 6743, 6744, 6746, 6747, 6748, 6749, 6750, 6751, 6753, 6754, 6755, 6756, 6757].each{ run -> qa.allowMiscBit(run) }

def reader = new HipoReader()
reader.open(hipoPath)
def event = new Event()
def factory = reader.getSchemaFactory()
def banks = ['RUN::config','REC::Event','REC::Particle','REC::Calorimeter','REC::Cherenkov','REC::Traj','REC::Scintillator'].collect{ new Bank(factory.getSchema(it)) }

int nread = 0
int n_ele = 0
int n_elepip = 0
int n_had = 0
while(reader.hasNext()){
    reader.nextEvent(event)
    banks.each{ event.read(it) }
    if(!banks.every()){ continue }
    def (runb, evb, partb, ecb, ccb, trajb, scb) = banks
    def run = runb.getInt("run", 0)
    def evn = runb.getInt("event", 0)
    if(!(ismc || qa.pass(run, evn))){ continue }
    nread++

    def canele = ElectronCandidate.getElectronCandidate(0, partb, ecb, ccb, trajb, isinb)
    if(canele == null || !canele.iselectron(ElectronCandidate.Cut.PID)){ continue }

    def DC_ele = DCEdgeCandidate.getDCEdgeCandidate(0, partb, trajb)
    float nphe = (float) htcc_nphe(ccb)
    float pcalE = fval(canele.pcal_energy)
    float elp = fval(canele.p)
    float ecinE = fval(canele.ecin_energy)
    float ecoutE = fval(canele.ecout_energy)
    float sftot = Float.NaN
    if(!Float.isNaN(elp) && elp > 0 && !Float.isNaN(pcalE) && !Float.isNaN(ecinE) && !Float.isNaN(ecoutE)){
        sftot = (pcalE + ecinE + ecoutE) / elp
    }
    def pcalSec = canele.getPCALsector()
    int esec = (pcalSec != null) ? (int) pcalSec : -1
    float vz = fval(canele.vz)
    float e_edge1 = fval(DC_ele.getEdge(1))
    float e_edge2 = fval(DC_ele.getEdge(2))
    float e_edge3 = fval(DC_ele.getEdge(3))
    int all_ele = all_electron_flag(canele, DC_ele)
    float el_chi2pid = partb.getFloat("chi2pid", 0)
    float Hx = pcal_hit_coord(ecb, 0, "hx")
    float Hy = pcal_hit_coord(ecb, 0, "hy")
    float V_PCal = fval(canele.pcal_lv)
    float W_PCal = fval(canele.pcal_lw)

    float xrot1 = Float.NaN, yrot1 = Float.NaN
    float xrot2 = Float.NaN, yrot2 = Float.NaN
    float xrot3 = Float.NaN, yrot3 = Float.NaN
    float x6 = Float.NaN, y6 = Float.NaN, z6 = Float.NaN
    float x18 = Float.NaN, y18 = Float.NaN, z18 = Float.NaN
    float x36 = Float.NaN, y36 = Float.NaN, z36 = Float.NaN
    for(int ii = 0; ii < trajb.getRows(); ii++){
        if(trajb.getShort("pindex", ii) != 0){ continue }
        if(trajb.getByte("detector", ii) != 6){ continue }
        int layer = (int) trajb.getByte("layer", ii)
        if(layer == 6){  x6  = trajb.getFloat("x", ii); y6  = trajb.getFloat("y", ii); z6  = trajb.getFloat("z", ii) }
        if(layer == 18){ x18 = trajb.getFloat("x", ii); y18 = trajb.getFloat("y", ii); z18 = trajb.getFloat("z", ii) }
        if(layer == 36){ x36 = trajb.getFloat("x", ii); y36 = trajb.getFloat("y", ii); z36 = trajb.getFloat("z", ii) }
    }
    if(esec >= 1 && esec <= 6){
        if(!Float.isNaN(x6)){  def xy = rotate_dc(x6,  y6,  z6,  esec); xrot1 = (float)xy[0]; yrot1 = (float)xy[1] }
        if(!Float.isNaN(x18)){ def xy = rotate_dc(x18, y18, z18, esec); xrot2 = (float)xy[0]; yrot2 = (float)xy[1] }
        if(!Float.isNaN(x36)){ def xy = rotate_dc(x36, y36, z36, esec); xrot3 = (float)xy[0]; yrot3 = (float)xy[1] }
    }

    tt.fill(0, nphe, pcalE, elp, sftot, esec, vz, e_edge1, e_edge2, e_edge3,
            xrot1, yrot1, xrot2, yrot2, xrot3, yrot3,
            nani, nanf, nanf, nanf, nanf,
            nanf, nanf, nani, nanf, nanf, nanf, nanf,
            all_ele, el_chi2pid, nanf, nanf, Hx, Hy, V_PCal, W_PCal)
    n_ele++

    for(int ipart = 1; ipart < partb.getRows(); ipart++){
        def canpip = PionCandidate.getPionCandidate(ipart, partb, trajb, isinb)
        if(canpip != null && canpip.ispip(PionCandidate.Cut.PID)){
            def DC_pip = DCEdgeCandidate.getDCEdgeCandidate(ipart, partb, trajb)
            int pip_status = particle_status(partb, ipart)
            float pip_chi2pid = partb.getFloat("chi2pid", ipart)
            float pip_p = fval(canpip.p)
            float dvz = fval(canpip.dvz)
            tt.fill(1, nphe, pcalE, elp, sftot, esec, vz, e_edge1, e_edge2, e_edge3,
                    xrot1, yrot1, xrot2, yrot2, xrot3, yrot3,
                    pip_status, pip_chi2pid,
                    fval(DC_pip.getEdge(1)), fval(DC_pip.getEdge(2)), fval(DC_pip.getEdge(3)),
                    nanf, nanf, nani, nanf, nanf, nanf, nanf,
                    all_ele, el_chi2pid, pip_p, dvz, Hx, Hy, V_PCal, W_PCal)
            n_elepip++
        }
    }

    for(int ipart = 0; ipart < partb.getRows(); ipart++){
        def charge = partb.getByte("charge", ipart)
        if(charge <= 0){ continue }
        double px = partb.getFloat("px", ipart)
        double py = partb.getFloat("py", ipart)
        double pz = partb.getFloat("pz", ipart)
        float had_p = (float) Math.sqrt(px*px + py*py + pz*pz)
        float had_beta = partb.getFloat("beta", ipart)
        int had_status = particle_status(partb, ipart)
        float had_chi2pid = partb.getFloat("chi2pid", ipart)
        def DC_had = DCEdgeCandidate.getDCEdgeCandidate(ipart, partb, trajb)
        tt.fill(2, nphe, pcalE, elp, sftot, esec, vz, e_edge1, e_edge2, e_edge3,
                xrot1, yrot1, xrot2, yrot2, xrot3, yrot3,
                nani, nanf, nanf, nanf, nanf,
                had_p, had_beta, had_status, had_chi2pid,
                fval(DC_had.getEdge(1)), fval(DC_had.getEdge(2)), fval(DC_had.getEdge(3)),
                all_ele, el_chi2pid, nanf, nanf, Hx, Hy, V_PCal, W_PCal)
        n_had++
    }
}
reader.close()

tt.write()
ff.close()

println("Wrote ROOT TTree: ${rootName}")
println("  QA events ${nread}; ele ${n_ele}; elepip ${n_elepip}; had ${n_had}")
println("Finished Chapter 3 HIPO TTree for ${hipoName}")
