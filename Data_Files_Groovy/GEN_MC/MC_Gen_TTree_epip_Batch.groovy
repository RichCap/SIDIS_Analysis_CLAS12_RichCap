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


def beam = LorentzVector.withPID(11,0,0,10.6041)
def target = LorentzVector.withPID(2212,0,0,0)

def isinb = ! ( args[0].contains('outb') || args[0].contains('torus+1') )
def ismc = args[0].contains("gemc")

def suff = isinb ? 'inb' : 'outb'
if(ismc) suff += '.mc'
else suff += '.qa'

def outname = args[0].split("/")[-1]
// def ff = new ROOTFile("calc_MC_Gen_sidis_epip_richcap_NC_smearing.${suff}.${outname}.root")
// def tt = ff.makeNtuple('h22','title','event:runN:ex:ey:ez:px:py:pz:esec:pipsec:ww:Q2_groovy')
// def tt = ff.makeNtuple('h22','title','event/I:runN/I:ex:ey:ez:el:elth:elPhi:el_E:px:py:pz:pip:pipth:pipPhi:pip_E:esec/I:pipsec/I:esec_a/I:pipsec_a/I:MM:MM2:Q2:s:W:xB:v:y:z:gamma:epsilon')
// def tt = ff.makeNtuple('h22','title','event/I:runN/I:ex:ey:ez:el:elth:elPhi:px:py:pz:pip:pipth:pipPhi:esec/I:pipsec/I:esec_a/I:pipsec_a/I:MM:MM2:Q2:W:xB:y:gamma:epsilon')

def ff = new ROOTFile("MC_Gen_sidis_epip_richcap.${suff}.${outname}.root")

// def tt = ff.makeTree('h22','title','event/I:runN/I:ex:ey:ez:el:elth:elPhi:el_E:px:py:pz:pip:pipth:pipPhi:pip_E:esec/I:pipsec/I:esec_a/I:pipsec_a/I:MM:MM2:Q2:s:W:xB:v:y:z:gamma:epsilon:Hx:Hy:elec_events_found/I')

def tt = ff.makeTree('h22','title','event/I:runN/I:ex:ey:ez:pipx:pipy:pipz:esec/I:pipsec/I:Hx:Hy:elec_events_found/I')

GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    QADB qa = new QADB()

    def reader = new HipoReader()
    reader.open(fname)
    def event = new Event()
    def factory = reader.getSchemaFactory()
    def banks = ['MC::Header', 'REC::Event', 'MC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator'].collect{new Bank(factory.getSchema(it))}
    
    int elec_total_found = 0;
    int elec_num_current = 0;
    int elec_events_found = 0;

    while(reader.hasNext()) {
        reader.nextEvent(event)
        banks.each{event.read(it)}

        if(banks.every()) {
            def (runb, evb, partb, ecb, ccb, trajb, scb) = banks

            def run = runb.getInt("run", 0)
            def evn = runb.getInt("event", 0)
            def pid = partb.getInt("pid", 0)
            
            if(pid == 11){
                // Is an electron
                elec_total_found += 1;
                
                
                for(int ipart = 1; ipart < partb.getRows(); ipart++){
                    def pid_pip = partb.getInt("pid",ipart)
                    
                    if(pid_pip == 211){
                        // Is a Pi+
                        
                        if(elec_total_found != elec_num_current){
                            elec_events_found += 1;
                            elec_num_current = elec_total_found;
                        }
                        
                        def ex = partb.getFloat("px", 0)
                        def ey = partb.getFloat("py", 0)
                        def ez = partb.getFloat("pz", 0)
                        def ele = LorentzVector.withPID(pid, ex, ey, ez)
                        
                        def px = partb.getFloat("px", ipart)
                        def py = partb.getFloat("py", ipart)
                        def pz = partb.getFloat("pz", ipart)
                        def pip0 = LorentzVector.withPID(pid_pip, px, py, pz)
                        
                        // def pip = pip0.p()

                        // def ww = (beam + target - ele).mass()
                        // def Q2 = -(beam - ele).mass2()

                        // if(pip>1.2 && ww>2 && Q2>1) {
                        // After this 'if' statement, the event being added to the ntuple is known to have at least one electron AND pi+ pion
                        // This 'if' statement also makes an 'initial' cut to the invarient mass (ww) and to Q^2

                        // // Cartesian Momentum Coordinates
                        // def ex = ele.px(), ey = ele.py(), ez = ele.pz()
                        // def px = pip0.px(), py = pip0.py(), pz = pip0.pz()

                        // // Sectors (From Detector) - Does not exist for generated files
                        // def esec =canele.getPCALsector(), pipsec =canpip.getDCsector()


                        // Coordinate of the matched hit (cm) - for Valerii's cuts (done in python)
                        float Hx = ecb.getFloat("hx", 0)
                        float Hy = ecb.getFloat("hy", 0)



                        // // Spherical Momentum Coordinates
                        // def el = ele.p()
                        // def elth = (180/3.1415926)*ele.theta()
                        def elPhi = (180/3.1415926)*ele.phi()
                        // def pip = pip0.p()
                        // def pipth = (180/3.1415926)*pip0.theta()
                        def pipPhi = (180/3.1415926)*pip0.phi()


                        // // Particle Energy
                        // def el_E = ele.e(), pip_E = pip0.e()


                        // Electron Sectors (From Angle)
                        def esec_a = 0

                        if(elPhi >= -30 && elPhi < 30){
                            esec_a = 1
                        }
                        if(elPhi >= 30 && elPhi < 90){
                            esec_a = 2
                        }
                        if(elPhi >= 90 && elPhi < 150){
                            esec_a = 3
                        }
                        if(elPhi >= 150 || elPhi < -150){
                            esec_a = 4
                        }
                        if(elPhi >= -90 && elPhi < -30){
                            esec_a = 5
                        }
                        if(elPhi >= -150 && elPhi < -90){
                            esec_a = 6
                        }


                        // Pi+ Sectors (From Angle)
                        def pipsec_a = 0

                        if(pipPhi >= -45 && pipPhi < 15){
                            pipsec_a = 1
                        }
                        if(pipPhi >= 15 && pipPhi < 75){
                            pipsec_a = 2
                        }
                        if(pipPhi >= 75 && pipPhi < 135){
                            pipsec_a = 3
                        }
                        if(pipPhi >= 135 || pipPhi < -165){
                            pipsec_a = 4
                        }
                        if(pipPhi >= -105 && pipPhi < -45){
                            pipsec_a = 5
                        }
                        if(pipPhi >= -165 && pipPhi < -105){
                            pipsec_a = 6
                        }


                        // // Sectors (other definition for consistancy with other files)
                        // def esec = esec_a, pipsec = pipsec_a

                        // // Shifting Phi angles to define Phi as always greater than 0 degrees
                        // if(elPhi < 0){
                        //     elPhi = elPhi + 360
                        // }
                        // if(pipPhi < 0){
                        //     pipPhi = pipPhi + 360
                        // }


                        // // Missing Mass, q, v (lepton energy loss), xB, s (CM Energy Squared), W (Invariant Mass), y (lepton energy loss fraction), z, gamma, epsilon
                        // def epipX = beam + target - ele - pip0
                        // def MM = epipX.mass(), MM2 = epipX.mass2()
                        // def q = beam - ele
                        // def v = beam.e() - ele.e()
                        // def xB = Q2/(2*target.mass()*v)
                        // def s = target.mass2() + 2*target.mass()*v - Q2
                        // def W = Math.pow(s, 0.5)
                        // // def y = (target.dot(q))/(target.dot(beam))
                        // def y = v/beam.e()
                        // def z = ((pip0.e())/(q.e()))
                        // def gamma = 2*target.mass()*(xB/Math.pow(Q2, 0.5))
                        // def epsilon = (1 - y - 0.25*(gamma*gamma)*(y*y))/(1 - y + 0.5*(y*y) + 0.25*(gamma*gamma)*(y*y))


                        // if(y < 0.75 && W > 2 && Q2 > 1 && MM > 1.5 && pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35){
                            // Final Kinematic Cuts (before python analysis) for reconstructed dataframes - not meant for generated files
                        // tt.fill(evn, run, ex, ey, ez, el, elth, elPhi, el_E,
                        //     px, py, pz, pip, pipth, pipPhi, pip_E,
                        //     esec, pipsec, esec_a, pipsec_a,
                        //     MM, MM2, Q2, s, W, xB,
                        //     v, y, z, gamma, epsilon,
                        //     Hx, Hy, elec_events_found)
                        tt.fill(evn, run, ex, ey, ez, px, py, pz,
                            esec_a, pipsec_a, Hx, Hy, elec_events_found)
                    }
                }
            }
        }
    }

    reader.close()
}
}

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