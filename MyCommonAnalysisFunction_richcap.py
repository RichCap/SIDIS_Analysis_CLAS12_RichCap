import ROOT

# Binning_Method = "_Y_bin"
Binning_Method = "_y_bin"
# Binning_Method = "_2"


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
    ERROR     = '\033[91m\033[1m' # Combines RED and BOLD
    Error     = '\033[91m\033[1m' # Same as ERROR
    
    
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

def Draw_Q2_Y_Bins(Input_Bin, line_width=3, Binning_Method_Input=Binning_Method):
    if("y_bin" in Binning_Method_Input):
        Borders_Q2_y = Q2_y_Border_Lines(Input_Bin)
        Q2_Max       = Borders_Q2_y[0][1][1]
        Q2_Min       = Borders_Q2_y[0][0][1]
        y_Max        = Borders_Q2_y[1][1][0]
        y_Min        = Borders_Q2_y[1][0][0]
    else:
        Q2_Max, Q2_Min, y_Max, y_Min = Q2_Y_Border_Lines(Input_Bin)
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

# Bin_Definition_Array = {'Q2-y=1, z-pT=1': [0.2, 0.16, 0.2, 0.05], 'Q2-y=1, z-pT=2': [0.2, 0.16, 0.3, 0.2], 'Q2-y=1, z-pT=3': [0.2, 0.16, 0.4, 0.3], 'Q2-y=1, z-pT=4': [0.2, 0.16, 0.5, 0.4], 'Q2-y=1, z-pT=58 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.6, 0.5], 'Q2-y=1, z-pT=59 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.75, 0.6], 'Q2-y=1, z-pT=60 - REMOVE, MIGRATION BIN': [0.2, 0.16, 1.0, 0.75], 'Q2-y=1, z-pT=5': [0.24, 0.2, 0.2, 0.05], 'Q2-y=1, z-pT=6': [0.24, 0.2, 0.3, 0.2], 'Q2-y=1, z-pT=7': [0.24, 0.2, 0.4, 0.3], 'Q2-y=1, z-pT=8': [0.24, 0.2, 0.5, 0.4], 'Q2-y=1, z-pT=9': [0.24, 0.2, 0.6, 0.5], 'Q2-y=1, z-pT=61 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.75, 0.6], 'Q2-y=1, z-pT=62 - REMOVE, MIGRATION BIN': [0.24, 0.2, 1.0, 0.75], 'Q2-y=1, z-pT=10': [0.31, 0.24, 0.2, 0.05], 'Q2-y=1, z-pT=11': [0.31, 0.24, 0.3, 0.2], 'Q2-y=1, z-pT=12': [0.31, 0.24, 0.4, 0.3], 'Q2-y=1, z-pT=13': [0.31, 0.24, 0.5, 0.4], 'Q2-y=1, z-pT=14': [0.31, 0.24, 0.6, 0.5], 'Q2-y=1, z-pT=15': [0.31, 0.24, 0.75, 0.6], 'Q2-y=1, z-pT=63 - REMOVE, MIGRATION BIN': [0.31, 0.24, 1.0, 0.75], 'Q2-y=1, z-pT=16': [0.41, 0.31, 0.2, 0.05], 'Q2-y=1, z-pT=17': [0.41, 0.31, 0.3, 0.2], 'Q2-y=1, z-pT=18': [0.41, 0.31, 0.4, 0.3], 'Q2-y=1, z-pT=19': [0.41, 0.31, 0.5, 0.4], 'Q2-y=1, z-pT=20': [0.41, 0.31, 0.6, 0.5], 'Q2-y=1, z-pT=21': [0.41, 0.31, 0.75, 0.6], 'Q2-y=1, z-pT=22': [0.41, 0.31, 1.0, 0.75], 'Q2-y=1, z-pT=23': [0.7, 0.41, 0.2, 0.05], 'Q2-y=1, z-pT=24': [0.7, 0.41, 0.3, 0.2], 'Q2-y=1, z-pT=25': [0.7, 0.41, 0.4, 0.3], 'Q2-y=1, z-pT=26': [0.7, 0.41, 0.5, 0.4], 'Q2-y=1, z-pT=27': [0.7, 0.41, 0.6, 0.5], 'Q2-y=1, z-pT=28': [0.7, 0.41, 0.75, 0.6], 'Q2-y=1, z-pT=29': [0.7, 0.41, 1.0, 0.75], 'Q2-y=1, z-pT=30, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=1, z-pT=31, MIGRATION BIN': [0.16, 0, 0.05, 0.2], 'Q2-y=1, z-pT=32, MIGRATION BIN': [0.16, 0, 0.2, 0.3], 'Q2-y=1, z-pT=33, MIGRATION BIN': [0.16, 0, 0.3, 0.4], 'Q2-y=1, z-pT=34, MIGRATION BIN': [0.16, 0, 0.4, 0.5], 'Q2-y=1, z-pT=35, MIGRATION BIN': [0.16, 0, 0.5, 0.6], 'Q2-y=1, z-pT=36, MIGRATION BIN': [0.16, 0, 0.6, 0.75], 'Q2-y=1, z-pT=37, MIGRATION BIN': [0.16, 0, 0.75, 1.0], 'Q2-y=1, z-pT=38, MIGRATION BIN': [0.16, 0, 10, 1.0], 'Q2-y=1, z-pT=39, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=1, z-pT=40, MIGRATION BIN': [0.16, 0.2, 10, 1.0], 'Q2-y=1, z-pT=41, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=1, z-pT=42, MIGRATION BIN': [0.2, 0.24, 10, 1.0], 'Q2-y=1, z-pT=43, MIGRATION BIN': [0.24, 0.31, 0.05, 0], 'Q2-y=1, z-pT=44, MIGRATION BIN': [0.24, 0.31, 10, 1.0], 'Q2-y=1, z-pT=45, MIGRATION BIN': [0.31, 0.41, 0.05, 0], 'Q2-y=1, z-pT=46, MIGRATION BIN': [0.31, 0.41, 10, 1.0], 'Q2-y=1, z-pT=47, MIGRATION BIN': [0.41, 0.7, 0.05, 0], 'Q2-y=1, z-pT=48, MIGRATION BIN': [0.41, 0.7, 10, 1.0], 'Q2-y=1, z-pT=49, MIGRATION BIN': [10, 0.7, 0, 0.05], 'Q2-y=1, z-pT=50, MIGRATION BIN': [10, 0.7, 0.05, 0.2], 'Q2-y=1, z-pT=51, MIGRATION BIN': [10, 0.7, 0.2, 0.3], 'Q2-y=1, z-pT=52, MIGRATION BIN': [10, 0.7, 0.3, 0.4], 'Q2-y=1, z-pT=53, MIGRATION BIN': [10, 0.7, 0.4, 0.5], 'Q2-y=1, z-pT=54, MIGRATION BIN': [10, 0.7, 0.5, 0.6], 'Q2-y=1, z-pT=55, MIGRATION BIN': [10, 0.7, 0.6, 0.75], 'Q2-y=1, z-pT=56, MIGRATION BIN': [10, 0.7, 0.75, 1.0], 'Q2-y=1, z-pT=57, MIGRATION BIN': [10, 0.7, 10, 1.0], 'Q2-y=2, z-pT=1': [0.23, 0.19, 0.25, 0.05], 'Q2-y=2, z-pT=2': [0.23, 0.19, 0.35, 0.25], 'Q2-y=2, z-pT=3': [0.23, 0.19, 0.45, 0.35], 'Q2-y=2, z-pT=4': [0.23, 0.19, 0.54, 0.45], 'Q2-y=2, z-pT=60 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.67, 0.54], 'Q2-y=2, z-pT=61 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.93, 0.67], 'Q2-y=2, z-pT=5': [0.26, 0.23, 0.25, 0.05], 'Q2-y=2, z-pT=6': [0.26, 0.23, 0.35, 0.25], 'Q2-y=2, z-pT=7': [0.26, 0.23, 0.45, 0.35], 'Q2-y=2, z-pT=8': [0.26, 0.23, 0.54, 0.45], 'Q2-y=2, z-pT=9': [0.26, 0.23, 0.67, 0.54], 'Q2-y=2, z-pT=62 - REMOVE, MIGRATION BIN': [0.26, 0.23, 0.93, 0.67], 'Q2-y=2, z-pT=10': [0.31, 0.26, 0.25, 0.05], 'Q2-y=2, z-pT=11': [0.31, 0.26, 0.35, 0.25], 'Q2-y=2, z-pT=12': [0.31, 0.26, 0.45, 0.35], 'Q2-y=2, z-pT=13': [0.31, 0.26, 0.54, 0.45], 'Q2-y=2, z-pT=14': [0.31, 0.26, 0.67, 0.54], 'Q2-y=2, z-pT=63 - REMOVE, MIGRATION BIN': [0.31, 0.26, 0.93, 0.67], 'Q2-y=2, z-pT=15': [0.38, 0.31, 0.25, 0.05], 'Q2-y=2, z-pT=16': [0.38, 0.31, 0.35, 0.25], 'Q2-y=2, z-pT=17': [0.38, 0.31, 0.45, 0.35], 'Q2-y=2, z-pT=18': [0.38, 0.31, 0.54, 0.45], 'Q2-y=2, z-pT=19': [0.38, 0.31, 0.67, 0.54], 'Q2-y=2, z-pT=20': [0.38, 0.31, 0.93, 0.67], 'Q2-y=2, z-pT=21': [0.5, 0.38, 0.25, 0.05], 'Q2-y=2, z-pT=22': [0.5, 0.38, 0.35, 0.25], 'Q2-y=2, z-pT=23': [0.5, 0.38, 0.45, 0.35], 'Q2-y=2, z-pT=24': [0.5, 0.38, 0.54, 0.45], 'Q2-y=2, z-pT=25': [0.5, 0.38, 0.67, 0.54], 'Q2-y=2, z-pT=26': [0.5, 0.38, 0.93, 0.67], 'Q2-y=2, z-pT=27': [0.75, 0.5, 0.25, 0.05], 'Q2-y=2, z-pT=28': [0.75, 0.5, 0.35, 0.25], 'Q2-y=2, z-pT=29': [0.75, 0.5, 0.45, 0.35], 'Q2-y=2, z-pT=30': [0.75, 0.5, 0.54, 0.45], 'Q2-y=2, z-pT=31': [0.75, 0.5, 0.67, 0.54], 'Q2-y=2, z-pT=64 - REMOVE, MIGRATION BIN': [0.75, 0.5, 0.93, 0.67], 'Q2-y=2, z-pT=32, MIGRATION BIN': [0.19, 0, 0.05, 0], 'Q2-y=2, z-pT=33, MIGRATION BIN': [0.19, 0, 0.05, 0.25], 'Q2-y=2, z-pT=34, MIGRATION BIN': [0.19, 0, 0.25, 0.35], 'Q2-y=2, z-pT=35, MIGRATION BIN': [0.19, 0, 0.35, 0.45], 'Q2-y=2, z-pT=36, MIGRATION BIN': [0.19, 0, 0.45, 0.54], 'Q2-y=2, z-pT=37, MIGRATION BIN': [0.19, 0, 0.54, 0.67], 'Q2-y=2, z-pT=38, MIGRATION BIN': [0.19, 0, 0.67, 0.93], 'Q2-y=2, z-pT=39, MIGRATION BIN': [0.19, 0, 10, 0.93], 'Q2-y=2, z-pT=40, MIGRATION BIN': [0.19, 0.23, 0.05, 0], 'Q2-y=2, z-pT=41, MIGRATION BIN': [0.19, 0.23, 10, 0.93], 'Q2-y=2, z-pT=42, MIGRATION BIN': [0.23, 0.26, 0.05, 0], 'Q2-y=2, z-pT=43, MIGRATION BIN': [0.23, 0.26, 10, 0.93], 'Q2-y=2, z-pT=44, MIGRATION BIN': [0.26, 0.31, 0.05, 0], 'Q2-y=2, z-pT=45, MIGRATION BIN': [0.26, 0.31, 10, 0.93], 'Q2-y=2, z-pT=46, MIGRATION BIN': [0.31, 0.38, 0.05, 0], 'Q2-y=2, z-pT=47, MIGRATION BIN': [0.31, 0.38, 10, 0.93], 'Q2-y=2, z-pT=48, MIGRATION BIN': [0.38, 0.5, 0.05, 0], 'Q2-y=2, z-pT=49, MIGRATION BIN': [0.38, 0.5, 10, 0.93], 'Q2-y=2, z-pT=50, MIGRATION BIN': [0.5, 0.75, 0.05, 0], 'Q2-y=2, z-pT=51, MIGRATION BIN': [0.5, 0.75, 10, 0.93], 'Q2-y=2, z-pT=52, MIGRATION BIN': [10, 0.75, 0, 0.05], 'Q2-y=2, z-pT=53, MIGRATION BIN': [10, 0.75, 0.05, 0.25], 'Q2-y=2, z-pT=54, MIGRATION BIN': [10, 0.75, 0.25, 0.35], 'Q2-y=2, z-pT=55, MIGRATION BIN': [10, 0.75, 0.35, 0.45], 'Q2-y=2, z-pT=56, MIGRATION BIN': [10, 0.75, 0.45, 0.54], 'Q2-y=2, z-pT=57, MIGRATION BIN': [10, 0.75, 0.54, 0.67], 'Q2-y=2, z-pT=58, MIGRATION BIN': [10, 0.75, 0.67, 0.93], 'Q2-y=2, z-pT=59, MIGRATION BIN': [10, 0.75, 10, 0.93], 'Q2-y=3, z-pT=1': [0.28, 0.22, 0.2, 0.05], 'Q2-y=3, z-pT=2': [0.28, 0.22, 0.3, 0.2], 'Q2-y=3, z-pT=3': [0.28, 0.22, 0.4, 0.3], 'Q2-y=3, z-pT=4': [0.28, 0.22, 0.5, 0.4], 'Q2-y=3, z-pT=5': [0.28, 0.22, 0.6, 0.5], 'Q2-y=3, z-pT=47 - REMOVE, MIGRATION BIN': [0.28, 0.22, 0.75, 0.6], 'Q2-y=3, z-pT=6': [0.35, 0.28, 0.2, 0.05], 'Q2-y=3, z-pT=7': [0.35, 0.28, 0.3, 0.2], 'Q2-y=3, z-pT=8': [0.35, 0.28, 0.4, 0.3], 'Q2-y=3, z-pT=9': [0.35, 0.28, 0.5, 0.4], 'Q2-y=3, z-pT=10': [0.35, 0.28, 0.6, 0.5], 'Q2-y=3, z-pT=11': [0.35, 0.28, 0.75, 0.6], 'Q2-y=3, z-pT=12': [0.45, 0.35, 0.2, 0.05], 'Q2-y=3, z-pT=13': [0.45, 0.35, 0.3, 0.2], 'Q2-y=3, z-pT=14': [0.45, 0.35, 0.4, 0.3], 'Q2-y=3, z-pT=15': [0.45, 0.35, 0.5, 0.4], 'Q2-y=3, z-pT=16': [0.45, 0.35, 0.6, 0.5], 'Q2-y=3, z-pT=17': [0.45, 0.35, 0.75, 0.6], 'Q2-y=3, z-pT=18': [0.7, 0.45, 0.2, 0.05], 'Q2-y=3, z-pT=19': [0.7, 0.45, 0.3, 0.2], 'Q2-y=3, z-pT=20': [0.7, 0.45, 0.4, 0.3], 'Q2-y=3, z-pT=21': [0.7, 0.45, 0.5, 0.4], 'Q2-y=3, z-pT=22': [0.7, 0.45, 0.6, 0.5], 'Q2-y=3, z-pT=48 - REMOVE, MIGRATION BIN': [0.7, 0.45, 0.75, 0.6], 'Q2-y=3, z-pT=23, MIGRATION BIN': [0.22, 0, 0.05, 0], 'Q2-y=3, z-pT=24, MIGRATION BIN': [0.22, 0, 0.05, 0.2], 'Q2-y=3, z-pT=25, MIGRATION BIN': [0.22, 0, 0.2, 0.3], 'Q2-y=3, z-pT=26, MIGRATION BIN': [0.22, 0, 0.3, 0.4], 'Q2-y=3, z-pT=27, MIGRATION BIN': [0.22, 0, 0.4, 0.5], 'Q2-y=3, z-pT=28, MIGRATION BIN': [0.22, 0, 0.5, 0.6], 'Q2-y=3, z-pT=29, MIGRATION BIN': [0.22, 0, 0.6, 0.75], 'Q2-y=3, z-pT=30, MIGRATION BIN': [0.22, 0, 10, 0.75], 'Q2-y=3, z-pT=31, MIGRATION BIN': [0.22, 0.28, 0.05, 0], 'Q2-y=3, z-pT=32, MIGRATION BIN': [0.22, 0.28, 10, 0.75], 'Q2-y=3, z-pT=33, MIGRATION BIN': [0.28, 0.35, 0.05, 0], 'Q2-y=3, z-pT=34, MIGRATION BIN': [0.28, 0.35, 10, 0.75], 'Q2-y=3, z-pT=35, MIGRATION BIN': [0.35, 0.45, 0.05, 0], 'Q2-y=3, z-pT=36, MIGRATION BIN': [0.35, 0.45, 10, 0.75], 'Q2-y=3, z-pT=37, MIGRATION BIN': [0.45, 0.7, 0.05, 0], 'Q2-y=3, z-pT=38, MIGRATION BIN': [0.45, 0.7, 10, 0.75], 'Q2-y=3, z-pT=39, MIGRATION BIN': [10, 0.7, 0, 0.05], 'Q2-y=3, z-pT=40, MIGRATION BIN': [10, 0.7, 0.05, 0.2], 'Q2-y=3, z-pT=41, MIGRATION BIN': [10, 0.7, 0.2, 0.3], 'Q2-y=3, z-pT=42, MIGRATION BIN': [10, 0.7, 0.3, 0.4], 'Q2-y=3, z-pT=43, MIGRATION BIN': [10, 0.7, 0.4, 0.5], 'Q2-y=3, z-pT=44, MIGRATION BIN': [10, 0.7, 0.5, 0.6], 'Q2-y=3, z-pT=45, MIGRATION BIN': [10, 0.7, 0.6, 0.75], 'Q2-y=3, z-pT=46, MIGRATION BIN': [10, 0.7, 10, 0.75], 'Q2-y=4, z-pT=1': [0.34, 0.26, 0.2, 0.05], 'Q2-y=4, z-pT=2': [0.34, 0.26, 0.29, 0.2], 'Q2-y=4, z-pT=3': [0.34, 0.26, 0.38, 0.29], 'Q2-y=4, z-pT=4': [0.34, 0.26, 0.48, 0.38], 'Q2-y=4, z-pT=5': [0.34, 0.26, 0.61, 0.48], 'Q2-y=4, z-pT=6': [0.38, 0.34, 0.2, 0.05], 'Q2-y=4, z-pT=7': [0.38, 0.34, 0.29, 0.2], 'Q2-y=4, z-pT=8': [0.38, 0.34, 0.38, 0.29], 'Q2-y=4, z-pT=9': [0.38, 0.34, 0.48, 0.38], 'Q2-y=4, z-pT=10': [0.38, 0.34, 0.61, 0.48], 'Q2-y=4, z-pT=11': [0.43, 0.38, 0.2, 0.05], 'Q2-y=4, z-pT=12': [0.43, 0.38, 0.29, 0.2], 'Q2-y=4, z-pT=13': [0.43, 0.38, 0.38, 0.29], 'Q2-y=4, z-pT=14': [0.43, 0.38, 0.48, 0.38], 'Q2-y=4, z-pT=15': [0.43, 0.38, 0.61, 0.48], 'Q2-y=4, z-pT=16': [0.5, 0.43, 0.2, 0.05], 'Q2-y=4, z-pT=17': [0.5, 0.43, 0.29, 0.2], 'Q2-y=4, z-pT=18': [0.5, 0.43, 0.38, 0.29], 'Q2-y=4, z-pT=19': [0.5, 0.43, 0.48, 0.38], 'Q2-y=4, z-pT=20': [0.5, 0.43, 0.61, 0.48], 'Q2-y=4, z-pT=21': [0.6, 0.5, 0.2, 0.05], 'Q2-y=4, z-pT=22': [0.6, 0.5, 0.29, 0.2], 'Q2-y=4, z-pT=23': [0.6, 0.5, 0.38, 0.29], 'Q2-y=4, z-pT=24': [0.6, 0.5, 0.48, 0.38], 'Q2-y=4, z-pT=49 - REMOVE, MIGRATION BIN': [0.6, 0.5, 0.61, 0.48], 'Q2-y=4, z-pT=25, MIGRATION BIN': [0.26, 0, 0.05, 0], 'Q2-y=4, z-pT=26, MIGRATION BIN': [0.26, 0, 0.05, 0.2], 'Q2-y=4, z-pT=27, MIGRATION BIN': [0.26, 0, 0.2, 0.29], 'Q2-y=4, z-pT=28, MIGRATION BIN': [0.26, 0, 0.29, 0.38], 'Q2-y=4, z-pT=29, MIGRATION BIN': [0.26, 0, 0.38, 0.48], 'Q2-y=4, z-pT=30, MIGRATION BIN': [0.26, 0, 0.48, 0.61], 'Q2-y=4, z-pT=31, MIGRATION BIN': [0.26, 0, 10, 0.61], 'Q2-y=4, z-pT=32, MIGRATION BIN': [0.26, 0.34, 0.05, 0], 'Q2-y=4, z-pT=33, MIGRATION BIN': [0.26, 0.34, 10, 0.61], 'Q2-y=4, z-pT=34, MIGRATION BIN': [0.34, 0.38, 0.05, 0], 'Q2-y=4, z-pT=35, MIGRATION BIN': [0.34, 0.38, 10, 0.61], 'Q2-y=4, z-pT=36, MIGRATION BIN': [0.38, 0.43, 0.05, 0], 'Q2-y=4, z-pT=37, MIGRATION BIN': [0.38, 0.43, 10, 0.61], 'Q2-y=4, z-pT=38, MIGRATION BIN': [0.43, 0.5, 0.05, 0], 'Q2-y=4, z-pT=39, MIGRATION BIN': [0.43, 0.5, 10, 0.61], 'Q2-y=4, z-pT=40, MIGRATION BIN': [0.5, 0.6, 0.05, 0], 'Q2-y=4, z-pT=41, MIGRATION BIN': [0.5, 0.6, 10, 0.61], 'Q2-y=4, z-pT=42, MIGRATION BIN': [10, 0.6, 0, 0.05], 'Q2-y=4, z-pT=43, MIGRATION BIN': [10, 0.6, 0.05, 0.2], 'Q2-y=4, z-pT=44, MIGRATION BIN': [10, 0.6, 0.2, 0.29], 'Q2-y=4, z-pT=45, MIGRATION BIN': [10, 0.6, 0.29, 0.38], 'Q2-y=4, z-pT=46, MIGRATION BIN': [10, 0.6, 0.38, 0.48], 'Q2-y=4, z-pT=47, MIGRATION BIN': [10, 0.6, 0.48, 0.61], 'Q2-y=4, z-pT=48, MIGRATION BIN': [10, 0.6, 10, 0.61], 'Q2-y=5, z-pT=1': [0.2, 0.16, 0.22, 0.05], 'Q2-y=5, z-pT=2': [0.2, 0.16, 0.32, 0.22], 'Q2-y=5, z-pT=3': [0.2, 0.16, 0.41, 0.32], 'Q2-y=5, z-pT=4': [0.2, 0.16, 0.51, 0.41], 'Q2-y=5, z-pT=61 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.65, 0.51], 'Q2-y=5, z-pT=62 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.98, 0.65], 'Q2-y=5, z-pT=5': [0.24, 0.2, 0.22, 0.05], 'Q2-y=5, z-pT=6': [0.24, 0.2, 0.32, 0.22], 'Q2-y=5, z-pT=7': [0.24, 0.2, 0.41, 0.32], 'Q2-y=5, z-pT=8': [0.24, 0.2, 0.51, 0.41], 'Q2-y=5, z-pT=9': [0.24, 0.2, 0.65, 0.51], 'Q2-y=5, z-pT=63 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.98, 0.65], 'Q2-y=5, z-pT=10': [0.3, 0.24, 0.22, 0.05], 'Q2-y=5, z-pT=11': [0.3, 0.24, 0.32, 0.22], 'Q2-y=5, z-pT=12': [0.3, 0.24, 0.41, 0.32], 'Q2-y=5, z-pT=13': [0.3, 0.24, 0.51, 0.41], 'Q2-y=5, z-pT=14': [0.3, 0.24, 0.65, 0.51], 'Q2-y=5, z-pT=64 - REMOVE, MIGRATION BIN': [0.3, 0.24, 0.98, 0.65], 'Q2-y=5, z-pT=15': [0.38, 0.3, 0.22, 0.05], 'Q2-y=5, z-pT=16': [0.38, 0.3, 0.32, 0.22], 'Q2-y=5, z-pT=17': [0.38, 0.3, 0.41, 0.32], 'Q2-y=5, z-pT=18': [0.38, 0.3, 0.51, 0.41], 'Q2-y=5, z-pT=19': [0.38, 0.3, 0.65, 0.51], 'Q2-y=5, z-pT=20': [0.38, 0.3, 0.98, 0.65], 'Q2-y=5, z-pT=21': [0.49, 0.38, 0.22, 0.05], 'Q2-y=5, z-pT=22': [0.49, 0.38, 0.32, 0.22], 'Q2-y=5, z-pT=23': [0.49, 0.38, 0.41, 0.32], 'Q2-y=5, z-pT=24': [0.49, 0.38, 0.51, 0.41], 'Q2-y=5, z-pT=25': [0.49, 0.38, 0.65, 0.51], 'Q2-y=5, z-pT=26': [0.49, 0.38, 0.98, 0.65], 'Q2-y=5, z-pT=27': [0.72, 0.49, 0.22, 0.05], 'Q2-y=5, z-pT=28': [0.72, 0.49, 0.32, 0.22], 'Q2-y=5, z-pT=29': [0.72, 0.49, 0.41, 0.32], 'Q2-y=5, z-pT=30': [0.72, 0.49, 0.51, 0.41], 'Q2-y=5, z-pT=31': [0.72, 0.49, 0.65, 0.51], 'Q2-y=5, z-pT=32': [0.72, 0.49, 0.98, 0.65], 'Q2-y=5, z-pT=33, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=5, z-pT=34, MIGRATION BIN': [0.16, 0, 0.05, 0.22], 'Q2-y=5, z-pT=35, MIGRATION BIN': [0.16, 0, 0.22, 0.32], 'Q2-y=5, z-pT=36, MIGRATION BIN': [0.16, 0, 0.32, 0.41], 'Q2-y=5, z-pT=37, MIGRATION BIN': [0.16, 0, 0.41, 0.51], 'Q2-y=5, z-pT=38, MIGRATION BIN': [0.16, 0, 0.51, 0.65], 'Q2-y=5, z-pT=39, MIGRATION BIN': [0.16, 0, 0.65, 0.98], 'Q2-y=5, z-pT=40, MIGRATION BIN': [0.16, 0, 10, 0.98], 'Q2-y=5, z-pT=41, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=5, z-pT=42, MIGRATION BIN': [0.16, 0.2, 10, 0.98], 'Q2-y=5, z-pT=43, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=5, z-pT=44, MIGRATION BIN': [0.2, 0.24, 10, 0.98], 'Q2-y=5, z-pT=45, MIGRATION BIN': [0.24, 0.3, 0.05, 0], 'Q2-y=5, z-pT=46, MIGRATION BIN': [0.24, 0.3, 10, 0.98], 'Q2-y=5, z-pT=47, MIGRATION BIN': [0.3, 0.38, 0.05, 0], 'Q2-y=5, z-pT=48, MIGRATION BIN': [0.3, 0.38, 10, 0.98], 'Q2-y=5, z-pT=49, MIGRATION BIN': [0.38, 0.49, 0.05, 0], 'Q2-y=5, z-pT=50, MIGRATION BIN': [0.38, 0.49, 10, 0.98], 'Q2-y=5, z-pT=51, MIGRATION BIN': [0.49, 0.72, 0.05, 0], 'Q2-y=5, z-pT=52, MIGRATION BIN': [0.49, 0.72, 10, 0.98], 'Q2-y=5, z-pT=53, MIGRATION BIN': [10, 0.72, 0, 0.05], 'Q2-y=5, z-pT=54, MIGRATION BIN': [10, 0.72, 0.05, 0.22], 'Q2-y=5, z-pT=55, MIGRATION BIN': [10, 0.72, 0.22, 0.32], 'Q2-y=5, z-pT=56, MIGRATION BIN': [10, 0.72, 0.32, 0.41], 'Q2-y=5, z-pT=57, MIGRATION BIN': [10, 0.72, 0.41, 0.51], 'Q2-y=5, z-pT=58, MIGRATION BIN': [10, 0.72, 0.51, 0.65], 'Q2-y=5, z-pT=59, MIGRATION BIN': [10, 0.72, 0.65, 0.98], 'Q2-y=5, z-pT=60, MIGRATION BIN': [10, 0.72, 10, 0.98], 'Q2-y=6, z-pT=1': [0.23, 0.18, 0.22, 0.05], 'Q2-y=6, z-pT=2': [0.23, 0.18, 0.32, 0.22], 'Q2-y=6, z-pT=3': [0.23, 0.18, 0.41, 0.32], 'Q2-y=6, z-pT=4': [0.23, 0.18, 0.51, 0.41], 'Q2-y=6, z-pT=52 - REMOVE, MIGRATION BIN': [0.23, 0.18, 0.65, 0.51], 'Q2-y=6, z-pT=53 - REMOVE, MIGRATION BIN': [0.23, 0.18, 1.05, 0.65], 'Q2-y=6, z-pT=5': [0.28, 0.23, 0.22, 0.05], 'Q2-y=6, z-pT=6': [0.28, 0.23, 0.32, 0.22], 'Q2-y=6, z-pT=7': [0.28, 0.23, 0.41, 0.32], 'Q2-y=6, z-pT=8': [0.28, 0.23, 0.51, 0.41], 'Q2-y=6, z-pT=9': [0.28, 0.23, 0.65, 0.51], 'Q2-y=6, z-pT=54 - REMOVE, MIGRATION BIN': [0.28, 0.23, 1.05, 0.65], 'Q2-y=6, z-pT=10': [0.35, 0.28, 0.22, 0.05], 'Q2-y=6, z-pT=11': [0.35, 0.28, 0.32, 0.22], 'Q2-y=6, z-pT=12': [0.35, 0.28, 0.41, 0.32], 'Q2-y=6, z-pT=13': [0.35, 0.28, 0.51, 0.41], 'Q2-y=6, z-pT=14': [0.35, 0.28, 0.65, 0.51], 'Q2-y=6, z-pT=55 - REMOVE, MIGRATION BIN': [0.35, 0.28, 1.05, 0.65], 'Q2-y=6, z-pT=15': [0.45, 0.35, 0.22, 0.05], 'Q2-y=6, z-pT=16': [0.45, 0.35, 0.32, 0.22], 'Q2-y=6, z-pT=17': [0.45, 0.35, 0.41, 0.32], 'Q2-y=6, z-pT=18': [0.45, 0.35, 0.51, 0.41], 'Q2-y=6, z-pT=19': [0.45, 0.35, 0.65, 0.51], 'Q2-y=6, z-pT=20': [0.45, 0.35, 1.05, 0.65], 'Q2-y=6, z-pT=21': [0.75, 0.45, 0.22, 0.05], 'Q2-y=6, z-pT=22': [0.75, 0.45, 0.32, 0.22], 'Q2-y=6, z-pT=23': [0.75, 0.45, 0.41, 0.32], 'Q2-y=6, z-pT=24': [0.75, 0.45, 0.51, 0.41], 'Q2-y=6, z-pT=25': [0.75, 0.45, 0.65, 0.51], 'Q2-y=6, z-pT=56 - REMOVE, MIGRATION BIN': [0.75, 0.45, 1.05, 0.65], 'Q2-y=6, z-pT=26, MIGRATION BIN': [0.18, 0, 0.05, 0], 'Q2-y=6, z-pT=27, MIGRATION BIN': [0.18, 0, 0.05, 0.22], 'Q2-y=6, z-pT=28, MIGRATION BIN': [0.18, 0, 0.22, 0.32], 'Q2-y=6, z-pT=29, MIGRATION BIN': [0.18, 0, 0.32, 0.41], 'Q2-y=6, z-pT=30, MIGRATION BIN': [0.18, 0, 0.41, 0.51], 'Q2-y=6, z-pT=31, MIGRATION BIN': [0.18, 0, 0.51, 0.65], 'Q2-y=6, z-pT=32, MIGRATION BIN': [0.18, 0, 0.65, 1.05], 'Q2-y=6, z-pT=33, MIGRATION BIN': [0.18, 0, 10, 1.05], 'Q2-y=6, z-pT=34, MIGRATION BIN': [0.18, 0.23, 0.05, 0], 'Q2-y=6, z-pT=35, MIGRATION BIN': [0.18, 0.23, 10, 1.05], 'Q2-y=6, z-pT=36, MIGRATION BIN': [0.23, 0.28, 0.05, 0], 'Q2-y=6, z-pT=37, MIGRATION BIN': [0.23, 0.28, 10, 1.05], 'Q2-y=6, z-pT=38, MIGRATION BIN': [0.28, 0.35, 0.05, 0], 'Q2-y=6, z-pT=39, MIGRATION BIN': [0.28, 0.35, 10, 1.05], 'Q2-y=6, z-pT=40, MIGRATION BIN': [0.35, 0.45, 0.05, 0], 'Q2-y=6, z-pT=41, MIGRATION BIN': [0.35, 0.45, 10, 1.05], 'Q2-y=6, z-pT=42, MIGRATION BIN': [0.45, 0.75, 0.05, 0], 'Q2-y=6, z-pT=43, MIGRATION BIN': [0.45, 0.75, 10, 1.05], 'Q2-y=6, z-pT=44, MIGRATION BIN': [10, 0.75, 0, 0.05], 'Q2-y=6, z-pT=45, MIGRATION BIN': [10, 0.75, 0.05, 0.22], 'Q2-y=6, z-pT=46, MIGRATION BIN': [10, 0.75, 0.22, 0.32], 'Q2-y=6, z-pT=47, MIGRATION BIN': [10, 0.75, 0.32, 0.41], 'Q2-y=6, z-pT=48, MIGRATION BIN': [10, 0.75, 0.41, 0.51], 'Q2-y=6, z-pT=49, MIGRATION BIN': [10, 0.75, 0.51, 0.65], 'Q2-y=6, z-pT=50, MIGRATION BIN': [10, 0.75, 0.65, 1.05], 'Q2-y=6, z-pT=51, MIGRATION BIN': [10, 0.75, 10, 1.05], 'Q2-y=7, z-pT=1': [0.28, 0.22, 0.2, 0.05], 'Q2-y=7, z-pT=2': [0.28, 0.22, 0.29, 0.2], 'Q2-y=7, z-pT=3': [0.28, 0.22, 0.38, 0.29], 'Q2-y=7, z-pT=4': [0.28, 0.22, 0.48, 0.38], 'Q2-y=7, z-pT=5': [0.28, 0.22, 0.6, 0.48], 'Q2-y=7, z-pT=53 - REMOVE, MIGRATION BIN': [0.28, 0.22, 0.83, 0.6], 'Q2-y=7, z-pT=6': [0.33, 0.28, 0.2, 0.05], 'Q2-y=7, z-pT=7': [0.33, 0.28, 0.29, 0.2], 'Q2-y=7, z-pT=8': [0.33, 0.28, 0.38, 0.29], 'Q2-y=7, z-pT=9': [0.33, 0.28, 0.48, 0.38], 'Q2-y=7, z-pT=10': [0.33, 0.28, 0.6, 0.48], 'Q2-y=7, z-pT=54 - REMOVE, MIGRATION BIN': [0.33, 0.28, 0.83, 0.6], 'Q2-y=7, z-pT=11': [0.4, 0.33, 0.2, 0.05], 'Q2-y=7, z-pT=12': [0.4, 0.33, 0.29, 0.2], 'Q2-y=7, z-pT=13': [0.4, 0.33, 0.38, 0.29], 'Q2-y=7, z-pT=14': [0.4, 0.33, 0.48, 0.38], 'Q2-y=7, z-pT=15': [0.4, 0.33, 0.6, 0.48], 'Q2-y=7, z-pT=16': [0.4, 0.33, 0.83, 0.6], 'Q2-y=7, z-pT=17': [0.51, 0.4, 0.2, 0.05], 'Q2-y=7, z-pT=18': [0.51, 0.4, 0.29, 0.2], 'Q2-y=7, z-pT=19': [0.51, 0.4, 0.38, 0.29], 'Q2-y=7, z-pT=20': [0.51, 0.4, 0.48, 0.38], 'Q2-y=7, z-pT=21': [0.51, 0.4, 0.6, 0.48], 'Q2-y=7, z-pT=22': [0.51, 0.4, 0.83, 0.6], 'Q2-y=7, z-pT=23': [0.7, 0.51, 0.2, 0.05], 'Q2-y=7, z-pT=24': [0.7, 0.51, 0.29, 0.2], 'Q2-y=7, z-pT=25': [0.7, 0.51, 0.38, 0.29], 'Q2-y=7, z-pT=26': [0.7, 0.51, 0.48, 0.38], 'Q2-y=7, z-pT=55 - REMOVE, MIGRATION BIN': [0.7, 0.51, 0.6, 0.48], 'Q2-y=7, z-pT=56 - REMOVE, MIGRATION BIN': [0.7, 0.51, 0.83, 0.6], 'Q2-y=7, z-pT=27, MIGRATION BIN': [0.22, 0, 0.05, 0], 'Q2-y=7, z-pT=28, MIGRATION BIN': [0.22, 0, 0.05, 0.2], 'Q2-y=7, z-pT=29, MIGRATION BIN': [0.22, 0, 0.2, 0.29], 'Q2-y=7, z-pT=30, MIGRATION BIN': [0.22, 0, 0.29, 0.38], 'Q2-y=7, z-pT=31, MIGRATION BIN': [0.22, 0, 0.38, 0.48], 'Q2-y=7, z-pT=32, MIGRATION BIN': [0.22, 0, 0.48, 0.6], 'Q2-y=7, z-pT=33, MIGRATION BIN': [0.22, 0, 0.6, 0.83], 'Q2-y=7, z-pT=34, MIGRATION BIN': [0.22, 0, 10, 0.83], 'Q2-y=7, z-pT=35, MIGRATION BIN': [0.22, 0.28, 0.05, 0], 'Q2-y=7, z-pT=36, MIGRATION BIN': [0.22, 0.28, 10, 0.83], 'Q2-y=7, z-pT=37, MIGRATION BIN': [0.28, 0.33, 0.05, 0], 'Q2-y=7, z-pT=38, MIGRATION BIN': [0.28, 0.33, 10, 0.83], 'Q2-y=7, z-pT=39, MIGRATION BIN': [0.33, 0.4, 0.05, 0], 'Q2-y=7, z-pT=40, MIGRATION BIN': [0.33, 0.4, 10, 0.83], 'Q2-y=7, z-pT=41, MIGRATION BIN': [0.4, 0.51, 0.05, 0], 'Q2-y=7, z-pT=42, MIGRATION BIN': [0.4, 0.51, 10, 0.83], 'Q2-y=7, z-pT=43, MIGRATION BIN': [0.51, 0.7, 0.05, 0], 'Q2-y=7, z-pT=44, MIGRATION BIN': [0.51, 0.7, 10, 0.83], 'Q2-y=7, z-pT=45, MIGRATION BIN': [10, 0.7, 0, 0.05], 'Q2-y=7, z-pT=46, MIGRATION BIN': [10, 0.7, 0.05, 0.2], 'Q2-y=7, z-pT=47, MIGRATION BIN': [10, 0.7, 0.2, 0.29], 'Q2-y=7, z-pT=48, MIGRATION BIN': [10, 0.7, 0.29, 0.38], 'Q2-y=7, z-pT=49, MIGRATION BIN': [10, 0.7, 0.38, 0.48], 'Q2-y=7, z-pT=50, MIGRATION BIN': [10, 0.7, 0.48, 0.6], 'Q2-y=7, z-pT=51, MIGRATION BIN': [10, 0.7, 0.6, 0.83], 'Q2-y=7, z-pT=52, MIGRATION BIN': [10, 0.7, 10, 0.83], 'Q2-y=8, z-pT=1': [0.32, 0.27, 0.21, 0.05], 'Q2-y=8, z-pT=2': [0.32, 0.27, 0.31, 0.21], 'Q2-y=8, z-pT=3': [0.32, 0.27, 0.4, 0.31], 'Q2-y=8, z-pT=4': [0.32, 0.27, 0.5, 0.4], 'Q2-y=8, z-pT=5': [0.36, 0.32, 0.21, 0.05], 'Q2-y=8, z-pT=6': [0.36, 0.32, 0.31, 0.21], 'Q2-y=8, z-pT=7': [0.36, 0.32, 0.4, 0.31], 'Q2-y=8, z-pT=8': [0.36, 0.32, 0.5, 0.4], 'Q2-y=8, z-pT=9': [0.4, 0.36, 0.21, 0.05], 'Q2-y=8, z-pT=10': [0.4, 0.36, 0.31, 0.21], 'Q2-y=8, z-pT=11': [0.4, 0.36, 0.4, 0.31], 'Q2-y=8, z-pT=12': [0.4, 0.36, 0.5, 0.4], 'Q2-y=8, z-pT=13': [0.45, 0.4, 0.21, 0.05], 'Q2-y=8, z-pT=14': [0.45, 0.4, 0.31, 0.21], 'Q2-y=8, z-pT=15': [0.45, 0.4, 0.4, 0.31], 'Q2-y=8, z-pT=16': [0.45, 0.4, 0.5, 0.4], 'Q2-y=8, z-pT=17': [0.5, 0.45, 0.21, 0.05], 'Q2-y=8, z-pT=18': [0.5, 0.45, 0.31, 0.21], 'Q2-y=8, z-pT=19': [0.5, 0.45, 0.4, 0.31], 'Q2-y=8, z-pT=20': [0.5, 0.45, 0.5, 0.4], 'Q2-y=8, z-pT=21': [0.6, 0.5, 0.21, 0.05], 'Q2-y=8, z-pT=22': [0.6, 0.5, 0.31, 0.21], 'Q2-y=8, z-pT=47 - REMOVE, MIGRATION BIN': [0.6, 0.5, 0.4, 0.31], 'Q2-y=8, z-pT=48 - REMOVE, MIGRATION BIN': [0.6, 0.5, 0.5, 0.4], 'Q2-y=8, z-pT=23, MIGRATION BIN': [0.27, 0, 0.05, 0], 'Q2-y=8, z-pT=24, MIGRATION BIN': [0.27, 0, 0.05, 0.21], 'Q2-y=8, z-pT=25, MIGRATION BIN': [0.27, 0, 0.21, 0.31], 'Q2-y=8, z-pT=26, MIGRATION BIN': [0.27, 0, 0.31, 0.4], 'Q2-y=8, z-pT=27, MIGRATION BIN': [0.27, 0, 0.4, 0.5], 'Q2-y=8, z-pT=28, MIGRATION BIN': [0.27, 0, 10, 0.5], 'Q2-y=8, z-pT=29, MIGRATION BIN': [0.27, 0.32, 0.05, 0], 'Q2-y=8, z-pT=30, MIGRATION BIN': [0.27, 0.32, 10, 0.5], 'Q2-y=8, z-pT=31, MIGRATION BIN': [0.32, 0.36, 0.05, 0], 'Q2-y=8, z-pT=32, MIGRATION BIN': [0.32, 0.36, 10, 0.5], 'Q2-y=8, z-pT=33, MIGRATION BIN': [0.36, 0.4, 0.05, 0], 'Q2-y=8, z-pT=34, MIGRATION BIN': [0.36, 0.4, 10, 0.5], 'Q2-y=8, z-pT=35, MIGRATION BIN': [0.4, 0.45, 0.05, 0], 'Q2-y=8, z-pT=36, MIGRATION BIN': [0.4, 0.45, 10, 0.5], 'Q2-y=8, z-pT=37, MIGRATION BIN': [0.45, 0.5, 0.05, 0], 'Q2-y=8, z-pT=38, MIGRATION BIN': [0.45, 0.5, 10, 0.5], 'Q2-y=8, z-pT=39, MIGRATION BIN': [0.5, 0.6, 0.05, 0], 'Q2-y=8, z-pT=40, MIGRATION BIN': [0.5, 0.6, 10, 0.5], 'Q2-y=8, z-pT=41, MIGRATION BIN': [10, 0.6, 0, 0.05], 'Q2-y=8, z-pT=42, MIGRATION BIN': [10, 0.6, 0.05, 0.21], 'Q2-y=8, z-pT=43, MIGRATION BIN': [10, 0.6, 0.21, 0.31], 'Q2-y=8, z-pT=44, MIGRATION BIN': [10, 0.6, 0.31, 0.4], 'Q2-y=8, z-pT=45, MIGRATION BIN': [10, 0.6, 0.4, 0.5], 'Q2-y=8, z-pT=46, MIGRATION BIN': [10, 0.6, 10, 0.5], 'Q2-y=9, z-pT=1': [0.2, 0.16, 0.22, 0.05], 'Q2-y=9, z-pT=2': [0.2, 0.16, 0.3, 0.22], 'Q2-y=9, z-pT=3': [0.2, 0.16, 0.38, 0.3], 'Q2-y=9, z-pT=4': [0.2, 0.16, 0.46, 0.38], 'Q2-y=9, z-pT=5': [0.2, 0.16, 0.58, 0.46], 'Q2-y=9, z-pT=59 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.74, 0.58], 'Q2-y=9, z-pT=60 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.95, 0.74], 'Q2-y=9, z-pT=6': [0.24, 0.2, 0.22, 0.05], 'Q2-y=9, z-pT=7': [0.24, 0.2, 0.3, 0.22], 'Q2-y=9, z-pT=8': [0.24, 0.2, 0.38, 0.3], 'Q2-y=9, z-pT=9': [0.24, 0.2, 0.46, 0.38], 'Q2-y=9, z-pT=10': [0.24, 0.2, 0.58, 0.46], 'Q2-y=9, z-pT=61 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.74, 0.58], 'Q2-y=9, z-pT=62 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.95, 0.74], 'Q2-y=9, z-pT=11': [0.3, 0.24, 0.22, 0.05], 'Q2-y=9, z-pT=12': [0.3, 0.24, 0.3, 0.22], 'Q2-y=9, z-pT=13': [0.3, 0.24, 0.38, 0.3], 'Q2-y=9, z-pT=14': [0.3, 0.24, 0.46, 0.38], 'Q2-y=9, z-pT=15': [0.3, 0.24, 0.58, 0.46], 'Q2-y=9, z-pT=16': [0.3, 0.24, 0.74, 0.58], 'Q2-y=9, z-pT=63 - REMOVE, MIGRATION BIN': [0.3, 0.24, 0.95, 0.74], 'Q2-y=9, z-pT=17': [0.42, 0.3, 0.22, 0.05], 'Q2-y=9, z-pT=18': [0.42, 0.3, 0.3, 0.22], 'Q2-y=9, z-pT=19': [0.42, 0.3, 0.38, 0.3], 'Q2-y=9, z-pT=20': [0.42, 0.3, 0.46, 0.38], 'Q2-y=9, z-pT=21': [0.42, 0.3, 0.58, 0.46], 'Q2-y=9, z-pT=22': [0.42, 0.3, 0.74, 0.58], 'Q2-y=9, z-pT=23': [0.42, 0.3, 0.95, 0.74], 'Q2-y=9, z-pT=24': [0.7, 0.42, 0.22, 0.05], 'Q2-y=9, z-pT=25': [0.7, 0.42, 0.3, 0.22], 'Q2-y=9, z-pT=26': [0.7, 0.42, 0.38, 0.3], 'Q2-y=9, z-pT=27': [0.7, 0.42, 0.46, 0.38], 'Q2-y=9, z-pT=28': [0.7, 0.42, 0.58, 0.46], 'Q2-y=9, z-pT=29': [0.7, 0.42, 0.74, 0.58], 'Q2-y=9, z-pT=30': [0.7, 0.42, 0.95, 0.74], 'Q2-y=9, z-pT=31, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=9, z-pT=32, MIGRATION BIN': [0.16, 0, 0.05, 0.22], 'Q2-y=9, z-pT=33, MIGRATION BIN': [0.16, 0, 0.22, 0.3], 'Q2-y=9, z-pT=34, MIGRATION BIN': [0.16, 0, 0.3, 0.38], 'Q2-y=9, z-pT=35, MIGRATION BIN': [0.16, 0, 0.38, 0.46], 'Q2-y=9, z-pT=36, MIGRATION BIN': [0.16, 0, 0.46, 0.58], 'Q2-y=9, z-pT=37, MIGRATION BIN': [0.16, 0, 0.58, 0.74], 'Q2-y=9, z-pT=38, MIGRATION BIN': [0.16, 0, 0.74, 0.95], 'Q2-y=9, z-pT=39, MIGRATION BIN': [0.16, 0, 10, 0.95], 'Q2-y=9, z-pT=40, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=9, z-pT=41, MIGRATION BIN': [0.16, 0.2, 10, 0.95], 'Q2-y=9, z-pT=42, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=9, z-pT=43, MIGRATION BIN': [0.2, 0.24, 10, 0.95], 'Q2-y=9, z-pT=44, MIGRATION BIN': [0.24, 0.3, 0.05, 0], 'Q2-y=9, z-pT=45, MIGRATION BIN': [0.24, 0.3, 10, 0.95], 'Q2-y=9, z-pT=46, MIGRATION BIN': [0.3, 0.42, 0.05, 0], 'Q2-y=9, z-pT=47, MIGRATION BIN': [0.3, 0.42, 10, 0.95], 'Q2-y=9, z-pT=48, MIGRATION BIN': [0.42, 0.7, 0.05, 0], 'Q2-y=9, z-pT=49, MIGRATION BIN': [0.42, 0.7, 10, 0.95], 'Q2-y=9, z-pT=50, MIGRATION BIN': [10, 0.7, 0, 0.05], 'Q2-y=9, z-pT=51, MIGRATION BIN': [10, 0.7, 0.05, 0.22], 'Q2-y=9, z-pT=52, MIGRATION BIN': [10, 0.7, 0.22, 0.3], 'Q2-y=9, z-pT=53, MIGRATION BIN': [10, 0.7, 0.3, 0.38], 'Q2-y=9, z-pT=54, MIGRATION BIN': [10, 0.7, 0.38, 0.46], 'Q2-y=9, z-pT=55, MIGRATION BIN': [10, 0.7, 0.46, 0.58], 'Q2-y=9, z-pT=56, MIGRATION BIN': [10, 0.7, 0.58, 0.74], 'Q2-y=9, z-pT=57, MIGRATION BIN': [10, 0.7, 0.74, 0.95], 'Q2-y=9, z-pT=58, MIGRATION BIN': [10, 0.7, 10, 0.95], 'Q2-y=10, z-pT=1': [0.23, 0.19, 0.21, 0.05], 'Q2-y=10, z-pT=2': [0.23, 0.19, 0.31, 0.21], 'Q2-y=10, z-pT=3': [0.23, 0.19, 0.4, 0.31], 'Q2-y=10, z-pT=4': [0.23, 0.19, 0.5, 0.4], 'Q2-y=10, z-pT=60 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.64, 0.5], 'Q2-y=10, z-pT=61 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.9, 0.64], 'Q2-y=10, z-pT=5': [0.26, 0.23, 0.21, 0.05], 'Q2-y=10, z-pT=6': [0.26, 0.23, 0.31, 0.21], 'Q2-y=10, z-pT=7': [0.26, 0.23, 0.4, 0.31], 'Q2-y=10, z-pT=8': [0.26, 0.23, 0.5, 0.4], 'Q2-y=10, z-pT=9': [0.26, 0.23, 0.64, 0.5], 'Q2-y=10, z-pT=62 - REMOVE, MIGRATION BIN': [0.26, 0.23, 0.9, 0.64], 'Q2-y=10, z-pT=10': [0.32, 0.26, 0.21, 0.05], 'Q2-y=10, z-pT=11': [0.32, 0.26, 0.31, 0.21], 'Q2-y=10, z-pT=12': [0.32, 0.26, 0.4, 0.31], 'Q2-y=10, z-pT=13': [0.32, 0.26, 0.5, 0.4], 'Q2-y=10, z-pT=14': [0.32, 0.26, 0.64, 0.5], 'Q2-y=10, z-pT=63 - REMOVE, MIGRATION BIN': [0.32, 0.26, 0.9, 0.64], 'Q2-y=10, z-pT=15': [0.4, 0.32, 0.21, 0.05], 'Q2-y=10, z-pT=16': [0.4, 0.32, 0.31, 0.21], 'Q2-y=10, z-pT=17': [0.4, 0.32, 0.4, 0.31], 'Q2-y=10, z-pT=18': [0.4, 0.32, 0.5, 0.4], 'Q2-y=10, z-pT=19': [0.4, 0.32, 0.64, 0.5], 'Q2-y=10, z-pT=20': [0.4, 0.32, 0.9, 0.64], 'Q2-y=10, z-pT=21': [0.5, 0.4, 0.21, 0.05], 'Q2-y=10, z-pT=22': [0.5, 0.4, 0.31, 0.21], 'Q2-y=10, z-pT=23': [0.5, 0.4, 0.4, 0.31], 'Q2-y=10, z-pT=24': [0.5, 0.4, 0.5, 0.4], 'Q2-y=10, z-pT=25': [0.5, 0.4, 0.64, 0.5], 'Q2-y=10, z-pT=26': [0.5, 0.4, 0.9, 0.64], 'Q2-y=10, z-pT=27': [0.72, 0.5, 0.21, 0.05], 'Q2-y=10, z-pT=28': [0.72, 0.5, 0.31, 0.21], 'Q2-y=10, z-pT=29': [0.72, 0.5, 0.4, 0.31], 'Q2-y=10, z-pT=30': [0.72, 0.5, 0.5, 0.4], 'Q2-y=10, z-pT=31': [0.72, 0.5, 0.64, 0.5], 'Q2-y=10, z-pT=64 - REMOVE, MIGRATION BIN': [0.72, 0.5, 0.9, 0.64], 'Q2-y=10, z-pT=32, MIGRATION BIN': [0.19, 0, 0.05, 0], 'Q2-y=10, z-pT=33, MIGRATION BIN': [0.19, 0, 0.05, 0.21], 'Q2-y=10, z-pT=34, MIGRATION BIN': [0.19, 0, 0.21, 0.31], 'Q2-y=10, z-pT=35, MIGRATION BIN': [0.19, 0, 0.31, 0.4], 'Q2-y=10, z-pT=36, MIGRATION BIN': [0.19, 0, 0.4, 0.5], 'Q2-y=10, z-pT=37, MIGRATION BIN': [0.19, 0, 0.5, 0.64], 'Q2-y=10, z-pT=38, MIGRATION BIN': [0.19, 0, 0.64, 0.9], 'Q2-y=10, z-pT=39, MIGRATION BIN': [0.19, 0, 10, 0.9], 'Q2-y=10, z-pT=40, MIGRATION BIN': [0.19, 0.23, 0.05, 0], 'Q2-y=10, z-pT=41, MIGRATION BIN': [0.19, 0.23, 10, 0.9], 'Q2-y=10, z-pT=42, MIGRATION BIN': [0.23, 0.26, 0.05, 0], 'Q2-y=10, z-pT=43, MIGRATION BIN': [0.23, 0.26, 10, 0.9], 'Q2-y=10, z-pT=44, MIGRATION BIN': [0.26, 0.32, 0.05, 0], 'Q2-y=10, z-pT=45, MIGRATION BIN': [0.26, 0.32, 10, 0.9], 'Q2-y=10, z-pT=46, MIGRATION BIN': [0.32, 0.4, 0.05, 0], 'Q2-y=10, z-pT=47, MIGRATION BIN': [0.32, 0.4, 10, 0.9], 'Q2-y=10, z-pT=48, MIGRATION BIN': [0.4, 0.5, 0.05, 0], 'Q2-y=10, z-pT=49, MIGRATION BIN': [0.4, 0.5, 10, 0.9], 'Q2-y=10, z-pT=50, MIGRATION BIN': [0.5, 0.72, 0.05, 0], 'Q2-y=10, z-pT=51, MIGRATION BIN': [0.5, 0.72, 10, 0.9], 'Q2-y=10, z-pT=52, MIGRATION BIN': [10, 0.72, 0, 0.05], 'Q2-y=10, z-pT=53, MIGRATION BIN': [10, 0.72, 0.05, 0.21], 'Q2-y=10, z-pT=54, MIGRATION BIN': [10, 0.72, 0.21, 0.31], 'Q2-y=10, z-pT=55, MIGRATION BIN': [10, 0.72, 0.31, 0.4], 'Q2-y=10, z-pT=56, MIGRATION BIN': [10, 0.72, 0.4, 0.5], 'Q2-y=10, z-pT=57, MIGRATION BIN': [10, 0.72, 0.5, 0.64], 'Q2-y=10, z-pT=58, MIGRATION BIN': [10, 0.72, 0.64, 0.9], 'Q2-y=10, z-pT=59, MIGRATION BIN': [10, 0.72, 10, 0.9], 'Q2-y=11, z-pT=1': [0.27, 0.22, 0.2, 0.05], 'Q2-y=11, z-pT=2': [0.27, 0.22, 0.3, 0.2], 'Q2-y=11, z-pT=3': [0.27, 0.22, 0.4, 0.3], 'Q2-y=11, z-pT=4': [0.27, 0.22, 0.54, 0.4], 'Q2-y=11, z-pT=46 - REMOVE, MIGRATION BIN': [0.27, 0.22, 0.69, 0.54], 'Q2-y=11, z-pT=5': [0.32, 0.27, 0.2, 0.05], 'Q2-y=11, z-pT=6': [0.32, 0.27, 0.3, 0.2], 'Q2-y=11, z-pT=7': [0.32, 0.27, 0.4, 0.3], 'Q2-y=11, z-pT=8': [0.32, 0.27, 0.54, 0.4], 'Q2-y=11, z-pT=9': [0.32, 0.27, 0.69, 0.54], 'Q2-y=11, z-pT=10': [0.4, 0.32, 0.2, 0.05], 'Q2-y=11, z-pT=11': [0.4, 0.32, 0.3, 0.2], 'Q2-y=11, z-pT=12': [0.4, 0.32, 0.4, 0.3], 'Q2-y=11, z-pT=13': [0.4, 0.32, 0.54, 0.4], 'Q2-y=11, z-pT=14': [0.4, 0.32, 0.69, 0.54], 'Q2-y=11, z-pT=15': [0.53, 0.4, 0.2, 0.05], 'Q2-y=11, z-pT=16': [0.53, 0.4, 0.3, 0.2], 'Q2-y=11, z-pT=17': [0.53, 0.4, 0.4, 0.3], 'Q2-y=11, z-pT=18': [0.53, 0.4, 0.54, 0.4], 'Q2-y=11, z-pT=19': [0.53, 0.4, 0.69, 0.54], 'Q2-y=11, z-pT=20': [0.69, 0.53, 0.2, 0.05], 'Q2-y=11, z-pT=21': [0.69, 0.53, 0.3, 0.2], 'Q2-y=11, z-pT=47 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.4, 0.3], 'Q2-y=11, z-pT=48 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.54, 0.4], 'Q2-y=11, z-pT=49 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.69, 0.54], 'Q2-y=11, z-pT=22, MIGRATION BIN': [0.22, 0, 0.05, 0], 'Q2-y=11, z-pT=23, MIGRATION BIN': [0.22, 0, 0.05, 0.2], 'Q2-y=11, z-pT=24, MIGRATION BIN': [0.22, 0, 0.2, 0.3], 'Q2-y=11, z-pT=25, MIGRATION BIN': [0.22, 0, 0.3, 0.4], 'Q2-y=11, z-pT=26, MIGRATION BIN': [0.22, 0, 0.4, 0.54], 'Q2-y=11, z-pT=27, MIGRATION BIN': [0.22, 0, 0.54, 0.69], 'Q2-y=11, z-pT=28, MIGRATION BIN': [0.22, 0, 10, 0.69], 'Q2-y=11, z-pT=29, MIGRATION BIN': [0.22, 0.27, 0.05, 0], 'Q2-y=11, z-pT=30, MIGRATION BIN': [0.22, 0.27, 10, 0.69], 'Q2-y=11, z-pT=31, MIGRATION BIN': [0.27, 0.32, 0.05, 0], 'Q2-y=11, z-pT=32, MIGRATION BIN': [0.27, 0.32, 10, 0.69], 'Q2-y=11, z-pT=33, MIGRATION BIN': [0.32, 0.4, 0.05, 0], 'Q2-y=11, z-pT=34, MIGRATION BIN': [0.32, 0.4, 10, 0.69], 'Q2-y=11, z-pT=35, MIGRATION BIN': [0.4, 0.53, 0.05, 0], 'Q2-y=11, z-pT=36, MIGRATION BIN': [0.4, 0.53, 10, 0.69], 'Q2-y=11, z-pT=37, MIGRATION BIN': [0.53, 0.69, 0.05, 0], 'Q2-y=11, z-pT=38, MIGRATION BIN': [0.53, 0.69, 10, 0.69], 'Q2-y=11, z-pT=39, MIGRATION BIN': [10, 0.69, 0, 0.05], 'Q2-y=11, z-pT=40, MIGRATION BIN': [10, 0.69, 0.05, 0.2], 'Q2-y=11, z-pT=41, MIGRATION BIN': [10, 0.69, 0.2, 0.3], 'Q2-y=11, z-pT=42, MIGRATION BIN': [10, 0.69, 0.3, 0.4], 'Q2-y=11, z-pT=43, MIGRATION BIN': [10, 0.69, 0.4, 0.54], 'Q2-y=11, z-pT=44, MIGRATION BIN': [10, 0.69, 0.54, 0.69], 'Q2-y=11, z-pT=45, MIGRATION BIN': [10, 0.69, 10, 0.69], 'Q2-y=12, z-pT=1': [0.31, 0.27, 0.22, 0.05], 'Q2-y=12, z-pT=2': [0.31, 0.27, 0.32, 0.22], 'Q2-y=12, z-pT=3': [0.31, 0.27, 0.41, 0.32], 'Q2-y=12, z-pT=4': [0.35, 0.31, 0.22, 0.05], 'Q2-y=12, z-pT=5': [0.35, 0.31, 0.32, 0.22], 'Q2-y=12, z-pT=6': [0.35, 0.31, 0.41, 0.32], 'Q2-y=12, z-pT=7': [0.4, 0.35, 0.22, 0.05], 'Q2-y=12, z-pT=8': [0.4, 0.35, 0.32, 0.22], 'Q2-y=12, z-pT=9': [0.4, 0.35, 0.41, 0.32], 'Q2-y=12, z-pT=10': [0.5, 0.4, 0.22, 0.05], 'Q2-y=12, z-pT=29 - REMOVE, MIGRATION BIN': [0.5, 0.4, 0.32, 0.22], 'Q2-y=12, z-pT=30 - REMOVE, MIGRATION BIN': [0.5, 0.4, 0.41, 0.32], 'Q2-y=12, z-pT=11, MIGRATION BIN': [0.27, 0, 0.05, 0], 'Q2-y=12, z-pT=12, MIGRATION BIN': [0.27, 0, 0.05, 0.22], 'Q2-y=12, z-pT=13, MIGRATION BIN': [0.27, 0, 0.22, 0.32], 'Q2-y=12, z-pT=14, MIGRATION BIN': [0.27, 0, 0.32, 0.41], 'Q2-y=12, z-pT=15, MIGRATION BIN': [0.27, 0, 10, 0.41], 'Q2-y=12, z-pT=16, MIGRATION BIN': [0.27, 0.31, 0.05, 0], 'Q2-y=12, z-pT=17, MIGRATION BIN': [0.27, 0.31, 10, 0.41], 'Q2-y=12, z-pT=18, MIGRATION BIN': [0.31, 0.35, 0.05, 0], 'Q2-y=12, z-pT=19, MIGRATION BIN': [0.31, 0.35, 10, 0.41], 'Q2-y=12, z-pT=20, MIGRATION BIN': [0.35, 0.4, 0.05, 0], 'Q2-y=12, z-pT=21, MIGRATION BIN': [0.35, 0.4, 10, 0.41], 'Q2-y=12, z-pT=22, MIGRATION BIN': [0.4, 0.5, 0.05, 0], 'Q2-y=12, z-pT=23, MIGRATION BIN': [0.4, 0.5, 10, 0.41], 'Q2-y=12, z-pT=24, MIGRATION BIN': [10, 0.5, 0, 0.05], 'Q2-y=12, z-pT=25, MIGRATION BIN': [10, 0.5, 0.05, 0.22], 'Q2-y=12, z-pT=26, MIGRATION BIN': [10, 0.5, 0.22, 0.32], 'Q2-y=12, z-pT=27, MIGRATION BIN': [10, 0.5, 0.32, 0.41], 'Q2-y=12, z-pT=28, MIGRATION BIN': [10, 0.5, 10, 0.41], 'Q2-y=13, z-pT=1': [0.2, 0.16, 0.22, 0.05], 'Q2-y=13, z-pT=2': [0.2, 0.16, 0.35, 0.22], 'Q2-y=13, z-pT=3': [0.2, 0.16, 0.45, 0.35], 'Q2-y=13, z-pT=52 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.6, 0.45], 'Q2-y=13, z-pT=53 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.9, 0.6], 'Q2-y=13, z-pT=4': [0.24, 0.2, 0.22, 0.05], 'Q2-y=13, z-pT=5': [0.24, 0.2, 0.35, 0.22], 'Q2-y=13, z-pT=6': [0.24, 0.2, 0.45, 0.35], 'Q2-y=13, z-pT=7': [0.24, 0.2, 0.6, 0.45], 'Q2-y=13, z-pT=54 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.9, 0.6], 'Q2-y=13, z-pT=8': [0.29, 0.24, 0.22, 0.05], 'Q2-y=13, z-pT=9': [0.29, 0.24, 0.35, 0.22], 'Q2-y=13, z-pT=10': [0.29, 0.24, 0.45, 0.35], 'Q2-y=13, z-pT=11': [0.29, 0.24, 0.6, 0.45], 'Q2-y=13, z-pT=55 - REMOVE, MIGRATION BIN': [0.29, 0.24, 0.9, 0.6], 'Q2-y=13, z-pT=12': [0.36, 0.29, 0.22, 0.05], 'Q2-y=13, z-pT=13': [0.36, 0.29, 0.35, 0.22], 'Q2-y=13, z-pT=14': [0.36, 0.29, 0.45, 0.35], 'Q2-y=13, z-pT=15': [0.36, 0.29, 0.6, 0.45], 'Q2-y=13, z-pT=16': [0.36, 0.29, 0.9, 0.6], 'Q2-y=13, z-pT=17': [0.51, 0.36, 0.22, 0.05], 'Q2-y=13, z-pT=18': [0.51, 0.36, 0.35, 0.22], 'Q2-y=13, z-pT=19': [0.51, 0.36, 0.45, 0.35], 'Q2-y=13, z-pT=20': [0.51, 0.36, 0.6, 0.45], 'Q2-y=13, z-pT=21': [0.51, 0.36, 0.9, 0.6], 'Q2-y=13, z-pT=22': [0.72, 0.51, 0.22, 0.05], 'Q2-y=13, z-pT=23': [0.72, 0.51, 0.35, 0.22], 'Q2-y=13, z-pT=24': [0.72, 0.51, 0.45, 0.35], 'Q2-y=13, z-pT=25': [0.72, 0.51, 0.6, 0.45], 'Q2-y=13, z-pT=56 - REMOVE, MIGRATION BIN': [0.72, 0.51, 0.9, 0.6], 'Q2-y=13, z-pT=26, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=13, z-pT=27, MIGRATION BIN': [0.16, 0, 0.05, 0.22], 'Q2-y=13, z-pT=28, MIGRATION BIN': [0.16, 0, 0.22, 0.35], 'Q2-y=13, z-pT=29, MIGRATION BIN': [0.16, 0, 0.35, 0.45], 'Q2-y=13, z-pT=30, MIGRATION BIN': [0.16, 0, 0.45, 0.6], 'Q2-y=13, z-pT=31, MIGRATION BIN': [0.16, 0, 0.6, 0.9], 'Q2-y=13, z-pT=32, MIGRATION BIN': [0.16, 0, 10, 0.9], 'Q2-y=13, z-pT=33, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=13, z-pT=34, MIGRATION BIN': [0.16, 0.2, 10, 0.9], 'Q2-y=13, z-pT=35, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=13, z-pT=36, MIGRATION BIN': [0.2, 0.24, 10, 0.9], 'Q2-y=13, z-pT=37, MIGRATION BIN': [0.24, 0.29, 0.05, 0], 'Q2-y=13, z-pT=38, MIGRATION BIN': [0.24, 0.29, 10, 0.9], 'Q2-y=13, z-pT=39, MIGRATION BIN': [0.29, 0.36, 0.05, 0], 'Q2-y=13, z-pT=40, MIGRATION BIN': [0.29, 0.36, 10, 0.9], 'Q2-y=13, z-pT=41, MIGRATION BIN': [0.36, 0.51, 0.05, 0], 'Q2-y=13, z-pT=42, MIGRATION BIN': [0.36, 0.51, 10, 0.9], 'Q2-y=13, z-pT=43, MIGRATION BIN': [0.51, 0.72, 0.05, 0], 'Q2-y=13, z-pT=44, MIGRATION BIN': [0.51, 0.72, 10, 0.9], 'Q2-y=13, z-pT=45, MIGRATION BIN': [10, 0.72, 0, 0.05], 'Q2-y=13, z-pT=46, MIGRATION BIN': [10, 0.72, 0.05, 0.22], 'Q2-y=13, z-pT=47, MIGRATION BIN': [10, 0.72, 0.22, 0.35], 'Q2-y=13, z-pT=48, MIGRATION BIN': [10, 0.72, 0.35, 0.45], 'Q2-y=13, z-pT=49, MIGRATION BIN': [10, 0.72, 0.45, 0.6], 'Q2-y=13, z-pT=50, MIGRATION BIN': [10, 0.72, 0.6, 0.9], 'Q2-y=13, z-pT=51, MIGRATION BIN': [10, 0.72, 10, 0.9], 'Q2-y=14, z-pT=1': [0.23, 0.19, 0.2, 0.05], 'Q2-y=14, z-pT=2': [0.23, 0.19, 0.3, 0.2], 'Q2-y=14, z-pT=3': [0.23, 0.19, 0.4, 0.3], 'Q2-y=14, z-pT=4': [0.23, 0.19, 0.5, 0.4], 'Q2-y=14, z-pT=56 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.65, 0.5], 'Q2-y=14, z-pT=57 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.8, 0.65], 'Q2-y=14, z-pT=5': [0.27, 0.23, 0.2, 0.05], 'Q2-y=14, z-pT=6': [0.27, 0.23, 0.3, 0.2], 'Q2-y=14, z-pT=7': [0.27, 0.23, 0.4, 0.3], 'Q2-y=14, z-pT=8': [0.27, 0.23, 0.5, 0.4], 'Q2-y=14, z-pT=9': [0.27, 0.23, 0.65, 0.5], 'Q2-y=14, z-pT=58 - REMOVE, MIGRATION BIN': [0.27, 0.23, 0.8, 0.65], 'Q2-y=14, z-pT=10': [0.32, 0.27, 0.2, 0.05], 'Q2-y=14, z-pT=11': [0.32, 0.27, 0.3, 0.2], 'Q2-y=14, z-pT=12': [0.32, 0.27, 0.4, 0.3], 'Q2-y=14, z-pT=13': [0.32, 0.27, 0.5, 0.4], 'Q2-y=14, z-pT=14': [0.32, 0.27, 0.65, 0.5], 'Q2-y=14, z-pT=59 - REMOVE, MIGRATION BIN': [0.32, 0.27, 0.8, 0.65], 'Q2-y=14, z-pT=15': [0.4, 0.32, 0.2, 0.05], 'Q2-y=14, z-pT=16': [0.4, 0.32, 0.3, 0.2], 'Q2-y=14, z-pT=17': [0.4, 0.32, 0.4, 0.3], 'Q2-y=14, z-pT=18': [0.4, 0.32, 0.5, 0.4], 'Q2-y=14, z-pT=19': [0.4, 0.32, 0.65, 0.5], 'Q2-y=14, z-pT=60 - REMOVE, MIGRATION BIN': [0.4, 0.32, 0.8, 0.65], 'Q2-y=14, z-pT=20': [0.53, 0.4, 0.2, 0.05], 'Q2-y=14, z-pT=21': [0.53, 0.4, 0.3, 0.2], 'Q2-y=14, z-pT=22': [0.53, 0.4, 0.4, 0.3], 'Q2-y=14, z-pT=23': [0.53, 0.4, 0.5, 0.4], 'Q2-y=14, z-pT=24': [0.53, 0.4, 0.65, 0.5], 'Q2-y=14, z-pT=61 - REMOVE, MIGRATION BIN': [0.53, 0.4, 0.8, 0.65], 'Q2-y=14, z-pT=25': [0.69, 0.53, 0.2, 0.05], 'Q2-y=14, z-pT=26': [0.69, 0.53, 0.3, 0.2], 'Q2-y=14, z-pT=27': [0.69, 0.53, 0.4, 0.3], 'Q2-y=14, z-pT=62 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.5, 0.4], 'Q2-y=14, z-pT=63 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.65, 0.5], 'Q2-y=14, z-pT=64 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.8, 0.65], 'Q2-y=14, z-pT=28, MIGRATION BIN': [0.19, 0, 0.05, 0], 'Q2-y=14, z-pT=29, MIGRATION BIN': [0.19, 0, 0.05, 0.2], 'Q2-y=14, z-pT=30, MIGRATION BIN': [0.19, 0, 0.2, 0.3], 'Q2-y=14, z-pT=31, MIGRATION BIN': [0.19, 0, 0.3, 0.4], 'Q2-y=14, z-pT=32, MIGRATION BIN': [0.19, 0, 0.4, 0.5], 'Q2-y=14, z-pT=33, MIGRATION BIN': [0.19, 0, 0.5, 0.65], 'Q2-y=14, z-pT=34, MIGRATION BIN': [0.19, 0, 0.65, 0.8], 'Q2-y=14, z-pT=35, MIGRATION BIN': [0.19, 0, 10, 0.8], 'Q2-y=14, z-pT=36, MIGRATION BIN': [0.19, 0.23, 0.05, 0], 'Q2-y=14, z-pT=37, MIGRATION BIN': [0.19, 0.23, 10, 0.8], 'Q2-y=14, z-pT=38, MIGRATION BIN': [0.23, 0.27, 0.05, 0], 'Q2-y=14, z-pT=39, MIGRATION BIN': [0.23, 0.27, 10, 0.8], 'Q2-y=14, z-pT=40, MIGRATION BIN': [0.27, 0.32, 0.05, 0], 'Q2-y=14, z-pT=41, MIGRATION BIN': [0.27, 0.32, 10, 0.8], 'Q2-y=14, z-pT=42, MIGRATION BIN': [0.32, 0.4, 0.05, 0], 'Q2-y=14, z-pT=43, MIGRATION BIN': [0.32, 0.4, 10, 0.8], 'Q2-y=14, z-pT=44, MIGRATION BIN': [0.4, 0.53, 0.05, 0], 'Q2-y=14, z-pT=45, MIGRATION BIN': [0.4, 0.53, 10, 0.8], 'Q2-y=14, z-pT=46, MIGRATION BIN': [0.53, 0.69, 0.05, 0], 'Q2-y=14, z-pT=47, MIGRATION BIN': [0.53, 0.69, 10, 0.8], 'Q2-y=14, z-pT=48, MIGRATION BIN': [10, 0.69, 0, 0.05], 'Q2-y=14, z-pT=49, MIGRATION BIN': [10, 0.69, 0.05, 0.2], 'Q2-y=14, z-pT=50, MIGRATION BIN': [10, 0.69, 0.2, 0.3], 'Q2-y=14, z-pT=51, MIGRATION BIN': [10, 0.69, 0.3, 0.4], 'Q2-y=14, z-pT=52, MIGRATION BIN': [10, 0.69, 0.4, 0.5], 'Q2-y=14, z-pT=53, MIGRATION BIN': [10, 0.69, 0.5, 0.65], 'Q2-y=14, z-pT=54, MIGRATION BIN': [10, 0.69, 0.65, 0.8], 'Q2-y=14, z-pT=55, MIGRATION BIN': [10, 0.69, 10, 0.8], 'Q2-y=15, z-pT=1': [0.28, 0.22, 0.23, 0.05], 'Q2-y=15, z-pT=2': [0.28, 0.22, 0.33, 0.23], 'Q2-y=15, z-pT=3': [0.28, 0.22, 0.47, 0.33], 'Q2-y=15, z-pT=4': [0.33, 0.28, 0.23, 0.05], 'Q2-y=15, z-pT=5': [0.33, 0.28, 0.33, 0.23], 'Q2-y=15, z-pT=6': [0.33, 0.28, 0.47, 0.33], 'Q2-y=15, z-pT=7': [0.4, 0.33, 0.23, 0.05], 'Q2-y=15, z-pT=8': [0.4, 0.33, 0.33, 0.23], 'Q2-y=15, z-pT=9': [0.4, 0.33, 0.47, 0.33], 'Q2-y=15, z-pT=10': [0.51, 0.4, 0.23, 0.05], 'Q2-y=15, z-pT=11': [0.51, 0.4, 0.33, 0.23], 'Q2-y=15, z-pT=30 - REMOVE, MIGRATION BIN': [0.51, 0.4, 0.47, 0.33], 'Q2-y=15, z-pT=12, MIGRATION BIN': [0.22, 0, 0.05, 0], 'Q2-y=15, z-pT=13, MIGRATION BIN': [0.22, 0, 0.05, 0.23], 'Q2-y=15, z-pT=14, MIGRATION BIN': [0.22, 0, 0.23, 0.33], 'Q2-y=15, z-pT=15, MIGRATION BIN': [0.22, 0, 0.33, 0.47], 'Q2-y=15, z-pT=16, MIGRATION BIN': [0.22, 0, 10, 0.47], 'Q2-y=15, z-pT=17, MIGRATION BIN': [0.22, 0.28, 0.05, 0], 'Q2-y=15, z-pT=18, MIGRATION BIN': [0.22, 0.28, 10, 0.47], 'Q2-y=15, z-pT=19, MIGRATION BIN': [0.28, 0.33, 0.05, 0], 'Q2-y=15, z-pT=20, MIGRATION BIN': [0.28, 0.33, 10, 0.47], 'Q2-y=15, z-pT=21, MIGRATION BIN': [0.33, 0.4, 0.05, 0], 'Q2-y=15, z-pT=22, MIGRATION BIN': [0.33, 0.4, 10, 0.47], 'Q2-y=15, z-pT=23, MIGRATION BIN': [0.4, 0.51, 0.05, 0], 'Q2-y=15, z-pT=24, MIGRATION BIN': [0.4, 0.51, 10, 0.47], 'Q2-y=15, z-pT=25, MIGRATION BIN': [10, 0.51, 0, 0.05], 'Q2-y=15, z-pT=26, MIGRATION BIN': [10, 0.51, 0.05, 0.23], 'Q2-y=15, z-pT=27, MIGRATION BIN': [10, 0.51, 0.23, 0.33], 'Q2-y=15, z-pT=28, MIGRATION BIN': [10, 0.51, 0.33, 0.47], 'Q2-y=15, z-pT=29, MIGRATION BIN': [10, 0.51, 10, 0.47], 'Q2-y=16, z-pT=1': [0.2, 0.16, 0.22, 0.05], 'Q2-y=16, z-pT=2': [0.2, 0.16, 0.31, 0.22], 'Q2-y=16, z-pT=3': [0.2, 0.16, 0.44, 0.31], 'Q2-y=16, z-pT=46 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.7, 0.44], 'Q2-y=16, z-pT=4': [0.24, 0.2, 0.22, 0.05], 'Q2-y=16, z-pT=5': [0.24, 0.2, 0.31, 0.22], 'Q2-y=16, z-pT=6': [0.24, 0.2, 0.44, 0.31], 'Q2-y=16, z-pT=47 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.7, 0.44], 'Q2-y=16, z-pT=7': [0.29, 0.24, 0.22, 0.05], 'Q2-y=16, z-pT=8': [0.29, 0.24, 0.31, 0.22], 'Q2-y=16, z-pT=9': [0.29, 0.24, 0.44, 0.31], 'Q2-y=16, z-pT=10': [0.29, 0.24, 0.7, 0.44], 'Q2-y=16, z-pT=11': [0.36, 0.29, 0.22, 0.05], 'Q2-y=16, z-pT=12': [0.36, 0.29, 0.31, 0.22], 'Q2-y=16, z-pT=13': [0.36, 0.29, 0.44, 0.31], 'Q2-y=16, z-pT=14': [0.36, 0.29, 0.7, 0.44], 'Q2-y=16, z-pT=15': [0.45, 0.36, 0.22, 0.05], 'Q2-y=16, z-pT=16': [0.45, 0.36, 0.31, 0.22], 'Q2-y=16, z-pT=17': [0.45, 0.36, 0.44, 0.31], 'Q2-y=16, z-pT=18': [0.45, 0.36, 0.7, 0.44], 'Q2-y=16, z-pT=19': [0.62, 0.45, 0.22, 0.05], 'Q2-y=16, z-pT=20': [0.62, 0.45, 0.31, 0.22], 'Q2-y=16, z-pT=21': [0.62, 0.45, 0.44, 0.31], 'Q2-y=16, z-pT=48 - REMOVE, MIGRATION BIN': [0.62, 0.45, 0.7, 0.44], 'Q2-y=16, z-pT=22, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=16, z-pT=23, MIGRATION BIN': [0.16, 0, 0.05, 0.22], 'Q2-y=16, z-pT=24, MIGRATION BIN': [0.16, 0, 0.22, 0.31], 'Q2-y=16, z-pT=25, MIGRATION BIN': [0.16, 0, 0.31, 0.44], 'Q2-y=16, z-pT=26, MIGRATION BIN': [0.16, 0, 0.44, 0.7], 'Q2-y=16, z-pT=27, MIGRATION BIN': [0.16, 0, 10, 0.7], 'Q2-y=16, z-pT=28, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=16, z-pT=29, MIGRATION BIN': [0.16, 0.2, 10, 0.7], 'Q2-y=16, z-pT=30, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=16, z-pT=31, MIGRATION BIN': [0.2, 0.24, 10, 0.7], 'Q2-y=16, z-pT=32, MIGRATION BIN': [0.24, 0.29, 0.05, 0], 'Q2-y=16, z-pT=33, MIGRATION BIN': [0.24, 0.29, 10, 0.7], 'Q2-y=16, z-pT=34, MIGRATION BIN': [0.29, 0.36, 0.05, 0], 'Q2-y=16, z-pT=35, MIGRATION BIN': [0.29, 0.36, 10, 0.7], 'Q2-y=16, z-pT=36, MIGRATION BIN': [0.36, 0.45, 0.05, 0], 'Q2-y=16, z-pT=37, MIGRATION BIN': [0.36, 0.45, 10, 0.7], 'Q2-y=16, z-pT=38, MIGRATION BIN': [0.45, 0.62, 0.05, 0], 'Q2-y=16, z-pT=39, MIGRATION BIN': [0.45, 0.62, 10, 0.7], 'Q2-y=16, z-pT=40, MIGRATION BIN': [10, 0.62, 0, 0.05], 'Q2-y=16, z-pT=41, MIGRATION BIN': [10, 0.62, 0.05, 0.22], 'Q2-y=16, z-pT=42, MIGRATION BIN': [10, 0.62, 0.22, 0.31], 'Q2-y=16, z-pT=43, MIGRATION BIN': [10, 0.62, 0.31, 0.44], 'Q2-y=16, z-pT=44, MIGRATION BIN': [10, 0.62, 0.44, 0.7], 'Q2-y=16, z-pT=45, MIGRATION BIN': [10, 0.62, 10, 0.7], 'Q2-y=17, z-pT=1': [0.23, 0.19, 0.19, 0.05], 'Q2-y=17, z-pT=2': [0.23, 0.19, 0.28, 0.19], 'Q2-y=17, z-pT=3': [0.23, 0.19, 0.37, 0.28], 'Q2-y=17, z-pT=4': [0.29, 0.23, 0.19, 0.05], 'Q2-y=17, z-pT=5': [0.29, 0.23, 0.28, 0.19], 'Q2-y=17, z-pT=6': [0.29, 0.23, 0.37, 0.28], 'Q2-y=17, z-pT=7': [0.35, 0.29, 0.19, 0.05], 'Q2-y=17, z-pT=8': [0.35, 0.29, 0.28, 0.19], 'Q2-y=17, z-pT=9': [0.35, 0.29, 0.37, 0.28], 'Q2-y=17, z-pT=10': [0.45, 0.35, 0.19, 0.05], 'Q2-y=17, z-pT=29 - REMOVE, MIGRATION BIN': [0.45, 0.35, 0.28, 0.19], 'Q2-y=17, z-pT=30 - REMOVE, MIGRATION BIN': [0.45, 0.35, 0.37, 0.28], 'Q2-y=17, z-pT=11, MIGRATION BIN': [0.19, 0, 0.05, 0], 'Q2-y=17, z-pT=12, MIGRATION BIN': [0.19, 0, 0.05, 0.19], 'Q2-y=17, z-pT=13, MIGRATION BIN': [0.19, 0, 0.19, 0.28], 'Q2-y=17, z-pT=14, MIGRATION BIN': [0.19, 0, 0.28, 0.37], 'Q2-y=17, z-pT=15, MIGRATION BIN': [0.19, 0, 10, 0.37], 'Q2-y=17, z-pT=16, MIGRATION BIN': [0.19, 0.23, 0.05, 0], 'Q2-y=17, z-pT=17, MIGRATION BIN': [0.19, 0.23, 10, 0.37], 'Q2-y=17, z-pT=18, MIGRATION BIN': [0.23, 0.29, 0.05, 0], 'Q2-y=17, z-pT=19, MIGRATION BIN': [0.23, 0.29, 10, 0.37], 'Q2-y=17, z-pT=20, MIGRATION BIN': [0.29, 0.35, 0.05, 0], 'Q2-y=17, z-pT=21, MIGRATION BIN': [0.29, 0.35, 10, 0.37], 'Q2-y=17, z-pT=22, MIGRATION BIN': [0.35, 0.45, 0.05, 0], 'Q2-y=17, z-pT=23, MIGRATION BIN': [0.35, 0.45, 10, 0.37], 'Q2-y=17, z-pT=24, MIGRATION BIN': [10, 0.45, 0, 0.05], 'Q2-y=17, z-pT=25, MIGRATION BIN': [10, 0.45, 0.05, 0.19], 'Q2-y=17, z-pT=26, MIGRATION BIN': [10, 0.45, 0.19, 0.28], 'Q2-y=17, z-pT=27, MIGRATION BIN': [10, 0.45, 0.28, 0.37], 'Q2-y=17, z-pT=28, MIGRATION BIN': [10, 0.45, 10, 0.37]}
Bin_Definition_Array = {'Q2-y=1, z-pT=1': [0.2, 0.16, 0.2, 0.05], 'Q2-y=1, z-pT=2': [0.2, 0.16, 0.3, 0.2], 'Q2-y=1, z-pT=3': [0.2, 0.16, 0.4, 0.3], 'Q2-y=1, z-pT=4': [0.2, 0.16, 0.5, 0.4], 'Q2-y=1, z-pT=58 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.6, 0.5], 'Q2-y=1, z-pT=59 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.75, 0.6], 'Q2-y=1, z-pT=60 - REMOVE, MIGRATION BIN': [0.2, 0.16, 1.0, 0.75], 'Q2-y=1, z-pT=5': [0.24, 0.2, 0.2, 0.05], 'Q2-y=1, z-pT=6': [0.24, 0.2, 0.3, 0.2], 'Q2-y=1, z-pT=7': [0.24, 0.2, 0.4, 0.3], 'Q2-y=1, z-pT=8': [0.24, 0.2, 0.5, 0.4], 'Q2-y=1, z-pT=9': [0.24, 0.2, 0.6, 0.5], 'Q2-y=1, z-pT=61 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.75, 0.6], 'Q2-y=1, z-pT=62 - REMOVE, MIGRATION BIN': [0.24, 0.2, 1.0, 0.75], 'Q2-y=1, z-pT=10': [0.31, 0.24, 0.2, 0.05], 'Q2-y=1, z-pT=11': [0.31, 0.24, 0.3, 0.2], 'Q2-y=1, z-pT=12': [0.31, 0.24, 0.4, 0.3], 'Q2-y=1, z-pT=13': [0.31, 0.24, 0.5, 0.4], 'Q2-y=1, z-pT=14': [0.31, 0.24, 0.6, 0.5], 'Q2-y=1, z-pT=15': [0.31, 0.24, 0.75, 0.6], 'Q2-y=1, z-pT=63 - REMOVE, MIGRATION BIN': [0.31, 0.24, 1.0, 0.75], 'Q2-y=1, z-pT=16': [0.41, 0.31, 0.2, 0.05], 'Q2-y=1, z-pT=17': [0.41, 0.31, 0.3, 0.2], 'Q2-y=1, z-pT=18': [0.41, 0.31, 0.4, 0.3], 'Q2-y=1, z-pT=19': [0.41, 0.31, 0.5, 0.4], 'Q2-y=1, z-pT=20': [0.41, 0.31, 0.6, 0.5], 'Q2-y=1, z-pT=21': [0.41, 0.31, 0.75, 0.6], 'Q2-y=1, z-pT=22': [0.41, 0.31, 1.0, 0.75], 'Q2-y=1, z-pT=23': [0.7, 0.41, 0.2, 0.05], 'Q2-y=1, z-pT=24': [0.7, 0.41, 0.3, 0.2], 'Q2-y=1, z-pT=25': [0.7, 0.41, 0.4, 0.3], 'Q2-y=1, z-pT=26': [0.7, 0.41, 0.5, 0.4], 'Q2-y=1, z-pT=27': [0.7, 0.41, 0.6, 0.5], 'Q2-y=1, z-pT=28': [0.7, 0.41, 0.75, 0.6], 'Q2-y=1, z-pT=29': [0.7, 0.41, 1.0, 0.75], 'Q2-y=1, z-pT=30, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=1, z-pT=31, MIGRATION BIN': [0.16, 0, 0.05, 0.2], 'Q2-y=1, z-pT=32, MIGRATION BIN': [0.16, 0, 0.2, 0.3], 'Q2-y=1, z-pT=33, MIGRATION BIN': [0.16, 0, 0.3, 0.4], 'Q2-y=1, z-pT=34, MIGRATION BIN': [0.16, 0, 0.4, 0.5], 'Q2-y=1, z-pT=35, MIGRATION BIN': [0.16, 0, 0.5, 0.6], 'Q2-y=1, z-pT=36, MIGRATION BIN': [0.16, 0, 0.6, 0.75], 'Q2-y=1, z-pT=37, MIGRATION BIN': [0.16, 0, 0.75, 1.0], 'Q2-y=1, z-pT=38, MIGRATION BIN': [0.16, 0, 1.2, 1.0], 'Q2-y=1, z-pT=39, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=1, z-pT=40, MIGRATION BIN': [0.16, 0.2, 1.2, 1.0], 'Q2-y=1, z-pT=41, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=1, z-pT=42, MIGRATION BIN': [0.2, 0.24, 1.2, 1.0], 'Q2-y=1, z-pT=43, MIGRATION BIN': [0.24, 0.31, 0.05, 0], 'Q2-y=1, z-pT=44, MIGRATION BIN': [0.24, 0.31, 1.2, 1.0], 'Q2-y=1, z-pT=45, MIGRATION BIN': [0.31, 0.41, 0.05, 0], 'Q2-y=1, z-pT=46, MIGRATION BIN': [0.31, 0.41, 1.2, 1.0], 'Q2-y=1, z-pT=47, MIGRATION BIN': [0.41, 0.7, 0.05, 0], 'Q2-y=1, z-pT=48, MIGRATION BIN': [0.41, 0.7, 1.2, 1.0], 'Q2-y=1, z-pT=49, MIGRATION BIN': [1.2, 0.7, 0, 0.05], 'Q2-y=1, z-pT=50, MIGRATION BIN': [1.2, 0.7, 0.05, 0.2], 'Q2-y=1, z-pT=51, MIGRATION BIN': [1.2, 0.7, 0.2, 0.3], 'Q2-y=1, z-pT=52, MIGRATION BIN': [1.2, 0.7, 0.3, 0.4], 'Q2-y=1, z-pT=53, MIGRATION BIN': [1.2, 0.7, 0.4, 0.5], 'Q2-y=1, z-pT=54, MIGRATION BIN': [1.2, 0.7, 0.5, 0.6], 'Q2-y=1, z-pT=55, MIGRATION BIN': [1.2, 0.7, 0.6, 0.75], 'Q2-y=1, z-pT=56, MIGRATION BIN': [1.2, 0.7, 0.75, 1.0], 'Q2-y=1, z-pT=57, MIGRATION BIN': [1.2, 0.7, 1.2, 1.0], 'Q2-y=2, z-pT=1': [0.23, 0.19, 0.25, 0.05], 'Q2-y=2, z-pT=2': [0.23, 0.19, 0.35, 0.25], 'Q2-y=2, z-pT=3': [0.23, 0.19, 0.45, 0.35], 'Q2-y=2, z-pT=4': [0.23, 0.19, 0.54, 0.45], 'Q2-y=2, z-pT=60 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.67, 0.54], 'Q2-y=2, z-pT=61 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.93, 0.67], 'Q2-y=2, z-pT=5': [0.26, 0.23, 0.25, 0.05], 'Q2-y=2, z-pT=6': [0.26, 0.23, 0.35, 0.25], 'Q2-y=2, z-pT=7': [0.26, 0.23, 0.45, 0.35], 'Q2-y=2, z-pT=8': [0.26, 0.23, 0.54, 0.45], 'Q2-y=2, z-pT=9': [0.26, 0.23, 0.67, 0.54], 'Q2-y=2, z-pT=62 - REMOVE, MIGRATION BIN': [0.26, 0.23, 0.93, 0.67], 'Q2-y=2, z-pT=10': [0.31, 0.26, 0.25, 0.05], 'Q2-y=2, z-pT=11': [0.31, 0.26, 0.35, 0.25], 'Q2-y=2, z-pT=12': [0.31, 0.26, 0.45, 0.35], 'Q2-y=2, z-pT=13': [0.31, 0.26, 0.54, 0.45], 'Q2-y=2, z-pT=14': [0.31, 0.26, 0.67, 0.54], 'Q2-y=2, z-pT=63 - REMOVE, MIGRATION BIN': [0.31, 0.26, 0.93, 0.67], 'Q2-y=2, z-pT=15': [0.38, 0.31, 0.25, 0.05], 'Q2-y=2, z-pT=16': [0.38, 0.31, 0.35, 0.25], 'Q2-y=2, z-pT=17': [0.38, 0.31, 0.45, 0.35], 'Q2-y=2, z-pT=18': [0.38, 0.31, 0.54, 0.45], 'Q2-y=2, z-pT=19': [0.38, 0.31, 0.67, 0.54], 'Q2-y=2, z-pT=20': [0.38, 0.31, 0.93, 0.67], 'Q2-y=2, z-pT=21': [0.5, 0.38, 0.25, 0.05], 'Q2-y=2, z-pT=22': [0.5, 0.38, 0.35, 0.25], 'Q2-y=2, z-pT=23': [0.5, 0.38, 0.45, 0.35], 'Q2-y=2, z-pT=24': [0.5, 0.38, 0.54, 0.45], 'Q2-y=2, z-pT=25': [0.5, 0.38, 0.67, 0.54], 'Q2-y=2, z-pT=26': [0.5, 0.38, 0.93, 0.67], 'Q2-y=2, z-pT=27': [0.75, 0.5, 0.25, 0.05], 'Q2-y=2, z-pT=28': [0.75, 0.5, 0.35, 0.25], 'Q2-y=2, z-pT=29': [0.75, 0.5, 0.45, 0.35], 'Q2-y=2, z-pT=30': [0.75, 0.5, 0.54, 0.45], 'Q2-y=2, z-pT=31': [0.75, 0.5, 0.67, 0.54], 'Q2-y=2, z-pT=64 - REMOVE, MIGRATION BIN': [0.75, 0.5, 0.93, 0.67], 'Q2-y=2, z-pT=32, MIGRATION BIN': [0.19, 0, 0.05, 0], 'Q2-y=2, z-pT=33, MIGRATION BIN': [0.19, 0, 0.05, 0.25], 'Q2-y=2, z-pT=34, MIGRATION BIN': [0.19, 0, 0.25, 0.35], 'Q2-y=2, z-pT=35, MIGRATION BIN': [0.19, 0, 0.35, 0.45], 'Q2-y=2, z-pT=36, MIGRATION BIN': [0.19, 0, 0.45, 0.54], 'Q2-y=2, z-pT=37, MIGRATION BIN': [0.19, 0, 0.54, 0.67], 'Q2-y=2, z-pT=38, MIGRATION BIN': [0.19, 0, 0.67, 0.93], 'Q2-y=2, z-pT=39, MIGRATION BIN': [0.19, 0, 1.2, 0.93], 'Q2-y=2, z-pT=40, MIGRATION BIN': [0.19, 0.23, 0.05, 0], 'Q2-y=2, z-pT=41, MIGRATION BIN': [0.19, 0.23, 1.2, 0.93], 'Q2-y=2, z-pT=42, MIGRATION BIN': [0.23, 0.26, 0.05, 0], 'Q2-y=2, z-pT=43, MIGRATION BIN': [0.23, 0.26, 1.2, 0.93], 'Q2-y=2, z-pT=44, MIGRATION BIN': [0.26, 0.31, 0.05, 0], 'Q2-y=2, z-pT=45, MIGRATION BIN': [0.26, 0.31, 1.2, 0.93], 'Q2-y=2, z-pT=46, MIGRATION BIN': [0.31, 0.38, 0.05, 0], 'Q2-y=2, z-pT=47, MIGRATION BIN': [0.31, 0.38, 1.2, 0.93], 'Q2-y=2, z-pT=48, MIGRATION BIN': [0.38, 0.5, 0.05, 0], 'Q2-y=2, z-pT=49, MIGRATION BIN': [0.38, 0.5, 1.2, 0.93], 'Q2-y=2, z-pT=50, MIGRATION BIN': [0.5, 0.75, 0.05, 0], 'Q2-y=2, z-pT=51, MIGRATION BIN': [0.5, 0.75, 1.2, 0.93], 'Q2-y=2, z-pT=52, MIGRATION BIN': [1.2, 0.75, 0, 0.05], 'Q2-y=2, z-pT=53, MIGRATION BIN': [1.2, 0.75, 0.05, 0.25], 'Q2-y=2, z-pT=54, MIGRATION BIN': [1.2, 0.75, 0.25, 0.35], 'Q2-y=2, z-pT=55, MIGRATION BIN': [1.2, 0.75, 0.35, 0.45], 'Q2-y=2, z-pT=56, MIGRATION BIN': [1.2, 0.75, 0.45, 0.54], 'Q2-y=2, z-pT=57, MIGRATION BIN': [1.2, 0.75, 0.54, 0.67], 'Q2-y=2, z-pT=58, MIGRATION BIN': [1.2, 0.75, 0.67, 0.93], 'Q2-y=2, z-pT=59, MIGRATION BIN': [1.2, 0.75, 1.2, 0.93], 'Q2-y=3, z-pT=1': [0.28, 0.22, 0.2, 0.05], 'Q2-y=3, z-pT=2': [0.28, 0.22, 0.3, 0.2], 'Q2-y=3, z-pT=3': [0.28, 0.22, 0.4, 0.3], 'Q2-y=3, z-pT=4': [0.28, 0.22, 0.5, 0.4], 'Q2-y=3, z-pT=5': [0.28, 0.22, 0.6, 0.5], 'Q2-y=3, z-pT=47 - REMOVE, MIGRATION BIN': [0.28, 0.22, 0.75, 0.6], 'Q2-y=3, z-pT=6': [0.35, 0.28, 0.2, 0.05], 'Q2-y=3, z-pT=7': [0.35, 0.28, 0.3, 0.2], 'Q2-y=3, z-pT=8': [0.35, 0.28, 0.4, 0.3], 'Q2-y=3, z-pT=9': [0.35, 0.28, 0.5, 0.4], 'Q2-y=3, z-pT=10': [0.35, 0.28, 0.6, 0.5], 'Q2-y=3, z-pT=11': [0.35, 0.28, 0.75, 0.6], 'Q2-y=3, z-pT=12': [0.45, 0.35, 0.2, 0.05], 'Q2-y=3, z-pT=13': [0.45, 0.35, 0.3, 0.2], 'Q2-y=3, z-pT=14': [0.45, 0.35, 0.4, 0.3], 'Q2-y=3, z-pT=15': [0.45, 0.35, 0.5, 0.4], 'Q2-y=3, z-pT=16': [0.45, 0.35, 0.6, 0.5], 'Q2-y=3, z-pT=17': [0.45, 0.35, 0.75, 0.6], 'Q2-y=3, z-pT=18': [0.7, 0.45, 0.2, 0.05], 'Q2-y=3, z-pT=19': [0.7, 0.45, 0.3, 0.2], 'Q2-y=3, z-pT=20': [0.7, 0.45, 0.4, 0.3], 'Q2-y=3, z-pT=21': [0.7, 0.45, 0.5, 0.4], 'Q2-y=3, z-pT=22': [0.7, 0.45, 0.6, 0.5], 'Q2-y=3, z-pT=48 - REMOVE, MIGRATION BIN': [0.7, 0.45, 0.75, 0.6], 'Q2-y=3, z-pT=23, MIGRATION BIN': [0.22, 0, 0.05, 0], 'Q2-y=3, z-pT=24, MIGRATION BIN': [0.22, 0, 0.05, 0.2], 'Q2-y=3, z-pT=25, MIGRATION BIN': [0.22, 0, 0.2, 0.3], 'Q2-y=3, z-pT=26, MIGRATION BIN': [0.22, 0, 0.3, 0.4], 'Q2-y=3, z-pT=27, MIGRATION BIN': [0.22, 0, 0.4, 0.5], 'Q2-y=3, z-pT=28, MIGRATION BIN': [0.22, 0, 0.5, 0.6], 'Q2-y=3, z-pT=29, MIGRATION BIN': [0.22, 0, 0.6, 0.75], 'Q2-y=3, z-pT=30, MIGRATION BIN': [0.22, 0, 1.2, 0.75], 'Q2-y=3, z-pT=31, MIGRATION BIN': [0.22, 0.28, 0.05, 0], 'Q2-y=3, z-pT=32, MIGRATION BIN': [0.22, 0.28, 1.2, 0.75], 'Q2-y=3, z-pT=33, MIGRATION BIN': [0.28, 0.35, 0.05, 0], 'Q2-y=3, z-pT=34, MIGRATION BIN': [0.28, 0.35, 1.2, 0.75], 'Q2-y=3, z-pT=35, MIGRATION BIN': [0.35, 0.45, 0.05, 0], 'Q2-y=3, z-pT=36, MIGRATION BIN': [0.35, 0.45, 1.2, 0.75], 'Q2-y=3, z-pT=37, MIGRATION BIN': [0.45, 0.7, 0.05, 0], 'Q2-y=3, z-pT=38, MIGRATION BIN': [0.45, 0.7, 1.2, 0.75], 'Q2-y=3, z-pT=39, MIGRATION BIN': [1.2, 0.7, 0, 0.05], 'Q2-y=3, z-pT=40, MIGRATION BIN': [1.2, 0.7, 0.05, 0.2], 'Q2-y=3, z-pT=41, MIGRATION BIN': [1.2, 0.7, 0.2, 0.3], 'Q2-y=3, z-pT=42, MIGRATION BIN': [1.2, 0.7, 0.3, 0.4], 'Q2-y=3, z-pT=43, MIGRATION BIN': [1.2, 0.7, 0.4, 0.5], 'Q2-y=3, z-pT=44, MIGRATION BIN': [1.2, 0.7, 0.5, 0.6], 'Q2-y=3, z-pT=45, MIGRATION BIN': [1.2, 0.7, 0.6, 0.75], 'Q2-y=3, z-pT=46, MIGRATION BIN': [1.2, 0.7, 1.2, 0.75], 'Q2-y=4, z-pT=1': [0.34, 0.26, 0.2, 0.05], 'Q2-y=4, z-pT=2': [0.34, 0.26, 0.29, 0.2], 'Q2-y=4, z-pT=3': [0.34, 0.26, 0.38, 0.29], 'Q2-y=4, z-pT=4': [0.34, 0.26, 0.48, 0.38], 'Q2-y=4, z-pT=5': [0.34, 0.26, 0.61, 0.48], 'Q2-y=4, z-pT=6': [0.38, 0.34, 0.2, 0.05], 'Q2-y=4, z-pT=7': [0.38, 0.34, 0.29, 0.2], 'Q2-y=4, z-pT=8': [0.38, 0.34, 0.38, 0.29], 'Q2-y=4, z-pT=9': [0.38, 0.34, 0.48, 0.38], 'Q2-y=4, z-pT=10': [0.38, 0.34, 0.61, 0.48], 'Q2-y=4, z-pT=11': [0.43, 0.38, 0.2, 0.05], 'Q2-y=4, z-pT=12': [0.43, 0.38, 0.29, 0.2], 'Q2-y=4, z-pT=13': [0.43, 0.38, 0.38, 0.29], 'Q2-y=4, z-pT=14': [0.43, 0.38, 0.48, 0.38], 'Q2-y=4, z-pT=15': [0.43, 0.38, 0.61, 0.48], 'Q2-y=4, z-pT=16': [0.5, 0.43, 0.2, 0.05], 'Q2-y=4, z-pT=17': [0.5, 0.43, 0.29, 0.2], 'Q2-y=4, z-pT=18': [0.5, 0.43, 0.38, 0.29], 'Q2-y=4, z-pT=19': [0.5, 0.43, 0.48, 0.38], 'Q2-y=4, z-pT=20': [0.5, 0.43, 0.61, 0.48], 'Q2-y=4, z-pT=21': [0.6, 0.5, 0.2, 0.05], 'Q2-y=4, z-pT=22': [0.6, 0.5, 0.29, 0.2], 'Q2-y=4, z-pT=23': [0.6, 0.5, 0.38, 0.29], 'Q2-y=4, z-pT=24': [0.6, 0.5, 0.48, 0.38], 'Q2-y=4, z-pT=49 - REMOVE, MIGRATION BIN': [0.6, 0.5, 0.61, 0.48], 'Q2-y=4, z-pT=25, MIGRATION BIN': [0.26, 0, 0.05, 0], 'Q2-y=4, z-pT=26, MIGRATION BIN': [0.26, 0, 0.05, 0.2], 'Q2-y=4, z-pT=27, MIGRATION BIN': [0.26, 0, 0.2, 0.29], 'Q2-y=4, z-pT=28, MIGRATION BIN': [0.26, 0, 0.29, 0.38], 'Q2-y=4, z-pT=29, MIGRATION BIN': [0.26, 0, 0.38, 0.48], 'Q2-y=4, z-pT=30, MIGRATION BIN': [0.26, 0, 0.48, 0.61], 'Q2-y=4, z-pT=31, MIGRATION BIN': [0.26, 0, 1.2, 0.61], 'Q2-y=4, z-pT=32, MIGRATION BIN': [0.26, 0.34, 0.05, 0], 'Q2-y=4, z-pT=33, MIGRATION BIN': [0.26, 0.34, 1.2, 0.61], 'Q2-y=4, z-pT=34, MIGRATION BIN': [0.34, 0.38, 0.05, 0], 'Q2-y=4, z-pT=35, MIGRATION BIN': [0.34, 0.38, 1.2, 0.61], 'Q2-y=4, z-pT=36, MIGRATION BIN': [0.38, 0.43, 0.05, 0], 'Q2-y=4, z-pT=37, MIGRATION BIN': [0.38, 0.43, 1.2, 0.61], 'Q2-y=4, z-pT=38, MIGRATION BIN': [0.43, 0.5, 0.05, 0], 'Q2-y=4, z-pT=39, MIGRATION BIN': [0.43, 0.5, 1.2, 0.61], 'Q2-y=4, z-pT=40, MIGRATION BIN': [0.5, 0.6, 0.05, 0], 'Q2-y=4, z-pT=41, MIGRATION BIN': [0.5, 0.6, 1.2, 0.61], 'Q2-y=4, z-pT=42, MIGRATION BIN': [1.2, 0.6, 0, 0.05], 'Q2-y=4, z-pT=43, MIGRATION BIN': [1.2, 0.6, 0.05, 0.2], 'Q2-y=4, z-pT=44, MIGRATION BIN': [1.2, 0.6, 0.2, 0.29], 'Q2-y=4, z-pT=45, MIGRATION BIN': [1.2, 0.6, 0.29, 0.38], 'Q2-y=4, z-pT=46, MIGRATION BIN': [1.2, 0.6, 0.38, 0.48], 'Q2-y=4, z-pT=47, MIGRATION BIN': [1.2, 0.6, 0.48, 0.61], 'Q2-y=4, z-pT=48, MIGRATION BIN': [1.2, 0.6, 1.2, 0.61], 'Q2-y=5, z-pT=1': [0.2, 0.16, 0.22, 0.05], 'Q2-y=5, z-pT=2': [0.2, 0.16, 0.32, 0.22], 'Q2-y=5, z-pT=3': [0.2, 0.16, 0.41, 0.32], 'Q2-y=5, z-pT=4': [0.2, 0.16, 0.51, 0.41], 'Q2-y=5, z-pT=61 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.65, 0.51], 'Q2-y=5, z-pT=62 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.98, 0.65], 'Q2-y=5, z-pT=5': [0.24, 0.2, 0.22, 0.05], 'Q2-y=5, z-pT=6': [0.24, 0.2, 0.32, 0.22], 'Q2-y=5, z-pT=7': [0.24, 0.2, 0.41, 0.32], 'Q2-y=5, z-pT=8': [0.24, 0.2, 0.51, 0.41], 'Q2-y=5, z-pT=9': [0.24, 0.2, 0.65, 0.51], 'Q2-y=5, z-pT=63 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.98, 0.65], 'Q2-y=5, z-pT=10': [0.3, 0.24, 0.22, 0.05], 'Q2-y=5, z-pT=11': [0.3, 0.24, 0.32, 0.22], 'Q2-y=5, z-pT=12': [0.3, 0.24, 0.41, 0.32], 'Q2-y=5, z-pT=13': [0.3, 0.24, 0.51, 0.41], 'Q2-y=5, z-pT=14': [0.3, 0.24, 0.65, 0.51], 'Q2-y=5, z-pT=64 - REMOVE, MIGRATION BIN': [0.3, 0.24, 0.98, 0.65], 'Q2-y=5, z-pT=15': [0.38, 0.3, 0.22, 0.05], 'Q2-y=5, z-pT=16': [0.38, 0.3, 0.32, 0.22], 'Q2-y=5, z-pT=17': [0.38, 0.3, 0.41, 0.32], 'Q2-y=5, z-pT=18': [0.38, 0.3, 0.51, 0.41], 'Q2-y=5, z-pT=19': [0.38, 0.3, 0.65, 0.51], 'Q2-y=5, z-pT=20': [0.38, 0.3, 0.98, 0.65], 'Q2-y=5, z-pT=21': [0.49, 0.38, 0.22, 0.05], 'Q2-y=5, z-pT=22': [0.49, 0.38, 0.32, 0.22], 'Q2-y=5, z-pT=23': [0.49, 0.38, 0.41, 0.32], 'Q2-y=5, z-pT=24': [0.49, 0.38, 0.51, 0.41], 'Q2-y=5, z-pT=25': [0.49, 0.38, 0.65, 0.51], 'Q2-y=5, z-pT=26': [0.49, 0.38, 0.98, 0.65], 'Q2-y=5, z-pT=27': [0.72, 0.49, 0.22, 0.05], 'Q2-y=5, z-pT=28': [0.72, 0.49, 0.32, 0.22], 'Q2-y=5, z-pT=29': [0.72, 0.49, 0.41, 0.32], 'Q2-y=5, z-pT=30': [0.72, 0.49, 0.51, 0.41], 'Q2-y=5, z-pT=31': [0.72, 0.49, 0.65, 0.51], 'Q2-y=5, z-pT=32': [0.72, 0.49, 0.98, 0.65], 'Q2-y=5, z-pT=33, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=5, z-pT=34, MIGRATION BIN': [0.16, 0, 0.05, 0.22], 'Q2-y=5, z-pT=35, MIGRATION BIN': [0.16, 0, 0.22, 0.32], 'Q2-y=5, z-pT=36, MIGRATION BIN': [0.16, 0, 0.32, 0.41], 'Q2-y=5, z-pT=37, MIGRATION BIN': [0.16, 0, 0.41, 0.51], 'Q2-y=5, z-pT=38, MIGRATION BIN': [0.16, 0, 0.51, 0.65], 'Q2-y=5, z-pT=39, MIGRATION BIN': [0.16, 0, 0.65, 0.98], 'Q2-y=5, z-pT=40, MIGRATION BIN': [0.16, 0, 1.2, 0.98], 'Q2-y=5, z-pT=41, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=5, z-pT=42, MIGRATION BIN': [0.16, 0.2, 1.2, 0.98], 'Q2-y=5, z-pT=43, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=5, z-pT=44, MIGRATION BIN': [0.2, 0.24, 1.2, 0.98], 'Q2-y=5, z-pT=45, MIGRATION BIN': [0.24, 0.3, 0.05, 0], 'Q2-y=5, z-pT=46, MIGRATION BIN': [0.24, 0.3, 1.2, 0.98], 'Q2-y=5, z-pT=47, MIGRATION BIN': [0.3, 0.38, 0.05, 0], 'Q2-y=5, z-pT=48, MIGRATION BIN': [0.3, 0.38, 1.2, 0.98], 'Q2-y=5, z-pT=49, MIGRATION BIN': [0.38, 0.49, 0.05, 0], 'Q2-y=5, z-pT=50, MIGRATION BIN': [0.38, 0.49, 1.2, 0.98], 'Q2-y=5, z-pT=51, MIGRATION BIN': [0.49, 0.72, 0.05, 0], 'Q2-y=5, z-pT=52, MIGRATION BIN': [0.49, 0.72, 1.2, 0.98], 'Q2-y=5, z-pT=53, MIGRATION BIN': [1.2, 0.72, 0, 0.05], 'Q2-y=5, z-pT=54, MIGRATION BIN': [1.2, 0.72, 0.05, 0.22], 'Q2-y=5, z-pT=55, MIGRATION BIN': [1.2, 0.72, 0.22, 0.32], 'Q2-y=5, z-pT=56, MIGRATION BIN': [1.2, 0.72, 0.32, 0.41], 'Q2-y=5, z-pT=57, MIGRATION BIN': [1.2, 0.72, 0.41, 0.51], 'Q2-y=5, z-pT=58, MIGRATION BIN': [1.2, 0.72, 0.51, 0.65], 'Q2-y=5, z-pT=59, MIGRATION BIN': [1.2, 0.72, 0.65, 0.98], 'Q2-y=5, z-pT=60, MIGRATION BIN': [1.2, 0.72, 1.2, 0.98], 'Q2-y=6, z-pT=1': [0.23, 0.18, 0.22, 0.05], 'Q2-y=6, z-pT=2': [0.23, 0.18, 0.32, 0.22], 'Q2-y=6, z-pT=3': [0.23, 0.18, 0.41, 0.32], 'Q2-y=6, z-pT=4': [0.23, 0.18, 0.51, 0.41], 'Q2-y=6, z-pT=52 - REMOVE, MIGRATION BIN': [0.23, 0.18, 0.65, 0.51], 'Q2-y=6, z-pT=53 - REMOVE, MIGRATION BIN': [0.23, 0.18, 1.05, 0.65], 'Q2-y=6, z-pT=5': [0.28, 0.23, 0.22, 0.05], 'Q2-y=6, z-pT=6': [0.28, 0.23, 0.32, 0.22], 'Q2-y=6, z-pT=7': [0.28, 0.23, 0.41, 0.32], 'Q2-y=6, z-pT=8': [0.28, 0.23, 0.51, 0.41], 'Q2-y=6, z-pT=9': [0.28, 0.23, 0.65, 0.51], 'Q2-y=6, z-pT=54 - REMOVE, MIGRATION BIN': [0.28, 0.23, 1.05, 0.65], 'Q2-y=6, z-pT=10': [0.35, 0.28, 0.22, 0.05], 'Q2-y=6, z-pT=11': [0.35, 0.28, 0.32, 0.22], 'Q2-y=6, z-pT=12': [0.35, 0.28, 0.41, 0.32], 'Q2-y=6, z-pT=13': [0.35, 0.28, 0.51, 0.41], 'Q2-y=6, z-pT=14': [0.35, 0.28, 0.65, 0.51], 'Q2-y=6, z-pT=55 - REMOVE, MIGRATION BIN': [0.35, 0.28, 1.05, 0.65], 'Q2-y=6, z-pT=15': [0.45, 0.35, 0.22, 0.05], 'Q2-y=6, z-pT=16': [0.45, 0.35, 0.32, 0.22], 'Q2-y=6, z-pT=17': [0.45, 0.35, 0.41, 0.32], 'Q2-y=6, z-pT=18': [0.45, 0.35, 0.51, 0.41], 'Q2-y=6, z-pT=19': [0.45, 0.35, 0.65, 0.51], 'Q2-y=6, z-pT=20': [0.45, 0.35, 1.05, 0.65], 'Q2-y=6, z-pT=21': [0.75, 0.45, 0.22, 0.05], 'Q2-y=6, z-pT=22': [0.75, 0.45, 0.32, 0.22], 'Q2-y=6, z-pT=23': [0.75, 0.45, 0.41, 0.32], 'Q2-y=6, z-pT=24': [0.75, 0.45, 0.51, 0.41], 'Q2-y=6, z-pT=25': [0.75, 0.45, 0.65, 0.51], 'Q2-y=6, z-pT=56 - REMOVE, MIGRATION BIN': [0.75, 0.45, 1.05, 0.65], 'Q2-y=6, z-pT=26, MIGRATION BIN': [0.18, 0, 0.05, 0], 'Q2-y=6, z-pT=27, MIGRATION BIN': [0.18, 0, 0.05, 0.22], 'Q2-y=6, z-pT=28, MIGRATION BIN': [0.18, 0, 0.22, 0.32], 'Q2-y=6, z-pT=29, MIGRATION BIN': [0.18, 0, 0.32, 0.41], 'Q2-y=6, z-pT=30, MIGRATION BIN': [0.18, 0, 0.41, 0.51], 'Q2-y=6, z-pT=31, MIGRATION BIN': [0.18, 0, 0.51, 0.65], 'Q2-y=6, z-pT=32, MIGRATION BIN': [0.18, 0, 0.65, 1.05], 'Q2-y=6, z-pT=33, MIGRATION BIN': [0.18, 0, 1.2, 1.05], 'Q2-y=6, z-pT=34, MIGRATION BIN': [0.18, 0.23, 0.05, 0], 'Q2-y=6, z-pT=35, MIGRATION BIN': [0.18, 0.23, 1.2, 1.05], 'Q2-y=6, z-pT=36, MIGRATION BIN': [0.23, 0.28, 0.05, 0], 'Q2-y=6, z-pT=37, MIGRATION BIN': [0.23, 0.28, 1.2, 1.05], 'Q2-y=6, z-pT=38, MIGRATION BIN': [0.28, 0.35, 0.05, 0], 'Q2-y=6, z-pT=39, MIGRATION BIN': [0.28, 0.35, 1.2, 1.05], 'Q2-y=6, z-pT=40, MIGRATION BIN': [0.35, 0.45, 0.05, 0], 'Q2-y=6, z-pT=41, MIGRATION BIN': [0.35, 0.45, 1.2, 1.05], 'Q2-y=6, z-pT=42, MIGRATION BIN': [0.45, 0.75, 0.05, 0], 'Q2-y=6, z-pT=43, MIGRATION BIN': [0.45, 0.75, 1.2, 1.05], 'Q2-y=6, z-pT=44, MIGRATION BIN': [1.2, 0.75, 0, 0.05], 'Q2-y=6, z-pT=45, MIGRATION BIN': [1.2, 0.75, 0.05, 0.22], 'Q2-y=6, z-pT=46, MIGRATION BIN': [1.2, 0.75, 0.22, 0.32], 'Q2-y=6, z-pT=47, MIGRATION BIN': [1.2, 0.75, 0.32, 0.41], 'Q2-y=6, z-pT=48, MIGRATION BIN': [1.2, 0.75, 0.41, 0.51], 'Q2-y=6, z-pT=49, MIGRATION BIN': [1.2, 0.75, 0.51, 0.65], 'Q2-y=6, z-pT=50, MIGRATION BIN': [1.2, 0.75, 0.65, 1.05], 'Q2-y=6, z-pT=51, MIGRATION BIN': [1.2, 0.75, 1.2, 1.05], 'Q2-y=7, z-pT=1': [0.28, 0.22, 0.2, 0.05], 'Q2-y=7, z-pT=2': [0.28, 0.22, 0.29, 0.2], 'Q2-y=7, z-pT=3': [0.28, 0.22, 0.38, 0.29], 'Q2-y=7, z-pT=4': [0.28, 0.22, 0.48, 0.38], 'Q2-y=7, z-pT=5': [0.28, 0.22, 0.6, 0.48], 'Q2-y=7, z-pT=53 - REMOVE, MIGRATION BIN': [0.28, 0.22, 0.83, 0.6], 'Q2-y=7, z-pT=6': [0.33, 0.28, 0.2, 0.05], 'Q2-y=7, z-pT=7': [0.33, 0.28, 0.29, 0.2], 'Q2-y=7, z-pT=8': [0.33, 0.28, 0.38, 0.29], 'Q2-y=7, z-pT=9': [0.33, 0.28, 0.48, 0.38], 'Q2-y=7, z-pT=10': [0.33, 0.28, 0.6, 0.48], 'Q2-y=7, z-pT=54 - REMOVE, MIGRATION BIN': [0.33, 0.28, 0.83, 0.6], 'Q2-y=7, z-pT=11': [0.4, 0.33, 0.2, 0.05], 'Q2-y=7, z-pT=12': [0.4, 0.33, 0.29, 0.2], 'Q2-y=7, z-pT=13': [0.4, 0.33, 0.38, 0.29], 'Q2-y=7, z-pT=14': [0.4, 0.33, 0.48, 0.38], 'Q2-y=7, z-pT=15': [0.4, 0.33, 0.6, 0.48], 'Q2-y=7, z-pT=16': [0.4, 0.33, 0.83, 0.6], 'Q2-y=7, z-pT=17': [0.51, 0.4, 0.2, 0.05], 'Q2-y=7, z-pT=18': [0.51, 0.4, 0.29, 0.2], 'Q2-y=7, z-pT=19': [0.51, 0.4, 0.38, 0.29], 'Q2-y=7, z-pT=20': [0.51, 0.4, 0.48, 0.38], 'Q2-y=7, z-pT=21': [0.51, 0.4, 0.6, 0.48], 'Q2-y=7, z-pT=22': [0.51, 0.4, 0.83, 0.6], 'Q2-y=7, z-pT=23': [0.7, 0.51, 0.2, 0.05], 'Q2-y=7, z-pT=24': [0.7, 0.51, 0.29, 0.2], 'Q2-y=7, z-pT=25': [0.7, 0.51, 0.38, 0.29], 'Q2-y=7, z-pT=26': [0.7, 0.51, 0.48, 0.38], 'Q2-y=7, z-pT=55 - REMOVE, MIGRATION BIN': [0.7, 0.51, 0.6, 0.48], 'Q2-y=7, z-pT=56 - REMOVE, MIGRATION BIN': [0.7, 0.51, 0.83, 0.6], 'Q2-y=7, z-pT=27, MIGRATION BIN': [0.22, 0, 0.05, 0], 'Q2-y=7, z-pT=28, MIGRATION BIN': [0.22, 0, 0.05, 0.2], 'Q2-y=7, z-pT=29, MIGRATION BIN': [0.22, 0, 0.2, 0.29], 'Q2-y=7, z-pT=30, MIGRATION BIN': [0.22, 0, 0.29, 0.38], 'Q2-y=7, z-pT=31, MIGRATION BIN': [0.22, 0, 0.38, 0.48], 'Q2-y=7, z-pT=32, MIGRATION BIN': [0.22, 0, 0.48, 0.6], 'Q2-y=7, z-pT=33, MIGRATION BIN': [0.22, 0, 0.6, 0.83], 'Q2-y=7, z-pT=34, MIGRATION BIN': [0.22, 0, 1.2, 0.83], 'Q2-y=7, z-pT=35, MIGRATION BIN': [0.22, 0.28, 0.05, 0], 'Q2-y=7, z-pT=36, MIGRATION BIN': [0.22, 0.28, 1.2, 0.83], 'Q2-y=7, z-pT=37, MIGRATION BIN': [0.28, 0.33, 0.05, 0], 'Q2-y=7, z-pT=38, MIGRATION BIN': [0.28, 0.33, 1.2, 0.83], 'Q2-y=7, z-pT=39, MIGRATION BIN': [0.33, 0.4, 0.05, 0], 'Q2-y=7, z-pT=40, MIGRATION BIN': [0.33, 0.4, 1.2, 0.83], 'Q2-y=7, z-pT=41, MIGRATION BIN': [0.4, 0.51, 0.05, 0], 'Q2-y=7, z-pT=42, MIGRATION BIN': [0.4, 0.51, 1.2, 0.83], 'Q2-y=7, z-pT=43, MIGRATION BIN': [0.51, 0.7, 0.05, 0], 'Q2-y=7, z-pT=44, MIGRATION BIN': [0.51, 0.7, 1.2, 0.83], 'Q2-y=7, z-pT=45, MIGRATION BIN': [1.2, 0.7, 0, 0.05], 'Q2-y=7, z-pT=46, MIGRATION BIN': [1.2, 0.7, 0.05, 0.2], 'Q2-y=7, z-pT=47, MIGRATION BIN': [1.2, 0.7, 0.2, 0.29], 'Q2-y=7, z-pT=48, MIGRATION BIN': [1.2, 0.7, 0.29, 0.38], 'Q2-y=7, z-pT=49, MIGRATION BIN': [1.2, 0.7, 0.38, 0.48], 'Q2-y=7, z-pT=50, MIGRATION BIN': [1.2, 0.7, 0.48, 0.6], 'Q2-y=7, z-pT=51, MIGRATION BIN': [1.2, 0.7, 0.6, 0.83], 'Q2-y=7, z-pT=52, MIGRATION BIN': [1.2, 0.7, 1.2, 0.83], 'Q2-y=8, z-pT=1': [0.32, 0.27, 0.21, 0.05], 'Q2-y=8, z-pT=2': [0.32, 0.27, 0.31, 0.21], 'Q2-y=8, z-pT=3': [0.32, 0.27, 0.4, 0.31], 'Q2-y=8, z-pT=4': [0.32, 0.27, 0.5, 0.4], 'Q2-y=8, z-pT=5': [0.36, 0.32, 0.21, 0.05], 'Q2-y=8, z-pT=6': [0.36, 0.32, 0.31, 0.21], 'Q2-y=8, z-pT=7': [0.36, 0.32, 0.4, 0.31], 'Q2-y=8, z-pT=8': [0.36, 0.32, 0.5, 0.4], 'Q2-y=8, z-pT=9': [0.4, 0.36, 0.21, 0.05], 'Q2-y=8, z-pT=10': [0.4, 0.36, 0.31, 0.21], 'Q2-y=8, z-pT=11': [0.4, 0.36, 0.4, 0.31], 'Q2-y=8, z-pT=12': [0.4, 0.36, 0.5, 0.4], 'Q2-y=8, z-pT=13': [0.45, 0.4, 0.21, 0.05], 'Q2-y=8, z-pT=14': [0.45, 0.4, 0.31, 0.21], 'Q2-y=8, z-pT=15': [0.45, 0.4, 0.4, 0.31], 'Q2-y=8, z-pT=16': [0.45, 0.4, 0.5, 0.4], 'Q2-y=8, z-pT=17': [0.5, 0.45, 0.21, 0.05], 'Q2-y=8, z-pT=18': [0.5, 0.45, 0.31, 0.21], 'Q2-y=8, z-pT=19': [0.5, 0.45, 0.4, 0.31], 'Q2-y=8, z-pT=20': [0.5, 0.45, 0.5, 0.4], 'Q2-y=8, z-pT=21': [0.6, 0.5, 0.21, 0.05], 'Q2-y=8, z-pT=22': [0.6, 0.5, 0.31, 0.21], 'Q2-y=8, z-pT=47 - REMOVE, MIGRATION BIN': [0.6, 0.5, 0.4, 0.31], 'Q2-y=8, z-pT=48 - REMOVE, MIGRATION BIN': [0.6, 0.5, 0.5, 0.4], 'Q2-y=8, z-pT=23, MIGRATION BIN': [0.27, 0, 0.05, 0], 'Q2-y=8, z-pT=24, MIGRATION BIN': [0.27, 0, 0.05, 0.21], 'Q2-y=8, z-pT=25, MIGRATION BIN': [0.27, 0, 0.21, 0.31], 'Q2-y=8, z-pT=26, MIGRATION BIN': [0.27, 0, 0.31, 0.4], 'Q2-y=8, z-pT=27, MIGRATION BIN': [0.27, 0, 0.4, 0.5], 'Q2-y=8, z-pT=28, MIGRATION BIN': [0.27, 0, 1.2, 0.5], 'Q2-y=8, z-pT=29, MIGRATION BIN': [0.27, 0.32, 0.05, 0], 'Q2-y=8, z-pT=30, MIGRATION BIN': [0.27, 0.32, 1.2, 0.5], 'Q2-y=8, z-pT=31, MIGRATION BIN': [0.32, 0.36, 0.05, 0], 'Q2-y=8, z-pT=32, MIGRATION BIN': [0.32, 0.36, 1.2, 0.5], 'Q2-y=8, z-pT=33, MIGRATION BIN': [0.36, 0.4, 0.05, 0], 'Q2-y=8, z-pT=34, MIGRATION BIN': [0.36, 0.4, 1.2, 0.5], 'Q2-y=8, z-pT=35, MIGRATION BIN': [0.4, 0.45, 0.05, 0], 'Q2-y=8, z-pT=36, MIGRATION BIN': [0.4, 0.45, 1.2, 0.5], 'Q2-y=8, z-pT=37, MIGRATION BIN': [0.45, 0.5, 0.05, 0], 'Q2-y=8, z-pT=38, MIGRATION BIN': [0.45, 0.5, 1.2, 0.5], 'Q2-y=8, z-pT=39, MIGRATION BIN': [0.5, 0.6, 0.05, 0], 'Q2-y=8, z-pT=40, MIGRATION BIN': [0.5, 0.6, 1.2, 0.5], 'Q2-y=8, z-pT=41, MIGRATION BIN': [1.2, 0.6, 0, 0.05], 'Q2-y=8, z-pT=42, MIGRATION BIN': [1.2, 0.6, 0.05, 0.21], 'Q2-y=8, z-pT=43, MIGRATION BIN': [1.2, 0.6, 0.21, 0.31], 'Q2-y=8, z-pT=44, MIGRATION BIN': [1.2, 0.6, 0.31, 0.4], 'Q2-y=8, z-pT=45, MIGRATION BIN': [1.2, 0.6, 0.4, 0.5], 'Q2-y=8, z-pT=46, MIGRATION BIN': [1.2, 0.6, 1.2, 0.5], 'Q2-y=9, z-pT=1': [0.2, 0.16, 0.22, 0.05], 'Q2-y=9, z-pT=2': [0.2, 0.16, 0.3, 0.22], 'Q2-y=9, z-pT=3': [0.2, 0.16, 0.38, 0.3], 'Q2-y=9, z-pT=4': [0.2, 0.16, 0.46, 0.38], 'Q2-y=9, z-pT=5': [0.2, 0.16, 0.58, 0.46], 'Q2-y=9, z-pT=59 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.74, 0.58], 'Q2-y=9, z-pT=60 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.95, 0.74], 'Q2-y=9, z-pT=6': [0.24, 0.2, 0.22, 0.05], 'Q2-y=9, z-pT=7': [0.24, 0.2, 0.3, 0.22], 'Q2-y=9, z-pT=8': [0.24, 0.2, 0.38, 0.3], 'Q2-y=9, z-pT=9': [0.24, 0.2, 0.46, 0.38], 'Q2-y=9, z-pT=10': [0.24, 0.2, 0.58, 0.46], 'Q2-y=9, z-pT=61 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.74, 0.58], 'Q2-y=9, z-pT=62 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.95, 0.74], 'Q2-y=9, z-pT=11': [0.3, 0.24, 0.22, 0.05], 'Q2-y=9, z-pT=12': [0.3, 0.24, 0.3, 0.22], 'Q2-y=9, z-pT=13': [0.3, 0.24, 0.38, 0.3], 'Q2-y=9, z-pT=14': [0.3, 0.24, 0.46, 0.38], 'Q2-y=9, z-pT=15': [0.3, 0.24, 0.58, 0.46], 'Q2-y=9, z-pT=16': [0.3, 0.24, 0.74, 0.58], 'Q2-y=9, z-pT=63 - REMOVE, MIGRATION BIN': [0.3, 0.24, 0.95, 0.74], 'Q2-y=9, z-pT=17': [0.42, 0.3, 0.22, 0.05], 'Q2-y=9, z-pT=18': [0.42, 0.3, 0.3, 0.22], 'Q2-y=9, z-pT=19': [0.42, 0.3, 0.38, 0.3], 'Q2-y=9, z-pT=20': [0.42, 0.3, 0.46, 0.38], 'Q2-y=9, z-pT=21': [0.42, 0.3, 0.58, 0.46], 'Q2-y=9, z-pT=22': [0.42, 0.3, 0.74, 0.58], 'Q2-y=9, z-pT=23': [0.42, 0.3, 0.95, 0.74], 'Q2-y=9, z-pT=24': [0.7, 0.42, 0.22, 0.05], 'Q2-y=9, z-pT=25': [0.7, 0.42, 0.3, 0.22], 'Q2-y=9, z-pT=26': [0.7, 0.42, 0.38, 0.3], 'Q2-y=9, z-pT=27': [0.7, 0.42, 0.46, 0.38], 'Q2-y=9, z-pT=28': [0.7, 0.42, 0.58, 0.46], 'Q2-y=9, z-pT=29': [0.7, 0.42, 0.74, 0.58], 'Q2-y=9, z-pT=30': [0.7, 0.42, 0.95, 0.74], 'Q2-y=9, z-pT=31, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=9, z-pT=32, MIGRATION BIN': [0.16, 0, 0.05, 0.22], 'Q2-y=9, z-pT=33, MIGRATION BIN': [0.16, 0, 0.22, 0.3], 'Q2-y=9, z-pT=34, MIGRATION BIN': [0.16, 0, 0.3, 0.38], 'Q2-y=9, z-pT=35, MIGRATION BIN': [0.16, 0, 0.38, 0.46], 'Q2-y=9, z-pT=36, MIGRATION BIN': [0.16, 0, 0.46, 0.58], 'Q2-y=9, z-pT=37, MIGRATION BIN': [0.16, 0, 0.58, 0.74], 'Q2-y=9, z-pT=38, MIGRATION BIN': [0.16, 0, 0.74, 0.95], 'Q2-y=9, z-pT=39, MIGRATION BIN': [0.16, 0, 1.2, 0.95], 'Q2-y=9, z-pT=40, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=9, z-pT=41, MIGRATION BIN': [0.16, 0.2, 1.2, 0.95], 'Q2-y=9, z-pT=42, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=9, z-pT=43, MIGRATION BIN': [0.2, 0.24, 1.2, 0.95], 'Q2-y=9, z-pT=44, MIGRATION BIN': [0.24, 0.3, 0.05, 0], 'Q2-y=9, z-pT=45, MIGRATION BIN': [0.24, 0.3, 1.2, 0.95], 'Q2-y=9, z-pT=46, MIGRATION BIN': [0.3, 0.42, 0.05, 0], 'Q2-y=9, z-pT=47, MIGRATION BIN': [0.3, 0.42, 1.2, 0.95], 'Q2-y=9, z-pT=48, MIGRATION BIN': [0.42, 0.7, 0.05, 0], 'Q2-y=9, z-pT=49, MIGRATION BIN': [0.42, 0.7, 1.2, 0.95], 'Q2-y=9, z-pT=50, MIGRATION BIN': [1.2, 0.7, 0, 0.05], 'Q2-y=9, z-pT=51, MIGRATION BIN': [1.2, 0.7, 0.05, 0.22], 'Q2-y=9, z-pT=52, MIGRATION BIN': [1.2, 0.7, 0.22, 0.3], 'Q2-y=9, z-pT=53, MIGRATION BIN': [1.2, 0.7, 0.3, 0.38], 'Q2-y=9, z-pT=54, MIGRATION BIN': [1.2, 0.7, 0.38, 0.46], 'Q2-y=9, z-pT=55, MIGRATION BIN': [1.2, 0.7, 0.46, 0.58], 'Q2-y=9, z-pT=56, MIGRATION BIN': [1.2, 0.7, 0.58, 0.74], 'Q2-y=9, z-pT=57, MIGRATION BIN': [1.2, 0.7, 0.74, 0.95], 'Q2-y=9, z-pT=58, MIGRATION BIN': [1.2, 0.7, 1.2, 0.95], 'Q2-y=10, z-pT=1': [0.23, 0.19, 0.21, 0.05], 'Q2-y=10, z-pT=2': [0.23, 0.19, 0.31, 0.21], 'Q2-y=10, z-pT=3': [0.23, 0.19, 0.4, 0.31], 'Q2-y=10, z-pT=4': [0.23, 0.19, 0.5, 0.4], 'Q2-y=10, z-pT=60 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.64, 0.5], 'Q2-y=10, z-pT=61 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.9, 0.64], 'Q2-y=10, z-pT=5': [0.26, 0.23, 0.21, 0.05], 'Q2-y=10, z-pT=6': [0.26, 0.23, 0.31, 0.21], 'Q2-y=10, z-pT=7': [0.26, 0.23, 0.4, 0.31], 'Q2-y=10, z-pT=8': [0.26, 0.23, 0.5, 0.4], 'Q2-y=10, z-pT=9': [0.26, 0.23, 0.64, 0.5], 'Q2-y=10, z-pT=62 - REMOVE, MIGRATION BIN': [0.26, 0.23, 0.9, 0.64], 'Q2-y=10, z-pT=10': [0.32, 0.26, 0.21, 0.05], 'Q2-y=10, z-pT=11': [0.32, 0.26, 0.31, 0.21], 'Q2-y=10, z-pT=12': [0.32, 0.26, 0.4, 0.31], 'Q2-y=10, z-pT=13': [0.32, 0.26, 0.5, 0.4], 'Q2-y=10, z-pT=14': [0.32, 0.26, 0.64, 0.5], 'Q2-y=10, z-pT=63 - REMOVE, MIGRATION BIN': [0.32, 0.26, 0.9, 0.64], 'Q2-y=10, z-pT=15': [0.4, 0.32, 0.21, 0.05], 'Q2-y=10, z-pT=16': [0.4, 0.32, 0.31, 0.21], 'Q2-y=10, z-pT=17': [0.4, 0.32, 0.4, 0.31], 'Q2-y=10, z-pT=18': [0.4, 0.32, 0.5, 0.4], 'Q2-y=10, z-pT=19': [0.4, 0.32, 0.64, 0.5], 'Q2-y=10, z-pT=20': [0.4, 0.32, 0.9, 0.64], 'Q2-y=10, z-pT=21': [0.5, 0.4, 0.21, 0.05], 'Q2-y=10, z-pT=22': [0.5, 0.4, 0.31, 0.21], 'Q2-y=10, z-pT=23': [0.5, 0.4, 0.4, 0.31], 'Q2-y=10, z-pT=24': [0.5, 0.4, 0.5, 0.4], 'Q2-y=10, z-pT=25': [0.5, 0.4, 0.64, 0.5], 'Q2-y=10, z-pT=26': [0.5, 0.4, 0.9, 0.64], 'Q2-y=10, z-pT=27': [0.72, 0.5, 0.21, 0.05], 'Q2-y=10, z-pT=28': [0.72, 0.5, 0.31, 0.21], 'Q2-y=10, z-pT=29': [0.72, 0.5, 0.4, 0.31], 'Q2-y=10, z-pT=30': [0.72, 0.5, 0.5, 0.4], 'Q2-y=10, z-pT=31': [0.72, 0.5, 0.64, 0.5], 'Q2-y=10, z-pT=64 - REMOVE, MIGRATION BIN': [0.72, 0.5, 0.9, 0.64], 'Q2-y=10, z-pT=32, MIGRATION BIN': [0.19, 0, 0.05, 0], 'Q2-y=10, z-pT=33, MIGRATION BIN': [0.19, 0, 0.05, 0.21], 'Q2-y=10, z-pT=34, MIGRATION BIN': [0.19, 0, 0.21, 0.31], 'Q2-y=10, z-pT=35, MIGRATION BIN': [0.19, 0, 0.31, 0.4], 'Q2-y=10, z-pT=36, MIGRATION BIN': [0.19, 0, 0.4, 0.5], 'Q2-y=10, z-pT=37, MIGRATION BIN': [0.19, 0, 0.5, 0.64], 'Q2-y=10, z-pT=38, MIGRATION BIN': [0.19, 0, 0.64, 0.9], 'Q2-y=10, z-pT=39, MIGRATION BIN': [0.19, 0, 1.2, 0.9], 'Q2-y=10, z-pT=40, MIGRATION BIN': [0.19, 0.23, 0.05, 0], 'Q2-y=10, z-pT=41, MIGRATION BIN': [0.19, 0.23, 1.2, 0.9], 'Q2-y=10, z-pT=42, MIGRATION BIN': [0.23, 0.26, 0.05, 0], 'Q2-y=10, z-pT=43, MIGRATION BIN': [0.23, 0.26, 1.2, 0.9], 'Q2-y=10, z-pT=44, MIGRATION BIN': [0.26, 0.32, 0.05, 0], 'Q2-y=10, z-pT=45, MIGRATION BIN': [0.26, 0.32, 1.2, 0.9], 'Q2-y=10, z-pT=46, MIGRATION BIN': [0.32, 0.4, 0.05, 0], 'Q2-y=10, z-pT=47, MIGRATION BIN': [0.32, 0.4, 1.2, 0.9], 'Q2-y=10, z-pT=48, MIGRATION BIN': [0.4, 0.5, 0.05, 0], 'Q2-y=10, z-pT=49, MIGRATION BIN': [0.4, 0.5, 1.2, 0.9], 'Q2-y=10, z-pT=50, MIGRATION BIN': [0.5, 0.72, 0.05, 0], 'Q2-y=10, z-pT=51, MIGRATION BIN': [0.5, 0.72, 1.2, 0.9], 'Q2-y=10, z-pT=52, MIGRATION BIN': [1.2, 0.72, 0, 0.05], 'Q2-y=10, z-pT=53, MIGRATION BIN': [1.2, 0.72, 0.05, 0.21], 'Q2-y=10, z-pT=54, MIGRATION BIN': [1.2, 0.72, 0.21, 0.31], 'Q2-y=10, z-pT=55, MIGRATION BIN': [1.2, 0.72, 0.31, 0.4], 'Q2-y=10, z-pT=56, MIGRATION BIN': [1.2, 0.72, 0.4, 0.5], 'Q2-y=10, z-pT=57, MIGRATION BIN': [1.2, 0.72, 0.5, 0.64], 'Q2-y=10, z-pT=58, MIGRATION BIN': [1.2, 0.72, 0.64, 0.9], 'Q2-y=10, z-pT=59, MIGRATION BIN': [1.2, 0.72, 1.2, 0.9], 'Q2-y=11, z-pT=1': [0.27, 0.22, 0.2, 0.05], 'Q2-y=11, z-pT=2': [0.27, 0.22, 0.3, 0.2], 'Q2-y=11, z-pT=3': [0.27, 0.22, 0.4, 0.3], 'Q2-y=11, z-pT=4': [0.27, 0.22, 0.54, 0.4], 'Q2-y=11, z-pT=46 - REMOVE, MIGRATION BIN': [0.27, 0.22, 0.69, 0.54], 'Q2-y=11, z-pT=5': [0.32, 0.27, 0.2, 0.05], 'Q2-y=11, z-pT=6': [0.32, 0.27, 0.3, 0.2], 'Q2-y=11, z-pT=7': [0.32, 0.27, 0.4, 0.3], 'Q2-y=11, z-pT=8': [0.32, 0.27, 0.54, 0.4], 'Q2-y=11, z-pT=9': [0.32, 0.27, 0.69, 0.54], 'Q2-y=11, z-pT=10': [0.4, 0.32, 0.2, 0.05], 'Q2-y=11, z-pT=11': [0.4, 0.32, 0.3, 0.2], 'Q2-y=11, z-pT=12': [0.4, 0.32, 0.4, 0.3], 'Q2-y=11, z-pT=13': [0.4, 0.32, 0.54, 0.4], 'Q2-y=11, z-pT=14': [0.4, 0.32, 0.69, 0.54], 'Q2-y=11, z-pT=15': [0.53, 0.4, 0.2, 0.05], 'Q2-y=11, z-pT=16': [0.53, 0.4, 0.3, 0.2], 'Q2-y=11, z-pT=17': [0.53, 0.4, 0.4, 0.3], 'Q2-y=11, z-pT=18': [0.53, 0.4, 0.54, 0.4], 'Q2-y=11, z-pT=19': [0.53, 0.4, 0.69, 0.54], 'Q2-y=11, z-pT=20': [0.69, 0.53, 0.2, 0.05], 'Q2-y=11, z-pT=21': [0.69, 0.53, 0.3, 0.2], 'Q2-y=11, z-pT=47 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.4, 0.3], 'Q2-y=11, z-pT=48 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.54, 0.4], 'Q2-y=11, z-pT=49 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.69, 0.54], 'Q2-y=11, z-pT=22, MIGRATION BIN': [0.22, 0, 0.05, 0], 'Q2-y=11, z-pT=23, MIGRATION BIN': [0.22, 0, 0.05, 0.2], 'Q2-y=11, z-pT=24, MIGRATION BIN': [0.22, 0, 0.2, 0.3], 'Q2-y=11, z-pT=25, MIGRATION BIN': [0.22, 0, 0.3, 0.4], 'Q2-y=11, z-pT=26, MIGRATION BIN': [0.22, 0, 0.4, 0.54], 'Q2-y=11, z-pT=27, MIGRATION BIN': [0.22, 0, 0.54, 0.69], 'Q2-y=11, z-pT=28, MIGRATION BIN': [0.22, 0, 1.2, 0.69], 'Q2-y=11, z-pT=29, MIGRATION BIN': [0.22, 0.27, 0.05, 0], 'Q2-y=11, z-pT=30, MIGRATION BIN': [0.22, 0.27, 1.2, 0.69], 'Q2-y=11, z-pT=31, MIGRATION BIN': [0.27, 0.32, 0.05, 0], 'Q2-y=11, z-pT=32, MIGRATION BIN': [0.27, 0.32, 1.2, 0.69], 'Q2-y=11, z-pT=33, MIGRATION BIN': [0.32, 0.4, 0.05, 0], 'Q2-y=11, z-pT=34, MIGRATION BIN': [0.32, 0.4, 1.2, 0.69], 'Q2-y=11, z-pT=35, MIGRATION BIN': [0.4, 0.53, 0.05, 0], 'Q2-y=11, z-pT=36, MIGRATION BIN': [0.4, 0.53, 1.2, 0.69], 'Q2-y=11, z-pT=37, MIGRATION BIN': [0.53, 0.69, 0.05, 0], 'Q2-y=11, z-pT=38, MIGRATION BIN': [0.53, 0.69, 1.2, 0.69], 'Q2-y=11, z-pT=39, MIGRATION BIN': [1.2, 0.69, 0, 0.05], 'Q2-y=11, z-pT=40, MIGRATION BIN': [1.2, 0.69, 0.05, 0.2], 'Q2-y=11, z-pT=41, MIGRATION BIN': [1.2, 0.69, 0.2, 0.3], 'Q2-y=11, z-pT=42, MIGRATION BIN': [1.2, 0.69, 0.3, 0.4], 'Q2-y=11, z-pT=43, MIGRATION BIN': [1.2, 0.69, 0.4, 0.54], 'Q2-y=11, z-pT=44, MIGRATION BIN': [1.2, 0.69, 0.54, 0.69], 'Q2-y=11, z-pT=45, MIGRATION BIN': [1.2, 0.69, 1.2, 0.69], 'Q2-y=12, z-pT=1': [0.31, 0.27, 0.22, 0.05], 'Q2-y=12, z-pT=2': [0.31, 0.27, 0.32, 0.22], 'Q2-y=12, z-pT=3': [0.31, 0.27, 0.41, 0.32], 'Q2-y=12, z-pT=4': [0.35, 0.31, 0.22, 0.05], 'Q2-y=12, z-pT=5': [0.35, 0.31, 0.32, 0.22], 'Q2-y=12, z-pT=6': [0.35, 0.31, 0.41, 0.32], 'Q2-y=12, z-pT=7': [0.4, 0.35, 0.22, 0.05], 'Q2-y=12, z-pT=8': [0.4, 0.35, 0.32, 0.22], 'Q2-y=12, z-pT=9': [0.4, 0.35, 0.41, 0.32], 'Q2-y=12, z-pT=10': [0.5, 0.4, 0.22, 0.05], 'Q2-y=12, z-pT=29 - REMOVE, MIGRATION BIN': [0.5, 0.4, 0.32, 0.22], 'Q2-y=12, z-pT=30 - REMOVE, MIGRATION BIN': [0.5, 0.4, 0.41, 0.32], 'Q2-y=12, z-pT=11, MIGRATION BIN': [0.27, 0, 0.05, 0], 'Q2-y=12, z-pT=12, MIGRATION BIN': [0.27, 0, 0.05, 0.22], 'Q2-y=12, z-pT=13, MIGRATION BIN': [0.27, 0, 0.22, 0.32], 'Q2-y=12, z-pT=14, MIGRATION BIN': [0.27, 0, 0.32, 0.41], 'Q2-y=12, z-pT=15, MIGRATION BIN': [0.27, 0, 1.2, 0.41], 'Q2-y=12, z-pT=16, MIGRATION BIN': [0.27, 0.31, 0.05, 0], 'Q2-y=12, z-pT=17, MIGRATION BIN': [0.27, 0.31, 1.2, 0.41], 'Q2-y=12, z-pT=18, MIGRATION BIN': [0.31, 0.35, 0.05, 0], 'Q2-y=12, z-pT=19, MIGRATION BIN': [0.31, 0.35, 1.2, 0.41], 'Q2-y=12, z-pT=20, MIGRATION BIN': [0.35, 0.4, 0.05, 0], 'Q2-y=12, z-pT=21, MIGRATION BIN': [0.35, 0.4, 1.2, 0.41], 'Q2-y=12, z-pT=22, MIGRATION BIN': [0.4, 0.5, 0.05, 0], 'Q2-y=12, z-pT=23, MIGRATION BIN': [0.4, 0.5, 1.2, 0.41], 'Q2-y=12, z-pT=24, MIGRATION BIN': [1.2, 0.5, 0, 0.05], 'Q2-y=12, z-pT=25, MIGRATION BIN': [1.2, 0.5, 0.05, 0.22], 'Q2-y=12, z-pT=26, MIGRATION BIN': [1.2, 0.5, 0.22, 0.32], 'Q2-y=12, z-pT=27, MIGRATION BIN': [1.2, 0.5, 0.32, 0.41], 'Q2-y=12, z-pT=28, MIGRATION BIN': [1.2, 0.5, 1.2, 0.41], 'Q2-y=13, z-pT=1': [0.2, 0.16, 0.22, 0.05], 'Q2-y=13, z-pT=2': [0.2, 0.16, 0.35, 0.22], 'Q2-y=13, z-pT=3': [0.2, 0.16, 0.45, 0.35], 'Q2-y=13, z-pT=52 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.6, 0.45], 'Q2-y=13, z-pT=53 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.9, 0.6], 'Q2-y=13, z-pT=4': [0.24, 0.2, 0.22, 0.05], 'Q2-y=13, z-pT=5': [0.24, 0.2, 0.35, 0.22], 'Q2-y=13, z-pT=6': [0.24, 0.2, 0.45, 0.35], 'Q2-y=13, z-pT=7': [0.24, 0.2, 0.6, 0.45], 'Q2-y=13, z-pT=54 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.9, 0.6], 'Q2-y=13, z-pT=8': [0.29, 0.24, 0.22, 0.05], 'Q2-y=13, z-pT=9': [0.29, 0.24, 0.35, 0.22], 'Q2-y=13, z-pT=10': [0.29, 0.24, 0.45, 0.35], 'Q2-y=13, z-pT=11': [0.29, 0.24, 0.6, 0.45], 'Q2-y=13, z-pT=55 - REMOVE, MIGRATION BIN': [0.29, 0.24, 0.9, 0.6], 'Q2-y=13, z-pT=12': [0.36, 0.29, 0.22, 0.05], 'Q2-y=13, z-pT=13': [0.36, 0.29, 0.35, 0.22], 'Q2-y=13, z-pT=14': [0.36, 0.29, 0.45, 0.35], 'Q2-y=13, z-pT=15': [0.36, 0.29, 0.6, 0.45], 'Q2-y=13, z-pT=16': [0.36, 0.29, 0.9, 0.6], 'Q2-y=13, z-pT=17': [0.51, 0.36, 0.22, 0.05], 'Q2-y=13, z-pT=18': [0.51, 0.36, 0.35, 0.22], 'Q2-y=13, z-pT=19': [0.51, 0.36, 0.45, 0.35], 'Q2-y=13, z-pT=20': [0.51, 0.36, 0.6, 0.45], 'Q2-y=13, z-pT=21': [0.51, 0.36, 0.9, 0.6], 'Q2-y=13, z-pT=22': [0.72, 0.51, 0.22, 0.05], 'Q2-y=13, z-pT=23': [0.72, 0.51, 0.35, 0.22], 'Q2-y=13, z-pT=24': [0.72, 0.51, 0.45, 0.35], 'Q2-y=13, z-pT=25': [0.72, 0.51, 0.6, 0.45], 'Q2-y=13, z-pT=56 - REMOVE, MIGRATION BIN': [0.72, 0.51, 0.9, 0.6], 'Q2-y=13, z-pT=26, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=13, z-pT=27, MIGRATION BIN': [0.16, 0, 0.05, 0.22], 'Q2-y=13, z-pT=28, MIGRATION BIN': [0.16, 0, 0.22, 0.35], 'Q2-y=13, z-pT=29, MIGRATION BIN': [0.16, 0, 0.35, 0.45], 'Q2-y=13, z-pT=30, MIGRATION BIN': [0.16, 0, 0.45, 0.6], 'Q2-y=13, z-pT=31, MIGRATION BIN': [0.16, 0, 0.6, 0.9], 'Q2-y=13, z-pT=32, MIGRATION BIN': [0.16, 0, 1.2, 0.9], 'Q2-y=13, z-pT=33, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=13, z-pT=34, MIGRATION BIN': [0.16, 0.2, 1.2, 0.9], 'Q2-y=13, z-pT=35, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=13, z-pT=36, MIGRATION BIN': [0.2, 0.24, 1.2, 0.9], 'Q2-y=13, z-pT=37, MIGRATION BIN': [0.24, 0.29, 0.05, 0], 'Q2-y=13, z-pT=38, MIGRATION BIN': [0.24, 0.29, 1.2, 0.9], 'Q2-y=13, z-pT=39, MIGRATION BIN': [0.29, 0.36, 0.05, 0], 'Q2-y=13, z-pT=40, MIGRATION BIN': [0.29, 0.36, 1.2, 0.9], 'Q2-y=13, z-pT=41, MIGRATION BIN': [0.36, 0.51, 0.05, 0], 'Q2-y=13, z-pT=42, MIGRATION BIN': [0.36, 0.51, 1.2, 0.9], 'Q2-y=13, z-pT=43, MIGRATION BIN': [0.51, 0.72, 0.05, 0], 'Q2-y=13, z-pT=44, MIGRATION BIN': [0.51, 0.72, 1.2, 0.9], 'Q2-y=13, z-pT=45, MIGRATION BIN': [1.2, 0.72, 0, 0.05], 'Q2-y=13, z-pT=46, MIGRATION BIN': [1.2, 0.72, 0.05, 0.22], 'Q2-y=13, z-pT=47, MIGRATION BIN': [1.2, 0.72, 0.22, 0.35], 'Q2-y=13, z-pT=48, MIGRATION BIN': [1.2, 0.72, 0.35, 0.45], 'Q2-y=13, z-pT=49, MIGRATION BIN': [1.2, 0.72, 0.45, 0.6], 'Q2-y=13, z-pT=50, MIGRATION BIN': [1.2, 0.72, 0.6, 0.9], 'Q2-y=13, z-pT=51, MIGRATION BIN': [1.2, 0.72, 1.2, 0.9], 'Q2-y=14, z-pT=1': [0.23, 0.19, 0.2, 0.05], 'Q2-y=14, z-pT=2': [0.23, 0.19, 0.3, 0.2], 'Q2-y=14, z-pT=3': [0.23, 0.19, 0.4, 0.3], 'Q2-y=14, z-pT=4': [0.23, 0.19, 0.5, 0.4], 'Q2-y=14, z-pT=56 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.65, 0.5], 'Q2-y=14, z-pT=57 - REMOVE, MIGRATION BIN': [0.23, 0.19, 0.8, 0.65], 'Q2-y=14, z-pT=5': [0.27, 0.23, 0.2, 0.05], 'Q2-y=14, z-pT=6': [0.27, 0.23, 0.3, 0.2], 'Q2-y=14, z-pT=7': [0.27, 0.23, 0.4, 0.3], 'Q2-y=14, z-pT=8': [0.27, 0.23, 0.5, 0.4], 'Q2-y=14, z-pT=9': [0.27, 0.23, 0.65, 0.5], 'Q2-y=14, z-pT=58 - REMOVE, MIGRATION BIN': [0.27, 0.23, 0.8, 0.65], 'Q2-y=14, z-pT=10': [0.32, 0.27, 0.2, 0.05], 'Q2-y=14, z-pT=11': [0.32, 0.27, 0.3, 0.2], 'Q2-y=14, z-pT=12': [0.32, 0.27, 0.4, 0.3], 'Q2-y=14, z-pT=13': [0.32, 0.27, 0.5, 0.4], 'Q2-y=14, z-pT=14': [0.32, 0.27, 0.65, 0.5], 'Q2-y=14, z-pT=59 - REMOVE, MIGRATION BIN': [0.32, 0.27, 0.8, 0.65], 'Q2-y=14, z-pT=15': [0.4, 0.32, 0.2, 0.05], 'Q2-y=14, z-pT=16': [0.4, 0.32, 0.3, 0.2], 'Q2-y=14, z-pT=17': [0.4, 0.32, 0.4, 0.3], 'Q2-y=14, z-pT=18': [0.4, 0.32, 0.5, 0.4], 'Q2-y=14, z-pT=19': [0.4, 0.32, 0.65, 0.5], 'Q2-y=14, z-pT=60 - REMOVE, MIGRATION BIN': [0.4, 0.32, 0.8, 0.65], 'Q2-y=14, z-pT=20': [0.53, 0.4, 0.2, 0.05], 'Q2-y=14, z-pT=21': [0.53, 0.4, 0.3, 0.2], 'Q2-y=14, z-pT=22': [0.53, 0.4, 0.4, 0.3], 'Q2-y=14, z-pT=23': [0.53, 0.4, 0.5, 0.4], 'Q2-y=14, z-pT=24': [0.53, 0.4, 0.65, 0.5], 'Q2-y=14, z-pT=61 - REMOVE, MIGRATION BIN': [0.53, 0.4, 0.8, 0.65], 'Q2-y=14, z-pT=25': [0.69, 0.53, 0.2, 0.05], 'Q2-y=14, z-pT=26': [0.69, 0.53, 0.3, 0.2], 'Q2-y=14, z-pT=27': [0.69, 0.53, 0.4, 0.3], 'Q2-y=14, z-pT=62 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.5, 0.4], 'Q2-y=14, z-pT=63 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.65, 0.5], 'Q2-y=14, z-pT=64 - REMOVE, MIGRATION BIN': [0.69, 0.53, 0.8, 0.65], 'Q2-y=14, z-pT=28, MIGRATION BIN': [0.19, 0, 0.05, 0], 'Q2-y=14, z-pT=29, MIGRATION BIN': [0.19, 0, 0.05, 0.2], 'Q2-y=14, z-pT=30, MIGRATION BIN': [0.19, 0, 0.2, 0.3], 'Q2-y=14, z-pT=31, MIGRATION BIN': [0.19, 0, 0.3, 0.4], 'Q2-y=14, z-pT=32, MIGRATION BIN': [0.19, 0, 0.4, 0.5], 'Q2-y=14, z-pT=33, MIGRATION BIN': [0.19, 0, 0.5, 0.65], 'Q2-y=14, z-pT=34, MIGRATION BIN': [0.19, 0, 0.65, 0.8], 'Q2-y=14, z-pT=35, MIGRATION BIN': [0.19, 0, 1.2, 0.8], 'Q2-y=14, z-pT=36, MIGRATION BIN': [0.19, 0.23, 0.05, 0], 'Q2-y=14, z-pT=37, MIGRATION BIN': [0.19, 0.23, 1.2, 0.8], 'Q2-y=14, z-pT=38, MIGRATION BIN': [0.23, 0.27, 0.05, 0], 'Q2-y=14, z-pT=39, MIGRATION BIN': [0.23, 0.27, 1.2, 0.8], 'Q2-y=14, z-pT=40, MIGRATION BIN': [0.27, 0.32, 0.05, 0], 'Q2-y=14, z-pT=41, MIGRATION BIN': [0.27, 0.32, 1.2, 0.8], 'Q2-y=14, z-pT=42, MIGRATION BIN': [0.32, 0.4, 0.05, 0], 'Q2-y=14, z-pT=43, MIGRATION BIN': [0.32, 0.4, 1.2, 0.8], 'Q2-y=14, z-pT=44, MIGRATION BIN': [0.4, 0.53, 0.05, 0], 'Q2-y=14, z-pT=45, MIGRATION BIN': [0.4, 0.53, 1.2, 0.8], 'Q2-y=14, z-pT=46, MIGRATION BIN': [0.53, 0.69, 0.05, 0], 'Q2-y=14, z-pT=47, MIGRATION BIN': [0.53, 0.69, 1.2, 0.8], 'Q2-y=14, z-pT=48, MIGRATION BIN': [1.2, 0.69, 0, 0.05], 'Q2-y=14, z-pT=49, MIGRATION BIN': [1.2, 0.69, 0.05, 0.2], 'Q2-y=14, z-pT=50, MIGRATION BIN': [1.2, 0.69, 0.2, 0.3], 'Q2-y=14, z-pT=51, MIGRATION BIN': [1.2, 0.69, 0.3, 0.4], 'Q2-y=14, z-pT=52, MIGRATION BIN': [1.2, 0.69, 0.4, 0.5], 'Q2-y=14, z-pT=53, MIGRATION BIN': [1.2, 0.69, 0.5, 0.65], 'Q2-y=14, z-pT=54, MIGRATION BIN': [1.2, 0.69, 0.65, 0.8], 'Q2-y=14, z-pT=55, MIGRATION BIN': [1.2, 0.69, 1.2, 0.8], 'Q2-y=15, z-pT=1': [0.28, 0.22, 0.23, 0.05], 'Q2-y=15, z-pT=2': [0.28, 0.22, 0.33, 0.23], 'Q2-y=15, z-pT=3': [0.28, 0.22, 0.47, 0.33], 'Q2-y=15, z-pT=4': [0.33, 0.28, 0.23, 0.05], 'Q2-y=15, z-pT=5': [0.33, 0.28, 0.33, 0.23], 'Q2-y=15, z-pT=6': [0.33, 0.28, 0.47, 0.33], 'Q2-y=15, z-pT=7': [0.4, 0.33, 0.23, 0.05], 'Q2-y=15, z-pT=8': [0.4, 0.33, 0.33, 0.23], 'Q2-y=15, z-pT=9': [0.4, 0.33, 0.47, 0.33], 'Q2-y=15, z-pT=10': [0.51, 0.4, 0.23, 0.05], 'Q2-y=15, z-pT=11': [0.51, 0.4, 0.33, 0.23], 'Q2-y=15, z-pT=30 - REMOVE, MIGRATION BIN': [0.51, 0.4, 0.47, 0.33], 'Q2-y=15, z-pT=12, MIGRATION BIN': [0.22, 0, 0.05, 0], 'Q2-y=15, z-pT=13, MIGRATION BIN': [0.22, 0, 0.05, 0.23], 'Q2-y=15, z-pT=14, MIGRATION BIN': [0.22, 0, 0.23, 0.33], 'Q2-y=15, z-pT=15, MIGRATION BIN': [0.22, 0, 0.33, 0.47], 'Q2-y=15, z-pT=16, MIGRATION BIN': [0.22, 0, 1.2, 0.47], 'Q2-y=15, z-pT=17, MIGRATION BIN': [0.22, 0.28, 0.05, 0], 'Q2-y=15, z-pT=18, MIGRATION BIN': [0.22, 0.28, 1.2, 0.47], 'Q2-y=15, z-pT=19, MIGRATION BIN': [0.28, 0.33, 0.05, 0], 'Q2-y=15, z-pT=20, MIGRATION BIN': [0.28, 0.33, 1.2, 0.47], 'Q2-y=15, z-pT=21, MIGRATION BIN': [0.33, 0.4, 0.05, 0], 'Q2-y=15, z-pT=22, MIGRATION BIN': [0.33, 0.4, 1.2, 0.47], 'Q2-y=15, z-pT=23, MIGRATION BIN': [0.4, 0.51, 0.05, 0], 'Q2-y=15, z-pT=24, MIGRATION BIN': [0.4, 0.51, 1.2, 0.47], 'Q2-y=15, z-pT=25, MIGRATION BIN': [1.2, 0.51, 0, 0.05], 'Q2-y=15, z-pT=26, MIGRATION BIN': [1.2, 0.51, 0.05, 0.23], 'Q2-y=15, z-pT=27, MIGRATION BIN': [1.2, 0.51, 0.23, 0.33], 'Q2-y=15, z-pT=28, MIGRATION BIN': [1.2, 0.51, 0.33, 0.47], 'Q2-y=15, z-pT=29, MIGRATION BIN': [1.2, 0.51, 1.2, 0.47], 'Q2-y=16, z-pT=1': [0.2, 0.16, 0.22, 0.05], 'Q2-y=16, z-pT=2': [0.2, 0.16, 0.31, 0.22], 'Q2-y=16, z-pT=3': [0.2, 0.16, 0.44, 0.31], 'Q2-y=16, z-pT=46 - REMOVE, MIGRATION BIN': [0.2, 0.16, 0.7, 0.44], 'Q2-y=16, z-pT=4': [0.24, 0.2, 0.22, 0.05], 'Q2-y=16, z-pT=5': [0.24, 0.2, 0.31, 0.22], 'Q2-y=16, z-pT=6': [0.24, 0.2, 0.44, 0.31], 'Q2-y=16, z-pT=47 - REMOVE, MIGRATION BIN': [0.24, 0.2, 0.7, 0.44], 'Q2-y=16, z-pT=7': [0.29, 0.24, 0.22, 0.05], 'Q2-y=16, z-pT=8': [0.29, 0.24, 0.31, 0.22], 'Q2-y=16, z-pT=9': [0.29, 0.24, 0.44, 0.31], 'Q2-y=16, z-pT=10': [0.29, 0.24, 0.7, 0.44], 'Q2-y=16, z-pT=11': [0.36, 0.29, 0.22, 0.05], 'Q2-y=16, z-pT=12': [0.36, 0.29, 0.31, 0.22], 'Q2-y=16, z-pT=13': [0.36, 0.29, 0.44, 0.31], 'Q2-y=16, z-pT=14': [0.36, 0.29, 0.7, 0.44], 'Q2-y=16, z-pT=15': [0.45, 0.36, 0.22, 0.05], 'Q2-y=16, z-pT=16': [0.45, 0.36, 0.31, 0.22], 'Q2-y=16, z-pT=17': [0.45, 0.36, 0.44, 0.31], 'Q2-y=16, z-pT=18': [0.45, 0.36, 0.7, 0.44], 'Q2-y=16, z-pT=19': [0.62, 0.45, 0.22, 0.05], 'Q2-y=16, z-pT=20': [0.62, 0.45, 0.31, 0.22], 'Q2-y=16, z-pT=21': [0.62, 0.45, 0.44, 0.31], 'Q2-y=16, z-pT=48 - REMOVE, MIGRATION BIN': [0.62, 0.45, 0.7, 0.44], 'Q2-y=16, z-pT=22, MIGRATION BIN': [0.16, 0, 0.05, 0], 'Q2-y=16, z-pT=23, MIGRATION BIN': [0.16, 0, 0.05, 0.22], 'Q2-y=16, z-pT=24, MIGRATION BIN': [0.16, 0, 0.22, 0.31], 'Q2-y=16, z-pT=25, MIGRATION BIN': [0.16, 0, 0.31, 0.44], 'Q2-y=16, z-pT=26, MIGRATION BIN': [0.16, 0, 0.44, 0.7], 'Q2-y=16, z-pT=27, MIGRATION BIN': [0.16, 0, 1.2, 0.7], 'Q2-y=16, z-pT=28, MIGRATION BIN': [0.16, 0.2, 0.05, 0], 'Q2-y=16, z-pT=29, MIGRATION BIN': [0.16, 0.2, 1.2, 0.7], 'Q2-y=16, z-pT=30, MIGRATION BIN': [0.2, 0.24, 0.05, 0], 'Q2-y=16, z-pT=31, MIGRATION BIN': [0.2, 0.24, 1.2, 0.7], 'Q2-y=16, z-pT=32, MIGRATION BIN': [0.24, 0.29, 0.05, 0], 'Q2-y=16, z-pT=33, MIGRATION BIN': [0.24, 0.29, 1.2, 0.7], 'Q2-y=16, z-pT=34, MIGRATION BIN': [0.29, 0.36, 0.05, 0], 'Q2-y=16, z-pT=35, MIGRATION BIN': [0.29, 0.36, 1.2, 0.7], 'Q2-y=16, z-pT=36, MIGRATION BIN': [0.36, 0.45, 0.05, 0], 'Q2-y=16, z-pT=37, MIGRATION BIN': [0.36, 0.45, 1.2, 0.7], 'Q2-y=16, z-pT=38, MIGRATION BIN': [0.45, 0.62, 0.05, 0], 'Q2-y=16, z-pT=39, MIGRATION BIN': [0.45, 0.62, 1.2, 0.7], 'Q2-y=16, z-pT=40, MIGRATION BIN': [1.2, 0.62, 0, 0.05], 'Q2-y=16, z-pT=41, MIGRATION BIN': [1.2, 0.62, 0.05, 0.22], 'Q2-y=16, z-pT=42, MIGRATION BIN': [1.2, 0.62, 0.22, 0.31], 'Q2-y=16, z-pT=43, MIGRATION BIN': [1.2, 0.62, 0.31, 0.44], 'Q2-y=16, z-pT=44, MIGRATION BIN': [1.2, 0.62, 0.44, 0.7], 'Q2-y=16, z-pT=45, MIGRATION BIN': [1.2, 0.62, 1.2, 0.7], 'Q2-y=17, z-pT=1': [0.23, 0.19, 0.19, 0.05], 'Q2-y=17, z-pT=2': [0.23, 0.19, 0.28, 0.19], 'Q2-y=17, z-pT=3': [0.23, 0.19, 0.37, 0.28], 'Q2-y=17, z-pT=4': [0.29, 0.23, 0.19, 0.05], 'Q2-y=17, z-pT=5': [0.29, 0.23, 0.28, 0.19], 'Q2-y=17, z-pT=6': [0.29, 0.23, 0.37, 0.28], 'Q2-y=17, z-pT=7': [0.35, 0.29, 0.19, 0.05], 'Q2-y=17, z-pT=8': [0.35, 0.29, 0.28, 0.19], 'Q2-y=17, z-pT=9': [0.35, 0.29, 0.37, 0.28], 'Q2-y=17, z-pT=10': [0.45, 0.35, 0.19, 0.05], 'Q2-y=17, z-pT=29 - REMOVE, MIGRATION BIN': [0.45, 0.35, 0.28, 0.19], 'Q2-y=17, z-pT=30 - REMOVE, MIGRATION BIN': [0.45, 0.35, 0.37, 0.28], 'Q2-y=17, z-pT=11, MIGRATION BIN': [0.19, 0, 0.05, 0], 'Q2-y=17, z-pT=12, MIGRATION BIN': [0.19, 0, 0.05, 0.19], 'Q2-y=17, z-pT=13, MIGRATION BIN': [0.19, 0, 0.19, 0.28], 'Q2-y=17, z-pT=14, MIGRATION BIN': [0.19, 0, 0.28, 0.37], 'Q2-y=17, z-pT=15, MIGRATION BIN': [0.19, 0, 1.2, 0.37], 'Q2-y=17, z-pT=16, MIGRATION BIN': [0.19, 0.23, 0.05, 0], 'Q2-y=17, z-pT=17, MIGRATION BIN': [0.19, 0.23, 1.2, 0.37], 'Q2-y=17, z-pT=18, MIGRATION BIN': [0.23, 0.29, 0.05, 0], 'Q2-y=17, z-pT=19, MIGRATION BIN': [0.23, 0.29, 1.2, 0.37], 'Q2-y=17, z-pT=20, MIGRATION BIN': [0.29, 0.35, 0.05, 0], 'Q2-y=17, z-pT=21, MIGRATION BIN': [0.29, 0.35, 1.2, 0.37], 'Q2-y=17, z-pT=22, MIGRATION BIN': [0.35, 0.45, 0.05, 0], 'Q2-y=17, z-pT=23, MIGRATION BIN': [0.35, 0.45, 1.2, 0.37], 'Q2-y=17, z-pT=24, MIGRATION BIN': [1.2, 0.45, 0, 0.05], 'Q2-y=17, z-pT=25, MIGRATION BIN': [1.2, 0.45, 0.05, 0.19], 'Q2-y=17, z-pT=26, MIGRATION BIN': [1.2, 0.45, 0.19, 0.28], 'Q2-y=17, z-pT=27, MIGRATION BIN': [1.2, 0.45, 0.28, 0.37], 'Q2-y=17, z-pT=28, MIGRATION BIN': [1.2, 0.45, 1.2, 0.37]}

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=1):
    Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2 = 1, 1, 2
    if(str(Q2_y_Bin_Num_In) in ['1']):
        Migration_Bin_2 = 58
        Migration_Bin_1 = 30
        Total_Number_of_Bins = 63
    if(str(Q2_y_Bin_Num_In) in ['2']):
        Migration_Bin_2 = 60
        Migration_Bin_1 = 32
        Total_Number_of_Bins = 64
    if(str(Q2_y_Bin_Num_In) in ['3']):
        Migration_Bin_2 = 47
        Migration_Bin_1 = 23
        Total_Number_of_Bins = 48
    if(str(Q2_y_Bin_Num_In) in ['4']):
        Migration_Bin_2 = 49
        Migration_Bin_1 = 25
        Total_Number_of_Bins = 49
    if(str(Q2_y_Bin_Num_In) in ['5']):
        Migration_Bin_2 = 61
        Migration_Bin_1 = 33
        Total_Number_of_Bins = 64
    if(str(Q2_y_Bin_Num_In) in ['6']):
        Migration_Bin_2 = 52
        Migration_Bin_1 = 26
        Total_Number_of_Bins = 56
    if(str(Q2_y_Bin_Num_In) in ['7']):
        Migration_Bin_2 = 53
        Migration_Bin_1 = 27
        Total_Number_of_Bins = 56
    if(str(Q2_y_Bin_Num_In) in ['8']):
        Migration_Bin_2 = 47
        Migration_Bin_1 = 23
        Total_Number_of_Bins = 48
    if(str(Q2_y_Bin_Num_In) in ['9']):
        Migration_Bin_2 = 59
        Migration_Bin_1 = 31
        Total_Number_of_Bins = 63
    if(str(Q2_y_Bin_Num_In) in ['10']):
        Migration_Bin_2 = 60
        Migration_Bin_1 = 32
        Total_Number_of_Bins = 64
    if(str(Q2_y_Bin_Num_In) in ['11']):
        Migration_Bin_2 = 46
        Migration_Bin_1 = 22
        Total_Number_of_Bins = 49
    if(str(Q2_y_Bin_Num_In) in ['12']):
        Migration_Bin_2 = 29
        Migration_Bin_1 = 11
        Total_Number_of_Bins = 30
    if(str(Q2_y_Bin_Num_In) in ['13']):
        Migration_Bin_2 = 52
        Migration_Bin_1 = 26
        Total_Number_of_Bins = 56
    if(str(Q2_y_Bin_Num_In) in ['14']):
        Migration_Bin_2 = 56
        Migration_Bin_1 = 28
        Total_Number_of_Bins = 64
    if(str(Q2_y_Bin_Num_In) in ['15']):
        Migration_Bin_2 = 30
        Migration_Bin_1 = 12
        Total_Number_of_Bins = 30
    if(str(Q2_y_Bin_Num_In) in ['16']):
        Migration_Bin_2 = 46
        Migration_Bin_1 = 22
        Total_Number_of_Bins = 48
    if(str(Q2_y_Bin_Num_In) in ['17']):
        Migration_Bin_2 = 29
        Migration_Bin_1 = 11
        Total_Number_of_Bins = 30
    return [Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2]

##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Get_z_pT_Bin_Corners(z_pT_Bin_Num="All", Q2_y_Bin_Num=1):
    if(str(z_pT_Bin_Num) in ["All", "0"]):
        New_z_pT_Bin_Test_List = New_z_pT_Bin_Test(Q2_y_Bin_Num)
        z_Borders  = New_z_pT_Bin_Test_List[0][2]
        pT_Borders = New_z_pT_Bin_Test_List[1][2]
        return ["z", z_Borders, "pT", pT_Borders]
    Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2 = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Num)
    Bin_Definition_Array_str = "end"
    if(z_pT_Bin_Num   > (Migration_Bin_2 - 1)):
        Bin_Definition_Array_str = f'Q2-y={Q2_y_Bin_Num}, z-pT={z_pT_Bin_Num} - REMOVE, MIGRATION BIN'
    elif(z_pT_Bin_Num > (Migration_Bin_1 - 1)):
        Bin_Definition_Array_str = f'Q2-y={Q2_y_Bin_Num}, z-pT={z_pT_Bin_Num}, MIGRATION BIN'
    else:
        Bin_Definition_Array_str = f'Q2-y={Q2_y_Bin_Num}, z-pT={z_pT_Bin_Num}'
    return Bin_Definition_Array[Bin_Definition_Array_str]
    ###### return [z_max, z_min, pT_max, pT_min]
    
##=========================================================================================##
##=========================================================================================##
##=========================================================================================##

def Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=1, Set_Max_Y=False, Set_Max_X=False, Plot_Orientation_Input="z_pT"):
    Total_Number_of_Bins, Migration_Bin_1, Migration_Bin_2 = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_y_Bin_Num_In)
    z_pT_Bins_Borders = {}
    for z_pT in range(1, Total_Number_of_Bins + 1, 1):
        bin_color = 1 if(z_pT < Migration_Bin_1) else 2 if(z_pT < Migration_Bin_2) else 41
        line_size = 4 if(z_pT < Migration_Bin_1) else 2
        y_max, y_min, x_max, x_min = Get_z_pT_Bin_Corners(z_pT_Bin_Num=z_pT, Q2_y_Bin_Num=Q2_y_Bin_Num_In)
        if(Set_Max_Y):
            if(Set_Max_Y < y_max):
                y_max = Set_Max_Y
        if(Set_Max_X):
            if(Set_Max_X < x_max):
                x_max = Set_Max_X
        z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
        z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
        z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
        if(Plot_Orientation_Input not in ["pT_z"]):
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_max, y_max, x_min, y_max)
        else:
            z_pT_Bins_Borders["".join(["Line_1_of_z_pT_Bin_", str(z_pT)])].DrawLine(y_max, x_max, y_min, x_max)
        z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
        z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
        z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
        if(Plot_Orientation_Input not in ["pT_z"]):
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_min, y_max, x_min, y_min)
        else:
            z_pT_Bins_Borders["".join(["Line_2_of_z_pT_Bin_", str(z_pT)])].DrawLine(y_min, x_max, y_min, x_min)
        z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
        z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
        z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
        if(Plot_Orientation_Input not in ["pT_z"]):
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_min, y_min, x_max, y_min)
        else:
            z_pT_Bins_Borders["".join(["Line_3_of_z_pT_Bin_", str(z_pT)])].DrawLine(y_min, x_min, y_max, x_min)
        z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])] = ROOT.TLine()
        z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].SetLineColor(bin_color)
        z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].SetLineWidth(line_size)
        if(Plot_Orientation_Input not in ["pT_z"]):
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].DrawLine(x_max, y_min, x_max, y_max)
        else:
            z_pT_Bins_Borders["".join(["Line_4_of_z_pT_Bin_", str(z_pT)])].DrawLine(y_max, x_min, y_max, x_max)
    del z_pT_Bins_Borders

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