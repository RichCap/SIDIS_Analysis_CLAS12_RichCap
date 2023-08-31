#!/usr/bin/env python
# ==============================================================================
#  File and Version Information:
#       $Id$
#
#  Description:
#       Simple example usage of the RooUnfold package using toy MC.
#
#  Author: Tim Adye <T.J.Adye@rl.ac.uk>
#
# ==============================================================================

import sys
method = "bayes"
if(len(sys.argv) > 1):
    method = sys.argv[1]

from ROOT import gRandom, TH1, TH1D, TH2D, TCanvas, cout
import ROOT

import traceback
from datetime import datetime

ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetTitleOffset(1.3,'y')

ROOT.gStyle.SetGridColor(17)
ROOT.gStyle.SetPadGridX(1)
ROOT.gStyle.SetPadGridY(1)




class color:
    CYAN      = '\033[96m'
    PURPLE    = '\033[95m'
    BLUE      = '\033[94m'
    YELLOW    = '\033[93m'
    GREEN     = '\033[92m'
    RED       = '\033[91m'
    DARKCYAN  = '\033[36m'
    BOLD      = '\033[1m'
    LIGHT     = '\033[2m'
    ITALIC    = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK     = '\033[5m'
    DELTA     = '\u0394' # symbol
    END       = '\033[0m'
    
    
class color_bg:
    BLACK   = '\033[40m'
    RED     = '\033[41m'
    GREEN   = '\033[42m'
    YELLOW  = '\033[43m'
    BLUE    = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN    = '\033[46m'
    WHITE   = '\033[47m'
    RESET   = '\033[49m'
    END     = '\033[0m'
    
    
class root_color:
    # Colors
    White   = 0
    Black   = 1
    Red     = 2
    Green   = 3
    Blue    = 4
    Yellow  = 5
    Pink    = 6
    Cyan    = 7
    DGreen  = 8 # Dark Green
    Purple  = 9
    DGrey   = 13
    Grey    = 15
    LGrey   = 17
    Brown   = 28
    Gold    = 41
    Rust    = 46
    
    # Fonts
    Bold    = '#font[22]'
    Italic  = '#font[12]'
    
    # Symbols
    Delta   = '#Delta'
    Phi     = '#phi'
    Pi       = '#pi'
    Degrees = '#circ'
    
    Line    = '#splitline'

    

print("".join([color.BOLD, "\nStarting RG-A SIDIS Analysis\n", color.END]))

try:
    import RooUnfold
    # print("".join([color.GREEN, color.BOLD, "Perfect Success", color.END]))
except ImportError:
    print("".join([color.RED, color.BOLD, "ERROR: \n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n"]))
    print("Somehow the python module was not found, let's try loading the library by hand...")
    try:
        ROOT.gSystem.Load("libRooUnfold.so")
        print("".join([color.GREEN, "Success", color.END]))
    except:
        print("".join([color.RED, color.BOLD, "\nERROR IN IMPORTING RooUnfold...\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

        
# for ii in sys.modules:
#     if(str(ii) in ["ROOT", "RooUnfold"]):
#         print(ii)
#         print(sys.modules[ii])
# ==============================================================================
#  Gaussian smearing, systematic translation, and variable inefficiency
# ==============================================================================

def smear(xt):
    xeff = 0.3 + (1.0 - 0.3)/20*(xt + 10.0) #  efficiency
    x = gRandom.Rndm();
    if(x > xeff):
        return None
    # xsmear = gRandom.Gaus(-2.5, 0.2) #  bias and smear
    xsmear = gRandom.Gaus(-2.5, 0.9) #  bias and (Larger) smear
    return xt + xsmear


def smear_phi(xt):
    phi_rad = xt*ROOT.TMath.DegToRad()
    xeff = 0.65 + 0.35 * ROOT.TMath.Cos(6 * phi_rad) #  efficiency
    x = gRandom.Rndm();
    if(x > xeff):
        return None
    xsmear = gRandom.Gaus(-15, 20) #  bias and smear
    return xt + xsmear

# ==============================================================================
#  Example Unfolding
# ==============================================================================









##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##










def Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default"):
    
#############################################################################################################
#####=========================#####=======================================#####=========================#####
#####=====#####=====#####=====#####   Unfolding Method: "SVD" (Default)   #####=====#####=====#####=====#####
#####=========================#####=======================================#####=========================#####
#############################################################################################################
    if(Method in ["SVD", "Default"]):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.BLUE, "SVD", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")]))
#         print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main).replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), "")]))
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width

        ExREAL_1D.GetXaxis().SetRange(0,   nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0, nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0, nBins_CVM)     # Response Matrix (Y axis --> REC)
                        
        Covariance_Matrix = ROOT.TH2D("".join(["statcov_", str(Name_Main)]), "".join(["Covariance Matrix for: ", str(Name_Main)]), nBins_CVM, MinBinCVM, MaxBinCVM, nBins_CVM, MinBinCVM, MaxBinCVM)
        
        #######################################################################################
        ##==========##==========##   Filling the Covariance Matrix   ##==========##==========##
        #######################################################################################
        for CVM_Bin in range(0, nBins_CVM, 1):
            Covariance_Matrix.SetBinContent(CVM_Bin, CVM_Bin, ExREAL_1D.GetBinError(CVM_Bin)*ExREAL_1D.GetBinError(CVM_Bin))
        ######################################################################################
        ##==========##==========##   Filled the Covariance Matrix   ##==========##==========##
        ######################################################################################
             
        ########################################################
        ##=====##  Unfolding Regularization Parameter  ##=====##
        ########################################################
        Reg_Par = 13
        ########################################################
        ##=====##  Unfolding Regularization Parameter  ##=====##
        ########################################################
        
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D.GetNbinsX() == Response_2D.GetNbinsY()):
            try:
                Unfold_Obj = ROOT.TSVDUnfold(ExREAL_1D, Covariance_Matrix, MC_REC_1D, MC_GEN_1D, Response_2D)
                Unfold_Obj.SetNormalize(False)

                Unfolded_Histo = Unfold_Obj.Unfold(Reg_Par)

                Unfolded_Histo.SetLineColor(root_color.Pink)
                Unfolded_Histo.SetMarkerColor(root_color.Pink)
                Unfolded_Histo.SetMarkerSize(3)
                Unfolded_Histo.SetLineWidth(2)
                
                Unfolded_Determinate = Unfold_Obj.GetD()
                # Unfolded_Single_Value = Unfold_Obj[Unfolding_Canvas_Name].GetSV()

                unfolding_toys = 100

                Unfolded_Covariance_Matrix = Unfold_Obj.GetUnfoldCovMatrix(Covariance_Matrix, unfolding_toys)

                Error_Matrix = Unfold_Obj.GetAdetCovMatrix(100)

                Unfolded_Covariance_Matrix.Add(Error_Matrix)

                Regularized_CV_Matrix = Unfold_Obj.GetXtau()

                Regularized_CV_Matrix.Add(Error_Matrix)

                # Inverse_CV_Matrix = Unfold_Obj.GetXinv()

                for ii in range(1, Unfolded_Histo.GetNbinsX() + 1, 1):
                    Unfolded_Histo.SetBinError(ii, ROOT.sqrt(Regularized_CV_Matrix.GetBinContent(ii, ii)))
                
                Unfolded_Histo.SetTitle(((str(Unfolded_Histo.GetTitle()).replace("Experimental", "SVD Unfolded")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(Unfolded_Histo.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))
                
                List_Of_Outputs = [Unfolded_Histo, Unfold_Obj, Unfolded_Determinate, Unfolded_Covariance_Matrix, Regularized_CV_Matrix]    
                
                print("".join([color.BOLD, color.CYAN, "Finished ", color.BLUE, "SVD", color.END, color.BOLD, color.CYAN, " Unfolding Procedure.\n", color.END]))
                return List_Of_Outputs

            except:
                print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (SVD)...", color.END]))
                print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                
        else:
            print("unequal bins...")
            print("".join(["nBins_CVM               = ", str(nBins_CVM)]))
            print("".join(["MC_REC_1D.GetNbinsX()   = ", str(MC_REC_1D.GetNbinsX())]))
            print("".join(["MC_GEN_1D.GetNbinsX()   = ", str(MC_GEN_1D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsX() = ", str(Response_2D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsY() = ", str(Response_2D.GetNbinsY())]))
            return "ERROR"
###############################################################################################################
#####=========================#####=========================================#####=========================#####
#####=====#####=====#####=====#####     End of Method:  "SVD" (Default)     #####=====#####=====#####=====#####
#####=========================#####=========================================#####=========================#####
###############################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

############################################################################################################
#####=========================#####======================================#####=========================#####
#####=====#####=====#####=====#####    Unfolding Method: "Bin-by-Bin"    #####=====#####=====#####=====#####
#####=========================#####======================================#####=========================#####
############################################################################################################
    elif(Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))
        # print("".join([color.BOLD, "\tAcceptance Correction of Histogram:\n\t", color.END, str(MC_REC_1D.GetName()).replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), ""), ""]))
        if((str(MC_REC_1D.GetName()).find("-[NumBins")) != -1):
            Name_Print = str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName())[:(str(MC_REC_1D.GetName()).find("-[NumBins"))], ""), "))")
        else:
            Name_Print = str(MC_REC_1D.GetName())
        print("".join([color.BOLD, "\tAcceptance Correction of Histogram:\n\t", color.END, str(Name_Print).replace("(Data-Type='mdf'), ", "")]))
        try:
            Bin_Acceptance = MC_REC_1D.Clone()
            Bin_Acceptance.Sumw2()
            Bin_Acceptance.Divide(MC_GEN_1D)
            # Bin_Acceptance.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental Distribution of", "Bin-by-Bin Acceptance Correction factor for")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            Bin_Acceptance.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental Distribution of", "Bin-by-Bin Acceptance for")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            # Bin_Acceptance.GetYaxis().SetTitle("#frac{Number of REC Events}{Number of GEN Events}")
            Bin_Acceptance.GetYaxis().SetTitle("Acceptance")
            Bin_Acceptance.GetXaxis().SetTitle(str(Bin_Acceptance.GetXaxis().GetTitle()).replace("(REC)", ""))
            
            Bin_Unfolded = ExREAL_1D.Clone()
            Bin_Unfolded.Divide(Bin_Acceptance)
            Bin_Unfolded.SetTitle(((str(Bin_Unfolded.GetTitle()).replace("Experimental", "Bin-By-Bin Unfolded")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            
            cut_criteria = (0.01*Bin_Acceptance.GetBinContent(Bin_Acceptance.GetMaximumBin()))
            
            # for ii in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
            #     if(Bin_Acceptance.GetBinContent(ii) < cut_criteria):# or Bin_Acceptance.GetBinContent(ii) < 0.015):
            #         print("".join([color.RED, "\nBin ", str(ii), " had a very low acceptance...", color.END]))
            #         Bin_Unfolded.SetBinContent(ii, 0)
            
            print("".join([color.BOLD, color.CYAN, "Finished ", color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure.", color.END]))
            return [Bin_Unfolded, Bin_Acceptance]
        except:
            print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (Bin-by-Bin)...", color.END]))
            print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            return "ERROR"
############################################################################################################
#####=========================#####======================================#####=========================#####
#####=====#####=====#####=====#####     End of Method:  "Bin-by-Bin"     #####=====#####=====#####=====#####
#####=========================#####======================================#####=========================#####
############################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

##############################################################################################################
#####=========================#####========================================#####=========================#####
#####=====#####=====#####=====#####    Unfolding Method(s): "RooUnfold"    #####=====#####=====#####=====#####
#####=========================#####========================================#####=========================#####
##############################################################################################################
    elif("RooUnfold" in str(Method)):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.GREEN, "RooUnfold", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))        
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        # print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main).replace("".join([", (Var-D1='phi_t'-[NumBins=24, MinBin=0, MaxBin=360]), (Var-D2='z_pT_Bin", str(Binning_Method), "'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])"]), "")]))
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")]))
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width

        # print("".join([color.RED, color.BOLD, "\t\tnBins_CVM = ", str(nBins_CVM), "\n\t\tMinBinCVM = ", str(MinBinCVM), "\n\t\tMaxBinCVM = ", str(MaxBinCVM), color.END]))
        
        ExREAL_1D.GetXaxis().SetRange(0,   nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0, nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0, nBins_CVM)     # Response Matrix (Y axis --> REC)
        
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D.GetNbinsX() == Response_2D.GetNbinsY()):
            try:
                Response_RooUnfold = ROOT.RooUnfoldResponse(nBins_CVM, MinBinCVM, MaxBinCVM)
                
##==============##=======================================================##==============##
##==============##=====##     Constructing Response_RooUnfold     ##=====##==============##
##==============##=======================================================##==============##

                ##======================================##
                ##=====##     Generated Bins     ##=====##
                ##======================================##
                for gen_bin in range(0, nBins_CVM + 1, 1):
                    sum_of_gen = 0
                    gen_val    = Response_2D.GetXaxis().GetBinCenter(gen_bin)
                    ##======================================##
                    ##=====##   Reconstructed Bins   ##=====##
                    ##======================================##
                    for rec_bin in range(0, nBins_CVM + 1, 1):
                        rec_val = Response_2D.GetYaxis().GetBinCenter(rec_bin)
                        Res_Val = Response_2D.GetBinContent(gen_bin,  rec_bin)
                        sum_of_gen += Res_Val
                        
                        Response_RooUnfold.Fill(rec_val, gen_val, w=Res_Val)
                    ##======================================##
                    ##=====##   Reconstructed Bins   ##=====##
                    ##======================================##
                    gen_val_TRUE = MC_GEN_1D.GetBinContent(gen_bin)
                    if((gen_val_TRUE >= sum_of_gen) and (gen_val == MC_GEN_1D.GetBinCenter(gen_bin))):
                        gen_val_MISSED = gen_val_TRUE - sum_of_gen
                        Response_RooUnfold.Miss(gen_val, w=gen_val_MISSED)
                    else:
                        print("".join([color.RED, """
===================================================================================================================================================================================""", color.BOLD, """
MAJOR ERROR: sum_of_gen (""", str(sum_of_gen), """) is greater than gen_val_TRUE (""", str(gen_val_TRUE), """) for gen_bin = """, str(gen_bin), """ (i.e., there are more matched generated events than there should be generated events total)
             Error in this aspect of the code (need to check procedure/rewrite code)""", color.END, color.RED, """
===================================================================================================================================================================================
""", color.END]))
                ##======================================##
                ##=====##     Generated Bins     ##=====##
                ##======================================##
                
##==============##========================================================##==============##
##==============##=====##    Constructed the Response_RooUnfold    ##=====##==============##
##==============##========================================================##==============##


##==============##=======================================================##==============##
##==============##=====##      Applying the RooUnfold Method      ##=====##==============##
##==============##=======================================================##==============##
                Unfold_Title = "ERROR"
                if(str(Method) in ["RooUnfold", "RooUnfold_bayes"]):
                    Unfold_Title = "RooUnfold (Bayesian)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " method to unfold...", color.END]))

                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################
                    bayes_iterations = 10 if(("Multi_Dim" not in str(Name_Main)) or ("Multi_Dim_z_pT_Bin" in str(Name_Main))) else 4
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################

                    Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)

                elif("svd" in str(Method)):
                    Unfold_Title = "RooUnfold (SVD)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    ##################################################
                    ##=====##  SVD Regularization Parameter  ##=====##
                    ##################################################
                    Reg_Par = 13
                    ##################################################
                    ##=====##  SVD Regularization Parameter  ##=====##
                    ##################################################

                    Unfolding_Histo = ROOT.RooUnfoldSvd(Response_RooUnfold, ExREAL_1D, Reg_Par, 100)

                elif("bbb" in str(Method)):
                    Unfold_Title = "RooUnfold (Bin-by-Bin)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)

                elif("inv" in str(Method)):
                    Unfold_Title = "RooUnfold Inversion (without regulation)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldInvert(Response_RooUnfold, ExREAL_1D)

                else:
                    Unfold_Title = "RooUnfold (Bayesian)"
                    print("".join(["\t", color.RED, "Method '", color.BOLD, str(Method), color.END, color.RED, "' is unknown/undefined...", color.END]))
                    print("".join(["\t", color.RED, "Defaulting to using the ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.RED, " method to unfold...", color.END]))

                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################
                    bayes_iterations = 10
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################

                    Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)


##==============##==============================================================##==============##
##==============##=====##     Finished Applying the RooUnfold Method     ##=====##==============##
##==============##==============================================================##==============##

                Unfolded_Histo = Unfolding_Histo.Hunfold()
                # Unfolding_Histo.PrintTable(cout, hTrue);

                Unfolded_Histo.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental", str(Unfold_Title))).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))

                print("".join([color.BOLD, color.CYAN, "Finished ", color.GREEN, str(Unfold_Title), color.END, color.BOLD, color.CYAN, " Unfolding Procedure.\n", color.END]))
                return [Unfolded_Histo, Response_RooUnfold]

                        
            except:
                print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (RooUnfold)...", color.END]))
                print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, str(traceback.format_exc()), color.END]))
                
        else:
            print("".join([color.RED, "Unequal Bins...", color.END]))
            print("".join(["nBins_CVM = ", str(nBins_CVM)]))
            print("".join(["MC_REC_1D.GetNbinsX() = ",   str(MC_REC_1D.GetNbinsX())]))
            print("".join(["MC_GEN_1D.GetNbinsX() = ",   str(MC_GEN_1D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsX() = ", str(Response_2D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsY() = ", str(Response_2D.GetNbinsY())]))
            return "ERROR"
    

    else:
        print("".join(["Procedure for Method '", str(Method), "' has not yet been defined..."]))
        return "ERROR"
    
    print("".join([color.RED, color.BOLD, "\nERROR: DID NOT RETURN A HISTOGRAM YET...\n", color.END]))
    return "ERROR"




    
    
    
    
    
    
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##








##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##










def Unfold_Function_New(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, Method="Default"):
    
##############################################################################################################
#####=========================#####========================================#####=========================#####
#####=====#####=====#####=====#####   Unfolding Method: "SVD" (Original)   #####=====#####=====#####=====#####
#####=========================#####========================================#####=========================#####
##############################################################################################################
    if(Method in ["SVD"]):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.BLUE, "SVD", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")]))
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width

        ExREAL_1D.GetXaxis().SetRange(0,   nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0, nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0, nBins_CVM)     # Response Matrix (Y axis --> REC)
                        
        Covariance_Matrix = ROOT.TH2D("".join(["statcov_", str(Name_Main)]), "".join(["Covariance Matrix for: ", str(Name_Main)]), nBins_CVM, MinBinCVM, MaxBinCVM, nBins_CVM, MinBinCVM, MaxBinCVM)
        
        #######################################################################################
        ##==========##==========##   Filling the Covariance Matrix   ##==========##==========##
        #######################################################################################
        for CVM_Bin in range(0, nBins_CVM, 1):
            Covariance_Matrix.SetBinContent(CVM_Bin, CVM_Bin, ExREAL_1D.GetBinError(CVM_Bin)*ExREAL_1D.GetBinError(CVM_Bin))
        ######################################################################################
        ##==========##==========##   Filled the Covariance Matrix   ##==========##==========##
        ######################################################################################
             
        ########################################################
        ##=====##  Unfolding Regularization Parameter  ##=====##
        ########################################################
        Reg_Par = 13
        ########################################################
        ##=====##  Unfolding Regularization Parameter  ##=====##
        ########################################################
        
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D.GetNbinsX() == Response_2D.GetNbinsY()):
            try:
                Unfold_Obj = ROOT.TSVDUnfold(ExREAL_1D, Covariance_Matrix, MC_REC_1D, MC_GEN_1D, Response_2D)
                Unfold_Obj.SetNormalize(False)

                Unfolded_Histo = Unfold_Obj.Unfold(Reg_Par)

                Unfolded_Histo.SetLineColor(root_color.Pink)
                Unfolded_Histo.SetMarkerColor(root_color.Pink)
                Unfolded_Histo.SetMarkerSize(3)
                Unfolded_Histo.SetLineWidth(2)
                
                Unfolded_Determinate = Unfold_Obj.GetD()
                # Unfolded_Single_Value = Unfold_Obj[Unfolding_Canvas_Name].GetSV()

                unfolding_toys = 100

                Unfolded_Covariance_Matrix = Unfold_Obj.GetUnfoldCovMatrix(Covariance_Matrix, unfolding_toys)

                Error_Matrix = Unfold_Obj.GetAdetCovMatrix(100)

                Unfolded_Covariance_Matrix.Add(Error_Matrix)

                Regularized_CV_Matrix = Unfold_Obj.GetXtau()

                Regularized_CV_Matrix.Add(Error_Matrix)

                # Inverse_CV_Matrix = Unfold_Obj.GetXinv()

                for ii in range(1, Unfolded_Histo.GetNbinsX() + 1, 1):
                    Unfolded_Histo.SetBinError(ii, ROOT.sqrt(Regularized_CV_Matrix.GetBinContent(ii, ii)))
                
                Unfolded_Histo.SetTitle(((str(Unfolded_Histo.GetTitle()).replace("Experimental", "SVD Unfolded")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(Unfolded_Histo.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))
                
                List_Of_Outputs = [Unfolded_Histo, Unfold_Obj, Unfolded_Determinate, Unfolded_Covariance_Matrix, Regularized_CV_Matrix]    
                
                print("".join([color.BOLD, color.CYAN, "Finished ", color.BLUE, "SVD", color.END, color.BOLD, color.CYAN, " Unfolding Procedure.\n", color.END]))
                return List_Of_Outputs

            except:
                print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (SVD)...", color.END]))
                print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
                
        else:
            print("unequal bins...")
            print("".join(["nBins_CVM               = ", str(nBins_CVM)]))
            print("".join(["MC_REC_1D.GetNbinsX()   = ", str(MC_REC_1D.GetNbinsX())]))
            print("".join(["MC_GEN_1D.GetNbinsX()   = ", str(MC_GEN_1D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsX() = ", str(Response_2D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsY() = ", str(Response_2D.GetNbinsY())]))
            return "ERROR"
####################################################################################################################
#####=========================#####==============================================#####=========================#####
#####=====#####=====#####=====#####     End of Method: "SVD" (Original)          #####=====#####=====#####=====#####
#####=========================#####==============================================#####=========================#####
####################################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

############################################################################################################
#####=========================#####======================================#####=========================#####
#####=====#####=====#####=====#####    Unfolding Method: "Bin-by-Bin"    #####=====#####=====#####=====#####
#####=========================#####======================================#####=========================#####
############################################################################################################
    elif(Method in ["Bin", "bin", "Bin-by-Bin", "Bin by Bin"]):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))
        if((str(MC_REC_1D.GetName()).find("-[NumBins")) != -1):
            Name_Print = str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName()).replace(str(MC_REC_1D.GetName())[:(str(MC_REC_1D.GetName()).find("-[NumBins"))], ""), "))")
        else:
            Name_Print = str(MC_REC_1D.GetName())
        print("".join([color.BOLD, "\tAcceptance Correction of Histogram:\n\t", color.END, str(Name_Print).replace("(Data-Type='mdf'), ", "")]))
        try:
            Bin_Acceptance = MC_REC_1D.Clone()
            Bin_Acceptance.Sumw2()
            Bin_Acceptance.Divide(MC_GEN_1D)
            Bin_Acceptance.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental Distribution of", "Bin-by-Bin Acceptance for")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            # Bin_Acceptance.GetYaxis().SetTitle("#frac{Number of REC Events}{Number of GEN Events}")
            Bin_Acceptance.GetYaxis().SetTitle("Acceptance")
            Bin_Acceptance.GetXaxis().SetTitle(str(Bin_Acceptance.GetXaxis().GetTitle()).replace("(REC)", ""))
            
            Bin_Unfolded = ExREAL_1D.Clone()
            Bin_Unfolded.Divide(Bin_Acceptance)
            Bin_Unfolded.SetTitle(((str(Bin_Unfolded.GetTitle()).replace("Experimental", "Bin-By-Bin Unfolded")).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
            Bin_Unfolded.Sumw2()
            
            cut_criteria = (0.01*Bin_Acceptance.GetBinContent(Bin_Acceptance.GetMaximumBin()))
            
            # for ii in range(0, Bin_Acceptance.GetNbinsX() + 1, 1):
            #     if(Bin_Acceptance.GetBinContent(ii) < cut_criteria):# or Bin_Acceptance.GetBinContent(ii) < 0.015):
            #         print("".join([color.RED, "\nBin ", str(ii), " had a very low acceptance...", color.END]))
            #         Bin_Unfolded.SetBinContent(ii, 0)
            
            print("".join([color.BOLD, color.CYAN, "Finished ", color.PURPLE, "Bin-by-Bin", color.END, color.BOLD, color.CYAN, " Unfolding Procedure.", color.END]))
            return [Bin_Unfolded, Bin_Acceptance]
        except:
            print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (Bin-by-Bin)...", color.END]))
            print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            return "ERROR"
############################################################################################################
#####=========================#####======================================#####=========================#####
#####=====#####=====#####=====#####     End of Method:  "Bin-by-Bin"     #####=====#####=====#####=====#####
#####=========================#####======================================#####=========================#####
############################################################################################################

#############################################################################################################################################################################
#############################################################################################################################################################################

##############################################################################################################
#####=========================#####========================================#####=========================#####
#####=====#####=====#####=====#####    Unfolding Method(s): "RooUnfold"    #####=====#####=====#####=====#####
#####=========================#####========================================#####=========================#####
##############################################################################################################
    elif(("RooUnfold" in str(Method)) or (str(Method) in ["Default"])):
        print("".join([color.BOLD, color.CYAN, "Starting ", color.UNDERLINE, color.GREEN, "RooUnfold", color.END, color.BOLD, color.CYAN, " Unfolding Procedure...", color.END]))        
        Name_Main = Response_2D.GetName()
        if((str(Name_Main).find("-[NumBins")) != -1):
            Name_Main_Print = str(Name_Main).replace(str(Name_Main).replace(str(Name_Main)[:(str(Name_Main).find("-[NumBins"))], ""), "))")
        else:
            Name_Main_Print = str(Name_Main)
        print("".join([color.BOLD, "\tUnfolding Histogram:\n\t", color.END, str(Name_Main_Print).replace("(Data-Type='mdf'), ", "")]))
        
        nBins_CVM = ExREAL_1D.GetNbinsX()
        bin_Width = ExREAL_1D.GetBinWidth(1)
        MinBinCVM = ExREAL_1D.GetBinCenter(0)
        MaxBinCVM = ExREAL_1D.GetBinCenter(nBins_CVM)
        
        MinBinCVM += 0.5*bin_Width
        MaxBinCVM += 0.5*bin_Width
        
        ExREAL_1D.GetXaxis().SetRange(0,   nBins_CVM)     # Experimental/real data (rdf)
        MC_REC_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Reconstructed data (mdf)
        MC_GEN_1D.GetXaxis().SetRange(0,   nBins_CVM)     # MC Generated data (gdf)
        Response_2D.GetXaxis().SetRange(0, nBins_CVM)     # Response Matrix (X axis --> GEN)
        Response_2D.GetYaxis().SetRange(0, nBins_CVM)     # Response Matrix (Y axis --> REC)
        
        if(True):
            Response_2D_Input_Title = "".join([str(Response_2D.GetTitle()), ";", str(Response_2D.GetYaxis().GetTitle()), ";", str(Response_2D.GetXaxis().GetTitle())])
            Response_2D_Input       = ROOT.TH2D("".join([str(Response_2D.GetName()), "_Flipped"]), str(Response_2D_Input_Title), Response_2D.GetNbinsY(), MinBinCVM, MaxBinCVM, Response_2D.GetNbinsX(), MinBinCVM, MaxBinCVM)
            # Use the following code if the input Response Matrix plots the generated events on the x-axis
            # # The RooUnfold library takes Response Matrices which plot the true/generated events on the y-axis and the measured/reconstructed events on the x-axis
            ##==============##============================================##==============##
            ##==============##=====##     Flipping Response_2D     ##=====##==============##
            ##=========##   Generated Bins       ##=====##
            for gen_bin in range(0, nBins_CVM + 1, 1):
                ##=====##   Reconstructed Bins   ##=====##
                for rec_bin in range(0, nBins_CVM + 1, 1):
                    Res_Value = Response_2D.GetBinContent(gen_bin,    rec_bin)
                    Res_Error = Response_2D.GetBinError(gen_bin,      rec_bin)
                    Response_2D_Input.SetBinContent(rec_bin, gen_bin, Res_Value)
                    Response_2D_Input.SetBinError(rec_bin,   gen_bin, Res_Error)
            ##==============##=====##     Flipped Response_2D      ##=====##==============##
            ##==============##============================================##==============##
            Response_2D_Input.Sumw2()
        else:
            Response_2D_Input_Title = "".join([str(Response_2D.GetTitle()), ";", str(Response_2D.GetXaxis().GetTitle()), ";", str(Response_2D.GetYaxis().GetTitle())])
            Response_2D_Input       = Response_2D

        
        if(nBins_CVM == MC_REC_1D.GetNbinsX() == MC_GEN_1D.GetNbinsX() == Response_2D_Input.GetNbinsX() == Response_2D_Input.GetNbinsY()):
            try:
                # Response_RooUnfold = ROOT.RooUnfoldResponse(nBins_CVM, MinBinCVM, MaxBinCVM)
                Response_RooUnfold = ROOT.RooUnfoldResponse(MC_REC_1D, MC_GEN_1D, Response_2D_Input, "".join([str(Response_2D.GetName()), "_RooUnfoldResponse_Object"]), Response_2D_Input_Title)

##==============##=======================================================##==============##
##==============##=====##      Applying the RooUnfold Method      ##=====##==============##
##==============##=======================================================##==============##
                Unfold_Title = "ERROR"
                if("svd" in str(Method)):
                    Unfold_Title = "RooUnfold (SVD)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    ##################################################
                    ##=====##  SVD Regularization Parameter  ##=====##
                    ##################################################
                    Reg_Par = 13
                    ##################################################
                    ##=====##  SVD Regularization Parameter  ##=====##
                    ##################################################

                    Unfolding_Histo = ROOT.RooUnfoldSvd(Response_RooUnfold, ExREAL_1D, Reg_Par, 100)

                elif("bbb" in str(Method)):
                    Unfold_Title = "RooUnfold (Bin-by-Bin)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)

                elif("inv" in str(Method)):
                    Unfold_Title = "RooUnfold Inversion (without regulation)"
                    print("".join(["\t", color.CYAN, "Using ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " Unfolding Procedure...", color.END]))

                    Unfolding_Histo = ROOT.RooUnfoldInvert(Response_RooUnfold, ExREAL_1D)

                else:
                    Unfold_Title = "RooUnfold (Bayesian)"
                    if(str(Method) not in ["RooUnfold", "RooUnfold_bayes", "Default"]):
                        print("".join(["\t", color.RED, "Method '",                 color.BOLD,              str(Method),       color.END, color.RED,  "' is unknown/undefined...", color.END]))
                        print("".join(["\t", color.RED, "Defaulting to using the ", color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.RED,  " method to unfold...",      color.END]))
                    else:
                        print("".join(["\t", color.CYAN, "Using ",                  color.BOLD, color.GREEN, str(Unfold_Title), color.END, color.CYAN, " method to unfold...",      color.END]))
                        
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################
                    bayes_iterations = 10 if(("Multi_Dim" not in str(Name_Main)) or ("Multi_Dim_z_pT_Bin" in str(Name_Main))) else 4
                    #########################################
                    ##=====##  Bayesian Iterations  ##=====##
                    #########################################

                    Unfolding_Histo = ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)


##==============##==============================================================##==============##
##==============##=====##     Finished Applying the RooUnfold Method     ##=====##==============##
##==============##==============================================================##==============##

                Unfolded_Histo = Unfolding_Histo.Hunfold()

                Unfolded_Histo.SetTitle(((str(ExREAL_1D.GetTitle()).replace("Experimental", str(Unfold_Title))).replace("Cut: Complete Set of SIDIS Cuts", "")).replace("Cut:  Complete Set of SIDIS Cuts", ""))
                Unfolded_Histo.GetXaxis().SetTitle(str(ExREAL_1D.GetXaxis().GetTitle()).replace("(REC)", "(Smeared)" if("smeared" in str(Name_Main) or "smear" in str(Name_Main)) else ""))

                print("".join([color.BOLD, color.CYAN, "Finished ", color.GREEN, str(Unfold_Title), color.END, color.BOLD, color.CYAN, " Unfolding Procedure.\n", color.END]))
                return [Unfolded_Histo, Response_RooUnfold]

                        
            except:
                print("".join([color.BOLD, color.RED, "\nFAILED TO UNFOLD A HISTOGRAM (RooUnfold)...", color.END]))
                print("".join([color.BOLD, color.RED, "ERROR:\n", color.END, str(traceback.format_exc()), color.END]))
                
        else:
            print("".join([color.RED, "Unequal Bins...", color.END]))
            print("".join(["nBins_CVM = ", str(nBins_CVM)]))
            print("".join(["MC_REC_1D.GetNbinsX() = ",   str(MC_REC_1D.GetNbinsX())]))
            print("".join(["MC_GEN_1D.GetNbinsX() = ",   str(MC_GEN_1D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsX() = ", str(Response_2D.GetNbinsX())]))
            print("".join(["Response_2D.GetNbinsY() = ", str(Response_2D.GetNbinsY())]))
            return "ERROR"
    

    else:
        print("".join(["Procedure for Method '", str(Method), "' has not yet been defined..."]))
        return "ERROR"
    
    print("".join([color.RED, color.BOLD, "\nERROR: DID NOT RETURN A HISTOGRAM YET...\n", color.END]))
    return "ERROR"




    
    
    
    
    
    
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
##=======================================================================================================================================================================================================##
















# ###############################################################################################################
# ##=====##=====## TESTING WITH DEFAULT EXAMPLE FROM THIS CODE - CAME WITH THE RooUnfold LIBRARY ##=====##=====##
# ###############################################################################################################
# num_bin, min_bin, max_bin = 40, -10.0, 10.0
# Response       = ROOT.RooUnfoldResponse(num_bin, min_bin, max_bin)
# MC_Gen         = TH1D("MC_Gen", "MC GEN Test", num_bin, min_bin, max_bin)
# MC_Rec         = TH1D("MC_Rec", "MC REC Test", num_bin, min_bin, max_bin)
# Res_2D         = TH2D("Res_2D", "Response 2D", num_bin, min_bin, max_bin, num_bin, min_bin, max_bin)
# Res_2D_Flipped = TH2D("Res_2D_Flipped", "Response 2D ; Measured; Truth", num_bin, min_bin, max_bin, num_bin, min_bin, max_bin)
# #  Train with a Breit-Wigner, mean 0.3 and width 2.5.
# # num_Low = 0
# for ii in range(100000):
#     xt  = gRandom.BreitWigner(0.3 + 1, 2.5)
#     xt += gRandom.BreitWigner(0.3 - 3, 1.5)
#     # if(xt < -10):
#     #     num_Low += 1
#     #     print("".join([str(num_Low) ,") xt = ", str(xt)]))
#     if(abs(xt) > 10):
#         continue
#     x   = smear(xt)
#     MC_Gen.Fill(xt)
#     if(x != None):
#         Response.Fill(x, xt)
#         Res_2D.Fill(xt, x)
#         Res_2D_Flipped.Fill(x, xt)
#         MC_Rec.Fill(x)
#     else:
#         Response.Miss(xt)
# hTrue = TH1D("true", "Test Truth",    num_bin, min_bin, max_bin)
# hMeas = TH1D("meas", "Test Measured", num_bin, min_bin, max_bin)
# #  Test with a Gaussian, mean 0 and width 2.
# for ii in range(10000):
#     xt  = gRandom.Gaus(0.0 + 1, 2.0)
#     xt += gRandom.Gaus(0.0 - 3, 1.0)
#     x   = smear(xt)
#     if(abs(xt) > 10):
#         continue
#     hTrue.Fill(xt)
#     if(x != None): 
#         hMeas.Fill(x)
        
        
def Weight_Calc(phi_t):
    Par_B_Test   = -0.50;
    Par_C_Test   =  0.25;
    PHI_H        = phi_t*ROOT.TMath.DegToRad();
    Event_Weight = 1 + Par_B_Test*ROOT.TMath.Cos(PHI_H) + Par_C_Test*ROOT.TMath.Cos(2*PHI_H);
    return Event_Weight;

################################################################################################
##=====##=====## TESTING FOR PHI FROM 0 TO 360 DEGREES - DDEVELOPED SEPARATELY  ##=====##=====##
################################################################################################
num_bin, min_bin, max_bin = 24, 0, 360
random_generator = ROOT.TRandom3()
Response         = ROOT.RooUnfoldResponse(num_bin, min_bin, max_bin)
MC_Gen           = TH1D("MC_Gen",         "MC GEN Test", num_bin, min_bin, max_bin)
MC_Rec           = TH1D("MC_Rec",         "MC REC Test", num_bin, min_bin, max_bin)
Res_2D           = TH2D("Res_2D",         "Response 2D ; Truth; Measured", num_bin, min_bin, max_bin, num_bin, min_bin, max_bin)
Res_2D_Flipped   = TH2D("Res_2D_Flipped", "Response 2D ; Measured; Truth", num_bin, min_bin, max_bin, num_bin, min_bin, max_bin)
#  Creating set of histograms to be used as the 'MC' data to create the response matrix
for ii in range(100000):
    xt     = random_generator.Uniform(min_bin, max_bin)
    Weight = Weight_Calc(xt)
    x      = smear_phi(xt)
    MC_Gen.Fill(xt, w=Weight)
    if(x != None):
        if(x > 360):
            x += -360
        if(x < 0):
            x +=  360
        Response.Fill(x, xt,       w=Weight)
        Res_2D.Fill(xt,  x,        w=Weight)
        Res_2D_Flipped.Fill(x, xt, w=Weight)
        MC_Rec.Fill(x,             w=Weight)
    else:
        Response.Miss(xt,          w=Weight)
hTrue = TH1D("true", "Test Truth",    num_bin, min_bin, max_bin)
hMeas = TH1D("meas", "Test Measured", num_bin, min_bin, max_bin)
#  Creating set of histograms to be unfolded
for ii in range(10000):
    xt     = random_generator.Uniform(min_bin, max_bin)
    Weight = Weight_Calc(xt)
    x      = smear_phi(xt)
    hTrue.Fill(xt,    w=Weight)
    if(x != None): 
        if(x > 360):
            x += -360
        if(x < 0):
            x +=  360
        hMeas.Fill(x, w=Weight)
# hTrue = MC_Gen.Clone("true")
# hMeas = MC_Rec.Clone("meas") 
        
        
        
        
# if(method == "bayes"):
#     unfold = ROOT.RooUnfoldBayes(Response, hMeas, 5)
# elif(method == "svd"):
#     unfold = ROOT.RooUnfoldSvd(Response, hMeas, 20)
# elif(method == "bbb"):
#     unfold = ROOT.RooUnfoldBinByBin(Response, hMeas)
# elif(method == "inv"):
#     unfold = ROOT.RooUnfoldInvert(Response, hMeas)
# elif(method == "root"):
#     unfold = ROOT.RooUnfoldTUnfold(Response, hMeas)
# elif(method == "ids"):
#     unfold = ROOT.RooUnfoldIds(Response, hMeas, 3)
    
    
# My_Unfold_SVD_List = Unfold_Function(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="SVD")
# My_Unfold_SVD      = My_Unfold_SVD_List[0]









# hMeas.Sumw2()
# MC_Rec.Sumw2()
# MC_Gen.Sumw2()
# Res_2D.Sumw2()
# Res_2D_Flipped.Sumw2()


# Unfold_Bin_List           = Unfold_Function(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="Bin")
# Unfold_Bin                = Unfold_Bin_List[0]

# Unfold_RooUnfold_Bin_List = Unfold_Function(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="RooUnfold_bbb")
# Unfold_RooUnfold_Bin, Unfold_RooUnfold_Bin_Response    = Unfold_RooUnfold_Bin_List

# Unfold_RooUnfold_List     = Unfold_Function(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="RooUnfold_bayes")
# Unfold_RooUnfold,     Unfold_RooUnfold_Response        = Unfold_RooUnfold_List

# Unfold_RooUnfold_SVD_List = Unfold_Function(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="RooUnfold_svd")
# Unfold_RooUnfold_SVD, Unfold_RooUnfold_SVD_Response    = Unfold_RooUnfold_SVD_List




Unfold_Bin_List           = Unfold_Function_New(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="Bin")
Unfold_Bin                = Unfold_Bin_List[0]

Unfold_RooUnfold_Bin_List = Unfold_Function_New(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="RooUnfold_bbb")
Unfold_RooUnfold_Bin, Unfold_RooUnfold_Bin_Response        = Unfold_RooUnfold_Bin_List

Unfold_RooUnfold_List     = Unfold_Function_New(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="RooUnfold_bayes")
Unfold_RooUnfold,     Unfold_RooUnfold_Response            = Unfold_RooUnfold_List

Unfold_RooUnfold_SVD_List = Unfold_Function_New(Response_2D=Res_2D, ExREAL_1D=hMeas, MC_REC_1D=MC_Rec, MC_GEN_1D=MC_Gen, Method="RooUnfold_svd")
Unfold_RooUnfold_SVD, Unfold_RooUnfold_SVD_Response        = Unfold_RooUnfold_SVD_List



















# hUnfold = unfold.Hunfold()

# unfold.PrintTable(cout, hTrue)



Unfold_RooUnfold_Res_Matrix = Unfold_RooUnfold_Response.Hresponse()
Unfold_RooUnfold_Res_Matrix.SetTitle("#splitline{My RooUnfold Response Matrix}{From Unfold_Function(Method='RooUnfold_bayes')}; Measured; Truth")
Unfold_Test_Res_Matrix = Response.Hresponse()
Unfold_Test_Res_Matrix.SetTitle("Response Matrix from RooUnfoldExample.py; Measured; Truth")
Unfold_RooUnfold_Htruth = Unfold_RooUnfold_Response.Htruth()
Unfold_RooUnfold_Htruth.SetTitle("Truth from My Version of Unfold_RooUnfold_Response")
Unfold_Test_Htruth = Response.Htruth()
Unfold_Test_Htruth.SetTitle("Truth from RooUnfoldExample.py")


print("".join([color.BOLD, "\n\nFinished Unfolding...\n", color.END]))


max_bin_content_list = [hTrue, Unfold_RooUnfold_Bin, Unfold_Bin, Unfold_RooUnfold, Unfold_RooUnfold_SVD, MC_Gen, Unfold_RooUnfold_Htruth, Unfold_Test_Htruth]
max_bin_content_list = [hTrue, Unfold_RooUnfold_Bin, Unfold_Bin, Unfold_RooUnfold]
max_bin_content = 0
for hist in max_bin_content_list:
    # print("Testing:", str(hist.GetName()))
    if(max_bin_content  < hist.GetBinContent(hist.GetMaximumBin())):
        max_bin_content = hist.GetBinContent(hist.GetMaximumBin())
        # print(color.BOLD, "NEW MAX\n\n", color.END)
        
        
max_bin_content_list_2 = [hTrue, MC_Gen, Unfold_RooUnfold_Htruth, Unfold_Test_Htruth]
max_bin_content_2 = 0
for hist in max_bin_content_list_2:
    # print("Testing:", str(hist.GetName()))
    if(max_bin_content_2  < hist.GetBinContent(hist.GetMaximumBin())):
        max_bin_content_2 = hist.GetBinContent(hist.GetMaximumBin())

# print("max_bin_content comes from Histogram.GetName() =", max_histo_name)
        

hTrue.GetYaxis().SetRangeUser(0,                   1.25*max_bin_content)
hMeas.GetYaxis().SetRangeUser(0,                   1.25*max_bin_content)
Unfold_RooUnfold.GetYaxis().SetRangeUser(0,        1.25*max_bin_content)
Unfold_RooUnfold_SVD.GetYaxis().SetRangeUser(0,    1.25*max_bin_content)
Unfold_RooUnfold_Bin.GetYaxis().SetRangeUser(0,    1.25*max_bin_content)
Unfold_Bin.GetYaxis().SetRangeUser(0,              1.25*max_bin_content)
MC_Gen.GetYaxis().SetRangeUser(0,                  1.25*max_bin_content_2)
MC_Rec.GetYaxis().SetRangeUser(0,                  1.25*max_bin_content_2)
Unfold_RooUnfold_Htruth.GetYaxis().SetRangeUser(0, 1.25*max_bin_content_2)
Unfold_Test_Htruth.GetYaxis().SetRangeUser(0,      1.25*max_bin_content_2)

Res_2D.GetYaxis().SetRangeUser(min_bin,                         max_bin)
Res_2D_Flipped.GetYaxis().SetRangeUser(min_bin,                 max_bin)
Unfold_RooUnfold_Res_Matrix.GetYaxis().SetRangeUser(min_bin,    max_bin)
Unfold_Test_Res_Matrix.GetYaxis().SetRangeUser(min_bin,         max_bin)

hTrue.GetXaxis().SetRangeUser(min_bin,                          max_bin)
hMeas.GetXaxis().SetRangeUser(min_bin,                          max_bin)
Unfold_RooUnfold.GetXaxis().SetRangeUser(min_bin,               max_bin)
Unfold_RooUnfold_SVD.GetXaxis().SetRangeUser(min_bin,           max_bin)
Unfold_RooUnfold_Bin.GetXaxis().SetRangeUser(min_bin,           max_bin)
Unfold_Bin.GetXaxis().SetRangeUser(min_bin,                     max_bin)
MC_Gen.GetXaxis().SetRangeUser(min_bin,                         max_bin)
MC_Rec.GetXaxis().SetRangeUser(min_bin,                         max_bin)
Unfold_RooUnfold_Htruth.GetXaxis().SetRangeUser(min_bin,        max_bin)
Unfold_Test_Htruth.GetXaxis().SetRangeUser(min_bin,             max_bin)
Res_2D.GetXaxis().SetRangeUser(min_bin,                         max_bin)
Res_2D_Flipped.GetXaxis().SetRangeUser(min_bin,                 max_bin)
Unfold_RooUnfold_Res_Matrix.GetXaxis().SetRangeUser(min_bin,    max_bin)
Unfold_Test_Res_Matrix.GetXaxis().SetRangeUser(min_bin,         max_bin)

# canvas = ROOT.TCanvas("RooUnfold", method)
canvas = ROOT.TCanvas("RooUnfold", method, 1000, 1560)
canvas.Divide(1, 3)
canvas_lower = canvas.cd(2)

canvas_lower.Divide(2, 2)

canvas_lower.cd(1)
hTrue.SetLineStyle(1)
hTrue.SetLineWidth(2)
hTrue.SetLineColor(8)
hTrue.Draw("hist same E0")
hMeas.SetLineStyle(1)
hMeas.SetLineWidth(2)
hMeas.SetLineColor(1)
hMeas.Draw("hist same E0")
Unfold_RooUnfold_Bin.SetLineStyle(2)
Unfold_RooUnfold_Bin.SetLineColor(9)
Unfold_RooUnfold_Bin.SetLineWidth(3)
Unfold_RooUnfold_Bin.Draw("hist same E0")
Unfold_Bin.SetLineStyle(9)
Unfold_Bin.SetLineColor(41)
Unfold_Bin.SetLineWidth(1)
Unfold_Bin.Draw("hist same E0")


canvas_lower.cd(2)
hTrue.SetLineStyle(1)
hTrue.SetLineWidth(2)
hTrue.SetLineColor(8)
hTrue.Draw("hist same E0")
hMeas.SetLineStyle(1)
hMeas.SetLineWidth(2)
hMeas.SetLineColor(1)
hMeas.Draw("hist same E0")
Unfold_RooUnfold.SetLineStyle(2)
Unfold_RooUnfold.SetLineColor(6)
Unfold_RooUnfold.SetLineWidth(1)
Unfold_RooUnfold.Draw("hist same E0")



canvas_lower.cd(3)
hTrue.SetLineStyle(1)
hTrue.SetLineWidth(2)
hTrue.SetLineColor(8)
hTrue.Draw("hist same E0")
hMeas.SetLineStyle(1)
hMeas.SetLineWidth(2)
hMeas.SetLineColor(1)
hMeas.Draw("hist same E0")
Unfold_RooUnfold_SVD.SetLineStyle(3)
Unfold_RooUnfold_SVD.SetLineColor(28)
Unfold_RooUnfold_SVD.SetLineWidth(1)
Unfold_RooUnfold_SVD.Draw("hist same E0")


canvas_lower.cd(4)
Unfold_RooUnfold_Bin.Draw("hist same E0")
Unfold_RooUnfold.Draw("hist same E0")
Unfold_RooUnfold_SVD.Draw("hist same E0")
Unfold_Bin.Draw("hist same E0")








canvas.cd(1)
hTrue.SetLineStyle(1)
hTrue.SetLineWidth(2)
hTrue.SetLineColor(8)
hTrue.Draw("hist same E0")

hMeas.SetLineStyle(1)
hMeas.SetLineWidth(2)
hMeas.SetLineColor(1)
hMeas.Draw("hist same E0")

Unfold_RooUnfold_Bin.Draw("hist same E0")
Unfold_RooUnfold.Draw("hist same E0")
Unfold_RooUnfold_SVD.Draw("hist same E0")
Unfold_Bin.Draw("hist same E0")


Unfold_Legend = ROOT.TLegend(0.65, 0.25, 0.95, 0.55)
Unfold_Legend.SetNColumns(2)
Unfold_Legend.SetBorderSize(0)
Unfold_Legend.SetFillColor(0)
Unfold_Legend.SetFillStyle(2)

Unfold_Legend.AddEntry(hMeas,                "hMeas", "l")
Unfold_Legend.AddEntry(hTrue,                "hTrue", "l")
Unfold_Legend.AddEntry(Unfold_Bin,           "Bin-by-Bin", "l")
Unfold_Legend.AddEntry(Unfold_RooUnfold,     "Bayesian", "l")
Unfold_Legend.AddEntry(Unfold_RooUnfold_SVD, "SVD", "l")
Unfold_Legend.AddEntry(Unfold_RooUnfold_Bin, "(RooUnfold) Bin-by-Bin", "l")

Unfold_Legend.Draw("same")



canvas_lowest = canvas.cd(3)
canvas_lowest.Divide(3, 2)

canvas_lowest.cd(1)
hTrue.Draw("hist same E0")

canvas_lowest.cd(2)
hMeas.Draw("hist same E0")

canvas_lowest.cd(3)
Unfold_RooUnfold_Bin.SetTitle("Unfold_RooUnfold_Bin".replace("_", " "))
Unfold_RooUnfold_Bin.Draw("hist same E0")
hTrue.Draw("hist same E0")
hMeas.Draw("hist same E0")

canvas_lowest.cd(4)
Unfold_RooUnfold.SetTitle("Unfold_RooUnfold".replace("_", " "))
Unfold_RooUnfold.Draw("hist same E0")
hTrue.Draw("hist same E0")
hMeas.Draw("hist same E0")

canvas_lowest.cd(5)
Unfold_RooUnfold_SVD.SetTitle("Unfold_RooUnfold_SVD".replace("_", " "))
Unfold_RooUnfold_SVD.Draw("hist same E0")
hTrue.Draw("hist same E0")
hMeas.Draw("hist same E0")

canvas_lowest.cd(6)
Unfold_Bin.SetTitle("Unfold_Bin".replace("_", " "))
Unfold_Bin.Draw("hist same E0")
hTrue.Draw("hist same E0")
hMeas.Draw("hist same E0")

# canvas.Draw()
canvas.SaveAs("RooUnfold_Test_NEW_Phi_Mod_6.pdf")











canvas_Res = ROOT.TCanvas("RooUnfold_Res", method, 1200, 1200)
canvas_Res.Divide(1, 2)
ROOT.gStyle.SetOptStat(0)

canvas_Res_upper, canvas_Res_lower = canvas_Res.cd(1), canvas_Res.cd(2)

canvas_Res_upper.Divide(4, 1)
canvas_Res_lower.Divide(4, 1)


canvas_Res_upper.cd(1)
Unfold_RooUnfold_Res_Matrix.Draw("colz")

canvas_Res_upper.cd(2)
Unfold_Test_Res_Matrix.Draw("colz")

canvas_Res_upper.cd(3)
Res_2D_Flipped.SetTitle("FLIPPED INPUT Response Matrix; Measured; Truth")
Res_2D_Flipped.Draw("colz")

canvas_Res_upper.cd(4)
Res_2D.SetTitle("INPUT Response Matrix; Truth; Measured")
Res_2D.Draw("colz")


canvas_Res_lower.cd(1)
Unfold_RooUnfold_Htruth.Draw("hist same E0")

canvas_Res_lower.cd(2)
Unfold_Test_Htruth.Draw("hist same E0")

canvas_Res_lower.cd(3)
Unfold_RooUnfold_Htruth.SetTitle("".join(["#splitline{Comparison of 'True' Histograms}{#font[22]{Unfold_RooUnfold_Response} and #color[", str(root_color.Blue), "]{RooUnfoldExample.py}}"]))
Unfold_Test_Htruth.SetTitle("".join([     "#splitline{Comparison of 'True' Histograms}{#font[22]{Unfold_RooUnfold_Response} and #color[", str(root_color.Blue), "]{RooUnfoldExample.py}}"]))
Unfold_RooUnfold_Htruth.SetLineColor(root_color.Black)
Unfold_RooUnfold_Htruth.Draw("hist same E0")
Unfold_Test_Htruth.SetLineColor(root_color.Blue)
Unfold_Test_Htruth.Draw("hist same E0")

canvas_Res_lower.cd(4)
MC_Gen.SetTitle("".join(["#splitline{1D Histogram Inputs}{#color[", str(root_color.Green), "]{MC GEN} and #color[", str(root_color.Red), "]{MC REC}}"]))
MC_Rec.SetTitle("".join(["#splitline{1D Histogram Inputs}{#color[", str(root_color.Green), "]{MC GEN} and #color[", str(root_color.Red), "]{MC REC}}"]))
MC_Gen.SetLineColor(root_color.Green)
MC_Gen.Draw("hist same E0")
MC_Rec.SetLineColor(root_color.Red)
MC_Rec.Draw("hist same E0")


canvas_Res.SaveAs("RooUnfold_Response_Test_NEW_Phi_Mod_6.pdf")









#                 MC_GEN_1D = TH1D("MC_Generated",     "MC True",          nBins, MinBin, MaxBin)
#                 MC_REC_1D = TH1D("MC_Reconstructed", "MC Reconstructed", nBins, MinBin, MaxBin)
#                 Response_RooUnfold = ROOT.RooUnfoldResponse(nBins, MinBin, MaxBin)

#                 # Loop over your (generated) simulated events where:
#                 #     gen = "your generated variable's value"
#                 #     rec = "the reconstructed variable's value" 
#                 #     (rec is obtained after your 'gen' value has been smeared/passed through the detector's simulation)

#                     MC_GEN_1D.Fill(gen)
#                     if(rec != None):
#                         # i.e. if the generated event is detected after passing through the detector so that rec has a value
#                         Response_RooUnfold.Fill(rec, gen)
#                         MC_REC_1D.Fill(rec)
#                     else:
#                         Response_RooUnfold.Miss(gen)
#                         # i.e. the generated event was not detected after passing through the detector

                    
                    
                    
                    
#                 Response_RooUnfold = ROOT.RooUnfoldResponse(nBins, MinBin, MaxBin)
#                 for gen_bin in range(0, nBins + 1, 1):
#                     sum_of_gen = 0
#                     # 'sum_of_gen' counts the number of generated events that were also reconstructed
#                     gen        = Response_2D.GetXaxis().GetBinCenter(gen_bin)
#                     # In my TH2D histogram, the generated events are stored along the x-axis
#                     for rec_bin in range(0, nBins + 1, 1):
#                         rec     = Response_2D.GetYaxis().GetBinCenter(rec_bin)
#                         # The reconstructed events are stored along the y-axis
#                         Res_Val = Response_2D.GetBinContent(gen_bin,  rec_bin)
#                         # 'Res_Val' gives the total number of events in the response matrix for the given (gen_bin) vs (rec_bin) bin
#                         sum_of_gen += Res_Val
#                         Response_RooUnfold.Fill(rec, gen, w=Res_Val)
#                     gen_val_TRUE = MC_GEN_1D.GetBinContent(gen_bin)
#                     # 'gen_val_TRUE' counts the total number of generated events (regardless of reconstruction)
#                     if((gen_val_TRUE >= sum_of_gen) and (gen == MC_GEN_1D.GetBinCenter(gen_bin))):
#                         gen_val_MISSED = gen_val_TRUE - sum_of_gen
#                         Response_RooUnfold.Miss(gen, w=gen_val_MISSED)
#                     else:
#                         print("ERROR MESSAGE: More generated events are matched to reconstructed events than should exist in total")

                        
                        
                        
                     
# if(method   == "bayes"):
#     unfold   = ROOT.RooUnfoldBayes(response,    hMeas, 4);  #  OR
# elif(method == "svd"):
#     unfold   = ROOT.RooUnfoldSvd(response,      hMeas, 20); #  OR
# elif(method == "bbb"):
#     unfold   = ROOT.RooUnfoldBinByBin(response, hMeas);     #  OR  
# elif(method == "inv"):
#     unfold   = ROOT.RooUnfoldInvert(response,   hMeas);     #  OR  
# elif(method == "root"):
#     unfold   = ROOT.RooUnfoldTUnfold(response,  hMeas);     #  OR
# elif(method == "ids"):
#     unfold   = ROOT.RooUnfoldIds(response,      hMeas, 3);
# hUnfold = unfold.Hunfold();




#                 if(Method   == "Bayesian"):
#                     bayes_iterations = 10
#                     Unfolding_Histo =    ROOT.RooUnfoldBayes(Response_RooUnfold, ExREAL_1D, bayes_iterations)
#                 elif(Method == "SVD"):
#                     Regularization_Parameter = 13
#                     Unfolding_Histo =      ROOT.RooUnfoldSvd(Response_RooUnfold, ExREAL_1D, Regularization_Parameter)
#                 elif(Method == "Bin-by-bin"):
#                     Unfolding_Histo = ROOT.RooUnfoldBinByBin(Response_RooUnfold, ExREAL_1D)
#                 elif(Method == "Invert"):
#                     Unfolding_Histo =   ROOT.RooUnfoldInvert(Response_RooUnfold, ExREAL_1D)
#                 elif(Method == "TUnfold"):
#                     Unfolding_Histo =  ROOT.RooUnfoldTUnfold(Response_RooUnfold, ExREAL_1D)
#                 elif(Method == "IDS"):
#                     Unfolding_Histo =      ROOT.RooUnfoldIds(Response_RooUnfold, ExREAL_1D, 3)
#                 Unfolded_Histo = Unfolding_Histo.Hunfold()
                
                
                
                
                
                