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

long StartTime = System.nanoTime()

Sugar.enable()

def isinb = ! ( args[0].contains('outb') || args[0].contains('torus+1') )
def ismc  = args[0].contains("gemc")

def suff = isinb ? 'inb' : 'outb'
if(ismc) suff += '.mc'
else suff += '.qa'

def outname = args[0].split("/")[-1]

// File is made with just the scattered electron being detected (i.e., not looping to find the π+ pions for the SIDIS events)
def ff = new ROOTFile("MC_Gen_DIS_eX_richcap.${suff}.${outname}.root")

def tt = ff.makeTree('h22', 'title', 'event/I:runN/I:beamCharge:ex:ey:ez:esec/I')

int Total_Events_Found = 0

GParsPool.withPool 2,{
args.eachParallel{fname->
    println(fname)
    // QADB qa = new QADB()

    def reader = new HipoReader()
    reader.open(fname)
    def event = new Event()
    def factory = reader.getSchemaFactory()
    def banks = ['MC::Header', 'REC::Event', 'MC::Particle', 'REC::Calorimeter', 'REC::Cherenkov', 'REC::Traj', 'REC::Scintillator'].collect{new Bank(factory.getSchema(it))}

    while(reader.hasNext()){
        reader.nextEvent(event)
        banks.each{event.read(it)}

        if(banks.every()){
            def (runb, evb, partb, ecb, ccb, trajb, scb) = banks

            def run = runb.getInt("run",   0)
            def evn = runb.getInt("event", 0)
            def pid = partb.getInt("pid",  0)

            if(pid == 11){ // Is an electron
                def beamCharge = evb.getFloat("beamCharge", 0)
                def ex     = partb.getFloat("px", 0)
                def ey     = partb.getFloat("py", 0)
                def ez     = partb.getFloat("pz", 0)
                def ele    = LorentzVector.withPID(pid, ex, ey, ez)
                def elPhi  = (180/3.1415926)*ele.phi()
                def esec_a = 0 // Electron Sectors (From Angle)
                if(elPhi  >=  -30  && elPhi <   30){esec_a = 1}
                if(elPhi  >=   30  && elPhi <   90){esec_a = 2}
                if(elPhi  >=   90  && elPhi <  150){esec_a = 3}
                if(elPhi  >=  150  || elPhi < -150){esec_a = 4}
                if(elPhi  >=  -90  && elPhi <  -30){esec_a = 5}
                if(elPhi  >= -150  && elPhi <  -90){esec_a = 6}
                Total_Events_Found += 1; // Increment "total event" counter
                tt.fill(evn, run, beamCharge, ex, ey, ez, esec_a)
            }
        }
    }

    reader.close()
}
}

System.out.println("");

System.out.println("Total number of events found = " + Total_Events_Found);
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
