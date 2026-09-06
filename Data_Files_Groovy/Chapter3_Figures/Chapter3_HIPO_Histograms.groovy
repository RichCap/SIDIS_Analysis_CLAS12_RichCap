#!/usr/bin/env run-groovy
// Chapter 3 HIPO TTree job.
// One REAL nSidis HIPO file in, one small ROOT file of compact TTrees out.
// Intended to be launched with run_groovy_scripts_with_emails.py --source data --script-path this file.
// Do not run this script on a machine that does not contain the HIPO inputs.
//
// Trees:
//   ele    — one row per PID trigger electron (particle 0)
//   elepip — one row per e-pi+ pair in a PID-electron event
//   had    — one row per charge>0 hadron in a PID-electron event
// Optional cut combinations are applied later in plot_Chapter3_HIPO_hists.py.

import org.jlab.jnp.hipo4.io.HipoReader
import org.jlab.jnp.hipo4.data.Bank
import org.jlab.jnp.hipo4.data.Event
import org.jlab.jroot.ROOTFile
import uconn.utils.pid.stefan.ElectronCandidate
import uconn.utils.pid.stefan.PionCandidate
import clasqa.QADB

def hipoPath = args[0]
def isinb = ! ( hipoPath.contains('outb') || hipoPath.contains('torus+1') )
def ismc  = hipoPath.contains("gemc")
def hipoName = hipoPath.split("/")[-1]

def farmChapter3 = new File("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Chapter3_Figures")
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

int ival(def v) {
    if(v == null) { return -1 }
    return (int) v
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

def ff = new ROOTFile(rootName)
def ele_branches = 'nphe:pcal_energy:el_p:sftot:esec/I:vz:e_edge1:e_edge2:e_edge3:xrot1:yrot1:xrot2:yrot2:xrot3:yrot3'
def elepip_branches = ele_branches + ':pip_status/I:pip_chi2pid:p_edge1:p_edge2:p_edge3'
def had_branches = 'had_p:had_beta:had_status/I:had_chi2pid:h_edge1:h_edge2:h_edge3:pcal_energy:vz:e_edge1:e_edge2:e_edge3'
def t_ele = ff.makeTree('ele', 'Chapter 3 PID electrons', ele_branches)
def t_elepip = ff.makeTree('elepip', 'Chapter 3 e-pi+ pairs', elepip_branches)
def t_had = ff.makeTree('had', 'Chapter 3 positive hadrons', had_branches)

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

    t_ele.fill(nphe, pcalE, elp, sftot, esec, vz, e_edge1, e_edge2, e_edge3,
               xrot1, yrot1, xrot2, yrot2, xrot3, yrot3)
    n_ele++

    for(int ipart = 1; ipart < partb.getRows(); ipart++){
        def canpip = PionCandidate.getPionCandidate(ipart, partb, trajb, isinb)
        if(canpip != null && canpip.ispip(PionCandidate.Cut.PID)){
            def DC_pip = DCEdgeCandidate.getDCEdgeCandidate(ipart, partb, trajb)
            int pip_status = particle_status(partb, ipart)
            float pip_chi2pid = partb.getFloat("chi2pid", ipart)
            t_elepip.fill(nphe, pcalE, elp, sftot, esec, vz, e_edge1, e_edge2, e_edge3,
                          xrot1, yrot1, xrot2, yrot2, xrot3, yrot3,
                          pip_status, pip_chi2pid,
                          fval(DC_pip.getEdge(1)), fval(DC_pip.getEdge(2)), fval(DC_pip.getEdge(3)))
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
        t_had.fill(had_p, had_beta, had_status, had_chi2pid,
                   fval(DC_had.getEdge(1)), fval(DC_had.getEdge(2)), fval(DC_had.getEdge(3)),
                   pcalE, vz, e_edge1, e_edge2, e_edge3)
        n_had++
    }
}
reader.close()

t_ele.write()
t_elepip.write()
t_had.write()
ff.close()

println("Wrote ROOT TTrees: ${rootName}")
println("  QA events ${nread}; ele ${n_ele}; elepip ${n_elepip}; had ${n_had}")
println("Finished Chapter 3 HIPO TTrees for ${hipoName}")
