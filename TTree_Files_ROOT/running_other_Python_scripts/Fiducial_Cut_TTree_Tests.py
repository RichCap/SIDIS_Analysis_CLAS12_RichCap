#!/usr/bin/env python3

import argparse
import sys

# Add the path to sys.path temporarily
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *
# Now you can remove the path if you wish
sys.path.remove(script_dir)
del script_dir

# # Dictionary to define custom binning and range settings for specific variables
# variable_settings = {
#     "Q2":                        {"bins":  100, "range_min":    0.0, "range_max":  12.0},
#     "xB":                        {"bins":  100, "range_min":    0.0, "range_max":   0.9},
#     "y":                         {"bins":  100, "range_min":   0.05, "range_max":   0.9},
#     "z":                         {"bins":  100, "range_min":    0.0, "range_max":   1.2},
#     "pT":                        {"bins":  100, "range_min":    0.0, "range_max":   1.3},
#     "W":                         {"bins":  100, "range_min":    1.0, "range_max":   5.0},
#     "MM":                        {"bins":  100, "range_min":    0.0, "range_max":   5.0},
#     "el":                        {"bins":  100, "range_min":    0.0, "range_max":   9.0},
#     "pip":                       {"bins":  100, "range_min":    0.0, "range_max":   9.0},
#     "elth":                      {"bins":  120, "range_min":    0.0, "range_max":  60.0},
#     "pipth":                     {"bins":  160, "range_min":    0.0, "range_max":  80.0},
#     "elPhi":                     {"bins":  120, "range_min":    0.0, "range_max": 360.0},
#     "pipPhi":                    {"bins":  120, "range_min":    0.0, "range_max": 360.0},
#     "phi_t":                     {"bins":   60, "range_min":    0.0, "range_max": 360.0},
#     "Q2_Y_Bin":                  {"bins":   17, "range_min":    0.5, "range_max":  17.5},
#     "z_pT_Bin_Y_bin":            {"bins":   39, "range_min":    0.5, "range_max":  39.5},
#     "z_pT_Bin_Y_bin":            {"bins":   39, "range_min":    0.5, "range_max":  39.5},
#     "W_PCal":                    {"bins":  450, "range_min":    0.0, "range_max": 450.0},
#     "V_PCal":                    {"bins":  450, "range_min":    0.0, "range_max": 450.0},
#     "U_PCal":                    {"bins":  450, "range_min":    0.0, "range_max": 450.0},
#     "Hx":                        {"bins":  450, "range_min":    0.0, "range_max": 450.0},
#     "Hy":                        {"bins":  200, "range_min": -100.0, "range_max": 100.0},
# }

# Argument parser setup
parser = argparse.ArgumentParser(
    description=f"\n{color.BOLD}This script is for creating and drawing histograms related to new Fiducial Cuts being tested.{color.END}\n",
    epilog="""""",
    formatter_class=argparse.RawTextHelpFormatter
)

# # Additional histogram parameters
# parser.add_argument('-b', '--bins', type=int, default=50, help="".join([
#     "Number of bins for histograms (Default: 50).\n",
#     "Default by Variable:", "".join(f"\n{ii.rjust(25)} -> {str(variable_settings[ii]['bins']).rjust(8)}" for ii in variable_settings)
# ]))
# parser.add_argument('--range_min', type=float, default=0.0, help="".join([
#     "Minimum range for histograms (Default: 0.0).\n",
#     "Default by Variable:", "".join(f"\n{ii.rjust(25)} -> {str(variable_settings[ii]['range_min']).rjust(8)}" for ii in variable_settings)
# ]))
# parser.add_argument('--range_max', type=float, default=14.0, help="".join([
#     "Maximum range for histograms (Default: 14.0).\n",
#     "Default by Variable:", "".join(f"\n{ii.rjust(25)} -> {str(variable_settings[ii]['range_max']).rjust(8)}" for ii in variable_settings)
# ]))

# Arguments for existing script settings
# parser.add_argument("-v", "--variables",        nargs='+',                                                               required=True,                   help="Variables to plot as a list of strings or a list of lists for 2D plots")
# parser.add_argument("-df", "--rdf_list",        nargs='+', choices=['rdf', 'mdf', 'gdf'], default=['rdf', 'mdf', 'gdf'],                                  help="List of RDataFrames to use (default: all)")

# parser.add_argument("-t", "--title",                                                                                                            type=str, help="Optional additional title text to add")
# parser.add_argument("--Q2-y-Bin",               nargs='+',                                                                                      type=int, help="Cut on Q2_Y_Bin variable")
# parser.add_argument("--z-pT-Bin",               nargs='+',                                                                                      type=int, help="Cut on z_pT_Bin_Y_bin variable (requires Q2_Y_Bin cut)")
# parser.add_argument("-c", "--cut",                                                                                                              type=str, help="General cut string")
# parser.add_argument("-sc", "--show-cut",                                                                                 action='store_true',             help="Show general cut string in histogram title")
# parser.add_argument("-gc", "--gdf-special-cut",                                                                                                 type=str, help="Special cut for the gdf RDataFrame only")
parser.add_argument("-lr",   "--limit-range",                                                                                                   type=int, help="Apply limit to the number of events allowed in the RDataFrames (applied to all options)")



# Arguments for new lists and variables
parser.add_argument("--DC-2D-Bin-Nums", type=int,   default=170,      help="Set the 2D bin number for Drift Chamber (default: 170)")
parser.add_argument("--Phi-Bin-Nums",   type=int,   default=72,       help="Set the bin number for Phi (default: 72)")
parser.add_argument("--Phi-MaxRange",   type=float, default=360.0,    help="Set the max range for Phi (default: 360)")
parser.add_argument("--Theta-Bin-Nums", type=int,   default=30,       help="Set the bin number for Theta (default: 30)")
parser.add_argument("--Theta-MaxRange", type=float, default=60.0,     help="Set the max range for Theta (default: 60)")

# Lists of options
parser.add_argument("--List-of-Cuts",           nargs='+',                                               default=["Complete_SIDIS_Cuts"],               help="Specify list of cuts to apply")
parser.add_argument("-DC-L", "--DC-Layer-List", nargs='+', choices=["6", "18", "36"],                    default=["6", "18", "36"],                     help="Specify the Drift Chamber layer(s)")
parser.add_argument("-pL",   "--Particle-List", nargs='+', choices=["pip", "ele"],                       default=['pip'],                               help="Specify particle(s) to include (default: ['pip'])")
parser.add_argument("-pA",   "--P-Angle-List",  nargs='+', choices=["pipPhi", "pipth", "elPhi", "elth"], default=['pipPhi', 'elPhi'],                   help="Specify list of particle angles (default: ['pipPhi', 'elPhi'])")
parser.add_argument("-DC-C", "--DC-Coordinate", nargs='+', choices=["2D", "x", "y", "z"],                default=['2D'],                                help="Specify DC coordinate(s) (default: ['2D'])")
parser.add_argument("-sL",   "--Sector-List",   nargs='+', type=str,                                     default=['All'],                               help="List of sectors, e.g., 'All' or sectors 1-6 (default: 'All')")




args = parser.parse_args()
from Main_python_Working_with_TTree_Files import *

canvas, histograms, pl = {}, {}, {}
ROOT.gStyle.SetOptStat("i")



# print("\nSelecting Options...\n")

# # DC_2D_Bin_Nums = 100
# DC_2D_Bin_Nums = 160
# # DC_2D_Bin_Nums = 320


# # Phi___Bin_Nums =  90
# Phi___Bin_Nums =  72
# # Phi___Bin_Nums =  36
# Phi___MaxRange = 360
# # Theta_Bin_Nums =  60
# Theta_Bin_Nums =  30
# Theta_MaxRange =  60

DC_2D_Bin_Nums = args.DC_2D_Bin_Nums
Phi___Bin_Nums = args.Phi_Bin_Nums
Phi___MaxRange = args.Phi_MaxRange
Theta_Bin_Nums = args.Theta_Bin_Nums
Theta_MaxRange = args.Theta_MaxRange

# List_of_Cuts = ["Complete_SIDIS_Cuts"]
# List_of_Cuts.extend(["Valerii_DC_Fiducial_Cuts_ele_DC_6", "Valerii_DC_Fiducial_Cuts_ele_DC_18", "Valerii_DC_Fiducial_Cuts_ele_DC_36"])
# List_of_Cuts.extend(["Valerii_OG_Cut", "Valerii_PCal_Fiducial_Cuts"])
# # List_of_Cuts.extend(["My_pip_DC_Fiducial_Cuts"])

# DC_Layer_List = ["6", "18", "36"]
# # DC_Layer_List = ["6", "18"]
# # DC_Layer_List = ["36"]
# Particle_List = ["pip"]
# P_Angle__List = ["pipPhi", "pipth", "elPhi", "elth"]
# # P_Angle__List = ["pipPhi", "pipth"]
# # P_Angle__List = ["pipPhi"]

# # # P_Angle__List = ["pipPhi_DC_6", "pipth_DC_6", "pipPhi_DC_18", "pipth_DC_18", "pipPhi_DC_36", "pipth_DC_36"]

List_of_Cuts  = args.List_of_Cuts
DC_Layer_List = args.DC_Layer_List
Particle_List = args.Particle_List
P_Angle__List = args.P_Angle_List

# DC_Coordinate = ["2D", "x", "y", "z"] # Option "2D" is for the regular 2D DC hit position histograms while the other options are for making 1D histograms of the x, y, and z coordinates
# # DC_Coordinate = ["2D"]
# # DC_Coordinate = ["x"]

# Sector_List   = ["All"]
# Sector_List.extend([1, 2, 3, 4, 5, 6])

DC_Coordinate = args.DC_Coordinate
Sector_List   = args.Sector_List

# # Sector_List   = [1]

if(any("DC_" in plots for plots in P_Angle__List)):
    print(f"{color.BOLD}\nRunning with Drift Chamber Angles\n{color.END}")
    ROOT.gInterpreter.Declare("""double DC_Spherical_Coordinates(float DCx, float DCy, float DCz, int Coordinate){
        if(Coordinate == 0){ // Returns Radius/Magnitude
            return sqrt(DCx*DCx + DCy*DCy + DCz*DCz);
        }
        if(Coordinate == 1){ // Returns Theta
            return atan2(sqrt(DCx*DCx + DCy*DCy), DCz)*TMath::RadToDeg();
        }
        if(Coordinate == 2){ // Returns Phi
            double Phi_DC = atan2(DCy, DCx)*TMath::RadToDeg();
            if(Phi_DC < 0){Phi_DC += 360;}
            return Phi_DC;
        }
    };""")
    for plots in P_Angle__List:
        if("DC_" not in plots):
            continue
        else:
            Coordinate  = 0     if("Mag"  in plots) else 1     if("th"    in plots) else 2
            Particle_DC = "pip" if("pip"  in plots) else "ele"
            Layer_DC    = 6     if("DC_6" in plots) else 18    if("DC_18" in plots) else 36
            rdf = rdf.Define(f'{plots}', f'DC_Spherical_Coordinates({Particle_DC}_x_DC_{Layer_DC}, {Particle_DC}_y_DC_{Layer_DC}, {Particle_DC}_z_DC_{Layer_DC}, {Coordinate})')
            mdf = mdf.Define(f'{plots}', f'DC_Spherical_Coordinates({Particle_DC}_x_DC_{Layer_DC}, {Particle_DC}_y_DC_{Layer_DC}, {Particle_DC}_z_DC_{Layer_DC}, {Coordinate})')
    print(f"{color.BOLD}Done adding Drift Chamber Angles\n{color.END}")

print("\nAdding (Initial) Cuts to RDataFrames...\n")


if(args.limit_range):
    print(f"{color.Error}Applying an Event Limit ({args.limit_range} events) to the RDataFrames{color.END}")
    rdf = rdf.Range(args.limit_range)
    mdf = mdf.Range(args.limit_range)
rdf_cut = rdf
mdf_cut = mdf
for cut in List_of_Cuts:
    rdf_cut = rdf_cut.Filter(cut)
    mdf_cut = mdf_cut.Filter(cut)


rdf_cut = rdf_cut.Filter("Complete_SIDIS_Cuts && Valerii_OG_Cut && Valerii_PCal_Fiducial_Cuts")
mdf_cut = mdf_cut.Filter("Complete_SIDIS_Cuts && Valerii_OG_Cut && Valerii_PCal_Fiducial_Cuts")

print("\nAdding (Test) Cuts to RDataFrames...\n")

rdf_cut_2 = rdf_cut
mdf_cut_2 = mdf_cut

# rdf_cut_2 = rdf_cut.Filter("Complete_SIDIS_Cuts && Valerii_DC_Fiducial_Cuts_ele_DC_6 && Valerii_DC_Fiducial_Cuts_ele_DC_18 && Valerii_DC_Fiducial_Cuts_ele_DC_36 && Valerii_DC_Fiducial_Cuts_pip_DC_6 && Valerii_DC_Fiducial_Cuts_pip_DC_18 && Valerii_DC_Fiducial_Cuts_pip_DC_36 && Valerii_OG_Cut && Valerii_PCal_Fiducial_Cuts")
# mdf_cut_2 = mdf_cut.Filter("Complete_SIDIS_Cuts && Valerii_DC_Fiducial_Cuts_ele_DC_6 && Valerii_DC_Fiducial_Cuts_ele_DC_18 && Valerii_DC_Fiducial_Cuts_ele_DC_36 && Valerii_DC_Fiducial_Cuts_pip_DC_6 && Valerii_DC_Fiducial_Cuts_pip_DC_18 && Valerii_DC_Fiducial_Cuts_pip_DC_36 && Valerii_OG_Cut && Valerii_PCal_Fiducial_Cuts")
rdf_cut_2 = rdf_cut.Filter("Complete_SIDIS_Cuts && Valerii_DC_Fiducial_Cuts_ele_DC_6 && Valerii_DC_Fiducial_Cuts_ele_DC_18 && Valerii_DC_Fiducial_Cuts_ele_DC_36 && Valerii_OG_Cut && Valerii_PCal_Fiducial_Cuts")
mdf_cut_2 = mdf_cut.Filter("Complete_SIDIS_Cuts && Valerii_DC_Fiducial_Cuts_ele_DC_6 && Valerii_DC_Fiducial_Cuts_ele_DC_18 && Valerii_DC_Fiducial_Cuts_ele_DC_36 && Valerii_OG_Cut && Valerii_PCal_Fiducial_Cuts")

# rdf_cut_2 = Apply_Test_Fiducial_Cuts(Data_Frame_In=rdf_cut, List_of_Layers=["6", "18"], List_of_Particles=["pip"])
rdf_cut_2 = Apply_Test_Fiducial_Cuts(Data_Frame_In=rdf_cut, List_of_Layers=DC_Layer_List, List_of_Particles=["pip"])
# # rdf_cut_2 = Apply_Test_Fiducial_Cuts(Data_Frame_In=rdf_cut, List_of_Layers=DC_Layer_List, List_of_Particles=Particle_List)
# mdf_cut_2 = Apply_Test_Fiducial_Cuts(Data_Frame_In=mdf_cut, List_of_Layers=["6", "18"], List_of_Particles=["pip"])
mdf_cut_2 = Apply_Test_Fiducial_Cuts(Data_Frame_In=mdf_cut, List_of_Layers=DC_Layer_List, List_of_Particles=["pip"])
# # mdf_cut_2 = Apply_Test_Fiducial_Cuts(Data_Frame_In=mdf_cut, List_of_Layers=DC_Layer_List, List_of_Particles=Particle_List)

# rdf_cut_2 = rdf_cut_2.Filter("pipth > 6 && pipth < 30")
# mdf_cut_2 = mdf_cut_2.Filter("pipth > 6 && pipth < 30")

num_rdf_cut1_events = rdf_cut.Count().GetValue()
num_mdf_cut1_events = mdf_cut.Count().GetValue()
num_rdf_cut2_events = rdf_cut_2.Count().GetValue()
num_mdf_cut2_events = mdf_cut_2.Count().GetValue()

# Particle = "pip"
# DC_Layer = 6
# particle_angle = "pipPhi"
# # particle_angle = "pipth"
print("Starting loop through selected options...\n")
for         DC_Layer       in DC_Layer_List:
    DC_Layer = int(DC_Layer)
    for     Particle       in Particle_List:
        for particle_angle in P_Angle__List:
            if(("DC_" in particle_angle) and (f"DC_{DC_Layer}" not in particle_angle)):
                continue
            Angle_Bin_Nums = Phi___Bin_Nums if("th" not in particle_angle) else Theta_Bin_Nums
            Angle_MaxRange = Phi___MaxRange if("th" not in particle_angle) else Theta_MaxRange
            
            Particle_Title = "#pi^{+} Pion" if(Particle in ["pip"]) else "Electron"
            particle_angle_Title = "".join(["#phi" if("Phi" in particle_angle) else "#theta", "_{", "#pi^{+} Pion" if("pip" in particle_angle) else "Electron", "}"])
            if("DC_" in particle_angle):
                particle_angle_Title = f"DC {particle_angle_Title} (Layer {DC_Layer})"
        
            Sector = "All"
            # Sector = 3
            for Sector in Sector_List:
                if(Sector not in ["All", "0", 0]):
                    Sector = int(Sector)
                else:
                    Sector = "All"
                sector_cut = "esec != -2" if(str(Sector) in ["All", "0"]) else "".join(["esec" if(Particle not in ["pip"]) else "pipsec", " == ", str(Sector)])

                x_axis_DC_min, x_axis_DC_max     = -357, 357
                y_axis_DC_min, y_axis_DC_max     = -425, 425
                # y_axis_DC_min, y_axis_DC_max     = -400, 400
                
                
                if(Particle not in ["pip"]):
                    x_axis_DC_min, x_axis_DC_max         = -200, 200
                    y_axis_DC_min, y_axis_DC_max         = -100 - (50*int((DC_Layer/6)/3)), 100 + (50*int((DC_Layer/6)/3))
                else:
                    if(DC_Layer in [6]):
                        # x_axis_DC_min, x_axis_DC_max     = -150, 150
                        # y_axis_DC_min, y_axis_DC_max     = -175, 175
                        if(Sector == 1):
                            x_axis_DC_min, x_axis_DC_max =    0, 150
                            y_axis_DC_min, y_axis_DC_max = -100, 100
                        if(Sector == 2):
                            x_axis_DC_min, x_axis_DC_max = -50,  150
                            y_axis_DC_min, y_axis_DC_max =   0,  150
                        if(Sector == 3):
                            x_axis_DC_min, x_axis_DC_max = -150,  50
                            y_axis_DC_min, y_axis_DC_max =    0, 150
                        if(Sector == 4):
                            x_axis_DC_min, x_axis_DC_max = -150,   0
                            y_axis_DC_min, y_axis_DC_max = -100, 100
                        if(Sector == 5):
                            x_axis_DC_min, x_axis_DC_max = -150,  50
                            y_axis_DC_min, y_axis_DC_max = -160,   0
                        if(Sector == 6):
                            x_axis_DC_min, x_axis_DC_max =  -50, 150
                            y_axis_DC_min, y_axis_DC_max = -150,   0
                    if(DC_Layer in [18]):
                        # x_axis_DC_min, x_axis_DC_max     = -300, 300
                        # y_axis_DC_min, y_axis_DC_max     = -300, 300
                        if(Sector in [1]):
                            x_axis_DC_min, x_axis_DC_max = -5,   300
                            y_axis_DC_min, y_axis_DC_max = -200, 200
                        if(Sector in [2]):
                            x_axis_DC_min, x_axis_DC_max = -5,   300
                            y_axis_DC_min, y_axis_DC_max = -5,   300
                        if(Sector in [3]):
                            x_axis_DC_min, x_axis_DC_max = -300,   5
                            y_axis_DC_min, y_axis_DC_max = -5,   300
                        if(Sector in [4]):
                            x_axis_DC_min, x_axis_DC_max = -300,   5
                            y_axis_DC_min, y_axis_DC_max = -200, 200
                        if(Sector in [5]):
                            x_axis_DC_min, x_axis_DC_max = -300,   5
                            y_axis_DC_min, y_axis_DC_max = -300,   5
                        if(Sector in [6]):
                            x_axis_DC_min, x_axis_DC_max = -5,   275
                            y_axis_DC_min, y_axis_DC_max = -250,   5
                    if(DC_Layer in [36]):
                        # x_axis_DC_min, x_axis_DC_max     = -500, 500
                        # y_axis_DC_min, y_axis_DC_max     = -500, 500
                        if(Sector in [1]):
                            x_axis_DC_min, x_axis_DC_max = -5,   500
                            y_axis_DC_min, y_axis_DC_max = -200, 200
                        if(Sector in [2]):
                            x_axis_DC_min, x_axis_DC_max = -5,   500
                            y_axis_DC_min, y_axis_DC_max = -5,   500
                        if(Sector in [3]):
                            x_axis_DC_min, x_axis_DC_max = -500,   5
                            y_axis_DC_min, y_axis_DC_max = -5,   500
                        if(Sector in [4]):
                            x_axis_DC_min, x_axis_DC_max = -500,   5
                            y_axis_DC_min, y_axis_DC_max = -200, 200
                        if(Sector in [5]):
                            x_axis_DC_min, x_axis_DC_max = -500,   5
                            y_axis_DC_min, y_axis_DC_max = -500,   5
                        if(Sector in [6]):
                            x_axis_DC_min, x_axis_DC_max = -5,   500
                            y_axis_DC_min, y_axis_DC_max = -500,   5
                # print(f"y_axis_DC_min, y_axis_DC_max     = {y_axis_DC_min}, {y_axis_DC_max}")
                for hist_type      in DC_Coordinate:
                    if(("DC_" in particle_angle) and (str(hist_type) not in ["2D"])):
                        continue
                    
                    histo_name_rdf = f"RDF_{Particle}_{hist_type}_DC_Layer_{DC_Layer}_Main_{particle_angle}"
                    histo_name_mdf = f"MDF_{Particle}_{hist_type}_DC_Layer_{DC_Layer}_Main_{particle_angle}"
                    if(str(Sector) not in ["All"]):
                        histo_name_rdf = f"{histo_name_rdf}_Sector_{Sector}"
                        histo_name_mdf = f"{histo_name_mdf}_Sector_{Sector}"
                    print(f"{color.BOLD}\nCreating Histograms for histo_name_rdf = {color.UNDERLINE}{histo_name_rdf}{color.END}\n")
                    
                    if(hist_type in ["2D"]):
                        histograms[f"{histo_name_rdf}____Drift_Chamber"] = (rdf_cut.Filter(str(sector_cut))).Histo2D((f"{histo_name_rdf}____Drift_Chamber", f"#splitline{{#splitline{{#scale[2.25]{{Experimental Hits in Drift Chamber}}}}{{#scale[2.25]{{{Particle_Title} Layer {DC_Layer}}}}}}}{{#scale[2]{{Before Applying the (New) DC Fiducial Cuts}}}}; {Particle_Title} DC_{{x}} [cm]; {Particle_Title} DC_{{y}} [cm]", DC_2D_Bin_Nums, -425, 425, DC_2D_Bin_Nums, -425, 425), f"{Particle}_x_DC_{DC_Layer}", f"{Particle}_y_DC_{DC_Layer}")
                        histograms[f"{histo_name_mdf}____Drift_Chamber"] = (mdf_cut.Filter(str(sector_cut))).Histo2D((f"{histo_name_mdf}____Drift_Chamber", f"#splitline{{#splitline{{#scale[2.25]{{Monte Carlo Hits in Drift Chamber}}}}{{#scale[2.25]{{{Particle_Title} Layer {DC_Layer}}}}}}}{{#scale[2]{{Before Applying the (New) DC Fiducial Cuts}}}}; {Particle_Title} DC_{{x}} [cm]; {Particle_Title} DC_{{y}} [cm]",  DC_2D_Bin_Nums, -425, 425, DC_2D_Bin_Nums, -425, 425), f"{Particle}_x_DC_{DC_Layer}", f"{Particle}_y_DC_{DC_Layer}")
                        histograms[f"{histo_name_rdf}____Drift_Chamber"].GetXaxis().SetRangeUser(x_axis_DC_min, x_axis_DC_max)
                        histograms[f"{histo_name_rdf}____Drift_Chamber"].GetYaxis().SetRangeUser(y_axis_DC_min, y_axis_DC_max)
                        histograms[f"{histo_name_mdf}____Drift_Chamber"].GetXaxis().SetRangeUser(x_axis_DC_min, x_axis_DC_max)
                        histograms[f"{histo_name_mdf}____Drift_Chamber"].GetYaxis().SetRangeUser(y_axis_DC_min, y_axis_DC_max)
                    else:
                        histograms[f"{histo_name_rdf}____Drift_Chamber"] = (rdf_cut.Filter(str(sector_cut))).Histo1D((f"{histo_name_rdf}_{hist_type}___DC", f"#splitline{{#scale[2]{{{Particle_Title} DC_{{{hist_type}}} Layer {DC_Layer} {root_color.Bold}{{(Before Cuts)}}}}}}{{#scale[1.8]{{#splitline{{#color[{ROOT.kBlue}]{{Experimental Data Distribution}}}}{{#color[{ROOT.kRed}]{{Monte Carlo Distribution}}}}}}}}; {Particle_Title} DC_{{ {hist_type} }} [cm]; Normalized", DC_2D_Bin_Nums, -425, 425), f"{Particle}_{hist_type}_DC_{DC_Layer}")
                        histograms[f"{histo_name_mdf}____Drift_Chamber"] = (mdf_cut.Filter(str(sector_cut))).Histo1D((f"{histo_name_mdf}_{hist_type}___DC", f"#splitline{{#scale[2]{{{Particle_Title} DC_{{{hist_type}}} Layer {DC_Layer} {root_color.Bold}{{(Before Cuts)}}}}}}{{#scale[1.8]{{#splitline{{#color[{ROOT.kBlue}]{{Experimental Data Distribution}}}}{{#color[{ROOT.kRed}]{{Monte Carlo Distribution}}}}}}}}; {Particle_Title} DC_{{ {hist_type} }} [cm]; Normalized", DC_2D_Bin_Nums, -425, 425), f"{Particle}_{hist_type}_DC_{DC_Layer}")
                        histograms[f"{histo_name_rdf}____Drift_Chamber"] = histograms[f"{histo_name_rdf}____Drift_Chamber"].GetValue()
                        histograms[f"{histo_name_rdf}____Drift_Chamber"].SetLineColor(ROOT.kBlue)
                        histograms[f"{histo_name_mdf}____Drift_Chamber"] = histograms[f"{histo_name_mdf}____Drift_Chamber"].GetValue()
                        histograms[f"{histo_name_mdf}____Drift_Chamber"].SetLineColor(ROOT.kRed)

                    histograms[f"{histo_name_rdf}_{particle_angle}"] = (rdf_cut.Filter(str(sector_cut))).Histo1D((f"{histo_name_rdf}_{particle_angle}", "rdf (angle) Title", Angle_Bin_Nums, 0, Angle_MaxRange), str(particle_angle))
                    histograms[f"{histo_name_rdf}_{particle_angle}"] = histograms[f"{histo_name_rdf}_{particle_angle}"].GetValue()
                    histograms[f"{histo_name_rdf}_{particle_angle}"].SetLineColor(ROOT.kBlue)
                    histograms[f"{histo_name_mdf}_{particle_angle}"] = (mdf_cut.Filter(str(sector_cut))).Histo1D((f"{histo_name_mdf}_{particle_angle}", "mdf (angle) Title", Angle_Bin_Nums, 0, Angle_MaxRange), str(particle_angle))
                    histograms[f"{histo_name_mdf}_{particle_angle}"] = histograms[f"{histo_name_mdf}_{particle_angle}"].GetValue()
                    histograms[f"{histo_name_mdf}_{particle_angle}"].SetLineColor(ROOT.kRed)
                    
                    Normalize_Histogram(histograms[f"{histo_name_rdf}____Drift_Chamber"], set_total=num_rdf_cut1_events)
                    Normalize_Histogram(histograms[f"{histo_name_rdf}_{particle_angle}"], set_total=num_rdf_cut1_events)
                    Normalize_Histogram(histograms[f"{histo_name_mdf}____Drift_Chamber"], set_total=num_mdf_cut1_events)
                    Normalize_Histogram(histograms[f"{histo_name_mdf}_{particle_angle}"], set_total=num_mdf_cut1_events)
                    
                    histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"]     = histograms[f"{histo_name_rdf}____Drift_Chamber"].Clone(f"{histo_name_rdf}____Drift_Chamber_ratio")
                    if(hist_type not in ["2D"]):
                        histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].Add(histograms[f"{histo_name_mdf}____Drift_Chamber"], -1)
                        histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].Divide(histograms[f"{histo_name_rdf}____Drift_Chamber"])
                        histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].Scale(100)
                        histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].SetLineColor(ROOT.kBlack)
                    else:
                        histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"] = Ratio_of_2D_Histos(out_hist=histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"], rdf_hist=histograms[f"{histo_name_rdf}____Drift_Chamber"], mdf_hist=histograms[f"{histo_name_mdf}____Drift_Chamber"])
                    
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"] = histograms[f"{histo_name_rdf}_{particle_angle}"].Clone(f"{histo_name_rdf}_{particle_angle}_ratio")
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].Add(histograms[f"{histo_name_mdf}_{particle_angle}"], -1)
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].Divide(histograms[f"{histo_name_rdf}_{particle_angle}"])
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].Scale(100)
                    
                    if(hist_type in ["2D"]):
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"] = (rdf_cut_2.Filter(str(sector_cut))).Histo2D((f"{histo_name_rdf}_After_Cut____Drift_Chamber", f"#splitline{{#splitline{{#scale[2.25]{{Experimental Hits in Drift Chamber}}}}{{#scale[2.25]{{{Particle_Title} Layer {DC_Layer}}}}}}}{{#scale[2]{{AFTER Applying the (New) DC Fiducial Cuts}}}}; {Particle_Title} DC_{{x}} [cm]; {Particle_Title} DC_{{y}} [cm]", DC_2D_Bin_Nums, -425, 425, DC_2D_Bin_Nums, -425, 425), f"{Particle}_x_DC_{DC_Layer}", f"{Particle}_y_DC_{DC_Layer}")
                        histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"] = (mdf_cut_2.Filter(str(sector_cut))).Histo2D((f"{histo_name_mdf}_After_Cut____Drift_Chamber", f"#splitline{{#splitline{{#scale[2.25]{{Monte Carlo Hits in Drift Chamber}}}}{{#scale[2.25]{{{Particle_Title} Layer {DC_Layer}}}}}}}{{#scale[2]{{AFTER Applying the (New) DC Fiducial Cuts}}}}; {Particle_Title} DC_{{x}} [cm]; {Particle_Title} DC_{{y}} [cm]",  DC_2D_Bin_Nums, -425, 425, DC_2D_Bin_Nums, -425, 425), f"{Particle}_x_DC_{DC_Layer}", f"{Particle}_y_DC_{DC_Layer}")
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"].GetXaxis().SetRangeUser(x_axis_DC_min, x_axis_DC_max)
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"].GetYaxis().SetRangeUser(y_axis_DC_min, y_axis_DC_max)
                        histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"].GetXaxis().SetRangeUser(x_axis_DC_min, x_axis_DC_max)
                        histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"].GetYaxis().SetRangeUser(y_axis_DC_min, y_axis_DC_max)
                    else:
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"] = (rdf_cut_2.Filter(str(sector_cut))).Histo1D((f"{histo_name_rdf}_{hist_type}_After_Cut_____DC", f"#splitline{{#scale[2]{{{Particle_Title} DC_{{{hist_type}}} Layer {DC_Layer} {root_color.Bold}{{(After Cuts)}}}}}}{{#scale[1.8]{{#splitline{{#color[{ROOT.kBlue}]{{Experimental Data Distribution}}}}{{#color[{ROOT.kRed}]{{Monte Carlo Distribution}}}}}}}}; {Particle_Title} DC_{{ {hist_type} }} [cm]; Normalized", DC_2D_Bin_Nums, -425, 425), f"{Particle}_{hist_type}_DC_{DC_Layer}")
                        histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"] = (mdf_cut_2.Filter(str(sector_cut))).Histo1D((f"{histo_name_mdf}_{hist_type}_After_Cut_____DC", f"#splitline{{#scale[2]{{{Particle_Title} DC_{{{hist_type}}} Layer {DC_Layer} {root_color.Bold}{{(After Cuts)}}}}}}{{#scale[1.8]{{#splitline{{#color[{ROOT.kBlue}]{{Experimental Data Distribution}}}}{{#color[{ROOT.kRed}]{{Monte Carlo Distribution}}}}}}}}; {Particle_Title} DC_{{ {hist_type} }} [cm]; Normalized", DC_2D_Bin_Nums, -425, 425), f"{Particle}_{hist_type}_DC_{DC_Layer}")
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"] = histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"].GetValue()
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"].SetLineColor(ROOT.kBlue)
                        histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"] = histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"].GetValue()
                        histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"].SetLineColor(ROOT.kRed)
                    
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"] = (rdf_cut_2.Filter(str(sector_cut))).Histo1D((f"{histo_name_rdf}_After_Cut_{particle_angle}", "rdf (angle) Title - AFTER CUTS", Angle_Bin_Nums, 0, Angle_MaxRange), str(particle_angle))
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"] = histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"].GetValue()
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"].SetLineColor(ROOT.kBlue)
                    histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"] = (mdf_cut_2.Filter(str(sector_cut))).Histo1D((f"{histo_name_mdf}_After_Cut_{particle_angle}", "mdf (angle) Title - AFTER CUTS", Angle_Bin_Nums, 0, Angle_MaxRange), str(particle_angle))
                    histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"] = histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"].GetValue()
                    histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"].SetLineColor(ROOT.kRed)
                    
                    Normalize_Histogram(histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"], set_total=num_rdf_cut2_events)
                    Normalize_Histogram(histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"], set_total=num_rdf_cut2_events)
                    Normalize_Histogram(histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"], set_total=num_mdf_cut2_events)
                    Normalize_Histogram(histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"], set_total=num_mdf_cut2_events)
                    
                    histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"]     = histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"].Clone(f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio")
                    if(hist_type not in ["2D"]):
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].Add(histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"], -1)
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].Divide(histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"])
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].Scale(100)
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].SetLineColor(ROOT.kGreen)
                    else:
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"] = Ratio_of_2D_Histos(out_hist=histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"], rdf_hist=histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"], mdf_hist=histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"])
                    
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"] = histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"].Clone(f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio")
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].Add(histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"], -1)
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].Divide(histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"])
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].Scale(100)
                    
                    
                    print("\nCreating TCanvas...\n")
                    
                    canvas[histo_name_rdf] = Canvas_Create(Name=f"canvas_{histo_name_rdf}", Num_Columns=1, Num_Rows=3, Size_X=2400, Size_Y=1800, cd_Space=0)
                    canvas[histo_name_rdf].SetFillColor(17)  # Color index 17 corresponds to a light grey color
                    
                    canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"] = canvas[histo_name_rdf].cd(1)
                    canvas[f"{histo_name_rdf}_cd_After__New_Cuts"] = canvas[histo_name_rdf].cd(2)
                    canvas[f"{histo_name_rdf}_cd_SamePadNew_Cuts"] = canvas[histo_name_rdf].cd(3)
                    
                    Plot_All_Q = not False
                    
                    canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].SetPad(0.05, 0.545, 0.95, 0.95)
                    canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].SetPad(0.05, 0.05,  0.95, 0.555)
                    canvas[f"{histo_name_rdf}_cd_SamePadNew_Cuts"].SetPad(0.78 if(Plot_All_Q) else 0.71, 0.3, 0.9, 0.8)

                    canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].Divide(6 if(Plot_All_Q) else 4, 1, 0.01, 0.01)
                    canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].Divide(6 if(Plot_All_Q) else 4, 1, 0.01, 0.01)
                    
                    # canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].Divide((6 if(Plot_All_Q) else 4) if((hist_type in ["2D"]) or (Plot_All_Q)) else 5, 1, 0.01, 0.01)
                    # canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].Divide((6 if(Plot_All_Q) else 4) if((hist_type in ["2D"]) or (Plot_All_Q)) else 5, 1, 0.01, 0.01)
                    
                    set_common_yaxis_range(histograms[f"{histo_name_rdf}_{particle_angle}_ratio"], histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"])
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].SetLineColor(ROOT.kBlack)
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].SetLineColor(ROOT.kGreen)
                    
                    set_common_yaxis_range(histograms[f"{histo_name_rdf}_{particle_angle}_ratio"],     histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"])
                    set_common_yaxis_range(histograms[f"{histo_name_rdf}_{particle_angle}"],           histograms[f"{histo_name_mdf}_{particle_angle}"], histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"], histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"])
                    if(hist_type not in ["2D"]):
                        set_common_yaxis_range(histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"], histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"])
                        set_common_yaxis_range(histograms[f"{histo_name_rdf}____Drift_Chamber"],       histograms[f"{histo_name_mdf}____Drift_Chamber"], histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"], histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"])
                        histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].SetTitle(f"#splitline{{#scale[2]{{#splitline{{% Diff in Drift Chamber (Layer {DC_Layer})}}{{Comparison Between Data and MC}}}}}}{{#scale[1.8]{{#splitline{{{root_color.Bold}{{Before (New) DC Cuts}}}}{{#color[{ROOT.kGreen}]{{After (New) DC Cuts}}}}}}}}")
                    else:                
                        histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].SetTitle(f"#splitline{{#splitline{{#scale[2.5]{{% Diff in Drift Chamber (Layer {DC_Layer})}}}}{{#scale[1.5]{{Comparison of Data/MC Hits of the {Particle_Title}}}}}}}{{#scale[2]{{Before Applying the (New) DC Fiducial Cuts}}}}")
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].SetTitle(f"#splitline{{#splitline{{#scale[2.5]{{% Diff in Drift Chamber (Layer {DC_Layer})}}}}{{#scale[1.5]{{Comparison of Data/MC Hits of the {Particle_Title}}}}}}}{{#scale[2]{{After Applying the (New) DC Fiducial Cuts}}}}")
                    
                    histograms[f"{histo_name_rdf}_{particle_angle}"].SetTitle(f"#splitline{{#scale[2]{{Lab {particle_angle_Title} Angle {root_color.Bold}{{(Before Cuts)}}}}}}{{#scale[1.8]{{#splitline{{#color[{ROOT.kBlue}]{{Experimental Data Distribution}}}}{{#color[{ROOT.kRed}]{{Monte Carlo Distribution}}}}}}}}")
                    histograms[f"{histo_name_mdf}_{particle_angle}"].SetTitle(f"#splitline{{#scale[2]{{Lab {particle_angle_Title} Angle {root_color.Bold}{{(Before Cuts)}}}}}}{{#scale[1.8]{{#splitline{{#color[{ROOT.kBlue}]{{Experimental Data Distribution}}}}{{#color[{ROOT.kRed}]{{Monte Carlo Distribution}}}}}}}}")
                    
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"].SetTitle(f"#splitline{{#scale[2]{{Lab {particle_angle_Title} Angle {root_color.Bold}{{(After Cuts)}}}}}}{{#scale[1.8]{{#splitline{{#color[{ROOT.kBlue}]{{Experimental Data Distribution}}}}{{#color[{ROOT.kRed}]{{Monte Carlo Distribution}}}}}}}}")
                    histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"].SetTitle(f"#splitline{{#scale[2]{{Lab {particle_angle_Title} Angle {root_color.Bold}{{(After Cuts)}}}}}}{{#scale[1.8]{{#splitline{{#color[{ROOT.kBlue}]{{Experimental Data Distribution}}}}{{#color[{ROOT.kRed}]{{Monte Carlo Distribution}}}}}}}}")
                    
                    histograms[f"{histo_name_rdf}_{particle_angle}"].GetYaxis().SetTitle("Normalized")
                    histograms[f"{histo_name_mdf}_{particle_angle}"].GetYaxis().SetTitle("Normalized")
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"].GetYaxis().SetTitle("Normalized")
                    histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"].GetYaxis().SetTitle("Normalized")
                    
                    histograms[f"{histo_name_rdf}_{particle_angle}"].GetXaxis().SetTitle(f"{particle_angle_Title} [#circ]")
                    histograms[f"{histo_name_mdf}_{particle_angle}"].GetXaxis().SetTitle(f"{particle_angle_Title} [#circ]")
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"].GetXaxis().SetTitle(f"{particle_angle_Title} [#circ]")
                    histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"].GetXaxis().SetTitle(f"{particle_angle_Title} [#circ]")
                    
                    
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].SetTitle(f"#splitline{{#scale[2]{{#splitline{{% Diff of Lab {particle_angle_Title} Angle}}{{Comparison Between Data and MC}}}}}}{{#scale[1.8]{{#splitline{{{root_color.Bold}{{Before (New) DC Cuts}}}}{{#color[{ROOT.kGreen}]{{After (New) DC Cuts}}}}}}}}")
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].SetTitle(f"#splitline{{#scale[2]{{#splitline{{% Diff of Lab {particle_angle_Title} Angle}}{{Comparison Between Data and MC}}}}}}{{#scale[1.8]{{#splitline{{{root_color.Bold}{{Before (New) DC Cuts}}}}{{#color[{ROOT.kGreen}]{{After (New) DC Cuts}}}}}}}}")
                    
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].GetYaxis().SetTitle("% Difference")
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].GetYaxis().SetTitle("% Difference")
                    
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].GetXaxis().SetTitle(f"{particle_angle_Title} [#circ]")
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].GetXaxis().SetTitle(f"{particle_angle_Title} [#circ]")
                    
                    if(Plot_All_Q):
                        canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].cd(1)
                        histograms[f"{histo_name_rdf}____Drift_Chamber"].Draw("colz"             if(hist_type  in ["2D"]) else "hist EO same")
                        ROOT.gPad.SetLogz(0)
                        canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].cd(2                      if(hist_type  in ["2D"]) else 1)
                        histograms[f"{histo_name_mdf}____Drift_Chamber"].Draw("colz"             if(hist_type  in ["2D"]) else "hist EO same")
                        ROOT.gPad.SetLogz(0)
                    canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].cd((3 if(Plot_All_Q) else 1)  if((hist_type in ["2D"]) or (not Plot_All_Q)) else 2)
                    histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].Draw("colz"           if(hist_type  in ["2D"]) else "hist EO same")
                    if(hist_type in ["2D"]):
                        palette_move(canvas=canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"], histo=histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
                    ROOT.gPad.SetLogz(1)
                    if((hist_type not in ["2D"]) and Plot_All_Q):
                        canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].cd(3)
                        histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].Draw("hist EO same")
                        ROOT.gPad.SetLogz(1)
                    canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].cd(4 if(Plot_All_Q) else 2)
                    histograms[f"{histo_name_rdf}_{particle_angle}"].Draw("hist EO same")
                    histograms[f"{histo_name_mdf}_{particle_angle}"].Draw("hist EO same")
                    canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].cd(5 if(Plot_All_Q) else 3)
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].Draw("hist EO same")
                    
                    if(Plot_All_Q):
                        canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].cd(1)
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber"].Draw("colz"   if(hist_type  in ["2D"]) else "hist EO same")
                        ROOT.gPad.SetLogz(0)
                        canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].cd(2                      if(hist_type  in ["2D"]) else 1)
                        histograms[f"{histo_name_mdf}_After_Cut____Drift_Chamber"].Draw("colz"   if(hist_type  in ["2D"]) else "hist EO same")
                        ROOT.gPad.SetLogz(0)
                    canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].cd((3 if(Plot_All_Q) else 1)  if((hist_type in ["2D"]) or (not Plot_All_Q)) else 2)
                    histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].Draw("colz" if(hist_type  in ["2D"]) else "hist EO same")
                    if(hist_type in ["2D"]):
                        palette_move(canvas=canvas[f"{histo_name_rdf}_cd_After__New_Cuts"], histo=histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
                    ROOT.gPad.SetLogz(1)
                    if((hist_type not in ["2D"]) and Plot_All_Q):
                        canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].cd(3)
                        histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].Draw("hist EO same")
                        ROOT.gPad.SetLogz(1)
                    canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].cd(4 if(Plot_All_Q) else 2)
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}"].Draw("hist EO same")
                    histograms[f"{histo_name_mdf}_After_Cut_{particle_angle}"].Draw("hist EO same")
                    canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].cd(5 if(Plot_All_Q) else 3)
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].Draw("hist EO same")
                    
                    canvas[histo_name_rdf].cd(3)
                    canvas[histo_name_rdf].cd(3).SetTopMargin(0.05)
                    histograms[f"{histo_name_rdf}_{particle_angle}_ratio"].Draw("hist EO same")
                    histograms[f"{histo_name_rdf}_After_Cut_{particle_angle}_ratio"].Draw("hist EO same")
                    
                    canvas[histo_name_rdf].Update()
    
                    if(hist_type in ["2D"]):
                        CD_NUM_List = [1, 2, 3] if(Plot_All_Q) else [1]
                        list_of_lines = []
                        list_of_lines.append(polygon_all["".join(["Layer_", str(DC_Layer), "_", "" if (DC_Layer not in [6]) else "_", str(Particle)])])
                        for CD_NUM in CD_NUM_List:
                            try:
                                for ii, polygon_ii in enumerate(list_of_lines):
                                    n_points = len(polygon_ii)
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_Before"] = ROOT.TPolyLine(n_points + 1)
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}__After"] = ROOT.TPolyLine(n_points + 1)
                                    for i, (x, y) in enumerate(polygon_ii):
                                        pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_Before"].SetPoint(i, x, y)
                                        pl[f"{histo_name_rdf}_{CD_NUM}_{ii}__After"].SetPoint(i, x, y)
                                        # print(f"x, y = {x}, {y}")
                                    # Close the shape by repeating the first point
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_Before"].SetPoint(n_points, polygon_ii[0][0], polygon_ii[0][1])
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_Before"].SetLineColor(2)  # Red color
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_Before"].SetLineWidth(1)
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}__After"].SetPoint(n_points, polygon_ii[0][0], polygon_ii[0][1])
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}__After"].SetLineColor(2)  # Red color
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}__After"].SetLineWidth(1)
                                    canvas[f"{histo_name_rdf}_cd_Before_New_Cuts"].cd(CD_NUM)
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_Before"].Draw("same")
                                    canvas[f"{histo_name_rdf}_cd_After__New_Cuts"].cd(CD_NUM)
                                    pl[f"{histo_name_rdf}_{CD_NUM}_{ii}__After"].Draw("same")
                                canvas[histo_name_rdf].Update()
                            except:
                                print("ERROR in box.Draw('same')")
                                print(f"{color.Error}TRACEBACK:\n{color.END_B}{str(traceback.format_exc())}{color.END}")
                    
                        print("\nDrawing TCanvas...\n")
                        
                        # canvas[histo_name_rdf].Draw()
                        canvas[histo_name_rdf].Update()
                    
                    
                    
                    # canvas[f"canvas_{histo_name_rdf}_DC"] = Canvas_Create(Name=f"canvas_{histo_name_rdf}_DC", Num_Columns=2, Num_Rows=1, Size_X=1800, Size_Y=1600, cd_Space=0.01)
                    # canvas[f"canvas_{histo_name_rdf}_DC"].SetFillColor(17)  # Color index 17 corresponds to a light grey color
                    
                    # canvas[f"canvas_{histo_name_rdf}_DC"].cd(1).SetPad(0.1,   0.1, 0.495, 0.9)
                    # canvas[f"canvas_{histo_name_rdf}_DC"].cd(2).SetPad(0.505, 0.1, 0.9,   0.9)
                    
                    # canvas[f"canvas_{histo_name_rdf}_DC"].cd(1)
                    # # Draw_Canvas(canvas[f"canvas_{histo_name_rdf}_DC"], 1, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1)
                    # histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].Draw("colz")
                    # histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].GetXaxis().SetRangeUser(x_axis_DC_min, x_axis_DC_max)
                    # histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"].GetYaxis().SetRangeUser(y_axis_DC_min, y_axis_DC_max)
                    # ROOT.gPad.SetLogz(1)
                    # palette_move(canvas=canvas[f"canvas_{histo_name_rdf}_DC"], histo=histograms[f"{histo_name_rdf}____Drift_Chamber_ratio"],           x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
                    
                    # # canvas[f"canvas_{histo_name_rdf}_DC"].cd(2)
                    # # # Draw_Canvas(canvas[f"canvas_{histo_name_rdf}_DC"], 2, left_add=0.05, right_add=0.05, up_add=0.1, down_add=0.1)
                    # # histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].Draw("colz")
                    # # histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].GetXaxis().SetRangeUser(x_axis_DC_min, x_axis_DC_max)
                    # # histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"].GetYaxis().SetRangeUser(y_axis_DC_min, y_axis_DC_max)
                    # # palette_move(canvas=canvas[f"canvas_{histo_name_rdf}_DC"], histo=histograms[f"{histo_name_rdf}_After_Cut____Drift_Chamber_ratio"], x_left=0.905, x_right=0.925, y_up=0.9, y_down=0.1)
                    
                    # # for CD_NUM in [1, 2]:
                    # for CD_NUM in [1]:
                    #     try:
                    #         for ii, polygon_ii in enumerate(quadrilaterals):
                    #             n_points = len(polygon_ii)
                    #             pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_DC"] = ROOT.TPolyLine(n_points + 1)
                    #             for i, (x, y) in enumerate(polygon_ii):
                    #                 pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_DC"].SetPoint(i, x, y)
                    #             # Close the shape by repeating the first point
                    #             pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_DC"].SetPoint(n_points, polygon_ii[0][0], polygon_ii[0][1])
                    #             pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_DC"].SetLineColor(2)  # Red color
                    #             pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_DC"].SetLineWidth(1)
                    #             canvas[f"canvas_{histo_name_rdf}_DC"].cd(CD_NUM)
                    #             pl[f"{histo_name_rdf}_{CD_NUM}_{ii}_DC"].Draw("same")
                    #         canvas[f"canvas_{histo_name_rdf}_DC"].Update()
                    #     except:
                    #         print("ERROR in box.Draw('same')")
                    
                    # canvas[f"canvas_{histo_name_rdf}_DC"].Draw()
                    # canvas[f"canvas_{histo_name_rdf}_DC"].Update()
                    
                    # canvas[histo_name_rdf].Draw()
                    # canvas[histo_name_rdf].Update()
                    
                    
                    # print(str("".join([color.BOLD, """
                    
                    # auto Polygon_Layers = std::map<std::string, std::vector<std::pair<double, double>>>{
                    # \t""", str(str(str(str(str(str(str(polygon).replace("[", "{")).replace("], 'Lay", "}},\n\t{'Lay")).replace("]", "}")).replace(":", ",")).replace("(", "{")).replace(")", "}")).replace(", ", ", "), """
                    # };""", color.END])).replace("'", '"'))
        


for canvas_name in canvas:
    if("cd" not in str(canvas_name)):
        # Save_Name = f"{canvas_name}.root"
        Save_Name = f"{canvas_name}.png"
        # Save_Name = str(str(Save_Name).replace("RDF", "New_Fiducial_Cut_Test")).replace("_Main", "")
        # Save_Name = str(str(Save_Name).replace("RDF", "New_Theta_Cut_Test")).replace("_Main", "")
        Save_Name = str(str(Save_Name).replace("RDF", "DC_Fixed_Tests")).replace("_Main", "")
        print(f"{color.BBLUE}Saving: {color.END_B}{Save_Name}{color.END}\n")
        canvas[str(canvas_name)].SaveAs(Save_Name)

# End Time
end_time = datetime.now()
print(f"\nThe time that this code finished is {color.BOLD}{color.UNDERLINE}{format_time(end_time)}{color.END}")
# Time Difference
time_diff = end_time - start_time
days,  remainder = divmod(time_diff.seconds, 86400)  # 86400 seconds in a day
hours, remainder = divmod(remainder, 3600)          # 3600 seconds in an hour
minutes, seconds = divmod(remainder, 60)            # 60 seconds in a minute
# Print Total Time
print(f"""\n{color.BGREEN}The total time the code took to run the given files is:{color.END_B}
    {days} Day(s), {hours} Hour(s), {minutes} Minute(s), and {seconds} Second(s){color.END}""")

print("\n\nDone")
