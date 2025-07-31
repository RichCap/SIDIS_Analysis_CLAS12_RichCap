#!/usr/bin/env python3
import sys
import argparse


parser = argparse.ArgumentParser(description="Make Comparisons between Data, clasdis MC, and EvGen MC (based on Using_RDataFrames.ipynb)")
parser.add_argument('-kc', '--kinematic-compare', action='store_true', 
                    help='Runs Kinematic Comparisons')
parser.add_argument('-ac', '--acceptance-all',    action='store_true', 
                    help='Runs Acceptance Comparisons (no binning)')
parser.add_argument('-ab', '--acceptance',        action='store_true', 
                    help='Runs Binned Acceptance Comparisons (for all kinematic bins)')
parser.add_argument('-v',  '--verbose',           action='store_true', 
                    help='Prints more info while running')
parser.add_argument('-c',  '--cut',               type=str,
                    help='Adds additional cuts based on user input (Warning: applies to all datasets)')
parser.add_argument('-sf', '--File_Save_Format',  type=str, default=".png", choices=['.png', '.pdf'],
                    help='Save Format of Images')
parser.add_argument('-n', '--name',               type=str,
                    help='Extra save name that can be added to the saved images')
parser.add_argument('-t', '--title',              type=str,
                    help='Extra title text that can be added to the default titles')
parser.add_argument('-nrdf', '--num-rdf-files',   type=int, default=5,
                    help='Number of rdf RDataFrames to be included (Default = 5)')
parser.add_argument('-nMC', '--num-MC-files',     type=int, default=1,
                    help='Number of MC RDataFrames (MC REC and MC GEN) to be included (Default = 1)')
parser.add_argument('-hMX', '--use_HIGH_MX',       action='store_true',
                    help='Use with "-kc" option to normalize to High-Mx region')

args = parser.parse_args()

import ROOT, numpy, re
import traceback

# Add the path to sys.path temporarily
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
from ExtraAnalysisCodeValues import *
# Now you can remove the path if you wish
sys.path.remove(script_dir)
del script_dir

import math
import array
import copy


def variable_Title_name_new(variable_in):
    if(variable_in in ["k0_cut"]):
        return "E^{Cutoff}_{#gamma}"
    else:
        output = variable_Title_name(variable_in)
        output = output.replace(" (lepton energy loss fraction)", "")
        return output

def find_max_bin(hist):
    max_content = 0
    for bin_ii in range(1, hist.GetNbinsX() + 1):
        bin_content = hist.GetBinContent(bin_ii)
        if(bin_content > max_content):
            max_content = bin_content
    return max_content


ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')

ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)

ROOT.gStyle.SetOptStat(0)

ROOT.gROOT.SetBatch(1)

if(args.verbose):
    print(f"\n{color.BOLD}DEFINING CUT FUNCTIONS{color.END}\n")
Skipped_Fiducial_Cuts = ["Hpip", "DC_pip", "Electron"] # i.e. FC_14
##########################################################################################################################################################################################
##########################################################################################################################################################################################
Use_New_PF = True
def filter_Valerii(Data_Frame, Valerii_Cut, Include_Pion=Use_New_PF):
    if(("Valerii_Cut" in Valerii_Cut) or ("Complete" in Valerii_Cut)):
        Data_Frame_Clone = Data_Frame.Filter("".join(["""
            auto func = [&](double x, double k, double b){
                return k * x + b;
            };
            struct line{
                double k;
                double b;
            };
            auto isOutOfLines = [&](double x, double y, line topLine, line botLine){
                return y > func(x, topLine.k, topLine.b) || y < func(x, botLine.k, botLine.b);
            };
            auto BadElementKnockOut = [&](double hx, double hy, int sector, int cutLevel){
                double widthChange = 0;
                if (cutLevel == 0)  widthChange = -1;
                if (cutLevel == 2)  widthChange = 1;
                if (sector == 5) return true;
                if (sector == 1){
                    double k = tan(29.5*3.1415/180);
                    double b = -92;
                    bool test_sec_1 = (isOutOfLines(hx, hy, {k, b + widthChange} , {k, b - widthChange - 2.4}) && isOutOfLines(hx, hy, {k, b + widthChange - 9.1} , {k, b - widthChange - 9.1 - 2.4}) && isOutOfLines(hx, hy, {k, b + widthChange - 127} , {k, b - widthChange - 127 - 2.4}) && isOutOfLines(hx, hy, {k, b + widthChange - 127 - 8} , {k, b - widthChange -127 - 8 - 2.4}) );
                           
                    return test_sec_1;       
                }
                if (sector == 2){
                    double k = tan(30.4*3.1415/180);
                    double b = 120.5;
                    bool test_sec_2 = (isOutOfLines(hx, hy, {k, b + widthChange} , {k, b - widthChange - 4.4}));
                    return test_sec_2;
                }
                if (sector == 3){
                    bool test_sec_3 = ((hx - widthChange) > - 303 || (hx + widthChange) < -310);
                    return test_sec_3;
                }
                if (sector == 4){
                    double k = tan(-29.6*3.1415/180);
                    double b = -232.8;
                    bool test_sec_4 = (isOutOfLines(hx, hy, {k, b + widthChange} , {k, b - widthChange - 3.5}));
                    
                    return test_sec_4;
                }
                if (sector == 6){
                    double k = tan(-30.6*3.1415/180);
                    double b = -185;
                    
                    bool test_sec_6 = (isOutOfLines(hx, hy, {k, b + widthChange} , {k, b - widthChange - 2}) && isOutOfLines(hx, hy, {k, b + widthChange - 8.3} , {k, b - widthChange - 8.3 - 2.2}) );
                    
                    return test_sec_6;
                }
                return false;
            };
            """, "return BadElementKnockOut(Hx, Hy, esec, 1);" if((not Include_Pion) or True) else "return (BadElementKnockOut(Hx, Hy, esec, 1) && BadElementKnockOut(Hx_pip, Hy_pip, pipsec, 1));"]))
        return Data_Frame_Clone
    else:
        return Data_Frame

###################=======================================###################
##===============##        Full Filter + Cut Title        ##===============##
###################=======================================###################

def DF_Filter_Function_Full(DF_Out, Titles_or_DF="DF", Data_Type="rdf", Cut_Choice="no_cut", Smearing_Q=""):
    ##################################################
    ##==========## General Cuts (Start) ##==========##
    ##################################################
    cutname = " "
    if((Data_Type in ["pdf", "gen"]) and (Titles_or_DF == 'DF')):
        DF_Out = DF_Out.Filter("PID_el != 0 && PID_pip != 0")
    if((Cut_Choice in ["cut_Gen"])         and (Data_Type not in ["rdf"])):
        cutname         = "Generated MM Cut"
        if(Titles_or_DF == 'DF'):
            if(Data_Type in ["gdf"]):
                DF_Out  = DF_Out.Filter("sqrt(MM2) > 1.5")
            else:
                DF_Out  = DF_Out.Filter("sqrt(MM2_gen) > 1.5")       
    elif((Cut_Choice in ["cut_Exgen"])     and (Data_Type not in ["rdf"])):
        cutname         = "Generated MM Cut (Exclusive Events)"
        if(Titles_or_DF == 'DF'):
            if(Data_Type in ["gdf"]):
                DF_Out  = DF_Out.Filter("sqrt(MM2) < 1.5")
            else:
                DF_Out  = DF_Out.Filter("sqrt(MM2_gen) < 1.5")
    elif((Data_Type not in ["gdf", "gen"]) and ("no_cut" not in str(Cut_Choice))):
        if("Complete"   in Cut_Choice):
            cutname     = "Complete Set of "
            if(("smear" in Smearing_Q)     and (Data_Type != "rdf")):
                cutname = f"{cutname}(Smeared) "
            if(Titles_or_DF == 'DF'):
                DF_Out  = filter_Valerii(DF_Out, Cut_Choice)
                DF_Out  = New_Fiducial_Cuts_Function(Data_Frame_In=DF_Out, Skip_Options=Skipped_Fiducial_Cuts)
                if(("smear" in Smearing_Q) and (Data_Type != "rdf")):
                    if("str" in str(type(DF_Out))):
                        print(f"DF_Out = {type(DF_Out)}({DF_Out})")
                    # DF_Out  = DF_Out.Filter("smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 2 && smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
                    DF_Out  = DF_Out.Filter("(y_smeared < 0.75) && (xF_smeared > 0) && (W_smeared > 2) && (Q2_smeared > 2) && (pip_smeared > 1.25) && (pip_smeared < 5) && (5 < elth_smeared) && (elth_smeared < 35) && (5 < pipth_smeared) && (pipth_smeared < 35)")
                else:
                    DF_Out  = DF_Out.Filter("y < 0.75 && xF > 0 && W > 2 && Q2 > 2 && pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
            if("EDIS"   in Cut_Choice):
                cutname = f"{cutname} Exclusive "
                if(Titles_or_DF == 'DF'):
                    DF_Out      = DF_Out.Filter(str(Calculated_Exclusive_Cuts(Smearing_Q)))
            if("SIDIS"  in Cut_Choice):
                cutname = f"{cutname} SIDIS "
                # # REMOVED AS A TEST FOR THE COMPARISONS - NOT A PART OF THE ACTUAL ANALYSIS CUTS
                # if(Titles_or_DF == 'DF'):
                #     if(("smear" in Smearing_Q) and (Data_Type != "rdf")):
                #         # DF_Out  = DF_Out.Filter("sqrt(smeared_vals[1]) > 1.5")
                #         DF_Out  = DF_Out.Filter("sqrt(MM2_smeared) > 1.5")
                #     else:
                #         DF_Out  = DF_Out.Filter("sqrt(MM2) > 1.5")
            if("Proton" in Cut_Choice):
                cutname = f"{cutname} (Proton Cut) "
                if(Titles_or_DF == 'DF'):
                    DF_Out  = DF_Out.Filter("MM_pro > 1.35")
            if("RevPro" in Cut_Choice):
                cutname = f"{cutname} (Inverted Proton Cut) "
                if(Titles_or_DF == 'DF'):
                    DF_Out  = DF_Out.Filter("MM_pro < 1.35")
            # if("Binned"  in Cut_Choice):
            #     cutname = f"{cutname} (Binned) "
            #     if(Titles_or_DF == 'DF'):
            #         if(("smear" in Smearing_Q) and (Data_Type != "rdf")):
            #             if("5" in binning_option_list or "Y_bin"  in binning_option_list or "Y_Bin" in binning_option_list):
            #                 DF_Out = DF_Out.Filter("(Q2_Y_Bin_smeared > 0 && Q2_Y_Bin_smeared < 18) && (z_pT_Bin_Y_bin_smeared > 0)")
            #             else:
            #                 DF_Out = DF_Out.Filter("(Q2_y_Bin_smeared > 0 && Q2_y_Bin_smeared < 18) && (z_pT_Bin_y_bin_smeared > 0)")
            #         else:
            #             if("5" in binning_option_list or "Y_bin"  in binning_option_list or "Y_Bin" in binning_option_list):
            #                 DF_Out = DF_Out.Filter("(Q2_Y_Bin > 0 && Q2_Y_Bin < 18) && (z_pT_Bin_Y_bin > 0)")
            #             else:
            #                 DF_Out = DF_Out.Filter("(Q2_y_Bin > 0 && Q2_y_Bin < 18) && (z_pT_Bin_y_bin > 0)")
            if("MM" in Cut_Choice):
                cutname = f"{cutname} (Inverted MM) "
                if(Titles_or_DF == 'DF'):
                    if("smear" in Smearing_Q   and Data_Type != "rdf"):
                        DF_Out  = DF_Out.Filter("sqrt(smeared_vals[1]) < 1.5")
                    else:
                        DF_Out  = DF_Out.Filter("sqrt(MM2) < 1.5")
            if(("Gen" in Cut_Choice)           and (Data_Type not in ["rdf"])):
                cutname = f"{cutname} (Gen MM) "
                if(Titles_or_DF == 'DF'):
                    if(Data_Type in ["gdf"]):
                        DF_Out  = DF_Out.Filter("sqrt(MM2) > 1.5")
                    else:
                        DF_Out  = DF_Out.Filter("sqrt(MM2_gen) > 1.5")
            if(("Exgen" in Cut_Choice)         and (Data_Type not in ["rdf"])):
                cutname = f"{cutname} (Exclusive Gen MM) "
                if(Titles_or_DF == 'DF'):
                    if(Data_Type in ["gdf"]):
                        DF_Out  = DF_Out.Filter("sqrt(MM2) < 1.5")
                    else:
                        DF_Out  = DF_Out.Filter("sqrt(MM2_gen) < 1.5")
            cutname = f"{cutname} Cuts"
            # if(Skipped_Fiducial_Cuts != Default_Cut_Option):
            #     cutname = f"{cutname} (Skipped these Fiducial Cuts: {Skipped_Fiducial_Cuts})"
    else:
        # Generated Monte Carlo should not have cuts applied to it (until now...)
        cutname = "No Cuts"

    if("Integrate" in Cut_Choice):
        cutname = f"{cutname} (Bins for Integration)"
        if(Titles_or_DF == 'DF'):
            Bin_Integrate_Cuts = "((Q2_Y_Bin == 1) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 10) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 16) || (z_pT_Bin_Y_bin == 17))) || ((Q2_Y_Bin == 2) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 20) || (z_pT_Bin_Y_bin == 21))) || ((Q2_Y_Bin == 3) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 20) || (z_pT_Bin_Y_bin == 21))) || ((Q2_Y_Bin == 4) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 20) || (z_pT_Bin_Y_bin == 21) || (z_pT_Bin_Y_bin == 25) || (z_pT_Bin_Y_bin == 26) || (z_pT_Bin_Y_bin == 27))) || ((Q2_Y_Bin == 5) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 20) || (z_pT_Bin_Y_bin == 21))) || ((Q2_Y_Bin == 6) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15))) || ((Q2_Y_Bin == 7) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 20) || (z_pT_Bin_Y_bin == 21) || (z_pT_Bin_Y_bin == 25) || (z_pT_Bin_Y_bin == 26) || (z_pT_Bin_Y_bin == 27))) || ((Q2_Y_Bin == 8) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 4) || (z_pT_Bin_Y_bin == 6) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 11) || (z_pT_Bin_Y_bin == 12) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 16) || (z_pT_Bin_Y_bin == 17) || (z_pT_Bin_Y_bin == 18) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 21) || (z_pT_Bin_Y_bin == 22) || (z_pT_Bin_Y_bin == 23) || (z_pT_Bin_Y_bin == 24) || (z_pT_Bin_Y_bin == 26) || (z_pT_Bin_Y_bin == 27) || (z_pT_Bin_Y_bin == 28) || (z_pT_Bin_Y_bin == 29) || (z_pT_Bin_Y_bin == 31) || (z_pT_Bin_Y_bin == 32) || (z_pT_Bin_Y_bin == 33) || (z_pT_Bin_Y_bin == 34))) || ((Q2_Y_Bin == 9) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 4) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 10) || (z_pT_Bin_Y_bin == 11) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 16) || (z_pT_Bin_Y_bin == 17) || (z_pT_Bin_Y_bin == 18))) || ((Q2_Y_Bin == 10) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 20) || (z_pT_Bin_Y_bin == 21))) || ((Q2_Y_Bin == 11) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 6) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 11) || (z_pT_Bin_Y_bin == 12) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 16) || (z_pT_Bin_Y_bin == 17) || (z_pT_Bin_Y_bin == 18))) || ((Q2_Y_Bin == 12) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 4) || (z_pT_Bin_Y_bin == 6) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 11) || (z_pT_Bin_Y_bin == 12) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 16) || (z_pT_Bin_Y_bin == 17) || (z_pT_Bin_Y_bin == 18) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 21) || (z_pT_Bin_Y_bin == 22) || (z_pT_Bin_Y_bin == 23) || (z_pT_Bin_Y_bin == 24))) || ((Q2_Y_Bin == 13) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 6) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 11) || (z_pT_Bin_Y_bin == 12) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 16) || (z_pT_Bin_Y_bin == 17) || (z_pT_Bin_Y_bin == 18))) || ((Q2_Y_Bin == 14) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 19) || (z_pT_Bin_Y_bin == 20) || (z_pT_Bin_Y_bin == 21))) || ((Q2_Y_Bin == 15) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 6) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 11) || (z_pT_Bin_Y_bin == 12) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 16) || (z_pT_Bin_Y_bin == 17) || (z_pT_Bin_Y_bin == 18))) || ((Q2_Y_Bin == 16) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15))) || ((Q2_Y_Bin == 17) && ((z_pT_Bin_Y_bin == 1) || (z_pT_Bin_Y_bin == 2) || (z_pT_Bin_Y_bin == 3) || (z_pT_Bin_Y_bin == 4) || (z_pT_Bin_Y_bin == 7) || (z_pT_Bin_Y_bin == 8) || (z_pT_Bin_Y_bin == 9) || (z_pT_Bin_Y_bin == 10) || (z_pT_Bin_Y_bin == 13) || (z_pT_Bin_Y_bin == 14) || (z_pT_Bin_Y_bin == 15) || (z_pT_Bin_Y_bin == 16)))"
            if(("smear" in Smearing_Q) and (Data_Type != "rdf")):
                Bin_Integrate_Cuts = Bin_Integrate_Cuts.replace("in ==", "in_smeared ==")
            DF_Out = DF_Out.Filter(Bin_Integrate_Cuts)
    for sec in range(1, 7, 1):
        if("eS" not in Cut_Choice):
            break
        if(f"eS{sec}a" in Cut_Choice):
            cutname = f"{cutname} (Excluding Sector {sec} Electrons)"
            if(Titles_or_DF == 'DF'):
                DF_Out  = DF_Out.Filter(f"esec != {sec}")
                if(Data_Type in ["pdf", "gen"]):
                    DF_Out  = DF_Out.Filter(f"esec_gen != {sec}")
            break
        if(f"eS{sec}o" in Cut_Choice):
            cutname = f"{cutname} (Sector {sec} Electrons Only)"
            if(Titles_or_DF == 'DF'):
                DF_Out  = DF_Out.Filter(f"esec == {sec}")
                if(Data_Type in ["pdf", "gen"]):
                    DF_Out  = DF_Out.Filter(f"esec_gen == {sec}")
            break
    ##################################################
    ##==========##  General Cuts (End)  ##==========##
    ##################################################


    ###########################################
    ##=======================================##
    ##==========## Final Outputs ##==========##
    ##=======================================##
    ###########################################

    ##==========## Cut Name ##==========##
    if(Titles_or_DF == 'Cut'):
        return cutname
    ##==========## Cut Name ##==========##

    ##==========## Data Frame Output ##==========##
    if(Titles_or_DF == 'DF'): 
        return DF_Out
    ##==========## Data Frame Output ##==========##

    ###########################################
    ##=======================================##
    ##==========## Final Outputs ##==========##
    ##=======================================##
    ###########################################

###################=======================================###################
##===============##     Full Filter + Cut Title (End)     ##===============##
###################=======================================###################
    
##########################################################################################################################################################################################
##########################################################################################################################################################################################

if(args.verbose):
    print(f"\n{color.BOLD}CREATING FUNCTIONS FOR MAKING KINEMATIC BINNED ACCEPTANCE PLOTS\n{color.END}")
def Create_Binned_Acceptance_Hist(mdf_IN, gdf_IN, source, PHI_T_Binning=['phi_t', 0, 360, 24], Q2_Y_Bin=None, Z_PT_Bin=None):
    var, Min_range, Max_range, Num_of_Bins = PHI_T_Binning
    mdf_name = f"{var}_mdf_{source}"
    gdf_name = f"{var}_gdf_{source}"
    if(Q2_Y_Bin):
        mdf_IN_Binned     =        mdf_IN.Filter(f"Q2_Y_Bin == {Q2_Y_Bin}")
        gdf_IN_Binned     =        gdf_IN.Filter(f"Q2_Y_Bin == {Q2_Y_Bin}")
        if(Z_PT_Bin):
            mdf_IN_Binned = mdf_IN_Binned.Filter(f"z_pT_Bin_Y_bin == {Z_PT_Bin}")
            gdf_IN_Binned = gdf_IN_Binned.Filter(f"z_pT_Bin_Y_bin == {Z_PT_Bin}")
            mdf_name      = f"{mdf_name} Bin ({Q2_Y_Bin}-{Z_PT_Bin})"
            gdf_name      = f"{gdf_name} Bin ({Q2_Y_Bin}-{Z_PT_Bin})"
        else:
            mdf_name      = f"{mdf_name} Bin ({Q2_Y_Bin}-All)"
            gdf_name      = f"{gdf_name} Bin ({Q2_Y_Bin}-All)"
    else:
        mdf_IN_Binned     =        mdf_IN
        gdf_IN_Binned     =        gdf_IN

    mdf_hist = mdf_IN_Binned.Histo1D((mdf_name, f"{variable_Title_name_new(var)} from MC REC ({source}); {variable_Title_name_new(var)}", Num_of_Bins, Min_range, Max_range), var if(source not in ["clasdis"]) else f"{var}_smeared")
    gdf_hist = gdf_IN_Binned.Histo1D((gdf_name, f"{variable_Title_name_new(var)} from MC GEN ({source}); {variable_Title_name_new(var)}", Num_of_Bins, Min_range, Max_range), var)

    if(source in ["clasdis"]):
        mdf_hist.SetTitle(f"(Smeared) {mdf_hist.GetTitle()}")
        mdf_hist.GetXaxis().SetTitle(f"{variable_Title_name_new(var)} (Smeared)")
    if(Q2_Y_Bin):
        if(Z_PT_Bin):
            mdf_hist.SetTitle(f"#splitline{{{mdf_hist.GetTitle()}}}{{#color[{ROOT.kRed}]{{Q^{{2}}-y Bin: {Q2_Y_Bin}}} #topbar #color[{ROOT.kRed}]{{z-P_{{T}} Bin: {Z_PT_Bin}}}}}")
            gdf_hist.SetTitle(f"#splitline{{{gdf_hist.GetTitle()}}}{{#color[{ROOT.kRed}]{{Q^{{2}}-y Bin: {Q2_Y_Bin}}} #topbar #color[{ROOT.kRed}]{{z-P_{{T}} Bin: {Z_PT_Bin}}}}}")
        else:
            mdf_hist.SetTitle(f"#splitline{{{mdf_hist.GetTitle()}}}{{#color[{ROOT.kRed}]{{Q^{{2}}-y Bin: {Q2_Y_Bin}}}}}")
            gdf_hist.SetTitle(f"#splitline{{{gdf_hist.GetTitle()}}}{{#color[{ROOT.kRed}]{{Q^{{2}}-y Bin: {Q2_Y_Bin}}}}}")
            
    mdf_hist.SetLineColor(ROOT.kRed   if(source in ["clasdis"]) else ROOT.kMagenta)
    gdf_hist.SetLineColor(ROOT.kGreen if(source in ["clasdis"]) else ROOT.kCyan)
    
    mdf_hist.Sumw2()
    gdf_hist.Sumw2()
    
    acc_hist  = mdf_hist.Clone(mdf_name.replace("mdf", "Acceptance"))
    acc_hist.Divide(gdf_hist.GetValue())
    # acc_title = f"#scale[2]{{Acceptance for {variable_Title_name_new(var)} from {source}}}"
    acc_title = f"#scale[1]{{Acceptance for {variable_Title_name_new(var)} from {source}}}"
    if(Q2_Y_Bin):
        if(Z_PT_Bin):
            acc_title = f"#splitline{{{acc_title}}}{{#color[{ROOT.kRed}]{{Q^{{2}}-y Bin: {Q2_Y_Bin}}} #topbar #color[{ROOT.kRed}]{{z-P_{{T}} Bin: {Z_PT_Bin}}}}}"
        else:
            acc_title = f"#splitline{{{acc_title}}}{{#color[{ROOT.kRed}]{{Q^{{2}}-y Bin: {Q2_Y_Bin}}}}}"
    if(args.title):
        acc_title     = f"#splitline{{{acc_title}}}{{{args.title}}}"
    acc_hist.SetTitle(acc_title)
    acc_hist.GetYaxis().SetTitle("Acceptance")
    acc_hist.SetLineColor(ROOT.kAzure if(source not in ["clasdis"]) else ROOT.kAzure + 10)

    return mdf_hist, gdf_hist, acc_hist


def Acceptance_Compare_z_pT_Images_Together(Histogram_List_All, Q2_Y_Bin, Plot_Orientation="z_pT", Saving_Q=True, File_Save_Format=args.File_Save_Format):
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    # Use above for normal size, use below for 2x size (made with PDFs)
    Save_Name = f"Acceptance_Compare_for_Q2_Y_Bin_{Q2_Y_Bin}"
    # All_z_pT_Canvas = Canvas_Create(Name=Save_Name, Num_Columns=2, Num_Rows=1, Size_X=int(1800*4), Size_Y=int(1500*4), cd_Space=0.01)
    All_z_pT_Canvas = Canvas_Create(Name=Save_Name, Num_Columns=2, Num_Rows=1, Size_X=int(1800*2), Size_Y=int(1500*2), cd_Space=0.01)
    # All_z_pT_Canvas = Canvas_Create(Name=Save_Name, Num_Columns=2, Num_Rows=1, Size_X=int(1800), Size_Y=int(1500), cd_Space=0.01)
    All_z_pT_Canvas.SetFillColor(ROOT.kGray)
    All_z_pT_Canvas_cd_1       = All_z_pT_Canvas.cd(1)
    All_z_pT_Canvas_cd_1.SetFillColor(ROOT.kGray)
    All_z_pT_Canvas_cd_1.SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
    All_z_pT_Canvas_cd_1.Divide(1, 2, 0, 0)

    All_z_pT_Canvas_cd_1_Upper = All_z_pT_Canvas_cd_1.cd(1)
    All_z_pT_Canvas_cd_1_Upper.SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
    All_z_pT_Canvas_cd_1_Upper.Divide(1, 2, 0, 0)

    All_z_pT_Canvas_cd_1_Lower = All_z_pT_Canvas_cd_1.cd(2)
    All_z_pT_Canvas_cd_1_Lower.SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
    All_z_pT_Canvas_cd_1_Lower.Divide(1, 1, 0, 0)
    All_z_pT_Canvas_cd_1_Lower.cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)

    All_z_pT_Canvas_cd_2               = All_z_pT_Canvas.cd(2)
    All_z_pT_Canvas_cd_2.SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
    All_z_pT_Canvas_cd_2.SetFillColor(ROOT.kGray)

    if(Plot_Orientation in ["z_pT"]):
        number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
        All_z_pT_Canvas_cd_2.Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)
    else:
        number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
        All_z_pT_Canvas_cd_2.Divide(1, number_of_cols, 0.0001, 0.0001)
        for ii in range(1, number_of_cols + 1, 1):
            All_z_pT_Canvas_cd_2_cols = All_z_pT_Canvas_cd_2.cd(ii)
            All_z_pT_Canvas_cd_2_cols.Divide(number_of_rows, 1, 0.0001, 0.0001)
    
    ####  Canvas (Main) Creation End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Left)  ###################################################################################################################################################################################################################################################################################################################################################################################
    
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ####  Upper Left - i.e., 2D Histograms  ############################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    Q2_y_Name = f"Q2-y Bin ({Q2_Y_Bin}-All)"
    z_pT_Name = f"z-pT Bin ({Q2_y_Bin}-All)"
    ##===============##     Drawing Q2-y Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    Draw_Canvas(All_z_pT_Canvas_cd_1_Upper, 1, 0.15)
    Histogram_List_All[Q2_y_Name].Draw("colz")
    Histogram_List_All[Q2_y_Name].SetStats(1)
    # ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptStat("i")
    stats = Histogram_List_All[Q2_y_Name].GetListOfFunctions().FindObject("stats")
    if(stats):
        stats.SetX1NDC(0.80)  # New X start position
        stats.SetX2NDC(0.90)  # New X end position
        stats.SetY1NDC(0.85) # New Y start position
        stats.SetY2NDC(0.95) # New Y end position
    else:
        print(f"{color.Error}Error in (Q2-y) stat_box of Histogram_List_All[{Q2_y_Name}]...{color.END}\n\tstats = {stats}")
    palette_move(canvas=All_z_pT_Canvas_cd_1_Upper.cd(1), histo=Histogram_List_All[Q2_y_Name], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    # Histogram_List_All[Q2_y_Name].SetStats(0)
    Q2_y_borders = {}
    for Q2_Y_Bin_ii in range(1, 18, 1):
        Q2_y_borders[Q2_Y_Bin_ii] = Draw_Q2_Y_Bins(Input_Bin=Q2_Y_Bin_ii)
        for line in Q2_y_borders[Q2_Y_Bin_ii]:
            line.Draw("same")
    if(Q2_Y_Bin in range(1,18)):
        for line_Bin in Q2_y_borders[Q2_Y_Bin]:
            line_Bin.SetLineColor(ROOT.kRed)
            line_Bin.SetLineWidth(6)
            line_Bin.Draw("same")
    ##===============##     Drawing Q2-y Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ##===============##     Drawing z-pT Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    Draw_Canvas(All_z_pT_Canvas_cd_1_Upper, 2, 0.15)
    Histogram_List_All[z_pT_Name].Draw("colz")
    Histogram_List_All[z_pT_Name].SetStats(1)
    ROOT.gStyle.SetOptStat("i")
    # ROOT.gStyle.SetOptStat(0)
    stats = Histogram_List_All[z_pT_Name].GetListOfFunctions().FindObject("stats")
    if(stats):
        stats.SetX1NDC(0.80)  # New X start position
        stats.SetX2NDC(0.90)  # New X end position
        stats.SetY1NDC(0.85) # New Y start position
        stats.SetY2NDC(0.95) # New Y end position
    else:
        print(f"{color.Error}Error in (z-pT) stat_box of Histogram_List_All[{z_pT_Name}]...{color.END}\n\tstats = {stats}")
    palette_move(canvas=All_z_pT_Canvas_cd_1_Upper.cd(2), histo=Histogram_List_All[z_pT_Name], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
    # ROOT.gStyle.SetOptStat(1111)
    if(Plot_Orientation in ["pT_z"]):
        if(str(Q2_Y_Bin) not in ["0", "All"]):
            Histogram_List_All[z_pT_Name].GetXaxis().SetRangeUser(0, 1.2)
            Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin, Set_Max_Y=1.2, Set_Max_X=1.2, Plot_Orientation_Input=Plot_Orientation)
            MM_z_pT_borders = {}
            MM_z_pT_legend = ROOT.TLegend(0.8, 0.1, 0.95, 0.4)
            MM_z_pT_legend.SetNColumns(1)
            MM_z_pT_borders, MM_z_pT_legend = Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin, Plot_Orientation)
            for MM_lines in MM_z_pT_borders:
                MM_z_pT_borders[MM_lines].Draw("same")
            MM_z_pT_legend.Draw("same")
    else:
        if(str(Q2_Y_Bin) not in ["All", "0"]):
            Histogram_List_All[z_pT_Name].GetXaxis().SetRangeUser(0, 1.2)
            Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=Q2_Y_Bin, Set_Max_Y=1.2, Set_Max_X=1.2)
            MM_z_pT_borders = {}
            MM_z_pT_legend = ROOT.TLegend(0.5, 0.1, 0.9, 0.2)
            MM_z_pT_legend.SetNColumns(2)
            MM_z_pT_borders, MM_z_pT_legend = Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders, Q2_Y_Bin, Plot_Orientation)
            for MM_lines in MM_z_pT_borders:
                MM_z_pT_borders[MM_lines].Draw("same")
            MM_z_pT_legend.Draw("same")
    ##===============##     Drawing z-pT Histogram     ##===============## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    
    ####  Upper Left - i.e., 2D Histograms  ############################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ######################################################################=========================================================================================================================================================================================================================================================================#################################################################
    ######################################################################=========================================================================================================================================================================================================================================================================#################################################################
    ####  Lower Left - i.e., Integrated z-pT Bin  ######################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    
    Draw_Canvas(All_z_pT_Canvas_cd_1_Lower, 1, 0.15)
    ROOT.gStyle.SetOptStat(0)
    cd_1_Lower_max = max([find_max_bin(Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"]), find_max_bin(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"]), Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"]])
    Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"].GetYaxis().SetRangeUser(0,   1.2*cd_1_Lower_max)
    Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"].GetYaxis().SetRangeUser(0, 1.2*cd_1_Lower_max)
    Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"].Draw("E0 hist")
    Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"].Draw("E0 hist same")
    
    legend = ROOT.TLegend(0.65, 0.70, 0.92, 0.88, "", "NDC")
    legend.SetNColumns(1)  # or 2 for side-by-side entries
    # legend.SetBorderSize(0)   # no border
    legend.SetFillStyle(1)    # transparent background
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.SetMargin(0.15)    # internal padding
    legend.AddEntry(Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"],   f"#color[{ROOT.kAzure   }]{{Acceptance EvGen}}",   "lep")
    legend.AddEntry(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"], f"#color[{ROOT.kAzure+10}]{{Acceptance clasdis}}", "lep")
    legend.Draw()

    ####  Lower Left - i.e., Integrated z-pT Bin  ######################## ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ###################################################################### ################################################################# ################################################################# ################################################################# ################################################################# #################################################################
    ####  Filling Canvas (Left) End ################################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Right) - i.e., Individual z-pT Bins  #####################################################################################################################################################################################################################################################################################################################################################
    z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1]
    for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
        if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=False)):
            continue
        cd_number_of_z_pT_all_together = z_pT_Bin        

        try:
            if(Plot_Orientation in ["z_pT"]):
                All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2.cd(cd_number_of_z_pT_all_together)
                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(ROOT.kGray)
                All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
            else:
                cd_row = int(cd_number_of_z_pT_all_together/number_of_cols) + 1
                if(0 == (cd_number_of_z_pT_all_together%number_of_cols)):
                    cd_row += -1
                cd_col = cd_number_of_z_pT_all_together - ((cd_row - 1)*number_of_cols)
                
                All_z_pT_Canvas_cd_2_z_pT_Bin_Row = All_z_pT_Canvas_cd_2.cd((number_of_cols - cd_col) + 1)
                All_z_pT_Canvas_cd_2_z_pT_Bin     = All_z_pT_Canvas_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)
    
                All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(ROOT.kGray)
                All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
                
            Draw_Canvas(All_z_pT_Canvas_cd_2_z_pT_Bin, 1, 0.15)
            ROOT.gStyle.SetOptStat(0)
            Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetYaxis().SetRangeUser(0,   1.2*Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"])
            Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetYaxis().SetRangeUser(0, 1.2*Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"])
            Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Draw("E0 hist")
            Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Draw("E0 hist same")
        except:
            print(f"{color.Error}Error in Drawing Acceptance Plots for Bin ({Q2_y_Bin}-{z_pT_Bin}):\n{color.END_R}{str(traceback.format_exc())}{color.END}")
        
    ####  Filling Canvas (Right) - i.e., Individual z-pT Bins (End)  ###############################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    if(args.name):
        Save_Name = f"{Save_Name}_{args.name}{File_Save_Format}"
    else:
        Save_Name = f"{Save_Name}{File_Save_Format}"
    if(Saving_Q):
        All_z_pT_Canvas.SaveAs(Save_Name)
        print(f"{color.BOLD}Saved: {color.BBLUE}{Save_Name}{color.END}")
    else:
        print(f"{color.Error}Would be Saving: {color.BCYAN}{Save_Name}{color.END}")
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################ ################################################################ #####################
    ##################################################################### ################################################################ ################################################################ ################################################################ #####################
    return All_z_pT_Canvas



from pathlib import Path

if(__name__ == "__main__"):
    timer = RuntimeTimer()
    print(f"{color.BBLUE}\nCode is ready to run.{color.END}")
    timer.start()

    # List your folders here
    folders = [
        Path("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/REAL_Data"),
        Path("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/GEN_MC"),
        Path("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/Matching_REC_MC")
        # Path("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/Matching_REC_MC/Link_to_Volatile_MC_Matching")
    ]
    
    all_root_files = {}
    
    verbose = args.verbose
    
    for folder in folders:
        # print(str(folder.name))
        array_name = "rdf" if("REAL_Data" in str(folder.name)) else "mdf" if(("Matching_REC_MC" in str(folder.name)) or ("Link_to_Volatile_MC_Matching" in str(folder.name))) else "gdf"
        all_root_files[array_name] = []
        if("REAL_Data" not in str(folder.name)):
            all_root_files[f"{array_name}_clasdis"] = []
        if(not folder.exists()):
            print(f"{color.Error}WARNING - Folder not found: {color.END_B}{folder}{color.END}")
            continue
        if(not folder.is_dir()):
            print(f"{color.Error}WARNING - Not a directory: {color.END_B}{folder}{color.END}")
            continue
    
        # Gather only files at the top level of this folder
        root_files = [p for p in folder.iterdir() if((p.is_file()) and (".root" in str(p.name)))]
        if(verbose):
            print(f"\n{color.BOLD}Files in {color.BLUE}{folder}{color.END_B}:{color.END}")
        for num, f in enumerate(root_files):
            if(verbose):
                print(f"\t{num+1:>5.0f}:   {color.CYAN}{f.name}{color.END}")
            if("EvGen" in str(f.name)):
                all_root_files[array_name].append(f"{str(folder.name)}/{f.name}")
            elif("REAL" in str(folder.name)):
                if(len(all_root_files[array_name]) < args.num_rdf_files):
                    all_root_files[array_name].append(f"{str(folder.name)}/{f.name}")
            else:
                if(len(all_root_files[f"{array_name}_clasdis"]) < args.num_MC_files):
                    if((array_name in ["mdf"]) and (f"{str(folder.name).replace('Matching_REC_MC', 'GEN_MC')}/{str(f.name).replace('DataFrame_SIDIS_epip_MC_Matched', 'DataFrame_SIDIS_epip_MC_GEN')}" not in all_root_files["gdf_clasdis"])):
                    # if((array_name in ["mdf"]) and (f"{str(folder.name).replace('Link_to_Volatile_MC_Matching', 'GEN_MC')}/{str(f.name).replace('DataFrame_SIDIS_epip_MC_Matched', 'DataFrame_SIDIS_epip_MC_GEN')}" not in all_root_files["gdf_clasdis"])):
                        continue
                    all_root_files[f"{array_name}_clasdis"].append(f"{str(folder.name)}/{f.name}")
    
    print(f"\n\n{color.BOLD}Will Run With:{color.END}\n")
    for ii in all_root_files:
        print(f"\n\t{color.BLUE}{ii}:{color.END}")
        for jj in all_root_files[ii]:
            print(f"\t\t{jj}")
    
    print(f"\n{color.BOLD}LOADING DATAFRAMES{color.END}")
    
    rdf         = ROOT.RDataFrame("h22", all_root_files["rdf"])
    mdf_EvGen   = ROOT.RDataFrame("h22", all_root_files["mdf"])
    gdf_EvGen   = ROOT.RDataFrame("h22", all_root_files["gdf"])
    mdf_clasdis = ROOT.RDataFrame("h22", all_root_files["mdf_clasdis"])
    gdf_clasdis = ROOT.RDataFrame("h22", all_root_files["gdf_clasdis"])
    # rdf         = rdf.Range(5000)
    # mdf_EvGen   = mdf_EvGen.Range(5000)
    # gdf_EvGen   = gdf_EvGen.Range(5000)
    # mdf_clasdis = mdf_clasdis.Range(5000)
    # gdf_clasdis = gdf_clasdis.Range(5000)
    # rdf         = rdf.Range(500)
    # mdf_EvGen   = mdf_EvGen.Range(500)
    # gdf_EvGen   = gdf_EvGen.Range(500)
    # mdf_clasdis = mdf_clasdis.Range(500)
    # gdf_clasdis = gdf_clasdis.Range(500)
    
    print(f"\n{color.BBLUE}rdf{color.END}:")
    if(verbose or (not True)):
        for ii in range(0, len(rdf.GetColumnNames()), 1):
            print(f"\t{str((rdf.GetColumnNames())[ii]).ljust(38)} (type -> {rdf.GetColumnType(rdf.GetColumnNames()[ii])})")
    print(f"\tTotal entries in {color.BBLUE}rdf{color.END} files: \n{rdf.Count().GetValue():>20.0f}")
    
    print(f"\n{color.Error}mdf_clasdis{color.END}:")
    if(verbose or (not True)):
        for ii in range(0, len(mdf_clasdis.GetColumnNames()), 1):
            print(f"\t{str((mdf_clasdis.GetColumnNames())[ii]).ljust(38)} (type -> {mdf_clasdis.GetColumnType(mdf_clasdis.GetColumnNames()[ii])})")
    print(f"\tTotal entries in {color.Error}mdf_clasdis{color.END} files: \n{mdf_clasdis.Count().GetValue():>20.0f}")
    
    print(f"\n{color.BOLD}{color.PINK}mdf_EvGen{color.END}:")
    if(verbose or (not True)):
        for ii in range(0, len(mdf_EvGen.GetColumnNames()), 1):
            print(f"\t{str((mdf_EvGen.GetColumnNames())[ii]).ljust(38)} (type -> {mdf_EvGen.GetColumnType(mdf_EvGen.GetColumnNames()[ii])})")
    print(f"\tTotal entries in {color.BOLD}{color.PINK}mdf_EvGen{color.END} files: \n{mdf_EvGen.Count().GetValue():>20.0f}")
    
    print(f"\n{color.BGREEN}gdf_clasdis{color.END}:")
    if(verbose or (not True)):
        for ii in range(0, len(gdf_clasdis.GetColumnNames()), 1):
            print(f"\t{str((gdf_clasdis.GetColumnNames())[ii]).ljust(38)} (type -> {gdf_clasdis.GetColumnType(gdf_clasdis.GetColumnNames()[ii])})")
    print(f"\tTotal entries in {color.BGREEN}gdf_clasdis{color.END} files: \n{gdf_clasdis.Count().GetValue():>20.0f}")
    
    print(f"\n{color.BCYAN}gdf_EvGen{color.END}:")
    if(verbose or (not True)):
        for ii in range(0, len(gdf_EvGen.GetColumnNames()), 1):
            print(f"\t{str((gdf_EvGen.GetColumnNames())[ii]).ljust(38)} (type -> {gdf_EvGen.GetColumnType(gdf_EvGen.GetColumnNames()[ii])})")
    print(f"\tTotal entries in {color.BCYAN}gdf_EvGen{color.END} files: \n{gdf_EvGen.Count().GetValue():>20.0f}")
    
    print(f"\n{color.BOLD}DATAFRAMES LOADED\n{color.END}")
    timer.time_elapsed()
    print(f"\n{color.BOLD}APPLYING (BASE) CUTS\n{color.END}")
    if(verbose):
        print(f"""{color.BOLD}(Base) Cuts Include:{color.END_b}
clasdis Generation Cuts:{color.END}
mdf = mdf.Filter("((Q2_gen > 0.85) && (Q2_gen < 20.0)) && ((xB_gen > 0.05) && (xB_gen < 0.95)) && ((y_gen > 0.05) && (y_gen < 0.95)) && ((z_gen > 0.01) && (z_gen < 0.95)) && (((W_gen*W_gen) > 4.0) && ((W_gen*W_gen) < 50.0))")
gdf = gdf.Filter("((Q2     > 0.85) && (Q2     < 20.0)) && ((xB     > 0.05) && (xB     < 0.95)) && ((y     > 0.05) && (y     < 0.95)) && ((z     > 0.01) && (z     < 0.95)) && (((W    *    W) > 4.0) && ((W    *    W) < 50.0))")
{color.RED}clasdis Generation Cuts (y ended at 0.93 apparently?):{color.END}
mdf = mdf.Filter("((y_gen > 0.05) && (y_gen < 0.93))")
gdf = gdf.Filter("((y     > 0.05) && (y     < 0.93))")
{color.CYAN}EvGen Generation Cuts (OLD):{color.END}
mdf = mdf.Filter("((z_gen > 0.15) && (z_gen < 0.90))")
gdf = gdf.Filter("((z     > 0.15) && (z     < 0.90))")
{color.BOLD}Normal Analysis Cuts (See DF_Filter_Function_Full Function){color.END}\n\n""")
    
    # clasdis Generation Cuts
    mdf_EvGen   =   mdf_EvGen.Filter("((Q2_gen > 0.85) && (Q2_gen < 20.0)) && ((xB_gen > 0.05) && (xB_gen < 0.95)) && ((y_gen > 0.05) && (y_gen < 0.95)) && ((z_gen > 0.01) && (z_gen < 0.95)) && (((W_gen*W_gen) > 4.0) && ((W_gen*W_gen) < 50.0))")
    gdf_EvGen   =   gdf_EvGen.Filter("((Q2     > 0.85) && (Q2     < 20.0)) && ((xB     > 0.05) && (xB     < 0.95)) && ((y     > 0.05) && (y     < 0.95)) && ((z     > 0.01) && (z     < 0.95)) && (((W    *    W) > 4.0) && ((W    *    W) < 50.0))")
    mdf_clasdis = mdf_clasdis.Filter("((Q2_gen > 0.85) && (Q2_gen < 20.0)) && ((xB_gen > 0.05) && (xB_gen < 0.95)) && ((y_gen > 0.05) && (y_gen < 0.95)) && ((z_gen > 0.01) && (z_gen < 0.95)) && (((W_gen*W_gen) > 4.0) && ((W_gen*W_gen) < 50.0))")
    gdf_clasdis = gdf_clasdis.Filter("((Q2     > 0.85) && (Q2     < 20.0)) && ((xB     > 0.05) && (xB     < 0.95)) && ((y     > 0.05) && (y     < 0.95)) && ((z     > 0.01) && (z     < 0.95)) && (((W    *    W) > 4.0) && ((W    *    W) < 50.0))")
    
    # clasdis Generation Cuts (y ended at 0.93 apparently?)
    mdf_EvGen   =   mdf_EvGen.Filter("((y_gen > 0.05) && (y_gen < 0.93))")
    gdf_EvGen   =   gdf_EvGen.Filter("((y     > 0.05) && (y     < 0.93))")
    mdf_clasdis = mdf_clasdis.Filter("((y_gen > 0.05) && (y_gen < 0.93))")
    gdf_clasdis = gdf_clasdis.Filter("((y     > 0.05) && (y     < 0.93))")
    
    # EvGen Generation Cuts (OLD)
    mdf_EvGen   =   mdf_EvGen.Filter("((z_gen > 0.15) && (z_gen < 0.90))")
    gdf_EvGen   =   gdf_EvGen.Filter("((z     > 0.15) && (z     < 0.90))")
    mdf_clasdis = mdf_clasdis.Filter("((z_gen > 0.15) && (z_gen < 0.90))")
    gdf_clasdis = gdf_clasdis.Filter("((z     > 0.15) && (z     < 0.90))")
    
    
    # Normal Analysis Cuts
    rdf         = DF_Filter_Function_Full(DF_Out=rdf,         Titles_or_DF="DF", Data_Type="rdf", Cut_Choice="cut_Complete_SIDIS", Smearing_Q="")
    mdf_EvGen   = DF_Filter_Function_Full(DF_Out=mdf_EvGen,   Titles_or_DF="DF", Data_Type="mdf", Cut_Choice="cut_Complete_SIDIS", Smearing_Q="")
    mdf_clasdis = DF_Filter_Function_Full(DF_Out=mdf_clasdis, Titles_or_DF="DF", Data_Type="mdf", Cut_Choice="cut_Complete_SIDIS", Smearing_Q="smear")

    if(args.cut):
        print(f"{color.Error}Applying User Cut: {color.END_B}{args.cut}{color.END}")
        rdf         =         rdf.Filter(args.cut)
        mdf_EvGen   =   mdf_EvGen.Filter(args.cut)
        gdf_EvGen   =   gdf_EvGen.Filter(args.cut)
        mdf_clasdis = mdf_clasdis.Filter(args.cut)
        gdf_clasdis = gdf_clasdis.Filter(args.cut)
    
    print(f"\t(New) Total entries in {color.BBLUE}rdf        {color.END} files: \n{rdf.Count().GetValue():>20.0f}")
    print(f"\t(New) Total entries in {color.Error}mdf_clasdis{color.END} files: \n{mdf_clasdis.Count().GetValue():>20.0f}")
    print(f"\t(New) Total entries in {color.BOLD}{color.PINK}mdf_EvGen  {color.END} files: \n{mdf_EvGen.Count().GetValue():>20.0f}")
    print(f"\t(New) Total entries in {color.BGREEN}gdf_clasdis{color.END} files: \n{gdf_clasdis.Count().GetValue():>20.0f}")
    print(f"\t(New) Total entries in {color.BCYAN}gdf_EvGen  {color.END} files: \n{gdf_EvGen.Count().GetValue():>20.0f}")
    timer.time_elapsed()


    if(args.kinematic_compare):
        if(args.use_HIGH_MX):
            print(f"\n{color.BOLD}CREATING 1D MM HISTOGRAMS FOR HIGH-Mx NORMALIZATION FACTOR\n{color.END}")
            MM_Binning = ['MM', 2.5, 4.2, 60]
            histos = {}
            var, Min_range, Max_range, Num_of_Bins = MM_Binning
            rdf_name = f"{var}_rdf"
            mclasdis = f"{var}_mdf_clasdis"
            mdfEvGen = f"{var}_mdf_EvGen"
            gclasdis = f"{var}_gdf_clasdis"
            gdfEvGen = f"{var}_gdf_EvGen"
            Title = f"{variable_Title_name_new(var)} from SOURCE; {variable_Title_name_new(var)}"
            if(args.title):
                Title = f"#splitline{{{variable_Title_name_new(var)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var)}"
            histos[rdf_name] =         rdf.Histo1D((rdf_name, Title.replace("SOURCE", f"#color[{ROOT.kBlue   }]{{Experimental Data}}"),         Num_of_Bins, Min_range, Max_range),    var)
            histos[mclasdis] = mdf_clasdis.Histo1D((mclasdis, Title.replace("SOURCE", f"#color[{ROOT.kRed    }]{{Smeared MC REC (clasdis)}}"),  Num_of_Bins, Min_range, Max_range), f"{var}_smeared")
            histos[mdfEvGen] =   mdf_EvGen.Histo1D((mdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kMagenta}]{{MC REC (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var)
            histos[gclasdis] = gdf_clasdis.Histo1D((gclasdis, Title.replace("SOURCE", f"#color[{ROOT.kGreen  }]{{MC GEN (clasdis)}}"),          Num_of_Bins, Min_range, Max_range),    var)
            histos[gdfEvGen] =   gdf_EvGen.Histo1D((gdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kCyan   }]{{MC GEN (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var)
            histos[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var)} (Smeared)")
            histos[rdf_name].SetLineColor(ROOT.kBlue)
            histos[mclasdis].SetLineColor(ROOT.kRed)
            histos[mdfEvGen].SetLineColor(ROOT.kMagenta)
            histos[gclasdis].SetLineColor(ROOT.kGreen)
            histos[gdfEvGen].SetLineColor(ROOT.kCyan)
            rdf_name_norm_factor_HIGH_MX = histos[rdf_name].Integral()
            mclasdis_norm_factor_HIGH_MX = histos[mclasdis].Integral()
            mdfEvGen_norm_factor_HIGH_MX = histos[mdfEvGen].Integral()
            gclasdis_norm_factor_HIGH_MX = histos[gclasdis].Integral()
            gdfEvGen_norm_factor_HIGH_MX = histos[gdfEvGen].Integral()
            if(verbose):
                print(f"rdf_name_norm_factor_HIGH_MX = {rdf_name_norm_factor_HIGH_MX:>20.0f}")
                print(f"mclasdis_norm_factor_HIGH_MX = {mclasdis_norm_factor_HIGH_MX:>20.0f}")
                print(f"mdfEvGen_norm_factor_HIGH_MX = {mdfEvGen_norm_factor_HIGH_MX:>20.0f}")
                print(f"gclasdis_norm_factor_HIGH_MX = {gclasdis_norm_factor_HIGH_MX:>20.0f}")
                print(f"gdfEvGen_norm_factor_HIGH_MX = {gdfEvGen_norm_factor_HIGH_MX:>20.0f}")
            histos[f"norm_{rdf_name}"] = histos[rdf_name].Clone(f"norm_{rdf_name}")
            histos[f"norm_{mclasdis}"] = histos[mclasdis].Clone(f"norm_{mclasdis}")
            histos[f"norm_{mdfEvGen}"] = histos[mdfEvGen].Clone(f"norm_{mdfEvGen}")
            histos[f"norm_{gclasdis}"] = histos[gclasdis].Clone(f"norm_{gclasdis}")
            histos[f"norm_{gdfEvGen}"] = histos[gdfEvGen].Clone(f"norm_{gdfEvGen}")
            
            histos[f"norm_{rdf_name}"].Scale((1/rdf_name_norm_factor_HIGH_MX) if(rdf_name_norm_factor_HIGH_MX != 0) else 1)
            histos[f"norm_{mclasdis}"].Scale((1/mclasdis_norm_factor_HIGH_MX) if(mclasdis_norm_factor_HIGH_MX != 0) else 1)
            histos[f"norm_{mdfEvGen}"].Scale((1/mdfEvGen_norm_factor_HIGH_MX) if(mdfEvGen_norm_factor_HIGH_MX != 0) else 1)
            histos[f"norm_{gclasdis}"].Scale((1/gclasdis_norm_factor_HIGH_MX) if(gclasdis_norm_factor_HIGH_MX != 0) else 1)
            histos[f"norm_{gdfEvGen}"].Scale((1/gdfEvGen_norm_factor_HIGH_MX) if(gdfEvGen_norm_factor_HIGH_MX != 0) else 1)
            
            histos[f"norm_{rdf_name}"].SetTitle(f"Normalized {histos[rdf_name].GetTitle()}")
            histos[f"norm_{mclasdis}"].SetTitle(f"Normalized {histos[mclasdis].GetTitle()}")
            histos[f"norm_{mdfEvGen}"].SetTitle(f"Normalized {histos[mdfEvGen].GetTitle()}")
            histos[f"norm_{gclasdis}"].SetTitle(f"Normalized {histos[gclasdis].GetTitle()}")
            histos[f"norm_{gdfEvGen}"].SetTitle(f"Normalized {histos[gdfEvGen].GetTitle()}")
            
            histos[f"norm_{rdf_name}"].GetYaxis().SetTitle("Normalized")
            histos[f"norm_{mclasdis}"].GetYaxis().SetTitle("Normalized")
            histos[f"norm_{mdfEvGen}"].GetYaxis().SetTitle("Normalized")
            histos[f"norm_{gclasdis}"].GetYaxis().SetTitle("Normalized")
            histos[f"norm_{gdfEvGen}"].GetYaxis().SetTitle("Normalized")
            
            canvas = ROOT.TCanvas("MM_Norm_Factor", "My Canvas", int(912*1.55), int(547*1.55))
            canvas.Divide(6, 2)
            
            for cd_num, ii in enumerate([rdf_name, mclasdis, mdfEvGen, gclasdis, gdfEvGen]):
                canvas.cd(cd_num + 1)
                histos[ii].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(histos[ii]))
                histos[ii].Draw("E0 hist same")
                canvas.cd(cd_num + 7)
                histos[f"norm_{ii}"].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(histos[f"norm_{ii}"]))
                histos[f"norm_{ii}"].Draw("E0 hist same")
            
            # Draw Legend(s)
            canvas.cd(6)
            ROOT.gPad.Clear()
            ROOT.gPad.SetLeftMargin(0.2)
            ROOT.gPad.SetBottomMargin(0.2)
            
            group_info = [(ROOT.kBlue,    "Experimental Data"),
                          (ROOT.kRed,     "MC REC - clasdis"),
                          (ROOT.kGreen,   "MC GEN - clasdis"),
                          (ROOT.kMagenta, "MC REC - EvGen"),
                          (ROOT.kCyan,    "MC GEN - EvGen"),
                         ]
            y = 0.8
            for color_ii, label in group_info:
                line = ROOT.TLine()
                line.SetLineWidth(2)
                line.SetLineColor(color_ii)
                line.DrawLineNDC(0.1, y, 0.2, y)
                text = ROOT.TLatex()
                text.SetNDC()
                text.SetTextColor(color_ii)
                text.SetTextSize(0.1)
                text.SetTextFont(42)
                text.DrawLatex(0.22, y-0.01, label)
                y -= 0.1  # move down for next entry

            save_name = f"MM_Norm_Factor{args.File_Save_Format}" if(not args.name) else f"MM_Norm_Factor_{args.name}{args.File_Save_Format}"
            canvas.SaveAs(save_name)
            print(f"{color.BOLD}Saved: {color.BBLUE}{save_name}{color.END}")
            print(f"{color.BOLD}DONE CREATING 1D MM HISTOGRAMS FOR HIGH-Mx NORMALIZATION FACTOR{color.END}")
            timer.time_elapsed()
        else:
            print(f"{color.RED}NOT USING HIGH-Mx NORMALIZATION FACTOR{color.END}")
        print(f"\n{color.BOLD}CREATING 1D HISTOGRAMS/PLOTS\n{color.END}")
        phi_t_Binning              = ['phi_t',                            0,      360,    24]
        El_Binning                 = ['el',                               0,        8,   200]
        El_Th_Binning              = ['elth',                             0,       40,   200]
        El_Phi_Binning             = ['elPhi',                            0,      360,   200]
        Pip_Binning                = ['pip',                              0,        6,   200]
        Pip_Th_Binning             = ['pipth',                            0,       40,   200]
        Pip_Phi_Binning            = ['pipPhi',                           0,      360,   200]
        Q2_Binning                 = ['Q2',                               0,       14,   280]
        y_Binning                  = ['y',                                0,        1,   100]
        # y_Binning                  = ['y',                              0.9,        1,   100]
        xB_Binning                 = ['xB',                            0.09,    0.826,    50]
        z_Binning                  = ['z',                                0,     1.20,   120]
        # z_Binning                  = ['z',                                0,     0.20,   120]
        # pT_Binning                 = ['pT',                               0,     2.00,   200]
        pT_Binning                 = ['pT',                               0,     1.50,   150]
        MM_Binning                 = ['MM',                               0,      4.2,    60]
        W_Binning                  = ['W',                              0.9,      5.1,    14]
        Q2_y_z_pT_Binning          = ['Q2_y_z_pT_4D_Bin',              -0.5,    506.5,   507]
        z_pT_phi_h_Binning         = ['MultiDim_z_pT_Bin_Y_bin_phi_t', -1.5,    913.5,   915]
        Q2_y_z_pT_phi_h_5D_Binning = ['MultiDim_Q2_y_z_pT_phi_h',      -0.5,  11815.5, 11816]
        Hx_Binning                 = ['Hx',                            -400,      400,   800]
        Hy_Binning                 = ['Hy',                            -400,      400,   800]
        z_pT_Bin_Y_Binning         = ['z_pT_Bin_Y_bin',                -2.5,     41.5,    44]
        
        List_of_Quantities_1D = []
        List_of_Quantities_1D.append(MM_Binning)
        List_of_Quantities_1D.append(W_Binning)
        List_of_Quantities_1D.append(Q2_Binning)
        List_of_Quantities_1D.append(y_Binning)
        List_of_Quantities_1D.append(xB_Binning)
        List_of_Quantities_1D.append(z_Binning)
        List_of_Quantities_1D.append(pT_Binning)
        List_of_Quantities_1D.append(phi_t_Binning)
        List_of_Quantities_1D.append(El_Binning)
        List_of_Quantities_1D.append(El_Th_Binning)
        List_of_Quantities_1D.append(El_Phi_Binning)
        List_of_Quantities_1D.append(Pip_Binning)
        List_of_Quantities_1D.append(Pip_Th_Binning)
        List_of_Quantities_1D.append(Pip_Phi_Binning)
        # List_of_Quantities_1D.append(z_pT_Bin_Y_Binning)
        
        histos_compare, canvas_compare = {}, {}
        
        for num, (var, Min_range, Max_range, Num_of_Bins) in enumerate(List_of_Quantities_1D):
            rdf_name = f"{var}_rdf"
            mclasdis = f"{var}_mdf_clasdis"
            mdfEvGen = f"{var}_mdf_EvGen"
            gclasdis = f"{var}_gdf_clasdis"
            gdfEvGen = f"{var}_gdf_EvGen"
        
            Title = f"Plot of {variable_Title_name_new(var)} from SOURCE; {variable_Title_name_new(var)}"
            if(args.title):
                Title = f"#splitline{{Plot of {variable_Title_name_new(var)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var)}"
            histos_compare[rdf_name] =         rdf.Histo1D((rdf_name, Title.replace("SOURCE", f"#color[{ROOT.kBlue   }]{{Experimental Data}}"),         Num_of_Bins, Min_range, Max_range),    var)
            histos_compare[mclasdis] = mdf_clasdis.Histo1D((mclasdis, Title.replace("SOURCE", f"#color[{ROOT.kRed    }]{{Smeared MC REC (clasdis)}}"),  Num_of_Bins, Min_range, Max_range), f"{var}_smeared")
            histos_compare[mdfEvGen] =   mdf_EvGen.Histo1D((mdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kMagenta}]{{MC REC (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var)
            histos_compare[gclasdis] = gdf_clasdis.Histo1D((gclasdis, Title.replace("SOURCE", f"#color[{ROOT.kGreen  }]{{MC GEN (clasdis)}}"),          Num_of_Bins, Min_range, Max_range),    var)
            histos_compare[gdfEvGen] =   gdf_EvGen.Histo1D((gdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kCyan   }]{{MC GEN (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var)
            histos_compare[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var)} (Smeared)")
            
            histos_compare[rdf_name].SetLineColor(ROOT.kBlue)
            histos_compare[mclasdis].SetLineColor(ROOT.kRed)
            histos_compare[mdfEvGen].SetLineColor(ROOT.kMagenta)
            histos_compare[gclasdis].SetLineColor(ROOT.kGreen)
            histos_compare[gdfEvGen].SetLineColor(ROOT.kCyan)
        
            rdf_name_norm_factor = rdf_name_norm_factor_HIGH_MX if(args.use_HIGH_MX) else histos_compare[rdf_name].Integral()
            mclasdis_norm_factor = mclasdis_norm_factor_HIGH_MX if(args.use_HIGH_MX) else histos_compare[mclasdis].Integral()
            mdfEvGen_norm_factor = mdfEvGen_norm_factor_HIGH_MX if(args.use_HIGH_MX) else histos_compare[mdfEvGen].Integral()
            gclasdis_norm_factor = gclasdis_norm_factor_HIGH_MX if(args.use_HIGH_MX) else histos_compare[gclasdis].Integral()
            gdfEvGen_norm_factor = gdfEvGen_norm_factor_HIGH_MX if(args.use_HIGH_MX) else histos_compare[gdfEvGen].Integral()
        
        
            histos_compare[f"norm_{rdf_name}"] = histos_compare[rdf_name].Clone(f"norm_{rdf_name}")
            histos_compare[f"norm_{mclasdis}"] = histos_compare[mclasdis].Clone(f"norm_{mclasdis}")
            histos_compare[f"norm_{mdfEvGen}"] = histos_compare[mdfEvGen].Clone(f"norm_{mdfEvGen}")
            histos_compare[f"norm_{gclasdis}"] = histos_compare[gclasdis].Clone(f"norm_{gclasdis}")
            histos_compare[f"norm_{gdfEvGen}"] = histos_compare[gdfEvGen].Clone(f"norm_{gdfEvGen}")
        
            histos_compare[f"norm_{rdf_name}"].Scale((1/rdf_name_norm_factor) if(rdf_name_norm_factor != 0) else 1)
            histos_compare[f"norm_{mclasdis}"].Scale((1/mclasdis_norm_factor) if(mclasdis_norm_factor != 0) else 1)
            histos_compare[f"norm_{mdfEvGen}"].Scale((1/mdfEvGen_norm_factor) if(mdfEvGen_norm_factor != 0) else 1)
            histos_compare[f"norm_{gclasdis}"].Scale((1/gclasdis_norm_factor) if(gclasdis_norm_factor != 0) else 1)
            histos_compare[f"norm_{gdfEvGen}"].Scale((1/gdfEvGen_norm_factor) if(gdfEvGen_norm_factor != 0) else 1)
            
            canvas_compare[var] = ROOT.TCanvas(f"compare_{var}", "My Canvas", int(912*1.55), int(547*1.55))
            canvas_compare[var].Divide(5, 2)
        
            max_cd_1     = max([find_max_bin(histos_compare[f"norm_{mdfEvGen}"]), find_max_bin(histos_compare[f"norm_{mclasdis}"])])
            max_cd_3     = max([find_max_bin(histos_compare[f"norm_{mdfEvGen}"]), find_max_bin(histos_compare[f"norm_{rdf_name}"])])
            max_cd_4     = max([find_max_bin(histos_compare[f"norm_{mclasdis}"]), find_max_bin(histos_compare[f"norm_{rdf_name}"])])
            max_cd_1_3_4 = max([max_cd_1, max_cd_3, max_cd_4])
        
            canvas_compare[var].cd(1)
            mdf_title = f"Comparison of REC MC's for {variable_Title_name_new(var)}"
            if(args.title):
                mdf_title = f"#splitline{{{mdf_title}}}{{{args.title}}}"
            mdf_title = f"#scale[2]{{{mdf_title}}}"
            histos_compare[f"norm_{mdfEvGen}"].SetTitle(mdf_title)
            histos_compare[f"norm_{mdfEvGen}"].GetYaxis().SetRangeUser(0, 1.2*max_cd_1_3_4)
            histos_compare[f"norm_{mdfEvGen}"].Draw("E0 hist same")
            histos_compare[f"norm_{mclasdis}"].Draw("E0 hist same")
        
            canvas_compare[var].cd(6)
            histos_compare[f"Diff_in_{mdfEvGen}"] = histos_compare[f"norm_{mdfEvGen}"].Clone(f"Diff_in_{mdfEvGen}")
            histos_compare[f"Diff_in_{mdfEvGen}"].Divide(histos_compare[f"norm_{mclasdis}"])
            histos_compare[f"Diff_in_{mdfEvGen}"].SetTitle("#scale[2]{Ratio of REC MC's above}")
            histos_compare[f"Diff_in_{mdfEvGen}"].GetYaxis().SetTitle("#frac{EvGen}{clasdis}")
            histos_compare[f"Diff_in_{mdfEvGen}"].SetLineColor(ROOT.kPink - 7)
            histos_compare[f"Diff_in_{mdfEvGen}"].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(histos_compare[f"Diff_in_{mdfEvGen}"]))
            histos_compare[f"Diff_in_{mdfEvGen}"].Draw("E0 hist same")
            xmin = histos_compare[f"Diff_in_{mdfEvGen}"].GetXaxis().GetXmin()
            xmax = histos_compare[f"Diff_in_{mdfEvGen}"].GetXaxis().GetXmax()
            histos_compare[f"line_{mdfEvGen}"] = ROOT.TLine(xmin, 1.0, xmax, 1.0)
            histos_compare[f"line_{mdfEvGen}"].SetLineColor(ROOT.kGray + 3)
            histos_compare[f"line_{mdfEvGen}"].SetLineWidth(2)
            histos_compare[f"line_{mdfEvGen}"].SetLineStyle(2)
            histos_compare[f"line_{mdfEvGen}"].Draw("same")
            
            canvas_compare[var].cd(2)
            gdf_title = f"Comparison of GEN MC's for {variable_Title_name_new(var)}"
            if(args.title):
                gdf_title = f"#splitline{{{gdf_title}}}{{{args.title}}}"
            gdf_title = f"#scale[2]{{{gdf_title}}}"
            histos_compare[f"norm_{gdfEvGen}"].SetTitle(gdf_title)
            max_cd_2 = max([find_max_bin(histos_compare[f"norm_{gdfEvGen}"]), find_max_bin(histos_compare[f"norm_{gclasdis}"])])
            histos_compare[f"norm_{gdfEvGen}"].GetYaxis().SetRangeUser(0, 1.2*max_cd_2)
            histos_compare[f"norm_{gdfEvGen}"].Draw("E0 hist same")
            histos_compare[f"norm_{gclasdis}"].Draw("E0 hist same")
        
            canvas_compare[var].cd(7)
            histos_compare[f"Diff_in_{gdfEvGen}"] = histos_compare[f"norm_{gdfEvGen}"].Clone(f"Diff_in_{gdfEvGen}")
            histos_compare[f"Diff_in_{gdfEvGen}"].Divide(histos_compare[f"norm_{gclasdis}"])
            histos_compare[f"Diff_in_{gdfEvGen}"].SetTitle("#scale[2]{Ratio of GEN MC's above}")
            histos_compare[f"Diff_in_{gdfEvGen}"].GetYaxis().SetTitle("#frac{EvGen}{clasdis}")
            histos_compare[f"Diff_in_{gdfEvGen}"].SetLineColor(ROOT.kSpring + 9)
            histos_compare[f"Diff_in_{gdfEvGen}"].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(histos_compare[f"Diff_in_{gdfEvGen}"]))
            histos_compare[f"Diff_in_{gdfEvGen}"].Draw("E0 hist same")
            histos_compare[f"line_{mdfEvGen}"].Draw("same")
        
            canvas_compare[var].cd(3)
            rdf_title_EvGen = f"#splitline{{Comparison of}}{{Data to EvGen MC for {variable_Title_name_new(var)}}}"
            if(args.title):
                rdf_title_EvGen = f"#splitline{{{rdf_title_EvGen}}}{{{args.title}}}"
            rdf_title_EvGen = f"#scale[2]{{{rdf_title_EvGen}}}"
            histos_compare[f"norm_{rdf_name}"].SetTitle(rdf_title_EvGen)
            histos_compare[f"norm_{rdf_name}"].GetYaxis().SetRangeUser(0, 1.2*max_cd_1_3_4)
            histos_compare[f"norm_{rdf_name}"].Draw("E0 hist same")
            histos_compare[f"norm_{mdfEvGen}"].Draw("E0 hist same")
        
            canvas_compare[var].cd(4)
            rdf_title_clasdis = f"#splitline{{Comparison of}}{{Data to clasdis MC for {variable_Title_name_new(var)}}}"
            if(args.title):
                rdf_title_clasdis = f"#splitline{{{rdf_title_clasdis}}}{{{args.title}}}"
            rdf_title_clasdis = f"#scale[2]{{{rdf_title_clasdis}}}"
            histos_compare[f"norm_{mclasdis}"].SetTitle(rdf_title_clasdis)
            histos_compare[f"norm_{mclasdis}"].GetYaxis().SetRangeUser(0, 1.2*max_cd_1_3_4)
            histos_compare[f"norm_{mclasdis}"].Draw("E0 hist same")
            histos_compare[f"norm_{rdf_name}"].Draw("E0 hist same")
        
            # canvas_compare[var].cd(8)
            histos_compare[f"Diff_in_{rdf_name}"] = histos_compare[f"norm_{rdf_name}"].Clone(f"Diff_in_{rdf_name}")
            histos_compare[f"Diff_in_{rdf_name}"].Divide(histos_compare[f"norm_{mdfEvGen}"])
            histos_compare[f"Diff_in_{rdf_name}"].SetTitle("#scale[2]{Ratio of Data to EvGen MC above}")
            histos_compare[f"Diff_in_{rdf_name}"].GetYaxis().SetTitle("#frac{Data}{EvGen}")
            histos_compare[f"Diff_in_{rdf_name}"].SetLineColor(ROOT.kViolet + 1)
            # canvas_compare[var].cd(9)
            histos_compare[f"Diff_in_{mclasdis}"] = histos_compare[f"norm_{rdf_name}"].Clone(f"Diff_in_{mclasdis}")
            histos_compare[f"Diff_in_{mclasdis}"].Divide(histos_compare[f"norm_{mclasdis}"])
            histos_compare[f"Diff_in_{mclasdis}"].SetTitle("#scale[2]{Ratio of Data to clasdis MC above}")
            histos_compare[f"Diff_in_{mclasdis}"].GetYaxis().SetTitle("#frac{Data}{clasdis}")
            histos_compare[f"Diff_in_{mclasdis}"].SetLineColor(ROOT.kBlue + 3)
            max_cd_8_9 = max([find_max_bin(histos_compare[f"Diff_in_{rdf_name}"]), find_max_bin(histos_compare[f"Diff_in_{mclasdis}"])])
            
            canvas_compare[var].cd(8)
            histos_compare[f"Diff_in_{rdf_name}"].GetYaxis().SetRangeUser(0, 1.2*max_cd_8_9)
            histos_compare[f"Diff_in_{rdf_name}"].Draw("E0 hist same")
            histos_compare[f"line_{mdfEvGen}"].Draw("same")
        
            canvas_compare[var].cd(9)
            histos_compare[f"Diff_in_{mclasdis}"].GetYaxis().SetRangeUser(0, 1.2*max_cd_8_9)
            histos_compare[f"Diff_in_{mclasdis}"].Draw("E0 hist same")
            histos_compare[f"line_{mdfEvGen}"].Draw("same")
            
            # Draw Legend(s)
            canvas_compare[var].cd(5)
            ROOT.gPad.Clear()
            ROOT.gPad.SetLeftMargin(0.2)
            ROOT.gPad.SetBottomMargin(0.2)
            
            group_info = [(ROOT.kBlue,    "Experimental Data"),
                          (ROOT.kRed,     "MC REC - clasdis"),
                          (ROOT.kGreen,   "MC GEN - clasdis"),
                          (ROOT.kMagenta, "MC REC - EvGen"),
                          (ROOT.kCyan,    "MC GEN - EvGen"),
                         ]
            y = 0.8
            for color_ii, label in group_info:
                line = ROOT.TLine()
                line.SetLineWidth(2)
                line.SetLineColor(color_ii)
                line.DrawLineNDC(0.1, y, 0.2, y)
                text = ROOT.TLatex()
                text.SetNDC()
                text.SetTextColor(color_ii)
                text.SetTextSize(0.1)
                text.SetTextFont(42)
                text.DrawLatex(0.22, y-0.01, label)
                y -= 0.1  # move down for next entry

            save_name = f"Kinematic_Comparison_of_{var}{args.File_Save_Format}" if(not args.name) else f"Kinematic_Comparison_of_{var}_{args.name}{args.File_Save_Format}"
            if(args.use_HIGH_MX):
                save_name = f"Kinematic_Comparison_of_{var}_High_Mx_Norm{args.File_Save_Format}" if(not args.name) else f"Kinematic_Comparison_of_{var}_High_Mx_Norm_{args.name}{args.File_Save_Format}"
            canvas_compare[var].SaveAs(save_name)
            print(f"{color.BOLD}Saved: {color.BBLUE}{save_name}{color.END}")
        print(f"\n{color.BOLD}DONE CREATING 1D HISTOGRAMS\n{color.END}")
        timer.time_elapsed()
    else:
        print(f"\n{color.Error}Skipping Kinematic Comparison Plots{color.END}")

    
    if(args.acceptance_all):
        print(f"\n{color.BOLD}CREATING 1D (UNBINNED) ACCEPTANCE HISTOGRAMS/PLOTS\n{color.END}")
        phi_t_Binning              = ['phi_t',                            0,      360,    24]
        El_Binning                 = ['el',                               0,        8,   200]
        El_Th_Binning              = ['elth',                             0,       40,   200]
        El_Phi_Binning             = ['elPhi',                            0,      360,   200]
        Pip_Binning                = ['pip',                              0,        6,   200]
        Pip_Th_Binning             = ['pipth',                            0,       40,   200]
        Pip_Phi_Binning            = ['pipPhi',                           0,      360,   200]
        Q2_Binning                 = ['Q2',                               0,       14,   280]
        y_Binning                  = ['y',                                0,        1,   100]
        xB_Binning                 = ['xB',                            0.09,    0.826,    50]
        z_Binning                  = ['z',                                0,     1.20,   120]
        # z_Binning                  = ['z',                                0,     0.20,   120]
        pT_Binning                 = ['pT',                               0,     2.00,   200]
        MM_Binning                 = ['MM',                               0,      4.2,    60]
        # W_Binning                  = ['W',                              0.9,      5.1,    14]
        W_Binning                  = ['W',                              0.9,      5.1,    56]
        Q2_y_z_pT_Binning          = ['Q2_y_z_pT_4D_Bin',              -0.5,    506.5,   507]
        z_pT_phi_h_Binning         = ['MultiDim_z_pT_Bin_Y_bin_phi_t', -1.5,    913.5,   915]
        Q2_y_z_pT_phi_h_5D_Binning = ['MultiDim_Q2_y_z_pT_phi_h',      -0.5,  11815.5, 11816]
        Hx_Binning                 = ['Hx',                            -400,      400,   800]
        Hy_Binning                 = ['Hy',                            -400,      400,   800]
        
        List_of_Quantities_1D = []
        List_of_Quantities_1D.append(MM_Binning)
        List_of_Quantities_1D.append(W_Binning)
        List_of_Quantities_1D.append(phi_t_Binning)
        List_of_Quantities_1D.append(Q2_Binning)
        List_of_Quantities_1D.append(y_Binning)
        List_of_Quantities_1D.append(xB_Binning)
        List_of_Quantities_1D.append(z_Binning)
        List_of_Quantities_1D.append(pT_Binning)
        List_of_Quantities_1D.append(El_Binning)
        List_of_Quantities_1D.append(El_Th_Binning)
        List_of_Quantities_1D.append(El_Phi_Binning)
        List_of_Quantities_1D.append(Pip_Binning)
        List_of_Quantities_1D.append(Pip_Th_Binning)
        List_of_Quantities_1D.append(Pip_Phi_Binning)
        
        histos_acceptance, canvas_acceptance = {}, {}
        
        for num, (var, Min_range, Max_range, Num_of_Bins) in enumerate(List_of_Quantities_1D):
            mclasdis = f"{var}_mdf_clasdis"
            mdfEvGen = f"{var}_mdf_EvGen"
            gclasdis = f"{var}_gdf_clasdis"
            gdfEvGen = f"{var}_gdf_EvGen"
        
            Title = f"Acceptance Plot of {variable_Title_name_new(var)} from SOURCE; {variable_Title_name_new(var)}"
            if(args.title):
                Title = f"#splitline{{Acceptance Plot of {variable_Title_name_new(var)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var)}"
            
            histos_acceptance[mclasdis] = mdf_clasdis.Histo1D((mclasdis, Title.replace("SOURCE", f"#color[{ROOT.kRed    }]{{Smeared MC REC (clasdis)}}"),  Num_of_Bins, Min_range, Max_range), f"{var}_smeared")
            histos_acceptance[mdfEvGen] =   mdf_EvGen.Histo1D((mdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kMagenta}]{{MC REC (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var)
            histos_acceptance[gclasdis] = gdf_clasdis.Histo1D((gclasdis, Title.replace("SOURCE", f"#color[{ROOT.kGreen  }]{{MC GEN (clasdis)}}"),          Num_of_Bins, Min_range, Max_range),    var)
            histos_acceptance[gdfEvGen] =   gdf_EvGen.Histo1D((gdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kCyan   }]{{MC GEN (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var)
            histos_acceptance[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var)} (Smeared)")
            
            histos_acceptance[mclasdis].SetLineColor(ROOT.kRed)
            histos_acceptance[mdfEvGen].SetLineColor(ROOT.kMagenta)
            histos_acceptance[gclasdis].SetLineColor(ROOT.kGreen)
            histos_acceptance[gdfEvGen].SetLineColor(ROOT.kCyan)
            
            canvas_acceptance[var] = ROOT.TCanvas(f"Acceptance_{var}", "My Canvas", int(912*1.55), int(547*1.55))
            canvas_acceptance[var].Divide(3, 1)
        
            histos_acceptance[mdfEvGen].Sumw2()
            histos_acceptance[gdfEvGen].Sumw2()
            histos_acceptance[mclasdis].Sumw2()
            histos_acceptance[gclasdis].Sumw2()
        
            canvas_acceptance[var].cd(1)
            histos_acceptance[f"Acceptance_{mdfEvGen}"] = histos_acceptance[mdfEvGen].Clone(f"Acceptance_{mdfEvGen}")
            histos_acceptance[f"Acceptance_{mdfEvGen}"].Divide(histos_acceptance[gdfEvGen].GetValue())
            title_cd_1 = f"#scale[2]{{Acceptance for {variable_Title_name_new(var)}}}"
            if(args.title):
                title_cd_1 = f"#splitline{{{title_cd_1}}}{{{args.title}}}"
            histos_acceptance[f"Acceptance_{mdfEvGen}"].SetTitle(title_cd_1)
            histos_acceptance[f"Acceptance_{mdfEvGen}"].GetYaxis().SetTitle("Acceptance")
            histos_acceptance[f"Acceptance_{mdfEvGen}"].SetLineColor(ROOT.kAzure)
        
            histos_acceptance[f"Acceptance_{mclasdis}"] = histos_acceptance[mclasdis].Clone(f"Acceptance_{mclasdis}")
            histos_acceptance[f"Acceptance_{mclasdis}"].Divide(histos_acceptance[gclasdis].GetValue())
            histos_acceptance[f"Acceptance_{mclasdis}"].SetTitle(title_cd_1)
            histos_acceptance[f"Acceptance_{mclasdis}"].GetYaxis().SetTitle("Acceptance")
            histos_acceptance[f"Acceptance_{mclasdis}"].SetLineColor(ROOT.kAzure + 10)
        
            cd_1_max = max([find_max_bin(histos_acceptance[f"Acceptance_{mdfEvGen}"]), find_max_bin(histos_acceptance[f"Acceptance_{mclasdis}"]), 0])
            
            histos_acceptance[f"Acceptance_{mdfEvGen}"].GetYaxis().SetRangeUser(0, 1.2*cd_1_max)
            histos_acceptance[f"Acceptance_{mclasdis}"].GetYaxis().SetRangeUser(0, 1.2*cd_1_max)
            
            histos_acceptance[f"Acceptance_{mdfEvGen}"].Draw("E0 hist same")
            histos_acceptance[f"Acceptance_{mclasdis}"].Draw("E0 hist same")
            xmin = histos_acceptance[f"Acceptance_{mdfEvGen}"].GetXaxis().GetXmin()
            xmax = histos_acceptance[f"Acceptance_{mdfEvGen}"].GetXaxis().GetXmax()
            histos_acceptance[f"line_{mdfEvGen}"] = ROOT.TLine(xmin, 1.0, xmax, 1.0)
            histos_acceptance[f"line_{mdfEvGen}"].SetLineColor(ROOT.kGray + 3)
            histos_acceptance[f"line_{mdfEvGen}"].SetLineWidth(2)
            histos_acceptance[f"line_{mdfEvGen}"].SetLineStyle(2)
            histos_acceptance[f"line_{mdfEvGen}"].Draw("same")
        
            canvas_acceptance[var].cd(2)
            ROOT.gPad.Clear()
            ROOT.gPad.SetLeftMargin(0.2)
            ROOT.gPad.SetBottomMargin(0.2)
            
            # map colors → group labels
            group_info = [(ROOT.kAzure,       "EvGen"),
                          (ROOT.kAzure + 10,  "clasdis"),]
            y = 0.8
            text = ROOT.TLatex()
            text.SetNDC()
            text.SetTextColor(ROOT.kBlack)
            text.SetTextSize(0.1)
            text.SetTextFont(42)
            text.DrawLatex(0.22, y-0.01, "Acceptance for:")
            y -= 0.1
            for color_ii, label in group_info:
                line = ROOT.TLine()
                line.SetLineWidth(2)
                line.SetLineColor(color_ii)
                line.DrawLineNDC(0.1, y, 0.2, y)
                text = ROOT.TLatex()
                text.SetNDC()
                text.SetTextColor(color_ii)
                text.SetTextSize(0.1)
                text.SetTextFont(42)
                text.DrawLatex(0.22, y-0.01, label)
                y -= 0.1  # move down for next entry
        
        
            canvas_acceptance[var].cd(3)    
            histos_acceptance[f"Comparison_of_Acceptance_{mdfEvGen}"] = histos_acceptance[f"Acceptance_{mdfEvGen}"].Clone(f"Comparison_of_Acceptance_{mdfEvGen}")
            histos_acceptance[f"Comparison_of_Acceptance_{mdfEvGen}"].Divide(histos_acceptance[f"Acceptance_{mclasdis}"])
            # histos_acceptance[f"Comparison_of_Acceptance_{mdfEvGen}"].Scale(100)
            title_cd_3 = f"Ratio of Acceptances for {variable_Title_name_new(var)}"
            if(args.title):
                title_cd_3 = f"#splitline{{{title_cd_3}}}{{{args.title}}}"
            histos_acceptance[f"Comparison_of_Acceptance_{mdfEvGen}"].SetTitle(title_cd_3)
            histos_acceptance[f"Comparison_of_Acceptance_{mdfEvGen}"].SetLineColor(ROOT.kBlack)
            histos_acceptance[f"Comparison_of_Acceptance_{mdfEvGen}"].GetYaxis().SetRangeUser(0, 1.2*max([find_max_bin(histos_acceptance[f"Comparison_of_Acceptance_{mdfEvGen}"]), 0]))
            histos_acceptance[f"Comparison_of_Acceptance_{mdfEvGen}"].Draw("E0 hist same")
            histos_acceptance[f"line_{mdfEvGen}"].Draw("same")
            
            save_name = f"Unbinned_Acceptance_Comparison_of_{var}{args.File_Save_Format}" if(not args.name) else f"Unbinned_Acceptance_Comparison_of_{var}_{args.name}{args.File_Save_Format}"
            canvas_acceptance[var].SaveAs(save_name)
            print(f"{color.BOLD}Saved: {color.BBLUE}{save_name}{color.END}")
            
        print(f"\n{color.BOLD}DONE CREATING 1D (UNBINNED) ACCEPTANCE HISTOGRAMS\n{color.END}")
        timer.time_elapsed()
    else:
        print(f"\n{color.Error}Skipping (Unbinned) Acceptance Comparison Plots{color.END}")
        
    
    if(args.acceptance):
        print(f"\n{color.BOLD}MAKING ACCEPTANCE AS FUNCTION OF phi_h FOR ALL KINEMATIC BINS\n{color.END}")
        phi_t_Binning = ['phi_t',  0,   360,    24]
        Q2_Binning    = ['Q2',     0,    14,   280]
        y_Binning     = ['y',      0,     1,   100]
        z_Binning     = ['z',      0,  1.20,   120]
        pT_Binning    = ['pT',     0,  1.50,   150]
        
        rdf_binned         =         rdf.Filter("(Q2_Y_Bin > 0) && (z_pT_Bin_Y_bin > 0)")
        mdf_clasdis_binned = mdf_clasdis.Filter("(Q2_Y_Bin > 0) && (z_pT_Bin_Y_bin > 0)")
        mdf_EvGen_binned   =   mdf_EvGen.Filter("(Q2_Y_Bin > 0) && (z_pT_Bin_Y_bin > 0)")
        gdf_clasdis_binned = gdf_clasdis.Filter("(Q2_Y_Bin > 0) && (z_pT_Bin_Y_bin > 0)")
        gdf_EvGen_binned   =   gdf_EvGen.Filter("(Q2_Y_Bin > 0) && (z_pT_Bin_Y_bin > 0)")
        
        Histogram_List_All, Acceptance_Canvases = {}, {}
        count = 0
        for     Q2_y_Bin in range(1, 18):
            Histogram_List_All[f"Q2-y Bin ({Q2_y_Bin}-All)"] = (rdf_binned.Filter(f"Q2_Y_Bin == {Q2_y_Bin}")).Histo2D((f"Q2-y Bin ({Q2_y_Bin}-All)", f"#splitline{{Q^{{2}} vs y for #color[{ROOT.kBlue}]{{Experimental Data}}}}{{#color[{ROOT.kRed}]{{Q^{{2}}-y Bin {Q2_y_Bin}}}}}; y; Q^{{2}}",    y_Binning[3],  y_Binning[1],  y_Binning[2], Q2_Binning[3], Q2_Binning[1], Q2_Binning[2]),  y_Binning[0], Q2_Binning[0])
            Histogram_List_All[f"z-pT Bin ({Q2_y_Bin}-All)"] = (rdf_binned.Filter(f"Q2_Y_Bin == {Q2_y_Bin}")).Histo2D((f"z-pT Bin ({Q2_y_Bin}-All)", f"#splitline{{z vs P_{{T}} for #color[{ROOT.kBlue}]{{Experimental Data}}}}{{#color[{ROOT.kRed}]{{Q^{{2}}-y Bin {Q2_y_Bin}}}}}; P_{{T}}; z",   pT_Binning[3], pT_Binning[1], pT_Binning[2],  z_Binning[3],  z_Binning[1],  z_Binning[2]), pT_Binning[0],  z_Binning[0])
            _, _, Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"]   = Create_Binned_Acceptance_Hist(mdf_IN=mdf_EvGen_binned,   gdf_IN=gdf_EvGen_binned,   source="EvGen",   PHI_T_Binning=phi_t_Binning, Q2_Y_Bin=Q2_y_Bin, Z_PT_Bin=None)
            _, _, Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"] = Create_Binned_Acceptance_Hist(mdf_IN=mdf_clasdis_binned, gdf_IN=gdf_clasdis_binned, source="clasdis", PHI_T_Binning=phi_t_Binning, Q2_Y_Bin=Q2_y_Bin, Z_PT_Bin=None)
            count += 8
            Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"] = 0
            z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin)[1]
            for z_pT_Bin in range(1, z_pT_Bin_Range + 1):
                if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin, Z_PT_BIN=z_pT_Bin, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=False)):
                    continue
                count += 6
                # print(f"{Q2_y_Bin:>2.0f} - {z_pT_Bin:>2.0f} (z-pT Total: {z_pT_Bin_Range}) -- Current Histo Total: {count}")
                _, _, Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"]   = Create_Binned_Acceptance_Hist(mdf_IN=mdf_EvGen_binned,   gdf_IN=gdf_EvGen_binned,   source="EvGen",   PHI_T_Binning=phi_t_Binning, Q2_Y_Bin=Q2_y_Bin, Z_PT_Bin=z_pT_Bin)
                _, _, Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"] = Create_Binned_Acceptance_Hist(mdf_IN=mdf_clasdis_binned, gdf_IN=gdf_clasdis_binned, source="clasdis", PHI_T_Binning=phi_t_Binning, Q2_Y_Bin=Q2_y_Bin, Z_PT_Bin=z_pT_Bin)
                Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"] = max([find_max_bin(Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"]), find_max_bin(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"]), Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"]])
            Acceptance_Canvases[f"Acceptance for Q2_y_Bin = {Q2_y_Bin}"] = Acceptance_Compare_z_pT_Images_Together(Histogram_List_All=Histogram_List_All, Q2_Y_Bin=Q2_y_Bin, Plot_Orientation="z_pT", Saving_Q=True, File_Save_Format=args.File_Save_Format)
        if(verbose):
            print(f"{color.BOLD}Total Histos Made for Binned Acceptance Images = {color.BBLUE}{count}{color.END}")
        print(f"\n{color.BOLD}DONE MAKING BINNED ACCEPTANCE PLOTS\n{color.END}")
        timer.time_elapsed()
    else:
        print(f"\n{color.Error}Skipping Binned Acceptance Comparison Plots{color.END}")

    
    timer.stop()
    print(f"{color.BBLUE}Done Running 'using_RDataFrames_python.py'\n{color.END}")
        