#!/usr/bin/env python3
import sys
import argparse

parser = argparse.ArgumentParser(description="Make Comparisons between Data, clasdis MC, and EvGen MC (based on Using_RDataFrames.ipynb)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-kc', '--kinematic-compare',              action='store_true', 
                    help='Runs Kinematic Comparisons')
parser.add_argument('-ac', '--acceptance-all',                 action='store_true', 
                    help='Runs Acceptance Comparisons (no binning)')
parser.add_argument('-ab', '--acceptance',                     action='store_true', 
                    help='Runs Binned Acceptance Comparisons (for all kinematic bins)')
parser.add_argument('-abr', '--acceptance-ratio',              action='store_true', 
                    help='Similar to "-ab", but plots the ratios of the acceptances to show discrepancies')
parser.add_argument('-abd', '--acceptance-diff',               action='store_true', 
                    help='Similar to "-ab" and "-abr", but plots the percent difference between the acceptances to show discrepancies')
parser.add_argument('-v',  '--verbose',                        action='store_true', 
                    help='Prints more info while running')
parser.add_argument('-c',  '--cut',                            type=str,
                    help='Adds additional cuts based on user input (Warning: applies to all datasets)')
parser.add_argument('-sf', '--File_Save_Format',               type=str,    default=".png", choices=['.png', '.pdf'],
                    help='Save Format of Images')
parser.add_argument('-n', '--name',                            type=str,
                    help='Extra save name that can be added to the saved images')
parser.add_argument('-t', '--title',                           type=str,
                    help='Extra title text that can be added to the default titles')
parser.add_argument('-nrdf', '--num-rdf-files',                type=int,    default=5,
                    help='Number of rdf RDataFrames to be included')
parser.add_argument('-nMC', '--num-MC-files',                  type=int,    default=1,
                    help='Number of MC RDataFrames (MC REC and MC GEN) to be included — Can set to -1 to include all available files')
parser.add_argument('-bID', '--batch_id',                      type=int,    default=None, 
                    help="Uses pre-defined groups of data and (clasdis) MC files (other way of controlling `-nrdf` and `-nMC` — groups defined as of 11/14/2025 — Maximum Group Number: 57)")
parser.add_argument('-evnL', '--event_limit',                  type=int,
                    help="Event limit for all datasets (will set df.Range(...) based on this value, so only use if you don't want/need the full event statistics from the files — i.e., use for testing only)")
parser.add_argument('-NoEvGen', '--Do_not_use_EvGen',          action='store_true', 
                    help="Automatically turns off EvGen files (may cause some hard coded options to fail)")
parser.add_argument('-hMX', '--use_HIGH_MX',                   action='store_true',
                    help='Use with "-kc" option to normalize to High-Mx region')
# parser.add_argument('-2D', '--make_2D',                        action='store_true',
#                     help='Just Makes 2D Q2 vs y, Q2 vs xB, and z vs pT plots in different kinematic bins (rdf only) - Not finished')
parser.add_argument('-minA', '--min-accept-cut',               type=float, default=0.005,
                    help='Minimum Acceptance Cut. Applies to the acceptance histograms such that any bin with an acceptance below this cut is automatically set to 0 (does not work with `--make_2D_weight_binned_check` as of 11/4/2025)')
parser.add_argument('-MR', '--make_root',                      action='store_true',
                    help="Makes a ROOT output file like 'makeROOT_epip_SIDIS_histos_new.py' (but meant for fewer histograms per run — will update old files if the path given by `--root` already exists — in testing phase as of 11/10/2025)")
parser.add_argument('-vb', '--valerii_bins',                   action='store_true',
                    help="Runs code using Valerii's kinematic bins instead of mine (available only with the `--make_root` option as of 12/11/2025)")
parser.add_argument('-nohpp', '--do_not_use_hpp',              action='store_true',
                    help="Prevents the acceptance weights from being applied (with the '--make_root' option). Allows the JSON weights (injected modulations) to be applied without also needing the Acceptance weights.")
parser.add_argument('-aohpp', '--angles_only_hpp',             action='store_true',
                    help="Changes the acceptance weights being applied (with the '--make_root' option) so that only the azimuthal and polar angle weights are applied (no momentum weights).")
parser.add_argument('-r', '--root',                            type=str,   default="SIDIS_epip_All_File_Types_from_RDataFrames.root", 
                    help="Name of the ROOT file to be outputted by the '--make_root' option (will still append the string from '--name' just before the '.root' of this argument's value)")
parser.add_argument('-2Dw', '--make_2D_weight',                action='store_true',
                    help='Gives 2D weights for the data to MC ratios based on the particle kinematics (for acceptance uncertainty measurements) — Only uses clasdis files (as of 10/13/2025)')
parser.add_argument('-2DwC', '--make_2D_weight_check',         action='store_true',
                    help='Uses the 2D weights from the `--make_2D_weight` option to create 1D variable plots of Data, MC-REC, and MC-GEN — Only uses clasdis files (as of 1/15/2026)')
parser.add_argument('-VarwC', '--Var_weight_check',            type=str,   default="phi_h", choices=["phi_h", "Q2", "y", "xB", "z", "pT"],
                    help='Selects the 1D variable to be checked with `--make_2D_weight_check`')
parser.add_argument('-2DwBC', '--make_2D_weight_binned_check', action='store_true',
                    help='Uses the 2D weights from the `--make_2D_weight` option to create phi_h plots of Data, MC-REC, and MC-GEN in all the Q2-y-z-pT Bins — Also tests 1D Bin-by-Bin Corrections with these weights — Only uses clasdis files (as of 11/4/2025)')
parser.add_argument('-jsw', '--json_weights',                  action='store_true',
                    help='Use the json weights (for physics injections) given by the `--json_file` argument (only works with the `--make_2D_weight`, `--make_2D_weight_check`, and `--make_2D_weight_binned_check` options as of 11/4/2025)')
parser.add_argument('-jsf', '--json_file',                     type=str,   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json", 
                    help='JSON file path for using `json_weights`')
parser.add_argument('-hpp', '--hpp_input_file',                type=str,   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights.hpp", 
                    help="hpp file path that is used to apply the acceptance weights used/created by the '--make_2D_weight', '--make_2D_weight_check, and '--make_2D_weight_binned_check' options")
parser.add_argument('-hppOut', '--hpp_output_file',            type=str,   default="generated_acceptance_weights.hpp", 
                    help="Name of the hpp file to be outputted by the '--make_2D_weight' option (will still append the string from '--name' just before the '.hpp' of this argument's value)")
parser.add_argument('-f', '--fast',                            action='store_true',
                    help="Tries to run the code faster by skipping some printed outputs that take more time to run")
parser.add_argument('-e', '--email',                           action='store_true',
                    help="Sends an email when the script is done running (if selected)")
parser.add_argument('-em', '--email_message',                  type=str,   default="", 
                    help="Adds an extra user-defined message to emails sent with the `--email` option")

args = parser.parse_args()

rdf_batch = {1: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5302.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5349.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5181.root'], 2: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5168.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5047.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5159.root'], 3: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5391.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5378.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5333.root'], 4: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5257.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5199.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5351.root'], 5: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5235.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5204.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5360.root'], 6: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5401.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5039.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5116.root'], 7: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5253.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5229.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5262.root'], 8: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5306.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5127.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5043.root'], 9: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5200.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5419.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5355.root'], 10: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5231.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5191.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5359.root'], 11: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5323.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5247.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5368.root'], 12: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5415.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5381.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5341.root'], 13: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5225.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5160.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5370.root'], 14: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5208.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5137.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5053.root'], 15: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5316.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5195.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5239.root'], 16: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5374.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5345.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5221.root'], 17: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5164.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5190.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5358.root'], 18: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5369.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5380.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5414.root'], 19: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5340.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5398.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5215.root'], 20: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5371.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5052.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5194.root'], 21: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5238.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5317.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5211.root'], 22: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5375.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5344.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5220.root'], 23: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5165.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5180.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5303.root'], 24: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5046.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5169.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5158.root'], 25: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5390.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5404.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5379.root'], 26: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5198.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5234.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5205.root'], 27: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5361.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5117.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5038.root'], 28: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5400.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5219.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5336.root'], 29: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5252.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5307.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5126.root'], 30: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5201.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5418.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5354.root'], 31: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5230.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5311.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5130.root'], 32: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5416.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5382.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5320.root'], 33: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5163.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5128.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5342.root'], 34: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5373.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5119.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5036.root'], 35: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5386.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5324.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5196.root'], 36: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5315.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5258.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5377.root'], 37: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5032.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5167.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5346.root'], 38: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5222.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5120.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5182.root'], 39: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5301.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5406.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5392.root'], 40: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5319.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5138.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5334.root'], 41: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5250.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5402.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5124.root'], 42: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5040.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5261.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5305.root'], 43: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5203.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5367.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5248.root'], 44: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5356.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5232.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5045.root'], 45: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5300.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5183.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5393.root'], 46: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5407.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5318.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5237.root'], 47: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5139.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5206.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5362.root'], 48: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5335.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5403.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5125.root'], 49: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5041.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5304.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5249.root'], 50: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5202.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5366.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5357.root'], 51: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5233.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5193.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5310.root'], 52: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5383.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5417.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5129.root'], 53: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5162.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5343.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5339.root'], 54: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5216.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5372.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5153.root'], 55: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5325.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5197.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5051.root'], 56: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5212.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5376.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5259.root'], 57: ['REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5166.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5347.root', 'REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Sector_Tests_FC_14_V2_5223.root']}
mdf_batch = {1: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_10.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_11.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_12.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_13.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_14.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_15.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_16.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_17.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_18.root'], 2: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_19.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_20.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_21.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_22.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_23.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_24.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_25.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_26.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_27.root'], 3: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_28.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_29.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_30.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_31.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_32.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_33.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_34.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_35.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_36.root'], 4: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_37.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_38.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_39.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_40.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_41.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_42.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_43.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_44.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_45.root'], 5: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_46.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_47.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_48.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_49.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_50.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_51.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_52.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_53.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_54.root'], 6: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_7.root'], 7: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7901_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_7.root'], 8: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_7975_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_6.root'], 9: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8072_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_6.root'], 10: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8073_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_6.root'], 11: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8080_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_6.root'], 12: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8081_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_6.root'], 13: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8111_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_6.root'], 14: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8182_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_6.root'], 15: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8183_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_6.root'], 16: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8184_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_6.root'], 17: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8198_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_6.root'], 18: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8199_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_6.root'], 19: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8200_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_6.root'], 20: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8205_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_6.root'], 21: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8207_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_6.root'], 22: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8210_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_6.root'], 23: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8213_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_6.root'], 24: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8214_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_6.root'], 25: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8219_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_6.root'], 26: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8220_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_6.root'], 27: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8221_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_6.root'], 28: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8222_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_6.root'], 29: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8683_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_6.root'], 30: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8684_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_6.root'], 31: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8685_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_6.root'], 32: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8746_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_6.root'], 33: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8768_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_6.root'], 34: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8770_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_6.root'], 35: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8794_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_6.root'], 36: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8814_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_6.root'], 37: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8881_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_6.root'], 38: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8887_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_6.root'], 39: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8911_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_6.root'], 40: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8936_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_6.root'], 41: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8958_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_6.root'], 42: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8971_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_6.root'], 43: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8976_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_6.root'], 44: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_8989_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_5.root'], 45: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9030_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_5.root'], 46: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9034_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_5.root'], 47: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9040_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_5.root'], 48: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9047_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_2.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_5.root'], 49: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9107_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9136_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9136_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9136_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_2.root'], 50: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9142_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_2.root'], 51: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9209_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_2.root'], 52: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9434_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_2.root'], 53: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9448_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_2.root'], 54: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9468_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_2.root'], 55: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9470_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_2.root'], 56: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9592_9.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_0.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_1.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_2.root'], 57: ['Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_3.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_4.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_5.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_6.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_7.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_8.root', 'Matching_REC_MC/DataFrame_SIDIS_epip_MC_Matched_Pass_2_Acceptance_Tests_FC_14_V4_9626_9.root']}
gdf_batch = {1: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_10.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_11.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_12.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_13.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_14.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_15.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_16.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_17.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_18.root'], 2: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_19.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_20.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_21.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_22.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_23.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_24.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_25.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_26.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_27.root'], 3: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_28.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_29.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_30.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_31.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_32.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_33.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_34.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_35.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_36.root'], 4: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_37.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_38.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_39.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_40.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_41.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_42.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_43.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_44.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_45.root'], 5: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_46.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_47.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_48.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_49.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_50.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_51.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_52.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_53.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_54.root'], 6: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_7.root'], 7: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7901_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_7.root'], 8: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_7975_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_6.root'], 9: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8072_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_6.root'], 10: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8073_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_6.root'], 11: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8080_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_6.root'], 12: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8081_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_6.root'], 13: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8111_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_6.root'], 14: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8182_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_6.root'], 15: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8183_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_6.root'], 16: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8184_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_6.root'], 17: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8198_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_6.root'], 18: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8199_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_6.root'], 19: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8200_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_6.root'], 20: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8205_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_6.root'], 21: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8207_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_6.root'], 22: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8210_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_6.root'], 23: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8213_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_6.root'], 24: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8214_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_6.root'], 25: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8219_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_6.root'], 26: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8220_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_6.root'], 27: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8221_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_6.root'], 28: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8222_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_6.root'], 29: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8683_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_6.root'], 30: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8684_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_6.root'], 31: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8685_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_6.root'], 32: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8746_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_6.root'], 33: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8768_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_6.root'], 34: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8770_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_6.root'], 35: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8794_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_6.root'], 36: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8814_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_6.root'], 37: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8881_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_6.root'], 38: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8887_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_6.root'], 39: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8911_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_6.root'], 40: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8936_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_6.root'], 41: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8958_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_6.root'], 42: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8971_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_6.root'], 43: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8976_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_6.root'], 44: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_8989_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_5.root'], 45: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9030_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_5.root'], 46: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9034_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_5.root'], 47: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9040_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_5.root'], 48: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9047_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_2.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_5.root'], 49: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9107_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9136_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9136_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9136_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_2.root'], 50: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9142_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_2.root'], 51: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9209_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_2.root'], 52: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9434_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_2.root'], 53: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9448_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_2.root'], 54: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9468_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_2.root'], 55: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9470_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_2.root'], 56: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9592_9.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_0.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_1.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_2.root'], 57: ['GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_3.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_4.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_5.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_6.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_7.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_8.root', 'GEN_MC/DataFrame_SIDIS_epip_MC_GEN_Pass_2_Acceptance_Tests_V3_9626_9.root']}

if(".hpp" not in args.hpp_output_file):
    print(f"\n'--hpp_output_file' was set to {args.hpp_output_file}\n")
    raise ValueError("Invalid '--hpp_output_file' argument (the string must end with '.hpp')")

if(".root" not in args.root):
    print(f"\n'--root' was set to {args.root}\n")
    raise ValueError("Invalid '--root' argument (the string must end with '.root')")
    

if(args.name):
    args.hpp_output_file = str(args.hpp_output_file).replace(".hpp", f"_{args.name}.hpp") if(args.name not in str(args.hpp_output_file)) else str(args.hpp_output_file)
    args.root = str(args.root).replace(".root", f"_{args.name}.root") if(args.name not in str(args.root)) else str(args.root)

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


if(args.batch_id):
    print(f"\n\n{color_bg.YELLOW}\n\n\t{color.BGREEN}Running with batch files {color.CYAN}{color_bg.YELLOW}{color.UNDERLINE}{args.batch_id}{color.END}{color_bg.YELLOW}\t\n{color.END}")
    if((args.batch_id > 57) or (args.batch_id < 1)):
        # print(f"\n'--batch_id' was set to {args.batch_id}\n")
        raise ValueError("Invalid '--batch_id' argument (groups are defined from 1 to 57)")

args.Do_not_use_EvGen = (args.Do_not_use_EvGen or (args.make_2D_weight or args.make_2D_weight_check or args.make_2D_weight_binned_check))
if(args.Do_not_use_EvGen):
    print(f"\n{color.RED}Will NOT use EvGen Files at all{color.END}\n")

JSON_WEIGHT_FILE = args.json_file

if(not args.make_2D_weight):
    # Load the self-contained, generated header for acceptance weights (helpers + accw_* functions)
    print(f"{color.BBLUE}Loading {color.END_B}{args.hpp_input_file}{color.BBLUE} for acceptance weights (if applicable){color.END}\n")
    ROOT.gInterpreter.Declare(f'#include "{args.hpp_input_file}"')


if(args.do_not_use_hpp):
    print(f"{color.Error}Not using Acceptance Weights{color.END}")
elif(args.angles_only_hpp):
    print(f"{color.Error}Only using the angle Acceptance Weights (not weighing the lab momemtum for acceptance){color.END}")


import subprocess
def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    # Map ANSI codes to HTML spans
    ansi_html_map = { # Styles
                    '\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "",
                      # Colors
                    '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "",
                      # Reset (closes span)
                    '\033[0m': "",
                    }
    sorted_codes = sorted(ansi_html_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_html_map[code])
    # Remove any stray/unsupported ANSI codes that might remain
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text

def send_email(subject, body, recipient):
    # Send an email via the system mail command.
    html_body = ansi_to_html(body)
    subprocess.run(["mail", "-s", subject, recipient], input=html_body.encode(), check=False)


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


# def lumi(charge):
#     # Calculate the luminosity factor from input charge.
#     # Parameters
#     # charge : float
#     #     Charge delivered, in nanocoulombs (nC).
#     # Returns
#     # float
#     #     The luminosity factor in μb⁻¹ (microbarn⁻¹) units.
#     # Constants
#     RD   = 57.1                 # (unused, carried over)
#     qe   = 1.602177e-19         # electron charge, C
#     rho  = 0.0701               # density of H2 @20 K, g/cm³
#     A0   = 6.0221367e23         # Avogadro’s number, mol⁻¹
#     MH   = 1.00794              # atomic mass of H, g/mol
#     LT   = 5.0                  # target length, cm
#     CMB  = 1e30                 # cm² → μbarn
#     # Convert input from nanocoulombs to coulombs
#     charge_c = charge / 1e9
#     # Number of target nuclei per cm²
#     np_cm2 = LT * rho * A0 / MH
#     # Number of electrons hitting the target
#     ne = charge_c / qe
#     # Luminosity factor in μb⁻¹
#     factor = (ne * np_cm2) / CMB
#     return factor

# def Luminosity_Norm(Histo, generator):
#     # Luminosity = lumi(4.09744e+07) # 4.09744e+07 nC came from /lustre24/expphy/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/nSidis_* (as of 8/1/2025)
#     Luminosity = 53555744533.35742
#     generator_factor = 1
#     if(generator in ["clasdis"]):
#         Integrated_cs_from_gen = 6.834e4 # pb


def Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type=""):
    # Defined for the 'Y_bin' binning option
    if(str(Variable_Type) not in ["smear", "smeared", "GEN", "Gen", "gen", "", "norm", "normal", "default"]):
        print(f"The input: {color.RED}{Variable_Type}{color.END} was not recognized by the function Q2_y_z_pT_4D_Bin_Def_Function(Variable_Type='{Variable_Type}').\nFix input to use anything other than the default calculations of the 4D kinematic bin.")
        Variable_Type   = ""
        
    Q2_y_Bin_event_name = f"""Q2_Y_Bin{      "_smeared" if(str(Variable_Type) in ["smear", "smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen"]) else ""}"""
    z_pT_Bin_event_name = f"""z_pT_Bin_Y_bin{"_smeared" if(str(Variable_Type) in ["smear", "smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen"]) else ""}"""
    
    Q2_y_z_pT_4D_Bin_Def = f"""
    int Q2_y_Bin_event_val = {Q2_y_Bin_event_name};
    int z_pT_Bin_event_val = {z_pT_Bin_event_name};
    int Q2_y_z_pT_4D_Bin_event_val = 0;
    if(Q2_y_Bin_event_val >  1){{ Q2_y_z_pT_4D_Bin_event_val += 35; }}
    if(Q2_y_Bin_event_val >  2){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val >  3){{ Q2_y_z_pT_4D_Bin_event_val += 30; }}
    if(Q2_y_Bin_event_val >  4){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val >  5){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val >  6){{ Q2_y_z_pT_4D_Bin_event_val += 30; }}
    if(Q2_y_Bin_event_val >  7){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val >  8){{ Q2_y_z_pT_4D_Bin_event_val += 35; }}
    if(Q2_y_Bin_event_val >  9){{ Q2_y_z_pT_4D_Bin_event_val += 35; }}
    if(Q2_y_Bin_event_val > 10){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val > 11){{ Q2_y_z_pT_4D_Bin_event_val += 25; }}
    if(Q2_y_Bin_event_val > 12){{ Q2_y_z_pT_4D_Bin_event_val += 25; }}
    if(Q2_y_Bin_event_val > 13){{ Q2_y_z_pT_4D_Bin_event_val += 30; }}
    if(Q2_y_Bin_event_val > 14){{ Q2_y_z_pT_4D_Bin_event_val += 36; }}
    if(Q2_y_Bin_event_val > 15){{ Q2_y_z_pT_4D_Bin_event_val += 25; }}
    if(Q2_y_Bin_event_val > 16){{ Q2_y_z_pT_4D_Bin_event_val += 30; }}
    
    Q2_y_z_pT_4D_Bin_event_val += z_pT_Bin_event_val;
    
    if(Q2_y_Bin_event_val < 1 || z_pT_Bin_event_val < 1){{ Q2_y_z_pT_4D_Bin_event_val = 0; }}
    
    return Q2_y_z_pT_4D_Bin_event_val;
    """
    # Total number of bins: 546 — Includes the migration bins in the grid, but not the zero bin
    return Q2_y_z_pT_4D_Bin_Def


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
                if(Titles_or_DF == 'DF'):
                    if(("smear" in Smearing_Q) and (Data_Type != "rdf")):
                        # DF_Out  = DF_Out.Filter("sqrt(smeared_vals[1]) > 1.5")
                        DF_Out  = DF_Out.Filter("sqrt(MM2_smeared) > 1.5")
                    else:
                        DF_Out  = DF_Out.Filter("sqrt(MM2) > 1.5")
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
    if(source in ["clasdis"]):
        Q2_Y_Binning, z_pT_Bin_Y_binning = "Q2_Y_Bin_smeared", "z_pT_Bin_Y_bin_smeared"
    else:
        Q2_Y_Binning, z_pT_Bin_Y_binning = "Q2_Y_Bin", "z_pT_Bin_Y_bin"
    if(Q2_Y_Bin):
        mdf_IN_Binned     =        mdf_IN.Filter(f"{Q2_Y_Binning} == {Q2_Y_Bin}")
        gdf_IN_Binned     =        gdf_IN.Filter(f"Q2_Y_Bin == {Q2_Y_Bin}")
        if(Z_PT_Bin):
            mdf_IN_Binned = mdf_IN_Binned.Filter(f"{z_pT_Bin_Y_binning} == {Z_PT_Bin}")
            gdf_IN_Binned = gdf_IN_Binned.Filter(f"z_pT_Bin_Y_bin == {Z_PT_Bin}")
            mdf_name      = f"{mdf_name} Bin ({Q2_Y_Bin}-{Z_PT_Bin})"
            gdf_name      = f"{gdf_name} Bin ({Q2_Y_Bin}-{Z_PT_Bin})"
        else:
            mdf_name      = f"{mdf_name} Bin ({Q2_Y_Bin}-All)"
            gdf_name      = f"{gdf_name} Bin ({Q2_Y_Bin}-All)"
    else:
        mdf_IN_Binned     =        mdf_IN
        gdf_IN_Binned     =        gdf_IN

    if(source in ["clasdis"]):
        mdf_hist = mdf_IN_Binned.Histo1D((mdf_name, f"{variable_Title_name_new(var)} from MC REC ({source}); {variable_Title_name_new(var)}", Num_of_Bins, Min_range, Max_range), f"{var}_smeared")
        gdf_hist = gdf_IN_Binned.Histo1D((gdf_name, f"{variable_Title_name_new(var)} from MC GEN ({source}); {variable_Title_name_new(var)}", Num_of_Bins, Min_range, Max_range), var)
    else:
        mdf_hist = mdf_IN_Binned.Histo1D((mdf_name, f"{variable_Title_name_new(var)} from MC REC ({source}); {variable_Title_name_new(var)}", Num_of_Bins, Min_range, Max_range), var, "weight")
        gdf_hist = gdf_IN_Binned.Histo1D((gdf_name, f"{variable_Title_name_new(var)} from MC GEN ({source}); {variable_Title_name_new(var)}", Num_of_Bins, Min_range, Max_range), var, "weight")

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
    
    for ibin in range(1, acc_hist.GetNbinsX() + 1):  # bins are 1-indexed in ROOT
        if(acc_hist.GetBinContent(ibin) < args.min_accept_cut):
            acc_hist.SetBinContent(ibin, 0.0)

    return mdf_hist, gdf_hist, acc_hist


def Acceptance_Compare_z_pT_Images_Together(Histogram_List_All, Q2_Y_Bin, Plot_Orientation="z_pT", Saving_Q=True, File_Save_Format=args.File_Save_Format):
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    # Use above for normal size, use below for 2x size (made with PDFs)
    Save_Name = f"Acceptance_Compare_for_Q2_Y_Bin_{Q2_Y_Bin}"
    if(args.acceptance_ratio):
        Save_Name = f"Acceptance_Ratio_for_Q2_Y_Bin_{Q2_Y_Bin}"
    if(args.acceptance_diff):
        Save_Name = f"Acceptance_Diff_for_Q2_Y_Bin_{Q2_Y_Bin}"
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
    if(not (args.acceptance_ratio or args.acceptance_diff)):
        cd_1_Lower_max = max([find_max_bin(Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"]), find_max_bin(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"]), Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"]])
        Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"].GetYaxis().SetRangeUser(0,   1.2*cd_1_Lower_max)
        Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"].GetYaxis().SetRangeUser(0, 1.2*cd_1_Lower_max)
        Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"].Draw("E0 hist")
        Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"].Draw("E0 hist same")
        legend = ROOT.TLegend(0.65, 0.70, 0.95, 0.9, "", "NDC")
        legend.SetNColumns(1)  # or 2 for side-by-side entries
        # legend.SetBorderSize(0)   # no border
        legend.SetFillStyle(1)    # transparent background
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.SetMargin(0.15)    # internal padding
        legend.AddEntry(Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"],   f"#color[{ROOT.kAzure   }]{{Acceptance EvGen}}",   "lep")
        legend.AddEntry(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"], f"#color[{ROOT.kAzure+10}]{{Acceptance clasdis}}", "lep")
        legend.Draw()
        xmin = Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"].GetXaxis().GetXmin()
        xmax = Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"].GetXaxis().GetXmax()
        Acceptance_Line = ROOT.TLine(xmin, args.min_accept_cut, xmax, args.min_accept_cut)
        Acceptance_Line.SetLineColor(ROOT.kRed - 9)
        Acceptance_Line.SetLineWidth(2)
        Acceptance_Line.SetLineStyle(1)
        Acceptance_Line.Draw("same")
        ROOT.gPad.Update()
    elif(args.acceptance_ratio):
        Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].GetYaxis().SetRangeUser(0, max([1.2, 1.2*find_max_bin(Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"])]))
        Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].Draw("E0 hist")
        xmin = Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].GetXaxis().GetXmin()
        xmax = Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].GetXaxis().GetXmax()
        Acceptance_Line = ROOT.TLine(xmin, 1.0, xmax, 1.0)
        Acceptance_Line.SetLineColor(ROOT.kGray + 3)
        Acceptance_Line.SetLineWidth(2)
        Acceptance_Line.SetLineStyle(1)
        Acceptance_Line.Draw("same")
        ROOT.gPad.Update()
        try:
            if(not hasattr(All_z_pT_Canvas_cd_1_Lower, "AR_fit_store")):
                All_z_pT_Canvas_cd_1_Lower.AR_fit_store  = {}
            if(not hasattr(All_z_pT_Canvas_cd_1_Lower, "AR_text_store")):
                All_z_pT_Canvas_cd_1_Lower.AR_text_store = {}
            hist_key  = f"ratio Acceptance Bin ({Q2_y_Bin}-All)"
            fit_range_lower = 0.0
            fit_range_upper = 360.0
            n_bins          = Histogram_List_All[hist_key].GetNbinsX()
            for bin_lower in range(1, (n_bins // 2) + 1):
                if(Histogram_List_All[hist_key].GetBinContent(bin_lower) != 0):
                    fit_range_lower = Histogram_List_All[hist_key].GetXaxis().GetBinLowEdge(bin_lower)
                    break
            for bin_upper in range(n_bins, (n_bins // 2), -1):
                if(Histogram_List_All[hist_key].GetBinContent(bin_upper) != 0):
                    fit_range_upper = Histogram_List_All[hist_key].GetXaxis().GetBinUpEdge(bin_upper)
                    break
            func_name  = f"AR_fit_{Q2_y_Bin}-All" # Create or update a unique TF1 for this bin; keep it in a persistent store on the canvas
            if(func_name not in All_z_pT_Canvas_cd_1_Lower.AR_fit_store):
                All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name] = ROOT.TF1(func_name, "pol0", fit_range_lower, fit_range_upper)
            else:
                All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].SetRange(fit_range_lower, fit_range_upper)
            fit_result = Histogram_List_All[hist_key].Fit(All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name], "QRB0") # "QRB": Q=quiet, R=respect range, B=use bounding for errors, 0=suppress draw (done below)
            All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].SetLineColor(ROOT.kRed)
            All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].SetLineStyle(7)
            All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].SetLineWidth(2)
            # Pull results from the TF1 (works regardless of TFitResult validity)
            p0       = All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].GetParameter(0)
            p0e      = All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].GetParError(0)
            try:
                chi2 = All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].GetChisquare()
                ndf  = All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].GetNDF()
            except:
                chi2, ndf = "Fit_Chisquared", "Fit_ndf"
            try:
                chi2_text = f"{chi2:.3g}/{ndf}" if(isinstance(chi2, (int, float)) and isinstance(ndf, (int, float))) else f"{chi2}/{ndf}"
            except:
                chi2_text = f"{chi2}/{ndf}"
            if(func_name not in All_z_pT_Canvas_cd_1_Lower.AR_text_store):
                # (x1,y1,x2,y2) in NDC; adjust box if it overlaps your legend
                pv = ROOT.TPaveText(0.33, 0.15, 0.67, 0.29, "NDC")
                pv.SetFillStyle(0)
                pv.SetBorderSize(0)
                pv.SetTextAlign(12)   # left/middle
                pv.SetTextFont(42)
                # pv.SetTextSize(0.035)
                pv.SetTextSize(0.064)
                pv.SetTextColor(ROOT.kBlack)
                pv.SetName(f"AR_pave_{func_name}")
                All_z_pT_Canvas_cd_1_Lower.AR_text_store[func_name] = pv
            else:
                pv = All_z_pT_Canvas_cd_1_Lower.AR_text_store[func_name]
                pv.Clear()
            pv.AddText(f"A = {p0:.6f} #pm {p0e:.3f}")
            pv.AddText(f"#chi^{{2}}/ndf = {chi2_text}")
            All_z_pT_Canvas_cd_1_Lower.AR_fit_store[func_name].Draw("same")
            pv.Draw("same")
            ROOT.gPad.Modified()
            ROOT.gPad.Update()
        except Exception as fit_err:
            print(f"{color.Error}Acceptance-ratio constant-fit failed for Bin ({Q2_y_Bin}-All):{color.END_R} {str(fit_err)}{color.END}")
    else:
        # Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"]))
        Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].Draw("E0 hist")
        xmin = Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].GetXaxis().GetXmin()
        xmax = Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].GetXaxis().GetXmax()
        Acceptance_Line = ROOT.TLine(xmin, 0, xmax, 0)
        Acceptance_Line.SetLineColor(ROOT.kGray + 3)
        Acceptance_Line.SetLineWidth(2)
        Acceptance_Line.SetLineStyle(1)
        Acceptance_Line.Draw("same")
        ROOT.gPad.Update()

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

            # Ensure persistent stores exist on the parent canvas so objects survive the loop
            if(not hasattr(All_z_pT_Canvas_cd_2, "AR_fit_store")):
                All_z_pT_Canvas_cd_2.AR_fit_store  = {}
            if(not hasattr(All_z_pT_Canvas_cd_2, "AR_text_store")):
                All_z_pT_Canvas_cd_2.AR_text_store = {}

            if(not (args.acceptance_ratio or args.acceptance_diff)):
                Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetYaxis().SetRangeUser(0,   1.2*Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"])
                Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetYaxis().SetRangeUser(0, 1.2*Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"])
                Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Draw("E0 hist")
                Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Draw("E0 hist same")
                Acceptance_Line.Draw("same")
                ROOT.gPad.Update()
            elif(args.acceptance_ratio):
                # Draw the ratio histogram as before
                Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetYaxis().SetRangeUser(0, max([1.2, 1.2*Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"]]))
                Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Draw("E0 hist")
                Acceptance_Line.Draw("same")
                ROOT.gPad.Update()
                try:
                    hist_key  = f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"
                    fit_range_lower = 0.0
                    fit_range_upper = 360.0
                    n_bins          = Histogram_List_All[hist_key].GetNbinsX()
                    for bin_lower in range(1, (n_bins // 2) + 1):
                        if(Histogram_List_All[hist_key].GetBinContent(bin_lower) != 0):
                            fit_range_lower = Histogram_List_All[hist_key].GetXaxis().GetBinLowEdge(bin_lower)
                            break
                    for bin_upper in range(n_bins, (n_bins // 2), -1):
                        if(Histogram_List_All[hist_key].GetBinContent(bin_upper) != 0):
                            fit_range_upper = Histogram_List_All[hist_key].GetXaxis().GetBinUpEdge(bin_upper)
                            break
                    func_name  = f"AR_fit_{Q2_y_Bin}-{z_pT_Bin}" # Create or update a unique TF1 for this bin; keep it in a persistent store on the canvas
                    if(func_name not in All_z_pT_Canvas_cd_2.AR_fit_store):
                        All_z_pT_Canvas_cd_2.AR_fit_store[func_name] = ROOT.TF1(func_name, "pol0", fit_range_lower, fit_range_upper)
                    else:
                        All_z_pT_Canvas_cd_2.AR_fit_store[func_name].SetRange(fit_range_lower, fit_range_upper)
                    fit_result = Histogram_List_All[hist_key].Fit(All_z_pT_Canvas_cd_2.AR_fit_store[func_name], "QRB0") # "QRB": Q=quiet, R=respect range, B=use bounding for errors, 0=suppress draw (done below)
                    All_z_pT_Canvas_cd_2.AR_fit_store[func_name].SetLineColor(ROOT.kRed)
                    All_z_pT_Canvas_cd_2.AR_fit_store[func_name].SetLineStyle(7)
                    All_z_pT_Canvas_cd_2.AR_fit_store[func_name].SetLineWidth(2)
                    # Pull results from the TF1 (works regardless of TFitResult validity)
                    p0       = All_z_pT_Canvas_cd_2.AR_fit_store[func_name].GetParameter(0)
                    p0e      = All_z_pT_Canvas_cd_2.AR_fit_store[func_name].GetParError(0)
                    try:
                        chi2 = All_z_pT_Canvas_cd_2.AR_fit_store[func_name].GetChisquare()
                        ndf  = All_z_pT_Canvas_cd_2.AR_fit_store[func_name].GetNDF()
                    except:
                        chi2, ndf = "Fit_Chisquared", "Fit_ndf"
                    try:
                        chi2_text = f"{chi2:.3g}/{ndf}" if(isinstance(chi2, (int, float)) and isinstance(ndf, (int, float))) else f"{chi2}/{ndf}"
                    except:
                        chi2_text = f"{chi2}/{ndf}"
                    if(func_name not in All_z_pT_Canvas_cd_2.AR_text_store):
                        # (x1,y1,x2,y2) in NDC; adjust box if it overlaps your legend
                        pv = ROOT.TPaveText(0.33, 0.15, 0.67, 0.29, "NDC")
                        pv.SetFillStyle(0)
                        pv.SetBorderSize(0)
                        pv.SetTextAlign(12)   # left/middle
                        pv.SetTextFont(42)
                        # pv.SetTextSize(0.035)
                        pv.SetTextSize(0.064)
                        pv.SetTextColor(ROOT.kBlack)
                        pv.SetName(f"AR_pave_{func_name}")
                        All_z_pT_Canvas_cd_2.AR_text_store[func_name] = pv
                    else:
                        pv = All_z_pT_Canvas_cd_2.AR_text_store[func_name]
                        pv.Clear()
                    pv.AddText(f"A = {p0:.6f} #pm {p0e:.3f}")
                    pv.AddText(f"#chi^{{2}}/ndf = {chi2_text}")
                    All_z_pT_Canvas_cd_2.AR_fit_store[func_name].Draw("same")
                    pv.Draw("same")
                    ROOT.gPad.Modified()
                    ROOT.gPad.Update()
                except Exception as fit_err:
                    print(f"{color.Error}Acceptance-ratio constant-fit failed for Bin ({Q2_y_Bin}-{z_pT_Bin}):{color.END_R} {str(fit_err)}{color.END}")
            else:
                # Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetYaxis().SetRangeUser(0, 1.2*Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"])
                Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Draw("E0 hist")
                Acceptance_Line.Draw("same")
                ROOT.gPad.Update()
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




def DrawNormalizedHistos(histos_in, TPad_draw, Normalize_Q=True):
    # Draws a list of TH1 histograms normalized to unit area and automatically 
    # adjusts the y-axis to go from 0 to 1.2 × the maximum normalized bin height.
    if(not histos_in):
        print(f"{color.Error}Warning: empty histogram list passed to DrawNormalizedHistos(){color.END}")
        return
    if(not TPad_draw):
        print(f"{color.Error}Warning: Did not pass a TPad to DrawNormalizedHistos() to draw in{color.END}")
        return
    # Compute the largest normalized bin content among all histograms
    max_val = 0.0
    for h in histos_in:
        if(Normalize_Q):
            if(h and (h.Integral() != 0)):
                max_val = max([max_val, h.GetMaximum() / h.Integral()])
        else:
            max_val = max([max_val, h.GetMaximum()])
    y_max = (1.2 * max_val) if(max_val > 0) else 1.0

    Draw_Canvas(TPad_draw, 1, 0.15)
    # Draw all histograms normalized
    first = True
    for h in histos_in:
        if((not h) or (h.Integral() == 0)):
            continue
        if(Normalize_Q):
            # Force same normalization factor for all histograms
            h.DrawNormalized("H P E0" if(first) else "H P E0 same", 1.0)
        else:
            h.Draw("H P E0" if(first) else "H P E0 same")
        h.GetYaxis().SetRangeUser(0, y_max)
        first = False

import json
def z_pT_Images_Together_For_Comparisons(rdf_in=None, mdf_in=None, gdf_in=None, Q2_Y_Bin_List=range(1, 18), Plot_Orientation="z_pT", Nrdf="?", Nmdf="?"):
    import gc
    Saved_Histos, All_z_pT_Canvas, All_z_pT_Canvas_cd_1, All_z_pT_Canvas_cd_1_Upper, All_z_pT_Canvas_cd_1_Lower, All_z_pT_Canvas_cd_2, All_z_pT_Canvas_cd_2_cols, legend = {}, {}, {}, {}, {}, {}, {}, {}
    Uncertainty_Output = {}
    if(args.title):
        Uncertainty_Output["Info"] = f"""
JSON_WEIGHT_FILE = {JSON_WEIGHT_FILE}
Number of (requested) rdf Files (-nrdf) = {args.num_rdf_files}
    Number actually available: {Nrdf}
Number of (requested) mdf Files (-nMC)  = {args.num_MC_files}
    Number actually available: {Nmdf}
Extra Title(s):
{args.title}
"""
    else:
        Uncertainty_Output["Info"] = f"""
JSON_WEIGHT_FILE = {JSON_WEIGHT_FILE}
Number of (requested) rdf Files (-nrdf) = {args.num_rdf_files}
    Number actually available: {Nrdf}
Number of (requested) mdf Files (-nMC)  = {args.num_MC_files}
    Number actually available: {Nmdf}
Extra Title(s): N/A
"""
    for Q2_Y_Bin in Q2_Y_Bin_List:
        print(f"\n{color.BOLD}Starting Q2-y Bin {Q2_Y_Bin}{color.END}\n")
        timer.time_elapsed()
        # --- Cache one dataset group at a time (so only one big table lives in RAM)
        rdf_cached = rdf_in.Filter(f"Q2_Y_Bin == {Q2_Y_Bin}").Cache()
        gdf_cached = gdf_in.Filter(f"Q2_Y_Bin == {Q2_Y_Bin}").Cache()
        mdf_cached = mdf_in.Filter(f"Q2_Y_Bin_smeared == {Q2_Y_Bin}").Cache()
        Canvases_to_Make = [f"Uncorrected_Modulation_Comparisons_Q2_y_Bin_{Q2_Y_Bin}", f"Bin_by_Bin_Comparisons_of_Weights_Q2_y_Bin_{Q2_Y_Bin}", f"Weighed_Acceptance_Comparisons_Q2_y_Bin_{Q2_Y_Bin}"]
        ##############################################################################################################################################################################################################################################################################################################################################################################################################
        ####  Histogram Creations     #########################################################################################################################################################################
        z_pT_Bin_Range = range(0, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1] + 1)
        for z_PT_BIN_NUM  in z_pT_Bin_Range:
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_PT_BIN_NUM, BINNING_METHOD=Binning_Method, Common_z_pT_Range_Q=False)):
                continue
            Binning_Title = f"{root_color.Bold}{{Q^{{2}}-y Bin {Q2_Y_Bin} #topbar z-P_{{T}} Bin {z_PT_BIN_NUM if(z_PT_BIN_NUM != 0) else 'All'}}}"
            if(args.title):
                Binning_Title = f"#splitline{{{Binning_Title}}}{{{args.title}}}"
            Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})"]     = ((rdf_cached.Filter(f"z_pT_Bin_Y_bin {'=='         if(z_PT_BIN_NUM != 0) else '!='} {z_PT_BIN_NUM}")).Histo1D((f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})",         f"#splitline{{Experimental Distribution of #phi_{{h}}}}{{{Binning_Title}}}; #phi_{{h}}", 24, 0.0, 360.0), "phi_t")).GetValue()
            Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"] = ((mdf_cached.Filter(f"z_pT_Bin_Y_bin_smeared {'==' if(z_PT_BIN_NUM != 0) else '!='} {z_PT_BIN_NUM}")).Histo1D((f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW", f"#splitline{{Unweighed MC REC Distribution of #phi_{{h}}}}{{{Binning_Title}}}; #phi_{{h}}", 24, 0.0, 360.0), "phi_t_smeared")).GetValue()
            Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"] = ((gdf_cached.Filter(f"z_pT_Bin_Y_bin {'=='         if(z_PT_BIN_NUM != 0) else '!='} {z_PT_BIN_NUM}")).Histo1D((f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW", f"#splitline{{Unweighed MC GEN Distribution of #phi_{{h}}}}{{{Binning_Title}}}; #phi_{{h}}", 24, 0.0, 360.0), "phi_t")).GetValue()
            Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"] = ((mdf_cached.Filter(f"z_pT_Bin_Y_bin_smeared {'==' if(z_PT_BIN_NUM != 0) else '!='} {z_PT_BIN_NUM}")).Histo1D((f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW",   f"#splitline{{Weighed MC REC Distribution of #phi_{{h}}}}{{{Binning_Title}}}; #phi_{{h}}", 24, 0.0, 360.0), "phi_t_smeared", "Event_Weight")).GetValue()
            Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"] = ((gdf_cached.Filter(f"z_pT_Bin_Y_bin {'=='         if(z_PT_BIN_NUM != 0) else '!='} {z_PT_BIN_NUM}")).Histo1D((f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW",   f"#splitline{{Weighed MC GEN Distribution of #phi_{{h}}}}{{{Binning_Title}}}; #phi_{{h}}", 24, 0.0, 360.0), "phi_t",         "Event_Weight")).GetValue()

            Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})"].Sumw2()
            Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"].Sumw2()
            Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"].Sumw2()
            Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].Sumw2()
            Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].Sumw2()
            Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})"].SetLineColor(ROOT.kBlue)
            Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"].SetLineColor(ROOT.kRed)
            Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"].SetLineColor(ROOT.kGreen)
            Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].SetLineColor(ROOT.kViolet)
            Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].SetLineColor(ROOT.kTeal)
            for cor_W in ["_NoW", "_AcW"]:
                Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"] = Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"].Clone(f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}")
                Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"].Divide(Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"])
                Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"].SetTitle(f"#splitline{{{'Unweighed' if(cor_W == '_NoW') else 'Weighed'} MC Acceptance}}{{{Binning_Title}}}")
                Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"].SetLineColor(ROOT.kBlack if(cor_W == '_NoW') else (ROOT.kGray + 1))
                
                Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"] = Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})"].Clone(f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}")
                Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"].Divide(Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"])
                Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"].SetTitle(f"#splitline{{Bin-by-Bin Corrected Data (Using {'Unweighed' if(cor_W == '_NoW') else 'Weighed'} MC Acceptance)}}{{{Binning_Title}}}")
                Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM}){cor_W}"].SetLineColor(28 if(cor_W == '_NoW') else (ROOT.kOrange))
    
            Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_Synthetic"] = Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].Clone(f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_Synthetic")
            Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_Synthetic"].Divide(Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"])
            Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_Synthetic"].SetTitle(f"#splitline{{Bin-by-Bin Corrected Synthetic Data (Using Unweighed MC to Correct the Weighed MC)}}{{{Binning_Title}}}")
            Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_Synthetic"].SetLineColor(ROOT.kGreen + 2)

            for bin_idx in range(1, Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"].GetNbinsX() + 1):
                val1 = Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"].GetBinContent(bin_idx)
                err1 = Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_NoW"].GetBinError(bin_idx)
                val2 = Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].GetBinContent(bin_idx)
                err2 = Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].GetBinError(bin_idx)
                val3 = Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_Synthetic"].GetBinContent(bin_idx)
                err3 = Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_Synthetic"].GetBinError(bin_idx)
                val4 = Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].GetBinContent(bin_idx)
                err4 = Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_PT_BIN_NUM})_AcW"].GetBinError(bin_idx)
                
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"] = {}
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["phi_bin"] = bin_idx
                # The 'normal_bbb' means that the experimental data (rdf) was corrected with the normal (unmodulated) MC
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["content_normal_bbb"] = val1
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["error_normal_bbb"]   = err1
                # The 'MOD_bbb' means that the experimental data (rdf) was corrected with the modulated MC
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["content_MOD_bbb"]    = val2
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["error_MOD_bbb"]      = err2
                # The 'SIM_bbb' means that the synthetic data (modulated MC) was corrected with the normal MC
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["content_SIM_bbb"]    = val3
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["error_SIM_bbb"]      = err3
                # The 'SIM_gdf' means that the 'true' generated distribution of the synthetic data (modulated MC) that should converge with 'SIM_bbb'
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["content_SIM_gdf"]    = val4
                Uncertainty_Output[f"{Q2_Y_Bin}_{z_PT_BIN_NUM}_{bin_idx}"]["error_SIM_gdf"]      = err4
            
        ####  Histogram Creations     #########################################################################################################################################################################
        #######################################################################################################################################################################################################
        ####  Canvas (Main) Creation  #########################################################################################################################################################################
        for canvas_num, Canvas_Name in enumerate(Canvases_to_Make):
            All_z_pT_Canvas[Canvas_Name] = Canvas_Create(Name=Canvas_Name, Num_Columns=2, Num_Rows=1, Size_X=3900, Size_Y=2175, cd_Space=0.01)
            All_z_pT_Canvas[Canvas_Name].SetFillColor(root_color.LGrey)
            All_z_pT_Canvas_cd_1[Canvas_Name]       = All_z_pT_Canvas[Canvas_Name].cd(1)
            All_z_pT_Canvas_cd_1[Canvas_Name].SetFillColor(root_color.LGrey)
            All_z_pT_Canvas_cd_1[Canvas_Name].SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
            All_z_pT_Canvas_cd_1[Canvas_Name].Divide(1, 2, 0, 0)
            All_z_pT_Canvas_cd_1_Upper[Canvas_Name] = All_z_pT_Canvas_cd_1[Canvas_Name].cd(1)
            All_z_pT_Canvas_cd_1_Upper[Canvas_Name].SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
            All_z_pT_Canvas_cd_1_Upper[Canvas_Name].Divide(1, 1, 0, 0)
            All_z_pT_Canvas_cd_1_Lower[Canvas_Name] = All_z_pT_Canvas_cd_1[Canvas_Name].cd(2)
            All_z_pT_Canvas_cd_1_Lower[Canvas_Name].SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
            All_z_pT_Canvas_cd_1_Lower[Canvas_Name].Divide(1, 1, 0, 0)
            All_z_pT_Canvas_cd_1_Lower[Canvas_Name].cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)
            All_z_pT_Canvas_cd_2[Canvas_Name]       = All_z_pT_Canvas[Canvas_Name].cd(2)
            All_z_pT_Canvas_cd_2[Canvas_Name].SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
            All_z_pT_Canvas_cd_2[Canvas_Name].SetFillColor(root_color.LGrey)
            if(Plot_Orientation in ["z_pT"]):
                number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
                All_z_pT_Canvas_cd_2[Canvas_Name].Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)
            else:
                number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
                All_z_pT_Canvas_cd_2[Canvas_Name].Divide(1, number_of_cols, 0.0001, 0.0001)
                for ii in range(1, number_of_cols + 1, 1):
                    All_z_pT_Canvas_cd_2_cols[Canvas_Name] = All_z_pT_Canvas_cd_2[Canvas_Name].cd(ii)
                    All_z_pT_Canvas_cd_2_cols[Canvas_Name].Divide(number_of_rows, 1, 0.0001, 0.0001)
        ####  Canvas (Main) Creation End ######################################################################################################################################################################
        #######################################################################################################################################################################################################
            legend[Canvas_Name] = ROOT.TLegend(0.01, 0.01, 0.99, 0.99)
            Legend_Header = f"#splitline{{#scale[2]{{Q^{{2}}-y Bin {Q2_Y_Bin}}}}}{{#scale[1.5]{{Plots Shown}}}}"
            if("Uncorrected_Modulation_Comparisons"  in Canvas_Name):
                legend[Canvas_Name].SetHeader(f"#splitline{{Uncorrected Distributions for}}{{{Legend_Header}}}", "C")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)"],         "Experimental Distribution", "lep")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"], "Unweighed MC REC Distribution", "lep")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"], "Unweighed MC GEN Distribution", "lep")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_AcW"],   "Weighed MC REC Distribution", "lep")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_AcW"],   "Weighed MC GEN Distribution", "lep")
            elif("Bin_by_Bin_Comparisons_of_Weights" in Canvas_Name):
                legend[Canvas_Name].SetHeader(f"#splitline{{Bin-by-Bin Corrected Distributions for}}{{{Legend_Header}}}", "C")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"],                                                    "Data Corrected with Unweighed MC REC", "lep")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_AcW"],                                                      "Data Corrected with Weighed MC REC", "lep")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_Synthetic"], "#splitline{Corrected Synthetic Data}{Used Unweighed MC to Correct the Weighed MC}", "lep")
            elif("Weighed_Acceptance_Comparisons"    in Canvas_Name):
                legend[Canvas_Name].SetHeader(f"#splitline{{Bin-by-Bin Acceptances Distributions for}}{{{Legend_Header}}}", "C")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"], "Unweighed MC REC", "lep")
                legend[Canvas_Name].AddEntry(Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_AcW"],   "Weighed MC REC", "lep")
            else:
                legend[Canvas_Name].SetHeader("Unknown Option", "C")
                
            Draw_Canvas(All_z_pT_Canvas_cd_1_Upper[Canvas_Name], 1, 0.15)
            Blank = Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)"].Clone("EMPTY")
            Blank.SetTitle("")
            Blank.Draw("H P E0")
            legend[Canvas_Name].DrawClone()
            ROOT.gPad.Update()
            All_z_pT_Canvas[Canvas_Name].Update()
            Binning_Title = f"{root_color.Bold}{{Q^{{2}}-y Bin {Q2_Y_Bin} #topbar z-P_{{T}} Bin All}}"
            if(args.title):
                Binning_Title = f"#splitline{{{Binning_Title}}}{{{args.title}}}"
            if("Uncorrected_Modulation_Comparisons"  in Canvas_Name):
                Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)"].SetTitle(Binning_Title)
                DrawNormalizedHistos(histos_in=[Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)"],     Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"], Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"], Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_AcW"], Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_AcW"]], TPad_draw=All_z_pT_Canvas_cd_1_Lower[Canvas_Name], Normalize_Q=True)
            elif("Bin_by_Bin_Comparisons_of_Weights" in Canvas_Name):
                Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"].SetTitle(Binning_Title)
                DrawNormalizedHistos(histos_in=[Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"], Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_AcW"], Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_Synthetic"]],                                                                                                                     TPad_draw=All_z_pT_Canvas_cd_1_Lower[Canvas_Name], Normalize_Q=False)
            elif("Weighed_Acceptance_Comparisons"    in Canvas_Name):
                Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"].SetTitle(Binning_Title)
                DrawNormalizedHistos(histos_in=[Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_NoW"], Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_0)_AcW"]],                                                                                                                                                                                        TPad_draw=All_z_pT_Canvas_cd_1_Lower[Canvas_Name], Normalize_Q=False)
            All_z_pT_Canvas[Canvas_Name].Update()
    
            for z_pT in range(1, Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=int(Q2_Y_Bin))[1]+1):
                if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT, BINNING_METHOD=Binning_Method)):
                    continue
                cd_number_of_z_pT_all_together = z_pT
                if(Plot_Orientation in ["z_pT"]):
                    All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2[Canvas_Name].cd(cd_number_of_z_pT_all_together)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
                else:
                    cd_row = int(cd_number_of_z_pT_all_together/number_of_cols) + 1
                    if(0  ==    (cd_number_of_z_pT_all_together%number_of_cols)):
                        cd_row += -1
                    cd_col =     cd_number_of_z_pT_all_together - ((cd_row - 1)*number_of_cols)
                    All_z_pT_Canvas_cd_2_z_pT_Bin_Row = All_z_pT_Canvas_cd_2[Canvas_Name].cd((number_of_cols - cd_col) + 1)
                    All_z_pT_Canvas_cd_2_z_pT_Bin     = All_z_pT_Canvas_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(root_color.LGrey)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
    
                Binning_Title = f"{root_color.Bold}{{Q^{{2}}-y Bin {Q2_Y_Bin} #topbar z-P_{{T}} Bin {z_pT}}}"
                if(args.title):
                    Binning_Title = f"#splitline{{{Binning_Title}}}{{{args.title}}}"
                if("Uncorrected_Modulation_Comparisons"  in Canvas_Name):
                    Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})"].SetTitle(Binning_Title)
                    DrawNormalizedHistos(histos_in=[Saved_Histos[f"rdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})"],     Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_NoW"], Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_NoW"], Saved_Histos[f"mdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_AcW"], Saved_Histos[f"gdf_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_AcW"]], TPad_draw=All_z_pT_Canvas_cd_2_z_pT_Bin, Normalize_Q=True)
                elif("Bin_by_Bin_Comparisons_of_Weights" in Canvas_Name):
                    Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_NoW"].SetTitle(Binning_Title)
                    # DrawNormalizedHistos(histos_in=[Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_NoW"], Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_AcW"], Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_Synthetic"]],                                                                                                                               TPad_draw=All_z_pT_Canvas_cd_2_z_pT_Bin, Normalize_Q=False)
                    DrawNormalizedHistos(histos_in=[Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_NoW"], Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_AcW"], Saved_Histos[f"bbb_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_Synthetic"]],                                                                                                                               TPad_draw=All_z_pT_Canvas_cd_2_z_pT_Bin, Normalize_Q=True)
                elif("Weighed_Acceptance_Comparisons"    in Canvas_Name):
                    Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_NoW"].SetTitle(Binning_Title)
                    # DrawNormalizedHistos(histos_in=[Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_NoW"], Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_AcW"]],                                                                                                                                                                                                       TPad_draw=All_z_pT_Canvas_cd_2_z_pT_Bin, Normalize_Q=False)
                    DrawNormalizedHistos(histos_in=[Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_NoW"], Saved_Histos[f"acc_(Q2_y_Bin_{Q2_Y_Bin})_(z_pT_Bin_{z_pT})_AcW"]],                                                                                                                                                                                                       TPad_draw=All_z_pT_Canvas_cd_2_z_pT_Bin, Normalize_Q=True)
    
                ROOT.gPad.Update()
                All_z_pT_Canvas[Canvas_Name].Update()
                    
            ##################################################################### ################################################################ ################################################################
            #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################
            ##################################################################### ################################################################ ################################################################
            Save_Name = f"{Canvas_Name}_{args.name}{args.File_Save_Format}"
            if(Plot_Orientation != "z_pT"):
                Save_Name = Save_Name.replace(f"{args.name}{args.File_Save_Format}", f"{args.name}_Flipped{args.File_Save_Format}")
            for replace in ["(", ")", "'", '"', "'"]:
                Save_Name = Save_Name.replace(replace, "")
            Save_Name = Save_Name.replace("__", "_")
            Save_Name = Save_Name.replace("_None.", ".")
            Save_Name = Save_Name.replace("_.", ".")
            All_z_pT_Canvas[Canvas_Name].SaveAs(Save_Name)
            print(f"{color.BGREEN}Saved Image: {color.BBLUE}{Save_Name}{color.END}")
            timer.time_elapsed()
            ##################################################################### ################################################################ ################################################################
            #####==========#####        Saving Canvas        #####==========##### ################################################################ ################################################################
            ##################################################################### ################################################################ ################################################################
        # After all canvases for this Q2_Y_Bin are saved:
        del rdf_cached, mdf_cached, gdf_cached
        gc.collect()  # explicitly release cached memory

    json_output_name = f"Bin_by_Bin_Acceptance_Weight_Uncertainty_Differences{f'_{args.name}' if(args.name not in ['']) else ''}.json"
    print(f"{color.BOLD}Saving new JSON file {color.END}({color.PINK}{json_output_name}{color.END})")
    # Save all differences to JSON for later uncertainty mapping
    with open(json_output_name, "w") as json_file:
        json.dump(Uncertainty_Output, json_file, indent=4)
    print(f"\n{color.BBLUE}Saved all bin-by-bin differences to: {color.BGREEN}{json_output_name}{color.END}\n")
    timer.time_elapsed()
    

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
        # if((args.make_2D_weight) and ("REAL_Data" not in str(folder.name))):
        #     print(f"{color.Error}Not running {folder.name} for 2D only plots at this time{color.END}")
        #     continue
            
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
            if(("FC_14" in str(f.name)) and ("GEN_MC" in str(folder.name))):
                continue
            if(verbose):
                print(f"\t{num+1:>5.0f}:   {color.CYAN}{f.name}{color.END}")
            if("EvGen" in str(f.name)):
                if("Acceptance_Tests" not in str(f.name)):
                    continue
                if("V3"               not in str(f.name)):
                    continue
                if(args.Do_not_use_EvGen):
                    if(verbose):
                        print(f"\t{color.Error}Not using EvGen files for Acceptance weights{color.END}\n")
                    continue
                all_root_files[array_name].append(f"{str(folder.name)}/{f.name}")
            elif("REAL" in str(folder.name)):
                if(len(all_root_files[array_name]) < args.num_rdf_files):
                    all_root_files[array_name].append(f"{str(folder.name)}/{f.name}")
            else:
                if("Acceptance_Tests" not in str(f.name)):
                    continue
                if("mdf" in array_name):
                    if("V4"           not in str(f.name)):
                        continue
                elif("V3"             not in str(f.name)):
                    continue
                all_root_files[f"{array_name}_clasdis"].append(f"{str(folder.name)}/{f.name}")
                # if(len(all_root_files[f"{array_name}_clasdis"]) < args.num_MC_files):
                #     current_name = f"{str(folder.name).replace('Matching_REC_MC', 'GEN_MC')}/{str(f.name).replace('DataFrame_SIDIS_epip_MC_Matched', 'DataFrame_SIDIS_epip_MC_GEN')}"
                #     if((array_name in ["mdf"]) and ((current_name not in all_root_files["gdf_clasdis"]) and (current_name.replace("_FC_14", "") not in all_root_files["gdf_clasdis"]))):
                #     # if((array_name in ["mdf"]) and (f"{str(folder.name).replace('Link_to_Volatile_MC_Matching', 'GEN_MC')}/{str(f.name).replace('DataFrame_SIDIS_epip_MC_Matched', 'DataFrame_SIDIS_epip_MC_GEN')}" not in all_root_files["gdf_clasdis"])):
                #         continue
                #     all_root_files[f"{array_name}_clasdis"].append(f"{str(folder.name)}/{f.name}")

    if(args.num_MC_files < 0):
        args.num_MC_files = max([len(all_root_files["gdf_clasdis"]), len(all_root_files["mdf_clasdis"]), len(all_root_files["gdf"]), len(all_root_files["mdf"])])
    remove_list = []
    for mc           in ["", "_clasdis"]:
        if(args.Do_not_use_EvGen and ("clasdis" not in mc)):
            continue
        all_root_files[f"gdf{mc}"].sort()
        all_root_files[f"mdf{mc}"].sort()
        count = 0
        for gdf_name in all_root_files[f"gdf{mc}"]:
            mdf_name     = gdf_name.replace("GEN_MC/",        "Matching_REC_MC/")
            mdf_name     = mdf_name.replace("MC_GEN_Pass_2_", "MC_Matched_Pass_2_")
            mdf_name     = mdf_name.replace("Tests_V",        "Tests_FC_14_V")
            if("EvGen" not in mdf_name):
                mdf_name = mdf_name.replace("V3",             "V4")
            if((mdf_name not in all_root_files[f"mdf{mc}"]) or (count > args.num_MC_files)):
                # print(f"Can't find {[gdf_name, mdf_name]} in 'mdf{mc}'\n")
                remove_list.append([mc, gdf_name, mdf_name])
            else:
                count += 1
        count = 0
        for mdf_name in all_root_files[f"mdf{mc}"]:
            gdf_name     = mdf_name.replace("Matching_REC_MC/",   "GEN_MC/")
            gdf_name     = gdf_name.replace("MC_Matched_Pass_2_", "MC_GEN_Pass_2_")
            gdf_name     = gdf_name.replace("FC_14_",             "")
            if("EvGen" not in gdf_name):
                gdf_name = gdf_name.replace("V4",                 "V3")
            if((gdf_name not in all_root_files[f"gdf{mc}"]) or (count > args.num_MC_files)):
                # print(f"Can't find {[gdf_name, mdf_name]} in 'gdf{mc}'\n")
                remove_list.append([mc, gdf_name, mdf_name])
            else:
                count += 1
    
    for ii in remove_list:
        mc, gdf_name, mdf_name = ii
        if(gdf_name in all_root_files[f"gdf{mc}"]):
            # print(f"Removing: {gdf_name}")
            all_root_files[f"gdf{mc}"].remove(gdf_name)
        if(mdf_name in all_root_files[f"mdf{mc}"]):
            # print(f"Removing: {mdf_name}")
            all_root_files[f"mdf{mc}"].remove(mdf_name)
    
    print(f"\n\n{color.BOLD}Will Run With:{color.END}\n")
    if(args.batch_id):
        all_root_files["rdf"]         = rdf_batch[args.batch_id]
        all_root_files["mdf_clasdis"] = mdf_batch[args.batch_id]
        all_root_files["gdf_clasdis"] = gdf_batch[args.batch_id]

    for ii in all_root_files:
        print(f"\n\t{color.BLUE}{ii}:{color.END}")
        for jj in all_root_files[ii]:
            print(f"\t\t{jj}")
        print(f"\n\t{color.CYAN}Total Number of files = {color.BBLUE}{len(all_root_files[ii])}{color.END}")
        
    args.num_rdf_files = len(all_root_files["rdf"])
    args.num_MC_files  = len(all_root_files["mdf_clasdis"])
    
    print(f"\n{color.BOLD}LOADING DATAFRAMES{color.END}")
    
    rdf           = ROOT.RDataFrame("h22", all_root_files["rdf"])
    mdf_clasdis   = ROOT.RDataFrame("h22", all_root_files["mdf_clasdis"])
    gdf_clasdis   = ROOT.RDataFrame("h22", all_root_files["gdf_clasdis"])
    if(not args.Do_not_use_EvGen):
        mdf_EvGen = ROOT.RDataFrame("h22", all_root_files["mdf"])
        gdf_EvGen = ROOT.RDataFrame("h22", all_root_files["gdf"])
    # else:
    #     rdf         = rdf.Range(500000)
    #     mdf_clasdis = mdf_clasdis.Range(500000)
    #     gdf_clasdis = gdf_clasdis.Range(500000)
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
    if(args.event_limit):
        rdf           = rdf.Range(args.event_limit)
        mdf_clasdis   = mdf_clasdis.Range(args.event_limit)
        gdf_clasdis   = gdf_clasdis.Range(args.event_limit)
        if(not args.Do_not_use_EvGen):
            mdf_EvGen = mdf_EvGen.Range(args.event_limit)
            gdf_EvGen = gdf_EvGen.Range(args.event_limit)

    if(not rdf.HasColumn("MM2")):
        print(f"{color.Error}Need to (re)define {color.END_B}'MM2'{color.Error} for 'rdf'{color.END}")
        rdf = rdf.Define("MM2", "MM*MM")
    if(not args.Do_not_use_EvGen):
        if(not mdf_EvGen.HasColumn("MM2")):
            print(f"{color.Error}Need to (re)define {color.END_B}'MM2'{color.Error} for 'mdf_EvGen'{color.END}")
            mdf_EvGen = mdf_EvGen.Define("MM2", "MM*MM")
        if(not mdf_EvGen.HasColumn("MM2_smeared")):
            print(f"{color.Error}Need to (re)define {color.END_B}'MM2_smeared'{color.Error} for 'mdf_EvGen'{color.END}")
            mdf_EvGen = mdf_EvGen.Define("MM2_smeared", "MM_smeared*MM_smeared")
        if(not gdf_EvGen.HasColumn("MM2")):
            print(f"{color.Error}Need to (re)define {color.END_B}'MM2'{color.Error} for 'gdf_EvGen'{color.END}")
            gdf_EvGen = gdf_EvGen.Define("MM2", "MM*MM")
    if(not mdf_clasdis.HasColumn("MM2")):
        print(f"{color.Error}Need to (re)define {color.END_B}'MM2'{color.Error} for 'mdf_clasdis'{color.END}")
        mdf_clasdis = mdf_clasdis.Define("MM2", "MM*MM")
    if(not mdf_clasdis.HasColumn("MM2_smeared")):
        print(f"{color.Error}Need to (re)define {color.END_B}'MM2_smeared'{color.Error} for 'mdf_clasdis'{color.END}")
        mdf_clasdis = mdf_clasdis.Define("MM2_smeared", "MM_smeared*MM_smeared")
    if(not gdf_clasdis.HasColumn("MM2")):
        print(f"{color.Error}Need to (re)define {color.END_B}'MM2'{color.Error} for 'gdf_clasdis'{color.END}")
        gdf_clasdis = gdf_clasdis.Define("MM2", "MM*MM")
    
    print(f"\n{color.BBLUE}rdf{color.END}:")
    if(verbose or (not True)):
        for ii in range(0, len(rdf.GetColumnNames()), 1):
            print(f"\t{str((rdf.GetColumnNames())[ii]).ljust(38)} (type -> {rdf.GetColumnType(rdf.GetColumnNames()[ii])})")
    if(not args.fast):
        print(f"\tTotal entries in {color.BBLUE}rdf{color.END} files: \n{rdf.Count().GetValue():>20.0f}")
        timer.time_elapsed()
    else:
        print("Fast Load...")
    
    print(f"\n{color.Error}mdf_clasdis{color.END}:")
    if(verbose or (not True)):
        for ii in range(0, len(mdf_clasdis.GetColumnNames()), 1):
            print(f"\t{str((mdf_clasdis.GetColumnNames())[ii]).ljust(38)} (type -> {mdf_clasdis.GetColumnType(mdf_clasdis.GetColumnNames()[ii])})")
    if(not args.fast):
        print(f"\tTotal entries in {color.Error}mdf_clasdis{color.END} files: \n{mdf_clasdis.Count().GetValue():>20.0f}")
        timer.time_elapsed()
    else:
        print("Fast Load...")
    
    print(f"\n{color.BGREEN}gdf_clasdis{color.END}:")
    if(verbose or (not True)):
        for ii in range(0, len(gdf_clasdis.GetColumnNames()), 1):
            print(f"\t{str((gdf_clasdis.GetColumnNames())[ii]).ljust(38)} (type -> {gdf_clasdis.GetColumnType(gdf_clasdis.GetColumnNames()[ii])})")
    if(not args.fast):
        print(f"\tTotal entries in {color.BGREEN}gdf_clasdis{color.END} files: \n{gdf_clasdis.Count().GetValue():>20.0f}")
        timer.time_elapsed()
    else:
        print("Fast Load...")
    
    if(not args.Do_not_use_EvGen):
        print(f"\n{color.BOLD}{color.PINK}mdf_EvGen{color.END}:")
        if(verbose or (not True)):
            for ii in range(0, len(mdf_EvGen.GetColumnNames()), 1):
                print(f"\t{str((mdf_EvGen.GetColumnNames())[ii]).ljust(38)} (type -> {mdf_EvGen.GetColumnType(mdf_EvGen.GetColumnNames()[ii])})")
        if(not args.fast):
            print(f"\tTotal entries in {color.BOLD}{color.PINK}mdf_EvGen{color.END} files: \n{mdf_EvGen.Count().GetValue():>20.0f}")
            timer.time_elapsed()
        else:
            print("Fast Load...")
        
        print(f"\n{color.BCYAN}gdf_EvGen{color.END}:")
        if(verbose or (not True)):
            for ii in range(0, len(gdf_EvGen.GetColumnNames()), 1):
                print(f"\t{str((gdf_EvGen.GetColumnNames())[ii]).ljust(38)} (type -> {gdf_EvGen.GetColumnType(gdf_EvGen.GetColumnNames()[ii])})")
        if(not args.fast):
            print(f"\tTotal entries in {color.BCYAN}gdf_EvGen{color.END} files: \n{gdf_EvGen.Count().GetValue():>20.0f}")
            timer.time_elapsed()
        else:
            print("Fast Load...")
        
    
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
    
    # # clasdis Generation Cuts
    # mdf_EvGen   =   mdf_EvGen.Filter("((Q2_gen > 0.85) && (Q2_gen < 20.0)) && ((xB_gen > 0.05) && (xB_gen < 0.95)) && ((y_gen > 0.05) && (y_gen < 0.95)) && ((z_gen > 0.01) && (z_gen < 0.95)) && (((W_gen*W_gen) > 4.0) && ((W_gen*W_gen) < 50.0))")
    # gdf_EvGen   =   gdf_EvGen.Filter("((Q2     > 0.85) && (Q2     < 20.0)) && ((xB     > 0.05) && (xB     < 0.95)) && ((y     > 0.05) && (y     < 0.95)) && ((z     > 0.01) && (z     < 0.95)) && (((W    *    W) > 4.0) && ((W    *    W) < 50.0))")
    # mdf_clasdis = mdf_clasdis.Filter("((Q2_gen > 0.85) && (Q2_gen < 20.0)) && ((xB_gen > 0.05) && (xB_gen < 0.95)) && ((y_gen > 0.05) && (y_gen < 0.95)) && ((z_gen > 0.01) && (z_gen < 0.95)) && (((W_gen*W_gen) > 4.0) && ((W_gen*W_gen) < 50.0))")
    # gdf_clasdis = gdf_clasdis.Filter("((Q2     > 0.85) && (Q2     < 20.0)) && ((xB     > 0.05) && (xB     < 0.95)) && ((y     > 0.05) && (y     < 0.95)) && ((z     > 0.01) && (z     < 0.95)) && (((W    *    W) > 4.0) && ((W    *    W) < 50.0))")

    # EvGen Generation Cuts
    if(not args.Do_not_use_EvGen):
        mdf_EvGen =   mdf_EvGen.Filter("((Q2_gen > 1.5) && (Q2_gen < 20.0)) && ((xB_gen > 0.05) && (xB_gen < 0.95)) && ((y_gen > 0.05) && (y_gen < 0.95)) && ((z_gen > 0.01) && (z_gen < 0.95)) && (((W_gen*W_gen) > 4.0) && ((W_gen*W_gen) < 50.0))")
        gdf_EvGen =   gdf_EvGen.Filter("((Q2     > 1.5) && (Q2     < 20.0)) && ((xB     > 0.05) && (xB     < 0.95)) && ((y     > 0.05) && (y     < 0.95)) && ((z     > 0.01) && (z     < 0.95)) && (((W    *    W) > 4.0) && ((W    *    W) < 50.0))")
    mdf_clasdis   = mdf_clasdis.Filter("((Q2_gen > 1.5) && (Q2_gen < 20.0)) && ((xB_gen > 0.05) && (xB_gen < 0.95)) && ((y_gen > 0.05) && (y_gen < 0.95)) && ((z_gen > 0.01) && (z_gen < 0.95)) && (((W_gen*W_gen) > 4.0) && ((W_gen*W_gen) < 50.0))")
    gdf_clasdis   = gdf_clasdis.Filter("((Q2     > 1.5) && (Q2     < 20.0)) && ((xB     > 0.05) && (xB     < 0.95)) && ((y     > 0.05) && (y     < 0.95)) && ((z     > 0.01) && (z     < 0.95)) && (((W    *    W) > 4.0) && ((W    *    W) < 50.0))")
    
    # clasdis Generation Cuts (y ended at 0.93 apparently?)
    if(not args.Do_not_use_EvGen):
        mdf_EvGen =   mdf_EvGen.Filter("((y_gen > 0.05) && (y_gen < 0.93))")
        gdf_EvGen =   gdf_EvGen.Filter("((y     > 0.05) && (y     < 0.93))")
    mdf_clasdis   = mdf_clasdis.Filter("((y_gen > 0.05) && (y_gen < 0.93))")
    gdf_clasdis   = gdf_clasdis.Filter("((y     > 0.05) && (y     < 0.93))")
    
    # EvGen Generation Cuts (OLD)
    if(not args.Do_not_use_EvGen):
        mdf_EvGen =   mdf_EvGen.Filter("((z_gen > 0.15) && (z_gen < 0.90))")
        gdf_EvGen =   gdf_EvGen.Filter("((z     > 0.15) && (z     < 0.90))")
    mdf_clasdis   = mdf_clasdis.Filter("((z_gen > 0.15) && (z_gen < 0.90))")
    gdf_clasdis   = gdf_clasdis.Filter("((z     > 0.15) && (z     < 0.90))")

    if(not (args.kinematic_compare or args.Do_not_use_EvGen)):
        print(f"{color.BGREEN}Adding MM cuts to gdf files for Acceptance Corrections{color.END}\n")
        gdf_EvGen   =   gdf_EvGen.Filter("MM > 1.5")
        gdf_clasdis = gdf_clasdis.Filter("MM > 1.5")
    
    
    # Normal Analysis Cuts
    rdf           = DF_Filter_Function_Full(DF_Out=rdf,         Titles_or_DF="DF", Data_Type="rdf", Cut_Choice="cut_Complete_SIDIS", Smearing_Q="")
    if(not args.Do_not_use_EvGen):
        mdf_EvGen = DF_Filter_Function_Full(DF_Out=mdf_EvGen,   Titles_or_DF="DF", Data_Type="mdf", Cut_Choice="cut_Complete_SIDIS", Smearing_Q="")
    mdf_clasdis   = DF_Filter_Function_Full(DF_Out=mdf_clasdis, Titles_or_DF="DF", Data_Type="mdf", Cut_Choice="cut_Complete_SIDIS", Smearing_Q="smear")

    if(args.cut):
        print(f"{color.Error}Applying User Cut: {color.END_B}{args.cut}{color.END}")
        rdf           =         rdf.Filter(args.cut)
        if(not args.Do_not_use_EvGen):
            mdf_EvGen =   mdf_EvGen.Filter(args.cut)
            gdf_EvGen =   gdf_EvGen.Filter(args.cut)
        mdf_clasdis   = mdf_clasdis.Filter(args.cut)
        gdf_clasdis   = gdf_clasdis.Filter(args.cut)

    if(not args.fast):
        print(f"\t(New) Total entries in {color.BBLUE}rdf        {color.END} files: \n{rdf.Count().GetValue():>20.0f}")
        timer.time_elapsed()
        print(f"\t(New) Total entries in {color.Error}mdf_clasdis{color.END} files: \n{mdf_clasdis.Count().GetValue():>20.0f}")
        timer.time_elapsed()
        print(f"\t(New) Total entries in {color.BGREEN}gdf_clasdis{color.END} files: \n{gdf_clasdis.Count().GetValue():>20.0f}")
        timer.time_elapsed()
        if(not args.Do_not_use_EvGen):
            print(f"\t(New) Total entries in {color.BOLD}{color.PINK}mdf_EvGen  {color.END} files: \n{mdf_EvGen.Count().GetValue():>20.0f}")
            timer.time_elapsed()
            print(f"\t(New) Total entries in {color.BCYAN}gdf_EvGen  {color.END} files: \n{gdf_EvGen.Count().GetValue():>20.0f}")
            timer.time_elapsed()
    else:
        print(f"\n{color.BGREEN}Done with Cuts {color.END_B}(Ran with 'fast' setting to skip the statistics change){color.END}\n")

    if(args.make_2D_weight_binned_check):
        print(f"\n{color.BOLD}CREATING/TESTING ACCEPTANCE WEIGHTED HISTOGRAMS (phi_h in every individual Q2-y-z-pT bin){color.END}\n")
        
        # 1) Define Event_Weight on MC (mdf)
        if(args.json_weights):
            # With the Modulation weights option, apply the modulations to both gdf and mdf before adding the acceptance weights to mdf
            print(f"\n{color.BBLUE}Using phi_h Modulation Weights from the JSON file.{color.END}\n")
            with open(JSON_WEIGHT_FILE) as f:
                Fit_Pars = json.load(f)
                # Build the C++ initialization string
                cpp_map_str = "{"
                for key, val in Fit_Pars.items():
                    cpp_map_str += f'{{"{key}", {val}}},'
                cpp_map_str += "}"
                
                ROOT.gInterpreter.Declare(f"""
                #include <map>
                #include <string>
                #include <cmath>
                
                std::map<std::string, double> Fit_Pars = {cpp_map_str};
                
                double ComputeWeight(int Q2_y_Bin, int z_pT_Bin, double phi_h) {{
                    // build the keys dynamically
                    // std::string keyA = "A_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                    std::string keyB = "B_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                    std::string keyC = "C_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                
                    // safely retrieve parameters (default = 0)
                    // double Par_A = Fit_Pars.count(keyA) ? Fit_Pars[keyA] : 0.0;
                    double Par_B = Fit_Pars.count(keyB) ? Fit_Pars[keyB] : 0.0;
                    double Par_C = Fit_Pars.count(keyC) ? Fit_Pars[keyC] : 0.0;
                
                    // calculate weight
                    double phi_rad = phi_h * TMath::DegToRad();
                    double weight  = (1.0 + Par_B * std::cos(phi_rad) + Par_C * std::cos(2.0 * phi_rad));
                
                    return weight;
                }}
                """)
                
            # mdf_clasdis = mdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen) * (accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            gdf_clasdis = gdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_Y_Bin,     z_pT_Bin_Y_bin,     phi_t)")
            mdf_clasdis = mdf_clasdis.Define("W_pre", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
            mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            mdf_clasdis = mdf_clasdis.Define("Event_Weight", "W_pre * W_acc")
            # mdf_tmp     = mdf_clasdis.Define("W_pre", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
            # pre_sum     = mdf_tmp.Sum("W_pre").GetValue()
            # mdf_tmp     = mdf_tmp.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            # mdf_tmp     = mdf_tmp.Define("Event_Weight_raw", "W_pre * W_acc")
            # post_sum    = mdf_tmp.Sum("Event_Weight_raw").GetValue()
            # scale       = (pre_sum / post_sum) if(post_sum != 0.0) else 1.0
            # mdf_clasdis = mdf_tmp.Define("Event_Weight", f"Event_Weight_raw * ({scale})")
        else:
            # mdf_clasdis = mdf_clasdis.Define("Event_Weight", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            gdf_clasdis = gdf_clasdis.Define("Event_Weight", "1.0")
            # mdf_tmp     = mdf_clasdis.Define("Event_Weight", "1.0")
            # pre_sum     = mdf_tmp.Sum("Event_Weight").GetValue()
            # mdf_tmp     = mdf_tmp.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            # mdf_tmp     = mdf_tmp.Define("Event_Weight_raw", "Event_Weight * W_acc")
            # post_sum    = mdf_tmp.Sum("Event_Weight_raw").GetValue()
            # scale       = (pre_sum / post_sum) if(post_sum != 0.0) else 1.0
            # mdf_clasdis = mdf_tmp.Redefine("Event_Weight", f"Event_Weight_raw * ({scale})")
            mdf_clasdis = mdf_clasdis.Define("Event_Weight", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")

        print(f"\n{color.BOLD}About to start running 'z_pT_Images_Together_For_Comparisons'{color.END}\n")
        timer.time_elapsed()
        z_pT_Images_Together_For_Comparisons(rdf_in=rdf, mdf_in=mdf_clasdis, gdf_in=gdf_clasdis, Q2_Y_Bin_List=range(1, 18), Plot_Orientation="z_pT", Nrdf=len(all_root_files["rdf"]), Nmdf=len(all_root_files["mdf_clasdis"]))

        print(f"\n{color.BGREEN}Done Running 'z_pT_Images_Together_For_Comparisons'{color.END}\n")
        
    elif(args.make_2D_weight_check):
        print(f"\n{color.BOLD}CREATING/TESTING ACCEPTANCE WEIGHTED HISTOGRAMS ({args.Var_weight_check}){color.END}\n")
        
        # 1) Define Event_Weight on MC (mdf)
        if(args.json_weights):
            # With the Modulation weights option, apply the modulations to both gdf and mdf before adding the acceptance weights to mdf
            print(f"\n{color.BBLUE}Using phi_h Modulation Weights from the JSON file.{color.END}\n")
            with open(JSON_WEIGHT_FILE) as f:
                Fit_Pars = json.load(f)
                # Build the C++ initialization string
                cpp_map_str = "{"
                for key, val in Fit_Pars.items():
                    cpp_map_str += f'{{"{key}", {val}}},'
                cpp_map_str += "}"
                
                ROOT.gInterpreter.Declare(f"""
                #include <map>
                #include <string>
                #include <cmath>
                
                std::map<std::string, double> Fit_Pars = {cpp_map_str};
                
                double ComputeWeight(int Q2_y_Bin, int z_pT_Bin, double phi_h) {{
                    // build the keys dynamically
                    // std::string keyA = "A_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                    std::string keyB = "B_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                    std::string keyC = "C_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                
                    // safely retrieve parameters (default = 0)
                    // double Par_A = Fit_Pars.count(keyA) ? Fit_Pars[keyA] : 0.0;
                    double Par_B = Fit_Pars.count(keyB) ? Fit_Pars[keyB] : 0.0;
                    double Par_C = Fit_Pars.count(keyC) ? Fit_Pars[keyC] : 0.0;
                
                    // calculate weight
                    double phi_rad = phi_h * TMath::DegToRad();
                    double weight  = (1.0 + Par_B * std::cos(phi_rad) + Par_C * std::cos(2.0 * phi_rad));
                
                    return weight;
                }}
                """)
                
            # mdf_clasdis = mdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen) * (accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            gdf_clasdis = gdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_Y_Bin,     z_pT_Bin_Y_bin,     phi_t)")
            mdf_tmp     = mdf_clasdis.Define("W_pre", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
            pre_sum     = mdf_tmp.Sum("W_pre").GetValue()
            mdf_tmp     = mdf_tmp.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            mdf_tmp     = mdf_tmp.Define("Event_Weight_raw", "W_pre * W_acc")
            post_sum    = mdf_tmp.Sum("Event_Weight_raw").GetValue()
            scale       = (pre_sum / post_sum) if(post_sum != 0.0) else 1.0
            mdf_clasdis = mdf_tmp.Define("Event_Weight", f"Event_Weight_raw * ({scale})")
        else:
            # mdf_clasdis = mdf_clasdis.Define("Event_Weight", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            gdf_clasdis = gdf_clasdis.Define("Event_Weight", "1.0")
            mdf_tmp     = mdf_clasdis.Define("Event_Weight", "1.0")
            pre_sum     = mdf_tmp.Sum("Event_Weight").GetValue()
            mdf_tmp     = mdf_tmp.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
            mdf_tmp     = mdf_tmp.Define("Event_Weight_raw", "Event_Weight * W_acc")
            post_sum    = mdf_tmp.Sum("Event_Weight_raw").GetValue()
            scale       = (pre_sum / post_sum) if(post_sum != 0.0) else 1.0
            mdf_clasdis = mdf_tmp.Redefine("Event_Weight", f"Event_Weight_raw * ({scale})")

        print(f"\n{color.BOLD}Done defining the Event Weights{color.END}\n")
        timer.time_elapsed()


        varible_title = variable_Title_name_new(args.Var_weight_check)
        var, minBin, maxBin, numBin  = 'phi_t', 0.00,  360,  24
        if(str(args.Var_weight_check) in ["Q2"]):
            var, minBin, maxBin, numBin = "Q2", 0.00, 12.0, 240
        if(str(args.Var_weight_check) in ["y"]):
            var, minBin, maxBin, numBin =  "y", 0.05, 1.05, 100
        if(str(args.Var_weight_check) in ["xB"]):
            var, minBin, maxBin, numBin = "xB", 0.05, 0.85,  80
        if(str(args.Var_weight_check) in ["z"]):
            var, minBin, maxBin, numBin =  "z", 0.00, 1.20, 120
        if(str(args.Var_weight_check) in ["pT"]):
            var, minBin, maxBin, numBin = "pT", 0.00, 2.00, 200
        # 2) Book TH1D histograms for the selected variable
        Title = f"Comparisons of {varible_title}"
        if(args.title):
            Title = f"#splitline{{{Title}}}{{{args.title}}}"
        h_rdf =         rdf.Histo1D(("h_1D_rdf", f"{Title}; {varible_title}; Normalized",                                                               numBin, minBin, maxBin), f"{var}")
        h_mdf = mdf_clasdis.Histo1D(("h_1D_mdf", f"#splitline{{Comparisons of {varible_title}}}{{Without Reweighted MC}}; {varible_title}; Normalized", numBin, minBin, maxBin), f"{var}_smeared")
        h_gdf = gdf_clasdis.Histo1D(("h_1D_gdf", f"#splitline{{Comparisons of {varible_title}}}{{Without Reweighted MC}}; {varible_title}; Normalized", numBin, minBin, maxBin), f"{var}")
        w_mdf = mdf_clasdis.Histo1D(("w_1D_mdf", f"{Title}; {varible_title}; Normalized",                                                               numBin, minBin, maxBin), f"{var}_smeared", "Event_Weight")
        w_gdf = gdf_clasdis.Histo1D(("w_1D_gdf", f"{Title}; {varible_title}; Normalized",                                                               numBin, minBin, maxBin), f"{var}",         "Event_Weight")
        
        # 3) Set line colors (on the actual TH1 objects)
        h_rdf.GetValue().SetLineColor(ROOT.kBlue)
        h_mdf.GetValue().SetLineColor(ROOT.kRed)
        h_gdf.GetValue().SetLineColor(ROOT.kGreen)

        w_mdf.GetValue().SetLineColor(ROOT.kPink + 10)
        w_gdf.GetValue().SetLineColor(ROOT.kCyan)
        
        # 4) Make normalized clones for maxima AND drawing
        def _make_norm_clone(hptr, name):
            h = hptr.GetValue().Clone(name)
            integral = h.Integral()
            if((integral != 0.0)):
                h.Scale(1.0/integral)
            return h
        
        h_rdf_n = _make_norm_clone(h_rdf, "h_1D_rdf_norm")
        h_mdf_n = _make_norm_clone(h_mdf, "h_1D_mdf_norm")
        h_gdf_n = _make_norm_clone(h_gdf, "h_1D_gdf_norm")
        w_mdf_n = _make_norm_clone(w_mdf, "w_1D_mdf_norm")
        w_gdf_n = _make_norm_clone(w_gdf, "w_1D_gdf_norm")
        
        comp_wW = w_mdf_n.Clone("w_1D_Compare")
        comp_nW = h_mdf_n.Clone("h_1D_Compare")

        comp_wW.Divide(h_rdf_n)
        comp_nW.Divide(h_rdf_n)

        comp_wW.SetLineColor(ROOT.kBlack)
        comp_nW.SetLineColor(ROOT.kBlack)

        comp_wW.SetTitle(f"#scale[1.25]{{#splitline{{Comparisons of Data and MC}}{{WITH Reweighted MC}}}}; {varible_title}; #frac{{MC REC}}{{Data}}")
        comp_nW.SetTitle(f"#scale[1.25]{{#splitline{{Comparisons of Data and MC}}{{WITHOUT Reweighted MC}}}}; {varible_title}; #frac{{MC REC}}{{Data}}")

        CwW_max, CwW_min = comp_wW.GetMaximum(), comp_wW.GetMinimum()
        CnW_max, CnW_min = comp_nW.GetMaximum(), comp_nW.GetMinimum()

        Comp_Max = max([1.3*CwW_max, 1.3*CnW_max, 0.5*CwW_max, 0.5*CnW_max, 1.3])
        Comp_Min = min([1.3*CwW_max, 1.3*CnW_max, 0.5*CwW_max, 0.5*CnW_max, 0.7])
        
        rdf_max = h_rdf_n.GetMaximum()
        mdf_max = w_mdf_n.GetMaximum()
        gdf_max = w_gdf_n.GetMaximum()
        global_max = max([rdf_max, mdf_max, gdf_max, 1e-5])
        
        # 5) Draw overlay on one canvas (first drawn sets axes)
        # c_phi = ROOT.TCanvas("c_phi_t_overlay", "phi_t overlays", 900, 600)
        c_phi = ROOT.TCanvas("c_1D_overlay", f"{args.Var_weight_check} overlays", int(912*1.55*25), int(547*1.55*25))
        c_phi.Divide(2, 2)
        
        # ----- Pad 1: Data vs Reweighted MC -----
        c_phi.cd(1)
        h_rdf_n.GetYaxis().SetRangeUser(0.0, 1.2*global_max)
        h_rdf_n.Draw("H P E0")
        w_mdf_n.Draw("H P E0 same")
        w_gdf_n.Draw("H P E0 same")
        
        # Legend for pad 1
        # leg1 = ROOT.TLegend(0.62, 0.70, 0.88, 0.88)  # top-right; adjust if needed
        leg1 = ROOT.TLegend(0.38, 0.12, 0.62, 0.3)  # bottom-center
        leg1.SetBorderSize(0)
        leg1.SetFillStyle(0)
        leg1.SetTextSize(0.04)
        leg1.AddEntry(h_rdf_n, "Experimental Data", "l")
        leg1.AddEntry(w_mdf_n, "MC REC (Reweighted)", "l")
        leg1.AddEntry(w_gdf_n, "MC GEN (Modulated)", "l")
        leg1.Draw()
        
        # ----- Pad 2: Data vs Default MC -----
        c_phi.cd(2)
        h_gdf_n.GetYaxis().SetRangeUser(0.0, 1.2*global_max)
        h_gdf_n.Draw("H P E0")
        h_rdf_n.Draw("H P E0 same")
        h_mdf_n.Draw("H P E0 same")
        
        # Legend for pad 2
        leg2 = ROOT.TLegend(0.38, 0.12, 0.62, 0.3)  # bottom-center
        leg2.SetBorderSize(0)
        leg2.SetFillStyle(0)
        leg2.SetTextSize(0.04)
        leg2.AddEntry(h_rdf_n, "Experimental Data", "l")
        leg2.AddEntry(h_gdf_n, "MC GEN (Default)", "l")
        leg2.AddEntry(h_mdf_n, "MC REC (Default)", "l")
        leg2.Draw()
        
        # ----- Pad 3: Ratio WITH reweighting -----
        c_phi.cd(3)
        comp_wW.GetYaxis().SetRangeUser(Comp_Min, Comp_Max)
        comp_wW.Draw("H P E0")
        l_w = ROOT.TLine(0, 1.0, 360, 1.0)
        l_w.SetLineStyle(2)
        l_w.SetLineWidth(2)
        l_w.SetLineColor(ROOT.kGray)
        l_w.Draw("same")

        # Compute average bin content (exclude under/overflow)
        def _avg_bin_content(h):
            nb = h.GetNbinsX()
            s = 0.0
            for i in range(1, nb + 1):
                s += h.GetBinContent(i)
            return (s / nb) if(nb > 0) else 0.0
        
        avg_w = _avg_bin_content(comp_wW)
        # Add a small NDC stat box
        pt3 = ROOT.TPaveText(0.38, 0.6, 0.62, 0.65, "NDC")
        pt3.SetFillStyle(0)
        pt3.SetBorderSize(0)
        pt3.SetTextAlign(12)  # left-adjust text inside box
        pt3.SetTextSize(0.04)
        pt3.AddText(f"Average = {avg_w:.4f}")
        pt3.Draw()
        
        # ----- Pad 4: Ratio WITHOUT reweighting -----
        c_phi.cd(4)
        comp_nW.GetYaxis().SetRangeUser(Comp_Min, Comp_Max)
        comp_nW.Draw("H P E0")
        l_h = ROOT.TLine(0, 1.0, 360, 1.0)
        l_h.SetLineStyle(2)
        l_h.SetLineWidth(2)
        l_h.SetLineColor(ROOT.kGray)
        l_h.Draw("same")
        
        avg_nw = _avg_bin_content(comp_nW)
        # pt4 = ROOT.TPaveText(0.68, 0.80, 0.94, 0.92, "NDC")
        pt4 = ROOT.TPaveText(0.38, 0.6, 0.62, 0.65, "NDC")
        pt4.SetFillStyle(0)
        pt4.SetBorderSize(0)
        pt4.SetTextAlign(12)
        pt4.SetTextSize(0.04)
        pt4.AddText(f"Average = {avg_nw:.4f}")
        pt4.Draw()
        
        c_phi.Update()

        
        # save_name = f"phi_h_Comparison_with_Acceptance_Weights{args.File_Save_Format}" if(not args.name) else f"phi_h_Comparison_with_Acceptance_Weights_{args.name}{args.File_Save_Format}"
        save_name = f"{args.Var_weight_check}_Comparison_with_and_without_Acceptance_Weights{args.File_Save_Format}" if(not args.name) else f"{args.Var_weight_check}_Comparison_with_and_without_Acceptance_Weights_{args.name}{args.File_Save_Format}"
        c_phi.SaveAs(save_name)
        print(f"{color.BOLD}Saved: {color.BBLUE}{save_name}{color.END}")

    
    elif(args.make_2D_weight):
        print(f"\n{color.BOLD}CREATING ACCEPTANCE WEIGHTS HISTOGRAMS/CODE{color.END}\n")
        # El_Binning                 = ['el',     2.64, 7.88, 524]
        # El_Th_Binning              = ['elth',      5,   35, 300]
        # El_Phi_Binning             = ['elPhi',     0,  360, 720]
        # Pip_Binning                = ['pip',    1.25,    5, 375]
        # Pip_Th_Binning             = ['pipth',     5,   35, 300]
        # Pip_Phi_Binning            = ['pipPhi',    0,  360, 720]

        # El_Binning                 = ['el',      2.6,  7.9, 53]
        # El_Th_Binning              = ['elth',      5,   35, 30]
        # El_Phi_Binning             = ['elPhi',     0,  360, 72]
        # Pip_Binning                = ['pip',     1.2,    5, 38]
        # Pip_Th_Binning             = ['pipth',     5,   35, 30]
        # Pip_Phi_Binning            = ['pipPhi',    0,  360, 72]

        # El_Binning                 = ['el',      2.5,  8.0, 11]
        # El_Th_Binning              = ['elth',    7.5, 35.5, 14]
        # El_Phi_Binning             = ['elPhi',     0,  360, 36]
        # Pip_Binning                = ['pip',     1.0,    5,  8]
        # Pip_Th_Binning             = ['pipth',   7.5, 35.5, 14]
        # Pip_Phi_Binning            = ['pipPhi',    0,  360, 36]

        El_Binning                 = ['el',      2.5,  8.0,  44]
        El_Th_Binning              = ['elth',    7.5, 35.5,  56]
        El_Phi_Binning             = ['elPhi',     0,  360, 144]
        Pip_Binning                = ['pip',     1.0,    5,  32]
        Pip_Th_Binning             = ['pipth',   4.5, 35.5,  62]
        Pip_Phi_Binning            = ['pipPhi',    0,  360, 144]
        
        List_of_Quantities_2D = []
        List_of_Quantities_2D.append([El_Phi_Binning, Pip_Phi_Binning])
        List_of_Quantities_2D.append([El_Th_Binning,  Pip_Th_Binning])
        List_of_Quantities_2D.append([El_Binning,     Pip_Binning])
        
        histos_data_match = {}

        canvas_data_match = ROOT.TCanvas("canvas_data_match", "My Canvas", int(912*1.55*25), int(547*1.55*25))
        canvas_data_match.Divide(len(List_of_Quantities_2D), 5)

        # -----------------------------
        # 1) One-time C++ helpers
        # -----------------------------
        One_Time_Cpp_Helpers = r"""
#include <vector>
#include <algorithm>
#include <cmath>
#include <string>

inline int accw_findBin(const double value, const std::vector<double>& edges){
    if((value < edges.front()) or (value >= edges.back())){
        return -1;
    }
    auto it = std::upper_bound(edges.begin(), edges.end(), value);
    int idx = int(it - edges.begin()) - 1;
    if((idx < 0) or (idx >= int(edges.size()) - 1)){
        return -1;
    }
    return idx;
}

inline double accw_lookup2D(const double x, const double y,
                            const std::vector<double>& ex,
                            const std::vector<double>& ey,
                            const std::vector<double>& grid){
    const int nx = int(ex.size()) - 1;
    const int ny = int(ey.size()) - 1;

    int ix = accw_findBin(x, ex);
    int iy = accw_findBin(y, ey);

    if((ix < 0) or (iy < 0)){
        return 1.0; // under/overflow policy
    }

    const int idx = ix + nx*iy; // row-major
    double w = grid[idx];
    if(!(w >= 0.0) or (!std::isfinite(w))){
        return 1.0;
    }
    return w;
}
"""
        ROOT.gInterpreter.Declare(One_Time_Cpp_Helpers)

        # Accumulate generated wrappers to save for later use
        generated_wrappers_code = []
        generated_wrappers_code.append("// Auto-generated acceptance weight functions\n")

        def _cpp_list(vals):
            return "{" + ", ".join(f"{v:.16g}" for v in vals) + "}"

        if(args.json_weights):
            print(f"\n{color.BBLUE}Using phi_h Modulation Weights from the JSON file.{color.END}\n")
            with open(JSON_WEIGHT_FILE) as f:
                Fit_Pars = json.load(f)
                # Build the C++ initialization string
                cpp_map_str = "{"
                for key, val in Fit_Pars.items():
                    cpp_map_str += f'{{"{key}", {val}}},'
                cpp_map_str += "}"
                
                ROOT.gInterpreter.Declare(f"""
                #include <map>
                #include <string>
                #include <cmath>
                
                std::map<std::string, double> Fit_Pars = {cpp_map_str};
                
                double ComputeWeight(int Q2_y_Bin, int z_pT_Bin, double phi_h) {{
                    // build the keys dynamically
                    // std::string keyA = "A_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                    std::string keyB = "B_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                    std::string keyC = "C_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                
                    // safely retrieve parameters (default = 0)
                    // double Par_A = Fit_Pars.count(keyA) ? Fit_Pars[keyA] : 0.0;
                    double Par_B = Fit_Pars.count(keyB) ? Fit_Pars[keyB] : 0.0;
                    double Par_C = Fit_Pars.count(keyC) ? Fit_Pars[keyC] : 0.0;
                
                    // calculate weight
                    double phi_rad = phi_h * TMath::DegToRad();
                    double weight  = (1.0 + Par_B * std::cos(phi_rad) + Par_C * std::cos(2.0 * phi_rad));
                
                    return weight;
                }}
                """)
            wdf = mdf_clasdis.Define("ACC_Weight_Product", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
        else:
            wdf = mdf_clasdis.Define("ACC_Weight_Product", "1.0")

        print(f"\n{color.BOLD}Starting 2D Histogram Loops{color.END}\n")
        timer.time_elapsed()

        for num, (x_vars, y_vars) in enumerate(List_of_Quantities_2D):
            var_x, Min_range_x, Max_range_x, Num_of_Bins_x = x_vars
            var_y, Min_range_y, Max_range_y, Num_of_Bins_y = y_vars

            rdf_name        = f"{var_x}_vs_{var_y}_rdf"
            mclasdis        = f"{var_x}_vs_{var_y}_mdf"
            data_match_name = f"{var_x}_vs_{var_y}"

            print(f"\n{color.BOLD}Starting '{data_match_name}' Histograms{color.END}")
            
            Title = f"Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"
            if(args.title):
                Title = f"#splitline{{Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"

            # -----------------------------
            # 2) Build 2D histos
            # -----------------------------
            histos_data_match[rdf_name]                = rdf.Histo2D((rdf_name,                Title.replace("SOURCE", f"#color[{ROOT.kBlue}]{{Experimental Data}}"),               Num_of_Bins_x, Min_range_x, Max_range_x, Num_of_Bins_y, Min_range_y, Max_range_y),    var_x,              var_y)
            histos_data_match[mclasdis]                = wdf.Histo2D((mclasdis,                Title.replace("SOURCE", f"#color[{ROOT.kRed}]{{Smeared MC REC (clasdis)}}"),         Num_of_Bins_x, Min_range_x, Max_range_x, Num_of_Bins_y, Min_range_y, Max_range_y), f"{var_x}_smeared", f"{var_y}_smeared", "ACC_Weight_Product")
            histos_data_match[f"{mclasdis}_no_weight"] = wdf.Histo2D((f"{mclasdis}_no_weight", Title.replace("SOURCE", f"#color[{ROOT.kMagenta}]{{Unweighted MC REC (clasdis)}}"),  Num_of_Bins_x, Min_range_x, Max_range_x, Num_of_Bins_y, Min_range_y, Max_range_y), f"{var_x}_smeared", f"{var_y}_smeared")

            histos_data_match[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var_x)} (Smeared)")
            histos_data_match[mclasdis].GetYaxis().SetTitle(f"{variable_Title_name_new(var_y)} (Smeared)")
            histos_data_match[f"{mclasdis}_no_weight"].GetXaxis().SetTitle(f"{variable_Title_name_new(var_x)} (Smeared)")
            histos_data_match[f"{mclasdis}_no_weight"].GetYaxis().SetTitle(f"{variable_Title_name_new(var_y)} (Smeared)")

            rdf_name_norm_factor = histos_data_match[rdf_name].Integral()
            mclasdis_norm_factor = histos_data_match[mclasdis].Integral()
            mclasdis_NoWn_factor = histos_data_match[f"{mclasdis}_no_weight"].Integral()

            histos_data_match[f"norm_{rdf_name}"]           = histos_data_match[rdf_name].Clone(f"norm_{rdf_name}")
            histos_data_match[f"norm_{mclasdis}"]           = histos_data_match[mclasdis].Clone(f"norm_{mclasdis}")
            histos_data_match[f"norm_{mclasdis}_no_weight"] = histos_data_match[f"{mclasdis}_no_weight"].Clone(f"norm_{mclasdis}_no_weight")

            histos_data_match[f"norm_{rdf_name}"].Scale(          (1/rdf_name_norm_factor) if(rdf_name_norm_factor != 0) else 1)
            histos_data_match[f"norm_{mclasdis}"].Scale(          (1/mclasdis_norm_factor) if(mclasdis_norm_factor != 0) else 1)
            histos_data_match[f"norm_{mclasdis}_no_weight"].Scale((1/mclasdis_NoWn_factor) if(mclasdis_NoWn_factor != 0) else 1)

            histos_data_match[data_match_name] = histos_data_match[f"norm_{rdf_name}"].Clone(data_match_name)
            histos_data_match[data_match_name].Divide(histos_data_match[f"norm_{mclasdis}"])
            data_match_norm_factor = histos_data_match[data_match_name].Integral()
            histos_data_match[data_match_name].Scale((1/data_match_norm_factor) if(data_match_norm_factor != 0) else 1)
            
            if(args.title):
                histos_data_match[data_match_name].SetTitle(f"#splitline{{Ratio of #frac{{Data}}{{MC-REC}} for {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)}}}{{{args.title}}}")
            else:
                histos_data_match[data_match_name].SetTitle(f"Ratio of #frac{{Data}}{{MC-REC}} for {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)}")
            histos_data_match[data_match_name].SetTitle(f"#splitline{{{histos_data_match[data_match_name].GetTitle()}}}{{Ratio is Normalized to 1}}")

            # -----------------------------
            # 3) Extract edges + row-major weights from the ratio
            # -----------------------------
            H_w = histos_data_match[data_match_name]

            nx = H_w.GetXaxis().GetNbins()
            ny = H_w.GetYaxis().GetNbins()

            edges_x = [H_w.GetXaxis().GetBinLowEdge(i) for i in range(1, nx+1)]
            edges_x.append(H_w.GetXaxis().GetBinUpEdge(nx))

            edges_y = [H_w.GetYaxis().GetBinLowEdge(j) for j in range(1, ny+1)]
            edges_y.append(H_w.GetYaxis().GetBinUpEdge(ny))

            weights = []
            for iy in range(1, ny+1):
                for ix in range(1, nx+1):
                    val = H_w.GetBinContent(ix, iy)
                    # exp = histos_data_match[f"norm_{rdf_name}"].GetBinContent(ix, iy)
                    # if((val < 0.0) or (not math.isfinite(val)) or (exp == 0)):
                    if((val < 0.0) or (not math.isfinite(val))):
                        val = 1.0
                    weights.append(val)

            cpp_edges_x = _cpp_list(edges_x)
            cpp_edges_y = _cpp_list(edges_y)
            cpp_weights = _cpp_list(weights)

            # Pick a stable function name for this pair
            func_name = f"accw_{var_x}_vs_{var_y}"

            # -----------------------------
            # 4) Generate + declare the concrete C++ wrapper
            # -----------------------------
            wrapper_code = f"""
double {func_name}(const double x, const double y){{
    static const std::vector<double> EX = {cpp_edges_x};
    static const std::vector<double> EY = {cpp_edges_y};
    static const std::vector<double> GRID = {cpp_weights};
    return accw_lookup2D(x, y, EX, EY, GRID);
}}
"""
            ROOT.gInterpreter.Declare(wrapper_code)
            generated_wrappers_code.append(wrapper_code)

            # -----------------------------
            # 5) Apply weight to MC (using smeared cols) to draw the next weighted MC histo
            # -----------------------------
            weight_col = f"W_{var_x}_vs_{var_y}"
            # # Preserve the current total effective weight, then apply this pair's weight and renormalize
            # pre_sum = wdf.Sum("ACC_Weight_Product").GetValue()
            wdf = wdf.Define(weight_col, f"{func_name}({var_x}_smeared, {var_y}_smeared)").Redefine("ACC_Weight_Product", f"(ACC_Weight_Product) * ({weight_col})")
            # post_sum = wdf.Sum("ACC_Weight_Product").GetValue()
            # scale = (pre_sum / post_sum) if(post_sum != 0.0) else 1.0
            # wdf = wdf.Redefine("ACC_Weight_Product", f"(ACC_Weight_Product) * ({scale})")

            # -----------------------------
            # 6) Draw panels (ratio / data / MC)
            # -----------------------------
            cd_num = num + 1
            canvas_data_match.cd(cd_num)
            # ROOT.gPad.SetLogz(1)
            histos_data_match[data_match_name].Draw("colz")
            canvas_data_match.cd(cd_num +   len(List_of_Quantities_2D))
            # ROOT.gPad.SetLogz(1)
            histos_data_match[f"norm_{rdf_name}"].Draw("colz")
            canvas_data_match.cd(cd_num + 2*len(List_of_Quantities_2D))
            # ROOT.gPad.SetLogz(1)
            histos_data_match[f"norm_{mclasdis}_no_weight"].Draw("colz")
            canvas_data_match.cd(cd_num + 3*len(List_of_Quantities_2D))
            # ROOT.gPad.SetLogz(1)
            histos_data_match[f"norm_{mclasdis}"].Draw("colz")
            histos_data_match[f"norm_{mclasdis}"].SetTitle(f"#splitline{{{histos_data_match[f'norm_{mclasdis}'].GetTitle()}}}{{{root_color.Bold}{{#splitline{{Before Applying the Weights in this column}}{{Applied the weights from the columns to the left}}}}}}")
            print(f"{color.BOLD}Finished '{data_match_name}' Histograms{color.END}")
            timer.time_elapsed()
            
            
        print(f"\n{color.BOLD}Done Creating the Histograms for getting the new event weights{color.END}\n")
        timer.time_elapsed()
        for num, (x_vars, y_vars) in enumerate(List_of_Quantities_2D):
            var_x, Min_range_x, Max_range_x, Num_of_Bins_x = x_vars
            var_y, Min_range_y, Max_range_y, Num_of_Bins_y = y_vars
            mclasdis  = f"{var_x}_vs_{var_y}_mdf_Final"
            Title     = f"Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"
            if(args.title):
                Title = f"#splitline{{Plot of {variable_Title_name_new(var_x)} vs {variable_Title_name_new(var_y)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var_x)}; {variable_Title_name_new(var_y)}"
            histos_data_match[mclasdis] = wdf.Histo2D((mclasdis, Title.replace("SOURCE", f"#color[{ROOT.kRed}]{{Smeared MC REC (clasdis)}}"),  Num_of_Bins_x, Min_range_x, Max_range_x, Num_of_Bins_y, Min_range_y, Max_range_y), f"{var_x}_smeared", f"{var_y}_smeared", "ACC_Weight_Product")
            histos_data_match[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var_x)} (Smeared)")
            histos_data_match[mclasdis].GetYaxis().SetTitle(f"{variable_Title_name_new(var_y)} (Smeared)")
            mclasdis_norm_factor = histos_data_match[mclasdis].Integral()
            histos_data_match[f"norm_{mclasdis}"] = histos_data_match[mclasdis].Clone(f"norm_{mclasdis}")
            histos_data_match[f"norm_{mclasdis}"].Scale((1/mclasdis_norm_factor) if(mclasdis_norm_factor != 0) else 1)
            canvas_data_match.cd((num + 1) + 4*len(List_of_Quantities_2D))
            # ROOT.gPad.SetLogz(1)
            histos_data_match[f"norm_{mclasdis}"].Draw("colz")
            histos_data_match[f"norm_{mclasdis}"].SetTitle(f"#splitline{{{histos_data_match[f'norm_{mclasdis}'].GetTitle()}}}{{{root_color.Bold}{{After Applying ALL Weights in this image}}}}")
        # -----------------------------
        # 7) Save the canvas (ratio / data / weighted-MC)
        # -----------------------------
        save_name = f"Data_to_MC_Acceptance_Weights{args.File_Save_Format}" if(not args.name) else f"Data_to_MC_Acceptance_Weights_{args.name}{args.File_Save_Format}"
        canvas_data_match.SaveAs(save_name)
        print(f"{color.BOLD}Saved: {color.BBLUE}{save_name}{color.END}")

        # -----------------------------
        # 8) Emit a reusable header with all functions
        # -----------------------------
        header_body = "".join(generated_wrappers_code)
        header_path = args.hpp_output_file
        if(args.name):
            header_path = header_path.replace(".hpp", f"_{args.name}.hpp") if(args.name not in str(header_path)) else header_path

        with open(header_path, "w") as hf:
            hf.write("// This file was auto-generated by your acceptance-weight script.\n")
            hf.write("// It contains concrete lookup functions accw_<x>_vs_<y>(x, y).\n\n")
            hf.write("#pragma once\n\n")
            hf.write("// Embedded helper definitions (self-contained)\n")
            hf.write(One_Time_Cpp_Helpers)
            hf.write("\n\n")
            hf.write(header_body)

        print(f"{color.BOLD}Wrote weight functions to: {color.BBLUE}{header_path}{color.END}")
        print(f"\n{color.BOLD}===== BEGINNING OF GENERATED ACCEPTANCE-WEIGHT CODE ====={color.END}\n")
        print(header_body)
        print(f"\n{color.BOLD}=====    END OF GENERATED ACCEPTANCE-WEIGHT CODE    ====={color.END}\n")
        timer.time_elapsed()
        print(f"\n{color.BOLD}DONE CREATING ACCEPTANCE WEIGHTS HISTOGRAMS/CODE{color.END}\n")

    else:
        print(f"\n{color.Error}Skipping Acceptance Weight Histograms{color.END}")
    
    if(args.kinematic_compare):
        if(args.use_HIGH_MX):
            print(f"\n{color.BOLD}CREATING 1D MM HISTOGRAMS FOR HIGH-Mx NORMALIZATION FACTOR\n{color.END}")
            MM_Binning = ['MM', 2.5, 4.2, 6]
            histos = {}
            var, Min_range, Max_range, Num_of_Bins = MM_Binning
            # rdf_name = f"{var}_rdf"
            # mclasdis = f"{var}_mdf_clasdis"
            # mdfEvGen = f"{var}_mdf_EvGen"
            gclasdis = f"{var}_gdf_clasdis"
            gdfEvGen = f"{var}_gdf_EvGen"
            Title = f"{variable_Title_name_new(var)} from SOURCE; {variable_Title_name_new(var)}"
            if(args.title):
                Title = f"#splitline{{{variable_Title_name_new(var)} from SOURCE}}{{{args.title}}}; {variable_Title_name_new(var)}"
            # histos[rdf_name] =         rdf.Histo1D((rdf_name, Title.replace("SOURCE", f"#color[{ROOT.kBlue   }]{{Experimental Data}}"),         Num_of_Bins, Min_range, Max_range),    var)
            # histos[mclasdis] = mdf_clasdis.Histo1D((mclasdis, Title.replace("SOURCE", f"#color[{ROOT.kRed    }]{{Smeared MC REC (clasdis)}}"),  Num_of_Bins, Min_range, Max_range), f"{var}_smeared")
            # histos[mdfEvGen] =   mdf_EvGen.Histo1D((mdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kMagenta}]{{MC REC (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var, "weight")
            histos[gclasdis] = gdf_clasdis.Histo1D((gclasdis, Title.replace("SOURCE", f"#color[{ROOT.kGreen  }]{{MC GEN (clasdis)}}"),          Num_of_Bins, Min_range, Max_range),    var)
            histos[gdfEvGen] =   gdf_EvGen.Histo1D((gdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kCyan   }]{{MC GEN (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var, "weight")
            # histos[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var)} (Smeared)")
            # histos[rdf_name].SetLineColor(ROOT.kBlue)
            # histos[mclasdis].SetLineColor(ROOT.kRed)
            # histos[mdfEvGen].SetLineColor(ROOT.kMagenta)
            histos[gclasdis].SetLineColor(ROOT.kGreen)
            histos[gdfEvGen].SetLineColor(ROOT.kCyan)
            # rdf_name_norm_factor_HIGH_MX = histos[rdf_name].Integral()
            # mclasdis_norm_factor_HIGH_MX = histos[mclasdis].Integral()
            # mdfEvGen_norm_factor_HIGH_MX = histos[mdfEvGen].Integral()
            gclasdis_norm_factor_HIGH_MX = histos[gclasdis].Integral()
            gdfEvGen_norm_factor_HIGH_MX = histos[gdfEvGen].Integral()
            if(verbose):
                # print(f"rdf_name_norm_factor_HIGH_MX = {rdf_name_norm_factor_HIGH_MX:>20.0f}")
                # print(f"mclasdis_norm_factor_HIGH_MX = {mclasdis_norm_factor_HIGH_MX:>20.0f}")
                # print(f"mdfEvGen_norm_factor_HIGH_MX = {mdfEvGen_norm_factor_HIGH_MX:>20.0f}")
                print(f"gclasdis_norm_factor_HIGH_MX = {gclasdis_norm_factor_HIGH_MX:>20.0f}")
                print(f"gdfEvGen_norm_factor_HIGH_MX = {gdfEvGen_norm_factor_HIGH_MX:>20.0f}")
            # histos[f"norm_{rdf_name}"] = histos[rdf_name].Clone(f"norm_{rdf_name}")
            # histos[f"norm_{mclasdis}"] = histos[mclasdis].Clone(f"norm_{mclasdis}")
            # histos[f"norm_{mdfEvGen}"] = histos[mdfEvGen].Clone(f"norm_{mdfEvGen}")
            histos[f"norm_{gclasdis}"] = histos[gclasdis].Clone(f"norm_{gclasdis}")
            histos[f"norm_{gdfEvGen}"] = histos[gdfEvGen].Clone(f"norm_{gdfEvGen}")
            
            # histos[f"norm_{rdf_name}"].Scale((1/rdf_name_norm_factor_HIGH_MX) if(rdf_name_norm_factor_HIGH_MX != 0) else 1)
            # histos[f"norm_{mclasdis}"].Scale((1/mclasdis_norm_factor_HIGH_MX) if(mclasdis_norm_factor_HIGH_MX != 0) else 1)
            # histos[f"norm_{mdfEvGen}"].Scale((1/mdfEvGen_norm_factor_HIGH_MX) if(mdfEvGen_norm_factor_HIGH_MX != 0) else 1)
            histos[f"norm_{gclasdis}"].Scale((1/gclasdis_norm_factor_HIGH_MX) if(gclasdis_norm_factor_HIGH_MX != 0) else 1)
            histos[f"norm_{gdfEvGen}"].Scale((1/gdfEvGen_norm_factor_HIGH_MX) if(gdfEvGen_norm_factor_HIGH_MX != 0) else 1)
            
            # histos[f"norm_{rdf_name}"].SetTitle(f"Normalized {histos[rdf_name].GetTitle()}")
            # histos[f"norm_{mclasdis}"].SetTitle(f"Normalized {histos[mclasdis].GetTitle()}")
            # histos[f"norm_{mdfEvGen}"].SetTitle(f"Normalized {histos[mdfEvGen].GetTitle()}")
            histos[f"norm_{gclasdis}"].SetTitle(f"Normalized {histos[gclasdis].GetTitle()}")
            histos[f"norm_{gdfEvGen}"].SetTitle(f"Normalized {histos[gdfEvGen].GetTitle()}")
            
            # histos[f"norm_{rdf_name}"].GetYaxis().SetTitle("Normalized")
            # histos[f"norm_{mclasdis}"].GetYaxis().SetTitle("Normalized")
            # histos[f"norm_{mdfEvGen}"].GetYaxis().SetTitle("Normalized")
            histos[f"norm_{gclasdis}"].GetYaxis().SetTitle("Normalized")
            histos[f"norm_{gdfEvGen}"].GetYaxis().SetTitle("Normalized")


            canvas = ROOT.TCanvas("MM_Norm_Factor", "My Canvas", int(912*1.55), int(547*1.55))
            canvas.Divide(3, 2)
            for cd_num, ii in enumerate([gclasdis, gdfEvGen]):
                canvas.cd(cd_num + 1)
                histos[ii].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(histos[ii]))
                histos[ii].Draw("E0 hist same")
                canvas.cd(cd_num + 4)
                histos[f"norm_{ii}"].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(histos[f"norm_{ii}"]))
                histos[f"norm_{ii}"].Draw("E0 hist same")
            # Draw Legend(s)
            canvas.cd(3)
            ROOT.gPad.Clear()
            ROOT.gPad.SetLeftMargin(0.2)
            ROOT.gPad.SetBottomMargin(0.2)
            
            # canvas = ROOT.TCanvas("MM_Norm_Factor", "My Canvas", int(912*1.55), int(547*1.55))
            # canvas.Divide(6, 2)
            # for cd_num, ii in enumerate([rdf_name, mclasdis, mdfEvGen, gclasdis, gdfEvGen]):
            #     canvas.cd(cd_num + 1)
            #     histos[ii].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(histos[ii]))
            #     histos[ii].Draw("E0 hist same")
            #     canvas.cd(cd_num + 7)
            #     histos[f"norm_{ii}"].GetYaxis().SetRangeUser(0, 1.2*find_max_bin(histos[f"norm_{ii}"]))
            #     histos[f"norm_{ii}"].Draw("E0 hist same")
            # # Draw Legend(s)
            # canvas.cd(6)
            # ROOT.gPad.Clear()
            # ROOT.gPad.SetLeftMargin(0.2)
            # ROOT.gPad.SetBottomMargin(0.2)
            
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
        # phi_t_Binning              = ['phi_t',                            0,      360,    24]
        # El_Binning                 = ['el',                               0,        8,   200]
        # El_Th_Binning              = ['elth',                             0,       40,   200]
        # El_Phi_Binning             = ['elPhi',                            0,      360,   200]
        # Pip_Binning                = ['pip',                              0,        6,   200]
        # Pip_Th_Binning             = ['pipth',                            0,       40,   200]
        # Pip_Phi_Binning            = ['pipPhi',                           0,      360,   200]
        # Q2_Binning                 = ['Q2',                               0,       14,   280]
        # y_Binning                  = ['y',                                0,        1,   100]
        # # y_Binning                  = ['y',                              0.9,        1,   100]
        # xB_Binning                 = ['xB',                            0.09,    0.826,    50]
        # z_Binning                  = ['z',                                0,     1.20,   120]
        # # z_Binning                  = ['z',                                0,     0.20,   120]
        # # pT_Binning                 = ['pT',                               0,     2.00,   200]
        # pT_Binning                 = ['pT',                               0,     1.50,   150]
        # MM_Binning                 = ['MM',                               0,      4.2,    60]
        # W_Binning                  = ['W',                              0.9,      5.1,    14]
        # Q2_y_z_pT_Binning          = ['Q2_y_z_pT_4D_Bin',              -0.5,    506.5,   507]
        # z_pT_phi_h_Binning         = ['MultiDim_z_pT_Bin_Y_bin_phi_t', -1.5,    913.5,   915]
        # Q2_y_z_pT_phi_h_5D_Binning = ['MultiDim_Q2_y_z_pT_phi_h',      -0.5,  11815.5, 11816]
        # Hx_Binning                 = ['Hx',                            -400,      400,   800]
        # Hy_Binning                 = ['Hy',                            -400,      400,   800]
        # z_pT_Bin_Y_Binning         = ['z_pT_Bin_Y_bin',                -2.5,     41.5,    44]

        phi_t_Binning              = ['phi_t',                            0,      360,    24]
        El_Binning                 = ['el',                               0,        8,    20]
        El_Th_Binning              = ['elth',                             0,       40,    20]
        El_Phi_Binning             = ['elPhi',                            0,      360,    20]
        Pip_Binning                = ['pip',                              0,        6,    20]
        Pip_Th_Binning             = ['pipth',                            0,       40,    20]
        Pip_Phi_Binning            = ['pipPhi',                           0,      360,    20]
        Q2_Binning                 = ['Q2',                               0,        9,    25]
        y_Binning                  = ['y',                             0.05,     1.05,    22]
        xB_Binning                 = ['xB',                               0,      0.7,    25]
        z_Binning                  = ['z',                                0,     0.95,    25]
        pT_Binning                 = ['pT',                               0,     1.05,    25]
        MM_Binning                 = ['MM',                             0.5,      4.5,    25]
        W_Binning                  = ['W',                             0.99,     4.99,    20]
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
            histos_compare[mdfEvGen] =   mdf_EvGen.Histo1D((mdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kMagenta}]{{MC REC (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var, "weight")
            histos_compare[gclasdis] = gdf_clasdis.Histo1D((gclasdis, Title.replace("SOURCE", f"#color[{ROOT.kGreen  }]{{MC GEN (clasdis)}}"),          Num_of_Bins, Min_range, Max_range),    var)
            histos_compare[gdfEvGen] =   gdf_EvGen.Histo1D((gdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kCyan   }]{{MC GEN (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var, "weight")
            histos_compare[mclasdis].GetXaxis().SetTitle(f"{variable_Title_name_new(var)} (Smeared)")
            
            histos_compare[rdf_name].SetLineColor(ROOT.kBlue)
            histos_compare[mclasdis].SetLineColor(ROOT.kRed)
            histos_compare[mdfEvGen].SetLineColor(ROOT.kMagenta)
            histos_compare[gclasdis].SetLineColor(ROOT.kGreen)
            histos_compare[gdfEvGen].SetLineColor(ROOT.kCyan)

            # rdf_name_norm_factor = rdf_name_norm_factor_HIGH_MX if(args.use_HIGH_MX) else histos_compare[rdf_name].Integral()
            # mclasdis_norm_factor = mclasdis_norm_factor_HIGH_MX if(args.use_HIGH_MX) else histos_compare[mclasdis].Integral()
            # mdfEvGen_norm_factor = mdfEvGen_norm_factor_HIGH_MX if(args.use_HIGH_MX) else histos_compare[mdfEvGen].Integral()
            rdf_name_norm_factor = histos_compare[rdf_name].Integral()
            mclasdis_norm_factor = histos_compare[mclasdis].Integral()
            mdfEvGen_norm_factor = histos_compare[mdfEvGen].Integral()
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
            if(args.use_HIGH_MX):
                gdf_title = f"#splitline{{{gdf_title}}}{{Normalized to High M_{{X}}}}"
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
        
            # # canvas_compare[var].cd(8)
            # histos_compare[f"Diff_in_{rdf_name}"] = histos_compare[f"norm_{rdf_name}"].Clone(f"Diff_in_{rdf_name}")
            # histos_compare[f"Diff_in_{rdf_name}"].Divide(histos_compare[f"norm_{mdfEvGen}"])
            # histos_compare[f"Diff_in_{rdf_name}"].SetTitle("#scale[2]{Ratio of Data to EvGen MC above}")
            # histos_compare[f"Diff_in_{rdf_name}"].GetYaxis().SetTitle("#frac{Data}{EvGen}")
            # histos_compare[f"Diff_in_{rdf_name}"].SetLineColor(ROOT.kViolet + 1)
            histos_compare[f"Diff_in_{rdf_name}"] = histos_compare[f"norm_{rdf_name}"].Clone(f"Diff_in_{rdf_name}")
            histos_compare[f"Diff_in_{rdf_name}"].Add(histos_compare[f"norm_{mdfEvGen}"], -1.0)
            histos_compare[f"Diff_in_{rdf_name}"].Divide(histos_compare[f"norm_{mdfEvGen}"])
            histos_compare[f"Diff_in_{rdf_name}"].Scale(100.0)
            histos_compare[f"Diff_in_{rdf_name}"].SetTitle("#scale[2]{Percent Difference of Data from EvGen MC above}")
            histos_compare[f"Diff_in_{rdf_name}"].GetYaxis().SetTitle("Percent Difference (%)")
            histos_compare[f"Diff_in_{rdf_name}"].SetLineColor(ROOT.kViolet + 1)
            # # canvas_compare[var].cd(9)
            # histos_compare[f"Diff_in_{mclasdis}"] = histos_compare[f"norm_{rdf_name}"].Clone(f"Diff_in_{mclasdis}")
            # histos_compare[f"Diff_in_{mclasdis}"].Divide(histos_compare[f"norm_{mclasdis}"])
            # histos_compare[f"Diff_in_{mclasdis}"].SetTitle("#scale[2]{Ratio of Data to clasdis MC above}")
            # histos_compare[f"Diff_in_{mclasdis}"].GetYaxis().SetTitle("#frac{Data}{clasdis}")
            # histos_compare[f"Diff_in_{mclasdis}"].SetLineColor(ROOT.kBlue + 3)
            histos_compare[f"Diff_in_{mclasdis}"] = histos_compare[f"norm_{rdf_name}"].Clone(f"Diff_in_{mclasdis}")
            histos_compare[f"Diff_in_{mclasdis}"].Add(histos_compare[f"norm_{mclasdis}"], -1.0)
            histos_compare[f"Diff_in_{mclasdis}"].Divide(histos_compare[f"norm_{mclasdis}"])
            histos_compare[f"Diff_in_{mclasdis}"].Scale(100.0)
            histos_compare[f"Diff_in_{mclasdis}"].SetTitle("#scale[2]{Percent Difference of Data from clasdis MC above}")
            histos_compare[f"Diff_in_{mclasdis}"].GetYaxis().SetTitle("Percent Difference (%)")
            histos_compare[f"Diff_in_{mclasdis}"].SetLineColor(ROOT.kBlue + 3)
            max_cd_8_9 = max([find_max_bin(histos_compare[f"Diff_in_{rdf_name}"]), find_max_bin(histos_compare[f"Diff_in_{mclasdis}"])])
            
            canvas_compare[var].cd(8)
            # histos_compare[f"Diff_in_{rdf_name}"].GetYaxis().SetRangeUser(0, 1.2*max_cd_8_9)
            histos_compare[f"Diff_in_{rdf_name}"].Draw("E0 hist same")
            histos_compare[f"line_{mdfEvGen}"].Draw("same")
        
            canvas_compare[var].cd(9)
            # histos_compare[f"Diff_in_{mclasdis}"].GetYaxis().SetRangeUser(0, 1.2*max_cd_8_9)
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
            timer.time_elapsed()
        print(f"\n{color.BOLD}DONE CREATING 1D HISTOGRAMS\n{color.END}")
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
        # List_of_Quantities_1D.append(El_Binning)
        # List_of_Quantities_1D.append(El_Th_Binning)
        # List_of_Quantities_1D.append(El_Phi_Binning)
        # List_of_Quantities_1D.append(Pip_Binning)
        # List_of_Quantities_1D.append(Pip_Th_Binning)
        # List_of_Quantities_1D.append(Pip_Phi_Binning)
        
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
            histos_acceptance[mdfEvGen] =   mdf_EvGen.Histo1D((mdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kMagenta}]{{MC REC (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var, "weight")
            histos_acceptance[gclasdis] = gdf_clasdis.Histo1D((gclasdis, Title.replace("SOURCE", f"#color[{ROOT.kGreen  }]{{MC GEN (clasdis)}}"),          Num_of_Bins, Min_range, Max_range),    var)
            histos_acceptance[gdfEvGen] =   gdf_EvGen.Histo1D((gdfEvGen, Title.replace("SOURCE", f"#color[{ROOT.kCyan   }]{{MC GEN (EvGen)}}"),            Num_of_Bins, Min_range, Max_range),    var, "weight")
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
            timer.time_elapsed()
        print(f"\n{color.BOLD}DONE CREATING 1D (UNBINNED) ACCEPTANCE HISTOGRAMS\n{color.END}")
    else:
        print(f"\n{color.Error}Skipping (Unbinned) Acceptance Comparison Plots{color.END}")
        
    
    if(args.acceptance or args.acceptance_ratio or args.acceptance_diff):
        print(f"\n{color.BOLD}MAKING ACCEPTANCE AS FUNCTION OF phi_h FOR ALL KINEMATIC BINS{color.END}")
        if(args.acceptance_ratio or args.acceptance_diff):
            print(f"Making the {color.BOLD}{'ratios' if(args.acceptance_ratio) else 'Percent Diff'}{color.END} of the acceptances to show discrepancies...\n")
        else:
            print("")
        phi_t_Binning = ['phi_t',  0,   360,    24]
        Q2_Binning    = ['Q2',     0,    14,   280]
        y_Binning     = ['y',      0,     1,   100]
        z_Binning     = ['z',      0,  1.20,   120]
        pT_Binning    = ['pT',     0,  1.50,   150]
        
        rdf_binned         =         rdf.Filter("(Q2_Y_Bin > 0) && (z_pT_Bin_Y_bin > 0)")
        # mdf_clasdis_binned = mdf_clasdis.Filter("(Q2_Y_Bin > 0) && (z_pT_Bin_Y_bin > 0)")
        mdf_clasdis_binned = mdf_clasdis.Filter("(Q2_Y_Bin_smeared > 0) && (z_pT_Bin_Y_bin_smeared > 0)")
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
            if(args.acceptance_ratio):
                Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"] = Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"].Clone(f"ratio Acceptance Bin ({Q2_y_Bin}-All)")
                Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].Divide(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"])
                # Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].SetTitle(str(Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].GetTitle()).replace("from EvGen", "Ratio (#frac{EvGen}{clasdis})"))
                Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].SetTitle(str(str(Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].GetTitle()).replace("from EvGen", "")).replace("Acceptance for", "Acceptance Ratio #frac{EvGen}{clasdis} for "))
                Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].GetYaxis().SetTitle("#frac{EvGen}{clasdis}")
                Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-All)"].SetLineColor(ROOT.kBlack)
                count += 1
            if(args.acceptance_diff):
                Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"] = Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-All)"].Clone(f"diff Acceptance Bin ({Q2_y_Bin}-All)")
                Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].Add(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"], -1.0)
                Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].Divide(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-All)"])
                Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].Scale(100.0)
                Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].SetTitle(str(Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].GetTitle()).replace("from EvGen", "Percent Diff (#frac{EvGen - clasdis}{clasdis})"))
                Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].GetYaxis().SetTitle("Percent Difference (%)")
                Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-All)"].SetLineColor(ROOT.kBlack)
                count += 1
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
                if(args.acceptance_ratio):
                    Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"] = Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Clone(f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})")
                    Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Divide(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"])
                    # Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].SetTitle(str(Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetTitle()).replace("from EvGen", "Ratio (#frac{EvGen}{clasdis})"))
                    Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].SetTitle(str(str(Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetTitle()).replace("from EvGen", "")).replace("Acceptance for", "Acceptance Ratio #frac{EvGen}{clasdis} for "))
                    Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetYaxis().SetTitle("#frac{EvGen}{clasdis}")
                    Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].SetLineColor(ROOT.kBlack)
                    count += 1
                    Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"] = max([find_max_bin(Histogram_List_All[f"ratio Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"]), Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"]])
                elif(args.acceptance_diff):
                    Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"] = Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Clone(f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})")
                    Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Add(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"], -1.0)
                    Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Divide(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"])
                    Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].Scale(100.0)
                    Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].SetTitle(str(Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetTitle()).replace("from EvGen", "Percent Diff (#frac{EvGen - clasdis}{clasdis})"))
                    Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].GetYaxis().SetTitle("Percent Difference (%)")
                    Histogram_List_All[f"diff Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"].SetLineColor(ROOT.kBlack)
                    count += 1
                else:
                    Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"] = max([find_max_bin(Histogram_List_All[f"EvGen Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"]), find_max_bin(Histogram_List_All[f"clasdis Acceptance Bin ({Q2_y_Bin}-{z_pT_Bin})"]), Histogram_List_All[f"Acceptance max for {Q2_y_Bin}"]])
            print(f"{color.BOLD}Ready to Create Acceptance Image for Q2-y Bin = {Q2_y_Bin}{color.END}")
            timer.time_elapsed()
            Acceptance_Canvases[f"Acceptance for Q2_y_Bin = {Q2_y_Bin}"] = Acceptance_Compare_z_pT_Images_Together(Histogram_List_All=Histogram_List_All, Q2_Y_Bin=Q2_y_Bin, Plot_Orientation="z_pT", Saving_Q=True, File_Save_Format=args.File_Save_Format)
            timer.time_elapsed()
        if(verbose):
            print(f"{color.BOLD}Total Histos Made for Binned Acceptance Images = {color.BBLUE}{count}{color.END}")
        print(f"\n{color.BOLD}DONE MAKING BINNED ACCEPTANCE PLOTS\n{color.END}")
        timer.time_elapsed()
    else:
        print(f"\n{color.Error}Skipping Binned Acceptance Comparison Plots{color.END}")

    if(args.make_root):
        print(f"\n{color.BOLD}Making ROOT Output File{color.END}")
        from helper_functions_for_using_RDataFrames_python import *
        sys.stdout.flush()

        # if(not rdf.HasColumn("PID_pip")):
        #     print(f"\t{color.Error}WARNING:         'rdf' is missing 'PID_pip' — artifically defining as 211){color.END}")
        #     rdf = rdf.Define("PID_pip", "211")
        # if(not rdf.HasColumn("PID_el")):
        #     print(f"\t{color.Error}WARNING:         'rdf' is missing 'PID_el'  — artifically defining as 11){color.END}")
        #     rdf = rdf.Define("PID_el", "11")
        if(not rdf.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
            print(f"\t{color.Error}WARNING:         'rdf' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
            rdf = rdf.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
        if(not rdf.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
            print(f"\t{color.Error}WARNING:         'rdf' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
            rdf = rdf.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))
        if(not rdf.HasColumn("Q2_y_z_pT_4D_Bins")):
            print(f"\t{color.Error}WARNING:         'rdf' is missing 'Q2_y_z_pT_4D_Bins'){color.END}")
            rdf = rdf.Define("Q2_y_z_pT_4D_Bins", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type=""))
            
        

        if(not mdf_clasdis.HasColumn("PID_pip")):
            # print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'PID_pip' — artifically defining as 211){color.END}")
            mdf_clasdis = mdf_clasdis.Define("PID_pip", "211")
        if(not mdf_clasdis.HasColumn("PID_el")):
            # print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'PID_el'  — artifically defining as 11){color.END}")
            mdf_clasdis = mdf_clasdis.Define("PID_el", "11")
        if(not mdf_clasdis.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
        if(not mdf_clasdis.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))
        if(not mdf_clasdis.HasColumn("Q2_y_z_pT_4D_Bins")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'Q2_y_z_pT_4D_Bins'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("Q2_y_z_pT_4D_Bins", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type=""))

        if(not mdf_clasdis.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t_gen")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t_gen'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_gen", Multi_Bin_Standard_Def_Function(Variable_Type="gen", Dimension="3D"))
        if(not mdf_clasdis.HasColumn("MultiDim_Q2_y_z_pT_phi_h_gen")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_Q2_y_z_pT_phi_h_gen'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("MultiDim_Q2_y_z_pT_phi_h_gen", Multi_Bin_Standard_Def_Function(Variable_Type="gen", Dimension="5D"))
        if(not mdf_clasdis.HasColumn("Q2_y_z_pT_4D_Bins_gen")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'Q2_y_z_pT_4D_Bins_gen'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("Q2_y_z_pT_4D_Bins_gen", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type="gen"))

        if(not mdf_clasdis.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t_smeared'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared", Multi_Bin_Standard_Def_Function(Variable_Type="smear", Dimension="3D"))
        if(not mdf_clasdis.HasColumn("MultiDim_Q2_y_z_pT_phi_h_smeared")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'MultiDim_Q2_y_z_pT_phi_h_smeared'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("MultiDim_Q2_y_z_pT_phi_h_smeared", Multi_Bin_Standard_Def_Function(Variable_Type="smear", Dimension="5D"))
        if(not mdf_clasdis.HasColumn("Q2_y_z_pT_4D_Bins_smeared")):
            print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing 'Q2_y_z_pT_4D_Bins_smeared'){color.END}")
            mdf_clasdis = mdf_clasdis.Define("Q2_y_z_pT_4D_Bins_smeared", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type="smear"))

        if(not gdf_clasdis.HasColumn("PID_pip")):
            # print(f"\t{color.RED}WARNING: 'gdf_clasdis' is missing 'PID_pip' — artifically defining as 211){color.END}")
            gdf_clasdis = gdf_clasdis.Define("PID_pip", "211")
        if(not gdf_clasdis.HasColumn("PID_el")):
            # print(f"\t{color.RED}WARNING: 'gdf_clasdis' is missing 'PID_el'  — artifically defining as 11){color.END}")
            gdf_clasdis = gdf_clasdis.Define("PID_el", "11")
        if(not gdf_clasdis.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
            print(f"\t{color.Error}WARNING: 'gdf_clasdis' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
            gdf_clasdis = gdf_clasdis.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
        if(not gdf_clasdis.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
            print(f"\t{color.Error}WARNING: 'gdf_clasdis' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
            gdf_clasdis = gdf_clasdis.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))
        if(not gdf_clasdis.HasColumn("Q2_y_z_pT_4D_Bins")):
            print(f"\t{color.Error}WARNING: 'gdf_clasdis' is missing 'Q2_y_z_pT_4D_Bins'){color.END}")
            gdf_clasdis = gdf_clasdis.Define("Q2_y_z_pT_4D_Bins", Q2_y_z_pT_4D_Bin_Def_Function_New(Variable_Type=""))

        if(not args.Do_not_use_EvGen):
	        if(not mdf_EvGen.HasColumn("PID_pip")):
	            print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'PID_pip' — artifically defining as 211){color.END}")
	            mdf_EvGen = mdf_EvGen.Define("PID_pip", "211")
	        if(not mdf_EvGen.HasColumn("PID_el")):
	            print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'PID_el'  — artifically defining as 11){color.END}")
	            mdf_EvGen = mdf_EvGen.Define("PID_el", "11")
	        if(not mdf_EvGen.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
	            # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
	            mdf_EvGen = mdf_EvGen.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
	        if(not mdf_EvGen.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
	            # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
	            mdf_EvGen = mdf_EvGen.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))

	        if(not mdf_EvGen.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t_gen")):
	            # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t_gen'){color.END}")
	            mdf_EvGen = mdf_EvGen.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_gen", Multi_Bin_Standard_Def_Function(Variable_Type="gen", Dimension="3D"))
	        if(not mdf_EvGen.HasColumn("MultiDim_Q2_y_z_pT_phi_h_gen")):
	            # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_Q2_y_z_pT_phi_h_gen'){color.END}")
	            mdf_EvGen = mdf_EvGen.Define("MultiDim_Q2_y_z_pT_phi_h_gen", Multi_Bin_Standard_Def_Function(Variable_Type="gen", Dimension="5D"))

	        if(not mdf_EvGen.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared")):
	            # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t_smeared'){color.END}")
	            mdf_EvGen = mdf_EvGen.Define("MultiDim_z_pT_Bin_Y_bin_phi_t_smeared", Multi_Bin_Standard_Def_Function(Variable_Type="smear", Dimension="3D"))
	        if(not mdf_EvGen.HasColumn("MultiDim_Q2_y_z_pT_phi_h_smeared")):
	            # print(f"\t{color.Error}WARNING:   'mdf_EvGen' is missing 'MultiDim_Q2_y_z_pT_phi_h_smeared'){color.END}")
	            mdf_EvGen = mdf_EvGen.Define("MultiDim_Q2_y_z_pT_phi_h_smeared", Multi_Bin_Standard_Def_Function(Variable_Type="smear", Dimension="5D"))

            
	        if(not gdf_EvGen.HasColumn("PID_pip")):
	            # print(f"\t{color.RED}WARNING:   'gdf_EvGen' is missing 'PID_pip' — artifically defining as 211){color.END}")
	            gdf_EvGen = gdf_EvGen.Define("PID_pip", "211")
	        if(not gdf_EvGen.HasColumn("PID_el")):
	            # print(f"\t{color.RED}WARNING:   'gdf_EvGen' is missing 'PID_el'  — artifically defining as 11){color.END}")
	            gdf_EvGen = gdf_EvGen.Define("PID_el", "11")
	        if(not gdf_EvGen.HasColumn("MultiDim_z_pT_Bin_Y_bin_phi_t")):
	            # print(f"\t{color.Error}WARNING:   'gdf_EvGen' is missing 'MultiDim_z_pT_Bin_Y_bin_phi_t'){color.END}")
	            gdf_EvGen = gdf_EvGen.Define("MultiDim_z_pT_Bin_Y_bin_phi_t", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"))
	        if(not gdf_EvGen.HasColumn("MultiDim_Q2_y_z_pT_phi_h")):
	            # print(f"\t{color.Error}WARNING:   'gdf_EvGen' is missing 'MultiDim_Q2_y_z_pT_phi_h'){color.END}")
	            gdf_EvGen = gdf_EvGen.Define("MultiDim_Q2_y_z_pT_phi_h", Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="5D"))

        if(args.valerii_bins):
            script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
            sys.path.append(script_dir)
            from Valerii_Kinematic_Binning_Code import *
            sys.path.remove(script_dir)
            del script_dir
            ROOT.gInterpreter.Declare(Run_this_str_with_gInterpreter_for_Valeriis_Bins)
            if(not rdf.HasColumn("Q2_xB_z_pT_4D_Bin_Valerii")):
                print(f"\t{color.Error}WARNING:         'rdf' is missing Valerii's Kinematic bins{color.END}")
                rdf         = add_valerii_bins(rdf_in=rdf,         var_type="")
            if(not mdf_clasdis.HasColumn("Q2_xB_z_pT_4D_Bin_Valerii")):
                print(f"\t{color.Error}WARNING: 'mdf_clasdis' is missing Valerii's Kinematic bins{color.END}")
                mdf_clasdis = add_valerii_bins(rdf_in=mdf_clasdis, var_type="")
                mdf_clasdis = add_valerii_bins(rdf_in=mdf_clasdis, var_type="_smeared")
                mdf_clasdis = add_valerii_bins(rdf_in=mdf_clasdis, var_type="_gen")
            if(not gdf_clasdis.HasColumn("Q2_xB_z_pT_4D_Bin_Valerii")):
                print(f"\t{color.Error}WARNING: 'gdf_clasdis' is missing Valerii's Kinematic bins{color.END}")
                gdf_clasdis = add_valerii_bins(rdf_in=gdf_clasdis, var_type="")
            

        if(args.json_weights):
            # With the Modulation weights option, apply the modulations to both gdf and mdf before adding the acceptance weights to mdf
            print(f"\n{color.BBLUE}Using phi_h Modulation Weights from the JSON file.{color.END}\n")
            with open(JSON_WEIGHT_FILE) as f:
                Fit_Pars = json.load(f)
                # Build the C++ initialization string
                cpp_map_str = "{"
                for key, val in Fit_Pars.items():
                    cpp_map_str += f'{{"{key}", {val}}},'
                cpp_map_str += "}"
                
                ROOT.gInterpreter.Declare(f"""
                #include <map>
                #include <string>
                #include <cmath>
                
                std::map<std::string, double> Fit_Pars = {cpp_map_str};
                
                double ComputeWeight(int Q2_y_Bin, int z_pT_Bin, double phi_h) {{
                    // build the keys dynamically
                    // std::string keyA = "A_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                    std::string keyB = "B_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                    std::string keyC = "C_" + std::to_string(Q2_y_Bin) + "_" + std::to_string(z_pT_Bin);
                
                    // safely retrieve parameters (default = 0)
                    // double Par_A = Fit_Pars.count(keyA) ? Fit_Pars[keyA] : 0.0;
                    double Par_B = Fit_Pars.count(keyB) ? Fit_Pars[keyB] : 0.0;
                    double Par_C = Fit_Pars.count(keyC) ? Fit_Pars[keyC] : 0.0;
                
                    // calculate weight
                    double phi_rad = phi_h * TMath::DegToRad();
                    double weight  = (1.0 + Par_B * std::cos(phi_rad) + Par_C * std::cos(2.0 * phi_rad));
                
                    return weight;
                }}
                """)
            gdf_clasdis = gdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_Y_Bin,     z_pT_Bin_Y_bin,     phi_t)")
            mdf_clasdis = mdf_clasdis.Define("Event_Weight", "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
            mdf_clasdis = mdf_clasdis.Define("W_pre",        "ComputeWeight(Q2_Y_Bin_gen, z_pT_Bin_Y_bin_gen, phi_t_gen)")
            if(not args.do_not_use_hpp):
                # pre_sum         = mdf_clasdis.Sum("W_pre").GetValue()
                if(args.angles_only_hpp):
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared))")
                else:
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
                # post_sum        = mdf_clasdis.Sum("Event_Weight_raw").GetValue()
                # scale           = (pre_sum / post_sum) if(post_sum != 0.0) else 1.0
                # mdf_clasdis     = mdf_clasdis.Define("Event_Weight", f"Event_Weight_raw * ({scale})")
            else:
                mdf_clasdis     = mdf_clasdis.Define("W_acc",                      "1.0")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
        else:
            gdf_clasdis = gdf_clasdis.Define("Event_Weight", "1.0")
            mdf_clasdis = mdf_clasdis.Define("Event_Weight", "1.0")
            mdf_clasdis = mdf_clasdis.Define("W_pre",        "1.0")
            if(not args.do_not_use_hpp):
                # pre_sum         = mdf_clasdis.Sum("W_pre").GetValue()
                if(args.angles_only_hpp):
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared))")
                else:
                    mdf_clasdis = mdf_clasdis.Define("W_acc", "(accw_elPhi_vs_pipPhi(elPhi_smeared, pipPhi_smeared)) * (accw_elth_vs_pipth(elth_smeared, pipth_smeared)) * (accw_el_vs_pip(el_smeared, pip_smeared))")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
                # post_sum        = mdf_clasdis.Sum("Event_Weight_raw").GetValue()
                # scale           = (pre_sum / post_sum) if(post_sum != 0.0) else 1.0
                # mdf_clasdis     = mdf_clasdis.Define("Event_Weight", f"Event_Weight_raw * ({scale})")
            else:
                mdf_clasdis     = mdf_clasdis.Define("W_acc",                      "1.0")
                mdf_clasdis     = mdf_clasdis.Define("Event_Weight_raw", "W_pre * W_acc")
        if(not args.do_not_use_hpp):
            mdf_clasdis = weight_norm_by_bins(df_in=mdf_clasdis, Histo_Data_In="mdf", verbose=args.verbose, Do_not_use_Smeared=False, Valerii_binning=args.valerii_bins) # See helper_functions_for_using_RDataFrames_python.py
        print(f"{color.BBLUE}Saving to: {color.BGREEN}{args.root}{color.END}")
        output_file = ROOT.TFile(args.root, "UPDATE")
        sys.stdout.flush()

        Res_Binning_2D_z_pT_In = ["z_pT_Bin_Y_bin_smeared", -0.5, 37.5, 38]
        z_pT_phi_h_Binning     = ['MultiDim_z_pT_Bin_Y_bin_phi_t', -1.5, 913.5, 915]
        if(args.valerii_bins):
            Res_Binning_2D_z_pT_In = ["z_pT_Bin_Valerii_smeared",  -0.5,  60.5, 61]
            z_pT_phi_h_Binning     = ['z_pT_phi_t_3D_Bin_Valerii', -1.5, 960.5, 962]
        Q2_y_or_xB_bin_range = range(-1, 18) if(not args.valerii_bins) else range(-1, 17)
        Bin_str = "Q2-y Bin" if(not args.valerii_bins) else "Valerii's Q2-xB Bin"
        for Q2_y_Bins in Q2_y_or_xB_bin_range:
            if(Q2_y_Bins == 0):
                continue
            print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}rdf{color.END_B} ({Bin_str} {Q2_y_Bins if(Q2_y_Bins > 0) else 'All'}){color.END}")
            make_rm_single(sdf=rdf,           Histo_Group="Response_Matrix_Normal",     Histo_Data="rdf", Histo_Cut="cut_Complete_SIDIS" if(not args.cut) else "cut_Complete_SIDIS_extra", Histo_Smear="",      Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=False,             Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            timer.time_elapsed()
            sys.stdout.flush()
            print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}mdf_clasdis{color.END_B} ({Bin_str} {Q2_y_Bins if(Q2_y_Bins > 0) else 'All'}){color.END}")
            make_rm_single(sdf=mdf_clasdis,   Histo_Group="Response_Matrix_Normal",     Histo_Data="mdf", Histo_Cut="cut_Complete_SIDIS" if(not args.cut) else "cut_Complete_SIDIS_extra", Histo_Smear="smear", Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=True,              Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            make_rm_single(sdf=mdf_clasdis,   Histo_Group="Background_Response_Matrix", Histo_Data="mdf", Histo_Cut="cut_Complete_SIDIS" if(not args.cut) else "cut_Complete_SIDIS_extra", Histo_Smear="smear", Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=True,              Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            timer.time_elapsed()
            sys.stdout.flush()
            print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}gdf_clasdis{color.END_B} ({Bin_str} {Q2_y_Bins if(Q2_y_Bins > 0) else 'All'}){color.END}")
            make_rm_single(sdf=gdf_clasdis,   Histo_Group="Response_Matrix_Normal",     Histo_Data="gdf", Histo_Cut="no_cut",                                                              Histo_Smear="",      Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=args.json_weights, Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            timer.time_elapsed()
            sys.stdout.flush()
            # if(not args.Do_not_use_EvGen):
            #     print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}mdf_EvGen{color.END_B} (Q2-y Bin {Q2_y_Bins}){color.END}")
            #     make_rm_single(sdf=mdf_EvGen, Histo_Group="Response_Matrix_Normal", Histo_Data="mdf", Histo_Cut="cut_Complete_SIDIS" if(not args.cut) else "cut_Complete_SIDIS_extra", Histo_Smear="",      Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=True,              Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            #     timer.time_elapsed()
            #     print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}gdf_EvGen{color.END_B} (Q2-y Bin {Q2_y_Bins}){color.END}")
            #     make_rm_single(sdf=gdf_EvGen, Histo_Group="Response_Matrix_Normal", Histo_Data="gdf", Histo_Cut="no_cut",                                                              Histo_Smear="",      Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=Q2_y_Bins, Use_Weight=True,              Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            #     timer.time_elapsed()
        if(not args.valerii_bins):
            print(f"{color.BBLUE}Done Saving the 3D phi_h Plots{color.END}\n\n{color.BOLD}Now Saving the other kinematic variable's response matricies{color.END}\n")
        Q2_Unfolding_Binning  = ['Q2',                   0,    14, 280]
        xB_Unfolding_Binning  = ['xB',                0.09, 0.826,  50]
        y_Unfolding_Binning   = ['y',                    0,   1.0, 100]
        z_Unfolding_Binning   = ['z',                    0,   1.2, 120]
        pT_Unfolding_Binning  = ['pT',                   0,   2.0, 200]
        El_Binning            = ['el',                 2.5,   8.0,  44]
        El_Th_Binning         = ['elth',               7.5,  35.5,  56]
        El_Phi_Binning        = ['elPhi',                0,   360, 144]
        Pip_Binning           = ['pip',                1.0,     5,  32]
        Pip_Th_Binning        = ['pipth',              4.5,  35.5,  62]
        Pip_Phi_Binning       = ['pipPhi',               0,   360, 144]
        Multi4D_Binning       = ['Q2_y_z_pT_4D_Bins', -0.5, 546.5, 547]

        # for Unfolding_Binning in [Q2_Unfolding_Binning, xB_Unfolding_Binning, y_Unfolding_Binning, z_Unfolding_Binning, pT_Unfolding_Binning]:
        for Unfolding_Binning in [Q2_Unfolding_Binning, xB_Unfolding_Binning, y_Unfolding_Binning, z_Unfolding_Binning, pT_Unfolding_Binning, El_Binning, El_Th_Binning, El_Phi_Binning, Pip_Binning, Pip_Th_Binning, Pip_Phi_Binning, Multi4D_Binning]:
        # for Unfolding_Binning in [Multi4D_Binning]:
            if(args.valerii_bins):
                break
            print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}rdf{color.END_B} (Variable: {Unfolding_Binning[0]}){color.END}")
            make_rm_single(sdf=rdf,           Histo_Group="Response_Matrix_Normal",     Histo_Data="rdf", Histo_Cut="cut_Complete_SIDIS" if(not args.cut) else "cut_Complete_SIDIS_extra", Histo_Smear="",      Binning="Y_bin", Var_Input=Unfolding_Binning, Q2_y_bin_num=-1, Use_Weight=False,                                            Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            timer.time_elapsed()
            sys.stdout.flush()
            print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}mdf_clasdis{color.END_B} (Variable: {Unfolding_Binning[0]}){color.END}")
            make_rm_single(sdf=mdf_clasdis,   Histo_Group="Response_Matrix_Normal",     Histo_Data="mdf", Histo_Cut="cut_Complete_SIDIS" if(not args.cut) else "cut_Complete_SIDIS_extra", Histo_Smear="smear", Binning="Y_bin", Var_Input=Unfolding_Binning, Q2_y_bin_num=-1, Use_Weight=(args.json_weights or (not args.do_not_use_hpp)), Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            make_rm_single(sdf=mdf_clasdis,   Histo_Group="Background_Response_Matrix", Histo_Data="mdf", Histo_Cut="cut_Complete_SIDIS" if(not args.cut) else "cut_Complete_SIDIS_extra", Histo_Smear="smear", Binning="Y_bin", Var_Input=Unfolding_Binning, Q2_y_bin_num=-1, Use_Weight=(args.json_weights or (not args.do_not_use_hpp)), Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            timer.time_elapsed()
            sys.stdout.flush()
            print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}gdf_clasdis{color.END_B} (Variable: {Unfolding_Binning[0]}){color.END}")
            make_rm_single(sdf=gdf_clasdis,   Histo_Group="Response_Matrix_Normal",     Histo_Data="gdf", Histo_Cut="no_cut",                                                              Histo_Smear="",      Binning="Y_bin", Var_Input=Unfolding_Binning, Q2_y_bin_num=-1, Use_Weight=args.json_weights,                                Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            timer.time_elapsed()
            sys.stdout.flush()
            # if(not args.Do_not_use_EvGen):
            #     print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}mdf_EvGen{color.END_B} (Variable: {Unfolding_Binning[0]}){color.END}")
            #     make_rm_single(sdf=mdf_EvGen, Histo_Group="Response_Matrix_Normal", Histo_Data="mdf", Histo_Cut="cut_Complete_SIDIS" if(not args.cut) else "cut_Complete_SIDIS_extra", Histo_Smear="",      Binning="Y_bin", Var_Input=Unfolding_Binning, Q2_y_bin_num=-1, Use_Weight=True,                                                 Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            #     timer.time_elapsed()
            #     print(f"{color.BBLUE}Saving Histograms for {color.BGREEN}gdf_EvGen{color.END_B} (Variable: {Unfolding_Binning[0]}){color.END}")
            #     make_rm_single(sdf=gdf_EvGen, Histo_Group="Response_Matrix_Normal", Histo_Data="gdf", Histo_Cut="no_cut",                                                              Histo_Smear="",      Binning="Y_bin", Var_Input=Unfolding_Binning, Q2_y_bin_num=-1, Use_Weight=True,                                                 Histograms_All={}, file_location=output_file, output_type=output_file, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=args.title)
            #     timer.time_elapsed()    
        
        print(f"{color.BBLUE}Done Saving...{color.END}\n")
        output_file.Close()
    else:
        print(f"\n{color.Error}Skipping ROOT Output File{color.END}")
        
    start_time = timer.start_find(return_Q=True)
    start_time = start_time.replace("Ran", "Started running")
    end_time, total_time, rate_line = timer.stop(return_Q=True)

    email_body = f"""
The 'using_RDataFrames_python.py' script has finished running.
{start_time}

{args.email_message}

Ran with the following arguments:
--kinematic-compare             --> {args.kinematic_compare}
--acceptance-all                --> {args.acceptance_all}
--acceptance                    --> {args.acceptance}
--acceptance-ratio              --> {args.acceptance_ratio}
--acceptance-diff               --> {args.acceptance_diff}
--verbose                       --> {args.verbose}
--cut                           --> {args.cut}
--File_Save_Format              --> {args.File_Save_Format}
--name                          --> {args.name}
--title                         --> {args.title}
--num-rdf-files                 --> {args.num_rdf_files}
--num-MC-files                  --> {args.num_MC_files}
--event_limit                   --> {args.event_limit}
--Do_not_use_EvGen              --> {args.Do_not_use_EvGen}
--use_HIGH_MX                   --> {args.use_HIGH_MX}
--min-accept-cut                --> {args.min_accept_cut}
--make_root                     --> {args.make_root}
--valerii_bins                  --> {args.valerii_bins}
--do_not_use_hpp                --> {args.do_not_use_hpp}
--angles_only_hpp               --> {args.angles_only_hpp}
--make_2D_weight                --> {args.make_2D_weight}
--make_2D_weight_check          --> {args.make_2D_weight_check}
--make_2D_weight_binned_check   --> {args.make_2D_weight_binned_check}
--json_weights                  --> {args.json_weights}
--json_file                     --> {args.json_file}
--hpp_input_file                --> {args.hpp_input_file}
--hpp_output_file               --> {args.hpp_output_file}
--root                          --> {args.root}
--fast                          --> {args.fast}

{end_time}
{total_time}
{rate_line}
    """
    
    if(args.email):
        send_email(subject="Finished Running the 'using_RDataFrames_python.py' Code", body=email_body, recipient="richard.capobianco@uconn.edu")
    print(email_body)
    
    print(f"""{color.BGREEN}{color_bg.YELLOW}
    \t                                   \t   
    \tThis code has now finished running.\t   
    \t                                   \t   {color.END}
    
    """)
    