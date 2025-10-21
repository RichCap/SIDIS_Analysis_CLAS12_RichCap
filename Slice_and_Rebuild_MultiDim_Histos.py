import ROOT
import traceback
from MyCommonAnalysisFunction_richcap import *
# from Convert_MultiDim_Kinematic_Bins  import *

# Global_Input = "Fail"

# def testing_import(str_input):
#     print(f"str_input = {str_input}\nGlobal_Input = {Global_Input}")

################################################################################################################################################################################################################################################
##==========##==========##           Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def MultiD_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="Multi_Dim_Q2_y_Bin_phi_t", Smear="", Out_Option="Save", Fitting_Input="default", Q2_y_Bin_Select="All", Pass_Version="", Sim_Test=False, Fit_Test=False, extra_function_terms=False):
    if(list is type(Histo)):
        Histo, Histo_Cut = Histo # If the input of Histo is given as a list, the first histogram is considered to be the main one to be sliced. 
                                 # The second one is considered to be the 'rdf' (or 'mdf') histogram used to tell when the edge bins should be cut (i.e., when the bin content of Histo_Cut = 0 --> Not good for acceptance).
    else:
        Histo_Cut = False
            
    Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}, {}
    if(str(Method) not in ["rdf", "gdf"]):
        if(((Smearing_Options in ["both", "no_smear"]) and (Smear in [""])) or ((Smearing_Options in ["both", "smear"]) and ("mear" in str(Smear)))):
            print(color.BLUE, "\nRunning MultiD_Slice(...)\n", color.END)
        else:
            print(color.Error, "\n\nWrong Smearing option for MultiD_Slice(...)\n\n", color.END)
            return "Error"
    elif(Smear in [""]):
        print(color.BLUE, "\nRunning MultiD_Slice(...)\n", color.END)
    else:
        print(color.Error, "\n\nWrong Smearing option for MultiD_Slice(...)\n\n", color.END)
        return "Error"
    
    try:
        Output_Histos, Output_Canvas = {}, {}
        
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("Combined_" not in str(Name) and "Multi_Dim" not in str(Name)):
                print(f"{color.RED}ERROR: WRONG TYPE OF HISTOGRAM\nName = {color.END}{Name}\nMultiD_Slice() should be used on 1D histograms with the 'Combined_' or 'Multi_Dim_' bin variable\n\n")
                return "Error"
            # if(("'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t_smeared'" not in str(Name)) and ("'Multi_Dim_Q2_y_Bin_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_y_Bin_phi_t_smeared'" not in str(Name)) and ("'Multi_Dim_Q2_phi_t" not in str(Name).replace("_smeared", "") and "'Multi_Dim_Q2_phi_t_smeared'" not in str(Name)) and (("'Combined_phi_t_Q2" not in str(Name).replace("_smeared", "") and "'Combined_phi_t_Q2_smeared'" not in str(Name)))):
            #     print("ERROR in MultiD_Slice(): Not set up for other variables (yet)")
            #     print("Name =", Name, "\n\n")
            #     return "Error"

        # if(Variable not in ["Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t", "Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t_smeared", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t_smeared", "Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t_smeared"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t_smeared"]), "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t_smeared", "Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared", "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method), "_smeared"]), "Combined_phi_t_Q2_y_Bin", "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]), "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method), "_smeared"])]):
        if(str(Variable).replace("_smeared", "") not in ["Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "".join(["Multi_Dim_Q2_xB_Bin", str(Binning_Method), "_phi_t"]), "".join(["Multi_Dim_z_pT_Bin", str(Binning_Method), "_phi_t"]), "Multi_Dim_Q2_y_Bin_phi_t", "Multi_Dim_Q2_y_Bin_phi_t", "Combined_phi_t_Q2", "".join(["Combined_phi_t_Q2_xB_Bin", str(Binning_Method)]), "Combined_phi_t_Q2_y_Bin", "".join(["Combined_phi_t_Q2_y_Bin", str(Binning_Method)]), "Multi_Dim_elth_phi_t", "Multi_Dim_pipth_phi_t", "Multi_Dim_elPhi_phi_t", "Multi_Dim_pipPhi_phi_t"]):
            print(f"{color.RED}ERROR in MultiD_Slice(): Not set up for other variables (yet){color.END}\nVariable = {Variable}\n\n")
            return "Error"

        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable,  "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
            
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        Method_Title = ""
        if(Method in ["rdf", "Experimental"]):
            Method_Title = "".join([" #color[", str(root_color.Blue), "]{(Experimental)}" if(not Sim_Test) else "]{(MC REC - Pre-Unfolded)}"])
            if(not Sim_Test):
                Variable = Variable.replace("_smeared", "")
                Smear    = ""
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
            # if((Sim_Test) and ("_smeared" not in str(Variable)) and (Smear in [""])):
            #     Variable = "".join([str(Variable), "_smeared"])
            #     Smear = "Smear"
        if(Method in ["gdf", "gen", "MC GEN"]):
            Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["tdf", "true"]):
            Method_Title = "".join([" #color[", str(root_color.Cyan),  "]{(MC TRUE)}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
            Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
        if(Method in ["bayes", "bayesian", "Bayesian"]):
            Method_Title = "".join([" #color[", str(root_color.Teal),  "]{(Bayesian Unfolded)}"])
        if(Method in ["Acceptance", "Background"]):
            Method_Title = "".join(["(", str(root_color.Bold),          "{", str(Method), "})"])
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###


        if(Title == "Default"):
            Title = str(Histo.GetTitle())
        elif(Title in ["norm", "standard"]):
            Title = "".join(["#splitline{", str(root_color.Bold), "{Multi-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{Multi_Dim_Var_Info}"])
            
            
        if(not extra_function_terms):
            fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        else:
            fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}))"
            
            # fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}) + D Cos(3#phi_{h}) + E Cos(4#phi_{h}))"

        
        if((Method in ["gdf", "gen", "MC GEN", "tdf", "true", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"]) and Fit_Test):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
            
        if((Pass_Version not in [""]) and (Pass_Version not in str(Title))):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{", str(Pass_Version), "}}"])
            
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
            

        #######################################################################
        #####==========#####   Setting Variable Binning    #####==========#####
        #######################################################################
                               # ['min',  'max',   'num_bins', 'size']
        Q2_Binning             = [1.4805, 11.8705, 20,         0.5195]
        Q2_xB_Binning          = [0,      8,       8,          1]
        # Q2_y_Binning         = [0,      18,      18,         1]
        Q2_y_Binning           = [-0.5,   18.5,    19,         1]
        
        z_pT_Binning           = [-0.5,   42.5,    43,         1]
        
        if("Y_bin" in str(Binning_Method)):
            z_pT_Binning       = [-1.5,   50.5,    52,         1]
            z_pT_Binning       = [-0.5,   37.5,    38,         1]
        
        # Q2_y_z_pT_4D_Binning   = [-0.5,   566.5,   567,        1]
        # Q2_y_z_pT_4D_Binning   = [-0.5,   512.5,   513,        1]
        Q2_y_z_pT_4D_Binning   = [-0.5,   506.5,   507,        1]
        
        particle_Th__Binning   = [5,  35, 30,  1]
        particle_Phi_Binning   = [0, 360, 24, 15]
        
        ###==============================================###
        ###========###  Setting Phi Binning   ###========###
        ###==============================================###
        phi_h_Binning          = [0,      360,     24,         15]
        if("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(Variable)):
            # phi_h_Binning      = [0,      360,     12,         30]
            phi_h_Binning      = [0,      360,     10,         36]
        ###==============================================###
        ###========###  Setting Phi Binning   ###========###
        ###==============================================###

        # NewDim_Bin_Min  = Q2_xB_Binning[0]
        # NewDim_Bin_Max  = Q2_xB_Binning[1]
        # NewDim_Bin_Num  = Q2_xB_Binning[2]
        # NewDim_Bin_Size = Q2_xB_Binning[3]
        # Num_Columns_Canvas, Num_Rows_Canvas = 4, 2
        # Multi_Dim_Var  = "Q2_xB"
        
        ###===============================================###
        ###========###  Setting Q2-y Binning   ###========###
        ###===============================================###
        NewDim_Bin_Min  = Q2_y_Binning[0]
        NewDim_Bin_Max  = Q2_y_Binning[1]
        NewDim_Bin_Num  = Q2_y_Binning[2]
        NewDim_Bin_Size = Q2_y_Binning[3]
        Num_Columns_Canvas, Num_Rows_Canvas = 4, 5
        Multi_Dim_Var  = "Q2_y"
        ###===============================================###
        ###========###  Setting Q2-y Binning   ###========###
        ###===============================================###
        
        ###===============================================###
        ###========###  Setting z-pT Binning   ###========###
        ###===============================================###
        if("z_pT_Bin" in Variable):
            NewDim_Bin_Min  = z_pT_Binning[0]
            NewDim_Bin_Max  = z_pT_Binning[1]
            NewDim_Bin_Num  = z_pT_Binning[2]
            NewDim_Bin_Size = z_pT_Binning[3]
            Num_Columns_Canvas, Num_Rows_Canvas = 6, 7
            Multi_Dim_Var  = "z_pT"
        ###===============================================###
        ###========###  Setting z-pT Binning   ###========###
        ###===============================================###
        
        ###===============================================###
        ###========###   Setting Q2 Binning    ###========###
        ###===============================================###
        if(Variable in ["Multi_Dim_Q2_phi_t", "Multi_Dim_Q2_phi_t_smeared", "Combined_phi_t_Q2", "Combined_phi_t_Q2_smeared"]):
            NewDim_Bin_Min  = Q2_Binning[0]
            NewDim_Bin_Max  = Q2_Binning[1]
            NewDim_Bin_Num  = Q2_Binning[2]
            NewDim_Bin_Size = Q2_Binning[3]
            Multi_Dim_Var   = "Q2"
            Num_Columns_Canvas, Num_Rows_Canvas = 4, 5
        ###===============================================###
        ###========###   Setting Q2 Binning    ###========###
        ###===============================================###
        
        
        ###===============================================###
        ###========###  Setting Theta Binning  ###========###
        ###===============================================###
        if(str(Variable).replace("_smeared", "") in ["Multi_Dim_elth_phi_t", "Multi_Dim_pipth_phi_t"]):
            NewDim_Bin_Min  = particle_Th__Binning[0]
            NewDim_Bin_Max  = particle_Th__Binning[1]
            NewDim_Bin_Num  = particle_Th__Binning[2]
            NewDim_Bin_Size = particle_Th__Binning[3]
            Multi_Dim_Var   = "elth" if(str(Variable).replace("_smeared", "") in ["Multi_Dim_elth_phi_t"]) else "pipth"
            Num_Columns_Canvas, Num_Rows_Canvas = 6, 6
        ###===============================================###
        ###========###  Setting Theta Binning  ###========###
        ###===============================================###
        
        
        ###===============================================###
        ###========###   Setting Phi Binning   ###========###
        ###===============================================###
        if(str(Variable).replace("_smeared", "") in ["Multi_Dim_elPhi_phi_t", "Multi_Dim_pipPhi_phi_t"]):
            NewDim_Bin_Min  = particle_Phi_Binning[0]
            NewDim_Bin_Max  = particle_Phi_Binning[1]
            NewDim_Bin_Num  = particle_Phi_Binning[2]
            NewDim_Bin_Size = particle_Phi_Binning[3]
            Multi_Dim_Var   = "elPhi" if(str(Variable).replace("_smeared", "") in ["Multi_Dim_elPhi_phi_t"]) else "pipPhi"
            Num_Columns_Canvas, Num_Rows_Canvas = 5, 5
        ###===============================================###
        ###========###   Setting Phi Binning   ###========###
        ###===============================================###
            
        Canvas_Size_X = 2400
        Canvas_Size_Y = 1200 if(Num_Rows_Canvas < 3) else 2400
        
        ###===============================================###
        ###========###   Setting 4D Binning    ###========###
        ###===============================================###
        if("Multi_Dim_Q2_y_z_pT_4D_Bin_phi_t" in str(Variable)):
            NewDim_Bin_Min  = Q2_y_z_pT_4D_Binning[0]
            NewDim_Bin_Max  = Q2_y_z_pT_4D_Binning[1]
            NewDim_Bin_Num  = Q2_y_z_pT_4D_Binning[2]
            NewDim_Bin_Size = Q2_y_z_pT_4D_Binning[3]
            Num_Columns_Canvas, Num_Rows_Canvas = 24, 24
            Multi_Dim_Var   = "Q2_y_z_pT"
            Canvas_Size_X   = 4800
            Canvas_Size_Y   = 4800
        ###===============================================###
        ###========###   Setting 4D Binning    ###========###
        ###===============================================###
        
        #######################################################################
        #####==========#####   Setting Variable Binning    #####==========#####
        #######################################################################
        
        
        
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="Multi-Dim Histo", Data_Type=str(Method), Cut_Type="Skip", Smear_Type=str(Smear), Q2_y_Bin="Multi_Dim_Q2_y_Bin_Info", z_pT_Bin="Multi_Dim_z_pT_Bin_Info", Bin_Extra="Multi_Dim_Bin_Info" if(Multi_Dim_Var not in ["Q2_xB", "Q2_y", "z_pT"]) else "Default", Variable="Default")
            if(str(Method) in ["tdf", "true"]):
                # print("".join([color.BBLUE, color_bg.RED, "\n\nMaking a Multi-Dim Histo for 'True' distribution\n", color.END]))
                # print("Name =", Name)
                Name = Name.replace("mdf", "tdf")
                Name = Name.replace("gdf", "tdf")
            # else:
            #     print("".join([color.BBLUE, color_bg.CYAN, "\nMaking a Multi-Dim Histo for '", str(Method), "' distribution\n", color.END]))
            #     print("Name =", Name, "\n")
            
        if(str(Multi_Dim_Var) in ["z_pT"]):
            Name = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(Q2_y_Bin_Select) if(str(Q2_y_Bin_Select) not in ["0"]) else "All"))
            
        if(Out_Option in ["Save", "save", "all", "All", "Canvas", "canvas"]):
            Output_Canvas = Canvas_Create(Name, Num_Columns=Num_Columns_Canvas, Num_Rows=Num_Rows_Canvas, Size_X=Canvas_Size_X, Size_Y=Canvas_Size_Y, cd_Space=0)
        
        bin_ii = 1 # 0 # if(Common_Name not in ["New_Binning_Schemes_V7_All", "New_Binning_Schemes_V8_All", "Gen_Cuts_V1_All", "Gen_Cuts_V2_All", "Gen_Cuts_V3_All", "Gen_Cuts_V4_All", "Gen_Cuts_V5_All"]) else 1
        # for NewDim_Bin in range(0, NewDim_Bin_Num + 1, 1):
        for NewDim_Bin in range(0, NewDim_Bin_Num - 1, 1):
            # if(NewDim_Bin != 0 and (Common_Name not in ["Multi_Dimension_Unfold_V3_All", "New_Binning_Schemes_V7_All", "New_Binning_Schemes_V8_All", "Gen_Cuts_V1_All", "Gen_Cuts_V2_All", "Gen_Cuts_V3_All", "Gen_Cuts_V4_All", "Gen_Cuts_V5_All"])):
            #     bin_ii  += -1
            
            if(str(Multi_Dim_Var) in ["Q2_xB", "Q2_y"]):
                Name_Out = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(NewDim_Bin)))
                Name_Out = str(Name_Out.replace("Multi_Dim_z_pT_Bin_Info", "All"))
            elif(str(Multi_Dim_Var) in ["z_pT"]):
                Name_Out = str(Name.replace("Multi_Dim_Q2_y_Bin_Info", str(Q2_y_Bin_Select) if(Q2_y_Bin_Select not in [0, "0"]) else "All"))
                Name_Out = str(Name_Out.replace("Multi_Dim_z_pT_Bin_Info", str(NewDim_Bin)))
                z_pT_Bin_Range = 42 if(str(Q2_y_Bin_Select) in ["2"]) else 36 if(str(Q2_y_Bin_Select) in ["4", "5", "9", "10"]) else 35 if(str(Q2_y_Bin_Select) in ["1", "3"]) else 30 if(str(Q2_y_Bin_Select) in ["6", "7", "8", "11"]) else 25 if(str(Q2_y_Bin_Select) in ["13", "14"]) else 20 if(str(Q2_y_Bin_Select) in ["12", "15", "16", "17"]) else 1
                if("Y_bin" in Binning_Method):
                    z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Select)[1]
                if(NewDim_Bin > z_pT_Bin_Range):
                    break
            else:
                Name_Out = str(Name.replace("Multi_Dim_Bin_Info",      str(NewDim_Bin)))
            
            if(str(Multi_Dim_Var) not in ["z_pT"]):
                Title_Out = str(Title.replace("Range: -1.5 #rightarrow 481.5 - Size: 1.0 per bin", "".join(["#scale[1.1]{Q^{2}" if(Multi_Dim_Var in ["Q2"]) else "Q^{2}-x_{B}" if(Multi_Dim_Var in ["Q2_xB"]) else "Q^{2}-y-z-P_{T}" if(Multi_Dim_Var in ["Q2_y_z_pT"]) else "Q^{2}-y", " Bin ", str(NewDim_Bin), "" if(Multi_Dim_Var in ["Q2_xB", "Q2_y", "Q2_y_z_pT"]) else "".join([": ", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*NewDim_Bin), 4)), "-", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*(NewDim_Bin + 1)), 4)), " [GeV^{2}]}"])])))
                Title_Out = str(Title_Out.replace("Multi_Dim_Var_Info",                            "".join(["#scale[1.1]{Q^{2}" if(Multi_Dim_Var in ["Q2"]) else "Q^{2}-x_{B}" if(Multi_Dim_Var in ["Q2_xB"]) else "Q^{2}-y-z-P_{T}" if(Multi_Dim_Var in ["Q2_y_z_pT"]) else "Q^{2}-y", " Bin ", str(NewDim_Bin), "" if(Multi_Dim_Var in ["Q2_xB", "Q2_y", "Q2_y_z_pT"]) else "".join([": ", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*NewDim_Bin), 4)), "-", str(round(NewDim_Bin_Min + (NewDim_Bin_Size*(NewDim_Bin + 1)), 4)), " [GeV^{2}]}"])])))
            else:
                Title_Out = str(Title.replace("Range: -1.5 #rightarrow 481.5 - Size: 1.0 per bin", "".join(["#scale[1.1]{Q^{2}-y Bin ", str(Q2_y_Bin_Select), ": z-P_{T} Bin ", str(NewDim_Bin), "}"])))
                Title_Out = str(Title_Out.replace("Multi_Dim_Var_Info",                            "".join(["#scale[1.1]{Q^{2}-y Bin ", str(Q2_y_Bin_Select), ": z-P_{T} Bin ", str(NewDim_Bin), "}"])))
                
            if("(z_pT_Bin_0)" in str(Name_Out)):
                Name_Out = str(Name_Out).replace("(z_pT_Bin_0)", "(z_pT_Bin_All)")
                
            #######################################################################
            #####==========#####   Filling Sliced Histogram    #####==========#####
            #######################################################################
            Output_Histos[Name_Out] = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
            
            ii_bin_num = 1
            for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                if(Histo_Cut is not False):
                    ii_bin_num += 1
                    bin_jj = Histo.FindBin(bin_ii)
                    Multi_Dim_cut_num = Histo_Cut.GetBinContent(bin_jj)
                    Multi_Dim_cut_err = Histo_Cut.GetBinError(bin_jj)
                    if((Multi_Dim_cut_num == 0) or (Multi_Dim_cut_num <= Multi_Dim_cut_err)):
                        Multi_Dim_phi_num = 0
                        Multi_Dim_phi_err = 0 # Histo.GetBinContent(bin_jj) + Histo.GetBinError(bin_jj)
                    else:
                        Multi_Dim_phi_num = Histo.GetBinContent(bin_jj)
                        Multi_Dim_phi_err = Histo.GetBinError(bin_jj)
                    Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],  Multi_Dim_phi_num)
                    Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), Multi_Dim_phi_err)
                    bin_ii += 1
                else:
                    ii_bin_num += 1
                    bin_jj = Histo.FindBin(bin_ii)
                    Multi_Dim_phi_num = Histo.GetBinContent(bin_jj)
                    Multi_Dim_phi_err = Histo.GetBinError(bin_jj)
                    Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],  Multi_Dim_phi_num)
                    Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), Multi_Dim_phi_err)
                    bin_ii += 1
            #######################################################################
            #####==========#####   Filling Sliced Histogram    #####==========#####
            #######################################################################

            #######################################################################
            #####==========#####   Drawing Histogram/Canvas    #####==========#####
            #######################################################################
            if(Out_Option in ["Save", "save", "all", "All", "Canvas", "canvas"]):
                Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
                # Output_Histos[Name_Out].Draw("same HIST text E0")
                Output_Histos[Name_Out].Draw("same HIST E0")
            if(Method in ["rdf", "Experimental"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Blue)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Blue)
            if(Method in ["mdf", "MC REC"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Red)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Red)
            if(Method in ["gdf", "gen", "MC GEN"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Green)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Green)
            if(Method in ["tdf", "true"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Cyan)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Cyan)
            if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Brown)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Brown)
            if(Method in ["bayes", "bayesian", "Bayesian"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Teal)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Teal)
            if(Method in ["Background"]):
                Output_Histos[Name_Out].SetLineColor(root_color.Black)
                Output_Histos[Name_Out].SetMarkerColor(root_color.Black)
            #######################################################################
            #####==========#####   Drawing Histogram/Canvas    #####==========#####
            #######################################################################
            
            
            Output_Histos[Name_Out].GetYaxis().SetRangeUser(0, 1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMaximumBin()))
            
            if(Out_Option in ["Save", "save", "all", "All", "Canvas", "canvas"]):
                configure_stat_box(hist=Output_Histos[Name_Out], show_entries=True, canvas=Output_Canvas)
                # Output_Canvas.Modified()
                # Output_Canvas.Update()
            
            
            ######################################################################
            #####==========#####     Fitting Distribution     #####==========#####
            ######################################################################
            if(Fitting_Input in ["default", "Default"] and Fit_Test):
                # Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("Multi-Dim Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("Multi-Dim Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("Multi-Dim Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("Multi-Dim Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting=Fitting_Input)
                Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("Multi-Dim Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("Multi-Dim Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("Multi-Dim Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("Multi-Dim Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting="default", Special=[Q2_y_Bin_Select, NewDim_Bin] if(str(Multi_Dim_Var) in ["z_pT"]) else "Normal") # Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out])
                if(Out_Option in ["Save", "save", "all", "All", "Canvas", "canvas"]):
                    Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
                    # Histo_To_Fit.Draw("same HIST text E0")
                    Output_Histos[Name_Out].Draw("same HIST E0")
                    Unfolded_Fit_Function[Name_Out.replace("Multi-Dim Histo", "Fit_Function")].Draw("same")
                    statbox_move(Histogram=Output_Histos[Name_Out], Canvas=Output_Canvas, Default_Stat_Obj="", Y1_add=0.25, Y2_add=0.45, X1_add=0.35, X2_add=0.75)
            elif((not Fit_Test) and (Out_Option in ["Save", "save", "all", "All", "Canvas", "canvas"])):
                Draw_Canvas(canvas=Output_Canvas, cd_num=NewDim_Bin, left_add=0.075, right_add=0.05, up_add=0.1, down_add=0.1)
                Output_Histos[Name_Out].Draw("same HIST E0")
            ######################################################################
            #####==========#####     Fitting Distribution     #####==========#####
            ######################################################################
            
            if(Out_Option in ["Save", "save", "all", "All", "Canvas", "canvas"]):
                Output_Canvas.Modified()
                Output_Canvas.Update()
            
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        
        
        ######################################################################
        #####==========#####        Saving Canvas         #####==========#####
        ######################################################################
        Save_Name = "".join(["Multi_Dim_Histo_", str(Variable).replace("_smeared", ""), "_Q2_y_Bin_", str(Q2_y_Bin_Select) if(str(Q2_y_Bin_Select) not in ["0"]) else "All", "_", str(Method) if(Method not in ["N/A"]) else "", "_Smeared" if("mear" in Smear) else "", str(File_Save_Format)]).replace(" ", "_")
        Save_Name = str((Save_Name.replace("-", "_")).replace("phi_t_", "phi_h_")).replace("__", "_")
        
        Save_Name = str(Save_Name.replace("phi_t", "phi_h"))
        
        Save_Name = str(Save_Name.replace("Multi_Dim_Histo_Multi_Dim", "Multi_Dim_Histo"))
        
        if(((Method in ["gdf", "gen", "MC GEN", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"])) and (extra_function_terms and "phi_h" in str(Save_Name))):
            Save_Name = str(Save_Name).replace(str(File_Save_Format), "".join(["_Extra_Parameters", str(File_Save_Format)]))
        
        if(("y_bin" in str(Binning_Method)) or ("Y_bin" in str(Binning_Method))):
            Save_Name = Save_Name.replace("_Q2_xB_Bin_", "_Q2_y_Bin_")
        if(Sim_Test):
            Save_Name = "".join(["Sim_Test_", Save_Name])
            
            
        Save_Name = Save_Name.replace("Q2_y_Bin_phi_h",                      "Q2_y_phi_h")
        Save_Name = Save_Name.replace("z_pT_Bin_y_bin_phi_h",                "z_pT_phi_h")
        Save_Name = Save_Name.replace("z_pT_Bin_Y_bin_phi_h",                "z_pT_phi_h")
        Save_Name = Save_Name.replace("".join(["_", str(File_Save_Format)]), str(File_Save_Format))
        Save_Name = Save_Name.replace("__",                                  "_")
        # if((Saving_Q) and (Out_Option in ["Save", "save", "Canvas", "canvas", "complete", "Complete"])):
        # if(Saving_Q and ("Acceptance" not in Method)):
        if(Saving_Q and ("Acceptance" not in Method) and (Out_Option in ["Save", "save"])):
            if("root" in str(File_Save_Format)):
                Output_Canvas.SetName(Save_Name.replace(".root", ""))
            Output_Canvas.SaveAs(Save_Name)
            del Output_Canvas
        # print("".join(["Saved: " if(Saving_Q and ("Acceptance" not in Method)) else "Would be Saving: ", color.BBLUE, str(Save_Name), color.END]))
        # print("".join(["Saved: " if(Saving_Q and ("Acceptance" not in Method) and (Out_Option in ["Save", "save", "Canvas", "canvas"])) else "Would be Saving: ", color.BBLUE, str(Save_Name), color.END]))
        print("".join(["Saved: " if(Saving_Q and ("Acceptance" not in Method) and (Out_Option in ["Save", "save"])) else "Would be Saving: ", color.BBLUE, str(Save_Name), color.END]))
        ######################################################################
        #####==========#####        Saving Canvas         #####==========#####
        ######################################################################
        
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
        if(Out_Option not in ["Save", "save"]):
            Output_List = []
            if(Out_Option in ["all", "All", "Histos", "histos", "Histo", "histo"]):
                Output_List.append(Output_Histos)
            if((Out_Option in ["all", "All", "Fit", "fit", "Pars", "pars"])):
                Output_List.append(Unfolded_Fit_Function)
            if((Out_Option in ["all", "All", "Pars", "pars"])):
                Output_List.append(Fit_Par_A)
                Output_List.append(Fit_Par_B)
                Output_List.append(Fit_Par_C)
            if(Out_Option in ["all", "All", "Canvas", "canvas"]):
                Output_List.append(Output_Canvas)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
    
    except:
        print("".join([color.Error, "MultiD_Slice(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        return "Error"

################################################################################################################################################################################################################################################
##==========##==========##           Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################



################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################
def Multi5D_Slice(Histo, Title="Default", Name="none", Method="N/A", Variable="MultiDim_Q2_y_z_pT_phi_h", Smear="", Out_Option="Save", Fitting_Input="default"):
    if(list is type(Histo)):
        Histo, Histo_Cut = Histo # If the input of Histo is given as a list, the first histogram is considered to be the main one to be sliced. 
                                 # The second one is considered to be the 'rdf' (or 'mdf') histogram used to tell when the edge bins should be cut (i.e., when the bin content of Histo_Cut = 0 --> Not good for acceptance).
    else:
        Histo_Cut = False
    Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C = {}, {}, {}, {}, {}, {}
    if(str(Method) not in ["rdf", "gdf"]):
        if(((Smearing_Options in ["both", "no_smear"]) and (Smear in [""])) or ((Smearing_Options in ["both", "smear"]) and ("mear" in str(Smear)))):
            print(color.BLUE, "\nRunning Multi5D_Slice(...)\n", color.END)
        else:
            print(color.Error, "\n\nWrong Smearing option for Multi5D_Slice(...)\n\n", color.END)
            return "Error"
    elif(Smear in [""]):
        print(color.BLUE,      "\nRunning Multi5D_Slice(...)\n", color.END)
    else:
        print(color.Error,     "\n\nWrong Smearing option for Multi5D_Slice(...)\n\n", color.END)
        return "Error"
    try:
        #######################################################################
        #####==========#####     Catching Input Errors     #####==========#####
        #######################################################################
        if(Name != "none"):
            if(Name in ["histo", "Histo", "input", "default"]):
                Name = Histo.GetName()
            if("MultiDim_Q2_y_z_pT_phi_h" not in str(Name)):
                print(color.RED, "ERROR: WRONG TYPE OF HISTOGRAM\nName =", color.END, Name, "\nMulti5D_Slice() should be used on the histograms with the 'MultiDim_Q2_y_z_pT_phi_h' bin variable\n\n")
                return "Error"
        if(str(Variable).replace("_smeared", "") not in ["MultiDim_Q2_y_z_pT_phi_h"]):
            print(color.RED, "ERROR in Multi5D_Slice(): Not set up for other variables (yet)", color.END, "\nVariable =", Variable, "\n\n")
            return "Error"
        if(("mear"     in str(Smear)) and ("_smeared" not in str(Variable))):
            Variable = "".join([Variable,  "_smeared"])
        if(("mear" not in str(Smear)) and ("_smeared"     in str(Variable))):
            Smear = "Smear"
        ########################################################################
        #####==========#####      Catching Input Errors     #####==========#####
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        Method_Title = ""
        if(Method in ["rdf", "Experimental"]):
            Method_Title = "".join([" #color[", str(root_color.Blue),  "]{(Experimental)}"       if(not Sim_Test)      else "]{(MC REC - Pre-Unfolded)}"])
            if(not Sim_Test):
                Variable = Variable.replace("_smeared", "")
                Smear    = ""
        if(Method in ["mdf", "MC REC"]):
            Method_Title = "".join([" #color[", str(root_color.Red),   "]{(MC REC)}"])
        if(Method in ["gdf", "gen", "MC GEN"]):
            Method_Title = "".join([" #color[", str(root_color.Green), "]{(MC GEN", " - Matched" if(Method in ["gen"]) else "", ")}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["tdf", "true"]):
            Method_Title = "".join([" #color[", str(root_color.Cyan),  "]{(MC TRUE)}"])
            Variable     = Variable.replace("_smeared", "")
            Smear        = ""
        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
            Method_Title = "".join([" #color[", str(root_color.Brown), "]{(Bin-by-Bin)}"])
        if(Method in ["bayes", "bayesian", "Bayesian"]):
            Method_Title = "".join([" #color[", str(root_color.Teal),  "]{(Bayesian Unfolded)}"])
        if(Method in ["Acceptance", "Background"]):
            Method_Title = "".join(["(", str(root_color.Bold),          "{", str(Method), "})"])
        ###===============================================###
        ###========###  Setting Method Title   ###========###
        ###===============================================###
        if(Title in ["Default", "norm", "standard"]):
            Title = str(Histo.GetTitle()) if(Title == "Default") else "".join(["#splitline{", str(root_color.Bold), "{5-Dimensional Plot of", " (Smeared)" if("mear" in Smear) else "", " #phi_{h}", str(Method_Title), "}}{MultiDim_5D_Var_Info}"])
        fit_function_title = "A (1 + B Cos(#phi_{h}) + C Cos(2#phi_{h}))"
        if((Method in ["gdf", "gen", "MC GEN", "tdf", "true", "bbb", "Bin", "Bin-by-Bin", "Bin-by-bin", "bayes", "bayesian", "Bayesian"]) and (Fitting_Input in ["default", "Default"]) and Fit_Test):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{Fitted with: ", str(fit_function_title), "}}"])
        if((Pass_Version not in [""]) and (Pass_Version not in str(Title))):
            Title = "".join(["#splitline{", str(Title), "}{", str(root_color.Bold), "{", str(Pass_Version), "}}"])
        ########################################################################
        #####==========#####    Setting Histogram Title     #####==========#####
        ########################################################################
        #####==========#####    Setting Variable Binning    #####==========#####
        ########################################################################
                      # ['min', 'max', 'num_bins', 'size']
        phi_h_Binning = [0,     360,   24,         15]
        ########################################################################
        #####==========#####   #Setting Variable Binning    #####==========#####
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        if(Name != "none"):
            Name = Histogram_Name_Def(out_print=Name, Histo_General="MultiDim_5D_Histo", Data_Type=str(Method), Cut_Type="Skip", Smear_Type=str(Smear), Q2_y_Bin="MultiDim_5D_Q2_y_Bin_Info", z_pT_Bin="MultiDim_5D_z_pT_Bin_Info", Bin_Extra="Default", Variable="Default")
            if(str(Method) in ["tdf", "true"]):
                # print("".join([color.BBLUE, color_bg.RED, "\n\nMaking a Multi-Dim Histo for 'True' distribution\n", color.END, "\nName =", str(Name), "\n"]))
                Name = Name.replace("mdf", "tdf")
                Name = Name.replace("gdf", "tdf")
            # else:
            #     print("".join([color.BBLUE, color_bg.CYAN, "\nMaking a Multi-Dim Histo for '", str(Method), "' distribution\n", color.END, "\nName =", str(Name), "\n"]))
        for Q2_y in Q2_xB_Bin_List:
            if(Q2_y not in ["0", "All"]):
                if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT=1", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")):
                    break
                else:
                    z_pT_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y)[1]
                    for z_pT in range(0, z_pT_Range+1):
                        Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{Q^{2}-y Bin: ", str(Q2_y) if(str(Q2_y) not in ["0"]) else "All", "} #topbar #color[", str(root_color.Red), "]{z-P_{T} Bin: ", str(z_pT) if(str(z_pT) not in ["0"]) else "All", "}}}"])
                        Title_Out = str(Title.replace("MultiDim_5D_Var_Info", Bin_Title))
                        if(z_pT not in [0]):
                            if("ERROR" == Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT}", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")):
                                break
                            else:
                                Start_phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT}",       End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT={z_pT+1}",     End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                if(End___phi_h_bin in ["ERROR"]):
                                    End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={int(Q2_y)+1}, z-pT=1", End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                                if((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]):
                                    continue
                        else:
                            Start_phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={Q2_y}, z-pT=1",                End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                            End___phi_h_bin = Convert_All_Kinematic_Bins(Start_Bins_Name=f"Q2-y={int(Q2_y)+1}, z-pT=1",         End_Bins_Name="MultiDim_Q2_y_z_pT_phi_h")
                        Name_Out = str(Name.replace("MultiDim_5D_Q2_y_Bin_Info",     str(Q2_y) if(str(Q2_y) not in ["0", "All"]) else "All"))
                        Name_Out = str(Name_Out.replace("MultiDim_5D_z_pT_Bin_Info", str(z_pT) if(str(z_pT) not in ["0", "All"]) else "All"))
                        Output_Histos[Name_Out] = ROOT.TH1D(Name_Out, "".join([str(Title_Out), "; ",  "(Smeared) " if("mear" in Smear) else "", "#phi_{h} [", str(root_color.Degrees), "]"]), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1])
                        # print(f"Making Output_Histos[{Name_Out}]...\n\tlen(Output_Histos[Name_Out]) = ", str(len(Output_Histos[Name_Out])))
                        #######################################################################
                        #####==========#####   Filling Sliced Histogram    #####==========#####
                        #######################################################################
                        ii_bin_num,  ii_LastNum  = Start_phi_h_bin, Start_phi_h_bin
                        phi_Content, phi___Error = {}, {}
                        for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] = 0
                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] = 0
                        while(ii_bin_num < End___phi_h_bin):
                            OverFlow_Con = False
                            if((End___phi_h_bin - Start_phi_h_bin) not in [phi_h_Binning[2]]):
                                # Conditions for combining all z-pT bins
                                Q2_y_bin_0 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num-1}", End_Bins_Name="Q2-y") if(ii_bin_num != 0) else 1
                                Q2_y_bin_1 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num}",   End_Bins_Name="Q2-y")
                                z_pT_bin_0 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num-1}", End_Bins_Name="z-pT") if(ii_bin_num != 0) else 1
                                z_pT_bin_1 = Convert_All_Kinematic_Bins(Start_Bins_Name=f"MultiDim_Q2_y_z_pT_phi_h={ii_bin_num}",   End_Bins_Name="z-pT")
                                if((z_pT_bin_0 != z_pT_bin_1) and (Q2_y_bin_0 == Q2_y_bin_1)):
                                    if(ii_LastNum + 1 == ii_bin_num):
                                        OverFlow_Con = True
                                    ii_LastNum = ii_bin_num
                                elif(Q2_y_bin_0 != Q2_y_bin_1):
                                    ii_LastNum = Start_phi_h_bin
                            if(OverFlow_Con):
                                ii_bin_num += 1
                                continue
                            else:
                                for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                                    if(Histo_Cut is not False):
                                        bin_ii = Histo.FindBin(ii_bin_num + 1)
                                        MultiDim_cut_num = Histo_Cut.GetBinContent(bin_ii)
                                        MultiDim_cut_err = Histo_Cut.GetBinError(bin_ii)
                                        if((MultiDim_cut_num == 0) or (MultiDim_cut_num <= MultiDim_cut_err)):
                                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] += 0
                                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += 0 # Histo.GetBinContent(bin_ii) + Histo.GetBinError(bin_ii)
                                        else:
                                            phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                            phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                                        ii_bin_num += 1
                                    else:
                                        bin_ii = Histo.FindBin(ii_bin_num + 1)
                                        phi_Content[phi_bin + 0.5*phi_h_Binning[3]] +=  Histo.GetBinContent(bin_ii)
                                        phi___Error[phi_bin + 0.5*phi_h_Binning[3]] += (Histo.GetBinError(bin_ii))*(Histo.GetBinError(bin_ii))
                                        ii_bin_num += 1
                        for phi_bin in range(phi_h_Binning[0], phi_h_Binning[1], phi_h_Binning[3]):
                            Output_Histos[Name_Out].Fill(                                       phi_bin + 0.5*phi_h_Binning[3],            phi_Content[phi_bin + 0.5*phi_h_Binning[3]])
                            Output_Histos[Name_Out].SetBinError(Output_Histos[Name_Out].FindBin(phi_bin + 0.5*phi_h_Binning[3]), ROOT.sqrt(phi___Error[phi_bin + 0.5*phi_h_Binning[3]]))
                        #######################################################################
                        #####==========#####   Filling Sliced Histogram    #####==========#####
                        #######################################################################
                        #####==========#####   Drawing Histogram Options   #####==========#####
                        #######################################################################
                        Output_Histos[Name_Out].GetYaxis().SetRangeUser(0, 1.5*Output_Histos[Name_Out].GetBinContent(Output_Histos[Name_Out].GetMaximumBin()))
                        if(Method in ["rdf", "Experimental"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Blue)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Blue)
                        if(Method in ["mdf", "MC REC"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Red)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Red)
                        if(Method in ["gdf", "gen", "MC GEN"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Green)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Green)
                        if(Method in ["tdf", "true"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Cyan)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Cyan)
                        if(Method in ["bbb", "Bin", "Bin-by-Bin", "Bin-by-bin"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Brown)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Brown)
                        if(Method in ["bayes", "bayesian", "Bayesian"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Teal)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Teal)
                        if(Method in ["Background"]):
                            Output_Histos[Name_Out].SetLineColor(root_color.Black)
                            Output_Histos[Name_Out].SetMarkerColor(root_color.Black)
                        #######################################################################
                        #####==========#####   Drawing Histogram Options   #####==========#####
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        #######################################################################
                        if(Fitting_Input in ["default", "Default"] and Fit_Test):
                            Output_Histos[Name_Out], Unfolded_Fit_Function[Name_Out.replace("MultiDim_5D_Histo", "Fit_Function")], Fit_Chisquared[Name_Out.replace("MultiDim_5D_Histo", "Chi_Squared")], Fit_Par_A[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_A")], Fit_Par_B[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_B")], Fit_Par_C[Name_Out.replace("MultiDim_5D_Histo", "Fit_Par_C")] = Fitting_Phi_Function(Histo_To_Fit=Output_Histos[Name_Out], Method=Method, Fitting="default", Special=[int(Q2_y), int(z_pT)])
                        #######################################################################
                        #####==========#####      Fitting Distribution     #####==========#####
                        #######################################################################
            # else:
            #     # Bin_Title = "".join([root_color.Bold, "{#scale[1.25]{#color[", str(root_color.Red), "]{All Binned Events}}}"])
            #     # Title_Out = str(Title.replace("MultiDim_5D_Var_Info", Bin_Title))
            #     print(f"{color.Error}\n\n\nError while running Multi5D_Slice(...):\n\tDo NOT run for Q2-y Bin = 'All'{color.END_R}\n\t(Plot is currently considered not important enough to warrent the effort to create){color.END}\n\n\n")
            #     return "Error"
            
        ################################################################################
        ###==============###========================================###==============###
        ###==============###   Creation of the Sliced Histograms    ###==============###
        ###==============###========================================###==============###
        ################################################################################
        
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
        if(Out_Option not in ["Save", "save"]):
            Output_List = []
            if(Out_Option in ["all", "All", "Histos", "histos", "Histo", "histo"]):
                Output_List.append(Output_Histos)
            if((Out_Option in ["all", "All", "Fit", "fit", "Pars", "pars"])):
                Output_List.append(Unfolded_Fit_Function)
            if((Out_Option in ["all", "All", "Pars", "pars"])):
                Output_List.append(Fit_Par_A)
                Output_List.append(Fit_Par_B)
                Output_List.append(Fit_Par_C)
            if(Out_Option in ["complete", "Complete"]):
                Output_List = [Output_Histos, Unfolded_Fit_Function, Fit_Chisquared, Fit_Par_A, Fit_Par_B, Fit_Par_C]
            return Output_List
        ######################################################################
        #####==========#####      Returning Outputs       #####==========#####
        ######################################################################
    except:
        print("".join([color.Error, "Multi5D_Slice(...) ERROR:\n", color.END, str(traceback.format_exc()), "\n"]))
        return "Error"

################################################################################################################################################################################################################################################
##==========##==========##        5D-Multidimensional Slice Function              ##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################################################################################################