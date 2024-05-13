#!/usr/bin/env python

import ROOT
from MyCommonAnalysisFunction_richcap import *
from Convert_MultiDim_Kinematic_Bins  import *

import traceback

Closure_Test = False
Sim_Test = False

############################################################################################################################################################
##==========##==========##     Unfolding Fit Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
############################################################################################################################################################

    
def Full_Calc_Fit(Histo, version="norm"):
    
    # Helping the closure tests with known values of B and C
    if(Closure_Test):
        B, C = -0.500, 0.025
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A    = (Histo_max_bin_num)/((1 + B*ROOT.cos(Histo_max_bin_phi) + C*ROOT.cos(2*Histo_max_bin_phi)))
    elif(Sim_Test):
        B, C = 0, 0
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A    = (Histo_max_bin_num)/((1 + B*ROOT.cos(Histo_max_bin_phi) + C*ROOT.cos(2*Histo_max_bin_phi)))
        
    else:
        Histo_180_bin = Histo.FindBin(155)
        Histo_240_bin = Histo.FindBin(300)
        Histo_max_bin = Histo.GetMaximumBin()
        if(Histo_max_bin == Histo_180_bin or Histo_max_bin == Histo_240_bin):
            # print("".join([color.RED, "(Minor) Error in 'Full_Calc_Fit': Same bin used in fits", color.END]))
            Histo_max_bin = Histo.FindBin(100)
        Histo_180_bin_y = Histo.GetBinContent(Histo_180_bin)
        Histo_240_bin_y = Histo.GetBinContent(Histo_240_bin)
        Histo_max_bin_y = Histo.GetBinContent(Histo_max_bin)
        Histo_180_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_180_bin)
        Histo_240_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_240_bin)
        Histo_max_bin_x = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_180_bin_Cos_phi   = ROOT.cos(Histo_180_bin_x)
        Histo_240_bin_Cos_phi   = ROOT.cos(Histo_240_bin_x)
        Histo_max_bin_Cos_phi   = ROOT.cos(Histo_max_bin_x)
        Histo_180_bin_Cos_2_phi = ROOT.cos(2*Histo_180_bin_x)
        Histo_240_bin_Cos_2_phi = ROOT.cos(2*Histo_240_bin_x)
        Histo_max_bin_Cos_2_phi = ROOT.cos(2*Histo_max_bin_x)
        numerator   = (Histo_180_bin_y*Histo_240_bin_Cos_phi*Histo_max_bin_Cos_2_phi) - (Histo_180_bin_Cos_phi*Histo_240_bin_y*Histo_max_bin_Cos_2_phi) - (Histo_180_bin_y*Histo_240_bin_Cos_2_phi*Histo_max_bin_Cos_phi) + (Histo_180_bin_Cos_2_phi*Histo_240_bin_y*Histo_max_bin_Cos_phi) + (Histo_180_bin_Cos_phi*Histo_240_bin_Cos_2_phi*Histo_max_bin_y) - (Histo_180_bin_Cos_2_phi*Histo_240_bin_Cos_phi*Histo_max_bin_y)
        denominator = (Histo_180_bin_Cos_phi*Histo_240_bin_Cos_2_phi)                 - (Histo_180_bin_Cos_2_phi*Histo_240_bin_Cos_phi)                 - (Histo_180_bin_Cos_phi*Histo_max_bin_Cos_2_phi)                 + (Histo_240_bin_Cos_phi*Histo_max_bin_Cos_2_phi)                 + (Histo_180_bin_Cos_2_phi*Histo_max_bin_Cos_phi)                 - (Histo_240_bin_Cos_2_phi*Histo_max_bin_Cos_phi)
        try:
            A = numerator/denominator
            # A = 0.025
            B = -0.2*A
            C = -0.1*A
            # C = ((Histo_240_bin_x - A) + (Histo_180_bin_x - A)*(Histo_240_bin_Cos_phi/Histo_180_bin_Cos_phi))/((Histo_240_bin_Cos_2_phi + (Histo_180_bin_Cos_2_phi*Histo_240_bin_Cos_phi)/Histo_180_bin_Cos_phi))
            # B = (Histo_max_bin - A - C*Histo_max_bin_Cos_2_phi)/(Histo_max_bin_Cos_phi)
        except:
            print("".join([color.Error, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
            A, B, C = "Error", "Error", "Error"

        try:
            Phi_low_bin = Histo.FindBin(157.5)
            Phi_mid_bin = Histo.FindBin(202.5)

            Phi_low_bin = Histo.FindBin(155)
            Phi_mid_bin = Histo.FindBin(300)

            # Phi_max_bin = Histo.FindBin(262.5)
            Phi_max_bin = Histo.GetMaximumBin()

            if(Phi_max_bin in [Phi_low_bin, Phi_mid_bin, Phi_low_bin - 1, Phi_mid_bin - 1, Phi_low_bin - 2, Phi_mid_bin - 2, Phi_low_bin + 1, Phi_mid_bin + 1, Phi_low_bin + 2, Phi_mid_bin + 2]):
                print("".join([color.RED, "(Minor) Error in 'Full_Calc_Fit': Same bin used in fits", color.END]))
                # Phi_max_bin = Histo.FindBin(187.5)
                Phi_max_bin = Histo.FindBin(262.5)

            Phi_low = (3.1415926/180)*Histo.GetBinCenter(Phi_low_bin)
            Phi_mid = (3.1415926/180)*Histo.GetBinCenter(Phi_mid_bin)
            Phi_max = (3.1415926/180)*Histo.GetBinCenter(Phi_max_bin)

            n2 = Histo.GetBinContent(Phi_max_bin)
            a2 = ROOT.cos(Phi_max)                # Cos_phi_max
            b2 = ROOT.cos(2*Phi_max)              # Cos_2_phi_max

            if(0 not in [ROOT.cos(Phi_max), ROOT.cos(2*Phi_max)]):
                n2 = Histo.GetBinContent(Phi_max_bin)
                a2 = ROOT.cos(Phi_max)            # Cos_phi_max
                b2 = ROOT.cos(2*Phi_max)          # Cos_2_phi_max
            elif(Phi_max_bin != Histo.FindBin(187.5)):
                print("".join([color.RED, "(Minor) Error in 'Full_Calc_Fit': Phi_max gives divide by 0 error", color.END]))
                Phi_max_bin = Histo.FindBin(187.5)
                Phi_max     = (3.1415926/180)*Histo.GetBinCenter(Phi_max_bin)
                n2 = Histo.GetBinContent(Phi_max_bin)
                a2 = ROOT.cos(Phi_max)            # Cos_phi_max
                b2 = ROOT.cos(2*Phi_max)          # Cos_2_phi_max

            if(0 in [ROOT.cos(Phi_max), ROOT.cos(2*Phi_max)]):
                print(color.Error, "POTENTIAL RISK OF DIVIDE BY 0 ERROR FOR Phi_max_bin =", Phi_max_bin, color.END)
                Phi_max_bin = Histo.FindBin(100 if(Phi_max_bin != Histo.FindBin(100)) else 247.5)
                Phi_max     = (3.1415926/180)*Histo.GetBinCenter(Phi_max_bin)
                n2 = Histo.GetBinContent(Phi_max_bin)
                a2 = ROOT.cos(Phi_max)            # Cos_phi_max
                b2 = ROOT.cos(2*Phi_max)          # Cos_2_phi_max

            n0 = Histo.GetBinContent(Phi_low_bin)
            n1 = Histo.GetBinContent(Phi_mid_bin)

            a0 = ROOT.cos(Phi_low)                # Cos_phi_low
            a1 = ROOT.cos(Phi_mid)                # Cos_phi_mid

            b0 = ROOT.cos(2*Phi_low)              # Cos_2_phi_low
            b1 = ROOT.cos(2*Phi_mid)              # Cos_2_phi_mid

            numerator_A   = a0*(b2*n1 - b1*n2) + b0*(a1*n2 - a2*n1) - n0*(a1*b2 - a2*b1)
            denominator_A = a0*(b2    - b1)    + b0*(a1    - a2)    -     a1*b2 + a2*b1

            numerator_B   = b0*(n1    -    n2) + b1*(n2    - n0)    + b2*(n0    - n1)
            denominator_B = a0*(b2*n1 - b1*n2) + b0*(a1*n2 - a2*n0) + n0*(a2*b1 - a1*b2)

            numerator_C   = a0*(n1    -    n2) + a1*(n2    - n0)    + a2*(n0    - n1)
            denominator_C = a0*(b1*n2 - b2*n1) + b0*(a2*n1 - a1*n2) + n0*(a1*b2 - a2*b1)

            if(denominator_A != 0):
                A = numerator_A/denominator_A
            else:
                print(color.RED, "\nError A - Divide by 0\n", color.END)
                A = n2/(1 + (numerator_B/denominator_B)*a2 + (numerator_C/denominator_C)*b2)

            if(denominator_B != 0):
                B = numerator_B/denominator_B
            else:
                print(color.RED, "\nError B - Divide by 0\n", color.END)
                print("a2 =", a2)
                print("A  =", A)
                print("denominator_C =", denominator_C)
                B = (1/a2)*((n2/A) - (numerator_C/denominator_C)*b2 - 1)

            if(denominator_C != 0):
                C = numerator_C/denominator_C
            else:
                print(color.RED, "\nError C - Divide by 0\n", color.END)
                C = (1/b2)*((n2/A) - B*a2 - 1)
        except:
            print("".join([color.Error, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
            print(color.Error, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)
            A, B, C = "Error", "Error", "Error"
        return [A, B, C]

############################################################################################################################################################
##==========##==========##     Unfolding Fit Function     ##==========##==========##==========##==========##==========##==========##==========##==========##
############################################################################################################################################################


###############################################################################################################################################################
##==========##==========##     Unfolding Fit Function V2     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################

# from scipy.optimize import curve_fit

# def func_fit(x, A, B, C):
#     return (A*(1 + B*(ROOT.cos(x)) + C*(ROOT.cos(2*x))))

from functools import partial

def func_fit(params, x, y):
    A, B, C = params
    y_pred = [A*(1 + B*(ROOT.cos(xi)) + C*(ROOT.cos(2*xi))) for xi in x]
    return sum((y_pred[i] - y[i])**2 for i in range(len(x)))

def nelder_mead(func, x0, args=(), max_iter=1000, tol=1e-6):
    N = len(x0)
    simplex = [x0]
    for i in range(N):
        point = list(x0)
        point[i] = x0[i] + 1.0
        simplex.append(point)
    
    for _ in range(max_iter):
        simplex.sort(key=lambda point: func(point, *args))
        if abs(func(simplex[0], *args) - func(simplex[-1], *args)) < tol:
            break
        centroid = [sum(simplex[i][j] for i in range(N)) / N for j in range(N)]
        reflected = [centroid[j] + (centroid[j] - simplex[-1][j]) for j in range(N)]
        if func(simplex[0], *args) <= func(reflected, *args) < func(simplex[-2], *args):
            simplex[-1] = reflected
            continue
        if func(reflected, *args) < func(simplex[0], *args):
            expanded = [centroid[j] + 2.0 * (centroid[j] - simplex[-1][j]) for j in range(N)]
            if func(expanded, *args) < func(reflected, *args):
                simplex[-1] = expanded
            else:
                simplex[-1] = reflected
            continue
        contracted = [centroid[j] + 0.5 * (simplex[-1][j] - centroid[j]) for j in range(N)]
        if func(contracted, *args) < func(simplex[-1], *args):
            simplex[-1] = contracted
            continue
        for i in range(1, N+1):
            simplex[i] = [simplex[0][j] + 0.5 * (simplex[i][j] - simplex[0][j]) for j in range(N)]
    
    return simplex[0]

def Full_Calc_Fit(Histo):
    # Helping the closure tests with known values of B and C
    if(Closure_Test):
        B_opt, C_opt = -0.500, 0.025
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A_opt    = (Histo_max_bin_num)/((1 + B_opt*ROOT.cos(Histo_max_bin_phi) + C_opt*ROOT.cos(2*Histo_max_bin_phi)))
    elif(Sim_Test):
        B_opt, C_opt = 0, 0
        Histo_max_bin     = Histo.GetMaximumBin()
        Histo_max_bin_phi = (3.1415926/180)*Histo.GetBinCenter(Histo_max_bin)
        Histo_max_bin_num = Histo.GetBinContent(Histo_max_bin)
        A_opt    = (Histo_max_bin_num)/((1 + B_opt*ROOT.cos(Histo_max_bin_phi) + C_opt*ROOT.cos(2*Histo_max_bin_phi)))
    else:
        x_data, y_data = [], []
        try:
            # print("Histo.GetNbinsX() =", Histo.GetNbinsX())
            for ii in range(0, Histo.GetNbinsX(), 1):
    #             x_data.append((3.1415926/180)*(Histo.GetBinCenter(ii)))
                x_data.append(Histo.GetBinCenter(ii))
                y_data.append(Histo.GetBinContent(ii))

    #         # Perform curve fitting
    #         popt, pcov = curve_fit(func_fit, x_data, y_data)
    #         # Extract the optimized parameters
    #         A_opt, B_opt, C_opt = popt

            # Perform optimization using the Nelder-Mead method
            initial_guess = [1e6, 1, 1]  # Initial guess for A, B, C
            optim_params = nelder_mead(partial(func_fit, x=x_data, y=y_data), initial_guess)

            # Extract the optimized parameters
            A_opt, B_opt, C_opt = optim_params

        except:
            print("".join([color.Error, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))

            print(color.Error, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)

            A_opt, B_opt, C_opt = "Error", "Error", "Error"
        
    return [A_opt, B_opt, C_opt]



extra_function_terms = False
# extra_function_terms = True

if(extra_function_terms):
    # def func_fit(params, x, y):
    #     A, B, C, D, E = params
    #     y_pred = [A*(1 + B*(ROOT.cos(xi)) + C*(ROOT.cos(2*xi)) + D*(ROOT.cos(3*xi)) + E*(ROOT.cos(4*xi))) for xi in x]
    #     return sum((y_pred[i] - y[i])**2 for i in range(len(x)))
    def func_fit(params, x, y):
        A, B, C, D = params
        y_pred = [A*(1 + B*(ROOT.cos(xi)) + C*(ROOT.cos(2*xi)) + D*(ROOT.cos(3*xi))) for xi in x]
        return sum((y_pred[i] - y[i])**2 for i in range(len(x)))

    def nelder_mead(func, x0, args=(), max_iter=1000, tol=1e-6):
        N = len(x0)
        simplex = [x0]
        for i in range(N):
            point = list(x0)
            point[i] = x0[i] + 1.0
            simplex.append(point)

        for _ in range(max_iter):
            simplex.sort(key=lambda point: func(point, *args))
            if abs(func(simplex[0], *args) - func(simplex[-1], *args)) < tol:
                break
            centroid = [sum(simplex[i][j] for i in range(N)) / N for j in range(N)]
            reflected = [centroid[j] + (centroid[j] - simplex[-1][j]) for j in range(N)]
            if func(simplex[0], *args) <= func(reflected, *args) < func(simplex[-2], *args):
                simplex[-1] = reflected
                continue
            if func(reflected, *args) < func(simplex[0], *args):
                expanded = [centroid[j] + 2.0 * (centroid[j] - simplex[-1][j]) for j in range(N)]
                if func(expanded, *args) < func(reflected, *args):
                    simplex[-1] = expanded
                else:
                    simplex[-1] = reflected
                continue
            contracted = [centroid[j] + 0.5 * (simplex[-1][j] - centroid[j]) for j in range(N)]
            if func(contracted, *args) < func(simplex[-1], *args):
                simplex[-1] = contracted
                continue
            for i in range(1, N+1):
                simplex[i] = [simplex[0][j] + 0.5 * (simplex[i][j] - simplex[0][j]) for j in range(N)]

        return simplex[0]

    
    def Full_Calc_Fit(Histo):
        x_data, y_data = [], []
        try:
            # print("Histo.GetNbinsX() =", Histo.GetNbinsX())
            for ii in range(0, Histo.GetNbinsX(), 1):
                x_data.append(Histo.GetBinCenter(ii))
                y_data.append(Histo.GetBinContent(ii))
            # Perform optimization using the Nelder-Mead method
            initial_guess = [1e6, 1, 1, 1]  # Initial guess for A, B, C, D
            optim_params = nelder_mead(partial(func_fit, x=x_data, y=y_data), initial_guess)
            # Extract the optimized parameters
            A_opt, B_opt, C_opt, D_opt = optim_params
        except:
            print("".join([color.Error, "Full_Calc_Fit(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
            print(color.Error, "\nERROR is with 'Histo'=", str(Histo), "\n", color.END)
            A_opt, B_opt, C_opt, D_opt = "Error", "Error", "Error", "Error"
        return [A_opt, B_opt, C_opt, D_opt]

###############################################################################################################################################################
##==========##==========##     Unfolding Fit Function V2     ##==========##==========##==========##==========##==========##==========##==========##==========##
###############################################################################################################################################################



######################################################################################################################################################################################################################################
##==========##==========##     Function For Naming (New) Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################################################################################################

import re
def Histogram_Name_Def(out_print, Histo_General="Find", Data_Type="Find", Cut_Type="Find", Smear_Type="Find", Q2_y_Bin="All", z_pT_Bin="All", Bin_Extra="Default", Variable="Default"):
    Pattern_List = []
    Pattern_Histo_General = r"\(Histo-Group='([^']+)'"
    Pattern_Data_Type     = r"\(Data-Type='([^']+)'"
    Pattern_Cut_Type      = r"\(Data-Cut='([^']+)'"
    Pattern_Smear_Type    = r"\(Smear-Type='([^']+)'"
    Pattern_Q2_y_Bin      = r"\[Q2-y-Bin=([^,]+),"
    Pattern_Var_1         = r"\(Var-D1='([^']+)'"
    Pattern_Var_2         = r"\(Var-D2='([^']+)'"
    # Pattern_Var_3         = r"\(Var-D3='([^']+)'"
    
    if(Histo_General  == "Find"):
        Pattern_List.append(Pattern_Histo_General)
    else:
        Pattern_List.append(Histo_General)
    if(Data_Type      == "Find"):
        Pattern_List.append(Pattern_Data_Type)
    else:
        Pattern_List.append(Data_Type)
    if(Cut_Type       == "Find"):
        Pattern_List.append(Pattern_Cut_Type)
    elif(Cut_Type not in ["Skip", "skip"]):
        Pattern_List.append(Cut_Type)
    if(Smear_Type     == "Find"):
        Pattern_List.append(Pattern_Smear_Type)
    else:
        Pattern_List.append(Smear_Type)
        

    if(Bin_Extra      == "Default"):
        Pattern_List.append(str("".join(["Q2_y_Bin_", str(Q2_y_Bin) if(Q2_y_Bin != 0) else "All"])) if(Q2_y_Bin not in ["Find"]) else Pattern_Q2_y_Bin)
        Pattern_List.append("".join(["z_pT_Bin_", str(z_pT_Bin) if(z_pT_Bin != 0) else "All"]))
    elif(Bin_Extra not in ["Skip", "skip"]):
        Pattern_List.append("".join(["Kinematic_Bin_", str(Bin_Extra) if(Bin_Extra != 0) else "All"]))
        
    if(Variable       == "Default"):
        Pattern_List.append(Pattern_Var_1)
        if("2D" in str(out_print) or "3D" in str(out_print)):
            Pattern_List.append(Pattern_Var_2)
            # Pattern_List.append(Pattern_Var_3)
    elif(Variable     in ["Find", "FindAll", "FindOnly"]):
        Pattern_List = [Pattern_Var_1]
        if("2D" in str(out_print) or "3D" in str(out_print)):
            Pattern_List.append(Pattern_Var_2)
            # Pattern_List.append(Pattern_Var_3)
    else:
        Pattern_List.append(Variable)
        
    if(Q2_y_Bin in ["FindOnly"]):
        Pattern_List = [Pattern_Q2_y_Bin]
        
    Name_Output = ""
    
    for pattern in Pattern_List:
        if(pattern in [r"\(Histo-Group='([^']+)'", r"\(Data-Type='([^']+)'", r"\(Data-Cut='([^']+)'", r"\(Smear-Type='([^']+)'", r"\[Q2-y-Bin=([^,]+),", r"\(Var-D1='([^']+)'", r"\(Var-D2='([^']+)'"]):
            match = re.search(pattern, out_print.replace("''", "' '"))
            if(match):
                histo_group = match.group(1)
                if((histo_group == " ")):
                    histo_group = "''"
                if(pattern == Pattern_Smear_Type):
                    histo_group = "".join(["SMEAR=", "".join(["'", str(histo_group), "'"]) if(histo_group != "''") else str(histo_group)]) 
                if(pattern == Pattern_Q2_y_Bin):
                    histo_group = "".join(["Q2_y_Bin_", str(histo_group)]) 
        else:
            histo_group = pattern
            if(pattern == Smear_Type):
                histo_group = "".join(["SMEAR=", pattern if(pattern != "") else "''"])
        Name_Output = "".join([Name_Output, "_(" if(str(Name_Output) != "") else "(", str(histo_group), ")"])
        # if(("rdf" in str(Name_Output)) or ("gdf" in str(Name_Output))):
        #     Name_Output = Name_Output.replace("Smear", "''")
        
    if((Variable in ["Find", "FindAll", "FindOnly"]) and (")_(" not in str(Name_Output))):
        Name_Output = Name_Output.replace("(", "")
        Name_Output = Name_Output.replace(")", "")
    
    return Name_Output

######################################################################################################################################################################################################################################
##==========##==========##     Function For Naming (New) Histograms     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Fitting_Phi_Function(Histo_To_Fit, Method="FIT", Fitting="default", Special="Normal"):
    if((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bay", "bayes", "bayesian", "Bayesian", "FIT", "SVD", "tdf", "true"]) and (Fitting in ["default", "Default"]) and Fit_Test):
        # if(Method in ["bayes", "bayesian", "Bayesian"]):
        #     print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nSpecial =", str(Special), "\nMethod =", str(Method), "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if(not extra_function_terms):
            A_Unfold, B_Unfold, C_Unfold = Full_Calc_Fit(Histo_To_Fit)
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)))"
        else:
            # A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold = Full_Calc_Fit(Histo_To_Fit)
            # fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)) + [E]*cos(4*x*(3.1415926/180)))"
            A_Unfold, B_Unfold, C_Unfold, D_Unfold = Full_Calc_Fit(Histo_To_Fit)
            fit_function = "[A]*(1 + [B]*cos(x*(3.1415926/180)) + [C]*cos(2*x*(3.1415926/180)) + [D]*cos(3*x*(3.1415926/180)))"
            
        Fitting_Function = ROOT.TF1("".join(["Fitting_Function", str(Method).replace(" ", "_")]), str(fit_function), 0, 360)
        # Fitting_Function.SetParName(0, "Parameter A")
        # Fitting_Function.SetParName(1, "Parameter B")
        # Fitting_Function.SetParName(2, "Parameter C")
        
        # if(not extra_function_terms):
        #     print(color.BBLUE, "A_Unfold, B_Unfold, C_Unfold =", color.END_B, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold)]), color.END)
        # else:
        if(extra_function_terms):
            # print(color.BBLUE, "A_Unfold, B_Unfold, C_Unfold, D_Unfold, E_Unfold =", color.END_B, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold), str(D_Unfold), str(E_Unfold)]), color.END)
            print(color.BBLUE, "A_Unfold, B_Unfold, C_Unfold, D_Unfold =", color.END_B, ", ".join([str(A_Unfold), str(B_Unfold), str(C_Unfold), str(D_Unfold)]), color.END)
            Fitting_Function.SetParName(3, "Parameter D")
            # Fitting_Function.SetParName(4, "Parameter E")
            
            
        fit_range_lower = 0
        fit_range_upper = 360
        # Number of bins in the histogram
        n_bins = Histo_To_Fit.GetNbinsX()
        
        # Find the lower fit range (first non-empty bin)
        for bin_lower in range(1, n_bins // 2 + 1):  # Search from the start to the center
            if(Histo_To_Fit.GetBinContent(bin_lower) != 0):
                fit_range_lower = Histo_To_Fit.GetXaxis().GetBinLowEdge(bin_lower)
                break  # Stop the loop once the first non-empty bin is found

        # Find the upper fit range (last non-empty bin)
        for bin_upper in range(n_bins, n_bins // 2, -1):  # Search from the end towards the center
            if(Histo_To_Fit.GetBinContent(bin_upper) != 0):
                fit_range_upper = Histo_To_Fit.GetXaxis().GetBinUpEdge(bin_upper)
                break  # Stop the loop once the last non-empty bin is found
        
        Fitting_Function.SetRange(fit_range_lower, fit_range_upper)
        
        Fitting_Function.SetLineColor(2)
        if(Special in ["Normal"]):
            if(Method in ["rdf", "Experimental"]):
                Fitting_Function.SetLineColor(root_color.Blue)
            if(Method in ["mdf", "MC REC"]):
                Fitting_Function.SetLineColor(root_color.Red)
            if(Method in ["gdf", "gen", "MC GEN"]):
                Fitting_Function.SetLineColor(root_color.Green)
            if(Method in ["tdf", "true"]):
                Fitting_Function.SetLineColor(root_color.Cyan)
            if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                Fitting_Function.SetLineColor(root_color.Brown)
            if(Method in ["bayes", "bayesian", "Bayesian", "bay"]):
                Fitting_Function.SetLineColor(root_color.Teal)
            if(Method in ["SVD"]):
                Fitting_Function.SetLineColor(root_color.Pink)
        
        Allow_Multiple_Fits   = True
        Allow_Multiple_Fits_C = True
        
        try:
            if("Error" not in [A_Unfold, B_Unfold, C_Unfold] or False):
                # This is the constant scaling factor - A (should basically always be positive)
                Fitting_Function.SetParameter(0,      abs(A_Unfold))
                # Fitting_Function.SetParLimits(0, 0.95*abs(A_Unfold), 1.05*abs(A_Unfold))
                Fitting_Function.SetParLimits(0, 0.05*abs(A_Unfold), 5.5*abs(A_Unfold))

                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                # Fitting_Function.SetParLimits(1, B_Unfold - 0.05*abs(B_Unfold), B_Unfold + 0.05*abs(B_Unfold))
                Fitting_Function.SetParLimits(1, B_Unfold - 5.5*abs(B_Unfold), B_Unfold + 5.5*abs(B_Unfold))

                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                # Fitting_Function.SetParLimits(2, C_Unfold - 0.05*abs(C_Unfold), C_Unfold + 0.05*abs(C_Unfold))
                Fitting_Function.SetParLimits(2, C_Unfold - 5.5*abs(C_Unfold), C_Unfold + 5.5*abs(C_Unfold))

                if(extra_function_terms):
                    try:
                        Fitting_Function.SetParameter(3, D_Unfold)
                        Fitting_Function.SetParLimits(3, D_Unfold - 5.5*abs(D_Unfold), D_Unfold + 5.5*abs(D_Unfold))

                        # Fitting_Function.SetParameter(4, E_Unfold)
                        # Fitting_Function.SetParLimits(4, E_Unfold - 5.5*abs(E_Unfold), E_Unfold + 5.5*abs(E_Unfold))
                    except:
                        print("".join([color.Error, "Fitting_Function ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
                        
                if((str(Special) not in ["Normal"]) and (str(type(Special)) not in [str(type("Normal"))]) and (not Closure_Test)):
                    try:
                        Q2_y_Bin_Special, z_pT_Bin_Special = Special
                        if(Method in ["bayes", "bayesian", "Bayesian", "bay", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                        # if(Method in ["bayes", "bayesian", "Bayesian"]):
                            if((str(Q2_y_Bin_Special) in ["5"]) and ("Pass_2" not in Common_Name)):
                                # print("\n\n\n\nAPPLYING SPECIAL PARAMETERS FOR:\nQ2_y_Bin_Special =", str(Q2_y_Bin_Special), "\nz_pT_Bin_Special =", str(z_pT_Bin_Special), "\n\n\n")
                                if(str(z_pT_Bin_Special) in ["26", "32"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.08)
                                    Fitting_Function.SetParLimits(1, -0.10, -0.065)
                                    Allow_Multiple_Fits = False
                                if(str(z_pT_Bin_Special) in ["8"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.07)
                                    Fitting_Function.SetParLimits(1, -0.08, -0.06)
                                    Allow_Multiple_Fits = False
                                if(str(z_pT_Bin_Special) in ["14"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.085)
                                    Fitting_Function.SetParLimits(1, -0.125, -0.05)
                                    
                                if(str(z_pT_Bin_Special) in ["9"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.10)
                                    Fitting_Function.SetParLimits(1, -0.145, -0.065)
                                    Allow_Multiple_Fits = False
                                    
                                if(str(z_pT_Bin_Special) in ["23"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.25)
                                    Fitting_Function.SetParLimits(1, -0.3, -0.16)
                                    # Allow_Multiple_Fits = False
                                    
                                   
                                # Just Cos(2*phi) Moments - C
                                if(str(z_pT_Bin_Special) in ["1", "7", "13", "19", "25", "31"]):
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.025)
                                    # Fitting_Function.SetParLimits(2, -0.06, 0)
                                    Fitting_Function.SetParLimits(2, -0.06, -0.01)
                                    Allow_Multiple_Fits_C = False
                                if(str(z_pT_Bin_Special) in ["2", "8", "14", "20", "26", "32"]):
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.02 if(str(z_pT_Bin_Special) not in ["2"]) else 0.01)
                                    if(str(z_pT_Bin_Special) in ["2", "8"]):
                                        Fitting_Function.SetParLimits(2, -0.01, 0.05)                                        
                                    else:
                                        Fitting_Function.SetParLimits(2, -0.04, 0.02)
                                    Allow_Multiple_Fits_C = False
                                if(str(z_pT_Bin_Special) in ["3", "9", "15", "21", "27", "33"]):
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.01)
                                    # Fitting_Function.SetParLimits(2, -0.03, 0.03)
                                    Fitting_Function.SetParLimits(2, -0.03, 0.01)
                                    Allow_Multiple_Fits_C = False
                                if(str(z_pT_Bin_Special) in ["4"]):
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0)
                                    # Fitting_Function.SetParLimits(2, -0.01, 0.025)
                                    Fitting_Function.SetParLimits(2, -0.01, 0.01)
                                    Allow_Multiple_Fits_C = False
                                    
                                    
                                if(str(z_pT_Bin_Special) in ["2"]):
                                    # Cos(phi) Moment - B
                                    # Fitting_Function.SetParameter(1, -0.1062)
                                    # # Fitting_Function.SetParLimits(1, -0.1062   - 0.005,    -0.1062 + 0.005)
                                    # Fitting_Function.SetParLimits(1, -0.125, -0.05)
                                    Fitting_Function.SetParameter(1, -0.1)
                                    Fitting_Function.SetParLimits(1, -0.105, -0.08)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.01945)
                                    Fitting_Function.SetParLimits(2, 0.01945   - 0.06,     0.01945 + 0.06)
                                    Allow_Multiple_Fits = False
                                if(str(z_pT_Bin_Special) in ["3"]):
                                    # # Cos(phi) Moment - B
                                    # Fitting_Function.SetParameter(1, -0.2175)
                                    # # Fitting_Function.SetParLimits(1, -0.2175   - 0.05,     -0.2175 + 0.05)
                                    # Fitting_Function.SetParLimits(1, -0.2175   - 0.025,     -0.2175 + 0.025)
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.1375)
                                    Fitting_Function.SetParLimits(1, -0.1, -0.16)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.001952)
                                    Fitting_Function.SetParLimits(2, 0.001952  - 0.003,   0.001952 + 0.003)
                                if(str(z_pT_Bin_Special) in ["4"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.195)
                                    Fitting_Function.SetParLimits(1, -0.18, -0.22)
                                if(str(z_pT_Bin_Special) in ["5"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.24)
                                    Fitting_Function.SetParLimits(1, -0.2, -0.3)
                                if(str(z_pT_Bin_Special) in ["6", "12", "18"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.35)
                                    Fitting_Function.SetParLimits(1, -0.35     - 0.5,        -0.35 + 0.5)
                                if(str(z_pT_Bin_Special) in ["13"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.027)
                                    Fitting_Function.SetParLimits(1, -0.09, 0)
                                if(str(z_pT_Bin_Special) in ["20"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.04262)
                                    # Fitting_Function.SetParLimits(1, -0.04262  - 0.02,    -0.04262 + 0.02)
                                    Fitting_Function.SetParLimits(1, -0.04262  - 0.005,    -0.04262 + 0.01)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.001472)
                                    Fitting_Function.SetParLimits(2, -0.001472 - 0.003,  -0.001472 + 0.003)
                                    
                                    # Fitting_Function.SetRange(30, 330)
                                    
                                if(str(z_pT_Bin_Special) in ["29"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.19)
                                    Fitting_Function.SetParLimits(1, -0.19     - 0.5,        -0.19 + 0.5)
                                if(str(z_pT_Bin_Special) in ["35"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.25)
                                    Fitting_Function.SetParLimits(1, -0.30, -0.175)
                                    Allow_Multiple_Fits = False
                                    
                            elif((str(Q2_y_Bin_Special) in ["5"]) and ("Pass_2" in Common_Name)):
                                # Pass 2 Fits
                                if(str(z_pT_Bin_Special) in ["1", "7", "13", "19", "25", "31"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.11 if(str(z_pT_Bin_Special) in ["1"])       else -0.1)
                                    Fitting_Function.SetParLimits(1, -0.15, 0)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.01 if(str(z_pT_Bin_Special) in ["1"])       else -0.02 if(str(z_pT_Bin_Special) in ["7"]) else -0.03 if(str(z_pT_Bin_Special) in ["13", "19", "25"]) else -0.057)
                                    Fitting_Function.SetParLimits(2, -0.07, 0)
                                if(str(z_pT_Bin_Special) in ["2", "8", "14", "20", "26", "32"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.1)
                                    Fitting_Function.SetParLimits(1, -0.2, 0)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, -0.05 if(str(z_pT_Bin_Special) in ["2"])       else 0.035 if(str(z_pT_Bin_Special) in ["8"])  else -0.03 if(str(z_pT_Bin_Special) in ["26", "32"]) else 0)
                                    Fitting_Function.SetParLimits(2, -0.05, 0.1)
                                if(str(z_pT_Bin_Special) in ["3", "9", "15", "21", "27", "33"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.2  if(str(z_pT_Bin_Special) in ["3"])       else -0.16 if(str(z_pT_Bin_Special) in ["9"])  else -0.135 if(str(z_pT_Bin_Special) in ["15"]) else -0.15 if(str(z_pT_Bin_Special) in ["21"]) else -0.155 if(str(z_pT_Bin_Special) in ["27"]) else -0.145)
                                    Fitting_Function.SetParLimits(1, -0.22, -0.1)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.009 if(str(z_pT_Bin_Special) in ["3"])       else 0.015 if(str(z_pT_Bin_Special) in ["9"])  else -0.005 if(str(z_pT_Bin_Special) in ["15"]) else -0.04 if(str(z_pT_Bin_Special) in ["21"]) else -0.015 if(str(z_pT_Bin_Special) in ["27"]) else -0.007)
                                    Fitting_Function.SetParLimits(2, -0.05, 0.02)
                                if(str(z_pT_Bin_Special) in ["4", "10", "16", "22", "28", "34"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.28 if(str(z_pT_Bin_Special) in ["4"])       else -0.24 if(str(z_pT_Bin_Special) in ["10"]) else -0.21  if(str(z_pT_Bin_Special) in ["16"]) else -0.2  if(str(z_pT_Bin_Special) in ["22"]) else -0.16  if(str(z_pT_Bin_Special) in ["28"]) else -0.18)
                                    Fitting_Function.SetParLimits(1, -0.3, -0.03)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.01  if(str(z_pT_Bin_Special) in ["4", "28"]) else 0.015 if(str(z_pT_Bin_Special) in ["10"]) else -0.025 if(str(z_pT_Bin_Special) in ["16"]) else  0    if(str(z_pT_Bin_Special) in ["22"]) else 0.022)
                                    Fitting_Function.SetParLimits(2, -0.05, 0.035)
                                if(str(z_pT_Bin_Special) in ["5", "11", "17", "23", "29"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.3  if(str(z_pT_Bin_Special) in ["5", "11"]) else -0.26 if(str(z_pT_Bin_Special) in ["17"]) else -0.25  if(str(z_pT_Bin_Special) in ["23"]) else -0.24)
                                    Fitting_Function.SetParLimits(1, -0.35, -0.2)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.01  if(str(z_pT_Bin_Special) in ["5"])       else  0.   if(str(z_pT_Bin_Special) in ["11"]) else  0.022 if(str(z_pT_Bin_Special) in ["17"]) else 0.041 if(str(z_pT_Bin_Special) in ["23"]) else 0.06)
                                    Fitting_Function.SetParLimits(2, -0.03, 0.08)
                                if(str(z_pT_Bin_Special) in ["6", "12", "18"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.4)
                                    Fitting_Function.SetParLimits(1, -0.5, -0.3)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.03 if(str(z_pT_Bin_Special) in ["6"]) else 0.075 if(str(z_pT_Bin_Special) in ["12"]) else 0.1)
                                    Fitting_Function.SetParLimits(2, 0.01, 0.14)
                                
                                
                            if(str(Q2_y_Bin_Special) in ["1"]):
                                if(str(z_pT_Bin_Special) in ["14", "21"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.3)
                                    Fitting_Function.SetParLimits(1, -0.4, -0.275)
                            if(str(Q2_y_Bin_Special) in ["2"]):
                                if(str(z_pT_Bin_Special) in ["7", "14", "21"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.3)
                                    Fitting_Function.SetParLimits(1, -0.4, -0.275)
                                    # Cos(2*phi) Moment - C
                                    Fitting_Function.SetParameter(2, 0.1)
                                    Fitting_Function.SetParLimits(2, 0.06, 0.2)
                            if(str(Q2_y_Bin_Special) in ["10"]):
                                if(str(z_pT_Bin_Special) in ["6", "12", "18", "24"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.275)
                                    Fitting_Function.SetParLimits(1, -0.4, -0.2)
                            if(str(Q2_y_Bin_Special) in ["14"]):
                                if(str(z_pT_Bin_Special) in ["2"]):
                                    # Cos(phi) Moment - B
                                    Fitting_Function.SetParameter(1, -0.1)
                                    Fitting_Function.SetParLimits(1, -0.12, -0.02)
                                if(str(z_pT_Bin_Special) in ["20"]):
                                    # Cos(phi) Moment - B
                                    if("y_bin" in Binning_Method):
                                        Fitting_Function.SetParameter(1, -0.25)
                                        Fitting_Function.SetParLimits(1, -0.3, -0.2)
                                    else:
                                        Fitting_Function.SetParameter(1, -0.02)
                                        Fitting_Function.SetParLimits(1, -0.06, 0)
                                
                                    
                    except:
                        print(color.Error, "\nERROR in Fitting_Phi_Function() for 'Special' arguement...", color.END)
                        print(color.BOLD,  "Traceback:\n", str(traceback.format_exc()), color.END, "\n")

            # else:
            #     print(color.Error, "\nFIXING PARAMETERS FOR TESTING\n", color.END)
            #     Fitting_Function= ROOT.TF1("".join(["Unfolded_Fit_Function_Method_", str(Method).replace(" ", "_")]), "[A]", 0, 360)
            #     # Fitting_Function.SetRange(0, 360)
            #     # This is the constant scaling factor - A
            #     Fitting_Function.SetParameter(0, 0.50*abs(Histo_To_Fit.GetMaximum))
            #     Fitting_Function.SetParLimits(0, 0.45*abs(Histo_To_Fit.GetMaximum), 0.55*abs(Histo_To_Fit.GetMaximum))
            
                # Fitting the plots now
                Histo_To_Fit.Fit(Fitting_Function, "QRB")
            else:
                # Fitting the plots now
                Histo_To_Fit.Fit(Fitting_Function, "QR")

            A_Unfold = Fitting_Function.GetParameter(0)
            B_Unfold = Fitting_Function.GetParameter(1)
            C_Unfold = Fitting_Function.GetParameter(2)
            

            # Re-fitting with the new parameters
            # The constant scaling factor - A
            Fitting_Function.SetParameter(0,     abs(A_Unfold))
            Fitting_Function.SetParLimits(0, 0.5*abs(A_Unfold), 1.5*abs(A_Unfold))
            
            # Allow_Multiple_Fits = True
            if(Allow_Multiple_Fits):
                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - 0.5*abs(B_Unfold), B_Unfold + 0.5*abs(B_Unfold))
            else:
                # Cos(phi) Moment - B
                Fitting_Function.SetParameter(1, B_Unfold)
                Fitting_Function.SetParLimits(1, B_Unfold - Fitting_Function.GetParError(1), B_Unfold + Fitting_Function.GetParError(1))
                
            # Allow_Multiple_Fits_C = True
            if(Allow_Multiple_Fits_C):
                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - 0.5*abs(C_Unfold), C_Unfold + 0.5*abs(C_Unfold))
            else:
                # Cos(2*phi) Moment - C
                Fitting_Function.SetParameter(2, C_Unfold)
                Fitting_Function.SetParLimits(2, C_Unfold - Fitting_Function.GetParError(2), C_Unfold + Fitting_Function.GetParError(2))

            if(extra_function_terms):
                D_Unfold = Fitting_Function.GetParameter(3)
                # E_Unfold = Fitting_Function.GetParameter(4)
                # Cos(3*phi) Moment - D
                Fitting_Function.SetParameter(3, D_Unfold)
                Fitting_Function.SetParLimits(3, D_Unfold - 0.5*abs(D_Unfold), D_Unfold + 0.5*abs(D_Unfold))
                # # Cos(4*phi) Moment - E
                # Fitting_Function.SetParameter(4, E_Unfold)
                # Fitting_Function.SetParLimits(4, E_Unfold - 0.5*abs(E_Unfold), E_Unfold + 0.5*abs(E_Unfold))

            # Re-Fitting the plots
            Histo_To_Fit.Fit(Fitting_Function, "QRB")
            
            A_Unfold       = Fitting_Function.GetParameter(0)
            B_Unfold       = Fitting_Function.GetParameter(1)
            C_Unfold       = Fitting_Function.GetParameter(2)

            A_Unfold_Error = Fitting_Function.GetParError(0)
            B_Unfold_Error = Fitting_Function.GetParError(1)
            C_Unfold_Error = Fitting_Function.GetParError(2)
            
            try:
                Fit_Chisquared = Fitting_Function.GetChisquare()
                Fit_ndf        = Fitting_Function.GetNDF()
            except:
                Fit_Chisquared = "Fit_Chisquared"
                Fit_ndf        = "Fit_ndf"

            Out_Put = [Histo_To_Fit,  Fitting_Function,   [Fit_Chisquared,    Fit_ndf],  [A_Unfold,    A_Unfold_Error],  [B_Unfold,    B_Unfold_Error],  [C_Unfold,    C_Unfold_Error]]
        except:
            print("".join([color.Error, "ERROR IN FITTING:\n", color.END, str(traceback.format_exc()), "\n"]))
            Out_Put = [Histo_To_Fit, "Fitting_Function",  ["Fit_Chisquared", "Fit_ndf"], ["A_Unfold", "A_Unfold_Error"], ["B_Unfold", "B_Unfold_Error"], ["C_Unfold", "C_Unfold_Error"]]
        
        return Out_Put
    else:
        print("\n\n\nERROR WITH Fitting_Phi_Function()\n\t'Method' or 'Fitting' is not selected for proper output...\n\n\n")
        return "ERROR"
    
################################################################################################################################################################################################################################################
##==========##==========##     Fitting Function For Phi Plots                     ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################