#!/usr/bin/env python3

import sys
import ROOT
import argparse
# import os
# import re
# import traceback
# from pathlib import Path

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
# from ExtraAnalysisCodeValues          import *
# from Convert_MultiDim_Kinematic_Bins  import *
from Binning_Dictionaries             import Full_Bin_Definition_Array #, Q2_y_Bin_rows_Array, Bin_Converter_4D_to_2D, Bin_Converter_5D
sys.path.remove(script_dir)
del script_dir

def Bin_Area_by_Widths_Calc(args=None, Q2_y_Bin=1, z_pT_Bin=1, phi_t_bin=15):
    # phi_t_bin should be 15 for the default phi_t plots since while the scale is applied to the full histogram, the per bin ∆phi_t is just the normal bin width
        # Update phi_t_bin whenever the bin sizes are changed
        # If the scale is applied to a 2D histogram of the other variables (i.e., integrated over the phi_t variable), then phi_t_bin should be set to 360
    Bin_Area = {"q2yTotal": 0, "zpTTotal": 0, "dQ2": 0, "d_y": 0, "dphi_t": phi_t_bin}
    for q2y_bin in range(1, 18):
        if(str(Q2_y_Bin) not in ["0", "All", str(q2y_bin)]):
            continue
        Bin_Area[f"Q2-y={q2y_bin}"] = {"q2yTotal": 0, "zpTTotal": 0, "dQ2": 0, "d_y": 0, "d_z": 0, "dpT": 0}
        Q2max, Q2min, y_max, y_min = Full_Bin_Definition_Array[f'Q2-y={q2y_bin}, Q2-y']
        Bin_Area[f"Q2-y={q2y_bin}"]["q2yTotal"] += abs(Q2max - Q2min)*abs(y_max - y_min)
        Bin_Area[f"Q2-y={q2y_bin}"]["dQ2"] += abs(Q2max - Q2min)
        Bin_Area[f"Q2-y={q2y_bin}"]["d_y"] += abs(y_max - y_min)
        Bin_Area["q2yTotal"] += abs(Q2max - Q2min)*abs(y_max - y_min)
        Bin_Area["dQ2"] += abs(Q2max - Q2min)
        Bin_Area["d_y"] += abs(y_max - y_min)
        for zpT_bin in range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=q2y_bin)[0] + 1):
            if((skip_condition_z_pT_bins(Q2_Y_BIN=q2y_bin, Z_PT_BIN=zpT_bin, BINNING_METHOD="Y_bin")) or (str(z_pT_Bin) not in ["0", "All", str(zpT_bin)])):
                continue
            z_max, z_min, pTmax, pTmin = Full_Bin_Definition_Array[f'Q2-y={q2y_bin}, z-pT={zpT_bin}']
            Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"] = {"q2yTotal": Bin_Area[f"Q2-y={q2y_bin}"]["q2yTotal"], "zpTTotal": abs(z_max - z_min)*abs(pTmax - pTmin), "d_z": abs(z_max - z_min), "dpT": abs(pTmax - pTmin)}
            Bin_Area[f"Q2-y={q2y_bin}"]["zpTTotal"]       += Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"]["zpTTotal"]
            Bin_Area[f"Q2-y={q2y_bin}"]["d_z"]            += Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"]["d_z"]
            Bin_Area[f"Q2-y={q2y_bin}"]["dpT"]            += Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"]["dpT"]
            Bin_Area["zpTTotal"]                          += Bin_Area[f"Q2-y={q2y_bin}"][f"z-pT={zpT_bin}"]["zpTTotal"]
    Bin_Width_Area_Scale = Bin_Area["q2yTotal"]*Bin_Area["zpTTotal"]*Bin_Area["dphi_t"]
    if((not hasattr(args, "verbose")) or args.verbose):
        print(f"Bin Area (∆Q2∆y∆z∆pT∆phi_t) for Bin ({Q2_y_Bin}-{z_pT_Bin}) = {Bin_Width_Area_Scale}")
    return Bin_Width_Area_Scale, Bin_Area

def lumi(charge):
    # Calculate the luminosity factor from input charge.
    # Parameters
    # charge : float
    #     Charge delivered, in nanocoulombs (nC).
    # Returns
    # float
    #     The luminosity factor in μb⁻¹ (microbarn⁻¹) units.
    # Constants
    RD   = 57.1                 # (unused, carried over)
    qe   = 1.602177e-19         # electron charge, C
    rho  = 0.0701               # density of H2 @20 K, g/cm³
    A0   = 6.0221367e23         # Avogadro’s number, mol⁻¹
    MH   = 1.00794              # atomic mass of H, g/mol
    LT   = 5.0                  # target length, cm
    CMB  = 1e30                 # cm² → μbarn
    # Convert input from nanocoulombs to coulombs
    charge_c = charge / 1e9
    # Number of target nuclei per cm²
    np_cm2 = LT * rho * A0 / MH
    # Number of electrons hitting the target
    ne = charge_c / qe
    # Luminosity factor in μb⁻¹
    factor = (ne * np_cm2) / CMB
    return factor

# 4.09744e+07 nC came from /lustre24/expphy/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/nSidis_* (as of 8/1/2025)
# 35023407.601823784 nC (or ~3.50234e+07 nC) came from `Charge_Summary_Data_sidis_epip_richcap.inb.qa.new8.nSidis_All_Files.json` as of 4/22/2026 (see '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/' for the log file)
def Cross_Section_Normalization(Histo=None, Q2_y_Bin=1, z_pT_Bin=1, phi_t_bin=15, Rename_Axis=False, args_in=None, charge_in=35023407.601823784, verbose_in=False):
    class args_custom:
        verbose = (args_in.verbose if(hasattr(args_in, "verbose")) else verbose_in) or ((Histo is None) and getattr(args_in, "verbose", True))
        charge  =  args_in.charge  if(hasattr(args_in, "charge"))  else charge_in
    Bin_Width_Area_Scale, _ = Bin_Area_by_Widths_Calc(args=args_custom, Q2_y_Bin=Q2_y_Bin, z_pT_Bin=z_pT_Bin, phi_t_bin=phi_t_bin)
    Luminosity = lumi(args_custom.charge)
    Normalize_Factor = 1.0
    if(args_custom.verbose):
        print(f"Luminosity = {Luminosity}")
    if(Histo is not None):
        if(Bin_Width_Area_Scale != 0.0):
            Histo.Scale(1.0/Bin_Width_Area_Scale)
            Normalize_Factor *= Bin_Width_Area_Scale
        else:
            print(f"\n{color.Error}Failed to scale histogram: {color.END_B}{Histo.GetName()}{color.END}\n")
            raise ValueError(f"Failed to scale histogram to 'Bin_Width_Area_Scale'. Bin Area = 0.")
        if(Luminosity != 0.0):
            Histo.Scale(1.0/Luminosity)
            Normalize_Factor *= Luminosity
        else:
            print(f"\n{color.Error}Failed to scale histogram: {color.END_B}{Histo.GetName()}{color.END}\n")
            raise ValueError(f"Failed to scale histogram to 'Luminosity'. Luminosity = 0.")
        if(Rename_Axis):
            Histo.GetYaxis().SetTitle("#frac{#sigma}{dQ^{2}dydzdP_{T}d#phi_{h}}")
        Histo.Normalize_Factor = Normalize_Factor
    return Histo, Bin_Width_Area_Scale, Luminosity
    
if(__name__ == "__main__"):
    class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
        pass
    p = argparse.ArgumentParser(description="Contains the functions used for normalizing to the differential cross section. This script is not meant to be used by itself, but it can print the normalation factors (including bin area and Luminosity) for a given kinematic bin if so desired.", formatter_class=RawDefaultsHelpFormatter)
    p.add_argument("-q2y", "-q2_y", "--Q2_y_Bin",
                   type=int,
                   default=1,
                   help="Q2-y bin to evaluate. Select '0' for 'All Bins'.")
    p.add_argument("-zpt", '-z_pt', '--z_pT_Bin',
                   type=int,
                   default=0,
                   help="z-pT bin to evaluate. Select '0' for 'All Bins'.")
    p.add_argument('-phi', '--phi_t_bin',
                   type=int,
                   default=15,
                   help="Size of the phi_t bin in degrees.")
    p.add_argument('-c', '--charge',
                   type=float,
                   default=4.09744e+07,
                   help="Charge (in 'nC') deposited in the experimental files (used for luminosity calculation).\nDefault value came from '/lustre24/expphy/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/nSidis_*' as of 8/1/2025.")
    p.add_argument('-v', '--verbose',
                   action='store_true',
                   help="Verbose prints.")
    args = p.parse_args()
    Cross_Section_Normalization(Histo=None, Q2_y_Bin=args.Q2_y_Bin, z_pT_Bin=args.z_pT_Bin, phi_t_bin=args.phi_t_bin, Rename_Axis=False, args_in=args, charge_in=args.charge, verbose_in=args.verbose)
    print("\nDone\n")
