import ROOT

Binning_Method = "_Y_bin"
# Binning_Method = "_y_bin"
# Binning_Method = "_2"


class color:
    CYAN      = '\033[96m'
    PURPLE    = '\033[95m'
    PINK      = '\033[35m'
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
    ERROR     = '\033[91m\033[1m' # Combines RED and BOLD
    Error     = '\033[91m\033[1m' # Same as ERROR
    BBLUE     = '\033[1m\033[94m' # Combines BLUE and BOLD
    BCYAN     = '\033[1m\033[96m' # Combines CYAN and BOLD
    BGREEN    = '\033[1m\033[92m' # Combines GREEN and BOLD
    BYELLOW   = '\033[1m\033[93m' # Combines YELLOW and BOLD
    END_B     = '\033[0m\033[1m'  # Combines END and BOLD
    END_R     = '\033[0m\033[91m' # Combines END and RED
    END_C     = '\033[0m\033[96m' # Combines END and CYAN
    END_G     = '\033[0m\033[92m' # Combines END and GREEN
    END_b     = '\033[0m\033[94m' # Combines END and BLUE
    
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
    Teal    = 30
    Gold    = 41
    Rust    = 46
    
    # Fonts
    Bold    = '#font[22]'
    Italic  = '#font[12]'
    
    # Symbols
    Delta   = '#Delta'
    Phi     = '#phi'
    π       = '#pi'
    Degrees = '#circ'
    
    Line    = '#splitline'


###################=========================###################
##===============##     Variable Titles     ##===============##
###################=========================###################

def variable_Title_name(variable):
    smeared_named, bank_named = '', ''
    if("_smeared" in variable):
        smeared_named = 'yes'
        variable = variable.replace("_smeared", "")
        
    if("_gen" in variable):
        bank_named = 'yes'
        variable = variable.replace("_gen",     "")
        
    Extra_Variable_Title     = ""
    if("Smeared_Effect_on_"  in variable):
        Extra_Variable_Title = "Smeared Effect on "
        variable = variable.replace("Smeared_Effect_on_",  "")
    if("Smeared_Percent_of_" in variable):
        Extra_Variable_Title = "Smeared (Percent) Effect on "
        variable = variable.replace("Smeared_Percent_of_", "")
    if("true"                in variable):
        Extra_Variable_Title = "(True Generated) "
        variable = variable.replace("true",        "")
    if("_Born"               in variable):
        Extra_Variable_Title = "(Born Level) "
        variable = variable.replace("_Born",       "")
    if("_Cor_q"              in variable):
        Extra_Variable_Title = "(Radiatively Corrected) "
        variable = variable.replace("_Cor_q",      "")
    if("_No_Rad_Cor"         in variable):
        Extra_Variable_Title = "(No Rad Cors) "
        variable = variable.replace("_No_Rad_Cor", "")


    
    output = 'error'

    if("MultiDim_Q2_y_z_pT_phi_h"        in variable):
        output  =  "5D Kinematic Bins (Q^{2}+y+z+P_{T}+#phi_{h})"
    if("MultiDim_z_pT_Bin_Y_bin_phi_t"   in variable):
        output  =  "3D Kinematic Bins (z+P_{T}+#phi_{h})"
    if("MultiDim_z_pT_Bin_Int_bin_phi_t" in variable):
        output  =  "(Integratable) 3D Kinematic Bins (z+P_{T}+#phi_{h})"
    if("MultiDim_Int_Q2_y_z_pT_phi_h"    in variable):
        output  =  "(Integratable) 5D Kinematic Bins (Q^{2}+y+z+P_{T}+#phi_{h})"
    if(variable in ['Hx', 'Hy']):
        output  =  str(variable)
    if(variable == 'Hx_pip'):
        output  =  "Hx_{#pi^{+}}"
    if(variable == 'Hy_pip'):
        output  =  "Hy_{#pi^{+}}"
    if(variable == 'ele_x_DC'):
        output  =  "Electron x_{DC}"
    if(variable == 'ele_y_DC'):
        output  =  "Electron y_{DC}"
    if(variable == 'ele_x_DC_rot'):
        output  =  "Electron x_{DC} (Rotated)"
    if(variable == 'ele_y_DC_rot'):
        output  =  "Electron y_{DC} (Rotated)"
    if(variable == 'pip_x_DC'):
        output  =  "Pion x_{DC}"
    if(variable == 'pip_y_DC'):
        output  =  "Pion y_{DC}"
    if(variable == 'pip_x_DC_rot'):
        output  =  "Pion x_{DC} (Rotated)"
    if(variable == 'pip_y_DC_rot'):
        output  =  "Pion y_{DC} (Rotated)"
    if(variable == 'ele_x_DC_6'):
        output  =  "Electron x_{DC} (Layer 6)"
    if(variable == 'ele_y_DC_6'):
        output  =  "Electron y_{DC} (Layer 6)"
    if(variable == 'ele_x_DC_6_rot'):
        output  =  "Electron x_{DC} (Rotated - Layer 6)"
    if(variable == 'ele_y_DC_6_rot'):
        output  =  "Electron y_{DC} (Rotated - Layer 6)"
    if(variable == 'pip_x_DC_6'):
        output  =  "Pion x_{DC} (Layer 6)"
    if(variable == 'pip_y_DC_6'):
        output  =  "Pion y_{DC} (Layer 6)"
    if(variable == 'pip_x_DC_6_rot'):
        output  =  "Pion x_{DC} (Rotated - Layer 6)"
    if(variable == 'pip_y_DC_6_rot'):
        output  =  "Pion y_{DC} (Rotated - Layer 6)"
    if(variable == 'ele_x_DC_18'):
        output  =  "Electron x_{DC} (Layer 18)"
    if(variable == 'ele_y_DC_18'):
        output  =  "Electron y_{DC} (Layer 18)"
    if(variable == 'ele_x_DC_18_rot'):
        output  =  "Electron x_{DC} (Rotated - Layer 18)"
    if(variable == 'ele_y_DC_18_rot'):
        output  =  "Electron y_{DC} (Rotated - Layer 18)"
    if(variable == 'pip_x_DC_18'):
        output  =  "Pion x_{DC} (Layer 18)"
    if(variable == 'pip_y_DC_18'):
        output  =  "Pion y_{DC} (Layer 18)"
    if(variable == 'pip_x_DC_18_rot'):
        output  =  "Pion x_{DC} (Rotated - Layer 18)"
    if(variable == 'pip_y_DC_18_rot'):
        output  =  "Pion y_{DC} (Rotated - Layer 18)"
    if(variable == 'ele_x_DC_36'):
        output  =  "Electron x_{DC} (Layer 36)"
    if(variable == 'ele_y_DC_36'):
        output  =  "Electron y_{DC} (Layer 36)"
    if(variable == 'ele_x_DC_36_rot'):
        output  =  "Electron x_{DC} (Rotated - Layer 36)"
    if(variable == 'ele_y_DC_36_rot'):
        output  =  "Electron y_{DC} (Rotated - Layer 36)"
    if(variable == 'pip_x_DC_36'):
        output  =  "Pion x_{DC} (Layer 36)"
    if(variable == 'pip_y_DC_36'):
        output  =  "Pion y_{DC} (Layer 36)"
    if(variable == 'pip_x_DC_36_rot'):
        output  =  "Pion x_{DC} (Rotated - Layer 36)"
    if(variable == 'pip_y_DC_36_rot'):
        output  =  "Pion y_{DC} (Rotated - Layer 36)"
    if(variable == 'el_E'):
        output  =  'E_{el}'
    if(variable == 'pip_E'):
        output  =  'E_{#pi^{+}}'
    if(variable == 'el'):
        output  =  "p_{el}"
    if(variable == 'el_V'):
        output  =  "p_{el} (at Vertex)"   
    if(variable == 'pip'):
        output  =  "p_{#pi^{+}}"
    if(variable == 'elth'):
        output  =  "#theta_{el}"
    if(variable == 'elth_V'):
        output  =  "#theta_{el} (at Vertex)"
    if(variable == 'pipth'):
        output  =  "#theta_{#pi^{+}}"
    if(variable == 'elPhi'):
        output  =  "#phi_{el}"
    if(variable == 'elPhi_V'):
        output  =  "#phi_{el} (at Vertex)"        
    if(variable == 'pipPhi'):
        output  =  "#phi_{#pi^{+}}"
    if(variable == 'MM'):
        output  =  "Missing Mass"
    if(variable == 'MM2'):
        output  =  "Missing Mass^{2}"
    if(variable == 'Q2'):
        output  =  "Q^{2}"
    if(variable == 'xB'):
        output  =  "x_{B}"
    if(variable == 'v'):
        output  =  "#nu (lepton energy loss)"
    if(variable == 's'):
        output  =  "s (CM Energy^{2})"
    if(variable == 'W'):
        output  =  "W (Invariant Mass)"
    if(variable == 'y'):
        output  =  "y (lepton energy loss fraction)"
    if(variable == 'z'):
        output  =  "z"
    if(variable == 'v'):
        output  =  "#nu"
    if(variable == 'epsilon'):
        output  =  "#epsilon"
    if(variable == 'pT'):
        output  =  "P_{T}"
    if(variable in ['phi_t', 'phi_h']):
        output  =  "#phi_{h}"
    if(variable == 'xF'):
        output  =  "x_{F} (Feynman x)"
    if(variable == 'pipx_CM'):
        output  =  "CM p_{#pi^{+}} in #hat{x}"
    if(variable == 'pipy_CM'):
        output  =  "CM p_{#pi^{+}} in #hat{y}"
    if(variable == 'pipz_CM'):
        output  =  "CM p_{#pi^{+}} in #hat{z}"
    if(variable == 'qx_CM'):
        output  =  "CM p_{q} in #hat{x}"
    if(variable == 'qy_CM'):
        output  =  "CM p_{q} in #hat{y}"
    if(variable == 'qz_CM'):
        output  =  "CM p_{q} in #hat{z}"
    if(variable == 'beamX_CM'):
        output  =  "CM p_{beam} in #hat{x}"
    if(variable == 'beamY_CM'):
        output  =  "CM p_{beam} in #hat{y}"
    if(variable == 'beamZ_CM'):
        output  =  "CM p_{beam} in #hat{z}"
    if(variable == 'eleX_CM'):
        output  =  "CM p_{el} in #hat{x}"
    if(variable == 'eleY_CM'):
        output  =  "CM p_{el} in #hat{y}"
    if(variable == 'eleZ_CM'):
        output  =  "CM p_{el} in #hat{z}"
    if(variable == 'event'):
        output  =  "Event Number"
    if(variable == 'runN'):
        output  =  "Run Number"
    if(variable == 'ex'):
        output  =  "Lab p_{el} in #hat{x}"
    if(variable == 'ey'):
        output  =  "Lab p_{el} in #hat{y}"
    if(variable == 'ez'):
        output  =  "Lab p_{el} in #hat{z}"
    if(variable == 'ex_V'):
        output  =  "Lab p_{el} in #hat{x} (at Vertex)"
    if(variable == 'ey_V'):
        output  =  "Lab p_{el} in #hat{y} (at Vertex)"
    if(variable == 'ez_V'):
        output  =  "Lab p_{el} in #hat{z} (at Vertex)"
    if(variable == 'px'):
        output  =  "Lab p_{#pi^{+}} in #hat{x}"
    if(variable == 'py'):
        output  =  "Lab p_{#pi^{+}} in #hat{y}"
    if(variable == 'pz'):
        output  =  "Lab p_{#pi^{+}} in #hat{z}"
    if(variable == 'esec'):
        output  =  "Electron Sector"
    if(variable == 'pipsec'):
        output  =  "#pi^{+} Sector"
    # if(variable == 'esec_a'):
    if('esec_a' in variable):
        output = "Electron Sector (Angle Def)"
    # if(variable == 'pipsec_a'):
    if('pipsec_a' in variable):
        output  =  "#pi^{+} Sector (Angle Def)"
    if(variable == 'Q2_xB_Bin'):
        output  =  "Q^{2}-x_{B} Bin"
    if(variable == 'Q2_xB_Bin_2'):
        output  =  "Q^{2}-x_{B} Bin (New)"
    if(variable == 'Q2_xB_Bin_Test'):
        output  =  "Q^{2}-x_{B} Bin (Test)"
    if(variable == 'Q2_xB_Bin_3'):
        output  =  "Q^{2}-x_{B} Bin (Square)"
    if(variable == 'Q2_xB_Bin_Off'):
        output  =  "Q^{2}-x_{B} Bin (Off)"
    if(variable == 'Q2_y_Bin'):
        output  =  "Q^{2}-y Bin (Old)"
    if(variable == 'Q2_Y_Bin'):
        output  =  "Q^{2}-y Bin"
    if(variable == 'z_pT_Bin'):
        output  =  "z-P_{T} Bin"
    if(variable == 'z_pT_Bin_2'):
        output  =  "z-P_{T} Bin (New)"
    if(variable == 'z_pT_Bin_Test'):
        output  =  "z-P_{T} Bin (Test)"
    if(variable == 'z_pT_Bin_3'):
        output  =  "z-P_{T} Bin (Square)"
    if(variable == 'z_pT_Bin_Off'):
        output  =  "z-P_{T} Bin (Off)"
    if(variable == 'z_pT_Bin_y_bin'):
        output  =  "z-P_{T} Bin (Old y-binning)"
    if(variable == 'z_pT_Bin_Y_bin'):
        output  =  "z-P_{T} Bin (y-binning)"
    if(variable == 'z_pT_Bin_Int_bin'):
        output  =  "z-P_{T} Bin (Easier Integration)"
    if(variable == 'elec_events_found'):
        output  =  "Number of Electrons Found"
    if(variable == 'Delta_Smear_El_P'):
        output  =  "#Delta_{Smeared}p_{el}"
    if(variable == 'Delta_Smear_El_Th'):
        output  =  "#Delta_{Smeared}#theta_{el}"
    if(variable == 'Delta_Smear_El_Phi'):
        output  =  "#Delta_{Smeared}#phi_{el}"
    if(variable == 'Delta_Smear_Pip_P'):
        output  =  "#Delta_{Smeared}p_{#pi^{+}}"
    if(variable == 'Delta_Smear_Pip_Th'):
        output  =  "#Delta_{Smeared}#theta_{#pi^{+}}"
    if(variable == 'Delta_Smear_Pip_Phi'):
        output  =  "#Delta_{Smeared}#phi_{#pi^{+}}"
    if(variable == 'Complete_Correction_Factor_Ele'):
        output  =  "Correction Factor for the Electron Momentum"
    if(variable == 'Complete_Correction_Factor_Pip'):
        output  =  "Correction Factor for the #pi^{+} Momentum"
    if(variable == 'Percent_phi_t'):
        output  =  "Percent Dif of #phi_{h} from Mom Cors"
    if(variable == 'Delta_phi_t'):
        output  =  "#Delta#phi_{h} from Mom Cors"
    if(variable in ['PID_el',  'PID_el_idx']):
        output  =  "Electron PID"
    if(variable in ['PID_pip', 'PID_pip_idx']):
        output  =  "#pi^{+} Pion PID"
    if(variable == 'layer_DC'):
        output  =  "DC Detector Layer"
    if(variable == 'layer_pip_DC'):
        output  =  "(Pion) DC Detector Layer"
    if(variable == 'layer_ele_DC'):
        output  =  "(Electron) DC Detector Layer"
    if(variable == 'V_PCal'):
        output  =  "V_{PCal}"
    if(variable == 'W_PCal'):
        output  =  "W_{PCal}"
    if(variable == 'U_PCal'):
        output  =  "U_{PCal}"
    if(variable == 'MM2_pro'):
        output  =  "Missing Mass^{2} (Proton)"
    if(variable == 'MM_pro'):
        output  =  "Missing Mass_{epX} (Proton)"
    if(variable == 'pro'):
        output  =  "p_{pro}"
    if(variable == 'rad_event'):
        output  =  "Radiative Event"
    if(variable == 'EBrems'):
        output  =  "EBrems"
    if(variable == 'SigRadCor'):
        output  =  "RC Factor"
    if(variable == 'sigma_rad'):
        output  =  "#sigma_{Rad}"
    if(variable == 'Angle_btw_scatt_gamma'):
        output  =  "#theta_{e-#gamma}"
    if(variable == 'Angle_Diff_ele_gamma'):
        output  =  "|#theta_{#gamma} - #theta_{el}|"
    if(variable == 'Angle_btw_beam__gamma'):
        output  =  "#theta_{beam-#gamma}"
    if(variable == 'gPhi'):
        output  =  "#phi_{#gamma}"
    if(variable == 'gTheta'):
        output  =  "#theta_{#gamma}"
    if(variable == 'photon'):
        output  =  "p_{#gamma}"
    if(variable == 'gE'):
        output  =  "E_{#gamma}"
    if(variable == 'gPhi_Tsai'):
        output  =  "#phi_{#gamma} (Tsai-Frame)"
    if(variable == 'gPhi_Tsai_rad'):
        output  =  "#phi_{#gamma} (Tsai-Frame) [Radians]"
    if('Theta_Tsai' in variable):
        for par in ["g", "b", "e"]:
            if(variable in [f'{par}Theta_Tsai', f'{par}Theta_Tsai_rad']):
                output = ''.join(["#theta_{", "#gamma" if(par == "g") else "Beam" if(par == "b") else "el" if(par == "e") else "ERROR", "} (Tsai-Frame)", " [Radians]" if("Tsai_rad" in variable) else ""])#"#circ]"])
    # if(variable == 'gTheta_Tsai'):
    #     output  =  "#theta_{#gamma} (Tsai-Frame)"
    # if(variable == 'gTheta_Tsai_rad'):
    #     output  =  "#theta_{#gamma} (Tsai-Frame) [Radians]"
    if(variable == 'rad_FSR_phi'):
        output  =  "#phi_{#gamma} (around scattered electron)"
    if(variable == 'rad_FSR_theta'):
        output  =  "#theta_{#gamma} (around scattered electron)"
    if(variable == 'beam_E'):
        output  =  "Beam Energy"
    if(variable == 'gR_status'):
        output  =  "Rad #gamma Status"
    if(variable == 'diff_in_rad_phi'):
        output  =  "|#phi_{#gamma} - #phi_{el} (at Vertex)|"
    if(variable == 'diff_in_rad_theta'):
        output  =  "#Delta(#theta_{el (at Vertex)} - #theta_{#gamma})"
    if(variable == 'cos_theta_Tsai'):
        output  =  "Cos(#theta_{#gamma (Tsai)})"
    if(variable == 'diff_in_Tsai_beam'):
        # output  =  "|#theta_{#gamma} - #theta_{beam}| (Tsai-Frame)"
        output  =  "#theta_{#gamma} - #theta_{beam} (Tsai-Frame)"
    if(variable == 'diff_in_Tsai_scat'):
        # output  =  "|#theta_{#gamma} - #theta_{el}| (Tsai-Frame)"
        output  =  "#theta_{#gamma} - #theta_{el} (Tsai-Frame)"
    if(variable in ['y_g_Tsai', 'z_g_Tsai']):
        output  =  f"Rad Photon p_{{{variable.replace('_g_Tsai', '')}}} (Tsai-Frame)"

    
        


    if("Bin_4D" in variable):
        output = "".join(["Combined 4D Bin",         " (Original)" if("OG" in variable) else ""])
    if("Bin_5D" in variable):
        output = "".join(["Combined 5D Bin",         " (Original)" if("OG" in variable) else ""])
    if("Bin_Res_4D" in variable):
        output = "".join(["Q^{2}-x_{B}-z-P_{T} Bin", " (Original)" if("OG" in variable) else ""])
    if("Combined_" in variable or "Multi_Dim" in variable):
        output = "".join(["Combined Binning: ", str(variable.replace("Combined_", ""))]).replace("Multi_Dim_", "")
        
    if(smeared_named == 'yes'):
        List_of_non_smearable_variables = ["esec", "pipsec", "prosec", "Hx", "Hy", "Hx_pip", "Hy_pip", "ele_x_DC_6", "ele_x_DC_18", "ele_x_DC_36", "pip_x_DC_6", "pip_x_DC_18", "pip_x_DC_36", "pro", "MM_pro", "V_PCal", "W_PCal", "U_PCal"]
        if(variable not in List_of_non_smearable_variables):
            output = "".join([output, " (Smeared)"])
        
    if(bank_named == 'yes'):
        output = "".join([output, " (Generated)"])
        
    if(Extra_Variable_Title not in [""]):
        output = "".join([str(Extra_Variable_Title), str(output)])
    
    if('error' in str(output)):
        print("".join(["A variable name was not recognized.\nPlease assign a new name for variable = ", str(variable)]))
        output = str(variable)

    return output

###################=========================###################
##===============##     Variable Titles     ##===============##
###################=========================###################


def Q2_xB_Border_Lines(Q2_xB_Bin_Select):
    # Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')
    # Notation used: points are given by [xB, Q2] in sets of 2 points so they can be used to create the appropriate TLines 
    # All (original) points are given in Table 4.2 on page 18 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl
    # Modifications made to Stefan's binning:
        # Size of some bins were reduced so that each bin did not have a minimum border value of Q2 < 2 (due to new cut)
        # One less Q2-xB bin (combined what was left of bin 1 with bin 3
            # The odd numbered bins are relabeled so that (example) the Q2-xB bin 5 defined by Stefan is now my Q2-xB bin 3 (the points above describe the only significant changes between Stefan's binning schemes and my own)
    Draw_Lines = []
    # Each appended list is defined in the following way:
        # Draw_Lines.append([[xB_Point_1, Q2_Point_1], [xB_Point_2, Q2_Point_2]])
    # To draw all bins, the input of this 'Q2_xB_Border_Lines' function should be Q2_xB_Bin_Select = -1
    # Any other value will draw just one single bin corresponding to the value of 'Q2_xB_Bin_Select'
    # For Q2_xB Bin 1
    if(Q2_xB_Bin_Select == 1 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.126602, 2], [0.15,     2.28]])
        Draw_Lines.append([[0.15,  2.28], [0.24,     3.625]])
        Draw_Lines.append([[0.24, 3.625], [0.24,     2.75]])
        Draw_Lines.append([[0.24,  2.75], [0.15,     2]])
        Draw_Lines.append([[0.15,     2], [0.126602, 2]])
    # For Q2_xB Bin 2
    if(Q2_xB_Bin_Select == 2 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.15,    2], [0.24, 2.75]])
        Draw_Lines.append([[0.24, 2.75], [0.24, 2]])
        Draw_Lines.append([[0.24,    2], [0.15, 2]])
    # For Q2_xB Bin 3
    if(Q2_xB_Bin_Select == 3 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.24,  2.75], [0.24, 3.625]])
        Draw_Lines.append([[0.24, 3.625], [0.34, 5.12]])
        Draw_Lines.append([[0.34,  5.12], [0.34, 3.63]])
        Draw_Lines.append([[0.34,  3.63], [0.24, 2.75]])
    # For Q2_xB Bin 4
    if(Q2_xB_Bin_Select == 4 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.24, 2], [0.24, 2.75]])
        Draw_Lines.append([[0.24, 2.75], [0.34, 3.63]])
        Draw_Lines.append([[0.34, 3.63], [0.34, 2]])
        Draw_Lines.append([[0.34, 2], [0.24, 2]])
    # For Q2_xB Bin 5
    if(Q2_xB_Bin_Select == 5 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.34, 3.63], [0.34, 5.12]])
        Draw_Lines.append([[0.34, 5.12], [0.45, 6.76]])
        Draw_Lines.append([[0.45, 6.76], [0.45, 4.7]])
        Draw_Lines.append([[0.45, 4.7], [0.34, 3.63]])
    # For Q2_xB Bin 6
    if(Q2_xB_Bin_Select == 6 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.34, 2], [0.34, 3.63]])
        Draw_Lines.append([[0.34, 3.63], [0.45, 4.7]])
        Draw_Lines.append([[0.45, 4.7], [0.45, 2.52]])
        Draw_Lines.append([[0.45, 2.52], [0.387826, 2]])
        Draw_Lines.append([[0.387826, 2], [0.34, 2]])
    # For Q2_xB Bin 7
    if(Q2_xB_Bin_Select == 7 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.45, 4.7], [0.45, 6.76]])
        Draw_Lines.append([[0.45, 6.76], [0.677, 10.185]])
        Draw_Lines.append([[0.677, 10.185], [0.7896, 11.351]])
        Draw_Lines.append([[0.7896, 11.351], [0.75, 9.52]])
        Draw_Lines.append([[0.75, 9.52], [0.708, 7.42]])
        Draw_Lines.append([[0.708, 7.42], [0.45, 4.7]])
    # For Q2_xB Bin 8
    if(Q2_xB_Bin_Select == 8 or Q2_xB_Bin_Select < 1):
        Draw_Lines.append([[0.45, 2.52], [0.45, 4.7]])
        Draw_Lines.append([[0.45, 4.7], [0.708, 7.42]])
        Draw_Lines.append([[0.708, 7.42], [0.64, 5.4]])
        Draw_Lines.append([[0.64, 5.4], [0.57, 4.05]])
        Draw_Lines.append([[0.57, 4.05], [0.50, 3.05]])
        Draw_Lines.append([[0.50, 3.05],[0.45, 2.52]])
    return Draw_Lines

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Q2_y_Border_Lines(Q2_y_Bin_Select):
    # Defining Borders for Q2 and y Bins (based on 'Q2_y_Bin_Select')
    # Notation used: points are given by [y, Q2] in sets of 2 points so they can be used to create the appropriate TLines 
    Draw_Lines = []
    ##=====####################=====##
    ##=====##   Q2 Group 1   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 2, 2.423
    # For Q2_y Bin 1
    if(Q2_y_Bin_Select == 1 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.75, Q2_max]])
        Draw_Lines.append([[0.75, Q2_max], [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 2
    if(Q2_y_Bin_Select == 2 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    # For Q2_y Bin 3
    if(Q2_y_Bin_Select == 3 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.45, Q2_min], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.55, Q2_min]])
        Draw_Lines.append([[0.55, Q2_min], [0.45, Q2_min]])
    # For Q2_y Bin 4
    if(Q2_y_Bin_Select == 4 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.3,  Q2_min], [0.3,  Q2_max]])
        Draw_Lines.append([[0.3,  Q2_max], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.45, Q2_min]])
        Draw_Lines.append([[0.45, Q2_min], [0.3,  Q2_min]])
    ##=====####################=====##
    ##=====##   Q2 Group 2   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 2.423, 2.987
    # For Q2_y Bin 5
    if(Q2_y_Bin_Select == 5 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.75, Q2_max]])
        Draw_Lines.append([[0.75, Q2_max], [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 6
    if(Q2_y_Bin_Select == 6 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    # For Q2_y Bin 7
    if(Q2_y_Bin_Select == 7 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.45, Q2_min], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.55, Q2_min]])
        Draw_Lines.append([[0.55, Q2_min], [0.45, Q2_min]])
    # For Q2_y Bin 8
    if(Q2_y_Bin_Select == 8 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.3,  Q2_min], [0.3,  Q2_max]])
        Draw_Lines.append([[0.3,  Q2_max], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.45, Q2_min]])
        Draw_Lines.append([[0.45, Q2_min], [0.3,  Q2_min]])
    ##=====####################=====##
    ##=====##   Q2 Group 3   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 2.987, 3.974
    # For Q2_y Bin 9
    if(Q2_y_Bin_Select == 9 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.75, Q2_max]])
        Draw_Lines.append([[0.75, Q2_max], [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 10
    if(Q2_y_Bin_Select == 10 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    # For Q2_y Bin 11
    if(Q2_y_Bin_Select == 11 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.45, Q2_min], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.55, Q2_min]])
        Draw_Lines.append([[0.55, Q2_min], [0.45, Q2_min]])
    # For Q2_y Bin 12
    if(Q2_y_Bin_Select == 12 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.35, Q2_min], [0.35, Q2_max]])
        Draw_Lines.append([[0.35, Q2_max], [0.45, Q2_max]])
        Draw_Lines.append([[0.45, Q2_max], [0.45, Q2_min]])
        Draw_Lines.append([[0.45, Q2_min], [0.35, Q2_min]])
    ##=====####################=====##
    ##=====##   Q2 Group 4   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 3.974, 5.384
    # For Q2_y Bin 13
    if(Q2_y_Bin_Select == 13 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.75, Q2_max]])
        Draw_Lines.append([[0.75, Q2_max], [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 14
    if(Q2_y_Bin_Select == 14 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    # For Q2_y Bin 15
    if(Q2_y_Bin_Select == 15 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.45, Q2_min], [0.45, 5.948]])
        Draw_Lines.append([[0.45, 5.948],  [0.55, 5.948]])
        Draw_Lines.append([[0.55, 5.948],  [0.55, Q2_min]])
        Draw_Lines.append([[0.55, Q2_min], [0.45, Q2_min]])
    ##=====####################=====##
    ##=====##   Q2 Group 5   ##=====##
    ##=====####################=====##
    Q2_min, Q2_max = 5.384, 7.922
    # For Q2_y Bin 16
    if(Q2_y_Bin_Select == 16 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.65, Q2_min], [0.65, 9.896]])
        Draw_Lines.append([[0.65, 9.896],  [0.75, 9.896]])
        Draw_Lines.append([[0.75, 9.896],  [0.75, Q2_min]])
        Draw_Lines.append([[0.75, Q2_min], [0.65, Q2_min]])
    # For Q2_y Bin 17
    if(Q2_y_Bin_Select == 17 or Q2_y_Bin_Select < 1):
        Draw_Lines.append([[0.55, Q2_min], [0.55, Q2_max]])
        Draw_Lines.append([[0.55, Q2_max], [0.65, Q2_max]])
        Draw_Lines.append([[0.65, Q2_max], [0.65, Q2_min]])
        Draw_Lines.append([[0.65, Q2_min], [0.55, Q2_min]])
    return Draw_Lines

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

# Rounded Q2 to the nearest 0.05 increment of the bin border
def Q2_Y_Border_Lines(Bin_In):
    Q2_min, Q2_max = 2.00, 2.40
    y_min,  y_max  = 0.65, 0.75
    ####=====######################=====####
    ####=====####  Q2 Group 1  ####=====####
    ####=====######################=====####
    if(Bin_In in range(1, 5, 1)):
        Q2_min, Q2_max = 2.00, 2.40
    ####=====######################=====####
    ####=====####  Q2 Group 2  ####=====####
    ####=====######################=====####
    if(Bin_In in range(5, 9, 1)):
        Q2_min, Q2_max = 2.40, 2.90
    ####=====######################=====####
    ####=====####  Q2 Group 3  ####=====####
    ####=====######################=====####
    if(Bin_In in range(9, 13, 1)):
        Q2_min, Q2_max = 2.90, 3.70
    ####=====######################=====####
    ####=====####  Q2 Group 4  ####=====####
    ####=====######################=====####
    if(Bin_In in range(13, 16, 1)):
        Q2_min, Q2_max = 3.70, 5.30
    ####=====######################=====####
    ####=====####  Q2 Group 5  ####=====####
    ####=====######################=====####
    if(Bin_In in range(16, 18, 1)):
        Q2_min, Q2_max = 5.30, 7.90
    ####=====#########################################=====####
    ####=====####  Q2 Group 0  -  Migration Bins  ####=====####
    ####=====#########################################=====####
    if(Bin_In in range(18, 24, 1)):
        Q2_min, Q2_max = 0.00, 2.00
    ####=====#########################################=====####
    ####=====####  Q2 Group 1.5 - Migration Bins  ####=====####
    ####=====#########################################=====####
    if(Bin_In in range(24, 26, 1)):
        Q2_min, Q2_max = 2.00, 2.40
    ####=====#########################################=====####
    ####=====####  Q2 Group 2.5 - Migration Bins  ####=====####
    ####=====#########################################=====####
    if(Bin_In in range(26, 28, 1)):
        Q2_min, Q2_max = 2.40, 2.90
    ####=====#########################################=====####
    ####=====####  Q2 Group 3.5 - Migration Bins  ####=====####
    ####=====#########################################=====####
    if(Bin_In in range(28, 30, 1)):
        Q2_min, Q2_max = 2.90, 3.70
    ####=====#########################################=====####
    ####=====####  Q2 Group 4.5 - Migration Bins  ####=====####
    ####=====#########################################=====####
    if(Bin_In in range(30, 33, 1)):
        Q2_min, Q2_max = 3.70, 5.30
    ####=====#########################################=====####
    ####=====####  Q2 Group 5.5 - Migration Bins  ####=====####
    ####=====#########################################=====####
    if(Bin_In in range(33, 36, 1)):
        Q2_min, Q2_max = 5.30, 7.90
    ####=====#########################################=====####
    ####=====####  Q2 Group 6  -  Migration Bins  ####=====####
    ####=====#########################################=====####
    if(Bin_In in range(36, 40, 1)):
        Q2_min, Q2_max = 7.90, 14.00
    ####=====######################=====####
    ####=====####  y  Group 1  ####=====####
    ####=====######################=====#### + Migration Bin(s)
    if(Bin_In in [1, 5,  9, 13, 16,            19, 37]):
        y_min, y_max = 0.65, 0.75
    ####=====######################=====####
    ####=====####  y  Group 2  ####=====####
    ####=====######################=====#### + Migration Bin(s)
    if(Bin_In in [2, 6, 10, 14, 17,            20, 38]):
        y_min, y_max = 0.55, 0.65
    ####=====######################=====####
    ####=====####  y  Group 3  ####=====####
    ####=====######################=====#### + Migration Bin(s)
    if(Bin_In in [3, 7, 11, 15,                21, 34, 39]):
        y_min, y_max = 0.45, 0.55
    ####=====######################=====####
    ####=====####  y  Group 4  ####=====####
    ####=====######################=====#### + Migration Bin(s)
    if(Bin_In in [4, 8, 12,                    22, 31, 35]):
        y_min, y_max = 0.35, 0.45
    ####=====#######################################=====####
    ####=====####  y  Group 0 - Migration Bins  ####=====####
    ####=====#######################################=====####
    if(Bin_In in [18, 24, 26, 28, 30, 33, 36]):
        y_min, y_max = 0.75, 0.99
    ####=====#######################################=====####
    ####=====####  y  Group 5 - Migration Bins  ####=====####
    ####=====#######################################=====####
    if(Bin_In in [23, 25, 27, 29, 32]):
        y_min, y_max = 0.1, 0.35
    return [Q2_max, Q2_min, y_max, y_min]

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Draw_Q2_Y_Bins(Input_Bin, line_width=3, Binning_Method_Input=Binning_Method, Use_xB=False):
    if("y_bin" in Binning_Method_Input):
        Borders_Q2_y = Q2_y_Border_Lines(Input_Bin)
        Q2_Max       = Borders_Q2_y[0][1][1]
        Q2_Min       = Borders_Q2_y[0][0][1]
        y_Max        = Borders_Q2_y[1][1][0]
        y_Min        = Borders_Q2_y[1][0][0]
    else:
        Q2_Max, Q2_Min, y_Max, y_Min = Q2_Y_Border_Lines(Input_Bin)
    if(Use_xB):
        Constant = 0.5/(0.938272*10.6)
        # For Max Q2
        xB_Min_Upper = Constant*(Q2_Max/y_Max)
        xB_Max_Upper = Constant*(Q2_Max/y_Min)
        # For Min Q2
        xB_Min_Lower = Constant*(Q2_Min/y_Max)
        xB_Max_Lower = Constant*(Q2_Min/y_Min)
        TLine_U = ROOT.TLine(xB_Min_Upper, Q2_Max, xB_Max_Upper, Q2_Max)
        TLine_D = ROOT.TLine(xB_Min_Lower, Q2_Min, xB_Max_Lower, Q2_Min)
        TLine_L = ROOT.TLine(xB_Min_Lower, Q2_Min, xB_Min_Upper, Q2_Max)
        TLine_R = ROOT.TLine(xB_Max_Lower, Q2_Min, xB_Max_Upper, Q2_Max)
    else:
        TLine_U = ROOT.TLine(y_Min, Q2_Max, y_Max, Q2_Max)
        TLine_D = ROOT.TLine(y_Min, Q2_Min, y_Max, Q2_Min)
        TLine_L = ROOT.TLine(y_Min, Q2_Min, y_Min, Q2_Max)
        TLine_R = ROOT.TLine(y_Max, Q2_Min, y_Max, Q2_Max)
    for Line in [TLine_U, TLine_D, TLine_L, TLine_R]:
        Line.SetLineWidth(line_width)
        if(Input_Bin in range(1, 18, 1)):
            Line.SetLineColor(1 if(line_width in [1, 2, 3]) else 3)
        elif(Input_Bin > 17):
            Line.SetLineColor(2)
            if(line_width in [2, 3]):
                Line.SetLineWidth(line_width - 1)
    return [TLine_U, TLine_D, TLine_L, TLine_R]

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

# For my 2D z-pT binning
def z_pT_Border_Lines(Q2_y_Bin_Select, Binning_Method_Input=Binning_Method):
    z_Borders  = [0.15, 0.70]
    pT_Borders = [0.05, 1.0]
    Num_z_Borders, Num_pT_Borders = 1, 1
    if("y_bin" in Binning_Method_Input):
        # Defining Borders for z and pT Bins (based on 'Q2_y_Bin')
        # For Q2-y Bin 1
        if(Q2_y_Bin_Select == 1):
            z_Borders  = [0.15, 0.20, 0.24, 0.29, 0.40, 0.73]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        # For Q2-y Bin 2
        if(Q2_y_Bin_Select == 2):
            z_Borders  = [0.18, 0.23, 0.26, 0.31, 0.38, 0.50, 0.74]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        # For Q2-y Bin 3
        if(Q2_y_Bin_Select == 3):
            z_Borders  = [0.22, 0.28, 0.35, 0.45, 0.60, 0.78]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        # For Q2-y Bin 4
        if(Q2_y_Bin_Select == 4):
            z_Borders  = [0.26, 0.32, 0.37, 0.43, 0.50, 0.60, 0.71]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80]
        # For Q2-y Bin 5
        if(Q2_y_Bin_Select == 5):
            z_Borders  = [0.15, 0.19, 0.24, 0.29, 0.38, 0.50, 0.73]
            pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]
        # For Q2-y Bin 6
        if(Q2_y_Bin_Select == 6):
            z_Borders  = [0.18, 0.23, 0.30, 0.39, 0.50, 0.78]
            pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0]
        # For Q2-y Bin 7
        if(Q2_y_Bin_Select == 7):
            z_Borders  = [0.21, 0.26, 0.30, 0.44, 0.55, 0.78]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.65, 1.0]
        # For Q2-y Bin 8
        if(Q2_y_Bin_Select in [8]):
            z_Borders  = [0.26, 0.32, 0.36, 0.40, 0.45, 0.53, 0.72]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.52, 0.75]
        # For Q2-y Bin 9
        if(Q2_y_Bin_Select in [9]):
            z_Borders  = [0.15, 0.20, 0.24, 0.30, 0.38, 0.48, 0.72]
            pT_Borders = [0.05, 0.22, 0.30, 0.38, 0.46, 0.60, 0.95]
        # For Q2-y Bin 10
        if(Q2_y_Bin_Select in [10]):
            z_Borders  = [0.18, 0.23, 0.26, 0.32, 0.40, 0.50, 0.72]
            pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.00]
        # For Q2-y Bin 11
        if(Q2_y_Bin_Select in [11]):
            z_Borders  = [0.21, 0.26, 0.32, 0.40, 0.50, 0.70]
            pT_Borders = [0.05, 0.20, 0.31, 0.40, 0.50, 0.64, 0.95]
        # For Q2-y Bin 12
        if(Q2_y_Bin_Select in [12]):
            z_Borders  = [0.26, 0.32, 0.40, 0.50, 0.70]
            pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.67]
        # For Q2-y Bin 13
        if(Q2_y_Bin_Select in [13]):
            z_Borders  = [0.15, 0.20, 0.24, 0.30, 0.40, 0.72]
            pT_Borders = [0.05, 0.23, 0.34, 0.43, 0.55, 0.90]
        # For Q2-y Bin 14
        if(Q2_y_Bin_Select in [14]):
            z_Borders  = [0.18, 0.23, 0.27, 0.33, 0.44, 0.74]
            pT_Borders = [0.05, 0.23, 0.34, 0.44, 0.55, 0.90]
        # For Q2-y Bin 15
        if(Q2_y_Bin_Select in [15]):
            z_Borders  = [0.21, 0.28, 0.35, 0.47, 0.72]
            pT_Borders = [0.05, 0.23, 0.34, 0.45, 0.58, 0.90]
        # For Q2-y Bin 16
        if(Q2_y_Bin_Select in [16]):
            z_Borders  = [0.15, 0.20, 0.25, 0.32, 0.41, 0.71]
            pT_Borders = [0.05, 0.24, 0.36, 0.55, 0.80]
        # For Q2-y Bin 17
        if(Q2_y_Bin_Select in [17]):
            z_Borders  = [0.18, 0.23, 0.30, 0.38, 0.48, 0.72]
            pT_Borders = [0.05, 0.23, 0.36, 0.51, 0.85]
        Num_z_Borders  = len(z_Borders)
        Num_pT_Borders = len(pT_Borders)
        # For Q2-y Bin 0 and -1
        if((Q2_y_Bin_Select < 1) or (Q2_y_Bin_Select > 17)):
            z_Borders      = [0.15, 0.70]
            pT_Borders     = [0.05, 1.0]
            Num_z_Borders, Num_pT_Borders = 1, 1
        if(Q2_y_Bin_Select == 0):
            print("ERROR")
        
##=========================================================================================##
    else:
        Q2_y_Bin_In = Q2_y_Bin_Select
        # Defining Borders for z and pT Bins (based on 'Q2_Y_Bin')
        # For Q2-y Bin 1
        if(Q2_y_Bin_In == 1):
            z_Borders  = [0.16, 0.20, 0.24, 0.31, 0.41, 0.70]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
        # For Q2-y Bin 2
        if(Q2_y_Bin_In == 2):
            z_Borders  = [0.19, 0.23, 0.26, 0.31, 0.38, 0.50, 0.75]
            pT_Borders = [0.05, 0.25, 0.35, 0.45, 0.54, 0.67, 0.93]
        # For Q2-y Bin 3
        if(Q2_y_Bin_In == 3):
            z_Borders  = [0.22, 0.28, 0.35, 0.45, 0.70]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75]
        # For Q2-y Bin 4
        if(Q2_y_Bin_In == 4):
            z_Borders  = [0.26, 0.34, 0.38, 0.43, 0.50, 0.60]
            pT_Borders = [0.05, 0.20, 0.29, 0.38, 0.48, 0.61]
        # For Q2-y Bin 5
        if(Q2_y_Bin_In == 5):
            z_Borders  = [0.16, 0.20, 0.24, 0.30, 0.38, 0.49, 0.72]
            pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 0.98]
        # For Q2-y Bin 6
        if(Q2_y_Bin_In == 6):
            z_Borders  = [0.18, 0.23, 0.28, 0.35, 0.45, 0.75]
            pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.05]
        # For Q2-y Bin 7
        if(Q2_y_Bin_In == 7):
            z_Borders  = [0.22, 0.28, 0.33, 0.40, 0.51, 0.70]
            pT_Borders = [0.05, 0.20, 0.29, 0.38, 0.48, 0.60, 0.83]
        # For Q2-y Bin 8
        if(Q2_y_Bin_In in [8]):
            z_Borders  = [0.27, 0.32, 0.36, 0.40, 0.45, 0.50, 0.60]
            pT_Borders = [0.05, 0.21, 0.31, 0.40, 0.50]
        # For Q2-y Bin 9
        if(Q2_y_Bin_In in [9]):
            z_Borders  = [0.16, 0.20, 0.24, 0.30, 0.42, 0.70]
            pT_Borders = [0.05, 0.22, 0.30, 0.38, 0.46, 0.58, 0.74, 0.95]
        # For Q2-y Bin 10
        if(Q2_y_Bin_In in [10]):
            z_Borders  = [0.19, 0.23, 0.26, 0.32, 0.40, 0.50, 0.72]
            pT_Borders = [0.05, 0.21, 0.31, 0.40, 0.50, 0.64, 0.90]
        # For Q2-y Bin 11
        if(Q2_y_Bin_In in [11]):
            z_Borders  = [0.22, 0.27, 0.32, 0.40, 0.53, 0.69]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.54, 0.69]
        # For Q2-y Bin 12
        if(Q2_y_Bin_In in [12]):
            z_Borders  = [0.27, 0.31, 0.35, 0.40, 0.50, 0.70]
            pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.67]
        # For Q2-y Bin 13
        if(Q2_y_Bin_In in [13]):
            z_Borders  = [0.00, 0.16, 0.20, 0.24, 0.29, 0.36, 0.51, 0.72]
            pT_Borders = [0.05, 0.22, 0.35, 0.45, 0.60, 0.90]
        # For Q2-y Bin 14
        if(Q2_y_Bin_In in [14]):
            z_Borders  = [0.19, 0.23, 0.27, 0.32, 0.40, 0.53, 0.69]
            pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.65, 0.80]
        # For Q2-y Bin 15
        if(Q2_y_Bin_In in [15]):
            z_Borders  = [0.22, 0.28, 0.33, 0.40, 0.51, 0.72]
            pT_Borders = [0.05, 0.23, 0.33, 0.47, 0.90]
        # For Q2-y Bin 16
        if(Q2_y_Bin_In in [16]):
            z_Borders  = [0.16, 0.20, 0.24, 0.29, 0.36, 0.45, 0.62]
            pT_Borders = [0.05, 0.22, 0.31, 0.44, 0.70, 1.00]
        # For Q2-y Bin 17
        if(Q2_y_Bin_In in [17]):
            z_Borders  = [0.19, 0.23, 0.29, 0.35, 0.45, 0.72]
            pT_Borders = [0.05, 0.19, 0.28, 0.37, 0.85]
        Num_z_Borders  = len(z_Borders)
        Num_pT_Borders = len(pT_Borders)
        # For Q2-y Bin 0 and -1
        if((Q2_y_Bin_In < 1) or (Q2_y_Bin_In > 17)):
            z_Borders  = [0.15, 0.70]
            pT_Borders = [0.05, 1.0]
            Num_z_Borders, Num_pT_Borders = 1, 1
        if(Q2_y_Bin_In == 0):
            print("ERROR")
##=========================================================================================##
                    # Info about z bins              # Info about pT bins         # Total number of z-pT bins
    output = [['z', Num_z_Borders, z_Borders], ['pT', Num_pT_Borders, pT_Borders], (Num_z_Borders-1)*(Num_pT_Borders-1)]
    return output

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

# Rounded z and pT to the nearest 0.01 increment of the bin border
def z_pT_Border_Lines_New(Q2_y_Bin_In):
    # Defining Borders for z and pT Bins (based on the test version of 'Q2_y_Bin')
    # For Q2-y Bin 1
    if(Q2_y_Bin_In == 1):
        z_Borders  = [0.16, 0.20, 0.24, 0.31, 0.41, 0.70]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0]
    # For Q2-y Bin 2
    if(Q2_y_Bin_In == 2):
        z_Borders  = [0.19, 0.23, 0.26, 0.31, 0.38, 0.50, 0.75]
        pT_Borders = [0.05, 0.25, 0.35, 0.45, 0.54, 0.67, 0.93]
    # For Q2-y Bin 3
    if(Q2_y_Bin_In == 3):
        z_Borders  = [0.22, 0.28, 0.35, 0.45, 0.70]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75]
    # For Q2-y Bin 4
    if(Q2_y_Bin_In == 4):
        z_Borders  = [0.26, 0.34, 0.38, 0.43, 0.50, 0.60]
        pT_Borders = [0.05, 0.20, 0.29, 0.38, 0.48, 0.61]
    # For Q2-y Bin 5
    if(Q2_y_Bin_In == 5):
        z_Borders  = [0.16, 0.20, 0.24, 0.30, 0.38, 0.49, 0.72]
        pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 0.98]
    # For Q2-y Bin 6
    if(Q2_y_Bin_In == 6):
        z_Borders  = [0.18, 0.23, 0.28, 0.35, 0.45, 0.75]
        pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.05]
    # For Q2-y Bin 7
    if(Q2_y_Bin_In == 7):
        z_Borders  = [0.22, 0.28, 0.33, 0.40, 0.51, 0.70]
        pT_Borders = [0.05, 0.20, 0.29, 0.38, 0.48, 0.60, 0.83]
    # For Q2-y Bin 8
    if(Q2_y_Bin_In in [8]):
        z_Borders  = [0.27, 0.32, 0.36, 0.40, 0.45, 0.50, 0.60]
        pT_Borders = [0.05, 0.21, 0.31, 0.40, 0.50]
    # For Q2-y Bin 9
    if(Q2_y_Bin_In in [9]):
        z_Borders  = [0.16, 0.20, 0.24, 0.30, 0.42, 0.70]
        pT_Borders = [0.05, 0.22, 0.30, 0.38, 0.46, 0.58, 0.74, 0.95]
    # For Q2-y Bin 10
    if(Q2_y_Bin_In in [10]):
        z_Borders  = [0.19, 0.23, 0.26, 0.32, 0.40, 0.50, 0.72]
        pT_Borders = [0.05, 0.21, 0.31, 0.40, 0.50, 0.64, 0.90]
    # For Q2-y Bin 11
    if(Q2_y_Bin_In in [11]):
        z_Borders  = [0.22, 0.27, 0.32, 0.40, 0.53, 0.69]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.54, 0.69]
    # For Q2-y Bin 12
    if(Q2_y_Bin_In in [12]):
        z_Borders  = [0.27, 0.31, 0.35, 0.40, 0.50, 0.70]
        pT_Borders = [0.05, 0.22, 0.32, 0.41, 0.67]
    # For Q2-y Bin 13
    if(Q2_y_Bin_In in [13]):
        z_Borders  = [0.00, 0.16, 0.20, 0.24, 0.29, 0.36, 0.51, 0.72]
        pT_Borders = [0.05, 0.22, 0.35, 0.45, 0.60, 0.90]
    # For Q2-y Bin 14
    if(Q2_y_Bin_In in [14]):
        z_Borders  = [0.19, 0.23, 0.27, 0.32, 0.40, 0.53, 0.69]
        pT_Borders = [0.05, 0.20, 0.30, 0.40, 0.50, 0.65, 0.80]
    # For Q2-y Bin 15
    if(Q2_y_Bin_In in [15]):
        z_Borders  = [0.22, 0.28, 0.33, 0.40, 0.51, 0.72]
        pT_Borders = [0.05, 0.23, 0.33, 0.47, 0.90]
    # For Q2-y Bin 16
    if(Q2_y_Bin_In in [16]):
        z_Borders  = [0.16, 0.20, 0.24, 0.29, 0.36, 0.45, 0.62]
        pT_Borders = [0.05, 0.22, 0.31, 0.44, 0.70, 1.00]
    # For Q2-y Bin 17
    if(Q2_y_Bin_In in [17]):
        z_Borders  = [0.19, 0.23, 0.29, 0.35, 0.45, 0.72]
        pT_Borders = [0.05, 0.19, 0.28, 0.37, 0.85]
    Num_z_Borders  = len(z_Borders)
    Num_pT_Borders = len(pT_Borders)
    # For Q2-y Bin 0 and -1
    if((Q2_y_Bin_In < 1) or (Q2_y_Bin_In > 17)):
        z_Borders  = [0.15, 0.70]
        pT_Borders = [0.05, 1.0]
        Num_z_Borders, Num_pT_Borders = 1, 1
    if(Q2_y_Bin_In == 0):
        print("ERROR")
                    # Info about z bins              # Info about pT bins         # Total number of z-pT bins
    output = [['z', Num_z_Borders, z_Borders], ['pT', Num_pT_Borders, pT_Borders], (Num_z_Borders-1)*(Num_pT_Borders-1)]
    return output

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

Bin_Definition_Array = {'Q2-y=1, z-pT=1': [0.71, 0.4, 0.22, 0.05], 'Q2-y=1, z-pT=2': [0.71, 0.4, 0.32, 0.22], 'Q2-y=1, z-pT=3': [0.71, 0.4, 0.42, 0.32], 'Q2-y=1, z-pT=4': [0.71, 0.4, 0.52, 0.42], 'Q2-y=1, z-pT=5': [0.71, 0.4, 0.63, 0.52], 'Q2-y=1, z-pT=6': [0.71, 0.4, 0.75, 0.63], 'Q2-y=1, z-pT=7': [0.71, 0.4, 0.99, 0.75], 'Q2-y=1, z-pT=8': [0.4, 0.29, 0.22, 0.05], 'Q2-y=1, z-pT=9': [0.4, 0.29, 0.32, 0.22], 'Q2-y=1, z-pT=10': [0.4, 0.29, 0.42, 0.32], 'Q2-y=1, z-pT=11': [0.4, 0.29, 0.52, 0.42], 'Q2-y=1, z-pT=12': [0.4, 0.29, 0.63, 0.52], 'Q2-y=1, z-pT=13': [0.4, 0.29, 0.75, 0.63], 'Q2-y=1, z-pT=14': [0.4, 0.29, 0.99, 0.75], 'Q2-y=1, z-pT=15': [0.29, 0.23, 0.22, 0.05], 'Q2-y=1, z-pT=16': [0.29, 0.23, 0.32, 0.22], 'Q2-y=1, z-pT=17': [0.29, 0.23, 0.42, 0.32], 'Q2-y=1, z-pT=18': [0.29, 0.23, 0.52, 0.42], 'Q2-y=1, z-pT=19': [0.29, 0.23, 0.63, 0.52], 'Q2-y=1, z-pT=20': [0.29, 0.23, 0.75, 0.63], 'Q2-y=1, z-pT=21 - REMOVE - MIGRATION BIN': [0.29, 0.23, 0.99, 0.75], 'Q2-y=1, z-pT=22': [0.23, 0.19, 0.22, 0.05], 'Q2-y=1, z-pT=23': [0.23, 0.19, 0.32, 0.22], 'Q2-y=1, z-pT=24': [0.23, 0.19, 0.42, 0.32], 'Q2-y=1, z-pT=25': [0.23, 0.19, 0.52, 0.42], 'Q2-y=1, z-pT=26': [0.23, 0.19, 0.63, 0.52], 'Q2-y=1, z-pT=27 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.75, 0.63], 'Q2-y=1, z-pT=28 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.99, 0.75], 'Q2-y=1, z-pT=29': [0.19, 0.16, 0.22, 0.05], 'Q2-y=1, z-pT=30': [0.19, 0.16, 0.32, 0.22], 'Q2-y=1, z-pT=31': [0.19, 0.16, 0.42, 0.32], 'Q2-y=1, z-pT=32': [0.19, 0.16, 0.52, 0.42], 'Q2-y=1, z-pT=33 - REMOVE - MIGRATION BIN': [0.19, 0.16, 0.63, 0.52], 'Q2-y=1, z-pT=34 - REMOVE - MIGRATION BIN': [0.19, 0.16, 0.75, 0.63], 'Q2-y=1, z-pT=35 - REMOVE - MIGRATION BIN': [0.19, 0.16, 0.99, 0.75], 'Q2-y=2, z-pT=1': [0.75, 0.5, 0.25, 0.05], 'Q2-y=2, z-pT=2': [0.75, 0.5, 0.35, 0.25], 'Q2-y=2, z-pT=3': [0.75, 0.5, 0.45, 0.35], 'Q2-y=2, z-pT=4': [0.75, 0.5, 0.54, 0.45], 'Q2-y=2, z-pT=5': [0.75, 0.5, 0.67, 0.54], 'Q2-y=2, z-pT=6': [0.75, 0.5, 0.93, 0.67], 'Q2-y=2, z-pT=7': [0.5, 0.38, 0.25, 0.05], 'Q2-y=2, z-pT=8': [0.5, 0.38, 0.35, 0.25], 'Q2-y=2, z-pT=9': [0.5, 0.38, 0.45, 0.35], 'Q2-y=2, z-pT=10': [0.5, 0.38, 0.54, 0.45], 'Q2-y=2, z-pT=11': [0.5, 0.38, 0.67, 0.54], 'Q2-y=2, z-pT=12': [0.5, 0.38, 0.93, 0.67], 'Q2-y=2, z-pT=13': [0.38, 0.31, 0.25, 0.05], 'Q2-y=2, z-pT=14': [0.38, 0.31, 0.35, 0.25], 'Q2-y=2, z-pT=15': [0.38, 0.31, 0.45, 0.35], 'Q2-y=2, z-pT=16': [0.38, 0.31, 0.54, 0.45], 'Q2-y=2, z-pT=17': [0.38, 0.31, 0.67, 0.54], 'Q2-y=2, z-pT=18': [0.38, 0.31, 0.93, 0.67], 'Q2-y=2, z-pT=19': [0.31, 0.26, 0.25, 0.05], 'Q2-y=2, z-pT=20': [0.31, 0.26, 0.35, 0.25], 'Q2-y=2, z-pT=21': [0.31, 0.26, 0.45, 0.35], 'Q2-y=2, z-pT=22': [0.31, 0.26, 0.54, 0.45], 'Q2-y=2, z-pT=23': [0.31, 0.26, 0.67, 0.54], 'Q2-y=2, z-pT=24 - REMOVE - MIGRATION BIN': [0.31, 0.26, 0.93, 0.67], 'Q2-y=2, z-pT=25': [0.26, 0.23, 0.25, 0.05], 'Q2-y=2, z-pT=26': [0.26, 0.23, 0.35, 0.25], 'Q2-y=2, z-pT=27': [0.26, 0.23, 0.45, 0.35], 'Q2-y=2, z-pT=28': [0.26, 0.23, 0.54, 0.45], 'Q2-y=2, z-pT=29': [0.26, 0.23, 0.67, 0.54], 'Q2-y=2, z-pT=30 - REMOVE - MIGRATION BIN': [0.26, 0.23, 0.93, 0.67], 'Q2-y=2, z-pT=31': [0.23, 0.19, 0.25, 0.05], 'Q2-y=2, z-pT=32': [0.23, 0.19, 0.35, 0.25], 'Q2-y=2, z-pT=33': [0.23, 0.19, 0.45, 0.35], 'Q2-y=2, z-pT=34': [0.23, 0.19, 0.54, 0.45], 'Q2-y=2, z-pT=35 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.67, 0.54], 'Q2-y=2, z-pT=36 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.93, 0.67], 'Q2-y=3, z-pT=1': [0.75, 0.56, 0.2, 0.05], 'Q2-y=3, z-pT=2': [0.75, 0.56, 0.3, 0.2], 'Q2-y=3, z-pT=3': [0.75, 0.56, 0.39, 0.3], 'Q2-y=3, z-pT=4': [0.75, 0.56, 0.49, 0.39], 'Q2-y=3, z-pT=5': [0.75, 0.56, 0.59, 0.49], 'Q2-y=3, z-pT=6': [0.75, 0.56, 0.76, 0.59], 'Q2-y=3, z-pT=7': [0.56, 0.41, 0.2, 0.05], 'Q2-y=3, z-pT=8': [0.56, 0.41, 0.3, 0.2], 'Q2-y=3, z-pT=9': [0.56, 0.41, 0.39, 0.3], 'Q2-y=3, z-pT=10': [0.56, 0.41, 0.49, 0.39], 'Q2-y=3, z-pT=11': [0.56, 0.41, 0.59, 0.49], 'Q2-y=3, z-pT=12': [0.56, 0.41, 0.76, 0.59], 'Q2-y=3, z-pT=13': [0.41, 0.33, 0.2, 0.05], 'Q2-y=3, z-pT=14': [0.41, 0.33, 0.3, 0.2], 'Q2-y=3, z-pT=15': [0.41, 0.33, 0.39, 0.3], 'Q2-y=3, z-pT=16': [0.41, 0.33, 0.49, 0.39], 'Q2-y=3, z-pT=17': [0.41, 0.33, 0.59, 0.49], 'Q2-y=3, z-pT=18': [0.41, 0.33, 0.76, 0.59], 'Q2-y=3, z-pT=19': [0.33, 0.28, 0.2, 0.05], 'Q2-y=3, z-pT=20': [0.33, 0.28, 0.3, 0.2], 'Q2-y=3, z-pT=21': [0.33, 0.28, 0.39, 0.3], 'Q2-y=3, z-pT=22': [0.33, 0.28, 0.49, 0.39], 'Q2-y=3, z-pT=23': [0.33, 0.28, 0.59, 0.49], 'Q2-y=3, z-pT=24': [0.33, 0.28, 0.76, 0.59], 'Q2-y=3, z-pT=25': [0.28, 0.22, 0.2, 0.05], 'Q2-y=3, z-pT=26': [0.28, 0.22, 0.3, 0.2], 'Q2-y=3, z-pT=27': [0.28, 0.22, 0.39, 0.3], 'Q2-y=3, z-pT=28': [0.28, 0.22, 0.49, 0.39], 'Q2-y=3, z-pT=29': [0.28, 0.22, 0.59, 0.49], 'Q2-y=3, z-pT=30 - REMOVE - MIGRATION BIN': [0.28, 0.22, 0.76, 0.59], 'Q2-y=4, z-pT=1': [0.71, 0.59, 0.2, 0.05], 'Q2-y=4, z-pT=2': [0.71, 0.59, 0.29, 0.2], 'Q2-y=4, z-pT=3': [0.71, 0.59, 0.38, 0.29], 'Q2-y=4, z-pT=4': [0.71, 0.59, 0.48, 0.38], 'Q2-y=4, z-pT=5': [0.71, 0.59, 0.61, 0.48], 'Q2-y=4, z-pT=6 - REMOVE - MIGRATION BIN': [0.71, 0.59, 0.85, 0.61], 'Q2-y=4, z-pT=7': [0.59, 0.5, 0.2, 0.05], 'Q2-y=4, z-pT=8': [0.59, 0.5, 0.29, 0.2], 'Q2-y=4, z-pT=9': [0.59, 0.5, 0.38, 0.29], 'Q2-y=4, z-pT=10': [0.59, 0.5, 0.48, 0.38], 'Q2-y=4, z-pT=11': [0.59, 0.5, 0.61, 0.48], 'Q2-y=4, z-pT=12': [0.59, 0.5, 0.85, 0.61], 'Q2-y=4, z-pT=13': [0.5, 0.43, 0.2, 0.05], 'Q2-y=4, z-pT=14': [0.5, 0.43, 0.29, 0.2], 'Q2-y=4, z-pT=15': [0.5, 0.43, 0.38, 0.29], 'Q2-y=4, z-pT=16': [0.5, 0.43, 0.48, 0.38], 'Q2-y=4, z-pT=17': [0.5, 0.43, 0.61, 0.48], 'Q2-y=4, z-pT=18': [0.5, 0.43, 0.85, 0.61], 'Q2-y=4, z-pT=19': [0.43, 0.38, 0.2, 0.05], 'Q2-y=4, z-pT=20': [0.43, 0.38, 0.29, 0.2], 'Q2-y=4, z-pT=21': [0.43, 0.38, 0.38, 0.29], 'Q2-y=4, z-pT=22': [0.43, 0.38, 0.48, 0.38], 'Q2-y=4, z-pT=23': [0.43, 0.38, 0.61, 0.48], 'Q2-y=4, z-pT=24': [0.43, 0.38, 0.85, 0.61], 'Q2-y=4, z-pT=25': [0.38, 0.33, 0.2, 0.05], 'Q2-y=4, z-pT=26': [0.38, 0.33, 0.29, 0.2], 'Q2-y=4, z-pT=27': [0.38, 0.33, 0.38, 0.29], 'Q2-y=4, z-pT=28': [0.38, 0.33, 0.48, 0.38], 'Q2-y=4, z-pT=29': [0.38, 0.33, 0.61, 0.48], 'Q2-y=4, z-pT=30 - REMOVE - MIGRATION BIN': [0.38, 0.33, 0.85, 0.61], 'Q2-y=4, z-pT=31': [0.33, 0.26, 0.2, 0.05], 'Q2-y=4, z-pT=32': [0.33, 0.26, 0.29, 0.2], 'Q2-y=4, z-pT=33': [0.33, 0.26, 0.38, 0.29], 'Q2-y=4, z-pT=34': [0.33, 0.26, 0.48, 0.38], 'Q2-y=4, z-pT=35': [0.33, 0.26, 0.61, 0.48], 'Q2-y=4, z-pT=36 - REMOVE - MIGRATION BIN': [0.33, 0.26, 0.85, 0.61], 'Q2-y=5, z-pT=1': [0.72, 0.49, 0.22, 0.05], 'Q2-y=5, z-pT=2': [0.72, 0.49, 0.32, 0.22], 'Q2-y=5, z-pT=3': [0.72, 0.49, 0.41, 0.32], 'Q2-y=5, z-pT=4': [0.72, 0.49, 0.51, 0.41], 'Q2-y=5, z-pT=5': [0.72, 0.49, 0.65, 0.51], 'Q2-y=5, z-pT=6': [0.72, 0.49, 0.98, 0.65], 'Q2-y=5, z-pT=7': [0.49, 0.38, 0.22, 0.05], 'Q2-y=5, z-pT=8': [0.49, 0.38, 0.32, 0.22], 'Q2-y=5, z-pT=9': [0.49, 0.38, 0.41, 0.32], 'Q2-y=5, z-pT=10': [0.49, 0.38, 0.51, 0.41], 'Q2-y=5, z-pT=11': [0.49, 0.38, 0.65, 0.51], 'Q2-y=5, z-pT=12': [0.49, 0.38, 0.98, 0.65], 'Q2-y=5, z-pT=13': [0.38, 0.3, 0.22, 0.05], 'Q2-y=5, z-pT=14': [0.38, 0.3, 0.32, 0.22], 'Q2-y=5, z-pT=15': [0.38, 0.3, 0.41, 0.32], 'Q2-y=5, z-pT=16': [0.38, 0.3, 0.51, 0.41], 'Q2-y=5, z-pT=17': [0.38, 0.3, 0.65, 0.51], 'Q2-y=5, z-pT=18': [0.38, 0.3, 0.98, 0.65], 'Q2-y=5, z-pT=19': [0.3, 0.24, 0.22, 0.05], 'Q2-y=5, z-pT=20': [0.3, 0.24, 0.32, 0.22], 'Q2-y=5, z-pT=21': [0.3, 0.24, 0.41, 0.32], 'Q2-y=5, z-pT=22': [0.3, 0.24, 0.51, 0.41], 'Q2-y=5, z-pT=23': [0.3, 0.24, 0.65, 0.51], 'Q2-y=5, z-pT=24 - REMOVE - MIGRATION BIN': [0.3, 0.24, 0.98, 0.65], 'Q2-y=5, z-pT=25': [0.24, 0.2, 0.22, 0.05], 'Q2-y=5, z-pT=26': [0.24, 0.2, 0.32, 0.22], 'Q2-y=5, z-pT=27': [0.24, 0.2, 0.41, 0.32], 'Q2-y=5, z-pT=28': [0.24, 0.2, 0.51, 0.41], 'Q2-y=5, z-pT=29': [0.24, 0.2, 0.65, 0.51], 'Q2-y=5, z-pT=30 - REMOVE - MIGRATION BIN': [0.24, 0.2, 0.98, 0.65], 'Q2-y=5, z-pT=31': [0.2, 0.16, 0.22, 0.05], 'Q2-y=5, z-pT=32': [0.2, 0.16, 0.32, 0.22], 'Q2-y=5, z-pT=33': [0.2, 0.16, 0.41, 0.32], 'Q2-y=5, z-pT=34': [0.2, 0.16, 0.51, 0.41], 'Q2-y=5, z-pT=35 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.65, 0.51], 'Q2-y=5, z-pT=36 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.98, 0.65], 'Q2-y=6, z-pT=1': [0.72, 0.45, 0.22, 0.05], 'Q2-y=6, z-pT=2': [0.72, 0.45, 0.32, 0.22], 'Q2-y=6, z-pT=3': [0.72, 0.45, 0.41, 0.32], 'Q2-y=6, z-pT=4': [0.72, 0.45, 0.51, 0.41], 'Q2-y=6, z-pT=5': [0.72, 0.45, 0.65, 0.51], 'Q2-y=6, z-pT=6': [0.72, 0.45, 1.0, 0.65], 'Q2-y=6, z-pT=7': [0.45, 0.35, 0.22, 0.05], 'Q2-y=6, z-pT=8': [0.45, 0.35, 0.32, 0.22], 'Q2-y=6, z-pT=9': [0.45, 0.35, 0.41, 0.32], 'Q2-y=6, z-pT=10': [0.45, 0.35, 0.51, 0.41], 'Q2-y=6, z-pT=11': [0.45, 0.35, 0.65, 0.51], 'Q2-y=6, z-pT=12': [0.45, 0.35, 1.0, 0.65], 'Q2-y=6, z-pT=13': [0.35, 0.28, 0.22, 0.05], 'Q2-y=6, z-pT=14': [0.35, 0.28, 0.32, 0.22], 'Q2-y=6, z-pT=15': [0.35, 0.28, 0.41, 0.32], 'Q2-y=6, z-pT=16': [0.35, 0.28, 0.51, 0.41], 'Q2-y=6, z-pT=17': [0.35, 0.28, 0.65, 0.51], 'Q2-y=6, z-pT=18 - REMOVE - MIGRATION BIN': [0.35, 0.28, 1.0, 0.65], 'Q2-y=6, z-pT=19': [0.28, 0.23, 0.22, 0.05], 'Q2-y=6, z-pT=20': [0.28, 0.23, 0.32, 0.22], 'Q2-y=6, z-pT=21': [0.28, 0.23, 0.41, 0.32], 'Q2-y=6, z-pT=22': [0.28, 0.23, 0.51, 0.41], 'Q2-y=6, z-pT=23': [0.28, 0.23, 0.65, 0.51], 'Q2-y=6, z-pT=24 - REMOVE - MIGRATION BIN': [0.28, 0.23, 1.0, 0.65], 'Q2-y=6, z-pT=25': [0.23, 0.18, 0.22, 0.05], 'Q2-y=6, z-pT=26': [0.23, 0.18, 0.32, 0.22], 'Q2-y=6, z-pT=27': [0.23, 0.18, 0.41, 0.32], 'Q2-y=6, z-pT=28': [0.23, 0.18, 0.51, 0.41], 'Q2-y=6, z-pT=29 - REMOVE - MIGRATION BIN': [0.23, 0.18, 0.65, 0.51], 'Q2-y=6, z-pT=30 - REMOVE - MIGRATION BIN': [0.23, 0.18, 1.0, 0.65], 'Q2-y=7, z-pT=1': [0.77, 0.58, 0.2, 0.05], 'Q2-y=7, z-pT=2': [0.77, 0.58, 0.29, 0.2], 'Q2-y=7, z-pT=3': [0.77, 0.58, 0.38, 0.29], 'Q2-y=7, z-pT=4': [0.77, 0.58, 0.48, 0.38], 'Q2-y=7, z-pT=5': [0.77, 0.58, 0.6, 0.48], 'Q2-y=7, z-pT=6 - REMOVE - MIGRATION BIN': [0.77, 0.58, 0.83, 0.6], 'Q2-y=7, z-pT=7': [0.58, 0.45, 0.2, 0.05], 'Q2-y=7, z-pT=8': [0.58, 0.45, 0.29, 0.2], 'Q2-y=7, z-pT=9': [0.58, 0.45, 0.38, 0.29], 'Q2-y=7, z-pT=10': [0.58, 0.45, 0.48, 0.38], 'Q2-y=7, z-pT=11': [0.58, 0.45, 0.6, 0.48], 'Q2-y=7, z-pT=12': [0.58, 0.45, 0.83, 0.6], 'Q2-y=7, z-pT=13': [0.45, 0.37, 0.2, 0.05], 'Q2-y=7, z-pT=14': [0.45, 0.37, 0.29, 0.2], 'Q2-y=7, z-pT=15': [0.45, 0.37, 0.38, 0.29], 'Q2-y=7, z-pT=16': [0.45, 0.37, 0.48, 0.38], 'Q2-y=7, z-pT=17': [0.45, 0.37, 0.6, 0.48], 'Q2-y=7, z-pT=18': [0.45, 0.37, 0.83, 0.6], 'Q2-y=7, z-pT=19': [0.37, 0.31, 0.2, 0.05], 'Q2-y=7, z-pT=20': [0.37, 0.31, 0.29, 0.2], 'Q2-y=7, z-pT=21': [0.37, 0.31, 0.38, 0.29], 'Q2-y=7, z-pT=22': [0.37, 0.31, 0.48, 0.38], 'Q2-y=7, z-pT=23': [0.37, 0.31, 0.6, 0.48], 'Q2-y=7, z-pT=24': [0.37, 0.31, 0.83, 0.6], 'Q2-y=7, z-pT=25': [0.31, 0.27, 0.2, 0.05], 'Q2-y=7, z-pT=26': [0.31, 0.27, 0.29, 0.2], 'Q2-y=7, z-pT=27': [0.31, 0.27, 0.38, 0.29], 'Q2-y=7, z-pT=28': [0.31, 0.27, 0.48, 0.38], 'Q2-y=7, z-pT=29': [0.31, 0.27, 0.6, 0.48], 'Q2-y=7, z-pT=30 - REMOVE - MIGRATION BIN': [0.31, 0.27, 0.83, 0.6], 'Q2-y=7, z-pT=31': [0.27, 0.22, 0.2, 0.05], 'Q2-y=7, z-pT=32': [0.27, 0.22, 0.29, 0.2], 'Q2-y=7, z-pT=33': [0.27, 0.22, 0.38, 0.29], 'Q2-y=7, z-pT=34': [0.27, 0.22, 0.48, 0.38], 'Q2-y=7, z-pT=35': [0.27, 0.22, 0.6, 0.48], 'Q2-y=7, z-pT=36 - REMOVE - MIGRATION BIN': [0.27, 0.22, 0.83, 0.6], 'Q2-y=8, z-pT=1': [0.7, 0.56, 0.2, 0.05], 'Q2-y=8, z-pT=2': [0.7, 0.56, 0.29, 0.2], 'Q2-y=8, z-pT=3': [0.7, 0.56, 0.37, 0.29], 'Q2-y=8, z-pT=4': [0.7, 0.56, 0.46, 0.37], 'Q2-y=8, z-pT=5': [0.7, 0.56, 0.6, 0.46], 'Q2-y=8, z-pT=6': [0.56, 0.49, 0.2, 0.05], 'Q2-y=8, z-pT=7': [0.56, 0.49, 0.29, 0.2], 'Q2-y=8, z-pT=8': [0.56, 0.49, 0.37, 0.29], 'Q2-y=8, z-pT=9': [0.56, 0.49, 0.46, 0.37], 'Q2-y=8, z-pT=10': [0.56, 0.49, 0.6, 0.46], 'Q2-y=8, z-pT=11': [0.49, 0.44, 0.2, 0.05], 'Q2-y=8, z-pT=12': [0.49, 0.44, 0.29, 0.2], 'Q2-y=8, z-pT=13': [0.49, 0.44, 0.37, 0.29], 'Q2-y=8, z-pT=14': [0.49, 0.44, 0.46, 0.37], 'Q2-y=8, z-pT=15': [0.49, 0.44, 0.6, 0.46], 'Q2-y=8, z-pT=16': [0.44, 0.39, 0.2, 0.05], 'Q2-y=8, z-pT=17': [0.44, 0.39, 0.29, 0.2], 'Q2-y=8, z-pT=18': [0.44, 0.39, 0.37, 0.29], 'Q2-y=8, z-pT=19': [0.44, 0.39, 0.46, 0.37], 'Q2-y=8, z-pT=20': [0.44, 0.39, 0.6, 0.46], 'Q2-y=8, z-pT=21': [0.39, 0.36, 0.2, 0.05], 'Q2-y=8, z-pT=22': [0.39, 0.36, 0.29, 0.2], 'Q2-y=8, z-pT=23': [0.39, 0.36, 0.37, 0.29], 'Q2-y=8, z-pT=24': [0.39, 0.36, 0.46, 0.37], 'Q2-y=8, z-pT=25': [0.39, 0.36, 0.6, 0.46], 'Q2-y=8, z-pT=26': [0.36, 0.33, 0.2, 0.05], 'Q2-y=8, z-pT=27': [0.36, 0.33, 0.29, 0.2], 'Q2-y=8, z-pT=28': [0.36, 0.33, 0.37, 0.29], 'Q2-y=8, z-pT=29': [0.36, 0.33, 0.46, 0.37], 'Q2-y=8, z-pT=30': [0.36, 0.33, 0.6, 0.46], 'Q2-y=8, z-pT=31': [0.33, 0.27, 0.2, 0.05], 'Q2-y=8, z-pT=32': [0.33, 0.27, 0.29, 0.2], 'Q2-y=8, z-pT=33': [0.33, 0.27, 0.37, 0.29], 'Q2-y=8, z-pT=34': [0.33, 0.27, 0.46, 0.37], 'Q2-y=8, z-pT=35': [0.33, 0.27, 0.6, 0.46], 'Q2-y=9, z-pT=1': [0.7, 0.42, 0.22, 0.05], 'Q2-y=9, z-pT=2': [0.7, 0.42, 0.3, 0.22], 'Q2-y=9, z-pT=3': [0.7, 0.42, 0.38, 0.3], 'Q2-y=9, z-pT=4': [0.7, 0.42, 0.46, 0.38], 'Q2-y=9, z-pT=5': [0.7, 0.42, 0.58, 0.46], 'Q2-y=9, z-pT=6': [0.7, 0.42, 0.74, 0.58], 'Q2-y=9, z-pT=7': [0.7, 0.42, 0.95, 0.74], 'Q2-y=9, z-pT=8': [0.42, 0.3, 0.22, 0.05], 'Q2-y=9, z-pT=9': [0.42, 0.3, 0.3, 0.22], 'Q2-y=9, z-pT=10': [0.42, 0.3, 0.38, 0.3], 'Q2-y=9, z-pT=11': [0.42, 0.3, 0.46, 0.38], 'Q2-y=9, z-pT=12': [0.42, 0.3, 0.58, 0.46], 'Q2-y=9, z-pT=13': [0.42, 0.3, 0.74, 0.58], 'Q2-y=9, z-pT=14': [0.42, 0.3, 0.95, 0.74], 'Q2-y=9, z-pT=15': [0.3, 0.24, 0.22, 0.05], 'Q2-y=9, z-pT=16': [0.3, 0.24, 0.3, 0.22], 'Q2-y=9, z-pT=17': [0.3, 0.24, 0.38, 0.3], 'Q2-y=9, z-pT=18': [0.3, 0.24, 0.46, 0.38], 'Q2-y=9, z-pT=19': [0.3, 0.24, 0.58, 0.46], 'Q2-y=9, z-pT=20': [0.3, 0.24, 0.74, 0.58], 'Q2-y=9, z-pT=21 - REMOVE - MIGRATION BIN': [0.3, 0.24, 0.95, 0.74], 'Q2-y=9, z-pT=22': [0.24, 0.2, 0.22, 0.05], 'Q2-y=9, z-pT=23': [0.24, 0.2, 0.3, 0.22], 'Q2-y=9, z-pT=24': [0.24, 0.2, 0.38, 0.3], 'Q2-y=9, z-pT=25': [0.24, 0.2, 0.46, 0.38], 'Q2-y=9, z-pT=26': [0.24, 0.2, 0.58, 0.46], 'Q2-y=9, z-pT=27 - REMOVE - MIGRATION BIN': [0.24, 0.2, 0.74, 0.58], 'Q2-y=9, z-pT=28 - REMOVE - MIGRATION BIN': [0.24, 0.2, 0.95, 0.74], 'Q2-y=9, z-pT=29': [0.2, 0.16, 0.22, 0.05], 'Q2-y=9, z-pT=30': [0.2, 0.16, 0.3, 0.22], 'Q2-y=9, z-pT=31': [0.2, 0.16, 0.38, 0.3], 'Q2-y=9, z-pT=32': [0.2, 0.16, 0.46, 0.38], 'Q2-y=9, z-pT=33 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.58, 0.46], 'Q2-y=9, z-pT=34 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.74, 0.58], 'Q2-y=9, z-pT=35 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.95, 0.74], 'Q2-y=10, z-pT=1': [0.72, 0.5, 0.21, 0.05], 'Q2-y=10, z-pT=2': [0.72, 0.5, 0.31, 0.21], 'Q2-y=10, z-pT=3': [0.72, 0.5, 0.4, 0.31], 'Q2-y=10, z-pT=4': [0.72, 0.5, 0.5, 0.4], 'Q2-y=10, z-pT=5': [0.72, 0.5, 0.64, 0.5], 'Q2-y=10, z-pT=6': [0.72, 0.5, 0.9, 0.64], 'Q2-y=10, z-pT=7': [0.5, 0.4, 0.21, 0.05], 'Q2-y=10, z-pT=8': [0.5, 0.4, 0.31, 0.21], 'Q2-y=10, z-pT=9': [0.5, 0.4, 0.4, 0.31], 'Q2-y=10, z-pT=10': [0.5, 0.4, 0.5, 0.4], 'Q2-y=10, z-pT=11': [0.5, 0.4, 0.64, 0.5], 'Q2-y=10, z-pT=12': [0.5, 0.4, 0.9, 0.64], 'Q2-y=10, z-pT=13': [0.4, 0.32, 0.21, 0.05], 'Q2-y=10, z-pT=14': [0.4, 0.32, 0.31, 0.21], 'Q2-y=10, z-pT=15': [0.4, 0.32, 0.4, 0.31], 'Q2-y=10, z-pT=16': [0.4, 0.32, 0.5, 0.4], 'Q2-y=10, z-pT=17': [0.4, 0.32, 0.64, 0.5], 'Q2-y=10, z-pT=18': [0.4, 0.32, 0.9, 0.64], 'Q2-y=10, z-pT=19': [0.32, 0.26, 0.21, 0.05], 'Q2-y=10, z-pT=20': [0.32, 0.26, 0.31, 0.21], 'Q2-y=10, z-pT=21': [0.32, 0.26, 0.4, 0.31], 'Q2-y=10, z-pT=22': [0.32, 0.26, 0.5, 0.4], 'Q2-y=10, z-pT=23': [0.32, 0.26, 0.64, 0.5], 'Q2-y=10, z-pT=24 - REMOVE - MIGRATION BIN': [0.32, 0.26, 0.9, 0.64], 'Q2-y=10, z-pT=25': [0.26, 0.23, 0.21, 0.05], 'Q2-y=10, z-pT=26': [0.26, 0.23, 0.31, 0.21], 'Q2-y=10, z-pT=27': [0.26, 0.23, 0.4, 0.31], 'Q2-y=10, z-pT=28': [0.26, 0.23, 0.5, 0.4], 'Q2-y=10, z-pT=29': [0.26, 0.23, 0.64, 0.5], 'Q2-y=10, z-pT=30 - REMOVE - MIGRATION BIN': [0.26, 0.23, 0.9, 0.64], 'Q2-y=10, z-pT=31': [0.23, 0.19, 0.21, 0.05], 'Q2-y=10, z-pT=32': [0.23, 0.19, 0.31, 0.21], 'Q2-y=10, z-pT=33': [0.23, 0.19, 0.4, 0.31], 'Q2-y=10, z-pT=34': [0.23, 0.19, 0.5, 0.4], 'Q2-y=10, z-pT=35 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.64, 0.5], 'Q2-y=10, z-pT=36 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.9, 0.64], 'Q2-y=11, z-pT=1': [0.73, 0.52, 0.2, 0.05], 'Q2-y=11, z-pT=2': [0.73, 0.52, 0.3, 0.2], 'Q2-y=11, z-pT=3': [0.73, 0.52, 0.4, 0.3], 'Q2-y=11, z-pT=4': [0.73, 0.52, 0.53, 0.4], 'Q2-y=11, z-pT=5': [0.73, 0.52, 0.69, 0.53], 'Q2-y=11, z-pT=6': [0.52, 0.39, 0.2, 0.05], 'Q2-y=11, z-pT=7': [0.52, 0.39, 0.3, 0.2], 'Q2-y=11, z-pT=8': [0.52, 0.39, 0.4, 0.3], 'Q2-y=11, z-pT=9': [0.52, 0.39, 0.53, 0.4], 'Q2-y=11, z-pT=10': [0.52, 0.39, 0.69, 0.53], 'Q2-y=11, z-pT=11': [0.39, 0.32, 0.2, 0.05], 'Q2-y=11, z-pT=12': [0.39, 0.32, 0.3, 0.2], 'Q2-y=11, z-pT=13': [0.39, 0.32, 0.4, 0.3], 'Q2-y=11, z-pT=14': [0.39, 0.32, 0.53, 0.4], 'Q2-y=11, z-pT=15': [0.39, 0.32, 0.69, 0.53], 'Q2-y=11, z-pT=16': [0.32, 0.27, 0.2, 0.05], 'Q2-y=11, z-pT=17': [0.32, 0.27, 0.3, 0.2], 'Q2-y=11, z-pT=18': [0.32, 0.27, 0.4, 0.3], 'Q2-y=11, z-pT=19': [0.32, 0.27, 0.53, 0.4], 'Q2-y=11, z-pT=20': [0.32, 0.27, 0.69, 0.53], 'Q2-y=11, z-pT=21': [0.27, 0.22, 0.2, 0.05], 'Q2-y=11, z-pT=22': [0.27, 0.22, 0.3, 0.2], 'Q2-y=11, z-pT=23': [0.27, 0.22, 0.4, 0.3], 'Q2-y=11, z-pT=24': [0.27, 0.22, 0.53, 0.4], 'Q2-y=11, z-pT=25 - REMOVE - MIGRATION BIN': [0.27, 0.22, 0.69, 0.53], 'Q2-y=12, z-pT=1': [0.7, 0.51, 0.2, 0.05], 'Q2-y=12, z-pT=2': [0.7, 0.51, 0.28, 0.2], 'Q2-y=12, z-pT=3': [0.7, 0.51, 0.36, 0.28], 'Q2-y=12, z-pT=4': [0.7, 0.51, 0.45, 0.36], 'Q2-y=12, z-pT=5 - REMOVE - MIGRATION BIN': [0.7, 0.51, 0.6, 0.45], 'Q2-y=12, z-pT=6': [0.51, 0.43, 0.2, 0.05], 'Q2-y=12, z-pT=7': [0.51, 0.43, 0.28, 0.2], 'Q2-y=12, z-pT=8': [0.51, 0.43, 0.36, 0.28], 'Q2-y=12, z-pT=9': [0.51, 0.43, 0.45, 0.36], 'Q2-y=12, z-pT=10': [0.51, 0.43, 0.6, 0.45], 'Q2-y=12, z-pT=11': [0.43, 0.37, 0.2, 0.05], 'Q2-y=12, z-pT=12': [0.43, 0.37, 0.28, 0.2], 'Q2-y=12, z-pT=13': [0.43, 0.37, 0.36, 0.28], 'Q2-y=12, z-pT=14': [0.43, 0.37, 0.45, 0.36], 'Q2-y=12, z-pT=15': [0.43, 0.37, 0.6, 0.45], 'Q2-y=12, z-pT=16': [0.37, 0.33, 0.2, 0.05], 'Q2-y=12, z-pT=17': [0.37, 0.33, 0.28, 0.2], 'Q2-y=12, z-pT=18': [0.37, 0.33, 0.36, 0.28], 'Q2-y=12, z-pT=19': [0.37, 0.33, 0.45, 0.36], 'Q2-y=12, z-pT=20': [0.37, 0.33, 0.6, 0.45], 'Q2-y=12, z-pT=21': [0.33, 0.27, 0.2, 0.05], 'Q2-y=12, z-pT=22': [0.33, 0.27, 0.28, 0.2], 'Q2-y=12, z-pT=23': [0.33, 0.27, 0.36, 0.28], 'Q2-y=12, z-pT=24': [0.33, 0.27, 0.45, 0.36], 'Q2-y=12, z-pT=25': [0.33, 0.27, 0.6, 0.45], 'Q2-y=13, z-pT=1': [0.72, 0.46, 0.22, 0.05], 'Q2-y=13, z-pT=2': [0.72, 0.46, 0.34, 0.22], 'Q2-y=13, z-pT=3': [0.72, 0.46, 0.44, 0.34], 'Q2-y=13, z-pT=4': [0.72, 0.46, 0.58, 0.44], 'Q2-y=13, z-pT=5': [0.72, 0.46, 0.9, 0.58], 'Q2-y=13, z-pT=6': [0.46, 0.35, 0.22, 0.05], 'Q2-y=13, z-pT=7': [0.46, 0.35, 0.34, 0.22], 'Q2-y=13, z-pT=8': [0.46, 0.35, 0.44, 0.34], 'Q2-y=13, z-pT=9': [0.46, 0.35, 0.58, 0.44], 'Q2-y=13, z-pT=10': [0.46, 0.35, 0.9, 0.58], 'Q2-y=13, z-pT=11': [0.35, 0.29, 0.22, 0.05], 'Q2-y=13, z-pT=12': [0.35, 0.29, 0.34, 0.22], 'Q2-y=13, z-pT=13': [0.35, 0.29, 0.44, 0.34], 'Q2-y=13, z-pT=14': [0.35, 0.29, 0.58, 0.44], 'Q2-y=13, z-pT=15': [0.35, 0.29, 0.9, 0.58], 'Q2-y=13, z-pT=16': [0.29, 0.24, 0.22, 0.05], 'Q2-y=13, z-pT=17': [0.29, 0.24, 0.34, 0.22], 'Q2-y=13, z-pT=18': [0.29, 0.24, 0.44, 0.34], 'Q2-y=13, z-pT=19': [0.29, 0.24, 0.58, 0.44], 'Q2-y=13, z-pT=20 - REMOVE - MIGRATION BIN': [0.29, 0.24, 0.9, 0.58], 'Q2-y=13, z-pT=21': [0.24, 0.2, 0.22, 0.05], 'Q2-y=13, z-pT=22': [0.24, 0.2, 0.34, 0.22], 'Q2-y=13, z-pT=23': [0.24, 0.2, 0.44, 0.34], 'Q2-y=13, z-pT=24': [0.24, 0.2, 0.58, 0.44], 'Q2-y=13, z-pT=25 - REMOVE - MIGRATION BIN': [0.24, 0.2, 0.9, 0.58], 'Q2-y=13, z-pT=26': [0.2, 0.16, 0.22, 0.05], 'Q2-y=13, z-pT=27': [0.2, 0.16, 0.34, 0.22], 'Q2-y=13, z-pT=28': [0.2, 0.16, 0.44, 0.34], 'Q2-y=13, z-pT=29 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.58, 0.44], 'Q2-y=13, z-pT=30 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.9, 0.58], 'Q2-y=14, z-pT=1': [0.71, 0.5, 0.21, 0.05], 'Q2-y=14, z-pT=2': [0.71, 0.5, 0.31, 0.21], 'Q2-y=14, z-pT=3': [0.71, 0.5, 0.4, 0.31], 'Q2-y=14, z-pT=4': [0.71, 0.5, 0.5, 0.4], 'Q2-y=14, z-pT=5': [0.71, 0.5, 0.64, 0.5], 'Q2-y=14, z-pT=6': [0.71, 0.5, 0.9, 0.64], 'Q2-y=14, z-pT=7': [0.5, 0.39, 0.21, 0.05], 'Q2-y=14, z-pT=8': [0.5, 0.39, 0.31, 0.21], 'Q2-y=14, z-pT=9': [0.5, 0.39, 0.4, 0.31], 'Q2-y=14, z-pT=10': [0.5, 0.39, 0.5, 0.4], 'Q2-y=14, z-pT=11': [0.5, 0.39, 0.64, 0.5], 'Q2-y=14, z-pT=12': [0.5, 0.39, 0.9, 0.64], 'Q2-y=14, z-pT=13': [0.39, 0.32, 0.21, 0.05], 'Q2-y=14, z-pT=14': [0.39, 0.32, 0.31, 0.21], 'Q2-y=14, z-pT=15': [0.39, 0.32, 0.4, 0.31], 'Q2-y=14, z-pT=16': [0.39, 0.32, 0.5, 0.4], 'Q2-y=14, z-pT=17': [0.39, 0.32, 0.64, 0.5], 'Q2-y=14, z-pT=18': [0.39, 0.32, 0.9, 0.64], 'Q2-y=14, z-pT=19': [0.32, 0.27, 0.21, 0.05], 'Q2-y=14, z-pT=20': [0.32, 0.27, 0.31, 0.21], 'Q2-y=14, z-pT=21': [0.32, 0.27, 0.4, 0.31], 'Q2-y=14, z-pT=22': [0.32, 0.27, 0.5, 0.4], 'Q2-y=14, z-pT=23': [0.32, 0.27, 0.64, 0.5], 'Q2-y=14, z-pT=24 - REMOVE - MIGRATION BIN': [0.32, 0.27, 0.9, 0.64], 'Q2-y=14, z-pT=25': [0.27, 0.23, 0.21, 0.05], 'Q2-y=14, z-pT=26': [0.27, 0.23, 0.31, 0.21], 'Q2-y=14, z-pT=27': [0.27, 0.23, 0.4, 0.31], 'Q2-y=14, z-pT=28': [0.27, 0.23, 0.5, 0.4], 'Q2-y=14, z-pT=29': [0.27, 0.23, 0.64, 0.5], 'Q2-y=14, z-pT=30 - REMOVE - MIGRATION BIN': [0.27, 0.23, 0.9, 0.64], 'Q2-y=14, z-pT=31': [0.23, 0.19, 0.21, 0.05], 'Q2-y=14, z-pT=32': [0.23, 0.19, 0.31, 0.21], 'Q2-y=14, z-pT=33': [0.23, 0.19, 0.4, 0.31], 'Q2-y=14, z-pT=34': [0.23, 0.19, 0.5, 0.4], 'Q2-y=14, z-pT=35 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.64, 0.5], 'Q2-y=14, z-pT=36 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.9, 0.64], 'Q2-y=15, z-pT=1': [0.73, 0.49, 0.22, 0.05], 'Q2-y=15, z-pT=2': [0.73, 0.49, 0.32, 0.22], 'Q2-y=15, z-pT=3': [0.73, 0.49, 0.42, 0.32], 'Q2-y=15, z-pT=4': [0.73, 0.49, 0.55, 0.42], 'Q2-y=15, z-pT=5 - REMOVE - MIGRATION BIN': [0.73, 0.49, 0.8, 0.55], 'Q2-y=15, z-pT=6': [0.49, 0.4, 0.22, 0.05], 'Q2-y=15, z-pT=7': [0.49, 0.4, 0.32, 0.22], 'Q2-y=15, z-pT=8': [0.49, 0.4, 0.42, 0.32], 'Q2-y=15, z-pT=9': [0.49, 0.4, 0.55, 0.42], 'Q2-y=15, z-pT=10': [0.49, 0.4, 0.8, 0.55], 'Q2-y=15, z-pT=11': [0.4, 0.32, 0.22, 0.05], 'Q2-y=15, z-pT=12': [0.4, 0.32, 0.32, 0.22], 'Q2-y=15, z-pT=13': [0.4, 0.32, 0.42, 0.32], 'Q2-y=15, z-pT=14': [0.4, 0.32, 0.55, 0.42], 'Q2-y=15, z-pT=15': [0.4, 0.32, 0.8, 0.55], 'Q2-y=15, z-pT=16': [0.32, 0.27, 0.22, 0.05], 'Q2-y=15, z-pT=17': [0.32, 0.27, 0.32, 0.22], 'Q2-y=15, z-pT=18': [0.32, 0.27, 0.42, 0.32], 'Q2-y=15, z-pT=19': [0.32, 0.27, 0.55, 0.42], 'Q2-y=15, z-pT=20 - REMOVE - MIGRATION BIN': [0.32, 0.27, 0.8, 0.55], 'Q2-y=15, z-pT=21': [0.27, 0.22, 0.22, 0.05], 'Q2-y=15, z-pT=22': [0.27, 0.22, 0.32, 0.22], 'Q2-y=15, z-pT=23': [0.27, 0.22, 0.42, 0.32], 'Q2-y=15, z-pT=24': [0.27, 0.22, 0.55, 0.42], 'Q2-y=15, z-pT=25 - REMOVE - MIGRATION BIN': [0.27, 0.22, 0.8, 0.55], 'Q2-y=16, z-pT=1': [0.67, 0.42, 0.22, 0.05], 'Q2-y=16, z-pT=2': [0.67, 0.42, 0.32, 0.22], 'Q2-y=16, z-pT=3': [0.67, 0.42, 0.42, 0.32], 'Q2-y=16, z-pT=4': [0.67, 0.42, 0.52, 0.42], 'Q2-y=16, z-pT=5': [0.67, 0.42, 0.66, 0.52], 'Q2-y=16, z-pT=6': [0.67, 0.42, 0.9, 0.66], 'Q2-y=16, z-pT=7': [0.42, 0.31, 0.22, 0.05], 'Q2-y=16, z-pT=8': [0.42, 0.31, 0.32, 0.22], 'Q2-y=16, z-pT=9': [0.42, 0.31, 0.42, 0.32], 'Q2-y=16, z-pT=10': [0.42, 0.31, 0.52, 0.42], 'Q2-y=16, z-pT=11': [0.42, 0.31, 0.66, 0.52], 'Q2-y=16, z-pT=12': [0.42, 0.31, 0.9, 0.66], 'Q2-y=16, z-pT=13': [0.31, 0.24, 0.22, 0.05], 'Q2-y=16, z-pT=14': [0.31, 0.24, 0.32, 0.22], 'Q2-y=16, z-pT=15': [0.31, 0.24, 0.42, 0.32], 'Q2-y=16, z-pT=16': [0.31, 0.24, 0.52, 0.42], 'Q2-y=16, z-pT=17': [0.31, 0.24, 0.66, 0.52], 'Q2-y=16, z-pT=18 - REMOVE - MIGRATION BIN': [0.31, 0.24, 0.9, 0.66], 'Q2-y=16, z-pT=19': [0.24, 0.2, 0.22, 0.05], 'Q2-y=16, z-pT=20': [0.24, 0.2, 0.32, 0.22], 'Q2-y=16, z-pT=21': [0.24, 0.2, 0.42, 0.32], 'Q2-y=16, z-pT=22': [0.24, 0.2, 0.52, 0.42], 'Q2-y=16, z-pT=23 - REMOVE - MIGRATION BIN': [0.24, 0.2, 0.66, 0.52], 'Q2-y=16, z-pT=24 - REMOVE - MIGRATION BIN': [0.24, 0.2, 0.9, 0.66], 'Q2-y=16, z-pT=25': [0.2, 0.16, 0.22, 0.05], 'Q2-y=16, z-pT=26': [0.2, 0.16, 0.32, 0.22], 'Q2-y=16, z-pT=27': [0.2, 0.16, 0.42, 0.32], 'Q2-y=16, z-pT=28 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.52, 0.42], 'Q2-y=16, z-pT=29 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.66, 0.52], 'Q2-y=16, z-pT=30 - REMOVE - MIGRATION BIN': [0.2, 0.16, 0.9, 0.66], 'Q2-y=17, z-pT=1': [0.68, 0.44, 0.19, 0.05], 'Q2-y=17, z-pT=2': [0.68, 0.44, 0.28, 0.19], 'Q2-y=17, z-pT=3': [0.68, 0.44, 0.37, 0.28], 'Q2-y=17, z-pT=4': [0.68, 0.44, 0.45, 0.37], 'Q2-y=17, z-pT=5': [0.68, 0.44, 0.55, 0.45], 'Q2-y=17, z-pT=6': [0.68, 0.44, 0.73, 0.55], 'Q2-y=17, z-pT=7': [0.44, 0.34, 0.19, 0.05], 'Q2-y=17, z-pT=8': [0.44, 0.34, 0.28, 0.19], 'Q2-y=17, z-pT=9': [0.44, 0.34, 0.37, 0.28], 'Q2-y=17, z-pT=10': [0.44, 0.34, 0.45, 0.37], 'Q2-y=17, z-pT=11': [0.44, 0.34, 0.55, 0.45], 'Q2-y=17, z-pT=12': [0.44, 0.34, 0.73, 0.55], 'Q2-y=17, z-pT=13': [0.34, 0.28, 0.19, 0.05], 'Q2-y=17, z-pT=14': [0.34, 0.28, 0.28, 0.19], 'Q2-y=17, z-pT=15': [0.34, 0.28, 0.37, 0.28], 'Q2-y=17, z-pT=16': [0.34, 0.28, 0.45, 0.37], 'Q2-y=17, z-pT=17': [0.34, 0.28, 0.55, 0.45], 'Q2-y=17, z-pT=18': [0.34, 0.28, 0.73, 0.55], 'Q2-y=17, z-pT=19': [0.28, 0.23, 0.19, 0.05], 'Q2-y=17, z-pT=20': [0.28, 0.23, 0.28, 0.19], 'Q2-y=17, z-pT=21': [0.28, 0.23, 0.37, 0.28], 'Q2-y=17, z-pT=22': [0.28, 0.23, 0.45, 0.37], 'Q2-y=17, z-pT=23': [0.28, 0.23, 0.55, 0.45], 'Q2-y=17, z-pT=24 - REMOVE - MIGRATION BIN': [0.28, 0.23, 0.73, 0.55], 'Q2-y=17, z-pT=25': [0.23, 0.19, 0.19, 0.05], 'Q2-y=17, z-pT=26': [0.23, 0.19, 0.28, 0.19], 'Q2-y=17, z-pT=27': [0.23, 0.19, 0.37, 0.28], 'Q2-y=17, z-pT=28': [0.23, 0.19, 0.45, 0.37], 'Q2-y=17, z-pT=29 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.55, 0.45], 'Q2-y=17, z-pT=30 - REMOVE - MIGRATION BIN': [0.23, 0.19, 0.73, 0.55], 'Q2-y=18': 'end'}

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=1):
    Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2 = 1, 1, list(range(1, 55))
    if(str(Q2_y_Bin_Num_In) in ['1']):
        Migration_Bin_2 = [21, 27, 28, 33, 34, 35]
        Migration_Bin_1 = 35
        Total_Number_of_Bins = 35
    if(str(Q2_y_Bin_Num_In) in ['2']):
        Migration_Bin_2 = [24, 30, 35, 36]
        Migration_Bin_1 = 36
        Total_Number_of_Bins = 36
    if(str(Q2_y_Bin_Num_In) in ['3']):
        Migration_Bin_2 = [30]
        Migration_Bin_1 = 30
        Total_Number_of_Bins = 30
    if(str(Q2_y_Bin_Num_In) in ['4']):
        # Migration_Bin_2 = [6, 30, 36]
        Migration_Bin_2 = [6, 30, 35, 36]
        Migration_Bin_1 = 36
        Total_Number_of_Bins = 36
    if(str(Q2_y_Bin_Num_In) in ['5']):
        Migration_Bin_2 = [24, 30, 35, 36]
        Migration_Bin_1 = 36
        Total_Number_of_Bins = 36
    if(str(Q2_y_Bin_Num_In) in ['6']):
        Migration_Bin_2 = [18, 24, 29, 30]
        Migration_Bin_1 = 30
        Total_Number_of_Bins = 30
    if(str(Q2_y_Bin_Num_In) in ['7']):
        Migration_Bin_2 = [6, 30, 36]
        Migration_Bin_1 = 36
        Total_Number_of_Bins = 36
    if(str(Q2_y_Bin_Num_In) in ['8']):
        # Migration_Bin_2 = []
        Migration_Bin_2 = [35]
        Migration_Bin_1 = 35
        Total_Number_of_Bins = 35
    if(str(Q2_y_Bin_Num_In) in ['9']):
        Migration_Bin_2 = [21, 27, 28, 33, 34, 35]
        Migration_Bin_1 = 35
        Total_Number_of_Bins = 35
    if(str(Q2_y_Bin_Num_In) in ['10']):
        Migration_Bin_2 = [24, 30, 35, 36]
        Migration_Bin_1 = 36
        Total_Number_of_Bins = 36
    if(str(Q2_y_Bin_Num_In) in ['11']):
        Migration_Bin_2 = [25]
        Migration_Bin_1 = 25
        Total_Number_of_Bins = 25
    if(str(Q2_y_Bin_Num_In) in ['12']):
        # Migration_Bin_2 = [5]
        Migration_Bin_2 = [5, 25]
        Migration_Bin_1 = 25
        Total_Number_of_Bins = 25
    if(str(Q2_y_Bin_Num_In) in ['13']):
        Migration_Bin_2 = [20, 25, 29, 30]
        Migration_Bin_1 = 30
        Total_Number_of_Bins = 30
    if(str(Q2_y_Bin_Num_In) in ['14']):
        Migration_Bin_2 = [24, 30, 35, 36]
        Migration_Bin_1 = 36
        Total_Number_of_Bins = 36
    if(str(Q2_y_Bin_Num_In) in ['15']):
        Migration_Bin_2 = [5, 20, 25]
        Migration_Bin_1 = 25
        Total_Number_of_Bins = 25
    if(str(Q2_y_Bin_Num_In) in ['16']):
        Migration_Bin_2 = [18, 23, 24, 28, 29, 30]
        Migration_Bin_1 = 30
        Total_Number_of_Bins = 30
    if(str(Q2_y_Bin_Num_In) in ['17']):
        Migration_Bin_2 = [24, 29, 30]
        Migration_Bin_1 = 30
        Total_Number_of_Bins = 30
    return [Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2]

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

Int_Bin_Definition_Array = { 'Q2-y=0, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=1':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=2':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=3':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=4':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=5':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=6':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=7':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=8':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=9':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=10':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=11':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=12':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=13':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=14':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=15':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=16':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=17':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=18':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=19':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=20':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=21':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=22':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=23':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=24':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=0, z-pT=25':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=1, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=1, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=1, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=1, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=1, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=1, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=1, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=1, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=1, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=1, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=1, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=1, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=1, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=1, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=1, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=1, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=1, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=1, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=1, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=1, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=1, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=1, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=1, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=1, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=1, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=1, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=1, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=2, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=2, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=2, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=2, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=2, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=2, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=2, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=2, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=2, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=2, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=2, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=2, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=2, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=2, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=2, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=2, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=2, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=2, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=2, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=2, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=2, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=2, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=2, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=2, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=2, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=2, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=2, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=3, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=3, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=3, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=3, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=3, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=3, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=3, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=3, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=3, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=3, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=3, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=3, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=3, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=3, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=3, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=3, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=3, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=3, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=3, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=3, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=3, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=3, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=3, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=3, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=3, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=3, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=3, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=4, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=4, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=4, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=4, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=4, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=4, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=4, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=4, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=4, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=4, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=4, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=4, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=4, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=4, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=4, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=4, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=4, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=4, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=4, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=4, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=4, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=4, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=4, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=4, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=4, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=4, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=4, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=5, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=5, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=5, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=5, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=5, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=5, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=5, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=5, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=5, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=5, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=5, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=5, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=5, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=5, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=5, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=5, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=5, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=5, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=5, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=5, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=5, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=5, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=5, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=5, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=5, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=5, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=5, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=6, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=6, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=6, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=6, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=6, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=6, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=6, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=6, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=6, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=6, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=6, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=6, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=6, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=6, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=6, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=6, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=6, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=6, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=6, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=6, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=6, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=6, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=6, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=6, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=6, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=6, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=6, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=7, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=7, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=7, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=7, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=7, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=7, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=7, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=7, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=7, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=7, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=7, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=7, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=7, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=7, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=7, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=7, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=7, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=7, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=7, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=7, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=7, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=7, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=7, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=7, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=7, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=7, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=7, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=8, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=8, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=8, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=8, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=8, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=8, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=8, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=8, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=8, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=8, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=8, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=8, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=8, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=8, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=8, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=8, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=8, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=8, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=8, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=8, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=8, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=8, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=8, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=8, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=8, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=8, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=8, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=9, z-pT=All':   [0.665,  0.27,   0.59,     0.05], 'Q2-y=9, z-pT=0':     [0.665,  0.27,   0.59,     0.05], 'Q2-y=9, z-pT=1':     [0.34,   0.27,   0.153,    0.05], 'Q2-y=9, z-pT=2':     [0.34,   0.27,   0.258,   0.153], 'Q2-y=9, z-pT=3':     [0.34,   0.27,   0.366,   0.258], 'Q2-y=9, z-pT=4':     [0.34,   0.27,   0.478,   0.366], 'Q2-y=9, z-pT=5':     [0.34,   0.27,   0.59,    0.478], 'Q2-y=9, z-pT=6':     [0.415,  0.34,   0.153,    0.05], 'Q2-y=9, z-pT=7':     [0.415,  0.34,   0.258,   0.153], 'Q2-y=9, z-pT=8':     [0.415,  0.34,   0.366,   0.258], 'Q2-y=9, z-pT=9':     [0.415,  0.34,   0.478,   0.366], 'Q2-y=9, z-pT=10':    [0.415,  0.34,   0.59,    0.478], 'Q2-y=9, z-pT=11':    [0.492,  0.415,  0.153,    0.05], 'Q2-y=9, z-pT=12':    [0.492,  0.415,  0.258,   0.153], 'Q2-y=9, z-pT=13':    [0.492,  0.415,  0.366,   0.258], 'Q2-y=9, z-pT=14':    [0.492,  0.415,  0.478,   0.366], 'Q2-y=9, z-pT=15':    [0.492,  0.415,  0.59,    0.478], 'Q2-y=9, z-pT=16':    [0.578,  0.492,  0.153,    0.05], 'Q2-y=9, z-pT=17':    [0.578,  0.492,  0.258,   0.153], 'Q2-y=9, z-pT=18':    [0.578,  0.492,  0.366,   0.258], 'Q2-y=9, z-pT=19':    [0.578,  0.492,  0.478,   0.366], 'Q2-y=9, z-pT=20':    [0.578,  0.492,  0.59,    0.478], 'Q2-y=9, z-pT=21':    [0.665,  0.578,  0.153,    0.05], 'Q2-y=9, z-pT=22':    [0.665,  0.578,  0.258,   0.153], 'Q2-y=9, z-pT=23':    [0.665,  0.578,  0.366,   0.258], 'Q2-y=9, z-pT=24':    [0.665,  0.578,  0.478,   0.366], 'Q2-y=9, z-pT=25':    [0.665,  0.578,  0.59,    0.478], 'Q2-y=10, z-pT=All':  [0.665,  0.27,   0.59,     0.05], 'Q2-y=10, z-pT=0':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=10, z-pT=1':    [0.34,   0.27,   0.153,    0.05], 'Q2-y=10, z-pT=2':    [0.34,   0.27,   0.258,   0.153], 'Q2-y=10, z-pT=3':    [0.34,   0.27,   0.366,   0.258], 'Q2-y=10, z-pT=4':    [0.34,   0.27,   0.478,   0.366], 'Q2-y=10, z-pT=5':    [0.34,   0.27,   0.59,    0.478], 'Q2-y=10, z-pT=6':    [0.415,  0.34,   0.153,    0.05], 'Q2-y=10, z-pT=7':    [0.415,  0.34,   0.258,   0.153], 'Q2-y=10, z-pT=8':    [0.415,  0.34,   0.366,   0.258], 'Q2-y=10, z-pT=9':    [0.415,  0.34,   0.478,   0.366], 'Q2-y=10, z-pT=10':   [0.415,  0.34,   0.59,    0.478], 'Q2-y=10, z-pT=11':   [0.492,  0.415,  0.153,    0.05], 'Q2-y=10, z-pT=12':   [0.492,  0.415,  0.258,   0.153], 'Q2-y=10, z-pT=13':   [0.492,  0.415,  0.366,   0.258], 'Q2-y=10, z-pT=14':   [0.492,  0.415,  0.478,   0.366], 'Q2-y=10, z-pT=15':   [0.492,  0.415,  0.59,    0.478], 'Q2-y=10, z-pT=16':   [0.578,  0.492,  0.153,    0.05], 'Q2-y=10, z-pT=17':   [0.578,  0.492,  0.258,   0.153], 'Q2-y=10, z-pT=18':   [0.578,  0.492,  0.366,   0.258], 'Q2-y=10, z-pT=19':   [0.578,  0.492,  0.478,   0.366], 'Q2-y=10, z-pT=20':   [0.578,  0.492,  0.59,    0.478], 'Q2-y=10, z-pT=21':   [0.665,  0.578,  0.153,    0.05], 'Q2-y=10, z-pT=22':   [0.665,  0.578,  0.258,   0.153], 'Q2-y=10, z-pT=23':   [0.665,  0.578,  0.366,   0.258], 'Q2-y=10, z-pT=24':   [0.665,  0.578,  0.478,   0.366], 'Q2-y=10, z-pT=25':   [0.665,  0.578,  0.59,    0.478], 'Q2-y=11, z-pT=All':  [0.665,  0.27,   0.59,     0.05], 'Q2-y=11, z-pT=0':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=11, z-pT=1':    [0.34,   0.27,   0.153,    0.05], 'Q2-y=11, z-pT=2':    [0.34,   0.27,   0.258,   0.153], 'Q2-y=11, z-pT=3':    [0.34,   0.27,   0.366,   0.258], 'Q2-y=11, z-pT=4':    [0.34,   0.27,   0.478,   0.366], 'Q2-y=11, z-pT=5':    [0.34,   0.27,   0.59,    0.478], 'Q2-y=11, z-pT=6':    [0.415,  0.34,   0.153,    0.05], 'Q2-y=11, z-pT=7':    [0.415,  0.34,   0.258,   0.153], 'Q2-y=11, z-pT=8':    [0.415,  0.34,   0.366,   0.258], 'Q2-y=11, z-pT=9':    [0.415,  0.34,   0.478,   0.366], 'Q2-y=11, z-pT=10':   [0.415,  0.34,   0.59,    0.478], 'Q2-y=11, z-pT=11':   [0.492,  0.415,  0.153,    0.05], 'Q2-y=11, z-pT=12':   [0.492,  0.415,  0.258,   0.153], 'Q2-y=11, z-pT=13':   [0.492,  0.415,  0.366,   0.258], 'Q2-y=11, z-pT=14':   [0.492,  0.415,  0.478,   0.366], 'Q2-y=11, z-pT=15':   [0.492,  0.415,  0.59,    0.478], 'Q2-y=11, z-pT=16':   [0.578,  0.492,  0.153,    0.05], 'Q2-y=11, z-pT=17':   [0.578,  0.492,  0.258,   0.153], 'Q2-y=11, z-pT=18':   [0.578,  0.492,  0.366,   0.258], 'Q2-y=11, z-pT=19':   [0.578,  0.492,  0.478,   0.366], 'Q2-y=11, z-pT=20':   [0.578,  0.492,  0.59,    0.478], 'Q2-y=11, z-pT=21':   [0.665,  0.578,  0.153,    0.05], 'Q2-y=11, z-pT=22':   [0.665,  0.578,  0.258,   0.153], 'Q2-y=11, z-pT=23':   [0.665,  0.578,  0.366,   0.258], 'Q2-y=11, z-pT=24':   [0.665,  0.578,  0.478,   0.366], 'Q2-y=11, z-pT=25':   [0.665,  0.578,  0.59,    0.478], 'Q2-y=12, z-pT=All':  [0.665,  0.27,   0.59,     0.05], 'Q2-y=12, z-pT=0':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=12, z-pT=1':    [0.34,   0.27,   0.153,    0.05], 'Q2-y=12, z-pT=2':    [0.34,   0.27,   0.258,   0.153], 'Q2-y=12, z-pT=3':    [0.34,   0.27,   0.366,   0.258], 'Q2-y=12, z-pT=4':    [0.34,   0.27,   0.478,   0.366], 'Q2-y=12, z-pT=5':    [0.34,   0.27,   0.59,    0.478], 'Q2-y=12, z-pT=6':    [0.415,  0.34,   0.153,    0.05], 'Q2-y=12, z-pT=7':    [0.415,  0.34,   0.258,   0.153], 'Q2-y=12, z-pT=8':    [0.415,  0.34,   0.366,   0.258], 'Q2-y=12, z-pT=9':    [0.415,  0.34,   0.478,   0.366], 'Q2-y=12, z-pT=10':   [0.415,  0.34,   0.59,    0.478], 'Q2-y=12, z-pT=11':   [0.492,  0.415,  0.153,    0.05], 'Q2-y=12, z-pT=12':   [0.492,  0.415,  0.258,   0.153], 'Q2-y=12, z-pT=13':   [0.492,  0.415,  0.366,   0.258], 'Q2-y=12, z-pT=14':   [0.492,  0.415,  0.478,   0.366], 'Q2-y=12, z-pT=15':   [0.492,  0.415,  0.59,    0.478], 'Q2-y=12, z-pT=16':   [0.578,  0.492,  0.153,    0.05], 'Q2-y=12, z-pT=17':   [0.578,  0.492,  0.258,   0.153], 'Q2-y=12, z-pT=18':   [0.578,  0.492,  0.366,   0.258], 'Q2-y=12, z-pT=19':   [0.578,  0.492,  0.478,   0.366], 'Q2-y=12, z-pT=20':   [0.578,  0.492,  0.59,    0.478], 'Q2-y=12, z-pT=21':   [0.665,  0.578,  0.153,    0.05], 'Q2-y=12, z-pT=22':   [0.665,  0.578,  0.258,   0.153], 'Q2-y=12, z-pT=23':   [0.665,  0.578,  0.366,   0.258], 'Q2-y=12, z-pT=24':   [0.665,  0.578,  0.478,   0.366], 'Q2-y=12, z-pT=25':   [0.665,  0.578,  0.59,    0.478], 'Q2-y=13, z-pT=All':  [0.665,  0.27,   0.59,     0.05], 'Q2-y=13, z-pT=0':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=13, z-pT=1':    [0.34,   0.27,   0.153,    0.05], 'Q2-y=13, z-pT=2':    [0.34,   0.27,   0.258,   0.153], 'Q2-y=13, z-pT=3':    [0.34,   0.27,   0.366,   0.258], 'Q2-y=13, z-pT=4':    [0.34,   0.27,   0.478,   0.366], 'Q2-y=13, z-pT=5':    [0.34,   0.27,   0.59,    0.478], 'Q2-y=13, z-pT=6':    [0.415,  0.34,   0.153,    0.05], 'Q2-y=13, z-pT=7':    [0.415,  0.34,   0.258,   0.153], 'Q2-y=13, z-pT=8':    [0.415,  0.34,   0.366,   0.258], 'Q2-y=13, z-pT=9':    [0.415,  0.34,   0.478,   0.366], 'Q2-y=13, z-pT=10':   [0.415,  0.34,   0.59,    0.478], 'Q2-y=13, z-pT=11':   [0.492,  0.415,  0.153,    0.05], 'Q2-y=13, z-pT=12':   [0.492,  0.415,  0.258,   0.153], 'Q2-y=13, z-pT=13':   [0.492,  0.415,  0.366,   0.258], 'Q2-y=13, z-pT=14':   [0.492,  0.415,  0.478,   0.366], 'Q2-y=13, z-pT=15':   [0.492,  0.415,  0.59,    0.478], 'Q2-y=13, z-pT=16':   [0.578,  0.492,  0.153,    0.05], 'Q2-y=13, z-pT=17':   [0.578,  0.492,  0.258,   0.153], 'Q2-y=13, z-pT=18':   [0.578,  0.492,  0.366,   0.258], 'Q2-y=13, z-pT=19':   [0.578,  0.492,  0.478,   0.366], 'Q2-y=13, z-pT=20':   [0.578,  0.492,  0.59,    0.478], 'Q2-y=13, z-pT=21':   [0.665,  0.578,  0.153,    0.05], 'Q2-y=13, z-pT=22':   [0.665,  0.578,  0.258,   0.153], 'Q2-y=13, z-pT=23':   [0.665,  0.578,  0.366,   0.258], 'Q2-y=13, z-pT=24':   [0.665,  0.578,  0.478,   0.366], 'Q2-y=13, z-pT=25':   [0.665,  0.578,  0.59,    0.478], 'Q2-y=14, z-pT=All':  [0.665,  0.27,   0.59,     0.05], 'Q2-y=14, z-pT=0':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=14, z-pT=1':    [0.34,   0.27,   0.153,    0.05], 'Q2-y=14, z-pT=2':    [0.34,   0.27,   0.258,   0.153], 'Q2-y=14, z-pT=3':    [0.34,   0.27,   0.366,   0.258], 'Q2-y=14, z-pT=4':    [0.34,   0.27,   0.478,   0.366], 'Q2-y=14, z-pT=5':    [0.34,   0.27,   0.59,    0.478], 'Q2-y=14, z-pT=6':    [0.415,  0.34,   0.153,    0.05], 'Q2-y=14, z-pT=7':    [0.415,  0.34,   0.258,   0.153], 'Q2-y=14, z-pT=8':    [0.415,  0.34,   0.366,   0.258], 'Q2-y=14, z-pT=9':    [0.415,  0.34,   0.478,   0.366], 'Q2-y=14, z-pT=10':   [0.415,  0.34,   0.59,    0.478], 'Q2-y=14, z-pT=11':   [0.492,  0.415,  0.153,    0.05], 'Q2-y=14, z-pT=12':   [0.492,  0.415,  0.258,   0.153], 'Q2-y=14, z-pT=13':   [0.492,  0.415,  0.366,   0.258], 'Q2-y=14, z-pT=14':   [0.492,  0.415,  0.478,   0.366], 'Q2-y=14, z-pT=15':   [0.492,  0.415,  0.59,    0.478], 'Q2-y=14, z-pT=16':   [0.578,  0.492,  0.153,    0.05], 'Q2-y=14, z-pT=17':   [0.578,  0.492,  0.258,   0.153], 'Q2-y=14, z-pT=18':   [0.578,  0.492,  0.366,   0.258], 'Q2-y=14, z-pT=19':   [0.578,  0.492,  0.478,   0.366], 'Q2-y=14, z-pT=20':   [0.578,  0.492,  0.59,    0.478], 'Q2-y=14, z-pT=21':   [0.665,  0.578,  0.153,    0.05], 'Q2-y=14, z-pT=22':   [0.665,  0.578,  0.258,   0.153], 'Q2-y=14, z-pT=23':   [0.665,  0.578,  0.366,   0.258], 'Q2-y=14, z-pT=24':   [0.665,  0.578,  0.478,   0.366], 'Q2-y=14, z-pT=25':   [0.665,  0.578,  0.59,    0.478], 'Q2-y=15, z-pT=All':  [0.665,  0.27,   0.59,     0.05], 'Q2-y=15, z-pT=0':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=15, z-pT=1':    [0.34,   0.27,   0.153,    0.05], 'Q2-y=15, z-pT=2':    [0.34,   0.27,   0.258,   0.153], 'Q2-y=15, z-pT=3':    [0.34,   0.27,   0.366,   0.258], 'Q2-y=15, z-pT=4':    [0.34,   0.27,   0.478,   0.366], 'Q2-y=15, z-pT=5':    [0.34,   0.27,   0.59,    0.478], 'Q2-y=15, z-pT=6':    [0.415,  0.34,   0.153,    0.05], 'Q2-y=15, z-pT=7':    [0.415,  0.34,   0.258,   0.153], 'Q2-y=15, z-pT=8':    [0.415,  0.34,   0.366,   0.258], 'Q2-y=15, z-pT=9':    [0.415,  0.34,   0.478,   0.366], 'Q2-y=15, z-pT=10':   [0.415,  0.34,   0.59,    0.478], 'Q2-y=15, z-pT=11':   [0.492,  0.415,  0.153,    0.05], 'Q2-y=15, z-pT=12':   [0.492,  0.415,  0.258,   0.153], 'Q2-y=15, z-pT=13':   [0.492,  0.415,  0.366,   0.258], 'Q2-y=15, z-pT=14':   [0.492,  0.415,  0.478,   0.366], 'Q2-y=15, z-pT=15':   [0.492,  0.415,  0.59,    0.478], 'Q2-y=15, z-pT=16':   [0.578,  0.492,  0.153,    0.05], 'Q2-y=15, z-pT=17':   [0.578,  0.492,  0.258,   0.153], 'Q2-y=15, z-pT=18':   [0.578,  0.492,  0.366,   0.258], 'Q2-y=15, z-pT=19':   [0.578,  0.492,  0.478,   0.366], 'Q2-y=15, z-pT=20':   [0.578,  0.492,  0.59,    0.478], 'Q2-y=15, z-pT=21':   [0.665,  0.578,  0.153,    0.05], 'Q2-y=15, z-pT=22':   [0.665,  0.578,  0.258,   0.153], 'Q2-y=15, z-pT=23':   [0.665,  0.578,  0.366,   0.258], 'Q2-y=15, z-pT=24':   [0.665,  0.578,  0.478,   0.366], 'Q2-y=15, z-pT=25':   [0.665,  0.578,  0.59,    0.478], 'Q2-y=16, z-pT=All':  [0.665,  0.27,   0.59,     0.05], 'Q2-y=16, z-pT=0':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=16, z-pT=1':    [0.34,   0.27,   0.153,    0.05], 'Q2-y=16, z-pT=2':    [0.34,   0.27,   0.258,   0.153], 'Q2-y=16, z-pT=3':    [0.34,   0.27,   0.366,   0.258], 'Q2-y=16, z-pT=4':    [0.34,   0.27,   0.478,   0.366], 'Q2-y=16, z-pT=5':    [0.34,   0.27,   0.59,    0.478], 'Q2-y=16, z-pT=6':    [0.415,  0.34,   0.153,    0.05], 'Q2-y=16, z-pT=7':    [0.415,  0.34,   0.258,   0.153], 'Q2-y=16, z-pT=8':    [0.415,  0.34,   0.366,   0.258], 'Q2-y=16, z-pT=9':    [0.415,  0.34,   0.478,   0.366], 'Q2-y=16, z-pT=10':   [0.415,  0.34,   0.59,    0.478], 'Q2-y=16, z-pT=11':   [0.492,  0.415,  0.153,    0.05], 'Q2-y=16, z-pT=12':   [0.492,  0.415,  0.258,   0.153], 'Q2-y=16, z-pT=13':   [0.492,  0.415,  0.366,   0.258], 'Q2-y=16, z-pT=14':   [0.492,  0.415,  0.478,   0.366], 'Q2-y=16, z-pT=15':   [0.492,  0.415,  0.59,    0.478], 'Q2-y=16, z-pT=16':   [0.578,  0.492,  0.153,    0.05], 'Q2-y=16, z-pT=17':   [0.578,  0.492,  0.258,   0.153], 'Q2-y=16, z-pT=18':   [0.578,  0.492,  0.366,   0.258], 'Q2-y=16, z-pT=19':   [0.578,  0.492,  0.478,   0.366], 'Q2-y=16, z-pT=20':   [0.578,  0.492,  0.59,    0.478], 'Q2-y=16, z-pT=21':   [0.665,  0.578,  0.153,    0.05], 'Q2-y=16, z-pT=22':   [0.665,  0.578,  0.258,   0.153], 'Q2-y=16, z-pT=23':   [0.665,  0.578,  0.366,   0.258], 'Q2-y=16, z-pT=24':   [0.665,  0.578,  0.478,   0.366], 'Q2-y=16, z-pT=25':   [0.665,  0.578,  0.59,    0.478], 'Q2-y=17, z-pT=All':  [0.665,  0.27,   0.59,     0.05], 'Q2-y=17, z-pT=0':    [0.665,  0.27,   0.59,     0.05], 'Q2-y=17, z-pT=1':    [0.34,   0.27,   0.153,    0.05], 'Q2-y=17, z-pT=2':    [0.34,   0.27,   0.258,   0.153], 'Q2-y=17, z-pT=3':    [0.34,   0.27,   0.366,   0.258], 'Q2-y=17, z-pT=4':    [0.34,   0.27,   0.478,   0.366], 'Q2-y=17, z-pT=5':    [0.34,   0.27,   0.59,    0.478], 'Q2-y=17, z-pT=6':    [0.415,  0.34,   0.153,    0.05], 'Q2-y=17, z-pT=7':    [0.415,  0.34,   0.258,   0.153], 'Q2-y=17, z-pT=8':    [0.415,  0.34,   0.366,   0.258], 'Q2-y=17, z-pT=9':    [0.415,  0.34,   0.478,   0.366], 'Q2-y=17, z-pT=10':   [0.415,  0.34,   0.59,    0.478], 'Q2-y=17, z-pT=11':   [0.492,  0.415,  0.153,    0.05], 'Q2-y=17, z-pT=12':   [0.492,  0.415,  0.258,   0.153], 'Q2-y=17, z-pT=13':   [0.492,  0.415,  0.366,   0.258], 'Q2-y=17, z-pT=14':   [0.492,  0.415,  0.478,   0.366], 'Q2-y=17, z-pT=15':   [0.492,  0.415,  0.59,    0.478], 'Q2-y=17, z-pT=16':   [0.578,  0.492,  0.153,    0.05], 'Q2-y=17, z-pT=17':   [0.578,  0.492,  0.258,   0.153], 'Q2-y=17, z-pT=18':   [0.578,  0.492,  0.366,   0.258], 'Q2-y=17, z-pT=19':   [0.578,  0.492,  0.478,   0.366], 'Q2-y=17, z-pT=20':   [0.578,  0.492,  0.59,    0.478], 'Q2-y=17, z-pT=21':   [0.665,  0.578,  0.153,    0.05], 'Q2-y=17, z-pT=22':   [0.665,  0.578,  0.258,   0.153], 'Q2-y=17, z-pT=23':   [0.665,  0.578,  0.366,   0.258], 'Q2-y=17, z-pT=24':   [0.665,  0.578,  0.478,   0.366], 'Q2-y=17, z-pT=25':   [0.665,  0.578,  0.59,    0.478], 'Q2-y=18': 'end'}

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Get_z_pT_Bin_Corners(z_pT_Bin_Num="All", Q2_y_Bin_Num=1, Integration_Bins_Q=False):
    if(Integration_Bins_Q):
        Bin_Definition_Array_str = f'Q2-y={str(Q2_y_Bin_Num).replace("All", "0")}, z-pT={z_pT_Bin_Num}'
        return Int_Bin_Definition_Array[Bin_Definition_Array_str]
        ###### return [z_max, z_min, pT_max, pT_min]
    else:
        if(str(z_pT_Bin_Num) in ["All", "0"]):
            New_z_pT_Bin_Test_List = New_z_pT_Bin_Test(Q2_y_Bin_Num)
            z_Borders  = New_z_pT_Bin_Test_List[0][2]
            pT_Borders = New_z_pT_Bin_Test_List[1][2]
            return ["z", z_Borders, "pT", pT_Borders]
        Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2 = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Num)
        Bin_Definition_Array_str = "end"
        if(z_pT_Bin_Num  in Migration_Bin_2):
            Bin_Definition_Array_str = f'Q2-y={Q2_y_Bin_Num}, z-pT={z_pT_Bin_Num} - REMOVE - MIGRATION BIN'
        elif(z_pT_Bin_Num > Migration_Bin_1):
            Bin_Definition_Array_str = f'Q2-y={Q2_y_Bin_Num}, z-pT={z_pT_Bin_Num} - MIGRATION BIN'
        else:
            Bin_Definition_Array_str = f'Q2-y={Q2_y_Bin_Num}, z-pT={z_pT_Bin_Num}'
        return Bin_Definition_Array[Bin_Definition_Array_str]
        ###### return [z_max, z_min, pT_max, pT_min]

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=1, Set_Max_Y=False, Set_Max_X=False, Plot_Orientation_Input="z_pT", Integration_Bins_Q=False):
    z_pT_Bins_Borders = {}
    if(Integration_Bins_Q):
        bin_color = root_color.Black
        line_size = 4
        for z_pT in range(1, 26, 1):
            y_max, y_min, x_max, x_min = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT, Q2_y_Bin_Num=Q2_y_Bin_Num_In, Integration_Bins_Q=True)
            if(Set_Max_Y):
                if(Set_Max_Y < y_max):
                    y_max = Set_Max_Y
            if(Set_Max_X):
                if(Set_Max_X < x_max):
                    x_max = Set_Max_X
            if(Plot_Orientation_Input in ["pT_z"]):
                x_max, x_min, y_max, y_min = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT, Q2_y_Bin_Num=Q2_y_Bin_Num_In, Integration_Bins_Q=True)
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_max, y_max, x_min, y_max)
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_min, y_max, x_min, y_min)
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_min, y_min, x_max, y_min)
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_max, y_min, x_max, y_max)
    else:
        Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2 = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Num_In)
        for z_pT in range(1, Total_Number_of_Bins + 1, 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_y_Bin_Num_In, Z_PT_BIN=z_pT, BINNING_METHOD="_Y_bin")):
                continue
            bin_color = 41 if(z_pT in Migration_Bin_2) else root_color.Black if(z_pT < (Migration_Bin_1 + 1)) else root_color.Red
            if(bin_color == root_color.Red):
                break
            line_size =  1 if(z_pT in Migration_Bin_2) else 4 if(z_pT < (Migration_Bin_1 + 1)) else 2
            y_max, y_min, x_max, x_min = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT, Q2_y_Bin_Num=Q2_y_Bin_Num_In)
            if(Set_Max_Y):
                if(Set_Max_Y < y_max):
                    y_max = Set_Max_Y
            if(Set_Max_X):
                if(Set_Max_X < x_max):
                    x_max = Set_Max_X
            if(Plot_Orientation_Input in ["pT_z"]):
                x_max, x_min, y_max, y_min = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT, Q2_y_Bin_Num=Q2_y_Bin_Num_In)
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_max, y_max, x_min, y_max)
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_min, y_max, x_min, y_min)
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_min, y_min, x_max, y_min)
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_max, y_min, x_max, y_max)
        # del z_pT_Bins_Borders

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=1, Integration_Bins_Q=False):
    if(Integration_Bins_Q):
        columns, rows = 5, 5
        return [rows, columns]
    if((str(Q2_Y_Bin_Input) in ["All", "all", "0", "-1", "-2", "-3"])):
        columns, rows = 1, 1
    if(str(Q2_Y_Bin_Input) == "1"):
        columns, rows = 7, 5
    if(str(Q2_Y_Bin_Input) == "2"):
        columns, rows = 6, 6
    if(str(Q2_Y_Bin_Input) == "3"):
        columns, rows = 6, 5
    if(str(Q2_Y_Bin_Input) == "4"):
        columns, rows = 6, 6
    if(str(Q2_Y_Bin_Input) == "5"):
        columns, rows = 6, 6
    if(str(Q2_Y_Bin_Input) == "6"):
        columns, rows = 6, 5
    if(str(Q2_Y_Bin_Input) == "7"):
        columns, rows = 6, 6
    if(str(Q2_Y_Bin_Input) == "8"):
        columns, rows = 5, 7
    if(str(Q2_Y_Bin_Input) == "9"):
        columns, rows = 7, 5
    if(str(Q2_Y_Bin_Input) == "10"):
        columns, rows = 6, 6
    if(str(Q2_Y_Bin_Input) == "11"):
        columns, rows = 5, 5
    if(str(Q2_Y_Bin_Input) == "12"):
        columns, rows = 5, 5
    if(str(Q2_Y_Bin_Input) == "13"):
        columns, rows = 5, 6
    if(str(Q2_Y_Bin_Input) == "14"):
        columns, rows = 6, 6
    if(str(Q2_Y_Bin_Input) == "15"):
        columns, rows = 5, 5
    if(str(Q2_Y_Bin_Input) == "16"):
        columns, rows = 6, 5
    if(str(Q2_Y_Bin_Input) == "17"):
        columns, rows = 6, 5
    return [rows, columns]
    # For normal orientation, row -> z values while columns -> pT values

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##




#####################################################################################################################################################
##==========##==========##     Missing Mass Lines for z-pT Histograms      ##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################

def MM_z_pT_Draw(z_val=0.1, MM_val=1.5, Q2_y_Bin=1, pT_Input="pT", Q2_y_value_pick="Center", Binning_Method_Input=Binning_Method):
    # If z_val="pT", then this function will return 2 equations to plot z as a function of pT (use when pT is on the x-axis)
        # Any other input will plot pT as a function of z
        # These options will only return 1 equation
    # If either z_val or pT_Input are inputted as numbers (i.e., anything other than a string), then this function will return a single calculation based on the input
        # If z_val != "pT", then not input of pT_Input will change the output of this code
        # If z_val and pT_Input are strings, then the output of this function will be the equation(s) for drawing the MM cut line
    Q2_val = 4.00
    y_val  = 0.55
    if(str(Q2_y_Bin) in ["1"]):
        Q2_val = 2.204
        y_val  = 0.6999
    if(str(Q2_y_Bin) in ["2"]):
        Q2_val = 2.206
        y_val  = 0.6003
    if(str(Q2_y_Bin) in ["3"]):
        Q2_val = 2.207
        y_val  = 0.5014
    if(str(Q2_y_Bin) in ["4"]):
        Q2_val = 2.206
        y_val  = 0.3883
    if(str(Q2_y_Bin) in ["5"]):
        Q2_val = 2.689
        y_val  = 0.6997
    if(str(Q2_y_Bin) in ["6"]):
        Q2_val = 2.689
        y_val  = 0.6001
    if(str(Q2_y_Bin) in ["7"]):
        Q2_val = 2.689
        y_val  = 0.5014
    if(str(Q2_y_Bin) in ["8"]):
        Q2_val = 2.681
        y_val  = 0.3921
    if(str(Q2_y_Bin) in ["9"]):
        Q2_val = 3.431
        y_val  = 0.6996
    if(str(Q2_y_Bin) in ["10"]):
        Q2_val = 3.426
        y_val  = 0.6004
    if(str(Q2_y_Bin) in ["11"]):
        Q2_val = 3.416
        y_val  = 0.5022
    if(str(Q2_y_Bin) in ["12"]):
        Q2_val = 3.391
        y_val  = 0.408
    if(str(Q2_y_Bin) in ["13"]):
        Q2_val = 4.582
        y_val  = 0.7003
    if(str(Q2_y_Bin) in ["14"]):
        Q2_val = 4.564
        y_val  = 0.6015
    if(str(Q2_y_Bin) in ["15"]):
        Q2_val = 4.663
        y_val  = 0.5049
    if(str(Q2_y_Bin) in ["16"]):
        Q2_val = 6.54
        y_val  = 0.7011
    if(str(Q2_y_Bin) in ["17"]):
        Q2_val = 6.221
        y_val  = 0.6045
    if(Q2_y_value_pick not in ["Center", "Center_N"]):
        if("y_bin" in Binning_Method_Input):
            Borders_Q2_y = Q2_y_Border_Lines(Q2_y_Bin)
            Q2_bin_max   = Borders_Q2_y[0][1][1]
            Q2_bin_min   = Borders_Q2_y[0][0][1]
            y_bin_max    = Borders_Q2_y[1][1][0]
            y_bin_min    = Borders_Q2_y[1][0][0]
        else:
            Q2_bin_max, Q2_bin_min, y_bin_max, y_bin_min = Q2_Y_Border_Lines(Q2_y_Bin)
            
        if(Q2_y_value_pick in ["Minimum"]):
            Q2_val   = Q2_bin_min
            y_val    = y_bin_max
        if(Q2_y_value_pick in ["Maximum"]):
            Q2_val   = Q2_bin_max
            y_val    = y_bin_min
    Ebeam   = 10.6041
    mpro    = 0.938272
    mpip    = 0.13957
    v_Term  = y_val*Ebeam
    W2_Term = mpro*mpro - Q2_val + 2*mpro*v_Term
    pT_val  = pT_Input
    if(z_val not in ["pT"]):
        B_Term      = 2*ROOT.sqrt(Q2_val + v_Term*v_Term)
        if(type(z_val) is not str):
            A_Term  = W2_Term - MM_val*MM_val + mpip*mpip - 2*(mpro + v_Term)*v_Term*z_val
            C_Term  = (v_Term*v_Term)*(z_val*z_val) - mpip*mpip
            pT_2    = C_Term - ((A_Term*A_Term)/(B_Term*B_Term))
            if(pT_2 > 0):
                pT_val = ROOT.sqrt(pT_2)
            else:
                print("\x1b[91m\x1b[1m", "\nERROR IN CALCULATING pT\n", "\x1b[0m\x1b[1m", "pT^2 =", pT_2, "should be greater than 0.", "\x1b[0m")
                print("Calculation Error occurred with the inputs of:", "\x1b[1m",        "\n\tz_val    =", z_val, "\n\tMM_val   =", MM_val, "\n\tQ2_y_Bin =", Q2_y_Bin, "\x1b[0m")
                pT_val = ROOT.sqrt(pT_2)
        else:
            A_Term  = "".join([str(W2_Term - MM_val*MM_val + mpip*mpip), " - ", str(2*(mpro + v_Term)*v_Term), "*x"])
            A2_Term = "".join(["(", str(A_Term), ")*(", str(A_Term), ")"])
            C_Term  = "".join([str(v_Term*v_Term), "*(x*x) - ", str(mpip*mpip)])
            pT_2    = "".join([str(C_Term), " - ((", str(A2_Term), ")/(", str(B_Term*B_Term), "))"])
            pT_val  = "".join(["sqrt(", str(pT_2), ")"])
        return pT_val
    else:
        A_Term      = mpro*mpro + mpip*mpip - Q2_val - MM_val*MM_val + 2*v_Term*mpro
        B_Term      = -2*(mpro*v_Term + v_Term*v_Term)
        C_Term      = 2*ROOT.sqrt(Q2_val + v_Term*v_Term)
        D_Term      = "".join(["(", str(mpip*mpip), ") + (x*x)"])
        Term_A      = ((B_Term*B_Term)/(C_Term*C_Term)) - (v_Term*v_Term)
        Term_B      = (2*A_Term*B_Term)/(C_Term*C_Term)
        Term_C      = "".join([str((A_Term*A_Term)/(C_Term*C_Term)), " + ", str(D_Term)])
        if(type(pT_Input) is not str):
            D_Term  = mpip*mpip + pT_val*pT_val
            Term_C  = (A_Term*A_Term)/(C_Term*C_Term) + D_Term
        z_function_p     = "".join(["((", str(-Term_B), ") + sqrt((", str(Term_B*Term_B), ") - ((", str(4*Term_A), ")*(", str(Term_C), "))))/(", str(2*Term_A), ")"])
        z_function_m     = "".join(["((", str(-Term_B), ") - sqrt((", str(Term_B*Term_B), ") - ((", str(4*Term_A), ")*(", str(Term_C), "))))/(", str(2*Term_A), ")"])
        if(type(pT_Input) is not str):
            z_function_p = round((-Term_B + ROOT.sqrt((Term_B*Term_B) - (4*Term_A*Term_C)))/(2*Term_A),  5)
            z_function_m = round((-Term_B - ROOT.sqrt((Term_B*Term_B) - (4*Term_A*Term_C)))/(2*Term_A),  5)
        return [z_function_p, z_function_m]
        
#####################################################################################################################################################
##==========##==========##     Missing Mass Lines for z-pT Histograms      ##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################



##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Draw_the_MM_Cut_Lines(MM_z_pT_legend, MM_z_pT_borders={}, Q2_Y_Bin=1, Plot_Orientation="pT_z"):
    if(Plot_Orientation in ["pT_z"]):
        for Q2_y_value_pick_ii in ["Minimum", "Maximum", "Center", "Center_N"]:
            MM = 0.93956 if(Q2_y_value_pick_ii in ["Center_N"]) else 1.5
            pT_function     = MM_z_pT_Draw(z_val="function", MM_val=MM, Q2_y_Bin=Q2_Y_Bin, pT_Input="pT", Q2_y_value_pick=str(Q2_y_value_pick_ii))
            z_values_step   = 0.001
            num_decimals    = 3
            z_values, z_min = 0, 0
            z_max           = 0.3 if(Q2_y_value_pick_ii in ["Maximum"]) else 0.6 if(MM not in [2.0]) else 0.17 if(str(Q2_Y_Bin) in ["12"]) else 0.34
            z_min_set_Q     = False
            while(z_values < 1.2):
                if(("nan" not in str(eval(str(pT_function.replace("x", str(z_values))).replace("sqrt", "ROOT.sqrt")))) and (not z_min_set_Q)):
                    z_min       = z_values
                    z_values    = z_max
                    z_min_set_Q = True
                if(("nan"     in str(eval(str(pT_function.replace("x", str(z_values))).replace("sqrt", "ROOT.sqrt")))) and (z_min_set_Q)):
                    z_max       = round(z_values - z_values_step, num_decimals)
                    break
                z_values += z_values_step
                z_values  = round(z_values, num_decimals)
            MM_z_pT_borders[str(Q2_y_value_pick_ii)] = ROOT.TF1("".join(["MM_Line_", str(Q2_y_value_pick_ii), "_Q2_y_Bin_", str(Q2_Y_Bin)]), pT_function, z_min, z_max)
            MM_z_pT_borders[str(Q2_y_value_pick_ii)].SetLineColor(12 if(Q2_y_value_pick_ii in ["Center"]) else 8 if(Q2_y_value_pick_ii in ["Maximum"]) else 46 if(Q2_y_value_pick_ii in ["Minimum"]) else 28)
            if(Q2_y_value_pick_ii not in ["Center"]):
                MM_z_pT_borders[str(Q2_y_value_pick_ii)].SetLineStyle(2)  # Dashed line
                MM_z_pT_borders[str(Q2_y_value_pick_ii)].SetLineWidth(4)
            else:
                MM_z_pT_borders[str(Q2_y_value_pick_ii)].SetLineWidth(2)
                MM_z_pT_borders[str(Q2_y_value_pick_ii)].SetLineWidth(2)
            MM_z_pT_borders[str(Q2_y_value_pick_ii)].Draw("same")
            Legend_Title_Name = "".join([str(Q2_y_value_pick_ii) if(str(Q2_y_value_pick_ii) not in ["Center_N"]) else "Center (Neutron)", " MM Cut"])
            MM_z_pT_legend.AddEntry(MM_z_pT_borders[str(Q2_y_value_pick_ii)], str(Legend_Title_Name), "l")
        MM_z_pT_legend.Draw("same")
    else:
        for Q2_y_value_pick_ii in ["Minimum", "Maximum", "Center", "Center_N"]:
            MM = 0.93956 if(Q2_y_value_pick_ii in ["Center_N"]) else 1.5
            z_function_p, z_function_m = MM_z_pT_Draw(z_val="pT", MM_val=MM, Q2_y_Bin=Q2_Y_Bin, pT_Input="pT", Q2_y_value_pick=str(Q2_y_value_pick_ii))
            pT_Max = 0.95 if(str(Q2_Y_Bin) in ["12"]) else 1.05 if(str(Q2_Y_Bin) in ["8", "15", "17"]) else 1.15 if(str(Q2_Y_Bin) in ["4", "11", "16"]) else 1.50
            while(pT_Max > 0):
                z_values = MM_z_pT_Draw(z_val="pT", MM_val=MM, Q2_y_Bin=Q2_Y_Bin, pT_Input=pT_Max, Q2_y_value_pick=str(Q2_y_value_pick_ii))
                rounding_condition = (round(z_values[0] - z_values[1], 2) == 0)
                if(("nan" not in str(z_values[1])) or (rounding_condition)):
                    break
                pT_Max += -0.000005
                pT_Max = round(pT_Max, 7)
            MM_z_pT_borders["".join(["P_",     str(Q2_y_value_pick_ii)])] = ROOT.TF1("".join(["P_MM_Line_", str(Q2_y_value_pick_ii), "_Q2_y_Bin_", str(Q2_Y_Bin)]), z_function_p, 0, pT_Max)
            MM_z_pT_borders["".join(["M_",     str(Q2_y_value_pick_ii)])] = ROOT.TF1("".join(["M_MM_Line_", str(Q2_y_value_pick_ii), "_Q2_y_Bin_", str(Q2_Y_Bin)]), z_function_m, 0, pT_Max)
            MM_z_pT_borders["".join(["P_",     str(Q2_y_value_pick_ii)])].SetLineColor(12 if(Q2_y_value_pick_ii in ["Center"]) else 8 if(Q2_y_value_pick_ii in ["Maximum"]) else 46 if(Q2_y_value_pick_ii in ["Minimum"]) else 28)
            MM_z_pT_borders["".join(["M_",     str(Q2_y_value_pick_ii)])].SetLineColor(12 if(Q2_y_value_pick_ii in ["Center"]) else 8 if(Q2_y_value_pick_ii in ["Maximum"]) else 46 if(Q2_y_value_pick_ii in ["Minimum"]) else 28)
            if(Q2_y_value_pick_ii not in ["Center"]):
                MM_z_pT_borders["".join(["P_", str(Q2_y_value_pick_ii)])].SetLineStyle(2)  # Dashed line
                MM_z_pT_borders["".join(["M_", str(Q2_y_value_pick_ii)])].SetLineStyle(2)
                MM_z_pT_borders["".join(["P_", str(Q2_y_value_pick_ii)])].SetLineWidth(4)
                MM_z_pT_borders["".join(["M_", str(Q2_y_value_pick_ii)])].SetLineWidth(4)
            else:
                MM_z_pT_borders["".join(["P_", str(Q2_y_value_pick_ii)])].SetLineWidth(2)
                MM_z_pT_borders["".join(["M_", str(Q2_y_value_pick_ii)])].SetLineWidth(2)
            MM_z_pT_borders["".join(["P_",     str(Q2_y_value_pick_ii)])].Draw("same")
            MM_z_pT_borders["".join(["M_",     str(Q2_y_value_pick_ii)])].Draw("same")
            Legend_Title_Name = "".join([str(Q2_y_value_pick_ii) if(str(Q2_y_value_pick_ii) not in ["Center_N"]) else "Center (Neutron)", " MM Cut"])
            MM_z_pT_legend.AddEntry(MM_z_pT_borders["".join(["P_", str(Q2_y_value_pick_ii)])], str(Legend_Title_Name), "l")
        MM_z_pT_legend.Draw("same")
        
    return [MM_z_pT_borders, MM_z_pT_legend]

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

#####################################################################################################################################################################
##==========##==========##     Function for Finding Kinematic Binning Info     ##==========##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################################
def Find_Q2_y_z_pT_Bin_Stats(Q2_y_Bin_Find, z_pT_Bin_Find="All", List_Of_Histos_For_Stats_Search="Use_Center", Smearing_Q="''", DataType="bbb", Binning_Method_Input=Binning_Method):
    if(str(List_Of_Histos_For_Stats_Search) in ["Use_Center"]):
        ####################======================================####################
        #####==========#####   Finding the Q2-y Bin Information   #####==========#####
        ####################======================================####################
        if("y_bin" in Binning_Method_Input):
            Borders_Q2_y = Q2_y_Border_Lines(Q2_y_Bin_Find)
            Q2_bin_max   = Borders_Q2_y[0][1][1]
            Q2_bin_min   = Borders_Q2_y[0][0][1]
            y_bin_max    = Borders_Q2_y[1][1][0]
            y_bin_min    = Borders_Q2_y[1][0][0]
        else:
            Borders_Q2_y = Q2_Y_Border_Lines(Q2_y_Bin_Find)
            Q2_bin_max, Q2_bin_min, y_bin_max, y_bin_min = Q2_Y_Border_Lines(Q2_y_Bin_Find)
        Q2_Center = (Q2_bin_max + Q2_bin_min)/2
        y_Center  = (y_bin_max  + y_bin_min)/2
        ####################======================================####################
        #####==========#####    Found the Q2-y Bin Information    #####==========#####
        ####################======================================####################

        ####################======================================####################
        #####==========#####   Finding the z-pT Bin Information   #####==========#####
        ####################======================================####################
        if(("y_bin" in Binning_Method_Input) or (str(z_pT_Bin_Find) in ["All", "0"])):
            Borders_z_pT   = z_pT_Border_Lines(Q2_y_Bin_Find)
            z_length       = Borders_z_pT[0][1] - 1
            pT_length      = Borders_z_pT[1][1] - 1
            if(str(z_pT_Bin_Find) not in ["All", "0"]):
                # This finds the dimensions of a particular z-pT bin for a given Q2-y bin
                z_bin      = ((z_pT_Bin_Find - 1) // pT_length) + 1
                z_bin      = (z_length + 1) - z_bin
                pT_bin     = ((z_pT_Bin_Find - 1) %  pT_length) + 1
                z_bin_max  = Borders_z_pT[0][2][z_bin]
                z_bin_min  = Borders_z_pT[0][2][z_bin  - 1]
                pT_bin_max = Borders_z_pT[1][2][pT_bin]
                pT_bin_min = Borders_z_pT[1][2][pT_bin - 1]
            else:
                # This gives the overall dimensions of the combined z-pT binning scheme for a given Q2-y bin (i.e., if all z-pT binned events are to be included)
                z_bin_max  = Borders_z_pT[0][2][len(Borders_z_pT[0][2]) - 1]
                z_bin_min  = Borders_z_pT[0][2][0]
                pT_bin_max = Borders_z_pT[1][2][len(Borders_z_pT[1][2]) - 1]
                pT_bin_min = Borders_z_pT[1][2][0]
        else:
            z_bin_max, z_bin_min, pT_bin_max, pT_bin_min = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT_Bin_Find, Q2_y_Bin_Num=Q2_y_Bin_Find)
        z_Center       = (z_bin_max  + z_bin_min)/2
        pT_Center      = (pT_bin_max + pT_bin_min)/2
        ####################======================================####################
        #####==========#####    Found the z-pT Bin Information    #####==========#####
        ####################======================================####################
        
        # Return order goes as [[Q2_bin_info, y_bin_info], [z_bin_info, pT_bin_info]]
            # Order of bin_info goes as: bin_info = [min_bin, center_bin, max_bin]
        return [[[Q2_bin_min, Q2_Center, Q2_bin_max], [y_bin_min, y_Center, y_bin_max]], [[z_bin_min, z_Center, z_bin_max], [pT_bin_min, pT_Center, pT_bin_max]]]
    else:
        Histo_Search_Name_Q2_y = "".join(["(Normal_2D)_(", str(DataType), ")_(SMEAR=", "''" if(str(Smearing_Q) in [""]) else str(Smearing_Q), ")_(Q2_y_Bin_", str(Q2_y_Bin_Find), ")_(z_pT_Bin_All)_(Q2)_(y)"])
        Histo_Search_Name_z_pT = "".join(["(Normal_2D)_(", str(DataType), ")_(SMEAR=", "''" if(str(Smearing_Q) in [""]) else str(Smearing_Q), ")_(Q2_y_Bin_", str(Q2_y_Bin_Find), ")_(z_pT_Bin_All)_(z)_(pT)"])
        
        Histo_Search_Q2_y      = List_Of_Histos_For_Stats_Search[str(Histo_Search_Name_Q2_y)]
        Histo_Search_z_pT      = List_Of_Histos_For_Stats_Search[str(Histo_Search_Name_z_pT)]
        
        # Find the z-pT bin corresponding to the provided value
        z_pT_bin_0 = Histo_Search_Q2_y.GetXaxis().FindBin(z_pT_Bin_Find if(str(z_pT_Bin_Find) not in ["All", "0"]) else 0)
        z_pT_bin_1 = Histo_Search_Q2_y.GetXaxis().FindBin(z_pT_Bin_Find if(str(z_pT_Bin_Find) not in ["All", "0"]) else Histo_Search_Q2_y.GetNbinsX())
        if(str(z_pT_Bin_Find) not in ["All", "0"]):
            Histo_Search_Q2_y.GetXaxis().SetRange(z_pT_bin_0, z_pT_bin_1)
            Histo_Search_z_pT.GetXaxis().SetRange(z_pT_bin_0, z_pT_bin_1)
            
        Histo_Search_Q2_y_2D = Histo_Search_Q2_y.Project3D("yz e").Clone(str(Histo_Search_Name_Q2_y).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", str(z_pT_Bin_Find)])))
        Histo_Search_z_pT_2D = Histo_Search_z_pT.Project3D("yz e").Clone(str(Histo_Search_Name_z_pT).replace("z_pT_Bin_All", "".join(["z_pT_Bin_", str(z_pT_Bin_Find)])))
        
        # Compute mean values and their errors for the (new) x and y axis
        pT_Center  = Histo_Search_z_pT_2D.GetMean(1)
        pT_Error   = Histo_Search_z_pT_2D.GetMeanError(1)
        z_Center   = Histo_Search_z_pT_2D.GetMean(2)
        z_Error    = Histo_Search_z_pT_2D.GetMeanError(2)
        z_bin_min  = z_Center  - z_Error
        z_bin_max  = z_Center  + z_Error
        pT_bin_min = pT_Center - pT_Error
        pT_bin_max = pT_Center + pT_Error
        if(str(z_pT_Bin_Find) not in ["All", "0"]):
            #####==========#####   Finding the Standard Q2-y Bin Information   #####==========#####
            if("y_bin" in Binning_Method_Input):
                Borders_Q2_y = Q2_y_Border_Lines(Q2_y_Bin_Find)
                Q2_bin_max   = Borders_Q2_y[0][1][1]
                Q2_bin_min   = Borders_Q2_y[0][0][1]
                y_bin_max    = Borders_Q2_y[1][1][0]
                y_bin_min    = Borders_Q2_y[1][0][0]
            else:
                Borders_Q2_y = Q2_Y_Border_Lines(Q2_y_Bin_Find)
                Q2_bin_max, Q2_bin_min, y_bin_max, y_bin_min = Q2_Y_Border_Lines(Q2_y_Bin_Find)
            Q2_Center = (Q2_bin_max + Q2_bin_min)/2
            y_Center  = (y_bin_max  + y_bin_min)/2
            #####==========#####    Found the Standard Q2-y Bin Information    #####==========#####
        else:
            # Not using for individual z-pT bins for more consistent values of Q2 and y (don't want them to change when plotting the fit parameters vs z/pT - may change my mind about this in the future maybe)
            y_Center   = Histo_Search_Q2_y.GetMean(1)
            y_Error    = Histo_Search_Q2_y.GetMeanError(1)
            Q2_Center  = Histo_Search_Q2_y.GetMean(2)
            Q2_Error   = Histo_Search_Q2_y.GetMeanError(2)
            Q2_bin_min = Q2_Center - Q2_Error
            Q2_bin_max = Q2_Center + Q2_Error
            y_bin_min  = y_Center  - y_Error
            y_bin_max  = y_Center  + y_Error
            
        # Return order goes as [[Q2_bin_info, y_bin_info], [z_bin_info, pT_bin_info]]
            # Order of bin_info goes as: bin_info = [min_bin, center_bin, max_bin]
        return [[[Q2_bin_min, Q2_Center, Q2_bin_max], [y_bin_min, y_Center, y_bin_max]], [[z_bin_min, z_Center, z_bin_max], [pT_bin_min, pT_Center, pT_bin_max]]]
        
#####################################################################################################################################################################
##==========##==========##     Function for Finding Kinematic Binning Info     ##==========##==========##==========##==========##==========##==========##==========##
#####################################################################################################################################################################








######################################################################################################################################################
##==========##==========##     Canvas Functions     ##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################
def Canvas_Create(Name, Num_Columns=1, Num_Rows=1, Size_X=600, Size_Y=800, cd_Space=0):
    canvas_test = ROOT.TCanvas(str(Name), str(Name), Size_X, Size_Y)
    canvas_test.Divide(Num_Columns, Num_Rows, cd_Space, cd_Space)
    canvas_test.SetGrid()
    ROOT.gStyle.SetAxisColor(16, 'xy')
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(1)
    return canvas_test


##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Draw_Canvas(canvas, cd_num, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1):
    canvas.cd(cd_num)
    try:
        canvas.cd(cd_num).SetLeftMargin(left_add)
        canvas.cd(cd_num).SetRightMargin(right_add)
        canvas.cd(cd_num).SetTopMargin(up_add)
        canvas.cd(cd_num).SetBottomMargin(down_add)
    # except:
    #     print("".join([color.Error, "ERROR:\n", color.END_R, str(traceback.format_exc()), color.END]))
    except Exception as e:
        print("".join([color.Error, "Draw_Canvas(...) ERROR: ", color.LIGHT, str(e), color.END]))
        print("".join(["canvas: ", str(canvas.GetName()), "\ncd_num: ", str(cd_num)]))


def palette_move(canvas, histo, x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1):
    canvas.Modified()
    canvas.Update()
    palette_test = 0
    while(palette_test < 4 and palette_test != -1):
        try:
            palette_histo = histo.GetListOfFunctions().FindObject("palette")

            palette_histo.SetX1NDC(x_left)
            palette_histo.SetX2NDC(x_right)
            palette_histo.SetY1NDC(y_down)
            palette_histo.SetY2NDC(y_up)

            canvas.Modified()
            canvas.Update()
            palette_test = -1
        except:
            palette_test += 1
    if(palette_test > 0):
            print("\nFailed to move palette...")
            
            
def configure_stat_box(hist, show_entries=True, canvas=False):
    ## Configure the stat box for a given histogram.
    ## Parameters:
    ##     - hist: The histogram to configure the stat box for.
    ##     - show_entries: A boolean flag to show or hide the number of entries.
    ## Assuming the default stat box is desired to be shown
    if(show_entries):
        hist.SetStats(1)  # Show the stat box
        # This sets what is shown in the stat box; "i" for entries
        ROOT.gStyle.SetOptStat("i")
        # If there's a need to adjust the position for this specific histogram, it can be done via the histogram's TPaveStats
        stats = hist.GetListOfFunctions().FindObject("stats")
        if(stats):
            stats.SetX1NDC(0)  # New X start position
            stats.SetX2NDC(0)  # New X end position
            stats.SetY1NDC(0)  # New Y start position
            stats.SetY2NDC(0)  # New Y end position
#             stats.SetX1NDC(0.7)  # New X start position
#             stats.SetX2NDC(0.9)  # New X end position
#             stats.SetY1NDC(0.7)  # New Y start position
#             stats.SetY2NDC(0.9)  # New Y end position
#             stats.SetX1NDC(0.35)  # New X start position
#             stats.SetX2NDC(0.75)  # New X end position
#             stats.SetY1NDC(0.25)  # New Y start position
#             stats.SetY2NDC(0.45)  # New Y end position
        else:
            print(f"{color.Error}Error in configure_stat_box...{color.END}\n\tstats = {stats}")
    # else:
    #     hist.SetStats(0)  # Hide the stat box
    if(canvas):
        canvas.Modified()
        canvas.Update()
            
            
def get_chisquare(hist):
    func_iter = hist.GetListOfFunctions().MakeIterator()
    fit_function = func_iter.Next()
    while(fit_function and not isinstance(fit_function, ROOT.TF1)):
        fit_function = func_iter.Next()
    if(fit_function):
        return fit_function.GetChisquare()
    else:
        return None


def get_fit_parameters_B_and_C(hist):
    func_iter = hist.GetListOfFunctions().MakeIterator()
    fit_function = func_iter.Next()
    while(fit_function and (not isinstance(fit_function, ROOT.TF1))):
        fit_function = func_iter.Next()
    if(fit_function):
        paramB = fit_function.GetParameter(1)
        paramC = fit_function.GetParameter(2)
        paramB_error = fit_function.GetParError(1)
        paramC_error = fit_function.GetParError(2)
        return paramB, paramB_error, paramC, paramC_error
    else:
        return None, None, None, None



def draw_preliminary_text(pad_or_canvas, x_pos=0.15, y_pos=0.12, text="PRELIMINARY", text_size=0.06, text_color_alpha=(ROOT.kRed, 0.2)):
    # Draws a TLatex text box on a specified ROOT TCanvas or TPad at the given normalized coordinates.
    # Parameters:
    # pad_or_canvas (ROOT.TPad or ROOT.TCanvas): The TPad or TCanvas to draw the text on.
    # x_pos (float): X position of the text box in normalized device coordinates (0 to 1).
    # y_pos (float): Y position of the text box in normalized device coordinates (0 to 1).
    # text (str): The text to display.
    # text_size (float): Size of the text (0.06 is a typical value for good visibility).
    # text_color_alpha (tuple): Tuple containing the color and alpha (transparency) of the text.
    # Returns:
    # ROOT.TLatex: The TLatex object used for drawing the text (do not need to save).
    
    # Make the specified pad or canvas the current one to ensure correct drawing
    pad_or_canvas.cd()

    # Create a new TLatex object for drawing text
    latex = ROOT.TLatex()

    # Set the text size and color with alpha transparency
    latex.SetTextSize(text_size)
    color, alpha = text_color_alpha
    latex.SetTextColorAlpha(color, alpha)

    # Draw the text at the specified position using normalized device coordinates (NDC)
    latex.DrawTextNDC(x_pos, y_pos, text)

    # Return the TLatex object so that it remains associated with the pad/canvas
    return latex
    
            
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def statbox_move(Histogram, Canvas, Default_Stat_Obj="", Y1_add=0.05, Y2_add=0.25, X1_add=0.05, X2_add=0.35, Print_Method="norm"):
    finding, search = 0, 0
    while(finding == 0 and search < 5):
        if(Default_Stat_Obj == ""):
            Default_Stat_Obj = Histogram.GetListOfFunctions().FindObject("stats")

        if("TPaveStats" not in str(type(Default_Stat_Obj))):
            try:
                Default_Stat_Obj = Histogram.GetListOfFunctions().FindObject("stats")# Default_Stat_Obj.FindObject("stats")
            except Exception as e:
                print("".join([color.RED, "statbox_move(...) ERROR:", str(e), "\nTRACEBACK:\n", color.END, str(traceback.format_exc())]))
        try:
            if(Print_Method == "norm"):
                Default_Stat_Obj.SetY1NDC(Y1_add)
                Default_Stat_Obj.SetY2NDC(Y2_add)
                Default_Stat_Obj.SetX1NDC(X1_add)
                Default_Stat_Obj.SetX2NDC(X2_add)
            if(Print_Method in ["off", "Off"]):
                Default_Stat_Obj.SetY1NDC(0)
                Default_Stat_Obj.SetY2NDC(0)
                Default_Stat_Obj.SetX1NDC(0)
                Default_Stat_Obj.SetX2NDC(0)
            Default_Stat_Obj.Draw("same")
            Canvas.Modified()
            Canvas.Update()
            finding += 1
        except:
            Canvas.Modified()
            Canvas.Update()
            finding = 0
            search += 1
    # if(search > 4):
    #     print(f"{color.RED}\nFailed search\n{color.END}")

        
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def print_rounded_str(number, rounding=0):
    try:
        if(rounding != 0 and abs(number) >= 0.001):
            output = round(number, rounding)
            output = "".join(["{:.", str(rounding), "}"]).format(number)
            # print("round")
        elif(rounding != 0):
            output = "".join(["{:.", str(rounding-1), "e}"]).format(number)
            # print("science")
        else:
            # print("other")
            output = number
        return output
    except Exception as e:
        print("".join([color.Error, "print_rounded_str(...) ERROR: number = ", str(output), " is not accepted", " --> failed to round input..." if(rounding != 0) else "", "\nERROR Output Is: \n", str(e), color.END]))
        print("".join([color.RED, "TRACEBACK:\n", color.END, str(traceback.format_exc())]))
        return number
    
    
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Error_Propagation(Type_of_Prop, Error1, Error2=0, Number1=0, Number2=0, Result=False):
    Error = False
    try:
        if("ave" in Type_of_Prop or "Ave" in Type_of_Prop or "average" in Type_of_Prop or "Average" in Type_of_Prop):
            # Average of given numbers
            if(type(Error1) is list):
                for x in Error1:
                    Error += (x - np.average(Error1))**2
                Error /= (len(Error1) - 1)
                Error *= 1/2
            else:
                ave = (Error1 + Error2)/2
                Error = ((Error1 - ave)**2 + (Error2 - ave)**2)**0.5
                
        if("add" in Type_of_Prop or "Add" in Type_of_Prop or "subtract" in Type_of_Prop or "Subtract" in Type_of_Prop or "sub" in Type_of_Prop or "Sub" in Type_of_Prop):
            # Addition or Subtraction
            Error = ((Error1)**2 + (Error2)**2)**0.5
            
        if("mult" in Type_of_Prop or "Mult" in Type_of_Prop or "multiply" in Type_of_Prop or "Multiply" in Type_of_Prop):
            # Multiplication
            if(not Result):
                Error = (Number1*Number2)*((Error1/Number1)**2 + (Error2/Number2)**2)**0.5
            else:
                Error = Result*((Error1/Number1)**2 + (Error2/Number2)**2)**0.5
            
        if("div" in Type_of_Prop or "Div" in Type_of_Prop or "divide" in Type_of_Prop or "Divide" in Type_of_Prop):
            # Division
            if(not Result):
                Error = (Number1/Number2)*((Error1/Number1)**2 + (Error2/Number2)**2)**0.5
            else:
                Error = Result*((Error1/Number1)**2 + (Error2/Number2)**2)**0.5
        
        if(not Error):
            print("ERROR: error not calculated... (See option selection for 'Type_of_Prop')")
        else:
            return Error
    except Exception as e:
        print("".join([color.RED, "Error taking Error Propagation with inputs:\n", color.END, "Type_of_Prop = ", str(Type_of_Prop), ", Error1 = ", str(Error1), ", Error2 = ", str(Error2), ", Number1 = ", str(Number1), ", Number2 = ", str(Number2), "".join([", Result = ", str(Result)]) if(not Result) else ""]))
        print("Error is: \n\t" + str(e))
        print("".join([color.RED, "TRACEBACK:\n", color.END, str(traceback.format_exc())]))
        
        
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


def Get_Max_Y_Histo_1D(Histo_List, Norm_Q="Default"):
    try:
        if(type(Histo_List) is not list):
            Histo_List = [Histo_List]
        Max_Y = 0
        for Histo in Histo_List:
            if(type(Histo) is not bool and type(Histo) is not str):
                # print("".join([color.BBLUE, "\n'", str(Histo.GetName()), "' Maximum = ", str(Histo.GetBinContent(Histo.GetMaximumBin())), " Total = ", str(Histo.Integral()), color.END]))
                if(Histo.Integral() != 0 and Histo.GetBinContent(Histo.GetMaximumBin()) != 0):
                    Test_Y = (Histo.GetBinContent(Histo.GetMaximumBin())) if((Norm_Q not in ["Normalized", "Norm"]) or (Norm_Q == "Default")) else ((Histo.GetBinContent(Histo.GetMaximumBin()))/(Histo.Integral()))
                else:
                    Test_Y = 0
                    print("".join([color.Error, "\n EMPTY HISTOGRAM: '", str(Histo.GetName()), "'\n\tMaximum = ", str(Histo.GetBinContent(Histo.GetMaximumBin())), "\n\tTotal = ", str(Histo.Integral()), color.END]))
                    print(Histo_List)
                    print(Histo)
                    for Histo2 in Histo_List:
                        print("".join([color.BBLUE if(Histo2 == Histo) else "\n", str(Histo2), color.END if(Histo2 == Histo) else "\n"]))
                if(Test_Y > Max_Y):
                    Max_Y = Test_Y   
        return Max_Y
    except:
        print("".join([color.Error, "\nERROR IN GETTING THE MAX Y OF THE 1D HISTOGRAMS...", color.END]))
        print("".join([color.Error, "ERROR:\n", color.END, str(traceback.format_exc())]))
        print(Histo_List)
        return "ERROR"
    
    
######################################################################################################################################################
##==========##==========##     Canvas Functions     ##==========##==========##==========##==========##==========##==========##==========##==========##
######################################################################################################################################################




def skip_condition_z_pT_bins(Q2_Y_BIN, Z_PT_BIN, BINNING_METHOD="_y_bin"):
    if("Y_bin" not in BINNING_METHOD):
        skip_condition_y_bins_return = (Q2_Y_BIN in [1]) and (Z_PT_BIN in [28, 34, 35])
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [2])          and (Z_PT_BIN in [28, 35, 41, 42])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [3])          and (Z_PT_BIN in [28, 35])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [4])          and (Z_PT_BIN in [6,  36])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [5])          and (Z_PT_BIN in [30, 36])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [6])          and (Z_PT_BIN in [30])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [7])          and (Z_PT_BIN in [24, 30])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [9])          and (Z_PT_BIN in [36])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [10])         and (Z_PT_BIN in [30, 36])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [11])         and (Z_PT_BIN in [24, 30])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [13, 14])     and (Z_PT_BIN in [25])))
        skip_condition_y_bins_return = skip_condition_y_bins_return or  (((Q2_Y_BIN in [15, 16, 17]) and (Z_PT_BIN in [20])))
        return skip_condition_y_bins_return
    elif("Y_bin" in BINNING_METHOD):
        skip_condition_Y_bins_return = (Z_PT_BIN in Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_BIN)[2])
        return skip_condition_Y_bins_return
    else:
        return False

        
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##


import re
def Find_Bins_From_Histo_Name(data_string):
    # Regular expression to extract NumBins, MinBin, and MaxBin
    pattern = r"NumBins=(\d+),\s*MinBin=([-+]?\d*\.?\d+),\s*MaxBin=([-+]?\d*\.?\d+)"

    # Search the string using the regular expression
    match = re.search(pattern, data_string)
    num_bins =   int(match.group(1)) if(match) else "Error"
    min_bin  = float(match.group(2)) if(match) else "Error"
    max_bin  = float(match.group(3)) if(match) else "Error"
    if(not match):
        print(f"{color.Error}No matching data found.{color.END}")
    # else:
    #     print(f"NumBins: {num_bins}, MinBin: {min_bin}, MaxBin: {max_bin}")
    
    return [num_bins, min_bin, max_bin]