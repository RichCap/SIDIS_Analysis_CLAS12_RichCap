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

import org.jlab.jnp.hipo4.data.Schema

// Clock Time & Runtime
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

def formatter = DateTimeFormatter.ofPattern("MM-dd-yyyy HH:mm:ss")
def startClock = LocalDateTime.now()
System.out.println("");
System.out.println("");
System.out.println("=== Script STARTED at: " + startClock.format(formatter) + " ===")
System.out.println("");
System.out.println("");
long StartTime = System.nanoTime()

Sugar.enable()

def isinb = ! ( args[0].contains('outb') || args[0].contains('torus+1') )
def ismc  = args[0].contains("gemc")

def suff = isinb ? 'inb' : 'outb'
if(ismc) suff += '.mc'
else suff += '.qa'

def outname = args[0].split("/")[-1]

// Updated on 4/10/2026: new8 adds pi-/proton flags and rho0 parent kinematics (skipped new7 to bring `MC_GEN` up-to-date with `Data` and `MC_REC`)
    // 5/29/2026: new9 is the same as new8 — just reran to ensure the number of files stayed the same since the matched script needed to be updated after the number of files (potentially) changed
def ff = new ROOTFile("MC_Gen_sidis_epip_richcap.${suff}.new9.${outname}.root")

// Added parent PIDs of both particles as of 12/17/2025 (with 'new6' version)
def branches_string = 'event/I:runN/I:beamCharge:Num_Pions/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Hx:Hy:Par_PID_el/I:Par_PID_pip/I'
// Added as of 4/10/2026
// Flags for exclusive events
branches_string += ':pim_present/I:proton_present/I'
// rho0 Kinematics
branches_string += ':rho0_px:rho0_py:rho0_pz:rho0_E:rho0_parent/I'
// Added as of 5/7/2026
branches_string += ':rho0_grandparent/I:exclusive_rho/I'
branches_string += ':pimx:pimy:pimz:Par_PID_pim/I'
branches_string += ':prox:proy:proz:Par_PID_pro/I'
// // NEW branches for mother chain, pi- kinematics, and exclusive rho flag
// branches_string += ':rho_mother_chain:pim_px:pim_py:pim_pz:pim_e:exclusive_rho/I:Par_PID_pim/I'

def tt = ff.makeTree('h22', 'title', branches_string)

// // Variable-length list for rho mother chain (must be declared before the loop)
// def rhoMotherChain = new java.util.ArrayList<Integer>()
// tt.Branch("rho_mother_chain", rhoMotherChain)

int Multiple_Pions_Per_Electron = 0
def num_of_rho0_found  = 0
def num_of_excl__rho0  = 0
int Total_Events_Found = 0

def beam = LorentzVector.withPID(11,0,0,10.6041)

def Q2_cut_Count   = 0
def Q2_nocut_Count = 0
def Q2_SIDIS_Count = 0


// ======================================================================
// Returns the BANK ROW (0-based) of the parent.
// Returns -1 if the particle has no parent (parent index == 0).
// ======================================================================
def getParentIndex(Bank lundBank, int row){
    Schema schema = lundBank.getSchema()
    int colType = schema.getType("parent")
    int rawParent = 0
    switch (colType) {
        case 0:  rawParent = lundBank.getByte("parent",  row); break
        case 1:  rawParent = lundBank.getInt("parent",   row); break
        case 2:  rawParent = lundBank.getShort("parent", row); break
        case 3:  rawParent = (int) lundBank.getFloat("parent", row); break
        default:
            System.out.println("WARNING: Unknown type for MC::Lund.parent = $colType (row $row)")
            rawParent = lundBank.getShort("parent", row)
    }
    if (rawParent <= 0) { return -1; } // no parent (beam electron, target proton, etc.)
    // Convert LUND index (starts at 1) → bank row (starts at 0)
    return rawParent - 1;
}

// ======================================================================
// Get full mother chain for rho0 (or any particle)
// Walks up the parent indices collecting PIDs until root (parent <= 0)
// ======================================================================
def getFullMotherChain(Bank lund, int startRow) {
    return 0;
    def chain = new java.util.ArrayList<Integer>()
    int current = startRow
    while (current >= 0 && current < lund.getRows()) {
        chain.add(lund.getInt("pid", current))
        int parentIdx = getParentIndex(lund, current)
        if (parentIdx <= 0 || parentIdx == current || parentIdx >= lund.getRows()) { break }
        current = parentIdx
    }
    return chain
}


// ------------------------------------------------------------
// Exclusive rho0 flag using type==1 (final-state particles only)
// ------------------------------------------------------------
def isExclusiveRho(Bank lund) {
    int nEle = 0, nPip = 0, nPim = 0, nProt = 0; nOther = 0;
    int rhoRow = -1;
    int pipRow = -1, pimRow = -1;
    int nrows = lund.getRows();
    for (int i = 0; i < nrows; i++) {
        int pid = lund.getInt("pid", i);
        if (pid ==  113) { rhoRow = i; }
        if (lund.getByte("type", i) != 1) { continue; }  // only final-state particles
        if      (pid ==   11) { nEle++; }
        else if (pid ==  211) { nPip++; pipRow = i; }
        else if (pid == -211) { nPim++; pimRow = i; }
        else if (pid == 2212) { nProt++; }
        else                  { nOther++; }
    }
    if (nEle != 1 || nPip != 1 || nPim != 1 || nProt != 1) { return 0; }
    if ((pipRow >= 0 && getParentIndex(lund, pipRow) == rhoRow) && (pimRow >= 0 && getParentIndex(lund, pimRow) == rhoRow)) { return 1; } // both pions must have rho0 as direct parent
    return 0;
}

// Tolerances for float comparisons (tune as needed)
final double ABS_TOL = 1e-6
final double REL_TOL = 1e-4
// Make them visible inside GPars parallel closures
this.ABS_TOL = ABS_TOL
this.REL_TOL = REL_TOL

// Helper: robust float compare (absolute + relative)
boolean nearlyEqual(double a, double b, double absTol, double relTol) {
    double diff = Math.abs(a - b)
    if (diff <= absTol) return true
    double scale = Math.max(Math.abs(a), Math.abs(b))
    return diff <= relTol * scale
}

// Helper: Converts booleans into integers (1 == true, 0 == false), or -1 if input is null.
Integer ConvertBoolean(Boolean bool) {
    if (bool == null) { return -1; } // Return -1 if the input is null
    return bool ? 1 : 0;
}


// Finds the LUND particle matching the provided PID and momentum and returns BOTH the immediate parent PID and the grandparent PID.
// Returns [parentPID: 0, grandparentPID: 0] if no matching particle is found.
def findParentPIDFromLund(def lund_in, int pid_in, float px_in, float py_in, float pz_in, double absTol, double relTol) {
    int nrows_lund = lund_in.getRows()
    for (int i = 0; i < nrows_lund; i++) {
        int   pid_lund = lund_in.getInt("pid",  i)
        float px_lund  = lund_in.getFloat("px", i)
        float py_lund  = lund_in.getFloat("py", i)
        float pz_lund  = lund_in.getFloat("pz", i)
        boolean pidOK  = (pid_lund == pid_in)
        boolean pxOK   = nearlyEqual(px_lund, px_in, absTol, relTol)
        boolean pyOK   = nearlyEqual(py_lund, py_in, absTol, relTol)
        boolean pzOK   = nearlyEqual(pz_lund, pz_in, absTol, relTol)
        if (!(pidOK && pxOK && pyOK && pzOK)) { continue }
        // ---- Match found ----
        int parentIndex = getParentIndex(lund_in, i)
        if (parentIndex < 0 || parentIndex >= nrows_lund || parentIndex == i) {
            System.out.println("[findParentPIDFromLund]: WARNING - Matched particle (PID=${pid_lund}) found with index ${i} (out of ${nrows_lund}), but parent index (${parentIndex}) is invalid")
            System.out.println("=== BAD PARENT INDEX DETECTED ===")
            System.out.println("Matched row ${i}: PID=${pid_lund}, px=${px_lund:.4f}, py=${py_lund:.4f}, pz=${pz_lund:.4f}")
            int index = lund_in.getInt("index", i)
            System.out.println("Parent index = ${parentIndex} (self = ${parentIndex == i} = ${index})")
            System.out.println("Full MC::Lund bank for this event:")
            for (int r = 0; r < nrows_lund; r++) {
                int p = lund_in.getInt("pid", r)
                int parent = getParentIndex(lund_in, r)
                int index_loop = lund_in.getInt("index", r)
                System.out.println("  Row ${r}: Index=${index_loop}, PID=${p}, parent=${parent}")
            }
            System.out.println("================================")
            return [parentPID: 0, grandparentPID: 0]
        }
        // else { System.out.println("[findParentPIDFromLund]: Matched the index...") }
        int parentPID = lund_in.getInt("pid", parentIndex)
        // ---- Grandparent ----
        int grandparentIndex = getParentIndex(lund_in, parentIndex)
        int grandparentPID = 0
        if ((grandparentIndex > 0) && (grandparentIndex < nrows_lund) && (grandparentIndex != parentIndex) && (grandparentIndex != i)) { grandparentPID = lund_in.getInt("pid", grandparentIndex) }
        return [parentPID: parentPID, grandparentPID: grandparentPID]
    }
    // ---- No match found ----
    System.out.println("ERROR - No matching particle found in LUND bank.")
    System.out.println("Target Particle = (pid,px,py,pz)=(${pid_in},${px_in},${py_in},${pz_in})")
    return [parentPID: 0, grandparentPID: 0]
}

// ------------------------------------------------------------
// Find Parent rho0s
// ------------------------------------------------------------
def findParent_rho(def lund_in, int pid_in, float px_in, float py_in, float pz_in, double absTol, double relTol) {
    int nrows_lund = lund_in.getRows()
    for (int i = 0; i < nrows_lund; i++) {
        // Pull candidate from MC::Lund at row i
        int  pid_lund  = lund_in.getInt("pid",  i)
        float px_lund  = lund_in.getFloat("px", i)
        float py_lund  = lund_in.getFloat("py", i)
        float pz_lund  = lund_in.getFloat("pz", i)
        // Compare with values you already extracted from the other bank
        boolean pidOK = (pid_lund == pid_in)
        boolean pxOK  = nearlyEqual(px_lund, px_in, absTol, relTol)
        boolean pyOK  = nearlyEqual(py_lund, py_in, absTol, relTol)
        boolean pzOK  = nearlyEqual(pz_lund, pz_in, absTol, relTol)
        // If this row does not match, continue searching
        if (!(pidOK && pxOK && pyOK && pzOK)) { continue }
        // ---- Match found ----
        int parentIndex = getParentIndex(lund_in, i)
        // Defensive check on parent index
        if (parentIndex < 0 || parentIndex >= nrows_lund) {
            // System.out.println("WARNING - Matched particle found, but parent index is invalid: ${parentIndex}")
            System.out.println("[findParent_rho]: WARNING - Matched particle found, but parent index is invalid: ${parentIndex}")
            return [
                parentPID       : 0,
                rho0_px         : 0.0,
                rho0_py         : 0.0,
                rho0_pz         : 0.0,
                rho0_E          : 0.0,
                rho0_parent     : 0,
                rho0_grandparent: 0
            ]
        }
        int parentPID = lund_in.getInt("pid", parentIndex)
        def rho0_px = 0.0;
        def rho0_py = 0.0;
        def rho0_pz = 0.0;
        def rho0_E  = 0.0;
        def rho0_parent = 0;
        def rho0_grandparent = 0;
        // def rho_mother_chain = new java.util.ArrayList<Integer>();
        if(parentPID == 113){   // rho0
            // get rho0 kinematics
            rho0_px = lund_in.getFloat("px", parentIndex);
            rho0_py = lund_in.getFloat("py", parentIndex);
            rho0_pz = lund_in.getFloat("pz", parentIndex);
            def rhoVec = LorentzVector.withPID(113, rho0_px, rho0_py, rho0_pz);
            rho0_E = rhoVec.e();
            // DIRECT WALK UP THE CHAIN — no second call to findParentPIDFromLund
            rho0_parent = parentPID;  // the PID of the rho0's parent
            int grandparentIndex = getParentIndex(lund_in, parentIndex);
            rho0_grandparent = 0;
            if ((grandparentIndex > 0) && (grandparentIndex < nrows_lund) && (grandparentIndex != parentIndex)) { rho0_grandparent = lund_in.getInt("pid", grandparentIndex); }
            // // NEW: full mother chain
            // rho_mother_chain = getFullMotherChain(lund_in, parentIndex);
        }
        return [
            parentPID       : parentPID,
            rho0_px         : rho0_px,
            rho0_py         : rho0_py,
            rho0_pz         : rho0_pz,
            rho0_E          : rho0_E,
            rho0_parent     : rho0_parent,
            rho0_grandparent: rho0_grandparent
            // rho_mother_chain: new java.util.ArrayList<Integer>()
        ]
    }
    // ---- No match found ---- 
    System.out.println("ERROR - No matching particle found in LUND bank.")
    System.out.println("Target Particle = (pid,px,py,pz)=(${pid_in},${px_in},${py_in},${pz_in})")
    return [
        parentPID       : 0,
        rho0_px         : 0.0,
        rho0_py         : 0.0,
        rho0_pz         : 0.0,
        rho0_E          : 0.0,
        rho0_parent     : 0,
        rho0_grandparent: 0
        // rho_mother_chain: new java.util.ArrayList<Integer>()
    ]
}

// ------------------------------------------------------------
// pi-/proton particle searches + π- kinematics (for exclusive events)
// ------------------------------------------------------------
def Search_Additional_Particles(def Particle_Bank, def Traj_Bank, def InbendingQ, def GenMC = false){
    boolean hasProton = false;
    boolean hasPim    = false;
    float pim_px = 0.0f;
    float pim_py = 0.0f;
    float pim_pz = 0.0f;
    float pim_e  = 0.0f;
    float pro_px = 0.0f;
    float pro_py = 0.0f;
    float pro_pz = 0.0f;
    float pro_e  = 0.0f;
    for (int ipart_p = 1; ipart_p < Particle_Bank.getRows(); ipart_p++) {
        if(GenMC){
            def pid_p_gen = Particle_Bank.getInt("pid", ipart_p)
            if(pid_p_gen == 2212){
                hasProton = true;
                pro_px = Particle_Bank.getFloat("px", ipart_p);
                pro_py = Particle_Bank.getFloat("py", ipart_p);
                pro_pz = Particle_Bank.getFloat("pz", ipart_p);
                def proVec = LorentzVector.withPID(2212, pro_px, pro_py, pro_pz);
                pro_e  = proVec.e();
            }
            if(pid_p_gen == -211){
                hasPim = true;
                pim_px = Particle_Bank.getFloat("px", ipart_p);
                pim_py = Particle_Bank.getFloat("py", ipart_p);
                pim_pz = Particle_Bank.getFloat("pz", ipart_p);
                def pimVec = LorentzVector.withPID(-211, pim_px, pim_py, pim_pz);
                pim_e  = pimVec.e();
                // pim_e  = Particle_Bank.getFloat("energy", ipart_p);
            }
        }
        else {
            def canpro = ProtonCandidate.getProtonCandidate(ipart_p, Particle_Bank, Traj_Bank, InbendingQ);
            if(canpro.isproton()){ 
                hasProton = true;
                def proVec = canpro.getLorentzVector();
                pro_px = proVec.px();
                pro_py = proVec.py();
                pro_pz = proVec.pz();
                pro_e  = proVec.e();
            }
            else {
                def canpim = PionCandidate.getPionCandidate(ipart_p, Particle_Bank, Traj_Bank, InbendingQ);
                if(canpim.ispim()){
                    hasPim = true;
                    def pimVec = canpim.getLorentzVector();
                    pim_px = pimVec.px();
                    pim_py = pimVec.py();
                    pim_pz = pimVec.pz();
                    pim_e  = pimVec.e();
                }
            }
        }
        if(hasProton && hasPim){ break }
    }
    return [
        hasProton  : hasProton,
        hasPim     : hasPim,
        pim_px     : pim_px,
        pim_py     : pim_py,
        pim_pz     : pim_pz,
        pim_e      : pim_e,
        pro_px     : pro_px,
        pro_py     : pro_py,
        pro_pz     : pro_pz,
        pro_e      : pro_e
    ];
}


GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    // QADB qa = new QADB()

    def reader = new HipoReader()
    reader.open(fname)
    def event = new Event()
    def factory = reader.getSchemaFactory()
    def banks = ['MC::Header', 'REC::Event', 'MC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator', 'MC::Lund'].collect{new Bank(factory.getSchema(it))}

    while(reader.hasNext()){
        reader.nextEvent(event)
        banks.each{event.read(it)}

        if(banks.every()){
            def (runb, evb, partb, ecb, ccb, trajb, scb, lund) = banks

            def run = runb.getInt("run",   0)
            def evn = runb.getInt("event", 0)
            def pid = partb.getInt("pid",  0)
            
            def beamCharge = evb.getFloat("beamCharge", 0)
            
            if(pid == 11){ // Is an electron
                
                int pionCount = 0 // Counter for pions (helps control double-counted electrons)
                
                def ex  = partb.getFloat("px", 0)
                def ey  = partb.getFloat("py", 0)
                def ez  = partb.getFloat("pz", 0)
                def ele = LorentzVector.withPID(pid, ex, ey, ez)
                def Q2  = -(beam - ele).mass2()
                
                // System.out.println("Finding electron Parent:");
                def el_parentInfo = findParentPIDFromLund(lund, pid, ex, ey, ez, ABS_TOL, REL_TOL);
                int parentPID_el  = el_parentInfo.parentPID;
                // System.out.println("parentPID_el = ${parentPID_el}");

                if(Q2 > 1.5){ Q2_cut_Count += 1;}
                else{ Q2_nocut_Count += 1;}

                def Extra_Particle_Search = Search_Additional_Particles(partb, trajb, isinb, true)
                
                for(int ipart = 1; ipart < partb.getRows(); ipart++){
                    def pid_pip = partb.getInt("pid", ipart)
                    
                    if(pid_pip == 211){ // Is a Pi+
                        
                        pionCount += 1;                                         // Increment pion counter
                        Total_Events_Found += 1;                                // Increment "total event" counter
                        if(pionCount != 1){ Multiple_Pions_Per_Electron += 1; } // Increment "number of double-counted electron" counter

                        if(Q2 > 1.5){ Q2_SIDIS_Count += 1; }
                        
                        def px = partb.getFloat("px", ipart)
                        def py = partb.getFloat("py", ipart)
                        def pz = partb.getFloat("pz", ipart)
                        def pip0 = LorentzVector.withPID(pid_pip, px, py, pz)
                        
                        // System.out.println("Finding pi+ pion Parent:");
                        def parent_of_pip      = findParent_rho(lund, pid_pip, px, py, pz, ABS_TOL, REL_TOL);
                        int parentPID_pi       = parent_of_pip.parentPID;
                        def rho0_px            = parent_of_pip.rho0_px;
                        def rho0_py            = parent_of_pip.rho0_py;
                        def rho0_pz            = parent_of_pip.rho0_pz;
                        def rho0_E             = parent_of_pip.rho0_E;
                        def rho0_parent        = parent_of_pip.rho0_parent;
                        def rho0_grandparent   = parent_of_pip.rho0_grandparent;
                        // NEW: get rho mother chain, pi-, and proton kinematics
                        int exclusive_rho_flag = isExclusiveRho(lund)
                        // rhoMotherChain.clear()
                        // rhoMotherChain.addAll(match_default.rho_mother_chain)
                        float pim_px           = Extra_Particle_Search.pim_px
                        float pim_py           = Extra_Particle_Search.pim_py
                        float pim_pz           = Extra_Particle_Search.pim_pz
                        // float pim_e         = Extra_Particle_Search.pim_e
                        float pro_px           = Extra_Particle_Search.pro_px
                        float pro_py           = Extra_Particle_Search.pro_py
                        float pro_pz           = Extra_Particle_Search.pro_pz
                        // float pro_e         = Extra_Particle_Search.pro_e
                        // NEW: π⁻/proton parent PID (immediate parents only)
                        int parentPID_pim = 0;
                        int parentPID_pro = 0;
                        if(Extra_Particle_Search.hasPim){ 
                            def pim_parentInfo = findParentPIDFromLund(lund, -211, Extra_Particle_Search.pim_px, Extra_Particle_Search.pim_py, Extra_Particle_Search.pim_pz, ABS_TOL, REL_TOL);
                            parentPID_pim = pim_parentInfo.parentPID;
                        }
                        if(Extra_Particle_Search.hasPro){ 
                            def pro_parentInfo = findParentPIDFromLund(lund, 2212, Extra_Particle_Search.pro_px, Extra_Particle_Search.pro_py, Extra_Particle_Search.pro_pz, ABS_TOL, REL_TOL);
                            parentPID_pro = pro_parentInfo.parentPID;
                        }
                        
                        // Coordinate of the matched hit (cm) - for Valerii's cuts (done in python)
                        float Hx = ecb.getFloat("hx", 0)
                        float Hy = ecb.getFloat("hy", 0)

                        // // Spherical Momentum Coordinates
                        def elPhi = (180/3.1415926)*ele.phi()
                        def pipPhi = (180/3.1415926)*pip0.phi()

                        // Electron Sectors (From Angle)
                        def esec_a = 0
                        if(elPhi >=  -30 && elPhi <   30){esec_a = 1}
                        if(elPhi >=   30 && elPhi <   90){esec_a = 2}
                        if(elPhi >=   90 && elPhi <  150){esec_a = 3}
                        if(elPhi >=  150 || elPhi < -150){esec_a = 4}
                        if(elPhi >=  -90 && elPhi <  -30){esec_a = 5}
                        if(elPhi >= -150 && elPhi <  -90){esec_a = 6}

                        // Pi+ Sectors (From Angle)
                        def pipsec_a = 0
                        if(pipPhi >=  -45 && pipPhi <   15){pipsec_a = 1}
                        if(pipPhi >=   15 && pipPhi <   75){pipsec_a = 2}
                        if(pipPhi >=   75 && pipPhi <  135){pipsec_a = 3}
                        if(pipPhi >=  135 || pipPhi < -165){pipsec_a = 4}
                        if(pipPhi >= -105 && pipPhi <  -45){pipsec_a = 5}
                        if(pipPhi >= -165 && pipPhi < -105){pipsec_a = 6}
                        
                        tt.fill(evn, run,     beamCharge,  pionCount,
                                ex, ey,       ez, px, py,  pz,
                                esec_a,       pipsec_a,    Hx, Hy,
                                parentPID_el, parentPID_pi,
                                // Flags for exclusive events
                                ConvertBoolean(Extra_Particle_Search.hasPim),
                                ConvertBoolean(Extra_Particle_Search.hasProton),
                                // rho0 Kinematics
                                rho0_px, rho0_py, rho0_pz, rho0_E, rho0_parent,
                                rho0_grandparent, exclusive_rho_flag,
                                // π- Kinematics
                                pim_px, pim_py, pim_pz, parentPID_pim,
                                // Proton Kinematics
                                pro_px, pro_py, pro_pz, parentPID_pro
                                )
                        if(parentPID_pi       == 113) { num_of_rho0_found += 1 }
                        if(exclusive_rho_flag == 1)   { num_of_excl__rho0 += 1 }
                    }
                }
            }
        }
    }

    reader.close()
}
}

System.out.println("");

System.out.println("Total number of events found                                = " + Total_Events_Found);
System.out.println("");

System.out.println("Number of times that Multiple Pions were found per Electron = " + Multiple_Pions_Per_Electron);
System.out.println("");

System.out.println("Number of rho0 Parents found                                = " + num_of_rho0_found);
System.out.println("Number of (Exclusive) rho0 Parents found                    = " + num_of_excl__rho0);
System.out.println("");

System.out.println("Total number of generated events found with Q2 > 1.5        = " + Q2_cut_Count);
System.out.println("Total number of generated events found with Q2 < 1.5        = " + Q2_nocut_Count);
System.out.println("Total number of   SIDIS   events found with Q2 > 1.5        = " + Q2_SIDIS_Count);
System.out.println("");

long RunTime = (System.nanoTime() - StartTime)/1000000000;

def endClock = LocalDateTime.now()
System.out.println("");
System.out.println("=== Script FINISHED at: " + endClock.format(formatter) + " ===")
System.out.println("");

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
