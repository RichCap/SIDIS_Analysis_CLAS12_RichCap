#!/usr/bin/env run-groovy
// Chapter 3 HIPO histogram job.
// One REAL nSidis HIPO file in, one small ROOT file of histograms out.
// Intended to be launched with run_groovy_scripts_with_emails.py --source data --script-path this file.
// Do not run this script on a machine that does not contain the HIPO inputs.

import org.jlab.jnp.hipo4.io.HipoReader
import org.jlab.jnp.hipo4.data.Bank
import org.jlab.jnp.hipo4.data.Event
import org.jlab.groot.data.H1F
import org.jlab.groot.data.H2F
import uconn.utils.pid.stefan.ElectronCandidate
import uconn.utils.pid.stefan.PionCandidate
import clasqa.QADB
import groovy.json.JsonOutput
import groovy.json.JsonBuilder

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
if(chapter3Dir == null || !new File(chapter3Dir, "json_hists_to_root.py").exists()){
    def sibling = new File("json_hists_to_root.py")
    if(sibling.exists()){ chapter3Dir = sibling.getAbsoluteFile().getParentFile() }
}
if(chapter3Dir == null || !new File(chapter3Dir, "json_hists_to_root.py").exists()){
    def parentSibling = new File("..", "json_hists_to_root.py")
    if(parentSibling.exists()){ chapter3Dir = parentSibling.getAbsoluteFile().getParentFile() }
}
if(chapter3Dir == null || !new File(chapter3Dir, "json_hists_to_root.py").exists()){
    chapter3Dir = farmChapter3
}

def outDirEnv = System.getenv("CHAPTER3_HIPO_OUTDIR")
def outDir = (outDirEnv != null && outDirEnv.trim() != "") ? outDirEnv.trim() : new File(chapter3Dir, "job_outputs").getAbsolutePath()
new File(outDir).mkdirs()
def jsonName = "${outDir}/Chapter3_HIPO_hists_${hipoName}.json"
def rootName = "${outDir}/Chapter3_HIPO_hists_${hipoName}.root"

// Fall 2018 inbending total-SF parameters (same arrays as Data_TTree_epip_Batch_Pass2.groovy).
double[] p0mean_inb  = [ 0.111767,    0.116619,    0.114606,    0.116586,    0.118251,    0.117391    ] as double[]
double[] p1mean_inb  = [-0.0281943,   0.0662751,  -0.0896597,   0.181465,    0.085993,    0.0186504   ] as double[]
double[] p2mean_inb  = [ 0.00711137,  0.00633334,  0.00912098,  0.00652068,  0.00416682,  0.00622289  ] as double[]
double[] p3mean_inb  = [-0.000878776,-0.000780257,-0.00108891,-0.000645957,-0.000485189,-0.000829729 ] as double[]
double[] p0sigma_inb = [-0.00497609,  0.0259435,  0.0296159,   0.0161445,   0.0239166,   0.0244309   ] as double[]
double[] p1sigma_inb = [ 0.0275006,  -0.000805156,-0.00449379,  0.0099462,   0.00192551,  0.00258059  ] as double[]
double[] p2sigma_inb = [ 0.00253641, -0.00386759, -0.00469883, -0.00182968, -0.00355973, -0.00398967 ] as double[]
double[] p3sigma_inb = [-0.000173549, 0.00030325,  0.000380195, 0.00012328,  0.000302528, 0.000340911] as double[]

def h_htcc = new H1F("h_htcc_nphe", "Electron HTCC N_{phe};N_{phe};Counts", 80, 0.0, 40.0)
def h_pcal = new H1F("h_pcal_energy", "Electron PCAL energy;E_{PCAL} [GeV];Counts", 120, 0.0, 1.2)
def h_sftot = [:]
def h_dc = [:]
for(int sec = 1; sec <= 6; sec++){
    h_sftot[sec] = new H2F("h_sftot_sec${sec}", "Sector ${sec};p_{e} [GeV];SF_{tot}", 80, 1.0, 10.5, 80, 0.05, 0.40)
    h_dc[6*100+sec]  = new H2F("h_ele_dc_r1_s${sec}", "R1 S${sec};x_{rot} [cm];y_{rot} [cm]", 80, -160, 20, 80, -90, 90)
    h_dc[18*100+sec] = new H2F("h_ele_dc_r2_s${sec}", "R2 S${sec};x_{rot} [cm];y_{rot} [cm]", 80, -220, 20, 80, -120, 120)
    h_dc[36*100+sec] = new H2F("h_ele_dc_r3_s${sec}", "R3 S${sec};x_{rot} [cm];y_{rot} [cm]", 80, -280, 20, 80, -160, 160)
}
def h_beta = new H2F("h_beta_poshad", "Positive hadrons;p [GeV];#beta", 120, 0.0, 8.0, 120, 0.4, 1.2)

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

def axis_of(obj, which){
    if(which == "x"){
        try { return obj.getXAxis() } catch(Exception e1){ return obj.getXaxis() }
    }
    try { return obj.getYAxis() } catch(Exception e2){ return obj.getYaxis() }
}

def serialize_h1(H1F h){
    def ax = axis_of(h, "x")
    int nb = ax.getNBins()
    def contents = []
    def errors = []
    for(int ib = 0; ib <= nb + 1; ib++){
        double val = h.getBinContent(ib)
        contents.add(val)
        errors.add(Math.sqrt(Math.abs(val)))
    }
    return [
        type     : "th1",
        name     : h.getName(),
        title    : h.getTitle(),
        nbins    : nb,
        xmin     : ax.min(),
        xmax     : ax.max(),
        contents : contents,
        errors   : errors,
        entries  : h.getEntries()
    ]
}

def serialize_h2(H2F h){
    def ax = axis_of(h, "x")
    def ay = axis_of(h, "y")
    int nx = ax.getNBins()
    int ny = ay.getNBins()
    def contents = []
    def errors = []
    for(int iy = 0; iy <= ny + 1; iy++){
        for(int ix = 0; ix <= nx + 1; ix++){
            double val = h.getBinContent(ix, iy)
            contents.add(val)
            errors.add(Math.sqrt(Math.abs(val)))
        }
    }
    return [
        type     : "th2",
        name     : h.getName(),
        title    : h.getTitle(),
        nbinsx   : nx,
        xmin     : ax.min(),
        xmax     : ax.max(),
        nbinsy   : ny,
        ymin     : ay.min(),
        ymax     : ay.max(),
        contents : contents,
        errors   : errors,
        entries  : h.getEntries()
    ]
}

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
    if(canele != null && canele.iselectron(ElectronCandidate.Cut.PID)){
        h_htcc.fill(htcc_nphe(ccb))
        if(canele.pcal_energy != null){
            h_pcal.fill((double) canele.pcal_energy)
        }
        def partp = canele.p
        def pcalE = canele.pcal_energy
        def ecinE = canele.ecin_energy
        def ecoutE = canele.ecout_energy
        def pcalSec = canele.getPCALsector()
        if(partp != null && partp > 0 && pcalE != null && ecinE != null && ecoutE != null && pcalSec != null){
            int sec = (int) pcalSec
            if(sec >= 1 && sec <= 6){
                double sftot = ((double)pcalE + (double)ecinE + (double)ecoutE) / (double)partp
                h_sftot[sec].fill((double)partp, sftot)
            }
        }
        int esec = (pcalSec != null) ? (int) pcalSec : 1
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
            if(!Float.isNaN(x6)){  def xy = rotate_dc(x6,  y6,  z6,  esec); h_dc[6*100+esec].fill(xy[0], xy[1]) }
            if(!Float.isNaN(x18)){ def xy = rotate_dc(x18, y18, z18, esec); h_dc[18*100+esec].fill(xy[0], xy[1]) }
            if(!Float.isNaN(x36)){ def xy = rotate_dc(x36, y36, z36, esec); h_dc[36*100+esec].fill(xy[0], xy[1]) }
        }
    }

    for(int ipart = 0; ipart < partb.getRows(); ipart++){
        def charge = partb.getByte("charge", ipart)
        if(charge <= 0){ continue }
        double px = partb.getFloat("px", ipart)
        double py = partb.getFloat("py", ipart)
        double pz = partb.getFloat("pz", ipart)
        double p = Math.sqrt(px*px + py*py + pz*pz)
        double beta = partb.getFloat("beta", ipart)
        if(p > 0 && beta > 0){
            h_beta.fill(p, beta)
        }
    }
}
reader.close()

def hist_list = []
hist_list.add(serialize_h1(h_htcc))
hist_list.add(serialize_h1(h_pcal))
hist_list.add(serialize_h2(h_beta))
for(int sec = 1; sec <= 6; sec++){
    hist_list.add(serialize_h2(h_sftot[sec]))
    hist_list.add(serialize_h2(h_dc[6*100+sec]))
    hist_list.add(serialize_h2(h_dc[18*100+sec]))
    hist_list.add(serialize_h2(h_dc[36*100+sec]))
}
def payload = [input_file: hipoPath, n_qa_events: nread, histograms: hist_list]
new File(jsonName).text = JsonOutput.prettyPrint(JsonOutput.toJson(payload))
println("Wrote JSON: ${jsonName}")

def converter = new File(chapter3Dir, "json_hists_to_root.py")
if(!converter.exists()){
    converter = new File("json_hists_to_root.py")
}
if(converter.exists()){
    def pb = ["python3", converter.getAbsolutePath(), jsonName, rootName].execute()
    pb.waitForProcessOutput(System.out, System.err)
    if(pb.exitValue() != 0){
        println("WARNING: json_hists_to_root.py failed with rc=${pb.exitValue()}. JSON remains at ${jsonName}")
    } else {
        println("Wrote ROOT: ${rootName}")
    }
} else {
    println("WARNING: json_hists_to_root.py not found; left JSON at ${jsonName}")
}

println("Finished Chapter 3 HIPO histograms for ${hipoName}")
