# This Code was last updated on 2-13-2023
# # Note-to-self: Also always update this note at end of script


# Most recent update notes:

# # All Updates have been moved to the github page/README.md file

    
# # This Code has been coverted such that 3D histograms are made instead of filtering Q2-xB/z-pT bins







# NOTE TO SELF: "Do not need 1D MC REC histograms (can make from the Response Matrix)"






##=================================================================================================================================================================##
##=================================================================================================================================================================##
##=================================================================================================================================================================##




from sys import argv
# Let there be 4 arguements in argv when running this code
# arguement 1: Name of this code (makeROOT_epip_SIDIS_histos.py)
# arguement 2: data-type
    # Options: 
    # 1) rdf --> Real Data
    # 2) mdf --> MC REC Data (Event matching is available)
    # 3) gdf --> MC GEN Data
    # 4) pdf --> Only Matched MC Events (REC events must be matched to their GEN counterparts if this option is selected)
# arguement 3: output type
    # Options: 
    # 1) histo --> root file contains the histograms made by this code
    # 2) data --> root file contains all information from the RDataFrame 
    # 3) tree --> root file contains all information from the RDataFrame (same as option 2)
    # 4) test --> sets arguement 4 to 'time' (does not save info - will test the DataFrame option instead of the histogram option)
    # 5) time --> sets arguement 4 to 'time' (does not save info - will test the histogram option - same as not giving a 4th arguement)
# arguement 4: file number (full file location)

# NOTE: The 3rd arguement is not necessary if the option for "histo" is desired (i.e., code is backwards compatible and works with only 3 arguements if desired)

# EXAMPLE: python makeROOT_epip_SIDIS_histos.py pdf All

# To see how many histograms will be made without processing any files, let the last arguement given be 'time'
# i.e., run the command:
# # python makeROOT_epip_SIDIS_histos.py df time
# # # df above can be any of the data-type options given above

try:
    code_name, datatype, output_type, file_location = argv
except:
    try:
        code_name, datatype, output_type = argv
    except:
        print("Error in arguments.")
        
    
datatype, output_type = str(datatype), str(output_type)


output_all_histo_names_Q = "yes"
output_all_histo_names_Q = "no"


if(output_type == "test"):
    output_all_histo_names_Q = "yes"
    print("Will be printing the histogram's IDs...")
    file_location = "time"
    output_type = "time"
elif(output_type != "histo" and output_type != "data" and output_type != "tree"):
    file_location = output_type
    if(output_type != "test" and output_type != "time"):
        output_type = "histo"


print("".join(["Output type will be: ", output_type]))

import ROOT, numpy
import array
from datetime import datetime
import copy
import traceback


class color:
    PURPLE    = '\033[95m'
    CYAN      = '\033[96m'
    DARKCYAN  = '\033[36m'
    BLUE      = '\033[94m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    DELTA     = '\u0394' # symbol
    END       = '\033[0m'



if(str(file_location) == 'all'):
    print("\nRunning all files together...\n")
if(str(file_location) == 'time'):
    print("\nRunning Count. Not saving results...\n")
    

if(datatype in ['rdf', 'mdf', 'gdf', 'pdf']):
    
    file_num = str(file_location)

    if(datatype == "rdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00", "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00", "")).replace(".hipo.root", "")

    if(datatype == "mdf" or datatype == "pdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        
    if(datatype == "gdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        file_num = str(file_num.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")

    
    
    ########################################################################################################################################################################
    ##==================================================================##============================##==================================================================##
    ##===============##===============##===============##===============##     Loading Data Files     ##===============##===============##===============##===============##
    ##==================================================================##============================##==================================================================##
    ########################################################################################################################################################################
    
    
    if(datatype == 'rdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            # rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*")
            rdf = ROOT.RDataFrame("h22", "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*")
            files_used_for_data_frame = "Data_sidis_epip_richcap.inb.qa.skim4_00*"
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            files_used_for_data_frame = "".join(["Data_sidis_epip_richcap.inb.qa.skim4_00", str(file_num), "*"])
            
    if(datatype == 'mdf' or datatype == 'pdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            # rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*")
            rdf = ROOT.RDataFrame("h22", "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*")
            files_used_for_data_frame = "MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*"
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            files_used_for_data_frame = "".join(["MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_", str(file_num), "*"])
            
    if(datatype == 'gdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            # rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*")
            rdf = ROOT.RDataFrame("h22", "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*")
            files_used_for_data_frame = "MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*"
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            files_used_for_data_frame = "".join(["MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_", str(file_num), "*"])
            
            
            
    
    print("".join(["\nLoading File(s): ", str(files_used_for_data_frame)]))
    
    
    
    ##========================================================================##
    ##====================##     Timing Information     ##====================##
    ##========================================================================##
    
    # Getting Current Date
    datetime_object_full = datetime.now()

    startMin_full, startHr_full, startDay_full = datetime_object_full.minute, datetime_object_full.hour, datetime_object_full.day

    if(datetime_object_full.minute < 10):
        timeMin_full = ''.join(['0', str(datetime_object_full.minute)])
    else:
        timeMin_full = str(datetime_object_full.minute)
    
    # Printing Current Time
    if(datetime_object_full.hour > 12 and datetime_object_full.hour < 24):
        print("".join(["The time that this code started is ", str((datetime_object_full.hour) - 12), ":", timeMin_full, " p.m."]))
    if(datetime_object_full.hour < 12 and datetime_object_full.hour > 0):
        print("".join(["The time that this code started is ", str(datetime_object_full.hour), ":", timeMin_full, " a.m."]))
    if(datetime_object_full.hour == 12):
        print("".join(["The time that this code started is ", str(datetime_object_full.hour), ":", timeMin_full, " p.m."]))
    if(datetime_object_full.hour == 0 or datetime_object_full.hour == 24):
        print("".join(["The time that this code started is 12:", timeMin_full, " a.m."]))
    
    
    ##========================================================================##
    ##====================##     Timing Information     ##====================##
    ##========================================================================##

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ###########################################################
    #################     Final ROOT File     #################
    
    
    ROOT_File_Output_Name = "Data_REC"
    
    # # # See README.md file for notes on versions older than "Unfolding_Tests_V9_"
         
    Extra_Name = "Unfolding_Tests_V9_"
    # New (Modified) Smearing Functions (Particle-dependant)
        # Modified the momentum smearing (As a function of theta/momentum - not both - choose to smear based on which variable provided the easiest fit to get the smearing factor)
        # New Theta smearing as a function of momentum
        
        
    Extra_Name = "Unfolding_Tests_V10_"
    # New (Modified) Smearing Functions (Particle-dependant)
    # Reduced number of plots made (for faster runtime)
    
    Extra_Name = "Unfolding_Tests_V11_"
    # New (Modified) Smearing Functions (Particle-dependant)
    # Increased number of plots made (relative to last version)
    
    
    Extra_Name = "Unfolding_Tests_V12_"
    # Extended the 2D plots and added more to show the phase space of the data
    # Modified the Pi+ Theta smearing function (as function of momentum)
    
    
    Extra_Name = "Unfolding_Tests_V13_"
    # Running fewer 1D histograms (just phi_t)
    # Added new multidimensional response matrix option which combines multiple variables into a new linearized bin definition
    # Modified the Pi+ Theta smearing function (as function of momentum) and the Electron Momentum smearing function (as a function of theta)
    
    
    Extra_Name = "Unfolding_Tests_V14_"
    # Modified the Pi+ Theta smearing function (as function of momentum) 
        # Testing to see if it is better to smear only one variable at a time (other variables could be improved at this moment, but only changing one aspect of the smearing function in this iteration)
    # Attempting to fix the issue with the multidimension variable creation function
        # Flipped the order of the Res_Var_Add variable list
    # Removed the Combined z-pT-phi_h variable from test (switched with the Q2-xB bin variable as an already defined multidimensional variable that can be unfolded as is)
        # The removed option has to many bins for efficient testing at this stage
    # Changed the phase space histograms (in 'Mom_Cor_Code') to include the particle momentum instead of the sector information
        # May be redundant with other histograms (in 'Normal_2D') which should be removed in the future (must make the other scripts compatible with these histograms before removing the 'Normal_2D' options)
    # Modified Dimension_Name_Function() to remove all ";"s from the outputs
    # Removed notification of "Skipping Normal 1D Histograms..." (now just assumed)
    
    
    Extra_Name = "Analysis_Note_Update_"
    # Added response matrices for the variables already shown in the analysis note (for update)
    # Removed smearing histograms, exclusive cuts, and combined variables (not needed here)
    
    
    Extra_Name = "Analysis_Note_Update_V2_"
    # Extended the z-pT bin axis for the response matrices (caused errors in the plots without kinematic binning)
    # Switched the kinematic variables (other than phi_h) to use the same binning scheme as was used at the last DNP meeting (just for the response matrix/1D plots)

    
    Extra_Name = "Analysis_Note_Update_V3_"
    # Resetted the z-pT bin axis for the response matrices (was not necessary before)
    # Fixed the issue with replicating old plots (issue was caused by a cut that prevented bin migration between the kinematic Q2-xB-z-pT bins which is only useful in the phi_t plots)
    # Using FX's smearing function
    
    
    Extra_Name = "Analysis_Note_Update_V4_"
    # Using my smearing function and momentum corrections
    
    
    if(datatype == 'rdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_Data_REC_", str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'mdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_Matched_", str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'gdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_GEN_", str(Extra_Name), str(file_num), ".root"])
    if(datatype == 'pdf'):
        ROOT_File_Output_Name = "".join(["SIDIS_epip_MC_Only_Matched_", str(Extra_Name), str(file_num), ".root"])
        
    if(output_type == "data" or output_type == "test"):
        ROOT_File_Output_Name = "".join(["DataFrame_", ROOT_File_Output_Name])
    
    print("".join(["\nFile being made is: \033[1m", ROOT_File_Output_Name, "\033[0m"]))
    
    
    
    #################     Final ROOT File     #################
    ###########################################################
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ################################################################     Done Loading Data Files     ################################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ############################################################    Particle Momentum Correction Code    ############################################################

    
    
    Mom_Correction_Q = "yes"
    # Mom_Correction_Q = "no"

    if(datatype != 'rdf'):
        Mom_Correction_Q = "no"
        
    Correction_Code_Full_In = """

    auto dppC = [&](float Px, float Py, float Pz, int sec, int ivec, int corON){

        if(corON == 0){ // corON == 0 --> DOES NOT apply the momentum corrections (i.e., turns the corrections 'off')
            double dp = 0;
            return dp;
        }

        else{ // corON != 0 --> Applies the momentum corrections (i.e., turns the corrections 'on')

            // ivec = 0 --> Electron Corrections
            // ivec = 1 --> π+ Corrections
            // ivec = 2 --> π- Corrections
            // ivec = 3 --> Proton Corrections

            // Momentum Magnitude
            double pp = sqrt(Px*Px + Py*Py + Pz*Pz);

            // Initializing the correction factor
            double dp = 0;

            // Defining Phi Angle
            double Phi = (180/3.1415926)*atan2(Py, Px);

            // (Initial) Shift of the Phi Angle (done to realign sectors whose data is separated when plotted from ±180˚)
            if(((sec == 4 || sec == 3) && Phi < 0) || (sec > 4 && Phi < 90)){
                Phi += 360;
            }

            // Getting Local Phi Angle
            double PhiLocal = Phi - (sec - 1)*60;

            // Applying Shift Functions to Phi Angles (local shifted phi = phi)
            double phi = PhiLocal;

            // For Electron Shift
            if(ivec == 0){
                phi = PhiLocal - 30/pp;
            }

            // For π+ Pion/Proton Shift
            if(ivec == 1 || ivec == 3){
                phi = PhiLocal + (32/(pp-0.05));
            }

            // For π- Pion Shift
            if(ivec == 2){
                phi = PhiLocal - (32/(pp-0.05));
            }

        
        
            //////////////////////////////////////////////////////////////////////////////////
            //==============================================================================//
            //==========//==========//     Electron Corrections     //==========//==========//
            //==============================================================================//
            //////////////////////////////////////////////////////////////////////////////////
            
            if(ivec == 0){
                if(sec == 1){
                    dp = ((-4.3303e-06)*phi*phi + (1.1006e-04)*phi + (-5.7235e-04))*pp*pp + ((3.2555e-05)*phi*phi + (-0.0014559)*phi + (0.0014878))*pp + ((-1.9577e-05)*phi*phi + (0.0017996)*phi + (0.025963));
                }
                if(sec == 2){
                    dp = ((-9.8045e-07)*phi*phi + (6.7395e-05)*phi + (-4.6757e-05))*pp*pp + ((-1.4958e-05)*phi*phi + (-0.0011191)*phi + (-0.0025143))*pp + ((1.2699e-04)*phi*phi + (0.0033121)*phi + (0.020819));
                }
                if(sec == 3){
                    dp = ((-5.9459e-07)*phi*phi + (-2.8289e-05)*phi + (-4.3541e-04))*pp*pp + ((-1.5025e-05)*phi*phi + (5.7730e-04)*phi + (-0.0077582))*pp + ((7.3348e-05)*phi*phi + (-0.001102)*phi + (0.057052));
                }
                if(sec == 4){
                    dp = ((-2.2714e-06)*phi*phi + (-3.0360e-05)*phi + (-8.9322e-04))*pp*pp + ((2.9737e-05)*phi*phi + (5.1142e-04)*phi + (0.0045641))*pp + ((-1.0582e-04)*phi*phi + (-5.6852e-04)*phi + (0.027506));
                }
                if(sec == 5){
                    dp = ((-1.1490e-06)*phi*phi + (-6.2147e-06)*phi + (-4.7235e-04))*pp*pp + ((3.7039e-06)*phi*phi + (-1.5943e-04)*phi + (-8.5238e-04))*pp + ((4.4069e-05)*phi*phi + (0.0014152)*phi + (0.031933));
                }
                if(sec == 6){
                    dp = ((1.1076e-06)*phi*phi + (4.0156e-05)*phi + (-1.6341e-04))*pp*pp + ((-2.8613e-05)*phi*phi + (-5.1861e-04)*phi + (-0.0056437))*pp + ((1.2419e-04)*phi*phi + (4.9084e-04)*phi + (0.049976));
                }
            }
            
            //////////////////////////////////////////////////////////////////////////////////
            //==============================================================================//
            //==========//==========//  Electron Corrections (End)  //==========//==========//
            //==============================================================================//
            //////////////////////////////////////////////////////////////////////////////////



            /////////////////////////////////////////////////////////////////////////////////
            //=============================================================================//
            //==========//==========//     π+ Pion Corrections     //==========//==========//
            //=============================================================================//
            /////////////////////////////////////////////////////////////////////////////////
            
            if(ivec == 1){
                if(sec == 1){
                    dp = ((-5.4904e-07)*phi*phi + (-1.4436e-05)*phi + (3.1534e-04))*pp*pp + ((3.8231e-06)*phi*phi + (3.6582e-04)*phi + (-0.0046759))*pp + ((-5.4913e-06)*phi*phi + (-4.0157e-04)*phi + (0.010767));
                    dp = dp + ((6.1103e-07)*phi*phi + (5.5291e-06)*phi + (-1.9120e-04))*pp*pp + ((-3.2300e-06)*phi*phi + (1.5377e-05)*phi + (7.5279e-04))*pp + ((2.1434e-06)*phi*phi + (-6.9572e-06)*phi + (-7.9333e-05));
                    dp = dp + ((-1.3049e-06)*phi*phi + (1.1295e-05)*phi + (4.5797e-04))*pp*pp + ((9.3122e-06)*phi*phi + (-5.1074e-05)*phi + (-0.0030757))*pp + ((-1.3102e-05)*phi*phi + (2.2153e-05)*phi + (0.0040938));
                }
                if(sec == 2){
                    dp = ((-1.0087e-06)*phi*phi + (2.1319e-05)*phi + (7.8641e-04))*pp*pp + ((6.7485e-06)*phi*phi + (7.3716e-05)*phi + (-0.0094591))*pp + ((-1.1820e-05)*phi*phi + (-3.8103e-04)*phi + (0.018936));
                    dp = dp + ((8.8155e-07)*phi*phi + (-2.8257e-06)*phi + (-2.6729e-04))*pp*pp + ((-5.4499e-06)*phi*phi + (3.8397e-05)*phi + (0.0015914))*pp + ((6.8926e-06)*phi*phi + (-5.9386e-05)*phi + (-0.0021749));
                    dp = dp + ((-2.0147e-07)*phi*phi + (1.1061e-05)*phi + (3.8827e-04))*pp*pp + ((4.9294e-07)*phi*phi + (-6.0257e-05)*phi + (-0.0022087))*pp + ((9.8548e-07)*phi*phi + (5.9047e-05)*phi + (0.0022905));
                }
                if(sec == 3){
                    dp = ((8.6722e-08)*phi*phi + (-1.7975e-05)*phi + (4.8118e-05))*pp*pp + ((2.6273e-06)*phi*phi + (3.1453e-05)*phi + (-0.0015943))*pp + ((-6.4463e-06)*phi*phi + (-5.8990e-05)*phi + (0.0041703));
                    dp = dp + ((9.6317e-07)*phi*phi + (-1.7659e-06)*phi + (-8.8318e-05))*pp*pp + ((-5.1346e-06)*phi*phi + (8.3318e-06)*phi + (3.7723e-04))*pp + ((3.9548e-06)*phi*phi + (-6.9614e-05)*phi + (2.1393e-04));
                    dp = dp + ((5.6438e-07)*phi*phi + (8.1678e-06)*phi + (-9.4406e-05))*pp*pp + ((-3.9074e-06)*phi*phi + (-6.5174e-05)*phi + (5.4218e-04))*pp + ((6.3198e-06)*phi*phi + (1.0611e-04)*phi + (-4.5749e-04));
                }
                if(sec == 4){
                    dp = ((4.3406e-07)*phi*phi + (-4.9036e-06)*phi + (2.3064e-04))*pp*pp + ((1.3624e-06)*phi*phi + (3.2907e-05)*phi + (-0.0034872))*pp + ((-5.1017e-06)*phi*phi + (2.4593e-05)*phi + (0.0092479));
                    dp = dp + ((6.0218e-07)*phi*phi + (-1.4383e-05)*phi + (-3.1999e-05))*pp*pp + ((-1.1243e-06)*phi*phi + (9.3884e-05)*phi + (-4.1985e-04))*pp + ((-1.8808e-06)*phi*phi + (-1.2222e-04)*phi + (0.0014037));
                    dp = dp + ((-2.5490e-07)*phi*phi + (-8.5120e-07)*phi + (7.9109e-05))*pp*pp + ((2.5879e-06)*phi*phi + (8.6108e-06)*phi + (-5.1533e-04))*pp + ((-4.4521e-06)*phi*phi + (-1.7012e-05)*phi + (7.4848e-04));
                }
                if(sec == 5){
                    dp = ((2.4292e-07)*phi*phi + (8.8741e-06)*phi + (2.9482e-04))*pp*pp + ((3.7229e-06)*phi*phi + (7.3215e-06)*phi + (-0.0050685))*pp + ((-1.1974e-05)*phi*phi + (-1.3043e-04)*phi + (0.0078836));
                    dp = dp + ((1.0867e-06)*phi*phi + (-7.7630e-07)*phi + (-4.4930e-05))*pp*pp + ((-5.6564e-06)*phi*phi + (-1.3417e-05)*phi + (2.5224e-04))*pp + ((6.8460e-06)*phi*phi + (9.0495e-05)*phi + (-4.6587e-04));
                    dp = dp + ((8.5720e-07)*phi*phi + (-6.7464e-06)*phi + (-4.0944e-05))*pp*pp + ((-4.7370e-06)*phi*phi + (5.8808e-05)*phi + (1.9047e-04))*pp + ((5.7404e-06)*phi*phi + (-1.1105e-04)*phi + (-1.9392e-04));
                }
                if(sec == 6){
                    dp = ((2.1191e-06)*phi*phi + (-3.3710e-05)*phi + (2.5741e-04))*pp*pp + ((-1.2915e-05)*phi*phi + (2.3753e-04)*phi + (-2.6882e-04))*pp + ((2.2676e-05)*phi*phi + (-2.3115e-04)*phi + (-0.001283));
                    dp = dp + ((6.0270e-07)*phi*phi + (-6.8200e-06)*phi + (1.3103e-04))*pp*pp + ((-1.8745e-06)*phi*phi + (3.8646e-05)*phi + (-8.8056e-04))*pp + ((2.0885e-06)*phi*phi + (-3.4932e-05)*phi + (4.5895e-04));
                    dp = dp + ((4.7349e-08)*phi*phi + (-5.7528e-06)*phi + (-3.4097e-06))*pp*pp + ((1.7731e-06)*phi*phi + (3.5865e-05)*phi + (-5.7881e-04))*pp + ((-9.7008e-06)*phi*phi + (-4.1836e-05)*phi + (0.0035403));
                }
            }
            
            /////////////////////////////////////////////////////////////////////////////////
            //=============================================================================//
            //==========//==========//  π+ Pion Corrections (End)  //==========//==========//
            //=============================================================================//
            /////////////////////////////////////////////////////////////////////////////////




            /////////////////////////////////////////////////////////////////////////////////
            //=============================================================================//
            //==========//==========//     π- Pion Corrections     //==========//==========//
            //=============================================================================//
            /////////////////////////////////////////////////////////////////////////////////

            if(ivec == 2){
                if(sec == 1){
                    dp = ((-4.0192658422317425e-06)*phi*phi - (2.660222128967742e-05)*phi + 0.004774434682983547)*pp*pp;
                    dp = dp + ((1.9549520962477972e-05)*phi*phi - 0.0002456062756770577*phi - 0.03787692408323466)*pp; 
                    dp = dp + (-2.128953094937459e-05)*phi*phi + 0.0002461708852239913*phi + 0.08060704449822174 - 0.01;
                }
                if(sec == 2){
                    dp = ((1.193010521758372e-05)*phi*phi - (5.996221756031922e-05)*phi + 0.0009093437955814359)*pp*pp;
                    dp = dp + ((-4.89113824430594e-05)*phi*phi + 0.00021676479488147118*phi - 0.01861892053916726)*pp;  
                    dp = dp + (4.446394152208071e-05)*phi*phi - (3.6592784167335244e-05)*phi + 0.05498710249944096 - 0.01;
                }
                if(sec == 3){
                    dp = ((-1.6596664895992133e-07)*phi*phi + (6.317189710683516e-05)*phi + 0.0016364212312654086)*pp*pp;
                    dp = dp + ((-2.898409777520318e-07)*phi*phi - 0.00014531513577533802*phi - 0.025456145839203827)*pp;  
                    dp = dp + (2.6432552410603506e-06)*phi*phi + 0.00018447151306275443*phi + 0.06442602664627255 - 0.01;
                }
                if(sec == 4){
                    dp = ((2.4035259647558634e-07)*phi*phi - (8.649647351491232e-06)*phi + 0.004558993439848128)*pp*pp;
                    dp = dp + ((-5.981498144060984e-06)*phi*phi + 0.00010582131454222416*phi - 0.033572004651981686)*pp;  
                    dp = dp + (8.70140266889548e-06)*phi*phi - 0.00020137414379966883*phi + 0.07258774523336173 - 0.01;   
                }
                if(sec == 5){
                    dp = ((2.5817024702834863e-06)*phi*phi + 0.00010132810066914441*phi + 0.003397314538804711)*pp*pp;
                    dp = dp + ((-1.5116941263931812e-05)*phi*phi - 0.00040679799541839254*phi - 0.028144285760769876)*pp;  
                    dp = dp + (1.4701931057951464e-05)*phi*phi + 0.0002426350390593454*phi + 0.06781682510174941 - 0.01;
                }
                if(sec == 6){
                    dp = ((-8.196823669099362e-07)*phi*phi - (5.280412421933636e-05)*phi + 0.0018457238328451137)*pp*pp;
                    dp = dp + ((5.2675062282094536e-06)*phi*phi + 0.0001515803461044587*phi - 0.02294371578470564)*pp;  
                    dp = dp + (-9.459454671739747e-06)*phi*phi - 0.0002389523716779765*phi + 0.06428970810739926 - 0.01;
                }
            }

            /////////////////////////////////////////////////////////////////////////////////
            //=============================================================================//
            //==========//==========//  π- Pion Corrections (End)  //==========//==========//
            //=============================================================================//
            /////////////////////////////////////////////////////////////////////////////////



            //////////////////////////////////////////////////////////////////////////////////
            //==============================================================================//
            //==========//==========//      Proton Corrections      //==========//==========//
            //==============================================================================//
            //////////////////////////////////////////////////////////////////////////////////

            if(ivec == 3){
                if(sec == 1){
                    dp = (5.415e-04)*pp*pp + (-1.0262e-02)*pp + (7.78075e-03);
                    dp = dp + ((1.2129e-04)*pp*pp + (1.5373e-04)*pp + (-2.7084e-04));
                }
                if(sec == 2){
                    dp = (-9.5439e-04)*pp*pp + (-2.86273e-03)*pp + (3.38149e-03);
                    dp = dp + ((-1.6890e-03)*pp*pp + (4.3744e-03)*pp + (-2.1218e-03));
                }
                if(sec == 3){
                    dp = (-5.5541e-04)*pp*pp + (-7.69739e-03)*pp + (5.7692e-03);
                    dp = dp + ((7.6422e-04)*pp*pp + (-1.5425e-03)*pp + (5.4255e-04));
                }
                if(sec == 4){
                    dp = (-1.944e-04)*pp*pp + (-5.77104e-03)*pp + (3.42399e-03);
                    dp = dp + ((1.1174e-03)*pp*pp + (-3.2747e-03)*pp + (2.3687e-03));
                }
                if(sec == 5){
                    dp = (1.54009e-03)*pp*pp + (-1.69437e-02)*pp + (1.04656e-02);
                    dp = dp + ((-2.1067e-04)*pp*pp + (1.2266e-03)*pp + (-1.0553e-03));
                }
                if(sec == 6){
                    dp = (2.38182e-03)*pp*pp + (-2.07301e-02)*pp + (1.72325e-02);
                    dp = dp + ((-3.6002e-04)*pp*pp + (8.9582e-04)*pp + (-1.0093e-03));
                }
            }

            //////////////////////////////////////////////////////////////////////////////////
            //==============================================================================//
            //==========//==========//   Proton Corrections (End)   //==========//==========//
            //==============================================================================//
            //////////////////////////////////////////////////////////////////////////////////


            return dp/pp;

        }
    };



    """
    

    if(Mom_Correction_Q != "yes"):
        print("".join([color.BOLD, color.BLUE, "\nNot running with Momentum Corrections\n", color.END]))
    else:
        print("".join([color.BOLD, color.BLUE, "\nRunning with Momentum Corrections\n", color.END]))
        

        
    ###################################################################################################################################################################
    #################################################################   End of Momentum Corrections   #################################################################
    ###----------##----------##----------##----------##----------##-------------------------------------##----------##----------##----------##----------##----------###
    ################################################################# Calculating Kinematic Variables #################################################################
    ###################################################################################################################################################################
    
    
    ######################################################################################
    ##=====##  These calculations may have been made in the groovy code already  ##=====##
    ######################################################################################
    
    
    ##=====## The following is for backwards compatibility ##=====##
    if("pipx" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipx", "px")
    if("pipy" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipy", "py")
    if("pipz" not in rdf.GetColumnNames()):
        rdf = rdf.Define("pipz", "pz")
    
    
    if('calc' not in files_used_for_data_frame):
        
        #####################     Energy     #####################

        try:
            rdf = rdf.Define("el_E","".join([str(Correction_Code_Full_In), """
            auto fe = dppC(ex, ey, ez, esec, 0, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
            auto ele = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
            auto ele_E = ele.E();
            return ele_E;
            """]))

            rdf = rdf.Define("pip_E","".join([str(Correction_Code_Full_In), """
            auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
            auto pip0_E = pip0.E();
            return pip0_E;
            """]))
            
        except:
            print("\nMomentum Corrections Failed...\n")
            rdf = rdf.Define("el_E","""
            auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
            auto ele_E = ele.E();
            return ele_E;
            """)
            rdf = rdf.Define("pip_E","""
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
            auto pip0_E = pip0.E();
            return pip0_E;
            """)

        
        if(datatype == "mdf" or datatype == "pdf"):
            rdf = rdf.Define("el_E_gen","""
            auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto ele_E_gen = ele.E();
            return ele_E_gen;
            """)

            rdf = rdf.Define("pip_E_gen","""
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
            auto pip0_E_gen = pip0.E();
            return pip0_E_gen;
            """)
        
        
        
        #####################     Momentum     #####################

        try:
            rdf = rdf.Define("el", "".join([str(Correction_Code_Full_In), """
            auto fe = dppC(ex, ey, ez, esec, 0, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
            double el_P = fe*(sqrt(ex*ex + ey*ey + ez*ez));
            return el_P;
            """]))
            
            rdf = rdf.Define("pip", "".join([str(Correction_Code_Full_In), """
            auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
            double pip_P = fpip*(sqrt(pipx*pipx + pipy*pipy + pipz*pipz));
            return pip_P;
            """]))
        except:
            print("\nMomentum Corrections Failed...\n")
            rdf = rdf.Define("el","sqrt(ex*ex + ey*ey + ez*ez)")
            rdf = rdf.Define("pip","sqrt(pipx*pipx + pipy*pipy + pipz*pipz)")

        
        if(datatype == "mdf" or datatype == "pdf"):
            rdf = rdf.Define("el_gen","sqrt(ex_gen*ex_gen + ey_gen*ey_gen + ez_gen*ez_gen)")
            rdf = rdf.Define("pip_gen","sqrt(pipx_gen*pipx_gen + pipy_gen*pipy_gen + pipz_gen*pipz_gen)")



        #####################     Theta Angle     #####################

        rdf = rdf.Define("elth","atan2(sqrt(ex*ex + ey*ey), ez)*TMath::RadToDeg()")
        rdf = rdf.Define("pipth","atan2(sqrt(pipx*pipx + pipy*pipy), pipz)*TMath::RadToDeg()")
        
        if(datatype == "mdf" or datatype == "pdf"):
            rdf = rdf.Define("elth_gen","atan2(sqrt(ex_gen*ex_gen + ey_gen*ey_gen), ez_gen)*TMath::RadToDeg()")
            rdf = rdf.Define("pipth_gen","atan2(sqrt(pipx_gen*pipx_gen + pipy_gen*pipy_gen), pipz_gen)*TMath::RadToDeg()")



        #####################     Phi Angle     #####################

        rdf = rdf.Define("elPhi","""
        auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto elPhi = ele.Phi()*TMath::RadToDeg();
        if(elPhi < 0){
            elPhi += 360;
        }
        return elPhi;
        """)

        rdf = rdf.Define("pipPhi","""
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        auto pipPhi = pip0.Phi()*TMath::RadToDeg();
        if(pipPhi < 0){
            pipPhi += 360;
        }
        return pipPhi;
        """)
        
        
        if(datatype == "mdf" or datatype == "pdf"):
            rdf = rdf.Define("elPhi_gen","""
            auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto elPhi_gen = ele.Phi()*TMath::RadToDeg();
            if(elPhi_gen < 0){
                elPhi_gen += 360;
            }
            return elPhi_gen;
            """)

            rdf = rdf.Define("pipPhi_gen","""
            auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipy_gen, 0.13957);
            auto pipPhi_gen = pip0.Phi()*TMath::RadToDeg();
            if(pipPhi_gen < 0){
                pipPhi_gen += 360;
            }
            return pipPhi_gen;
            """)



        #####################     Sectors (angle definitions)     #####################

        rdf = rdf.Define("esec_a","""

        auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto ele_phi = (180/3.1415926)*ele.Phi();

        int esec_a = 0;

        if(ele_phi >= -30 && ele_phi < 30){
            esec_a = 1;
        }
        if(ele_phi >= 30 && ele_phi < 90){
            esec_a = 2;
        }
        if(ele_phi >= 90 && ele_phi < 150){
            esec_a = 3;
        }
        if(ele_phi >= 150 || ele_phi < -150){
            esec_a = 4;
        }
        if(ele_phi >= -90 && ele_phi < -30){
            esec_a = 5;
        }
        if(ele_phi >= -150 && ele_phi < -90){
            esec_a = 6;
        }

        return esec_a;
        """)


        rdf = rdf.Define("pipsec_a","""

        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        auto pip_phi = (180/3.1415926)*pip0.Phi();

        int pipsec_a = 0;

        if(pip_phi >= -45 && pip_phi < 15){
            pipsec_a = 1;
        }
        if(pip_phi >= 15 && pip_phi < 75){
            pipsec_a = 2;
        }
        if(pip_phi >= 75 && pip_phi < 135){
            pipsec_a = 3;
        }
        if(pip_phi >= 135 || pip_phi < -165){
            pipsec_a = 4;
        }
        if(pip_phi >= -105 && pip_phi < -45){
            pipsec_a = 5;
        }
        if(pip_phi >= -165 && pip_phi < -105){
            pipsec_a = 6;
        }

        return pipsec_a;
        """)
        
        
        
        if(datatype == "mdf" or datatype == "pdf"):
            rdf = rdf.Define("esec_gen","""

            auto ele = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto ele_phi = (180/3.1415926)*ele.Phi();

            int esec_gen = 0;

            if(ele_phi >= -30 && ele_phi < 30){
                esec_gen = 1;
            }
            if(ele_phi >= 30 && ele_phi < 90){
                esec_gen = 2;
            }
            if(ele_phi >= 90 && ele_phi < 150){
                esec_gen = 3;
            }
            if(ele_phi >= 150 || ele_phi < -150){
                esec_gen = 4;
            }
            if(ele_phi >= -90 && ele_phi < -30){
                esec_gen = 5;
            }
            if(ele_phi >= -150 && ele_phi < -90){
                esec_gen = 6;
            }

            return esec_gen;
            """)


            rdf = rdf.Define("pipsec_gen","""

            auto pip0 = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
            auto pip_phi = (180/3.1415926)*pip0.Phi();

            int pipsec_gen = 0;

            if(pip_phi >= -45 && pip_phi < 15){
                pipsec_gen = 1;
            }
            if(pip_phi >= 15 && pip_phi < 75){
                pipsec_gen = 2;
            }
            if(pip_phi >= 75 && pip_phi < 135){
                pipsec_gen = 3;
            }
            if(pip_phi >= 135 || pip_phi < -165){
                pipsec_gen = 4;
            }
            if(pip_phi >= -105 && pip_phi < -45){
                pipsec_gen = 5;
            }
            if(pip_phi >= -165 && pip_phi < -105){
                pipsec_gen = 6;
            }

            return pipsec_gen;
            """)


        #####################     Other Values     #####################

        rdf = rdf.Define("vals", "".join([str(Correction_Code_Full_In), """
        
        auto fe = dppC(ex, ey, ez, esec, 0, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
        
        auto beam = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
        auto targ = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        
        auto ele = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto epipX = beam + targ - ele - pip0;
        auto q = beam - ele;
        auto Q2 = - q.M2();
        auto v = beam.E() - ele.E();
        auto xB = Q2/(2*targ.M()*v);
        auto W2 = targ.M2() + 2*targ.M()*v - Q2;
        auto W = sqrt(W2);
        auto y = (targ.Dot(q))/(targ.Dot(beam));
        auto z = ((pip0.E())/(q.E()));
        auto gamma = 2*targ.M()*(xB/sqrt(Q2));
        auto epsilon = (1 - y - 0.25*(gamma*gamma)*(y*y))/(1 - y + 0.5*(y*y) + 0.25*(gamma*gamma)*(y*y));
        
        std::vector<double> vals = {epipX.M(), epipX.M2(), Q2, xB, v, W2, W, y, z, epsilon};

        return vals;
        """]))


        rdf = rdf.Define('MM', 'vals[0]') # Missing Mass
        rdf = rdf.Define('MM2', 'vals[1]') # Missing Mass Squared 
        rdf = rdf.Define('Q2', 'vals[2]') # lepton momentum transfer squared
        rdf = rdf.Define('xB', 'vals[3]') # fraction of the proton momentum that is carried by the struck quark
        rdf = rdf.Define('v', 'vals[4]') # energy of the virtual photon
        rdf = rdf.Define('s', 'vals[5]') # center-of-mass energy squared
        rdf = rdf.Define('W', 'vals[6]') # center-of-mass energy
        rdf = rdf.Define('y', 'vals[7]') # energy fraction of the incoming lepton carried by the virtual photon
        rdf = rdf.Define('z', 'vals[8]') # energy fraction of the virtual photon carried by the outgoing hadron
        rdf = rdf.Define('epsilon', 'vals[9]') # ratio of the longitudinal and transverse photon flux
        
        
        
        if(datatype == "mdf" or datatype == "pdf"):
            rdf = rdf.Define("vals_gen","""
            auto beam_gen = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
            auto targ_gen = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
            auto ele_gen = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
            auto pip0_gen = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);

            auto epipX_gen = beam_gen + targ_gen - ele_gen - pip0_gen;
            auto q_gen = beam_gen - ele_gen;
            auto Q2_gen = - q_gen.M2();
            auto v_gen = beam_gen.E() - ele_gen.E();
            auto xB_gen = Q2_gen/(2*targ_gen.M()*v_gen);
            auto W2_gen = targ_gen.M2() + 2*targ_gen.M()*v_gen - Q2_gen;
            auto W_gen = sqrt(W2_gen);
            auto y_gen = (targ_gen.Dot(q_gen))/(targ_gen.Dot(beam_gen));
            auto z_gen = ((pip0_gen.E())/(q_gen.E()));
            auto gamma_gen = 2*targ_gen.M()*(xB_gen/sqrt(Q2_gen));
            auto epsilon_gen = (1 - y_gen - 0.25*(gamma_gen*gamma_gen)*(y_gen*y_gen))/(1 - y_gen + 0.5*(y_gen*y_gen) + 0.25*(gamma_gen*gamma_gen)*(y_gen*y_gen));

            std::vector<double> vals_gen = {epipX_gen.M(), epipX_gen.M2(), Q2_gen, xB_gen, v_gen, W2_gen, W_gen, y_gen, z_gen, epsilon_gen};

            return vals_gen;
            """)

            rdf = rdf.Define('MM_gen', 'vals_gen[0]')
            rdf = rdf.Define('MM2_gen', 'vals_gen[1]')
            rdf = rdf.Define('Q2_gen', 'vals_gen[2]')
            rdf = rdf.Define('xB_gen', 'vals_gen[3]')
            rdf = rdf.Define('v_gen', 'vals_gen[4]')
            rdf = rdf.Define('s_gen', 'vals_gen[5]')
            rdf = rdf.Define('W_gen', 'vals_gen[6]')
            rdf = rdf.Define('y_gen', 'vals_gen[7]')
            rdf = rdf.Define('z_gen', 'vals_gen[8]')
            rdf = rdf.Define('epsilon_gen', 'vals_gen[9]')
        
    
    ##############################################################################
    ##=====##  The above calculations used to be run in the groovy code  ##=====##
    ##############################################################################
    
    
    
    
    
    ####################################################################################################################################################################
    ###################################################     Done with Calculating (Initial) Kinematic Variables      ###################################################
    ###----------##----------##----------##----------##--------------------------------------------------------------##----------##----------##----------##----------###
    ###################################################       Rotation Matrix and Center-of-Mass/Boosted Frame       ###################################################
    ####################################################################################################################################################################
    
    
    Rotation_Matrix = """
    
    /////////////////////////////////////////////          Rotation Matrix          /////////////////////////////////////////////


    auto Rot_Matrix = [&](TLorentzVector vector, int Lab2CM_or_CM2Lab, double Theta_Rot, double Phi_Rot)
    {
        double Rot_X1 = vector.X();
        double Rot_Y1 = vector.Y();
        double Rot_Z1 = vector.Z();

        double Rot_X = Rot_X1;
        double Rot_Y = Rot_Y1;
        double Rot_Z = Rot_Z1;

        // Lab2CM_or_CM2Lab is a parameter which determines if you rotating from the lab frame to the CM frame, or if you are rotating back in the opposite direction
        // Lab2CM_or_CM2Lab = -1 gives a rotation to the CM frame (from the lab frame)
        // Lab2CM_or_CM2Lab = +1 gives a rotation to the lab frame (from the CM frame)


        Theta_Rot = -1*Theta_Rot;   // Always give the angle of rotation Theta as the value given by .Theta()
                                    // This subroutine will handle the fact that the matrix rotation wants the negative of the angle of rotation

        // Rotation to Lab Frame
        if(Lab2CM_or_CM2Lab == -1){
            Rot_X = Rot_X1*TMath::Cos(Theta_Rot)*TMath::Cos(Phi_Rot) - Rot_Z1*TMath::Sin(Theta_Rot) + Rot_Y1*TMath::Cos(Theta_Rot)*TMath::Sin(Phi_Rot);
            Rot_Y = Rot_Y1*TMath::Cos(Phi_Rot) - Rot_X1*TMath::Sin(Phi_Rot);
            Rot_Z = Rot_Z1*TMath::Cos(Theta_Rot) + Rot_X1*TMath::Cos(Phi_Rot)*TMath::Sin(Theta_Rot) + Rot_Y1*TMath::Sin(Theta_Rot)*TMath::Sin(Phi_Rot);
        }

        // Rotation to CM Frame
        if(Lab2CM_or_CM2Lab == 1){
            Rot_X = Rot_X1*TMath::Cos(Theta_Rot)*TMath::Cos(Phi_Rot) + Rot_Z1*TMath::Cos(Phi_Rot)*TMath::Sin(Theta_Rot) - Rot_Y1*TMath::Sin(Phi_Rot);
            Rot_Y = Rot_Y1*TMath::Cos(Phi_Rot) + Rot_X1*TMath::Sin(Phi_Rot)*TMath::Cos(Theta_Rot) + Rot_Z1*TMath::Sin(Theta_Rot)*TMath::Sin(Phi_Rot);
            Rot_Z = Rot_Z1*TMath::Cos(Theta_Rot) - Rot_X1*TMath::Sin(Theta_Rot);
        }

        TLorentzVector vector_Rotated(Rot_X, Rot_Y, Rot_Z, vector.E());

        return vector_Rotated;

    };



    /////////////////////////////////////////////          (End of) Rotation Matrix          /////////////////////////////////////////////
    
    
    """
    
    
    rdf = rdf.Define("vals2", "".join([str(Correction_Code_Full_In), """
        
    auto fe = dppC(ex, ey, ez, esec, 0, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
    auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
    
    auto beamM = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
    auto targM = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
    
    auto eleM = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
    auto pip0M = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
    
    auto lv_qMM = beamM - eleM;

    TLorentzVector beam(0, 0, 10.6041, beamM.E());
    TLorentzVector targ(0, 0, 0, targM.E());
    
    TLorentzVector ele(ex*fe, ey*fe, ez*fe, eleM.E());
    TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());
    
    TLorentzVector lv_q = beam - ele;


    ///////////////     Angles for Rotation     ///////////////
    double Theta_q = lv_q.Theta();
    double Phi_el = ele.Phi();


    """, str(Rotation_Matrix), """



    ///////////////     Rotating to CM Frame     ///////////////

    auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
    auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
    auto ele_Clone  = Rot_Matrix(ele,  -1, Theta_q, Phi_el);
    auto pip0_Clone = Rot_Matrix(pip0, -1, Theta_q, Phi_el);
    auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);


    ///////////////     Saving CM components     ///////////////

    double pipx_1 = pip0_Clone.X();
    double pipy_1 = pip0_Clone.Y();
    double pipz_1 = pip0_Clone.Z();

    double qx = lv_q_Clone.X();
    double qy = lv_q_Clone.Y();
    double qz = lv_q_Clone.Z();

    double beamx = beam_Clone.X();
    double beamy = beam_Clone.Y();
    double beamz = beam_Clone.Z();

    double elex = ele_Clone.X();
    double eley = ele_Clone.Y();
    double elez = ele_Clone.Z();


    ///////////////     Boosting Vectors     ///////////////

    auto fCM = lv_q_Clone + targ_Clone;
    auto boost = -(fCM.BoostVector());

    auto qlv_Boost(lv_q_Clone);
    auto ele_Boost(ele_Clone);
    auto pip_Boost(pip0_Clone);
    auto beamBoost(beam_Clone);
    auto targBoost(targ_Clone);

    qlv_Boost.Boost(boost);
    ele_Boost.Boost(boost);
    pip_Boost.Boost(boost);
    beamBoost.Boost(boost);
    targBoost.Boost(boost);


    TVector3 v0, v1;
    v0 = qlv_Boost.Vect().Cross(ele_Boost.Vect());
    v1 = qlv_Boost.Vect().Cross(pip_Boost.Vect());
    Double_t c0, c1, c2, c3;
    c0 = v0.Dot(pip_Boost.Vect());
    c1 = v0.Dot(v1);
    c2 = v0.Mag();
    c3 = v1.Mag();


    // Phi Trento (using Stefan's equation)
    double phi_t_cross_product = (c0/TMath::Abs(c0)) * TMath::ACos(c1 /(c2*c3));
    

    double Cos_theta_t = (pip0.Vect().Dot(lv_q.Vect()))/(pip0.Vect().Mag()*lv_q.Vect().Mag());
    double theta_t = TMath::ACos(Cos_theta_t);

    double pipTx = pip0.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
    double pipTy = pip0.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
    double pipTz = pip0.P()*TMath::Cos(theta_t);

    TVector3 pipT(pipTx, pipTy, pipTz);


    phi_t_cross_product = phi_t_cross_product*TMath::RadToDeg();


    ///////////////   x Feynmann   ///////////////
    double xF = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W);


    // pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
    double pT = sqrt(pipx_1*pipx_1 + pipy_1*pipy_1);
    double phi_t = pip0_Clone.Phi()*TMath::RadToDeg();


    if(phi_t < 0){
        phi_t += 360;
    }



    // std::vector<double> vals2 = {pT, phi_t, xF, pipx_1, pipy_1, pipz_1, qx, qy, qz, beamx, beamy, beamz, elex, eley, elez};
    std::vector<double> vals2 = {pT, phi_t, xF};


    return vals2;

    """]))



    rdf = rdf.Define('pT', 'vals2[0]')    # transverse momentum of the final state hadron
    rdf = rdf.Define('phi_t',' vals2[1]') # Most important angle (between lepton and hadron planes)
    rdf = rdf.Define('xF', 'vals2[2]')    # x Feynmann

    # rdf = rdf.Define('pipx_CM','vals2[3]') # CM pi+ x-momentum
    # rdf = rdf.Define('pipy_CM','vals2[4]') # CM pi+ y-momentum
    # rdf = rdf.Define('pipz_CM','vals2[5]') # CM pi+ z-momentum

    # rdf = rdf.Define('qx_CM','vals2[6]') # CM q x-momentum
    # rdf = rdf.Define('qy_CM','vals2[7]') # CM q y-momentum
    # rdf = rdf.Define('qz_CM','vals2[8]') # CM q z-momentum

    # rdf = rdf.Define('beamX_CM','vals2[9]')  # CM beam x-momentum
    # rdf = rdf.Define('beamY_CM','vals2[10]') # CM beam y-momentum
    # rdf = rdf.Define('beamZ_CM','vals2[11]') # CM beam z-momentum

    # rdf = rdf.Define('eleX_CM','vals2[12]') # CM scattered electron x-momentum
    # rdf = rdf.Define('eleY_CM','vals2[13]') # CM scattered electron y-momentum
    # rdf = rdf.Define('eleZ_CM','vals2[14]') # CM scattered electron z-momentum
    
    
    
    if(datatype == "mdf" or datatype == "pdf"):
        rdf = rdf.Define("vals2_gen", "".join(["""
        auto beamM = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
        auto targM = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        auto eleM = ROOT::Math::PxPyPzMVector(ex_gen, ey_gen, ez_gen, 0);
        auto pip0M = ROOT::Math::PxPyPzMVector(pipx_gen, pipy_gen, pipz_gen, 0.13957);
        auto lv_qMM = beamM - eleM;

        TLorentzVector beam(0, 0, 10.6041, beamM.E());
        TLorentzVector targ(0, 0, 0, targM.E());
        TLorentzVector ele(ex_gen, ey_gen, ez_gen, eleM.E());
        TLorentzVector pip0(pipx_gen, pipy_gen, pipz_gen, pip0M.E());
        TLorentzVector lv_q = beam - ele;


        ///////////////     Angles for Rotation     ///////////////
        double Theta_q = lv_q.Theta();
        double Phi_el = ele.Phi();


        """, str(Rotation_Matrix), """


        ///////////////     Rotating to CM Frame     ///////////////

        auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
        auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
        auto ele_Clone  = Rot_Matrix(ele,  -1, Theta_q, Phi_el);
        auto pip0_Clone = Rot_Matrix(pip0, -1, Theta_q, Phi_el);
        auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);


        ///////////////     Saving CM components     ///////////////

        double pipx_1_gen = pip0_Clone.X();
        double pipy_1_gen = pip0_Clone.Y();
        double pipz_1_gen = pip0_Clone.Z();

        double qx_gen = lv_q_Clone.X();
        double qy_gen = lv_q_Clone.Y();
        double qz_gen = lv_q_Clone.Z();

        double beamx_gen = beam_Clone.X();
        double beamy_gen = beam_Clone.Y();
        double beamz_gen = beam_Clone.Z();

        double elex_gen = ele_Clone.X();
        double eley_gen = ele_Clone.Y();
        double elez_gen = ele_Clone.Z();


        ///////////////     Boosting Vectors     ///////////////

        auto fCM = lv_q_Clone + targ_Clone;
        auto boost = -(fCM.BoostVector());

        auto qlv_Boost(lv_q_Clone);
        auto ele_Boost(ele_Clone);
        auto pip_Boost(pip0_Clone);
        auto beamBoost(beam_Clone);
        auto targBoost(targ_Clone);

        qlv_Boost.Boost(boost);
        ele_Boost.Boost(boost);
        pip_Boost.Boost(boost);
        beamBoost.Boost(boost);
        targBoost.Boost(boost);


        ///////////////////////////////////     At This Point: The particle vectors have all been rotated and boosted into the CM frame     ///////////////////////////////////

        TVector3 v0, v1;
        v0 = qlv_Boost.Vect().Cross(ele_Boost.Vect());
        v1 = qlv_Boost.Vect().Cross(pip_Boost.Vect());
        Double_t c0, c1, c2, c3;
        c0 = v0.Dot(pip_Boost.Vect());
        c1 = v0.Dot(v1);
        c2 = v0.Mag();
        c3 = v1.Mag();

        // Phi Trento (using Stefan's equation)
        double phi_t_cross_product = (c0/TMath::Abs(c0)) * TMath::ACos(c1 /(c2*c3));

        double Cos_theta_t = (pip0.Vect().Dot(lv_q.Vect()))/(pip0.Vect().Mag()*lv_q.Vect().Mag());
        double theta_t = TMath::ACos(Cos_theta_t);

        double pipTx_gen = pip0.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTy_gen = pip0.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTz_gen = pip0.P()*TMath::Cos(theta_t);

        TVector3 pipT(pipTx_gen, pipTy_gen, pipTz_gen);


        double phi_t_cross_product_gen = phi_t_cross_product_gen*TMath::RadToDeg();

        ///////////////   x Feynmann   ///////////////
        double xF_gen = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W_gen);


        // pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
        double pT_gen = sqrt(pipx_1_gen*pipx_1_gen + pipy_1_gen*pipy_1_gen);
        double phi_t_gen = pip0_Clone.Phi()*TMath::RadToDeg();


        if(phi_t_gen < 0){
            phi_t_gen += 360;
        }

        // std::vector<double> vals2_gen = {pT_gen, phi_t_gen, xF_gen, pipx_1_gen, pipy_1_gen, pipz_1_gen, qx_gen, qy_gen, qz_gen, beamx_gen, beamy_gen, beamz_gen, elex_gen, eley_gen, elez_gen};
        std::vector<double> vals2_gen = {pT_gen, phi_t_gen, xF_gen};


        return vals2_gen;

        """]))

        rdf = rdf.Define('pT_gen','vals2_gen[0]')
        rdf = rdf.Define('phi_t_gen','vals2_gen[1]')
        rdf = rdf.Define('xF_gen','vals2_gen[2]')
    
    
    
    #################################################################################################################################################################
    ###################################################       Done with Center-of-Mass/Boosted Frame (Main)       ###################################################
    ###----------##----------##----------##----------##-----------------------------------------------------------##----------##----------##----------##----------###
    ###################################################          Defining Smearing Function/Calculations          ###################################################
    #################################################################################################################################################################
    
    
    
    ##===============================================================================================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##=================================##     Defining the Smearing Functions     ##=================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##===============================================================================================================##
    
    smearing_function = """
    
        //===========================================================================//
        //=================//     Smearing Function (From FX)     //=================//
        //===========================================================================//
        
        auto smear_func = [&](TLorentzVector V4){

            // True generated values (i.e., values of the unsmeared TLorentzVector)

            double inM = V4.M();
            double smeared_P  = V4.P();
            double smeared_Th = V4.Theta();
            double smeared_Phi = V4.Phi();

            TLorentzVector V4_new(V4.X(), V4.Y(), V4.Z(), V4.E());

            // Calculate resolutions

            double smeared_ThD = TMath::RadToDeg()*smeared_Th;
            double momS1 = 0.0184291 - 0.0110083*smeared_ThD + 0.00227667*smeared_ThD*smeared_ThD - 0.000140152*smeared_ThD*smeared_ThD*smeared_ThD + (3.07424e-06)*smeared_ThD*smeared_ThD*smeared_ThD*smeared_ThD;
            double momS2 = 0.02*smeared_ThD;
            double momR  = 0.01 * TMath::Sqrt( TMath::Power(momS1*smeared_P,2) + TMath::Power(momS2,2));
            momR *= 2.0;

            // // From ∆P(El) Sigma distributions:
            // momR *= (0.02408)*V4.P()*V4.P() + (-0.25556)*V4.P() + (1.33331);

            double theS1 = 0.004*smeared_ThD + 0.1;
            double theS2 = 0;
            double theR  = TMath::Sqrt(TMath::Power(theS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(theS2,2) );
            theR *= 2.5;

            double phiS1 = 0.85 - 0.015*smeared_ThD;
            double phiS2 = 0.17 - 0.003*smeared_ThD;
            double phiR  = TMath::Sqrt(TMath::Power(phiS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(phiS2,2) );
            phiR *= 3.5;
            
            
            // cout<<"Smearing Factor for Phi: "<<phiR<<endl;
            // cout<<"Smearing Factor for Th: "<<theR<<endl;
            // cout<<"Smearing Factor for P: "<<momR<<endl;


            // cout<<"Pre-Smear Phi (degrees): "<<TMath::RadToDeg()*(smeared_Phi)<<endl;
            // cout<<"Pre-Smear Th (degrees): "<<TMath::RadToDeg()*(smeared_Th)<<endl;
            // cout<<"Pre-Smear P : "<<smeared_P<<endl;

            // overwrite EB (i.e., applying the smear)
            smeared_Phi += TMath::DegToRad() * phiR * gRandom->Gaus(0,1);
            smeared_Th += TMath::DegToRad() * theR * gRandom->Gaus(0,1);
            smeared_P  += momR  * gRandom->Gaus(0,1) *  V4.P();

            // cout<<"Smear-Factor Phi (degrees): "<<TMath::RadToDeg()*((TMath::DegToRad() * phiR * gRandom->Gaus(0,1)))<<endl;
            // cout<<"Smear-Factor Th (degrees): "<<TMath::RadToDeg()*((TMath::DegToRad() * theR * gRandom->Gaus(0,1)))<<endl;
            // cout<<"Smear-Factor P : "<<(momR  * gRandom->Gaus(0,1) *  V4.P())<<endl;

            // cout<<"Post-Smear Phi (degrees): "<<TMath::RadToDeg()*(smeared_Phi)<<endl;
            // cout<<"Post-Smear Th (degrees): "<<TMath::RadToDeg()*(smeared_Th)<<endl;
            // cout<<"Post-Smear P : "<<smeared_P<<endl;

            // EB_rec_mom = GEN_mom + resolution_momentum x gaussian x GEN_mom
            // EB_rec_ang = GEN_ang + resolution_angle x gaussian

            V4_new.SetE( TMath::Sqrt( smeared_P*smeared_P + inM*inM )  );
            V4_new.SetRho( smeared_P );
            V4_new.SetTheta( smeared_Th );
            V4_new.SetPhi( smeared_Phi );

            return V4_new;

        };
    
    """
    
    
    smearing_function = """
        //===========================================================================//
        //=================//     Modified Smearing Function      //=================//
        //===========================================================================//
        auto smear_func = [&](TLorentzVector V4, int ivec){
            // True generated values (i.e., values of the unsmeared TLorentzVector)
            double inM = V4.M();
            double smeared_P  = V4.P();
            double smeared_Th = V4.Theta();
            double smeared_Phi = V4.Phi();
            TLorentzVector V4_new(V4.X(), V4.Y(), V4.Z(), V4.E());
            // Calculate resolutions
            double smeared_ThD = TMath::RadToDeg()*smeared_Th;
            double momS1 = 0.0184291 - 0.0110083*smeared_ThD + 0.00227667*smeared_ThD*smeared_ThD - 0.000140152*smeared_ThD*smeared_ThD*smeared_ThD + (3.07424e-06)*smeared_ThD*smeared_ThD*smeared_ThD*smeared_ThD;
            double momS2 = 0.02*smeared_ThD;
            double momR  = 0.01 * TMath::Sqrt( TMath::Power(momS1*smeared_P,2) + TMath::Power(momS2,2));
            momR *= 2.0;
            if(ivec == 0){
                // From ∆P(Electron) Sigma distributions:
                momR *= (-1.0429e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (1.3654e-03)*(V4.Theta()*TMath::RadToDeg()) + (1.0663e+00);
                momR *= (-8.4052e-04)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (9.8234e-03)*(V4.Theta()*TMath::RadToDeg()) + (1.0144e+00);
                momR *= (1.5861e-02)*(V4.P())*(V4.P()) + (-1.5747e-01)*(V4.P()) + (1.3121e+00);
                momR *= (-9.6572e-04)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (1.6144e-02)*(V4.Theta()*TMath::RadToDeg()) + (9.5746e-01); 
            }
            if(ivec == 1){
                // From ∆P(Pi+ Pion) Sigma distributions:
                momR *= (-1.1676e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (4.3908e-02)*(V4.Theta()*TMath::RadToDeg()) + (4.3709e-01);
                momR *= (-2.3121e-02)*(V4.P())*(V4.P()) + (5.6810e-02)*(V4.P()) + (8.7293e-01);
                momR *= (-2.5476e-02)*(V4.P())*(V4.P()) + (7.6973e-02)*(V4.P()) + (8.6465e-01);
                momR *= (-2.6101e-02)*(V4.P())*(V4.P()) + (1.1440e-01)*(V4.P()) + (7.8815e-01);
            }
            double theS1 = 0.004*smeared_ThD + 0.1;
            double theS2 = 0;
            double theR  = TMath::Sqrt(TMath::Power(theS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(theS2,2) );
            theR *= 2.5;
            if(ivec == 0){
                // From ∆Theta(Electron) Sigma distributions (Function of Momentum):
                theR *= (-7.9405e-02)*(V4.P())*(V4.P()) + (9.3003e-01)*(V4.P()) + (-1.4985e+00);
                // From ∆Theta(Electron) Sigma distributions (Function of Theta):
                theR *= (-1.5170e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (5.1704e-02)*(V4.Theta()*TMath::RadToDeg()) + (7.9883e-01);
                // From ∆Theta(Electron) Sigma distributions (Function of Momentum):
                theR *= (-9.9576e-02)*(V4.P())*(V4.P()) + (1.1164e+00)*(V4.P()) + (-1.7216e+00);
            }
            if(ivec == 1){
                // From ∆Theta(Pi+ Pion) Sigma distributions (Function of Momentum):
                theR *= (-2.2858e-02)*(V4.P())*(V4.P()) + (2.3043e-01)*(V4.P()) + (5.7916e-01);                
                // From ∆Theta(Pi+ Pion) Sigma distributions (Function of Theta):
                theR *= (-1.5395e-03)*(V4.Theta()*TMath::RadToDeg())*(V4.Theta()*TMath::RadToDeg()) + (7.6614e-02)*(V4.Theta()*TMath::RadToDeg()) + (2.3594e-01);
                // From ∆Theta(Pi+ Pion) Sigma distributions (Function of Momentum):
                theR *= (-4.8283e-03)*(V4.P())*(V4.P()) + (1.6123e-01)*(V4.P()) + (7.6315e-01);
                // From ∆Theta(Pi+ Pion) Sigma distributions (Function of Momentum):
                theR *= (1.9715e-02)*(V4.P())*(V4.P()) + (-4.9812e-02)*(V4.P()) + (1.2059e+00);
                theR *= (2.7160e-02)*(V4.P())*(V4.P()) + (-1.0975e-01)*(V4.P()) + (1.2968e+00);
                // From ∆Theta(Pi+ Pion) Vs Momentum Sigma distributions:
                theR *= (-1.2412e-02)*(V4.P())*(V4.P()) + (1.8465e-01)*(V4.P()) + (7.5162e-01);
            }   
            double phiS1 = 0.85 - 0.015*smeared_ThD;
            double phiS2 = 0.17 - 0.003*smeared_ThD;
            double phiR  = TMath::Sqrt(TMath::Power(phiS1*TMath::Sqrt(smeared_P*smeared_P + 0.13957*0.13957)/(smeared_P*smeared_P),2) + TMath::Power(phiS2,2) );
            phiR *= 3.5;
            // overwrite EB (i.e., applying the smear)
            smeared_Phi += TMath::DegToRad() * phiR * gRandom->Gaus(0,1);
            smeared_Th += TMath::DegToRad() * theR * gRandom->Gaus(0,1);
            smeared_P  += momR  * gRandom->Gaus(0,1) *  V4.P();
            V4_new.SetE( TMath::Sqrt( smeared_P*smeared_P + inM*inM )  );
            V4_new.SetRho( smeared_P );
            V4_new.SetTheta( smeared_Th );
            V4_new.SetPhi( smeared_Phi );
            return V4_new;
        };
    """
    
    
    
    ##===============================================================================================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##=================================##     Applying the Smearing Functions     ##=================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##===============================================================================================================##
    
    if(datatype in ["mdf", "pdf"]):
        rdf = rdf.Define("smeared_vals", "".join(["""


        """, str(smearing_function), """

        auto beamM = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
        auto targM = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);
        auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

        TLorentzVector beam(0, 0, 10.6041, beamM.E());
        TLorentzVector targ(0, 0, 0, targM.E());
        TLorentzVector ele(ex, ey, ez, eleM.E());
        TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());

        TLorentzVector ele_NO_SMEAR(ex, ey, ez, eleM.E());
        TLorentzVector pip0_NO_SMEAR(pipx, pipy, pipz, pip0M.E());


        //========================================================================//
        //=================//     Smearing PxPyPzMVector's     //=================//
        //========================================================================//


        TLorentzVector ele_smeared  = smear_func(ele""", (");"  if("ivec" not in str(smearing_function)) else ", 0);"), """
        TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """


        //=========================================================================//
        //=================//     Vectors have been Smeared     //=================//
        //=========================================================================//

        TLorentzVector lv_q = beam - ele_smeared;


        auto Delta_Smear_El_P = abs(ele_smeared.P()) - abs(ele_NO_SMEAR.P()); // Delta_Smear_El.P();
        auto Delta_Smear_El_Th = (abs(ele_smeared.Theta()) - abs(ele_NO_SMEAR.Theta()))*TMath::RadToDeg(); // Delta_Smear_El.Theta()*TMath::RadToDeg();
        auto Delta_Smear_El_Phi = (abs(ele_smeared.Phi()) - abs(ele_NO_SMEAR.Phi()))*TMath::RadToDeg(); // Delta_Smear_El.Phi()*TMath::RadToDeg();

        auto Delta_Smear_Pip_P = abs(pip0_smeared.P()) - abs(pip0_NO_SMEAR.P()); // Delta_Smear_Pip.P();
        auto Delta_Smear_Pip_Th = (abs(pip0_smeared.Theta()) - abs(pip0_NO_SMEAR.Theta()))*TMath::RadToDeg(); // Delta_Smear_Pip.Theta()*TMath::RadToDeg();
        auto Delta_Smear_Pip_Phi = (abs(pip0_smeared.Phi()) - abs(pip0_NO_SMEAR.Phi()))*TMath::RadToDeg(); // Delta_Smear_Pip.Phi()*TMath::RadToDeg();




        // Rest of calculations are performed as normal from here


        auto epipX = beam + targ - ele_smeared - pip0_smeared;

        auto q_smeared = beam - ele_smeared;

        auto Q2_smeared = -q_smeared.M2();

        auto v_smeared = beam.E() - ele_smeared.E();

        auto xB_smeared = Q2_smeared/(2*targ.M()*v_smeared);

        auto W2_smeared = targ.M2() + 2*targ.M()*v_smeared - Q2_smeared;

        auto W_smeared = sqrt(W2_smeared);

        auto y_smeared = (targ.Dot(q_smeared))/(targ.Dot(beam));

        auto z_smeared = ((pip0_smeared.E())/(q_smeared.E()));

        auto gamma_smeared = 2*targ.M()*(xB_smeared/sqrt(Q2_smeared));

        auto epsilon_smeared = (1 - y_smeared - 0.25*(gamma_smeared*gamma_smeared)*(y_smeared*y_smeared))/(1 - y + 0.5*(y_smeared*y_smeared) + 0.25*(gamma_smeared*gamma_smeared)*(y_smeared*y_smeared));



        // Particles' (Smeared) Energies/Momentums/Angles
        auto ele_E_smeared = ele_smeared.E();
        auto pip0_E_smeared = pip0_smeared.E();

        auto el_smeared = ele_smeared.P();
        auto pip_smeared = pip0_smeared.P();

        auto elth_smeared = ele_smeared.Theta()*TMath::RadToDeg();
        auto pipth_smeared = pip0_smeared.Theta()*TMath::RadToDeg();

        auto elPhi_smeared = ele_smeared.Phi()*TMath::RadToDeg();

        if(elPhi_smeared < 0){
            elPhi_smeared += 360;
        }

        auto pipPhi_smeared = pip0_smeared.Phi()*TMath::RadToDeg();

        if(pipPhi_smeared < 0){
            pipPhi_smeared += 360;
        }



        //=================================================================================================================================//
        //==============================================//          Rotation Code          //==============================================//
        //=================================================================================================================================//



        ///////////////     Angles for Rotation     ///////////////
        double Theta_q = lv_q.Theta();
        double Phi_el = ele_smeared.Phi();


        """, str(Rotation_Matrix), """



        ///////////////     Rotating to CM Frame     ///////////////

        auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
        auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
        auto ele_Clone  = Rot_Matrix(ele_smeared,  -1, Theta_q, Phi_el);
        auto pip0_Clone = Rot_Matrix(pip0_smeared, -1, Theta_q, Phi_el);
        auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);


        ///////////////     Saving CM components     ///////////////

        double pipx_smeared = pip0_Clone.X();
        double pipy_smeared = pip0_Clone.Y();
        double pipz_smeared = pip0_Clone.Z();

        double qx_smeared = lv_q_Clone.X();
        double qy_smeared = lv_q_Clone.Y();
        double qz_smeared = lv_q_Clone.Z();

        double beamx_smeared = beam_Clone.X();
        double beamy_smeared = beam_Clone.Y();
        double beamz_smeared = beam_Clone.Z();

        double elex_smeared = ele_Clone.X();
        double eley_smeared = ele_Clone.Y();
        double elez_smeared = ele_Clone.Z();


        ///////////////     Boosting Vectors     ///////////////

        auto fCM = lv_q_Clone + targ_Clone;
        auto boost = -(fCM.BoostVector());

        auto qlv_Boost(lv_q_Clone);
        auto ele_Boost(ele_Clone);
        auto pip_Boost(pip0_Clone);
        auto beamBoost(beam_Clone);
        auto targBoost(targ_Clone);

        qlv_Boost.Boost(boost);
        ele_Boost.Boost(boost);
        pip_Boost.Boost(boost);
        beamBoost.Boost(boost);
        targBoost.Boost(boost);


        ///////////////////////////////////     At This Point: The particle vectors have all been rotated and boosted into the CM frame     ///////////////////////////////////


        TVector3 v0, v1;
        v0 = qlv_Boost.Vect().Cross(ele_Boost.Vect());
        v1 = qlv_Boost.Vect().Cross(pip_Boost.Vect());
        Double_t c0, c1, c2, c3;
        c0 = v0.Dot(pip_Boost.Vect());
        c1 = v0.Dot(v1);
        c2 = v0.Mag();
        c3 = v1.Mag();


        // Phi Trento (using Stefan's equation)
        double phi_t_cross_product = (c0/TMath::Abs(c0)) * TMath::ACos(c1 /(c2*c3));


        double Cos_theta_t = (pip0_smeared.Vect().Dot(lv_q.Vect()))/(pip0_smeared.Vect().Mag()*lv_q.Vect().Mag());
        double theta_t = TMath::ACos(Cos_theta_t);

        double pipTx = pip0_smeared.P()*TMath::Cos(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTy = pip0_smeared.P()*TMath::Sin(phi_t_cross_product)*TMath::Sin(theta_t);
        double pipTz = pip0_smeared.P()*TMath::Cos(theta_t);

        TVector3 pipT(pipTx, pipTy, pipTz);


        phi_t_cross_product = phi_t_cross_product*TMath::RadToDeg();


        ///////////////   x Feynmann   ///////////////
        double xF_smeared = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W);


        // pT and phi from the rotated hadron momentum (measured in the CM frame - invarient of boost)
        double pT_smeared = sqrt(pipx_smeared*pipx_smeared + pipy_smeared*pipy_smeared);
        double phi_t_smeared = pip0_Clone.Phi()*TMath::RadToDeg();


        if(phi_t_smeared < 0){
            phi_t_smeared += 360;
        }





        //===================================================================================================================================//
        //----------------------------------------------//===================================//----------------------------------------------//
        //==============================================//          Smeared Binning          //==============================================//
        //----------------------------------------------//===================================//----------------------------------------------//
        //===================================================================================================================================//


        //===================================================================================//
        //=======================//          Q2-xB Binning          //=======================//
        //===================================================================================//

        double Q2_xB_Bin_smeared = 0;

        /////////////////////////       Bin 1       /////////////////////////
        if(xB_smeared > 0.0835 && xB_smeared < 0.15){
            // Border lines of Bin 1:
            //                 Upper Border:
            //                          Q2_smeared = ((2.28 - 1.3)/(0.15 - 0.0835))*(xB_smeared - 0.0835) + 1.3
            //                 Q2_smeared must be less than the equation above for Bin 1
            //
            //                 Lower Border:
            //                          Q2_smeared = ((1.30 - 1.30)/(0.12 - 0.0835))*(xB_smeared - 0.0835) + 1.30   (if xB_smeared < 0.12)
            //                          Q2_smeared = ((1.38 - 1.30)/(0.15 - 0.1200))*(xB_smeared - 0.1200) + 1.30   (if xB_smeared > 0.12)
            //                 Q2_smeared must be greater than the equations above for Bin 1

            int Condition_Up = 0;
            int Condition_Down = 0;
            // Both Condition_Up and Condition_Down should be met for Bin 1 to be confirmed.
            // Code will verify both conditions seperately before checking that they have been met.
            // If the condition has been met, its value will be set to 1.
            // If either is still 0 when checked, the event will be consided as being outside of Bin 1


            // Testing Upper Border of Bin 1
            if(Q2_smeared <= ((2.28 - 1.3)/(0.15 - 0.0835))*(xB_smeared - 0.0835) + 1.3){
                Condition_Up = 1; // Condition for upper border of Bin 1 has been met
            }

            // Testing Lower Border of Bin 1
            if(xB_smeared < 0.12){
                if(Q2_smeared >= ((1.30 - 1.30)/(0.12 - 0.0835))*(xB_smeared - 0.0835) + 1.30){
                    Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                }
            }
            if(xB_smeared > 0.12){
                if(Q2_smeared >= ((1.38 - 1.30)/(0.15 - 0.1200))*(xB_smeared - 0.1200) + 1.30){
                    Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                }
            }


            if(Condition_Up == 1 && Condition_Down == 1){
                Q2_xB_Bin_smeared = 1;
                // Bin 1 Confirmed
            }

        }
        /////////////////////////     End of Bin 1     /////////////////////////



        /////////////////////////       Bin 2 or 3       /////////////////////////
        if(xB_smeared > 0.15 && xB_smeared < 0.24){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2_smeared = ((2.75 - 1.98)/(0.24 - 0.15))*(xB_smeared - 0.15) + 1.98

            // Deciding between Bins
            if(Q2_smeared < ((2.75 - 1.98)/(0.24 - 0.15))*(xB_smeared - 0.15) + 1.98){
                BinTest = 2; // Event will NOT go to bin 3
            }

            if(Q2_smeared > ((2.75 - 1.98)/(0.24 - 0.15))*(xB_smeared - 0.15) + 1.98){
                BinTest = 3; // Event will NOT go to bin 2
            }


            // Final Border Test

            // Bin 2
            if(BinTest == 2){
                // Border lines of Bin 2:   Q2_smeared = ((1.45 - 1.38)/(0.20 - 0.15))*(xB_smeared - 0.15) + 1.38   (if xB_smeared < 0.2)
                //                          Q2_smeared = ((1.50 - 1.45)/(0.24 - 0.20))*(xB_smeared - 0.24) + 1.50   (if xB_smeared > 0.2)

                if(xB_smeared < 0.2){
                    if(Q2_smeared >= ((1.45 - 1.38)/(0.20 - 0.15))*(xB_smeared - 0.15) + 1.38){
                        Q2_xB_Bin_smeared = 2;
                        // Bin 2 Confirmed
                    }
                }

                if(xB_smeared > 0.2){
                    if(Q2_smeared >= ((1.50 - 1.45)/(0.24 - 0.20))*(xB_smeared - 0.24) + 1.50){
                        Q2_xB_Bin_smeared = 2;
                        // Bin 2 Confirmed
                    }
                }

            }
            // End of Bin 2


            // Bin 3
            if(BinTest == 3){
                // Border line of Bin 3:   Q2_smeared = ((3.625 - 2.28)/(0.24 - 0.15))*(xB_smeared - 0.15) + 2.28

                if(Q2_smeared <= ((3.625 - 2.28)/(0.24 - 0.15))*(xB_smeared - 0.15) + 2.28){
                    Q2_xB_Bin_smeared = 3;
                    // Bin 3 Confirmed
                }

            }
            // End of Bin 3


        }
        /////////////////////////     End of Bin 2 and 3     /////////////////////////



        /////////////////////////       Bin 4 or 5       /////////////////////////
        if(xB_smeared > 0.24 && xB_smeared < 0.34){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2_smeared = ((3.63 - 2.75)/(0.34 - 0.24))*(xB_smeared - 0.24) + 2.75

            // Deciding between Bins
            if(Q2_smeared < ((3.63 - 2.75)/(0.34 - 0.24))*(xB_smeared - 0.24) + 2.75){
                BinTest = 4; // Event will NOT go to bin 5
            }

            if(Q2_smeared > ((3.63 - 2.75)/(0.34 - 0.24))*(xB_smeared - 0.24) + 2.75){
                BinTest = 5; // Event will NOT go to bin 4
            }


            // Final Border Test

            // Bin 4
            if(BinTest == 4){
                // Border lines of Bin 4:   Q2_smeared = ((1.53 - 1.50)/(0.27 - 0.24))*(xB_smeared - 0.24) + 1.50   (if xB_smeared < 0.27)
                //                          Q2_smeared = ((1.56 - 1.53)/(0.30 - 0.27))*(xB_smeared - 0.27) + 1.53   (if 0.27 < xB_smeared < 0.30)
                //                          Q2_smeared = ((1.60 - 1.56)/(0.34 - 0.30))*(xB_smeared - 0.30) + 1.56   (if xB_smeared > 0.3)

                if(xB_smeared < 0.27){
                    if(Q2_smeared >= ((1.53 - 1.50)/(0.27 - 0.24))*(xB_smeared - 0.24) + 1.50){
                        Q2_xB_Bin_smeared = 4;
                        // Bin 4 Confirmed
                    }
                }

                if(xB_smeared > 0.27 && xB_smeared < 0.30){
                    if(Q2_smeared >= ((1.56 - 1.53)/(0.30 - 0.27))*(xB_smeared - 0.27) + 1.53){
                        Q2_xB_Bin_smeared = 4;
                        // Bin 4 Confirmed
                    }
                }

                if(xB_smeared > 0.30){
                    if(Q2_smeared >= ((1.60 - 1.56)/(0.34 - 0.30))*(xB_smeared - 0.30) + 1.56){
                        Q2_xB_Bin_smeared = 4;
                        // Bin 4 Confirmed
                    }
                }

            }
            // End of Bin 4


            // Bin 5
            if(BinTest == 5){
                // Border line of Bin 5:   Q2_smeared = ((5.12 - 3.625)/(0.34 - 0.24))*(xB_smeared - 0.24) + 3.625

                if(Q2_smeared <= ((5.12 - 3.625)/(0.34 - 0.24))*(xB_smeared - 0.24) + 3.625){
                    Q2_xB_Bin_smeared = 5;
                    // Bin 5 Confirmed
                }

            }
            // End of Bin 5


        }
        /////////////////////////     End of Bin 4 and 5     /////////////////////////



        /////////////////////////       Bin 6 or 7       /////////////////////////
        if(xB_smeared > 0.34 && xB_smeared < 0.45){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2_smeared = ((4.7 - 3.63)/(0.45 - 0.34))*(xB_smeared - 0.34) + 3.63

            // Deciding between Bins
            if(Q2_smeared < ((4.7 - 3.63)/(0.45 - 0.34))*(xB_smeared - 0.34) + 3.63){
                BinTest = 6; // Event will NOT go to bin 7
            }

            if(Q2_smeared > ((4.7 - 3.63)/(0.45 - 0.34))*(xB_smeared - 0.34) + 3.63){
                BinTest = 7; // Event will NOT go to bin 6
            }


            // Final Border Test

            // Bin 6
            if(BinTest == 6){
                // Border line of Bin 6:   Q2_smeared = ((2.52 - 1.60)/(0.45 - 0.34))*(xB_smeared - 0.34) + 1.60

                if(Q2_smeared >= ((2.52 - 1.60)/(0.45 - 0.34))*(xB_smeared - 0.34) + 1.60){
                    Q2_xB_Bin_smeared = 6;
                    // Bin 6 Confirmed
                }

            }
            // End of Bin 6


            // Bin 7
            if(BinTest == 7){
                // Border line of Bin 7:   Q2_smeared = ((6.76 - 5.12)/(0.45 - 0.34))*(xB_smeared - 0.34) + 5.12

                if(Q2_smeared <= ((6.76 - 5.12)/(0.45 - 0.34))*(xB_smeared - 0.34) + 5.12){
                    Q2_xB_Bin_smeared = 7;
                    // Bin 7 Confirmed
                }

            }
            // End of Bin 7


        }
        /////////////////////////     End of Bin 6 and 7     /////////////////////////



        /////////////////////////       Bin 8 or 9       /////////////////////////
        if(xB_smeared > 0.45){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2_smeared = ((7.42 - 4.70)/(0.708 - 0.45))*(xB_smeared - 0.45) + 4.70    

            // Deciding between Bins
            if(Q2_smeared < ((7.42 - 4.70)/(0.708 - 0.45))*(xB_smeared - 0.45) + 4.70){
                BinTest = 8; // Event will NOT go to bin 9
            }
            if(Q2_smeared > ((7.42 - 4.70)/(0.708 - 0.45))*(xB_smeared - 0.45) + 4.70){
                BinTest = 9; // Event will NOT go to bin 8
            }


            // Final Border Test

            // Bin 8
            if(BinTest == 8){
                // Border lines of Bin 8:   Q2_smeared = ((3.05 - 2.52)/(0.500 - 0.45))*(xB_smeared - 0.45) + 2.52   (if xB_smeared < 0.50)
                //                          Q2_smeared = ((4.05 - 3.05)/(0.570 - 0.50))*(xB_smeared - 0.50) + 3.05   (if 0.50 < xB_smeared < 0.57)
                //                          Q2_smeared = ((5.40 - 4.05)/(0.640 - 0.57))*(xB_smeared - 0.57) + 4.05   (if 0.57 < xB_smeared < 0.64)
                //                          Q2_smeared = ((7.42 - 5.40)/(0.708 - 0.64))*(xB_smeared - 0.64) + 5.40   (if xB_smeared > 0.64)

                if(xB_smeared < 0.50){
                    if(Q2_smeared >= ((3.05 - 2.52)/(0.500 - 0.45))*(xB_smeared - 0.45) + 2.52){
                        Q2_xB_Bin_smeared = 8;
                        // Bin 8 Confirmed
                    }
                }

                if(xB_smeared > 0.50 && xB_smeared < 0.57){
                    if(Q2_smeared >= ((4.05 - 3.05)/(0.570 - 0.50))*(xB_smeared - 0.50) + 3.05){
                        Q2_xB_Bin_smeared = 8;
                        // Bin 8 Confirmed
                    }
                }

                if(xB_smeared > 0.57 && xB_smeared < 0.64){
                    if(Q2_smeared >= ((5.40 - 4.05)/(0.640 - 0.57))*(xB_smeared - 0.57) + 4.05){
                        Q2_xB_Bin_smeared = 8;
                        // Bin 8 Confirmed
                    }
                }

                if(xB_smeared > 0.64){
                    if(Q2_smeared >= ((7.42 - 5.40)/(0.708 - 0.64))*(xB_smeared - 0.64) + 5.40){
                        Q2_xB_Bin_smeared = 8;
                        // Bin 8 Confirmed
                    }
                }

            }
            // End of Bin 8


            // Bin 9
            if(BinTest == 9){
                // Border lines of Bin 9:
                //                 Uppermost Border:
                //                          Q2_smeared = ((10.185 -  6.760)/(0.6770 - 0.450))*(xB_smeared - 0.450) +  6.760   (if xB_smeared < 0.677)
                //                          Q2_smeared = ((11.351 - 10.185)/(0.7896 - 0.677))*(xB_smeared - 0.677) + 10.185   (if xB_smeared > 0.677)
                //                 Q2_smeared must be less than the equations above for Bin 9
                //
                //                 Rightmost Border:
                //                          Q2_smeared =  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB_smeared - 0.708) + 7.42   (if xB_smeared < 0.75)
                //                          Q2_smeared = ((11.351 - 9.52)/(0.7896 - 0.750))*(xB_smeared - 0.750) + 9.52   (if xB_smeared > 0.75)
                //                 Q2_smeared must be greater than the equations above for Bin 9

                int Condition_Up = 0;
                int Condition_Right = 0;
                // Both Condition_Up and Condition_Right should be met for Bin 9 to be confirmed.
                // Code will verify both conditions seperately before checking that they have been met.
                // If the condition has been met, its value will be set to 1.
                // If either is still 0 when checked, the event will be consided as being outside of Bin 9


                // Testing Uppermost Border of Bin 9
                if(xB_smeared < 0.677){
                    if(Q2_smeared <= ((10.185 -  6.760)/(0.6770 - 0.450))*(xB_smeared - 0.450) +  6.760){
                        Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                    }
                }
                if(xB_smeared > 0.677){
                    if(Q2_smeared <= ((11.351 - 10.185)/(0.7896 - 0.677))*(xB_smeared - 0.677) + 10.185){
                        Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                    }
                }

                // Testing Rightmost Border of Bin 9
                if(xB_smeared < 0.75){
                    if(Q2_smeared >=  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB_smeared - 0.708) + 7.42){
                        Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                    }
                }
                if(xB_smeared > 0.75){
                    if(Q2_smeared >= ((11.351 - 9.52)/(0.7896 - 0.750))*(xB_smeared - 0.750) + 9.52){
                        Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                    }
                }


                if(Condition_Up == 1 && Condition_Right == 1){
                    Q2_xB_Bin_smeared = 9;
                    // Bin 9 Confirmed
                }

            }
            // End of Bin 9

        }
        /////////////////////////     End of Bin 8 and 9     /////////////////////////



        //==================================================================================//
        //=======================//      End of Q2-xB Binning      //=======================//
        //=======================//================================//=======================//
        //=======================//          z-pT Binning          //=======================//
        //==================================================================================//



        double z_pT_Bin_smeared = 0;
        int Num_z_Borders = 0;
        int Num_pT_Borders = 0;


        /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

        auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
        {

            // z_or_pT = 0 corresponds to z bins
            // z_or_pT = 1 corresponds to pT bins

            // For Q2_xB Bin 1
            if(Q2_xB_Bin_Num == 1){
                float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 2
            if(Q2_xB_Bin_Num == 2){
                float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 3
            if(Q2_xB_Bin_Num == 3){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 4
            if(Q2_xB_Bin_Num == 4){
                float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 5
            if(Q2_xB_Bin_Num == 5){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 6
            if(Q2_xB_Bin_Num == 6){
                float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 7
            if(Q2_xB_Bin_Num == 7){
                float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 8
            if(Q2_xB_Bin_Num == 8){
                float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 9
            if(Q2_xB_Bin_Num == 9){
                float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }


            // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
            // return empty_Borders;
            float empty = 0;
            return empty;
        };


        /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////


        // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

        // For Q2_xB Bin 0
        if(Q2_xB_Bin_smeared== 0){
            z_pT_Bin_smeared = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
            Num_z_Borders = 0;
            Num_pT_Borders = 0;
        }
        // For Q2_xB Bin 1
        if(Q2_xB_Bin_smeared== 1){
            // float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 2
        if(Q2_xB_Bin_smeared== 2){
            // float z_Borders[]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 3
        if(Q2_xB_Bin_smeared== 3){
            // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 4
        if(Q2_xB_Bin_smeared== 4){
            // float z_Borders[]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
            Num_z_Borders = 7;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 5
        if(Q2_xB_Bin_smeared== 5){
            // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 6
        if(Q2_xB_Bin_smeared== 6){
            // float z_Borders[]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};
            Num_pT_Borders = 6;
        }
        // For Q2_xB Bin 7
        if(Q2_xB_Bin_smeared== 7){
            // float z_Borders[]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
            Num_z_Borders = 7;
            // float pT_Borders[] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};
            Num_pT_Borders = 7;
        }
        // For Q2_xB Bin 8
        if(Q2_xB_Bin_smeared== 8){
            // float z_Borders[]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.23, 0.34, 0.45, 0.70};
            Num_pT_Borders = 5;
        }
        // For Q2_xB Bin 9
        if(Q2_xB_Bin_smeared== 9){
            // float z_Borders[]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};
            Num_pT_Borders = 6;
        }

        if(Num_z_Borders == 0){
            // float  z_Borders[1]  = {0};
            Num_z_Borders = 1;
            // float  pT_Borders[1] = {0};
            Num_pT_Borders = 1;
        }


        int z_pT_Bin_smeared_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                // based on the number of times the loop has run

        // Determining z_pT Bins
        for(int zbin = 1; zbin < Num_z_Borders; zbin++){
            if(z_pT_Bin_smeared != 0){
                continue;   // If the bin has already been assigned, this line will end the loop.
                            // This is to make sure the loop does not run longer than what is necessary.
            }    

            if(z_smeared > Borders_function(Q2_xB_Bin_smeared, 0, zbin) && z_smeared < Borders_function(Q2_xB_Bin_smeared, 0, zbin - 1)){
                // Found the correct z bin

                for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                    if(z_pT_Bin_smeared != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                    if(pT_smeared > Borders_function(Q2_xB_Bin_smeared, 1, pTbin) && pT_smeared < Borders_function(Q2_xB_Bin_smeared, 1, pTbin+1)){
                        // Found the correct pT bin
                        z_pT_Bin_smeared = z_pT_Bin_smeared_count; // The value of the z_pT_Bin_smeared has been set
                        break;
                    }
                    else{
                        z_pT_Bin_smeared_count += 1; // Checking the next bin
                    }
                }

            }
            else{
                z_pT_Bin_smeared_count += (Num_pT_Borders - 1);
                // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                // This represents checking each pT bin for the given z bin without going through each entry in the loop.
            }    
        }



        //===================================================================================//
        //=======================//       End of z-pT Binning       //=======================//
        //===================================================================================//



        //==================================================================================================================================//
        //----------------------------------------------//==================================//----------------------------------------------//
        //==============================================//      End of Smeared Binning      //==============================================//
        //----------------------------------------------//==================================//----------------------------------------------//
        //==================================================================================================================================//



        // std::vector<double> smeared_vals = {epipX.M(), epipX.M2(), Q2_smeared, xB_smeared, v_smeared, W2_smeared, W_smeared, y_smeared, z_smeared, epsilon_smeared, pT_smeared, phi_t_smeared, xF_smeared, pipx_smeared, pipy_smeared, pipz_smeared, qx_smeared, qy_smeared, qz_smeared, beamx_smeared, beamy_smeared, beamz_smeared, elex_smeared, eley_smeared, elez_smeared, Q2_xB_Bin_smeared, z_pT_Bin_smeared, ele_E_smeared, pip0_E_smeared, el_smeared, pip_smeared, elth_smeared, pipth_smeared, elPhi_smeared, pipPhi_smeared};


        std::vector<double> smeared_vals = {epipX.M(), epipX.M2(), Q2_smeared, xB_smeared, v_smeared, W2_smeared, W_smeared, y_smeared, z_smeared, epsilon_smeared, pT_smeared, phi_t_smeared, xF_smeared, Q2_xB_Bin_smeared, z_pT_Bin_smeared, el_smeared, ele_E_smeared, elth_smeared, elPhi_smeared, pip_smeared, pip0_E_smeared, pipth_smeared, pipPhi_smeared, Delta_Smear_El_P, Delta_Smear_El_Th, Delta_Smear_El_Phi, Delta_Smear_Pip_P, Delta_Smear_Pip_Th, Delta_Smear_Pip_Phi};
        //                  smeared_vals = {    1    ,     2     ,      3    ,      4    ,     5    ,      6    ,     7    ,     8    ,     9    ,        10      ,     11    ,        12    ,     13    ,        14        ,       15        ,     16    ,       17     ,       18    ,        19    ,      20    ,        21     ,        22    ,         23    ,      24         ,      25          ,      26           ,      27          ,      28           ,      29            };

        return smeared_vals;

        """]))

        # Data_Frame_Clone = Data_Frame_Clone.Define('Q2_xB_Bin_smeared', 'smeared_vals[13]')
        # Data_Frame_Clone = Data_Frame_Clone.Define('z_pT_Bin_smeared', 'smeared_vals[14]')
        rdf = rdf.Define('Q2_xB_Bin_smeared', 'smeared_vals[13]')
        rdf = rdf.Define('z_pT_Bin_smeared', 'smeared_vals[14]')

        rdf = rdf.Define('Q2_xB_Bin_2_smeared', '''
            int Q2_xB_Bin_2_smeared = Q2_xB_Bin_smeared;

            if(Q2_xB_Bin_smeared > 1 && Q2_xB_Bin_2_smeared%2 != 0){
                Q2_xB_Bin_2_smeared += -2;
            }

            if(smeared_vals[2] < 2){
            // if(Q2_smeared < 2){
                Q2_xB_Bin_2_smeared = 0; 
            }

            return Q2_xB_Bin_2_smeared;
        ''')


        rdf = rdf.Define('z_pT_Bin_2_smeared', '''

            double z_smeared = smeared_vals[8];
            double pT_smeared = smeared_vals[10];

            auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
            {
                // z_or_pT = 0 corresponds to z bins
                // z_or_pT = 1 corresponds to pT bins

                // For Q2_xB Bin 1 (was 3 in old scheme)
                if(Q2_xB_Bin_Num == 1){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 2
                if(Q2_xB_Bin_Num == 2){
                    float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 3 (was 5 in old scheme)
                if(Q2_xB_Bin_Num == 3){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 4
                if(Q2_xB_Bin_Num == 4){
                    float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[6 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 5 (was 7 in old scheme)
                if(Q2_xB_Bin_Num == 5){
                    float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                    float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[6 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }    
                // For Q2_xB Bin 6
                if(Q2_xB_Bin_Num == 6){
                    float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                    float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                    if(z_or_pT == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 7 (was 9 in old scheme)
                if(Q2_xB_Bin_Num == 7){
                    float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                    float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                    if(z_or_pT == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 8
                if(Q2_xB_Bin_Num == 8){
                    float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                    float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};

                    if(z_or_pT == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }



                // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
                // return empty_Borders;
                float empty = 0;
                return empty;
            };


            /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////


            // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

            // Default:
            int Num_z_Borders = 8;
            int Num_pT_Borders = 8;
            int z_pT_Bin_2_smeared = 0;

            // For Q2_xB Bin 0
            if(Q2_xB_Bin_2_smeared == 0){
                z_pT_Bin_2_smeared = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
                Num_z_Borders = 0; Num_pT_Borders = 0;
            }
            // For Q2_xB Bin 1 (Uses Default for both borders)

            // For Q2_xB Bin 2 (Uses Default for both borders)

            // For Q2_xB Bin 3 (Uses Default for both borders)

            // For Q2_xB Bin 4 (Uses Default for pT borders)
            if(Q2_xB_Bin_2_smeared == 4){
                Num_z_Borders = 7;
            }

            // For Q2_xB Bin 5 (New scheme)
            if(Q2_xB_Bin_2_smeared == 5){
                Num_z_Borders = 7; Num_pT_Borders = 7;
            }

            // For Q2_xB Bin 6
            if(Q2_xB_Bin_2_smeared == 6){
                Num_z_Borders = 6; Num_pT_Borders = 6;
            }

            // For Q2_xB Bin 7 (New scheme)
            if(Q2_xB_Bin_2_smeared == 7){
                Num_z_Borders = 6; Num_pT_Borders = 6;
            }

            // For Q2_xB Bin 8
            if(Q2_xB_Bin_2_smeared == 8){
                Num_z_Borders = 6; Num_pT_Borders = 5;
            }

            if(Num_z_Borders == 0){
                Num_z_Borders = 1; Num_pT_Borders = 1;
            }


            int z_pT_Bin_2_smeared_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                    // based on the number of times the loop has run

            // Determining z_pT Bins
            for(int zbin = 1; zbin < Num_z_Borders; zbin++){
                if(z_pT_Bin_2_smeared != 0){
                    continue;   // If the bin has already been assigned, this line will end the loop.
                                // This is to make sure the loop does not run longer than what is necessary.
                }    

                if(z_smeared > Borders_function(Q2_xB_Bin_2_smeared, 0, zbin) && z_smeared < Borders_function(Q2_xB_Bin_2_smeared, 0, zbin - 1)){
                    // Found the correct z bin

                    for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                        if(z_pT_Bin_2_smeared != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                        if(pT_smeared > Borders_function(Q2_xB_Bin_2_smeared, 1, pTbin) && pT_smeared < Borders_function(Q2_xB_Bin_2_smeared, 1, pTbin+1)){
                            // Found the correct pT bin
                            z_pT_Bin_2_smeared = z_pT_Bin_2_smeared_count; // The value of the z_pT_Bin_2_smeared has been set
                            // cout<<"The value of the z_pT_Bin_2_smeared has been set as: "<<z_pT_Bin_2_smeared<<endl;
                            break;
                        }
                        else{
                            z_pT_Bin_2_smeared_count += 1; // Checking the next bin
                            // cout<<"Checking the next bin"<<endl;
                        }
                    }

                }
                else{
                    z_pT_Bin_2_smeared_count += (Num_pT_Borders - 1);
                    // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                    // This represents checking each pT bin for the given z bin without going through each entry in the loop.
                }    
            }

            return z_pT_Bin_2_smeared;

        ''')

        
        
        ##==================================================##
        ##==========## End of Smeared DataFrame ##==========##
        ##==================================================##
        
        
        

    def smear_frame_compatible(Data_Frame, Variable, Smearing_Q):
        
        if("smear" not in Smearing_Q or (datatype not in ["mdf", "pdf"]) or (str(Variable) in Data_Frame.GetColumnNames())):
            # Variable should already be defined/cannot smear real/generated data
            
            # if(str(Variable) in Data_Frame.GetColumnNames()):
            #     print("".join(["Already defined: ", str(Variable)]))
            
            return Data_Frame
        
        else:

            done_Q = 'no'
            
            if('MM' == Variable or 'MM_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('MM_smeared', 'smeared_vals[0]')

            if('MM2' == Variable or 'MM2_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('MM2_smeared', 'smeared_vals[1]')

            if('Q2' == Variable or 'Q2_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('Q2_smeared', 'smeared_vals[2]')

            if('xB' == Variable or 'xB_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('xB_smeared', 'smeared_vals[3]')

            if('v' == Variable or 'v_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('v_smeared', 'smeared_vals[4]')

            if('s' == Variable or 's_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('s_smeared', 'smeared_vals[5]')

            if('W' == Variable or 'W_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('W_smeared', 'smeared_vals[6]')

            if('y' == Variable or 'y_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('y_smeared', 'smeared_vals[7]')

            if('z' == Variable or 'z_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('z_smeared', 'smeared_vals[8]')

            if('epsilon' == Variable or 'epsilon_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('epsilon_smeared', 'smeared_vals[9]')

            if('pT' == Variable or 'pT_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pT_smeared', 'smeared_vals[10]')

            if('phi_t' == Variable or 'phi_t_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('phi_t_smeared', 'smeared_vals[11]')

            if('xF' == Variable or 'xF_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('xF_smeared', 'smeared_vals[12]')

            if('el' == Variable or 'el_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('el_smeared', 'smeared_vals[15]')

            if('el_E' == Variable or 'el_E_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('el_E_smeared', 'smeared_vals[16]')

            if('elth' == Variable or 'elth_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('elth_smeared', 'smeared_vals[17]')

            if('elPhi' == Variable or 'elPhi_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('elPhi_smeared', 'smeared_vals[18]')

            if('pip' == Variable or 'pip_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pip_smeared', 'smeared_vals[19]')

            if('pip_E' == Variable or 'pip_E_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pip_E_smeared', 'smeared_vals[20]')

            if('pipth' == Variable or 'pipth_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pipth_smeared', 'smeared_vals[21]')

            if('pipPhi' == Variable or 'pipPhi_smeared' == Variable):
                done_Q = 'yes'
                return Data_Frame.Define('pipPhi_smeared', 'smeared_vals[22]')

            if('Delta_Smear_El_P' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[23]')
            
            if('Delta_Smear_El_Th' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[24]')
            
            if('Delta_Smear_El_Phi' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[25]')
            
            if('Delta_Smear_Pip_P' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[26]')
            
            if('Delta_Smear_Pip_Th' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[27]')
            
            if('Delta_Smear_Pip_Phi' in Variable):
                done_Q = 'yes'
                return Data_Frame.Define(str(Variable), 'smeared_vals[28]')


            if(done_Q != 'yes'):
                # Failed to get a new definition
                return Data_Frame
            
        
    
    
    ##=========================================================================================================##
    ##---------------------------------##===================================##---------------------------------##
    ##=================================##     End of Smearing Functions     ##=================================##
    ##---------------------------------##===================================##---------------------------------##
    ##=========================================================================================================##
    
    
    
    ##==========================================================================================================##
    ##---------------------------------##====================================##---------------------------------##
    ##=================================##   ∆P from Exclusive Calculations   ##=================================##
    ##---------------------------------##====================================##---------------------------------##
    ##==========================================================================================================##
    

    ########################################################################################
    ####================================================================================####
    ##==========##==========##      ∆P Calculations (Normal)      ##==========##==========##
    ####================================================================================####
    ########################################################################################


    rdf = rdf.Define("Delta_Pel_Cors", "".join([str(Correction_Code_Full_In), """

        auto fe = dppC(ex, ey, ez, esec, 0, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = 10.6041;
        // Defined by the run group/data set

        double neutronM2 = 0.9396*0.9396;

        // Below are the kinematic calculations of the electron momentum (from el+pro->el+Pip+N) based on the assumption that the electron angle and π+ reconstruction were measured by the detector correctly for elastic events in the epipX channel
        // (The neutron is used as the "missing" particle)

        auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
            // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"
        auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
            // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"
        auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
            // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

        auto pel_Calculated = (termA + termC)/termB;

        auto Delta_Pel_Cors = pel_Calculated - eleC.P();

        return Delta_Pel_Cors;

    """]))


    rdf = rdf.Define("Delta_Ppip_Cors", "".join([str(Correction_Code_Full_In), """

        auto fe = dppC(ex, ey, ez, esec, 0, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = 10.6041;
        // Defined by the run group/data set

        double neutronM2 = 0.9396*0.9396;


        // Below are the kinematic calculations of the π+ momentum (from el+pro->el+Pip+N) based on the assumption that the π+ angle and electron reconstruction were measured by the detector correctly for elastic events in the epipX channel
        // (The neutron is used as the "missing" particle)

        auto termA = (neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2;
        auto termB = 0.938*(Beam_Energy - eleC.P()) - Beam_Energy*eleC.P()*(1 - cos(eleC.Theta()));
        auto termC = ((eleC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC))) - (Beam_Energy*cos(pipC.Theta())));

        auto sqrtTerm = ((termA - termB)*(termA - termB)) + (0.13957*0.13957)*((termC*termC) - ((0.938 + Beam_Energy - eleC.P())*(0.938 + Beam_Energy - eleC.P())));
        auto denominator = ((0.938 + Beam_Energy - eleC.P()) + termC)*((0.938 + Beam_Energy - eleC.P()) - termC);
        auto numeratorP = (termA - termB)*termC + (0.938 + Beam_Energy - eleC.P())*sqrt(sqrtTerm);
        auto numeratorM = (termA - termB)*termC - (0.938 + Beam_Energy - eleC.P())*sqrt(sqrtTerm);

        auto pip_CalculateP = numeratorP/denominator;
        auto pip_CalculateM = numeratorM/denominator;

        auto pip_Calculate = pip_CalculateP;

        if(abs(pipC.P() - pip_CalculateP) >= abs(pipC.P() - pip_CalculateM)){
            pip_Calculate = pip_CalculateM;
        }
        if(abs(pipC.P() - pip_CalculateP) <= abs(pipC.P() - pip_CalculateM)){
            pip_Calculate = pip_CalculateP;
        }

        auto Delta_Ppip_Cors = pip_Calculate - pipC.P();

        return Delta_Ppip_Cors;

    """]))
    

    ############################################################################################
    ####====================================================================================####
    ##==========##==========##      ∆Theta Calculations (Normal)      ##==========##==========##
    ####====================================================================================####
    ############################################################################################


    rdf = rdf.Define("Delta_Theta_el_Cors", "".join([str(Correction_Code_Full_In), """

        auto fe = dppC(ex, ey, ez, esec, 0, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = 10.6041;
        // Defined by the run group/data set

        double neutronM2 = 0.9396*0.9396;

        auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
            // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"
        
        // auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
        //     // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"
            
        auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy - 0.938;
            // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy" - "Proton Mass"
            
        auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
            // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

        auto Theta_el_Calculated = acos((1/Beam_Energy)*(((termA + termC)/eleC.P()) - termB));

        auto Delta_Theta_el_Cors = (180/3.1415926)*(Theta_el_Calculated - eleC.Theta());

        return Delta_Theta_el_Cors;

    """]))


    rdf = rdf.Define("Delta_Theta_pip_Cors",  "".join([str(Correction_Code_Full_In), """

        auto fe = dppC(ex, ey, ez, esec, 0, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;
        auto fpip = dppC(pipx, pipy, pipz, pipsec, 1, """, "0" if(Mom_Correction_Q != "yes") else "1", """) + 1;

        auto eleC = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pipC = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto Beam_Energy = 10.6041;
        // Defined by the run group/data set

        double neutronM2 = 0.9396*0.9396;

        auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
            // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"
        
        auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
            // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"
            
        // auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
        //     // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"
        
        auto termC = Beam_Energy*pipC.E() + 0.938*pipC.E();
            // termC --> "Initial Electron Beam Energy"*"π+ Energy" + "Proton Mass"*"π+ Energy"

        auto Theta_pip_Calculated = acos((termA + termC - termB*eleC.P())/(Beam_Energy*pipC.P()));

        auto Delta_Theta_pip_Cors = (180/3.1415926)*(Theta_pip_Calculated - pipC.Theta());

        return Delta_Theta_pip_Cors;

    """]))

    

    ###############################################################################################
    ####=======================================================================================####
    ##==========##==========##         ∆P Calculations (Smeared)         ##==========##==========##
    ####=======================================================================================####
    ###############################################################################################

    if("rdf" not in datatype and "gdf" not in datatype):

        rdf = rdf.Define("Delta_Pel_Cors_smeared", "".join([str(smearing_function), """

            auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

            TLorentzVector ele(ex, ey, ez, eleM.E());
            TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());

            TLorentzVector ele_smeared  = smear_func(ele""", (");"  if("ivec" not in str(smearing_function)) else ", 0);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = 10.6041;
            // Defined by the run group/data set

            double neutronM2 = 0.9396*0.9396;

            // Below are the kinematic calculations of the electron momentum (from el+pro->el+Pip+N) based on the assumption that the electron angle and π+ reconstruction were measured by the detector correctly for elastic events in the epipX channel
            // (The neutron is used as the "missing" particle)

            auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
                // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"
            auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
                // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"
            auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
                // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

            auto pel_Calculated = (termA + termC)/termB;

            auto Delta_Pel_Cors_smeared = pel_Calculated - eleC.P();

            return Delta_Pel_Cors_smeared;

        """]))


        rdf = rdf.Define("Delta_Ppip_Cors_smeared", "".join([str(smearing_function), """

            auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

            TLorentzVector ele(ex, ey, ez, eleM.E());
            TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());

            TLorentzVector ele_smeared  = smear_func(ele""", (");"  if("ivec" not in str(smearing_function)) else ", 0);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());


            auto Beam_Energy = 10.6041;
            // Defined by the run group/data set

            double neutronM2 = 0.9396*0.9396;


            // Below are the kinematic calculations of the π+ momentum (from el+pro->el+Pip+N) based on the assumption that the π+ angle and electron reconstruction were measured by the detector correctly for elastic events in the epipX channel
            // (The neutron is used as the "missing" particle)

            auto termA = (neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2;
            auto termB = 0.938*(Beam_Energy - eleC.P()) - Beam_Energy*eleC.P()*(1 - cos(eleC.Theta()));
            auto termC = ((eleC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC))) - (Beam_Energy*cos(pipC.Theta())));

            auto sqrtTerm = ((termA - termB)*(termA - termB)) + (0.13957*0.13957)*((termC*termC) - ((0.938 + Beam_Energy - eleC.P())*(0.938 + Beam_Energy - eleC.P())));
            auto denominator = ((0.938 + Beam_Energy - eleC.P()) + termC)*((0.938 + Beam_Energy - eleC.P()) - termC);
            auto numeratorP = (termA - termB)*termC + (0.938 + Beam_Energy - eleC.P())*sqrt(sqrtTerm);
            auto numeratorM = (termA - termB)*termC - (0.938 + Beam_Energy - eleC.P())*sqrt(sqrtTerm);

            auto pip_CalculateP = numeratorP/denominator;
            auto pip_CalculateM = numeratorM/denominator;

            auto pip_Calculate = pip_CalculateP;

            if(abs(pipC.P() - pip_CalculateP) >= abs(pipC.P() - pip_CalculateM)){
                pip_Calculate = pip_CalculateM;
            }
            if(abs(pipC.P() - pip_CalculateP) <= abs(pipC.P() - pip_CalculateM)){
                pip_Calculate = pip_CalculateP;
            }

            auto Delta_Ppip_Cors_smeared = pip_Calculate - pipC.P();

            return Delta_Ppip_Cors_smeared;

        """]))
    

        ############################################################################################
        ####====================================================================================####
        ##==========##==========##      ∆Theta Calculations (Smeared)      ##==========##==========##
        ####====================================================================================####
        ############################################################################################


        rdf = rdf.Define("Delta_Theta_el_Cors_smeared", "".join([str(smearing_function), """

            auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

            TLorentzVector ele(ex, ey, ez, eleM.E());
            TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());

            TLorentzVector ele_smeared  = smear_func(ele""", (");"  if("ivec" not in str(smearing_function)) else ", 0);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = 10.6041;
            // Defined by the run group/data set

            double neutronM2 = 0.9396*0.9396;

            auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
                // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"

            // auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
            //     // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"

            auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy - 0.938;
                // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy" - "Proton Mass"

            auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
                // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

            auto Theta_el_Calculated_smeared = acos((1/Beam_Energy)*(((termA + termC)/eleC.P()) - termB));

            auto Delta_Theta_el_Cors_smeared = (180/3.1415926)*(Theta_el_Calculated_smeared - eleC.Theta());

            return Delta_Theta_el_Cors_smeared;

        """]))


        rdf = rdf.Define("Delta_Theta_pip_Cors_smeared",  "".join([str(smearing_function),  """

            auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
            auto pip0M = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);

            TLorentzVector ele(ex, ey, ez, eleM.E());
            TLorentzVector pip0(pipx, pipy, pipz, pip0M.E());

            TLorentzVector ele_smeared  = smear_func(ele""", (");"  if("ivec" not in str(smearing_function)) else ", 0);"), """
            TLorentzVector pip0_smeared = smear_func(pip0""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """

            auto eleC = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), ele_smeared.M());
            auto pipC = ROOT::Math::PxPyPzMVector(pip0_smeared.X(), pip0_smeared.Y(), pip0_smeared.Z(), pip0_smeared.M());

            auto Beam_Energy = 10.6041;
            // Defined by the run group/data set

            double neutronM2 = 0.9396*0.9396;

            auto termA = ((neutronM2 - (0.938*0.938) - (0.13957*0.13957))/2) - 0.938*Beam_Energy;
                // termA --> (("Neutron Mass Squared" - "Proton Mass Squared" - "π+ Mass Squared")/2) - "Proton Mass"*"Initial Electron Beam Energy"

            auto termB = pipC.E() - pipC.P()*cos(ROOT::Math::VectorUtil::Angle(eleC, pipC)) - Beam_Energy*(1 - cos(eleC.Theta())) - 0.938;
                // termB --> "π+ Energy" - "π+ Momentum"*cos("Angle between Electron and π+") - "Initial Electron Beam Energy"*(1 - cos("Electron Theta")) - "Proton Mass"

            // auto termC = Beam_Energy*(pipC.E() - pipC.P()*cos(pipC.Theta())) + 0.938*pipC.E();
            //     // termC --> "Initial Electron Beam Energy"*("π+ Energy" - "π+ Momentum"*cos("π+ Theta")) + "Proton Mass"*"π+ Energy"

            auto termC = Beam_Energy*pipC.E() + 0.938*pipC.E();
                // termC --> "Initial Electron Beam Energy"*"π+ Energy" + "Proton Mass"*"π+ Energy"

            auto Theta_pip_Calculated_smeared = acos((termA + termC - termB*eleC.P())/(Beam_Energy*pipC.P()));

            auto Delta_Theta_pip_Cors_smeared = (180/3.1415926)*(Theta_pip_Calculated_smeared - pipC.Theta());

            return Delta_Theta_pip_Cors_smeared;

        """]))





    


    
    
    print("Kinematic Variables have been calculated.")
    ###################################################################################################################################################################
    ###################################################       Done with Calculating (All) Kinematic Variables       ###################################################
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###----------------------------------------------##-------------------------------------------------------------##----------------------------------------------###
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###################################################                  Making Cuts to DataFrames                  ###################################################
    ###################################################################################################################################################################


    
    def filter_Valerii(Data_Frame, Valerii_Cut):
        
        if("Valerii_Cut" in Valerii_Cut):

            Data_Frame_Clone = Data_Frame.Filter("""

                auto func = [&](double x, double k, double b)
                {
                    return k * x + b;
                };

                struct line{
                    double k;
                    double b;
                };

                auto isOutOfLines = [&](double x, double y, line topLine, line botLine)
                {
                    return y > func(x, topLine.k, topLine.b) || y < func(x, botLine.k, botLine.b);
                };

                // bool BadElementKnockOut(double hx, double hy, int sector, int cutLevel);     

                auto BadElementKnockOut = [&](double hx, double hy, int sector, int cutLevel)
                {

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


                return BadElementKnockOut(Hx, Hy, esec, 1);

                """)

            return Data_Frame_Clone
        
        else:
            return Data_Frame
    
    
    
    # Meant for the exclusive ep->eπ+(N) reaction
    def Calculated_Exclusive_Cuts(Smear_Q):
        output = "".join(["""
        
        """, str(smearing_function), """

        auto beam = ROOT::Math::PxPyPzMVector(0, 0, 10.6041, 0);
        auto targ = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938);
        auto ele = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto pip0 = ROOT::Math::PxPyPzMVector(pipx, pipy, pipz, 0.13957);
        
        """, """
        
        TLorentzVector eleS(ex, ey, ez, ele.E());
        TLorentzVector pipS(pipx, pipy, pipz, pip0.E());
        
        TLorentzVector ele_smeared = smear_func(eleS""", (");" if("ivec" not in str(smearing_function)) else ", 0);"), """
        TLorentzVector pip_smeared = smear_func(pipS""", (");" if("ivec" not in str(smearing_function)) else ", 1);"), """
        
        ele  = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), 0);
        pip0 = ROOT::Math::PxPyPzMVector(pip_smeared.X(), pip_smeared.Y(), pip_smeared.Z(), 0.13957);
        
        """ if("smear" in Smear_Q) else "", """

        auto MM_Vector = beam + targ - ele - pip0;

        // double elPhi = (180/3.1415926)*atan2(ey, ex);
        auto elPhi_cut = (180/3.1415926)*ele.Phi();

        if(((esec == 4 || esec == 3) && elPhi_cut < 0) || (esec > 4 && elPhi_cut < 90)){
            elPhi_cut += 360;
        }
        double localelPhiS = (elPhi_cut - (esec - 1)*60) - (30/ele.P());

        auto cut_up = 1.1;
        auto cut_down = 0;

        if(esec == 1){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up = (-0.002512)*ele.P() + (1.025113);  
                cut_down = (-0.006564)*ele.P() + (0.91629);
            }
            if(localelPhiS < -5){
                cut_up = (-0.002166)*ele.P() + (1.047257);
                cut_down = (-0.00436)*ele.P() + (0.919216);
            }
            if(localelPhiS > 5){
                cut_up = (-0.006649)*ele.P() + (1.036503);
                cut_down = (-0.008246)*ele.P() + (0.899835);
            }
        }
        if(esec == 2){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up = (-0.001108)*ele.P() + (1.012364);
                cut_down = (-0.004842)*ele.P() + (0.894447);
            }

            if(localelPhiS < -5){
                cut_up = (-0.000811)*ele.P() + (1.015682);
                cut_down = (-0.004621)*ele.P() + (0.898917);
            }

            if(localelPhiS > 5){
                cut_up = (-0.006132)*ele.P() + (1.03695);
                cut_down = (-0.009834)*ele.P() + (0.915225);
            }
        }
        if(esec == 3){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up = (-0.00808)*ele.P() + (1.053207);
                cut_down = (-0.014113)*ele.P() + (0.937174);
            }
            if(localelPhiS < -5){
                cut_up = (-0.011922)*ele.P() + (1.066027);
                cut_down = (-0.014898)*ele.P() + (0.925886);
            }
            if(localelPhiS > 5){
                cut_up = (-0.008165)*ele.P() + (1.06216);
                cut_down = (-0.009607)*ele.P() + (0.913684);
            }
        }
        if(esec == 4){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up = (-0.003636)*ele.P() + (1.040308);
                cut_down = (-0.006253)*ele.P() + (0.919061);
            }
            if(localelPhiS < -5){
                cut_up = (-0.004512)*ele.P() + (1.036327);
                cut_down = (-0.003965)*ele.P() + (0.88969);
            }
            if(localelPhiS > 5){
                cut_up = (-0.002362)*ele.P() + (1.045388);
                cut_down = (5.5e-05)*ele.P() + (0.884049);
            }
        }
        if(esec == 5){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up = (-0.00373)*ele.P() + (1.027939);
                cut_down = (-0.007682)*ele.P() + (0.920652);
            }
            if(localelPhiS < -5){
                cut_up = (-0.000977)*ele.P() + (1.011744);
                cut_down = (-0.003504)*ele.P() + (0.89456);
            }
            if(localelPhiS > 5){
                cut_up = (-0.007179)*ele.P() + (1.056021);
                cut_down = (-0.005851)*ele.P() + (0.908325);
            }
        }
        if(esec == 6){
            if(localelPhiS > -5 && localelPhiS < 5){
                cut_up = (-0.004726)*ele.P() + (1.037422);
                cut_down = (-0.007929)*ele.P() + (0.919135);
            }
            if(localelPhiS < -5){
                cut_up = (-0.005149)*ele.P() + (1.047543);
                cut_down = (-0.007816)*ele.P() + (0.926179);
            }
            if(localelPhiS > 5){
                cut_up = (-0.004952)*ele.P() + (1.031514);
                cut_down = (-0.009952)*ele.P() + (0.922387);
            }
        }

        return (MM_Vector.M() < cut_up && MM_Vector.M() > cut_down);

        """])
        
        return output
    
    
    
    ####################################################################################################################################################################
    ###################################################                Done Making Cuts to DataFrames                ###################################################
    ###                                              ##--------------------------------------------------------------##                                              ###
    ###----------------------------------------------##--------------------------------------------------------------##----------------------------------------------###
    ###                                              ##--------------------------------------------------------------##                                              ###
    ###################################################                  Defining Kinematic Binning                  ###################################################
    ####################################################################################################################################################################

    
    ###################################################################
    #####################     Bin Definitions     #####################
    #-----------------------------------------------------------------#
    ##############     Definitions for Q2 and xB Bins     #############
    
    
    # Q2 and xB Binning (See Table 4.2 on page 18 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
    rdf = rdf.Define("Q2_xB_Bin", """

        int Q2_xB_Bin = 0;

        /////////////////////////       Bin 1       /////////////////////////
        if(xB > 0.0835 && xB < 0.15){
            // Border lines of Bin 1:
            //                 Upper Border:
            //                          Q2 = ((2.28 - 1.3)/(0.15 - 0.0835))*(xB - 0.0835) + 1.3
            //                 Q2 must be less than the equation above for Bin 1
            //
            //                 Lower Border:
            //                          Q2 = ((1.30 - 1.30)/(0.12 - 0.0835))*(xB - 0.0835) + 1.30   (if xB < 0.12)
            //                          Q2 = ((1.38 - 1.30)/(0.15 - 0.1200))*(xB - 0.1200) + 1.30   (if xB > 0.12)
            //                 Q2 must be greater than the equations above for Bin 1

            int Condition_Up = 0;
            int Condition_Down = 0;
            // Both Condition_Up and Condition_Down should be met for Bin 1 to be confirmed.
            // Code will verify both conditions seperately before checking that they have been met.
            // If the condition has been met, its value will be set to 1.
            // If either is still 0 when checked, the event will be consided as being outside of Bin 1


            // Testing Upper Border of Bin 1
            if(Q2 <= ((2.28 - 1.3)/(0.15 - 0.0835))*(xB - 0.0835) + 1.3){
                Condition_Up = 1; // Condition for upper border of Bin 1 has been met
            }

            // Testing Lower Border of Bin 1
            if(xB < 0.12){
                if(Q2 >= ((1.30 - 1.30)/(0.12 - 0.0835))*(xB - 0.0835) + 1.30){
                    Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                }
            }
            if(xB > 0.12){
                if(Q2 >= ((1.38 - 1.30)/(0.15 - 0.1200))*(xB - 0.1200) + 1.30){
                    Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                }
            }


            if(Condition_Up == 1 && Condition_Down == 1){
                Q2_xB_Bin = 1;
                return Q2_xB_Bin; // Bin 1 Confirmed
            }

        }
        /////////////////////////     End of Bin 1     /////////////////////////




        /////////////////////////       Bin 2 or 3       /////////////////////////
        if(xB > 0.15 && xB < 0.24){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2 = ((2.75 - 1.98)/(0.24 - 0.15))*(xB - 0.15) + 1.98

            // Deciding between Bins
            if(Q2 < ((2.75 - 1.98)/(0.24 - 0.15))*(xB - 0.15) + 1.98){
                BinTest = 2; // Event will NOT go to bin 3
            }

            if(Q2 > ((2.75 - 1.98)/(0.24 - 0.15))*(xB - 0.15) + 1.98){
                BinTest = 3; // Event will NOT go to bin 2
            }



            // Final Border Test

            // Bin 2
            if(BinTest == 2){
                // Border lines of Bin 2:   Q2 = ((1.45 - 1.38)/(0.20 - 0.15))*(xB - 0.15) + 1.38   (if xB < 0.2)
                //                          Q2 = ((1.50 - 1.45)/(0.24 - 0.20))*(xB - 0.24) + 1.50   (if xB > 0.2)

                if(xB < 0.2){
                    if(Q2 >= ((1.45 - 1.38)/(0.20 - 0.15))*(xB - 0.15) + 1.38){
                        Q2_xB_Bin = 2;
                        return Q2_xB_Bin; // Bin 2 Confirmed
                    }
                }

                if(xB > 0.2){
                    if(Q2 >= ((1.50 - 1.45)/(0.24 - 0.20))*(xB - 0.24) + 1.50){
                        Q2_xB_Bin = 2;
                        return Q2_xB_Bin; // Bin 2 Confirmed
                    }
                }

            }
            // End of Bin 2


            // Bin 3
            if(BinTest == 3){
                // Border line of Bin 3:   Q2 = ((3.625 - 2.28)/(0.24 - 0.15))*(xB - 0.15) + 2.28

                if(Q2 <= ((3.625 - 2.28)/(0.24 - 0.15))*(xB - 0.15) + 2.28){
                    Q2_xB_Bin = 3;
                    return Q2_xB_Bin; // Bin 3 Confirmed
                }

            }
            // End of Bin 3


        }
        /////////////////////////     End of Bin 2 and 3     /////////////////////////




        /////////////////////////       Bin 4 or 5       /////////////////////////
        if(xB > 0.24 && xB < 0.34){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2 = ((3.63 - 2.75)/(0.34 - 0.24))*(xB - 0.24) + 2.75

            // Deciding between Bins
            if(Q2 < ((3.63 - 2.75)/(0.34 - 0.24))*(xB - 0.24) + 2.75){
                BinTest = 4; // Event will NOT go to bin 5
            }

            if(Q2 > ((3.63 - 2.75)/(0.34 - 0.24))*(xB - 0.24) + 2.75){
                BinTest = 5; // Event will NOT go to bin 4
            }



            // Final Border Test

            // Bin 4
            if(BinTest == 4){
                // Border lines of Bin 4:   Q2 = ((1.53 - 1.50)/(0.27 - 0.24))*(xB - 0.24) + 1.50   (if xB < 0.27)
                //                          Q2 = ((1.56 - 1.53)/(0.30 - 0.27))*(xB - 0.27) + 1.53   (if 0.27 < xB < 0.30)
                //                          Q2 = ((1.60 - 1.56)/(0.34 - 0.30))*(xB - 0.30) + 1.56   (if xB > 0.3)

                if(xB < 0.27){
                    if(Q2 >= ((1.53 - 1.50)/(0.27 - 0.24))*(xB - 0.24) + 1.50){
                        Q2_xB_Bin = 4;
                        return Q2_xB_Bin; // Bin 4 Confirmed
                    }
                }

                if(xB > 0.27 && xB < 0.30){
                    if(Q2 >= ((1.56 - 1.53)/(0.30 - 0.27))*(xB - 0.27) + 1.53){
                        Q2_xB_Bin = 4;
                        return Q2_xB_Bin; // Bin 4 Confirmed
                    }
                }

                if(xB > 0.30){
                    if(Q2 >= ((1.60 - 1.56)/(0.34 - 0.30))*(xB - 0.30) + 1.56){
                        Q2_xB_Bin = 4;
                        return Q2_xB_Bin; // Bin 4 Confirmed
                    }
                }

            }
            // End of Bin 4


            // Bin 5
            if(BinTest == 5){
                // Border line of Bin 5:   Q2 = ((5.12 - 3.625)/(0.34 - 0.24))*(xB - 0.24) + 3.625

                if(Q2 <= ((5.12 - 3.625)/(0.34 - 0.24))*(xB - 0.24) + 3.625){
                    Q2_xB_Bin = 5;
                    return Q2_xB_Bin; // Bin 5 Confirmed
                }

            }
            // End of Bin 5


        }
        /////////////////////////     End of Bin 4 and 5     /////////////////////////




        /////////////////////////       Bin 6 or 7       /////////////////////////
        if(xB > 0.34 && xB < 0.45){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2 = ((4.7 - 3.63)/(0.45 - 0.34))*(xB - 0.34) + 3.63

            // Deciding between Bins
            if(Q2 < ((4.7 - 3.63)/(0.45 - 0.34))*(xB - 0.34) + 3.63){
                BinTest = 6; // Event will NOT go to bin 7
            }

            if(Q2 > ((4.7 - 3.63)/(0.45 - 0.34))*(xB - 0.34) + 3.63){
                BinTest = 7; // Event will NOT go to bin 6
            }



            // Final Border Test

            // Bin 6
            if(BinTest == 6){
                // Border line of Bin 6:   Q2 = ((2.52 - 1.60)/(0.45 - 0.34))*(xB - 0.34) + 1.60

                if(Q2 >= ((2.52 - 1.60)/(0.45 - 0.34))*(xB - 0.34) + 1.60){
                    Q2_xB_Bin = 6;
                    return Q2_xB_Bin; // Bin 6 Confirmed
                }

            }
            // End of Bin 6


            // Bin 7
            if(BinTest == 7){
                // Border line of Bin 7:   Q2 = ((6.76 - 5.12)/(0.45 - 0.34))*(xB - 0.34) + 5.12

                if(Q2 <= ((6.76 - 5.12)/(0.45 - 0.34))*(xB - 0.34) + 5.12){
                    Q2_xB_Bin = 7;
                    return Q2_xB_Bin; // Bin 7 Confirmed
                }

            }
            // End of Bin 7


        }
        /////////////////////////     End of Bin 6 and 7     /////////////////////////




        /////////////////////////       Bin 8 or 9       /////////////////////////
        if(xB > 0.45){

            int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

            // line between bins: Q2 = ((7.42 - 4.70)/(0.708 - 0.45))*(xB - 0.45) + 4.70    

            // Deciding between Bins
            if(Q2 < ((7.42 - 4.70)/(0.708 - 0.45))*(xB - 0.45) + 4.70){
                BinTest = 8; // Event will NOT go to bin 9
            }
            if(Q2 > ((7.42 - 4.70)/(0.708 - 0.45))*(xB - 0.45) + 4.70){
                BinTest = 9; // Event will NOT go to bin 8
            }



            // Final Border Test

            // Bin 8
            if(BinTest == 8){
                // Border lines of Bin 8:   Q2 = ((3.05 - 2.52)/(0.500 - 0.45))*(xB - 0.45) + 2.52   (if xB < 0.50)
                //                          Q2 = ((4.05 - 3.05)/(0.570 - 0.50))*(xB - 0.50) + 3.05   (if 0.50 < xB < 0.57)
                //                          Q2 = ((5.40 - 4.05)/(0.640 - 0.57))*(xB - 0.57) + 4.05   (if 0.57 < xB < 0.64)
                //                          Q2 = ((7.42 - 5.40)/(0.708 - 0.64))*(xB - 0.64) + 5.40   (if xB > 0.64)

                if(xB < 0.50){
                    if(Q2 >= ((3.05 - 2.52)/(0.500 - 0.45))*(xB - 0.45) + 2.52){
                        Q2_xB_Bin = 8;
                        return Q2_xB_Bin; // Bin 8 Confirmed
                    }
                }

                if(xB > 0.50 && xB < 0.57){
                    if(Q2 >= ((4.05 - 3.05)/(0.570 - 0.50))*(xB - 0.50) + 3.05){
                        Q2_xB_Bin = 8;
                        return Q2_xB_Bin; // Bin 8 Confirmed
                    }
                }

                if(xB > 0.57 && xB < 0.64){
                    if(Q2 >= ((5.40 - 4.05)/(0.640 - 0.57))*(xB - 0.57) + 4.05){
                        Q2_xB_Bin = 8;
                        return Q2_xB_Bin; // Bin 8 Confirmed
                    }
                }

                if(xB > 0.64){
                    if(Q2 >= ((7.42 - 5.40)/(0.708 - 0.64))*(xB - 0.64) + 5.40){
                        Q2_xB_Bin = 8;
                        return Q2_xB_Bin; // Bin 8 Confirmed
                    }
                }

            }
            // End of Bin 8


            // Bin 9
            if(BinTest == 9){
                // Border lines of Bin 9:
                //                 Uppermost Border:
                //                          Q2 = ((10.185 -  6.760)/(0.6770 - 0.450))*(xB - 0.450) +  6.760   (if xB < 0.677)
                //                          Q2 = ((11.351 - 10.185)/(0.7896 - 0.677))*(xB - 0.677) + 10.185   (if xB > 0.677)
                //                 Q2 must be less than the equations above for Bin 9
                //
                //                 Rightmost Border:
                //                          Q2 =  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB - 0.708) + 7.42   (if xB < 0.75)
                //                          Q2 = ((11.351 - 9.52)/(0.7896 - 0.750))*(xB - 0.750) + 9.52   (if xB > 0.75)
                //                 Q2 must be greater than the equations above for Bin 9

                int Condition_Up = 0;
                int Condition_Right = 0;
                // Both Condition_Up and Condition_Right should be met for Bin 9 to be confirmed.
                // Code will verify both conditions seperately before checking that they have been met.
                // If the condition has been met, its value will be set to 1.
                // If either is still 0 when checked, the event will be consided as being outside of Bin 9


                // Testing Uppermost Border of Bin 9
                if(xB < 0.677){
                    if(Q2 <= ((10.185 -  6.760)/(0.6770 - 0.450))*(xB - 0.450) +  6.760){
                        Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                    }
                }
                if(xB > 0.677){
                    if(Q2 <= ((11.351 - 10.185)/(0.7896 - 0.677))*(xB - 0.677) + 10.185){
                        Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                    }
                }

                // Testing Rightmost Border of Bin 9
                if(xB < 0.75){
                    if(Q2 >=  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB - 0.708) + 7.42){
                        Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                    }
                }
                if(xB > 0.75){
                    if(Q2 >= ((11.351 - 9.52)/(0.7896 - 0.750))*(xB - 0.750) + 9.52){
                        Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                    }
                }


                if(Condition_Up == 1 && Condition_Right == 1){
                    Q2_xB_Bin = 9;
                    return Q2_xB_Bin; // Bin 9 Confirmed
                }

            }
            // End of Bin 9

        }
        /////////////////////////     End of Bin 8 and 9     /////////////////////////



        return Q2_xB_Bin;

    """)
    
    rdf = rdf.Define('Q2_xB_Bin_2', '''
        int Q2_xB_Bin_2 = Q2_xB_Bin;

        if(Q2_xB_Bin > 1 && Q2_xB_Bin_2%2 != 0){
            Q2_xB_Bin_2 += -2;
        }

        if(Q2 < 2){
            Q2_xB_Bin_2 = 0; 
        }

        return Q2_xB_Bin_2;
    ''')
    
    ###########     End of Definitions for Q2 and xB Bins     ##########
    #------------------------------------------------------------------#
    ###############     Definitions for z and pT Bins     ##############
    
    
    # z and pT Binning (See Table 4.3 on page 20 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
    rdf = rdf.Define("z_pT_Bin","""

        int z_pT_Bin = 0;
        int Num_z_Borders = 0;
        int Num_pT_Borders = 0;


        /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

        auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
        {

            // z_or_pT = 0 corresponds to z bins
            // z_or_pT = 1 corresponds to pT bins

            // For Q2_xB Bin 1
            if(Q2_xB_Bin_Num == 1){
                float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 2
            if(Q2_xB_Bin_Num == 2){
                float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 3
            if(Q2_xB_Bin_Num == 3){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 4
            if(Q2_xB_Bin_Num == 4){
                float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 5
            if(Q2_xB_Bin_Num == 5){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 6
            if(Q2_xB_Bin_Num == 6){
                float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 7
            if(Q2_xB_Bin_Num == 7){
                float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 8
            if(Q2_xB_Bin_Num == 8){
                float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 9
            if(Q2_xB_Bin_Num == 9){
                float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }


            // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
            // return empty_Borders;
            float empty = 0;
            return empty;
        };




        /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////



        // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

        // For Q2_xB Bin 0
        if(Q2_xB_Bin == 0){
            return z_pT_Bin; // Cannot create z-pT Bins without propper Q2-xB Bins
        }
        // For Q2_xB Bin 1
        if(Q2_xB_Bin == 1){
            // float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 2
        if(Q2_xB_Bin == 2){
            // float z_Borders[]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 3
        if(Q2_xB_Bin == 3){
            // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 4
        if(Q2_xB_Bin == 4){
            // float z_Borders[]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
            Num_z_Borders = 7;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 5
        if(Q2_xB_Bin == 5){
            // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
            Num_z_Borders = 8;
            // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
            Num_pT_Borders = 8;
        }
        // For Q2_xB Bin 6
        if(Q2_xB_Bin == 6){
            // float z_Borders[]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};
            Num_pT_Borders = 6;
        }
        // For Q2_xB Bin 7
        if(Q2_xB_Bin == 7){
            // float z_Borders[]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
            Num_z_Borders = 7;
            // float pT_Borders[] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};
            Num_pT_Borders = 7;
        }
        // For Q2_xB Bin 8
        if(Q2_xB_Bin == 8){
            // float z_Borders[]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.23, 0.34, 0.45, 0.70};
            Num_pT_Borders = 5;
        }
        // For Q2_xB Bin 9
        if(Q2_xB_Bin == 9){
            // float z_Borders[]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
            Num_z_Borders = 6;
            // float pT_Borders[] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};
            Num_pT_Borders = 6;
        }

        if(Num_z_Borders == 0){
            // float  z_Borders[1]  = {0};
            Num_z_Borders = 1;
            // float  pT_Borders[1] = {0};
            Num_pT_Borders = 1;
        }



        int z_pT_Bin_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                // based on the number of times the loop has run

        // Determining z_pT Bins
        for(int zbin = 1; zbin < Num_z_Borders; zbin++){
            if(z_pT_Bin != 0){
                continue;   // If the bin has already been assigned, this line will end the loop.
                            // This is to make sure the loop does not run longer than what is necessary.
            }    

            if(z > Borders_function(Q2_xB_Bin, 0, zbin) && z < Borders_function(Q2_xB_Bin, 0, zbin - 1)){
                // Found the correct z bin

                for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                    if(z_pT_Bin != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                    if(pT > Borders_function(Q2_xB_Bin, 1, pTbin) && pT < Borders_function(Q2_xB_Bin, 1, pTbin+1)){
                        // Found the correct pT bin
                        z_pT_Bin = z_pT_Bin_count; // The value of the z_pT_Bin has been set
                        return z_pT_Bin;
                    }
                    else{
                        z_pT_Bin_count = z_pT_Bin_count + 1; // Checking the next bin
                    }
                }

            }
            else{
                z_pT_Bin_count = z_pT_Bin_count + (Num_pT_Borders - 1);
                // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                // This represents checking each pT bin for the given z bin without going through each entry in the loop.
            }    
        }


        return z_pT_Bin;



    """)
    
    
    rdf = rdf.Define('z_pT_Bin_2', '''
    
        auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
        {
            // z_or_pT = 0 corresponds to z bins
            // z_or_pT = 1 corresponds to pT bins

            // For Q2_xB Bin 1 (was 3 in old scheme)
            if(Q2_xB_Bin_Num == 1){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 2
            if(Q2_xB_Bin_Num == 2){
                float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 3 (was 5 in old scheme)
            if(Q2_xB_Bin_Num == 3){
                float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[7 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 4
            if(Q2_xB_Bin_Num == 4){
                float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 5 (was 7 in old scheme)
            if(Q2_xB_Bin_Num == 5){
                float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                if(z_or_pT == 0){
                    return z_Borders[6 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }    
            // For Q2_xB Bin 6
            if(Q2_xB_Bin_Num == 6){
                float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 7 (was 9 in old scheme)
            if(Q2_xB_Bin_Num == 7){
                float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }
            // For Q2_xB Bin 8
            if(Q2_xB_Bin_Num == 8){
                float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};

                if(z_or_pT == 0){
                    return z_Borders[5 - entry];
                }
                if(z_or_pT == 1){
                    return pT_Borders[entry];
                }
            }



            // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
            // return empty_Borders;
            float empty = 0;
            return empty;
        };


        /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////


        // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

        // Default:
        int Num_z_Borders = 8; 
        int Num_pT_Borders = 8;
        int z_pT_Bin_2 = 0;

        // For Q2_xB Bin 0
        if(Q2_xB_Bin_2 == 0){
            z_pT_Bin_2 = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
            Num_z_Borders = 0; Num_pT_Borders = 0;
        }
        // For Q2_xB Bin 1 (Uses Default for both borders)

        // For Q2_xB Bin 2 (Uses Default for both borders)

        // For Q2_xB Bin 3 (Uses Default for both borders)

        // For Q2_xB Bin 4 (Uses Default for pT borders)
        if(Q2_xB_Bin_2 == 4){
            Num_z_Borders = 7;
        }

        // For Q2_xB Bin 5 (New scheme)
        if(Q2_xB_Bin_2 == 5){
            Num_z_Borders = 7; Num_pT_Borders = 7;
        }

        // For Q2_xB Bin 6
        if(Q2_xB_Bin_2 == 6){
            Num_z_Borders = 6; Num_pT_Borders = 6;
        }

        // For Q2_xB Bin 7 (New scheme)
        if(Q2_xB_Bin_2 == 7){
            Num_z_Borders = 6; Num_pT_Borders = 6;
        }

        // For Q2_xB Bin 8
        if(Q2_xB_Bin_2 == 8){
            Num_z_Borders = 6; Num_pT_Borders = 5;
        }

        if(Num_z_Borders == 0){
            Num_z_Borders = 1; Num_pT_Borders = 1;
        }


        int z_pT_Bin_2_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                // based on the number of times the loop has run

        // Determining z_pT Bins
        for(int zbin = 1; zbin < Num_z_Borders; zbin++){
            if(z_pT_Bin_2 != 0){
                continue;   // If the bin has already been assigned, this line will end the loop.
                            // This is to make sure the loop does not run longer than what is necessary.
            }    

            if(z > Borders_function(Q2_xB_Bin_2, 0, zbin) && z < Borders_function(Q2_xB_Bin_2, 0, zbin - 1)){
                // Found the correct z bin

                for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                    if(z_pT_Bin_2 != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                    if(pT > Borders_function(Q2_xB_Bin_2, 1, pTbin) && pT < Borders_function(Q2_xB_Bin_2, 1, pTbin+1)){
                        // Found the correct pT bin
                        z_pT_Bin_2 = z_pT_Bin_2_count; // The value of the z_pT_Bin_2 has been set
                        // cout<<"The value of the z_pT_Bin_2 has been set as: "<<z_pT_Bin_2<<endl;
                        break;
                    }
                    else{
                        z_pT_Bin_2_count += 1; // Checking the next bin
                        // cout<<"Checking the next bin"<<endl;
                    }
                }

            }
            else{
                z_pT_Bin_2_count += (Num_pT_Borders - 1);
                // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                // This represents checking each pT bin for the given z bin without going through each entry in the loop.
            }    
        }


        return z_pT_Bin_2;

    
    ''')
    
    
    ###########     End of Definitions for z and pT Bins     ##########
    #-----------------------------------------------------------------#
    #####################     Bin Definitions     #####################
    ###################################################################
    
    
    
    
    
    if(datatype == "mdf" or datatype == "pdf"):
        
        #############################################################################
        #####################     Generated Bin Definitions     #####################
        #---------------------------------------------------------------------------#
        ##############     Definitions for Generated Q2 and xB Bins     #############

        # Q2 and xB Binning (See Table 4.2 on page 18 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
        rdf = rdf.Define("Q2_xB_Bin_gen","""

            int Q2_xB_Bin_gen = 0;

            /////////////////////////       Bin 1       /////////////////////////
            if(xB_gen > 0.0835 && xB_gen < 0.15){
                // Border lines of Bin 1:
                //                 Upper Border:
                //                          Q2_gen = ((2.28 - 1.3)/(0.15 - 0.0835))*(xB_gen - 0.0835) + 1.3
                //                 Q2_gen must be less than the equation above for Bin 1
                //
                //                 Lower Border:
                //                          Q2_gen = ((1.30 - 1.30)/(0.12 - 0.0835))*(xB_gen - 0.0835) + 1.30   (if xB_gen < 0.12)
                //                          Q2_gen = ((1.38 - 1.30)/(0.15 - 0.1200))*(xB_gen - 0.1200) + 1.30   (if xB_gen > 0.12)
                //                 Q2_gen must be greater than the equations above for Bin 1

                int Condition_Up = 0;
                int Condition_Down = 0;
                // Both Condition_Up and Condition_Down should be met for Bin 1 to be confirmed.
                // Code will verify both conditions seperately before checking that they have been met.
                // If the condition has been met, its value will be set to 1.
                // If either is still 0 when checked, the event will be consided as being outside of Bin 1


                // Testing Upper Border of Bin 1
                if(Q2_gen <= ((2.28 - 1.3)/(0.15 - 0.0835))*(xB_gen - 0.0835) + 1.3){
                    Condition_Up = 1; // Condition for upper border of Bin 1 has been met
                }

                // Testing Lower Border of Bin 1
                if(xB_gen < 0.12){
                    if(Q2_gen >= ((1.30 - 1.30)/(0.12 - 0.0835))*(xB_gen - 0.0835) + 1.30){
                        Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                    }
                }
                if(xB_gen > 0.12){
                    if(Q2_gen >= ((1.38 - 1.30)/(0.15 - 0.1200))*(xB_gen - 0.1200) + 1.30){
                        Condition_Down = 1; // Condition for lower border of Bin 1 has been met
                    }
                }


                if(Condition_Up == 1 && Condition_Down == 1){
                    Q2_xB_Bin_gen = 1;
                    return Q2_xB_Bin_gen; // Bin 1 Confirmed
                }

            }
            /////////////////////////     End of Bin 1     /////////////////////////




            /////////////////////////       Bin 2 or 3       /////////////////////////
            if(xB_gen > 0.15 && xB_gen < 0.24){

                int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

                // line between bins: Q2_gen = ((2.75 - 1.98)/(0.24 - 0.15))*(xB_gen - 0.15) + 1.98

                // Deciding between Bins
                if(Q2_gen < ((2.75 - 1.98)/(0.24 - 0.15))*(xB_gen - 0.15) + 1.98){
                    BinTest = 2; // Event will NOT go to bin 3
                }

                if(Q2_gen > ((2.75 - 1.98)/(0.24 - 0.15))*(xB_gen - 0.15) + 1.98){
                    BinTest = 3; // Event will NOT go to bin 2
                }



                // Final Border Test

                // Bin 2
                if(BinTest == 2){
                    // Border lines of Bin 2:   Q2_gen = ((1.45 - 1.38)/(0.20 - 0.15))*(xB_gen - 0.15) + 1.38   (if xB_gen < 0.2)
                    //                          Q2_gen = ((1.50 - 1.45)/(0.24 - 0.20))*(xB_gen - 0.24) + 1.50   (if xB_gen > 0.2)

                    if(xB_gen < 0.2){
                        if(Q2_gen >= ((1.45 - 1.38)/(0.20 - 0.15))*(xB_gen - 0.15) + 1.38){
                            Q2_xB_Bin_gen = 2;
                            return Q2_xB_Bin_gen; // Bin 2 Confirmed
                        }
                    }

                    if(xB_gen > 0.2){
                        if(Q2_gen >= ((1.50 - 1.45)/(0.24 - 0.20))*(xB_gen - 0.24) + 1.50){
                            Q2_xB_Bin_gen = 2;
                            return Q2_xB_Bin_gen; // Bin 2 Confirmed
                        }
                    }

                }
                // End of Bin 2


                // Bin 3
                if(BinTest == 3){
                    // Border line of Bin 3:   Q2_gen = ((3.625 - 2.28)/(0.24 - 0.15))*(xB_gen - 0.15) + 2.28

                    if(Q2_gen <= ((3.625 - 2.28)/(0.24 - 0.15))*(xB_gen - 0.15) + 2.28){
                        Q2_xB_Bin_gen = 3;
                        return Q2_xB_Bin_gen; // Bin 3 Confirmed
                    }

                }
                // End of Bin 3


            }
            /////////////////////////     End of Bin 2 and 3     /////////////////////////




            /////////////////////////       Bin 4 or 5       /////////////////////////
            if(xB_gen > 0.24 && xB_gen < 0.34){

                int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

                // line between bins: Q2_gen = ((3.63 - 2.75)/(0.34 - 0.24))*(xB_gen - 0.24) + 2.75

                // Deciding between Bins
                if(Q2_gen < ((3.63 - 2.75)/(0.34 - 0.24))*(xB_gen - 0.24) + 2.75){
                    BinTest = 4; // Event will NOT go to bin 5
                }

                if(Q2_gen > ((3.63 - 2.75)/(0.34 - 0.24))*(xB_gen - 0.24) + 2.75){
                    BinTest = 5; // Event will NOT go to bin 4
                }



                // Final Border Test

                // Bin 4
                if(BinTest == 4){
                    // Border lines of Bin 4:   Q2_gen = ((1.53 - 1.50)/(0.27 - 0.24))*(xB_gen - 0.24) + 1.50   (if xB_gen < 0.27)
                    //                          Q2_gen = ((1.56 - 1.53)/(0.30 - 0.27))*(xB_gen - 0.27) + 1.53   (if 0.27 < xB_gen < 0.30)
                    //                          Q2_gen = ((1.60 - 1.56)/(0.34 - 0.30))*(xB_gen - 0.30) + 1.56   (if xB_gen > 0.3)

                    if(xB_gen < 0.27){
                        if(Q2_gen >= ((1.53 - 1.50)/(0.27 - 0.24))*(xB_gen - 0.24) + 1.50){
                            Q2_xB_Bin_gen = 4;
                            return Q2_xB_Bin_gen; // Bin 4 Confirmed
                        }
                    }

                    if(xB_gen > 0.27 && xB_gen < 0.30){
                        if(Q2_gen >= ((1.56 - 1.53)/(0.30 - 0.27))*(xB_gen - 0.27) + 1.53){
                            Q2_xB_Bin_gen = 4;
                            return Q2_xB_Bin_gen; // Bin 4 Confirmed
                        }
                    }

                    if(xB_gen > 0.30){
                        if(Q2_gen >= ((1.60 - 1.56)/(0.34 - 0.30))*(xB_gen - 0.30) + 1.56){
                            Q2_xB_Bin_gen = 4;
                            return Q2_xB_Bin_gen; // Bin 4 Confirmed
                        }
                    }

                }
                // End of Bin 4


                // Bin 5
                if(BinTest == 5){
                    // Border line of Bin 5:   Q2_gen = ((5.12 - 3.625)/(0.34 - 0.24))*(xB_gen - 0.24) + 3.625

                    if(Q2_gen <= ((5.12 - 3.625)/(0.34 - 0.24))*(xB_gen - 0.24) + 3.625){
                        Q2_xB_Bin_gen = 5;
                        return Q2_xB_Bin_gen; // Bin 5 Confirmed
                    }

                }
                // End of Bin 5


            }
            /////////////////////////     End of Bin 4 and 5     /////////////////////////




            /////////////////////////       Bin 6 or 7       /////////////////////////
            if(xB_gen > 0.34 && xB_gen < 0.45){

                int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

                // line between bins: Q2_gen = ((4.7 - 3.63)/(0.45 - 0.34))*(xB_gen - 0.34) + 3.63

                // Deciding between Bins
                if(Q2_gen < ((4.7 - 3.63)/(0.45 - 0.34))*(xB_gen - 0.34) + 3.63){
                    BinTest = 6; // Event will NOT go to bin 7
                }

                if(Q2_gen > ((4.7 - 3.63)/(0.45 - 0.34))*(xB_gen - 0.34) + 3.63){
                    BinTest = 7; // Event will NOT go to bin 6
                }



                // Final Border Test

                // Bin 6
                if(BinTest == 6){
                    // Border line of Bin 6:   Q2_gen = ((2.52 - 1.60)/(0.45 - 0.34))*(xB_gen - 0.34) + 1.60

                    if(Q2_gen >= ((2.52 - 1.60)/(0.45 - 0.34))*(xB_gen - 0.34) + 1.60){
                        Q2_xB_Bin_gen = 6;
                        return Q2_xB_Bin_gen; // Bin 6 Confirmed
                    }

                }
                // End of Bin 6


                // Bin 7
                if(BinTest == 7){
                    // Border line of Bin 7:   Q2_gen = ((6.76 - 5.12)/(0.45 - 0.34))*(xB_gen - 0.34) + 5.12

                    if(Q2_gen <= ((6.76 - 5.12)/(0.45 - 0.34))*(xB_gen - 0.34) + 5.12){
                        Q2_xB_Bin_gen = 7;
                        return Q2_xB_Bin_gen; // Bin 7 Confirmed
                    }

                }
                // End of Bin 7


            }
            /////////////////////////     End of Bin 6 and 7     /////////////////////////




            /////////////////////////       Bin 8 or 9       /////////////////////////
            if(xB_gen > 0.45){

                int BinTest = 0; //Test value for bin number (used while determining which bin the event belongs to)

                // line between bins: Q2_gen = ((7.42 - 4.70)/(0.708 - 0.45))*(xB_gen - 0.45) + 4.70    

                // Deciding between Bins
                if(Q2_gen < ((7.42 - 4.70)/(0.708 - 0.45))*(xB_gen - 0.45) + 4.70){
                    BinTest = 8; // Event will NOT go to bin 9
                }
                if(Q2_gen > ((7.42 - 4.70)/(0.708 - 0.45))*(xB_gen - 0.45) + 4.70){
                    BinTest = 9; // Event will NOT go to bin 8
                }



                // Final Border Test

                // Bin 8
                if(BinTest == 8){
                    // Border lines of Bin 8:   Q2_gen = ((3.05 - 2.52)/(0.500 - 0.45))*(xB_gen - 0.45) + 2.52   (if xB_gen < 0.50)
                    //                          Q2_gen = ((4.05 - 3.05)/(0.570 - 0.50))*(xB_gen - 0.50) + 3.05   (if 0.50 < xB_gen < 0.57)
                    //                          Q2_gen = ((5.40 - 4.05)/(0.640 - 0.57))*(xB_gen - 0.57) + 4.05   (if 0.57 < xB_gen < 0.64)
                    //                          Q2_gen = ((7.42 - 5.40)/(0.708 - 0.64))*(xB_gen - 0.64) + 5.40   (if xB_gen > 0.64)

                    if(xB_gen < 0.50){
                        if(Q2_gen >= ((3.05 - 2.52)/(0.500 - 0.45))*(xB_gen - 0.45) + 2.52){
                            Q2_xB_Bin_gen = 8;
                            return Q2_xB_Bin_gen; // Bin 8 Confirmed
                        }
                    }

                    if(xB_gen > 0.50 && xB_gen < 0.57){
                        if(Q2_gen >= ((4.05 - 3.05)/(0.570 - 0.50))*(xB_gen - 0.50) + 3.05){
                            Q2_xB_Bin_gen = 8;
                            return Q2_xB_Bin_gen; // Bin 8 Confirmed
                        }
                    }

                    if(xB_gen > 0.57 && xB_gen < 0.64){
                        if(Q2_gen >= ((5.40 - 4.05)/(0.640 - 0.57))*(xB_gen - 0.57) + 4.05){
                            Q2_xB_Bin_gen = 8;
                            return Q2_xB_Bin_gen; // Bin 8 Confirmed
                        }
                    }

                    if(xB_gen > 0.64){
                        if(Q2_gen >= ((7.42 - 5.40)/(0.708 - 0.64))*(xB_gen - 0.64) + 5.40){
                            Q2_xB_Bin_gen = 8;
                            return Q2_xB_Bin_gen; // Bin 8 Confirmed
                        }
                    }

                }
                // End of Bin 8


                // Bin 9
                if(BinTest == 9){
                    // Border lines of Bin 9:
                    //                 Uppermost Border:
                    //                          Q2_gen = ((10.185 -  6.760)/(0.6770 - 0.450))*(xB_gen - 0.450) +  6.760   (if xB_gen < 0.677)
                    //                          Q2_gen = ((11.351 - 10.185)/(0.7896 - 0.677))*(xB_gen - 0.677) + 10.185   (if xB_gen > 0.677)
                    //                 Q2_gen must be less than the equations above for Bin 9
                    //
                    //                 Rightmost Border:
                    //                          Q2_gen =  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB_gen - 0.708) + 7.42   (if xB_gen < 0.75)
                    //                          Q2_gen = ((11.351 - 9.52)/(0.7896 - 0.750))*(xB_gen - 0.750) + 9.52   (if xB_gen > 0.75)
                    //                 Q2_gen must be greater than the equations above for Bin 9

                    int Condition_Up = 0;
                    int Condition_Right = 0;
                    // Both Condition_Up and Condition_Right should be met for Bin 9 to be confirmed.
                    // Code will verify both conditions seperately before checking that they have been met.
                    // If the condition has been met, its value will be set to 1.
                    // If either is still 0 when checked, the event will be consided as being outside of Bin 9


                    // Testing Uppermost Border of Bin 9
                    if(xB_gen < 0.677){
                        if(Q2_gen <= ((10.185 -  6.760)/(0.6770 - 0.450))*(xB_gen - 0.450) +  6.760){
                            Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                        }
                    }
                    if(xB_gen > 0.677){
                        if(Q2_gen <= ((11.351 - 10.185)/(0.7896 - 0.677))*(xB_gen - 0.677) + 10.185){
                            Condition_Up = 1; // Condition for upper border of Bin 9 has been met
                        }
                    }

                    // Testing Rightmost Border of Bin 9
                    if(xB_gen < 0.75){
                        if(Q2_gen >=  ((9.520 - 7.42)/(0.7500 - 0.708))*(xB_gen - 0.708) + 7.42){
                            Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                        }
                    }
                    if(xB_gen > 0.75){
                        if(Q2_gen >= ((11.351 - 9.52)/(0.7896 - 0.750))*(xB_gen - 0.750) + 9.52){
                            Condition_Right = 1; // Condition for rightmost border of Bin 9 has been met
                        }
                    }


                    if(Condition_Up == 1 && Condition_Right == 1){
                        Q2_xB_Bin_gen = 9;
                        return Q2_xB_Bin_gen; // Bin 9 Confirmed
                    }

                }
                // End of Bin 9

            }
            /////////////////////////     End of Bin 8 and 9     /////////////////////////



            return Q2_xB_Bin_gen;

        """)

        
        rdf = rdf.Define('Q2_xB_Bin_2_gen', '''
            int Q2_xB_Bin_2_gen = Q2_xB_Bin_gen;

            if(Q2_xB_Bin_gen > 1 && Q2_xB_Bin_2_gen%2 != 0){
                Q2_xB_Bin_2_gen += -2;
            }

            if(Q2_gen < 1.94){
                Q2_xB_Bin_2_gen = 0; 
            }

            return Q2_xB_Bin_2_gen;
        ''')
        

        ###########     End of Definitions for Generated Q2 and xB Bins     ##########
        #----------------------------------------------------------------------------#
        ###############     Definitions for Generated z and pT Bins     ##############


        # z and pT Binning (See Table 4.3 on page 20 of "A multidimensional study of SIDIS π+ beam spin asymmetry over a wide range of kinematics" - Stefan Diehl)
        rdf = rdf.Define("z_pT_Bin_gen","""

            int z_pT_Bin_gen = 0;
            int Num_z_Borders = 0;
            int Num_pT_Borders = 0;


            /////////////////////////////////////////          Automatic Function for Border Creation          /////////////////////////////////////////

            auto Borders_function = [&](int Q2_xB_Bin_gen_Num, int z_or_pT_gen, int entry)
            {

                // z_or_pT_gen = 0 corresponds to z bins
                // z_or_pT_gen = 1 corresponds to pT bins

                // For Q2_xB Bin 1
                if(Q2_xB_Bin_gen_Num == 1){
                    float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 2
                if(Q2_xB_Bin_gen_Num == 2){
                    float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 3
                if(Q2_xB_Bin_gen_Num == 3){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 4
                if(Q2_xB_Bin_gen_Num == 4){
                    float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[6 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 5
                if(Q2_xB_Bin_gen_Num == 5){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 6
                if(Q2_xB_Bin_gen_Num == 6){
                    float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                    float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                    if(z_or_pT_gen == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 7
                if(Q2_xB_Bin_gen_Num == 7){
                    float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                    float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                    if(z_or_pT_gen == 0){
                        return z_Borders[6 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 8
                if(Q2_xB_Bin_gen_Num == 8){
                    float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                    float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};

                    if(z_or_pT_gen == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 9
                if(Q2_xB_Bin_gen_Num == 9){
                    float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                    float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                    if(z_or_pT_gen == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT_gen == 1){
                        return pT_Borders[entry];
                    }
                }


                // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
                // return empty_Borders;
                float empty = 0;
                return empty;
            };




            /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////



            // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin_gen')

            // For Q2_xB Bin 0
            if(Q2_xB_Bin_gen == 0){
                return z_pT_Bin_gen; // Cannot create z-pT Bins without propper Q2-xB Bins
            }
            // For Q2_xB Bin 1
            if(Q2_xB_Bin_gen == 1){
                // float  z_Borders[8] = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                Num_z_Borders = 8;
                // float pT_Borders[8] = {0.05, 0.22, 0.32, 0.41, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 2
            if(Q2_xB_Bin_gen == 2){
                // float z_Borders[]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                Num_z_Borders = 8;
                // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 3
            if(Q2_xB_Bin_gen == 3){
                // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                Num_z_Borders = 8;
                // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 4
            if(Q2_xB_Bin_gen == 4){
                // float z_Borders[]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                Num_z_Borders = 7;
                // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 5
            if(Q2_xB_Bin_gen == 5){
                // float z_Borders[]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                Num_z_Borders = 8;
                // float pT_Borders[] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};
                Num_pT_Borders = 8;
            }
            // For Q2_xB Bin 6
            if(Q2_xB_Bin_gen == 6){
                // float z_Borders[]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                Num_z_Borders = 6;
                // float pT_Borders[] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};
                Num_pT_Borders = 6;
            }
            // For Q2_xB Bin 7
            if(Q2_xB_Bin_gen == 7){
                // float z_Borders[]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                Num_z_Borders = 7;
                // float pT_Borders[] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};
                Num_pT_Borders = 7;
            }
            // For Q2_xB Bin 8
            if(Q2_xB_Bin_gen == 8){
                // float z_Borders[]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                Num_z_Borders = 6;
                // float pT_Borders[] = {0.05, 0.23, 0.34, 0.45, 0.70};
                Num_pT_Borders = 5;
            }
            // For Q2_xB Bin 9
            if(Q2_xB_Bin_gen == 9){
                // float z_Borders[]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                Num_z_Borders = 6;
                // float pT_Borders[] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};
                Num_pT_Borders = 6;
            }

            if(Num_z_Borders == 0){
                // float  z_Borders[1]  = {0};
                Num_z_Borders = 1;
                // float  pT_Borders[1] = {0};
                Num_pT_Borders = 1;
            }



            int z_pT_Bin_gen_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                    // based on the number of times the loop has run

            // Determining z_pT Bins
            for(int zbin = 1; zbin < Num_z_Borders; zbin++){
                if(z_pT_Bin_gen != 0){
                    continue;   // If the bin has already been assigned, this line will end the loop.
                                // This is to make sure the loop does not run longer than what is necessary.
                }    

                if(z_gen > Borders_function(Q2_xB_Bin_gen, 0, zbin) && z_gen < Borders_function(Q2_xB_Bin_gen, 0, zbin - 1)){
                    // Found the correct z bin

                    for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                        if(z_pT_Bin_gen != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                        if(pT_gen > Borders_function(Q2_xB_Bin_gen, 1, pTbin) && pT_gen < Borders_function(Q2_xB_Bin_gen, 1, pTbin+1)){
                            // Found the correct pT bin
                            z_pT_Bin_gen = z_pT_Bin_gen_count; // The value of the z_pT_Bin_gen has been set
                            return z_pT_Bin_gen;
                        }
                        else{
                            z_pT_Bin_gen_count = z_pT_Bin_gen_count + 1; // Checking the next bin
                        }
                    }

                }
                else{
                    z_pT_Bin_gen_count = z_pT_Bin_gen_count + (Num_pT_Borders - 1);
                    // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                    // This represents checking each pT bin for the given z bin without going through each entry in the loop.
                }    
            }


            return z_pT_Bin_gen;



        """)
        
        
        rdf = rdf.Define('z_pT_Bin_2_gen', '''

            auto Borders_function = [&](int Q2_xB_Bin_Num, int z_or_pT, int entry)
            {
                // z_or_pT = 0 corresponds to z bins
                // z_or_pT = 1 corresponds to pT bins

                // For Q2_xB Bin 1 (was 3 in old scheme)
                if(Q2_xB_Bin_Num == 1){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 2
                if(Q2_xB_Bin_Num == 2){
                    float z_Borders[8]  = {0.18, 0.25, 0.29, 0.34, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 3 (was 5 in old scheme)
                if(Q2_xB_Bin_Num == 3){
                    float z_Borders[8]  = {0.15, 0.20, 0.24, 0.29, 0.36, 0.445, 0.55, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[7 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 4
                if(Q2_xB_Bin_Num == 4){
                    float z_Borders[7]  = {0.20, 0.29, 0.345, 0.41, 0.50, 0.60, 0.70};
                    float pT_Borders[8] = {0.05, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[6 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 5 (was 7 in old scheme)
                if(Q2_xB_Bin_Num == 5){
                    float z_Borders[7]  = {0.15, 0.215, 0.26, 0.32, 0.40, 0.50, 0.70};
                    float pT_Borders[7] = {0.05, 0.22, 0.32, 0.41, 0.51, 0.65, 1.0};

                    if(z_or_pT == 0){
                        return z_Borders[6 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }    
                // For Q2_xB Bin 6
                if(Q2_xB_Bin_Num == 6){
                    float z_Borders[6]  = {0.22, 0.32, 0.40, 0.47, 0.56, 0.70};
                    float pT_Borders[6] = {0.05, 0.22, 0.32, 0.42, 0.54, 0.80};

                    if(z_or_pT == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 7 (was 9 in old scheme)
                if(Q2_xB_Bin_Num == 7){
                    float z_Borders[6]  = {0.15, 0.23, 0.30, 0.39, 0.50, 0.70};
                    float pT_Borders[6] = {0.05, 0.23, 0.34, 0.435, 0.55, 0.80};

                    if(z_or_pT == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }
                // For Q2_xB Bin 8
                if(Q2_xB_Bin_Num == 8){
                    float z_Borders[6]  = {0.22, 0.30, 0.36, 0.425, 0.50, 0.70};
                    float pT_Borders[5] = {0.05, 0.23, 0.34, 0.45, 0.70};

                    if(z_or_pT == 0){
                        return z_Borders[5 - entry];
                    }
                    if(z_or_pT == 1){
                        return pT_Borders[entry];
                    }
                }

                // float  empty_Borders[1]  = {0}; // In case all other conditions fail somehow
                // return empty_Borders;
                float empty = 0;
                return empty;
            };


            /////////////////////////////////////////          End of Automatic Function for Border Creation          /////////////////////////////////////////


            // Defining Borders for z and pT Bins (based on 'Q2_xB_Bin')

            // Default:
            int Num_z_Borders = 8;
            int Num_pT_Borders = 8;
            int z_pT_Bin_2_gen = 0;

            // For Q2_xB Bin 0
            if(Q2_xB_Bin_2_gen == 0){
                z_pT_Bin_2_gen = 0; // Cannot create z-pT Bins without propper Q2-xB Bins
                Num_z_Borders = 0; Num_pT_Borders = 0;
            }
            // For Q2_xB Bin 1 (Uses Default for both borders)

            // For Q2_xB Bin 2 (Uses Default for both borders)

            // For Q2_xB Bin 3 (Uses Default for both borders)

            // For Q2_xB Bin 4 (Uses Default for pT borders)
            if(Q2_xB_Bin_2_gen == 4){
                Num_z_Borders = 7;
            }

            // For Q2_xB Bin 5 (New scheme)
            if(Q2_xB_Bin_2_gen == 5){
                Num_z_Borders = 7; Num_pT_Borders = 7;
            }

            // For Q2_xB Bin 6
            if(Q2_xB_Bin_2_gen == 6){
                Num_z_Borders = 6; Num_pT_Borders = 6;
            }

            // For Q2_xB Bin 7 (New scheme)
            if(Q2_xB_Bin_2_gen == 7){
                Num_z_Borders = 6; Num_pT_Borders = 6;
            }

            // For Q2_xB Bin 8
            if(Q2_xB_Bin_2_gen == 8){
                Num_z_Borders = 6; Num_pT_Borders = 5;
            }

            if(Num_z_Borders == 0){
                Num_z_Borders = 1; Num_pT_Borders = 1;
            }


            int z_pT_Bin_2_gen_count = 1; // This is a dummy variable used by the loops to correctly assign the bin number
                                    // based on the number of times the loop has run

            // Determining z_pT Bins
            for(int zbin = 1; zbin < Num_z_Borders; zbin++){
                if(z_pT_Bin_2_gen != 0){
                    continue;   // If the bin has already been assigned, this line will end the loop.
                                // This is to make sure the loop does not run longer than what is necessary.
                }    

                if(z_gen > Borders_function(Q2_xB_Bin_2_gen, 0, zbin) && z_gen < Borders_function(Q2_xB_Bin_2_gen, 0, zbin - 1)){
                    // Found the correct z bin

                    for(int pTbin = 0; pTbin < Num_pT_Borders - 1; pTbin++){
                        if(z_pT_Bin_2_gen != 0){continue;}    // If the bin has already been assigned, this line will end the loop. (Same reason as above)

                        if(pT_gen > Borders_function(Q2_xB_Bin_2_gen, 1, pTbin) && pT_gen < Borders_function(Q2_xB_Bin_2_gen, 1, pTbin+1)){
                            // Found the correct pT bin
                            z_pT_Bin_2_gen = z_pT_Bin_2_gen_count; // The value of the z_pT_Bin_2_gen has been set
                            // cout<<"The value of the z_pT_Bin_2_gen has been set as: "<<z_pT_Bin_2_gen<<endl;
                            break;
                        }
                        else{
                            z_pT_Bin_2_gen_count += 1; // Checking the next bin
                            // cout<<"Checking the next bin"<<endl;
                        }
                    }

                }
                else{
                    z_pT_Bin_2_gen_count += (Num_pT_Borders - 1);
                    // For each z bin that fails, the bin count goes up by (Num_pT_Borders - 1).
                    // This represents checking each pT bin for the given z bin without going through each entry in the loop.
                }    
            }


            return z_pT_Bin_2_gen;
        
        
        ''')


        ###########     End of Definitions for Generated z and pT Bins     ##########
        #---------------------------------------------------------------------------#
        
    ##===================================================##
    ##=====##=====##   4D Kinematic Bins   ##=====##=====##
    ##===================================================##
    
    rdf = rdf.Define('Bin_4D', """

        int add_to_bin = 0;
        int Bin_4D = -1; // Updated on 7-19-2022

        if(Q2_xB_Bin_2 == 0){
            Bin_4D = -1; // Updated on 7-19-2022
            return Bin_4D;
        }
        if(Q2_xB_Bin_2 == 1){
            add_to_bin = 0;
        }
        if(Q2_xB_Bin_2 == 2){
            add_to_bin = 50;
        }
        if(Q2_xB_Bin_2 == 3){
            add_to_bin = 100;
        }
        if(Q2_xB_Bin_2 == 4){
            add_to_bin = 150;
        }
        if(Q2_xB_Bin_2 == 5){
            add_to_bin = 193;
        }
        if(Q2_xB_Bin_2 == 6){
            add_to_bin = 230;
        }
        if(Q2_xB_Bin_2 == 7){
            add_to_bin = 256;
        }
        if(Q2_xB_Bin_2 == 8){
            add_to_bin = 283;
        }

        Bin_4D = z_pT_Bin_2 + add_to_bin;

        return Bin_4D;

    """)
    
    
    rdf = rdf.Define('Bin_Res_4D', """
    
        int add_to_bin = 0;
        int Bin_Res_4D = -1;

        if(Q2_xB_Bin_2 == 0 || z_pT_Bin_2 == 0){
            Bin_Res_4D = -1; // Might want to change to 0 later...
            return Bin_Res_4D;
            // Events outside of either binning scheme is automatically given a Bin_Res_4D bin value of -1
            // No spaces are given between bins
        }
        if(Q2_xB_Bin_2 == 1){
            add_to_bin = 0;
        }
        if(Q2_xB_Bin_2 == 2){
            add_to_bin = 49;
        }
        if(Q2_xB_Bin_2 == 3){
            add_to_bin = 98;
        }
        if(Q2_xB_Bin_2 == 4){
            add_to_bin = 147;
        }
        if(Q2_xB_Bin_2 == 5){
            add_to_bin = 189;
        }
        if(Q2_xB_Bin_2 == 6){
            add_to_bin = 225;
        }
        if(Q2_xB_Bin_2 == 7){
            add_to_bin = 250;
        }
        if(Q2_xB_Bin_2 == 8){
            add_to_bin = 275;
        }

        Bin_Res_4D = z_pT_Bin_2 + add_to_bin;

        return Bin_Res_4D;

    
    """)
    

    
    rdf = rdf.Define('Bin_4D_OG', """

        int add_to_bin = 0;
        int Bin_4D_OG = -1;

        if(Q2_xB_Bin == 0){
            Bin_4D_OG = -1;
            return Bin_4D_OG;
        }
        if(Q2_xB_Bin == 1){
            add_to_bin = 0;
        }
        if(Q2_xB_Bin == 2){
            add_to_bin = 50;
        }
        if(Q2_xB_Bin == 3){
            add_to_bin = 100;
        }
        if(Q2_xB_Bin == 4){
            add_to_bin = 150;
        }
        if(Q2_xB_Bin == 5){
            add_to_bin = 193;
        }
        if(Q2_xB_Bin == 6){
            add_to_bin = 243;
        }
        if(Q2_xB_Bin == 7){
            add_to_bin = 269;
        }
        if(Q2_xB_Bin == 8){
            add_to_bin = 306;
        }
        if(Q2_xB_Bin == 9){
            add_to_bin = 327;
        }

        Bin_4D_OG = z_pT_Bin + add_to_bin;

        return Bin_4D_OG;

    """)
    
    
    
    rdf = rdf.Define('Bin_Res_4D_OG', """
    
        int add_to_bin = 0;
        int Bin_Res_4D_OG = -1;

        if(Q2_xB_Bin == 0 || z_pT_Bin == 0){
            Bin_Res_4D_OG = -1;
            return Bin_Res_4D_OG;
            // Events outside of either binning scheme is automatically given a Bin_Res_4D bin value of -1
            // No spaces are given between bins
        }
        if(Q2_xB_Bin == 1){
            add_to_bin = 0;
        }
        if(Q2_xB_Bin == 2){
            add_to_bin = 49;
        }
        if(Q2_xB_Bin == 3){
            add_to_bin = 98;
        }
        if(Q2_xB_Bin == 4){
            add_to_bin = 147;
        }
        if(Q2_xB_Bin == 5){
            add_to_bin = 189;
        }
        if(Q2_xB_Bin == 6){
            add_to_bin = 238;
        }
        if(Q2_xB_Bin == 7){
            add_to_bin = 263;
        }
        if(Q2_xB_Bin == 8){
            add_to_bin = 299;
        }
        if(Q2_xB_Bin == 9){
            add_to_bin = 319;
        }

        Bin_Res_4D_OG = z_pT_Bin + add_to_bin;

        return Bin_Res_4D_OG;
    
    """)


    if(datatype == "mdf" or datatype == "pdf"):
        rdf = rdf.Define('Bin_4D_smeared', """

            int add_to_bin = 0;
            int Bin_4D_smeared = -1; // Updated on 7-19-2022

            if(Q2_xB_Bin_2_smeared == 0){
                Bin_4D_smeared = -1; // Updated on 7-19-2022
                return Bin_4D_smeared;
            }
            if(Q2_xB_Bin_2_smeared == 1){
                add_to_bin = 0;
            }
            if(Q2_xB_Bin_2_smeared == 2){
                add_to_bin = 50;
            }
            if(Q2_xB_Bin_2_smeared == 3){
                add_to_bin = 100;
            }
            if(Q2_xB_Bin_2_smeared == 4){
                add_to_bin = 150;
            }
            if(Q2_xB_Bin_2_smeared == 5){
                add_to_bin = 193;
            }
            if(Q2_xB_Bin_2_smeared == 6){
                add_to_bin = 230;
            }
            if(Q2_xB_Bin_2_smeared == 7){
                add_to_bin = 256;
            }
            if(Q2_xB_Bin_2_smeared == 8){
                add_to_bin = 283;
            }

            Bin_4D_smeared = z_pT_Bin_2_smeared + add_to_bin;

            return Bin_4D_smeared;

        """)
        
        rdf = rdf.Define('Bin_Res_4D_smeared', """

            int add_to_bin = 0;
            int Bin_Res_4D_smeared = -1;

            if(Q2_xB_Bin_2_smeared == 0 || z_pT_Bin_2_smeared == 0){
                Bin_Res_4D_smeared = -1;
                return Bin_Res_4D_smeared;
                // Events outside of either binning scheme is automatically given a Bin_Res_4D_smeared bin value of -1
                // No spaces are given between bins
            }
            if(Q2_xB_Bin_2_smeared == 1){
                add_to_bin = 0;
            }
            if(Q2_xB_Bin_2_smeared == 2){
                add_to_bin = 49;
            }
            if(Q2_xB_Bin_2_smeared == 3){
                add_to_bin = 98;
            }
            if(Q2_xB_Bin_2_smeared == 4){
                add_to_bin = 147;
            }
            if(Q2_xB_Bin_2_smeared == 5){
                add_to_bin = 189;
            }
            if(Q2_xB_Bin_2_smeared == 6){
                add_to_bin = 225;
            }
            if(Q2_xB_Bin_2_smeared == 7){
                add_to_bin = 250;
            }
            if(Q2_xB_Bin_2_smeared == 8){
                add_to_bin = 275;
            }

            Bin_Res_4D_smeared = z_pT_Bin_2_smeared + add_to_bin;

            return Bin_Res_4D_smeared;

        """)

        rdf = rdf.Define('Bin_4D_OG_smeared', """

            int add_to_bin = 0;
            int Bin_4D_OG_smeared = -1;

            if(Q2_xB_Bin_smeared == 0){
                Bin_4D_OG_smeared = -1;
                return Bin_4D_OG_smeared;
            }
            if(Q2_xB_Bin_smeared == 1){
                add_to_bin = 0;
            }
            if(Q2_xB_Bin_smeared == 2){
                add_to_bin = 50;
            }
            if(Q2_xB_Bin_smeared == 3){
                add_to_bin = 100;
            }
            if(Q2_xB_Bin_smeared == 4){
                add_to_bin = 150;
            }
            if(Q2_xB_Bin_smeared == 5){
                add_to_bin = 193;
            }
            if(Q2_xB_Bin_smeared == 6){
                add_to_bin = 243;
            }
            if(Q2_xB_Bin_smeared == 7){
                add_to_bin = 269;
            }
            if(Q2_xB_Bin_smeared == 8){
                add_to_bin = 306;
            }
            if(Q2_xB_Bin_smeared == 9){
                add_to_bin = 327;
            }

            Bin_4D_OG_smeared = z_pT_Bin_smeared + add_to_bin;

            return Bin_4D_OG_smeared;

        """)
        
        rdf = rdf.Define('Bin_Res_4D_OG_smeared', """

            int add_to_bin = 0;
            int Bin_Res_4D_OG_smeared = -1;

            if(Q2_xB_Bin_smeared == 0 || z_pT_Bin_smeared == 0){
                Bin_Res_4D_OG_smeared = -1;
                return Bin_Res_4D_OG_smeared;
                // Events outside of either binning scheme is automatically given a Bin_Res_4D_OG_smeared bin value of -1
                // No spaces are given between bins
            }
            if(Q2_xB_Bin_smeared == 1){
                add_to_bin = 0;
            }
            if(Q2_xB_Bin_smeared == 2){
                add_to_bin = 49;
            }
            if(Q2_xB_Bin_smeared == 3){
                add_to_bin = 98;
            }
            if(Q2_xB_Bin_smeared == 4){
                add_to_bin = 147;
            }
            if(Q2_xB_Bin_smeared == 5){
                add_to_bin = 189;
            }
            if(Q2_xB_Bin_smeared == 6){
                add_to_bin = 238;
            }
            if(Q2_xB_Bin_smeared == 7){
                add_to_bin = 263;
            }
            if(Q2_xB_Bin_smeared == 8){
                add_to_bin = 299;
            }
            if(Q2_xB_Bin_smeared == 9){
                add_to_bin = 319;
            }

            Bin_Res_4D_OG_smeared = z_pT_Bin_smeared + add_to_bin;

            return Bin_Res_4D_OG_smeared;

        """)
        
        
        rdf = rdf.Define('Bin_4D_gen', """
        
            int add_to_bin = 0;
            int Bin_4D_gen = -1; // Updated on 7-19-2022
            
            
            if(PID_el == 0 || PID_pip == 0){
                // Event is unmatched
                Bin_4D_gen = -2; // Added on 7-19-2022
                return Bin_4D_gen;
                
                // When a reconstructed event does not have a matching generated event, the missing generated bin will be defined as bin = -2
                // bin = -1 is given to matched event that did not land in any defined Q2-xB bins
                // bin = 0 is given to events which land within the boarders of the first Q2-xB but does not land in any z-pT bins
                // Note: Only bin = -2 is unique to the 'Bin_4D_gen' variable. "bin = -1" and "bin = 0" hold identical meanings for all other datasets to which this scheme is applied
                
            }
            
            if(Q2_xB_Bin_2_gen == 0){
                Bin_4D_gen = -1; // Updated on 7-19-2022
                return Bin_4D_gen;
            }
            if(Q2_xB_Bin_2_gen == 1){
                add_to_bin = 0;
            }
            if(Q2_xB_Bin_2_gen == 2){
                add_to_bin = 50;
            }
            if(Q2_xB_Bin_2_gen == 3){
                add_to_bin = 100;
            }
            if(Q2_xB_Bin_2_gen == 4){
                add_to_bin = 150;
            }
            if(Q2_xB_Bin_2_gen == 5){
                add_to_bin = 193;
            }
            if(Q2_xB_Bin_2_gen == 6){
                add_to_bin = 230;
            }
            if(Q2_xB_Bin_2_gen == 7){
                add_to_bin = 256;
            }
            if(Q2_xB_Bin_2_gen == 8){
                add_to_bin = 283;
            }
            
            Bin_4D_gen = z_pT_Bin_2_gen + add_to_bin;
            
            return Bin_4D_gen;
        
        """)
        
        
        rdf = rdf.Define('Bin_Res_4D_gen', """

            int add_to_bin = 0;
            int Bin_Res_4D_gen = -1;
            
            if(PID_el == 0 || PID_pip == 0){
                // Event is unmatched
                Bin_Res_4D_gen = -2;
                return Bin_Res_4D_gen;
                
                // When a reconstructed event does not have a matching generated event, the missing generated bin will be defined as bin = -2
                // bin = -1 is given to matched event that did not land in any defined Q2-xB or z-pT bins
                // bin = 0 is empty, in keeping with prior definitions of the binning schemes (may change later)
                // Other 'Bin_Res_4D' binning schemes are identical to this except for the addition of the -2 bin
                
            }

            if(Q2_xB_Bin_2_gen == 0 || z_pT_Bin_2_gen == 0){
                Bin_Res_4D_gen = -1;
                return Bin_Res_4D_gen;
            }
            if(Q2_xB_Bin_2_gen == 1){
                add_to_bin = 0;
            }
            if(Q2_xB_Bin_2_gen == 2){
                add_to_bin = 49;
            }
            if(Q2_xB_Bin_2_gen == 3){
                add_to_bin = 98;
            }
            if(Q2_xB_Bin_2_gen == 4){
                add_to_bin = 147;
            }
            if(Q2_xB_Bin_2_gen == 5){
                add_to_bin = 189;
            }
            if(Q2_xB_Bin_2_gen == 6){
                add_to_bin = 225;
            }
            if(Q2_xB_Bin_2_gen == 7){
                add_to_bin = 250;
            }
            if(Q2_xB_Bin_2_gen == 8){
                add_to_bin = 275;
            }

            Bin_Res_4D_gen = z_pT_Bin_2_gen + add_to_bin;

            return Bin_Res_4D_gen;


        """)
        
        
        
        rdf = rdf.Define('Bin_4D_OG_gen', """
        
            int add_to_bin = 0;
            int Bin_4D_OG_gen = -1;
            
            
            if(PID_el == 0 || PID_pip == 0){
                // Event is unmatched
                Bin_4D_OG_gen = -2;
                return Bin_4D_OG_gen;
                
                // When a reconstructed event does not have a matching generated event, the missing generated bin will be defined as bin = -2
                // bin = -1 is given to matched event that did not land in any defined Q2-xB bins
                // bin = 0 is given to events which land within the boarders of the first Q2-xB but does not land in any z-pT bins
                // Note: Only bin = -2 is unique to the 'Bin_4D_OG_gen' variable. "bin = -1" and "bin = 0" hold identical meanings for all other datasets to which this scheme is applied
                
            }
            
            if(Q2_xB_Bin_gen == 0){
                Bin_4D_OG_gen = -1;
                return Bin_4D_OG_gen;
            }
            if(Q2_xB_Bin_gen == 1){
                add_to_bin = 0;
            }
            if(Q2_xB_Bin_gen == 2){
                add_to_bin = 50;
            }
            if(Q2_xB_Bin_gen == 3){
                add_to_bin = 100;
            }
            if(Q2_xB_Bin_gen == 4){
                add_to_bin = 150;
            }
            if(Q2_xB_Bin_gen == 5){
                add_to_bin = 193;
            }
            if(Q2_xB_Bin_gen == 6){
                add_to_bin = 243;
            }
            if(Q2_xB_Bin_gen == 7){
                add_to_bin = 269;
            }
            if(Q2_xB_Bin_gen == 8){
                add_to_bin = 306;
            }
           if(Q2_xB_Bin_gen == 9){
                add_to_bin = 327;
            }
            
            Bin_4D_OG_gen = z_pT_Bin_gen + add_to_bin;
            
            return Bin_4D_OG_gen;
        
        """)
        
        
        rdf = rdf.Define('Bin_Res_4D_OG_gen', """

            int add_to_bin = 0;
            int Bin_Res_4D_OG_gen = -1;
            
            if(PID_el == 0 || PID_pip == 0){
                // Event is unmatched
                Bin_Res_4D_OG_gen = -2;
                return Bin_Res_4D_OG_gen;
                
                // When a reconstructed event does not have a matching generated event, the missing generated bin will be defined as bin = -2
                // bin = -1 is given to matched event that did not land in any defined Q2-xB or z-pT bins
                // bin = 0 is empty, in keeping with prior definitions of the binning schemes (may change later)
                // Other 'Bin_Res_4D' binning schemes are identical to this except for the addition of the -2 bin
                
            }
            
            if(Q2_xB_Bin_gen == 0 || z_pT_Bin_gen == 0){
                Bin_Res_4D_OG_gen = -1;
                return Bin_Res_4D_OG_gen;
            }
            if(Q2_xB_Bin_gen == 1){
                add_to_bin = 0;
            }
            if(Q2_xB_Bin_gen == 2){
                add_to_bin = 49;
            }
            if(Q2_xB_Bin_gen == 3){
                add_to_bin = 98;
            }
            if(Q2_xB_Bin_gen == 4){
                add_to_bin = 147;
            }
            if(Q2_xB_Bin_gen == 5){
                add_to_bin = 189;
            }
            if(Q2_xB_Bin_gen == 6){
                add_to_bin = 238;
            }
            if(Q2_xB_Bin_gen == 7){
                add_to_bin = 263;
            }
            if(Q2_xB_Bin_gen == 8){
                add_to_bin = 299;
            }
            if(Q2_xB_Bin_gen == 9){
                add_to_bin = 319;
            }

            Bin_Res_4D_OG_gen = z_pT_Bin_gen + add_to_bin;

            return Bin_Res_4D_OG_gen;

        """)
        

        
        
        
        
    ##===================================================##
    ##=====##=====##   5D Kinematic Bins   ##=====##=====##
    ##===================================================##
        
    rdf = rdf.Define('Bin_5D', """
    int phi_t_bin = (phi_t/10) + 1;
    auto Bin_5D = Bin_4D + phi_t_bin;
    if(phi_t_bin < 0 || phi_t_bin > 37){
        // The phi angle should not be less than 0˚ or greater than 360˚ (by definition, there should not be any overflow bins)
        Bin_5D = -2;
    }
    return Bin_5D;
    """)
    
    rdf = rdf.Define('Bin_5D_OG', """
    int phi_t_bin = (phi_t/10) + 1;
    auto Bin_5D_OG = Bin_4D_OG + phi_t_bin;
    if(phi_t_bin < 0 || phi_t_bin > 37){
        // The phi angle should not be less than 0˚ or greater than 360˚ (by definition, there should not be any overflow bins)
        Bin_5D_OG = -2;
    }
    return Bin_5D_OG;
    """)
    
    if(datatype in ["mdf", "pdf"]):
        rdf = rdf.Define('Bin_5D_smeared', """
        int phi_t_bin_smeared = (smeared_vals[11]/10) + 1;
        auto Bin_5D_smeared = Bin_4D_smeared + phi_t_bin_smeared;
        if(phi_t_bin_smeared < 0 || phi_t_bin_smeared > 37){
            // The phi angle should not be less than 0˚ or greater than 360˚ (by definition, there should not be any overflow bins)
            Bin_5D_smeared = -2;
        }
        return Bin_5D_smeared;
        """)
        rdf = rdf.Define('Bin_5D_OG_smeared', """
        int phi_t_bin_smeared = (smeared_vals[11]/10) + 1;
        auto Bin_5D_OG_smeared = Bin_4D_OG_smeared + phi_t_bin_smeared;
        if(phi_t_bin_smeared < 0 || phi_t_bin_smeared > 37){
            // The phi angle should not be less than 0˚ or greater than 360˚ (by definition, there should not be any overflow bins)
            Bin_5D_OG_smeared = -2;
        }
        return Bin_5D_OG_smeared;
        """)
    
        rdf = rdf.Define('Bin_5D_gen', """
        int phi_t_bin_gen = (phi_t_gen/10) + 1;
        auto Bin_5D_gen = Bin_4D_gen + phi_t_bin_gen;
        if(phi_t_bin_gen < 0 || phi_t_bin_gen > 37){
            // The phi angle should not be less than 0˚ or greater than 360˚ (by definition, there should not be any overflow bins)
            Bin_5D_gen = -3;
        }
        return Bin_5D_gen;
        """)
        
        rdf = rdf.Define('Bin_5D_OG_gen', """
        int phi_t_bin_gen = (phi_t_gen/10) + 1;
        auto Bin_5D_OG_gen = Bin_4D_OG_gen + phi_t_bin_gen;
        if(phi_t_bin_gen < 0 || phi_t_bin_gen > 37){
            // The phi angle should not be less than 0˚ or greater than 360˚ (by definition, there should not be any overflow bins)
            Bin_5D_OG_gen = -3;
        }
        return Bin_5D_OG_gen;
        """)
        
        
        
        
        
    #####################     Generated Bin Definitions     #####################
    #############################################################################
    #####################      Matched Bin Definitions      #####################


##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    
    def Bin_Purity_Filter_Fuction(dataframe, variable, min_range, max_range, number_of_bins):

        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])


        if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable or "Bin_4D" in variable or "Bin_5D" in variable):

            if("sec" in variable):
                gen_variable = gen_variable.replace("_a", "")

            filter_name = "".join([variable, " == ", gen_variable, " && ", variable, " != 0"])

        else:

            bin_size = (max_range - min_range)/number_of_bins


            filter_name = "".join(["""

            // cout<<endl<<"Starting a new line of purity filtering..."<<endl;

            int rec_bin = (""", str(variable), """ - """, str(min_range), """)/""", str(bin_size), """;
            int gen_bin = (""", str(gen_variable), """ - """, str(min_range), """)/""", str(bin_size), """;

            // cout<<endl<<"The reconstructed event (with the value Name_""", str(variable), """ = "<<""", str(variable), """<<") was found in bin "<<rec_bin<<" (Range = "<<(""", str(min_range), """ + (rec_bin)*""", str(bin_size), """)<<" --> "<<(""", str(min_range), """ + (rec_bin + 1)*""", str(bin_size), """)<<")"<<endl;
            // cout<<"The generated event (with the value Name_""", str(gen_variable), """ = "<<""", str(gen_variable), """<<") was found in bin "<<gen_bin<<" (Range = "<<(""", str(min_range), """ + (gen_bin)*""", str(bin_size), """)<<" --> "<<(""", str(min_range), """ + (gen_bin + 1)*""", str(bin_size), """)<<")"<<endl<<endl;


            bool filter_Q = (rec_bin == gen_bin && PID_el != 0 && PID_pip != 0);


            return filter_Q;



            """])


        return dataframe.Filter(str(filter_name))
    
    
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    def Bin_Number_Variable_Function(DF, Variable, min_range, max_range, number_of_bins, DF_Type=datatype):
        
        # if("Q2_xB_Bin" in Variable or "z_pT_Bin" in Variable or "sec" in Variable or "Bin_4D" in Variable or "Bin_5D" in Variable):
        #     # Already defined
        #     return DF
        
        if((("Bin" in Variable) or ("sec" in Variable)) or (DF == "continue") or ("Combined_" in Variable)):
            # Already defined
            return DF
        
        else:
            
            GEN_Variable = "".join([Variable.replace("_smeared", ""), "_gen"])

            out_put_DF = DF

            bin_size = (max_range - min_range)/number_of_bins

            rec_bin = "".join(["""

            int rec_bin = ((""", str(Variable), """ - """, str(min_range), """)/""", str(bin_size), """) + 1;

            if(""", str(Variable), """ < """, str(min_range), """){
                // Below binning range
                rec_bin = 0;
            }

            if(""", str(Variable), """ > """, str(max_range), """){
                // Above binning range
                rec_bin = """, str(number_of_bins + 1), """;
            }

            return rec_bin;

            """])


            gen_bin = "".join(["""

            int gen_bin = ((""", str(GEN_Variable), """ - """, str(min_range), """)/""", str(bin_size), """) + 1;

            if(""", str(GEN_Variable), """ < """, str(min_range), """){
                // Below binning range
                gen_bin = 0;
            }

            if(""", str(GEN_Variable), """ > """, str(max_range), """){
                // Above binning range
                gen_bin = """, str(number_of_bins + 1), """;
            }

            if(PID_el == 0 || PID_pip == 0){
                // Event is unmatched
                gen_bin = """, str(number_of_bins + 2), """;
            }

            return gen_bin;

            """])

            out_put_DF = out_put_DF.Define("".join([str(Variable), "_REC_BIN"]), rec_bin)
            if(DF_Type not in ["rdf", "gdf"]):
                out_put_DF = out_put_DF.Define("".join([str(Variable), "_GEN_BIN"]), gen_bin)


        return out_put_DF


##########################################################################################################################################################################################
##########################################################################################################################################################################################

    def Multi_Dimensional_Bin_Construction(DF, Variables_To_Combine, Smearing_Q="", Data_Type=datatype, return_option="DF"):
        # print("".join(["Combining Variables: Multi_Dimensional_Bin_Construction(DF, Variables_To_Combine='", str(Variables_To_Combine), "', Smearing_Q='", str(Smearing_Q), "', Data_Type='", str(Data_Type), "', return_option='", str(return_option), "')"]))
        # Try to test later in the randomly generated rdataframe (see 'MC_DataFrame_Volume_Calculation.ipynb')
        # When combining variables, each subsequent entry in the list 'Variables_To_Combine' will be inserted within the previous variable
            # Therefore, to see the phi_h distribution in a combined Q2-xB-z-pT bin, let Variables_To_Combine = [['Q2-xB bin info'], ['z-pT bin info'], ['phi_h info']]
            # For the bin info of the Q2-xB/z-pT bins, make sure that the Min_Bin = 0 and Max_Bin = Num_Bin
            # Note: This function should be able to combine any number of variables, but the rest of the code may not be optimized to combine 4 variables at the same time (rewrite other parts of code if this becomes necessary)
        DF_Res_Error = False # Helps trigger error message for when this function fails to calculate the variables for the response matrices
        try:
            if(DF == "continue"):
                return "continue"
            if(list is not type(Variables_To_Combine) or len(Variables_To_Combine) <= 1):
                print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dimensional_Bin_Construction...\nImproper information was provided to combine multidimensional bins\n", color.END, color.RED, "Must provide a list of variables to combine with the input parameter: 'Variables_To_Combine'", color.END]))
                if(return_option == "DF"):
                    return DF
                else:
                    return Variables_To_Combine
            else:
                
                Vars_Data_Type_Output = [""] if((return_option != "DF_Res") or (Data_Type in ["rdf", "gdf"])) else ["", "_gen"]
                
                for rec_or_gen in Vars_Data_Type_Output:
                    try:
                        variable_name_1, Min_Bin_1, Max_Bin_1, Num_Bin_1 = Variables_To_Combine[0]
                        Bin_Size_1 = (Max_Bin_1 - Min_Bin_1)/Num_Bin_1
                        Bin_Group_Numbers = Num_Bin_1

                        if(rec_or_gen == ""):
                            if((Smearing_Q != "") and ("_smeared" not in variable_name_1)):
                                print("".join([color.RED, color.BOLD, "ERROR: MISSING SMEARING OPTION DURING Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ")", color.END]))
                                variable_name_1 = "".join([str(variable_name_1), "_smeared"])
                            if((Smearing_Q == "") and ("_smeared" in variable_name_1)):
                                print("".join([color.RED, color.BOLD, "ERROR: SMEARING OPTION NOT SELECTED DURING Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ")", color.END]))
                                variable_name_1 = str(variable_name_1).replace("_smeared", "")
                        else:
                            variable_name_1 = "".join([str(variable_name_1).replace("_smeared", ""), "_gen"])


                        # Combined_Bin_All = "".join(["""
                        # int Combined_Bin_Start = ((""", str(variable_name_1), """ - """, str(Min_Bin_1), """)/""", str(Bin_Size_1), """) + 1;
                        # if(""", str(variable_name_1), """ < """, str(Min_Bin_1), """){
                        #     // Below binning range
                        #     Combined_Bin_Start = 0;
                        # }
                        # if(""", str(variable_name_1), """ > """, str(Max_Bin_1), """){
                        #     // Above binning range
                        #     Combined_Bin_Start = """, str(Num_Bin_1 + 1), """;
                        # }
                        # """])

                        Combined_Bin_All = "".join(["""
    int Combined_Bin_Final = 0;
    int Combined_Bin_Start = ((""", str(variable_name_1), """ - """, str(Min_Bin_1), """)/""", str(Bin_Size_1), """) + 1;
    if((""", str(variable_name_1), """ < """, str(Min_Bin_1), """) || (""", str(variable_name_1), """ > """, str(Max_Bin_1), """)){
        // Outside binning range (will only combine events which are within all given binning schemes)
        Combined_Bin_Final = -1;
        return Combined_Bin_Final;
    }
    Combined_Bin_Final = Combined_Bin_Start;
                        """])

                    except:
                        print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dimensional_Bin_Construction...\nError in retriving base variable for new multidimensional bin variable.\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))   


                    if(("DF" in return_option) and (rec_or_gen == "")):
                        try:
                            if(Smearing_Q != ""):
                                DF_Final = smear_frame_compatible(DF, variable_name_1, Smearing_Q)
                            else:
                                DF_Final = DF
                        except:
                            print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dimensional_Bin_Construction...\nError in smearing.\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))   


                    Combined_Bin_Title = "".join(["Combined_", str(variable_name_1)])

                    for variable_binning in Variables_To_Combine:
                        variable_name, Min_Bin, Max_Bin, Num_Bin = variable_binning
                        Bin_Size = (Max_Bin - Min_Bin)/Num_Bin

                        if(rec_or_gen == ""):
                            if((Smearing_Q != "") and ("_smeared" not in variable_name)):
                                print("".join([color.RED, "ERROR: MISSING (SECONDARY) SMEARING OPTION DURING Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ")", color.END]))
                                variable_name = "".join([str(variable_name), "_smeared"])
                            if((Smearing_Q == "") and ("_smeared" in variable_name_1)):
                                print("".join([color.RED, "ERROR: (SECONDARY) SMEARING OPTION NOT SELECTED DURING Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ")", color.END]))
                                variable_name = str(variable_name).replace("_smeared", "")
                            if((("_smeared" in variable_name_1) and ("_smeared" not in variable_name)) or (("_smeared" not in variable_name_1) and ("_smeared" in variable_name))):
                                print("".join([color.BOLD, color.RED, "/nMAJOR WARNING: COMBINING VARIABLES THAT DO NOT HAVE THE SAME SMEARING OPTION APPLIED (CHECK Multi_Dimensional_Bin_Construction(Variables_To_Combine=", str(Variables_To_Combine), ") MANUALLY)\n", color.END]))
                        else:
                            variable_name = "".join([str(variable_name).replace("_smeared", ""), "_gen"])
                            
                        if(variable_name_1 == variable_name):
                            # Skip first variable in list
                            continue

                        if(("DF" in return_option) and (rec_or_gen == "")):
                            try:
                                if(Smearing_Q != ""):
                                    DF_Final = smear_frame_compatible(DF_Final, variable_name, Smearing_Q)
                            except:
                                print("".join([color.BOLD, color.RED, "ERROR IN Multi_Dimensional_Bin_Construction...\nError in smearing.\nTraceback:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))   


                        Combined_Bin_All = "".join([Combined_Bin_All, """
    int Combined_Add_""", str(variable_name), """ = ((""", str(variable_name), """ - """, str(Min_Bin), """)/""", str(Bin_Size), """);
    if((""", str(variable_name), """ < """, str(Min_Bin), """) || (""", str(variable_name), """ > """, str(Max_Bin), """)){
        // Outside binning range (will only combine events which are within all given binning schemes)
        Combined_Bin_Final = -1;
        return Combined_Bin_Final;
    }
    Combined_Bin_Final += (""", str(Bin_Group_Numbers), """*Combined_Add_""", str(variable_name), """);
                        """])

                        Bin_Group_Numbers = Bin_Group_Numbers*Num_Bin
                        Combined_Bin_Title = "".join([str(Combined_Bin_Title.replace("_smeared", "")).replace("_gen", ""), "_", str(variable_name)])
                        if((rec_or_gen != "") and ("_gen" not in Combined_Bin_Title)):
                            Combined_Bin_Title = "".join([str(Combined_Bin_Title), "_gen"])

                    Combined_Bin_All = "".join([Combined_Bin_All, """
    return Combined_Bin_Final;"""])

                    if(return_option == "DF"):
                        try:
                            DF_Final = DF_Final.Define(str(Combined_Bin_Title), str(Combined_Bin_All))
                            return DF_Final
                        except:
                            print("".join([color.BOLD, color.RED, "\nERROR IN FINAL STEP OF Multi_Dimensional_Bin_Construction:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
                    elif(return_option == "DF_Res"):
                        try:
                            # print("".join(["DF_Final = DF_Final.Define(", str(Combined_Bin_Title), ", ", str(Combined_Bin_All), ")"]))
                            DF_Final = DF_Final.Define(str(Combined_Bin_Title), str(Combined_Bin_All))
                        except:
                            print("".join([color.BOLD, color.RED, "\nERROR IN FINAL STEP OF Multi_Dimensional_Bin_Construction:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
                    else:
                        return [str(Combined_Bin_Title), -1.5, Bin_Group_Numbers + 1.5, Bin_Group_Numbers + 3]
            
        except:
            print("".join([color.BOLD, color.RED, "\n\nMAJOR ERROR IN Multi_Dimensional_Bin_Construction:\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
            DF_Res_Error = True
           
        if(return_option != "DF_Res" or DF_Res_Error):
            print("".join([color.BOLD, color.RED, "\n\nMAJOR ERROR IN Multi_Dimensional_Bin_Construction:\nFAILURE TO RETURN ANYTHING", color.END]))
            return DF
        else:
            return DF_Final
         
    
##########################################################################################################################################################################################
##########################################################################################################################################################################################

    def Delta_Matched_DF(dataframe, variable):
        output = "continue"
        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
        if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable or dataframe == "continue"):
            # Cannot uses these types of variables in this type of histogram
            return "continue"
        else:
            output = dataframe.Define("Delta_Matched_Value", "".join([str(variable), " - ", str(gen_variable)]))

        return output


##########################################################################################################################################################################################
##########################################################################################################################################################################################


    def Delta_Matched_Bin_Calc(Variable, Min_Bin, Max_Bin):
        output = "continue"
        Min_Dif, Max_Dif = (Min_Bin - Max_Bin), (Max_Bin - Min_Bin)

        if("th" in Variable):
            Min_Dif, Max_Dif = -6, 6

        if("Phi" in Variable):
            Min_Dif, Max_Dif = -10, 10

        Num_of_Bins = int((Max_Dif - Min_Dif)/0.005)
        if(Num_of_Bins < 400):
            Num_of_Bins = 400
        elif(Num_of_Bins < 200):
            Num_of_Bins = 200
        elif(Num_of_Bins > 1500):
            Num_of_Bins = 1500
        elif(Num_of_Bins > 1200):
            Num_of_Bins = 1200
        elif(Num_of_Bins > 800):
            Num_of_Bins = 800
        else:
            Num_of_Bins = 600
        if(((Max_Dif - Min_Dif)/Num_of_Bins) > 1 and (Max_Dif - Min_Dif) < 800):
            Num_of_Bins = int(Max_Dif - Min_Dif)


        output = [Num_of_Bins, Min_Dif, Max_Dif]

        return output
    
    
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    
    
    ###################################################################################################################################################################
    ###################################################                 Done With Kinematic Binning                 ###################################################
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###----------------------------------------------##-------------------------------------------------------------##----------------------------------------------###
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###################################################          Defining Helpful Functions for Histograms          ###################################################
    ###################################################################################################################################################################

    
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    
    ###################=========================###################
    ##===============##     Variable Titles     ##===============##
    ###################=========================###################
    
    def variable_Title_name(variable):

        smeared_named, bank_named = '', ''
        
        if("_smeared" in variable):
            smeared_named = 'yes'
            variable = variable.replace("_smeared","")
            
        if("_gen" in variable):
            bank_named = 'yes'
            variable = variable.replace("_gen","")
        
        output = 'error'    

        if(variable == 'el_E'):
            output = 'E_{el}'
        if(variable == 'pip_E'):
            output = 'E_{#pi^{+}}'
        if(variable == 'el'):
            output = "p_{el}"
        if(variable == 'pip'):
            output = "p_{#pi^{+}}"
        if(variable == 'elth'):
            output = "#theta_{el}"
        if(variable == 'pipth'):
            output = "#theta_{#pi^{+}}"
        if(variable == 'elPhi'):
            output = "#phi_{el}"
        if(variable == 'pipPhi'):
            output = "#phi_{#pi^{+}}"
        if(variable == 'MM'):
            output = "Missing Mass"
        if(variable == 'MM2'):
            output = "Missing Mass^{2}"
        if(variable == 'Q2'):
            output = "Q^{2}"
        if(variable == 'xB'):
            output = "x_{B}"
        if(variable == 'v'):
            output = "#nu (lepton energy loss)"
        if(variable == 's'):
            output = "s (CM Energy^{2})"
        if(variable == 'W'):
            output = "W (Invariant Mass)"
        if(variable == 'y'):
            output = "y (lepton energy loss fraction)"
        if(variable == 'z'):
            output = "z"
        if(variable == 'epsilon'):
            output = "#epsilon"
        if(variable == 'pT'):
            output = "P_{T}"
        if(variable in ['phi_t', 'phi_h']):
            output = "#phi_{h}"
        if(variable == 'xF'):
            output = "x_{F} (Feynman x)"
        if(variable == 'pipx_CM'):
            output = "CM p_{#pi^{+}} in #hat{x}"
        if(variable == 'pipy_CM'):
            output = "CM p_{#pi^{+}} in #hat{y}"
        if(variable == 'pipz_CM'):
            output = "CM p_{#pi^{+}} in #hat{z}"
        if(variable == 'qx_CM'):
            output = "CM p_{q} in #hat{x}"
        if(variable == 'qy_CM'):
            output = "CM p_{q} in #hat{y}"
        if(variable == 'qz_CM'):
            output = "CM p_{q} in #hat{z}"
        if(variable == 'beamX_CM'):
            output = "CM p_{beam} in #hat{x}"
        if(variable == 'beamY_CM'):
            output = "CM p_{beam} in #hat{y}"
        if(variable == 'beamZ_CM'):
            output = "CM p_{beam} in #hat{z}"
        if(variable == 'eleX_CM'):
            output = "CM p_{el} in #hat{x}"
        if(variable == 'eleY_CM'):
            output = "CM p_{el} in #hat{y}"
        if(variable == 'eleZ_CM'):
            output = "CM p_{el} in #hat{z}"
        if(variable == 'event'):
            output = "Event Number"
        if(variable == 'runN'):
            output = "Run Number"
        if(variable == 'ex'):
            output = "Lab p_{el} in #hat{x}"
        if(variable == 'ey'):
            output = "Lab p_{el} in #hat{y}"
        if(variable == 'ez'):
            output = "Lab p_{el} in #hat{z}"
        if(variable == 'px'):
            output = "Lab p_{#pi^{+}} in #hat{x}"
        if(variable == 'py'):
            output = "Lab p_{#pi^{+}} in #hat{y}"
        if(variable == 'pz'):
            output = "Lab p_{#pi^{+}} in #hat{z}"
        if(variable == 'esec'):
            output = "Electron Sector"
        if(variable == 'pipsec'):
            output = "#pi^{+} Sector"
        # if(variable == 'esec_a'):
        if('esec_a' in variable):
            output = "Electron Sector (Angle Def)"
        # if(variable == 'pipsec_a'):
        if('pipsec_a' in variable):
            output = "#pi^{+} Sector (Angle Def)"
        if(variable == 'Q2_xB_Bin'):
            output = "Q^{2}-x_{B} Bin"
        if(variable == 'Q2_xB_Bin_2'):
            output = "Q^{2}-x_{B} Bin (New)"
        if(variable == 'z_pT_Bin'):
            output = "z-P_{T} Bin"
        if(variable == 'z_pT_Bin_2'):
            output = "z-P_{T} Bin (New)"
        if(variable == 'elec_events_found'):
            output = "Number of Electrons Found"
        if(variable == 'Delta_Smear_El_P'):
            output = "#Delta_{Smeared}p_{el}"
        if(variable == 'Delta_Smear_El_Th'):
            output = "#Delta_{Smeared}#theta_{el}"
        if(variable == 'Delta_Smear_El_Phi'):
            output = "#Delta_{Smeared}#phi_{el}"
        if(variable == 'Delta_Smear_Pip_P'):
            output = "#Delta_{Smeared}p_{#pi^{+}}"
        if(variable == 'Delta_Smear_Pip_Th'):
            output = "#Delta_{Smeared}#theta_{#pi^{+}}"
        if(variable == 'Delta_Smear_Pip_Phi'):
            output = "#Delta_{Smeared}#phi_{#pi^{+}}"
        if("Bin_4D" in variable):
            output = "".join(["Combined 4D Bin", " (Original)" if("OG" in variable) else ""])
        if("Bin_5D" in variable):
            output = "".join(["Combined 5D Bin", " (Original)" if("OG" in variable) else ""])
        if("Bin_Res_4D" in variable):
            output = "".join(["Q^{2}-x_{B}-z-P_{T} Bin", " (Original)" if("OG" in variable) else ""])
        if("Combined_" in variable):
            output = "".join(["Combined Binning: ", str(variable.replace("Combined_", ""))])
            

        if(smeared_named == 'yes'):
            output = "".join([output, " (Smeared)"])
            
        if(bank_named == 'yes'):
            output = "".join([output, " (Generated)"])
        
        if(output == 'error'):
            print("".join(["A variable name was not recognized.\nPlease assign a new name for variable = ", str(variable)]))
            output = str(variable)

        return output
    

    ###################=========================###################
    ##===============##     Variable Titles     ##===============##
    ###################=========================###################
    
    
##########################################################################################################################################################################################
##########################################################################################################################################################################################
    
    
    ###################=======================================###################
    ##===============##        Full Filter + Cut Title        ##===============##
    ###################=======================================###################
    
    def DF_Filter_Function_Full(DF, Variables, Titles_or_DF, Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type="rdf", Cut_Choice="no_cut", Smearing_Q="", Binning_Q="", Sec_type="", Sec_num=-1):

        # if("2" not in Binning_Q and "P2" in Cut_Choice):
        #     return "continue"
        # if('str' in str(type(Variables)) and Q2_xB_Bin_Filter != -1 and Variables != "2D_Purity"):
        #     return "continue"

        ##===============================================##
        ##----------## Skipping Bad Requests ##----------##
        ##===============================================##
        # No smearing frames which are not the Monte Carlo Reconstructed
        if((Data_Type not in ["mdf", "pdf", "udf"] and ("miss_idf" not in Data_Type)) and "smear" in Smearing_Q):
            return "continue"
        # No Cuts for Monte Carlo Generated events
        if((Data_Type in ["gdf", "gen"]) and "no_cut" not in Cut_Choice):
            return "continue"
        # No PID cuts except for matched MC events
        if((Data_Type not in ["pdf", "gen"]) and "PID" in Cut_Choice):
            return "continue"
        ##===============================================##
        ##----------## Skipping Bad Requests ##----------##
        ##===============================================##


        ##=======================================================##
        ##----------## Smeared Binning (MC REC Only) ##----------##
        ##=======================================================##
        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_xB_Bin", "z_pT_Bin"
        if("2" in Binning_Q):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_2"]), "".join([z_pT_Bin_Filter_str, "_2"])
        # No smearing frames which are not the Monte Carlo Reconstructed
        if((Data_Type in ["mdf", "pdf", "udf"] or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_smeared"]), "".join([z_pT_Bin_Filter_str, "_smeared"])
        if(Data_Type == "gen"):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_gen"]), "".join([z_pT_Bin_Filter_str, "_gen"])
        ##=======================================================##
        ##----------## Smeared Binning (MC REC->End) ##----------##
        ##=======================================================##


        ##==========================================================##
        ##----------## Kinematic Binning (Filter - str) ##----------##
        ##==========================================================##
        Filter_Name, Q2_xB_BinList_Name, z_pT_BinList_Name = "", "", ""

        if(Q2_xB_Bin_Filter == -2):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "Only Binned Events", "".join([str(Q2_xB_Bin_Filter_str), " != 0"]), -1

        if(Q2_xB_Bin_Filter == -1):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "All Events", "", -2

        if(Q2_xB_Bin_Filter == 0):
            Q2_xB_BinList_Name, Filter_1, z_pT_Bin_Filter = "None - Events without a bin", "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Filter)]), -2

        if(Q2_xB_Bin_Filter > 0):
            Q2_xB_BinList_Name, Filter_1 = "".join([variable_Title_name(Q2_xB_Bin_Filter_str), ": ", str(Q2_xB_Bin_Filter)]), "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Filter)])

        if(z_pT_Bin_Filter == -2): # This skips z-pT bins
            z_pT_BinList_Name, Filter_2 = "", ""

        if(z_pT_Bin_Filter == -1):
            z_pT_BinList_Name, Filter_2 = "Only Binned Events", "".join([str(z_pT_Bin_Filter_str), " != 0"])

        if(z_pT_Bin_Filter == 0):
            z_pT_BinList_Name, Filter_2 = "None - Events without a bin", "".join([str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter)])

        if(z_pT_Bin_Filter > 0):
            z_pT_BinList_Name, Filter_2 = "".join([variable_Title_name(z_pT_Bin_Filter_str), ": ", str(z_pT_Bin_Filter)]), "".join([str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter)])


        if(Filter_2 != ""):
            Filter_Name = "".join([Filter_1, " && ", Filter_2])
        else:
            Filter_Name = Filter_1
        ##==========================================================##
        ##----------## Kinematic Binning (Filter - End) ##----------##
        ##==========================================================##


        ##===============================================##
        ##----------## Sector Filter (Start) ##----------##
        ##===============================================##
        if(Titles_or_DF == 'DF'):
            if(Filter_Name != ""):
                if(Sec_type != '' and Sec_num != -1):
                    Filter_Name = "".join([Filter_Name, " && ", str(Sec_type), " == ", str(Sec_num)])
            elif(Sec_type != '' and Sec_num != -1):
                Filter_Name = "".join([str(Sec_type), " == ", str(Sec_num)])


            if(Filter_Name != ""):
                print(Filter_Name)
                DF_Out = DF.Filter(Filter_Name)
            else:
                DF_Out = DF

        else:
            particle_sector = ""
            if(Sec_type != '' and Sec_num != -1):
                if('esec' in Sec_type):
                    particle_sector = 'El'
                if('pipsec' in Sec_type):
                    particle_sector = 'Pi+'
                if('_a' in Sec_type):
                    particle_sector = ''.join([particle_sector, ' (Angle Def)'])

                Sector_Title_Name = ''.join([particle_sector, ' Sector ', str(Sec_num)])
            else:
                Sector_Title_Name = ''
        ##===============================================##
        ##----------##  Sector Filter (End)  ##----------##
        ##===============================================##



        ##################################################
        ##==========## General Cuts (Start) ##==========##
        ##################################################
        cutname = " "
        if((Data_Type in ["pdf", "gen"]) and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el != 0 && PID_pip != 0")

        if(Data_Type == "udf" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el == 0 || PID_pip == 0")

        if(Data_Type == "miss_idf" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && (PID_el != 11 || PID_pip != 211)")

        if(Data_Type == "miss_idf_el" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_el != 11")

        if(Data_Type == "miss_idf_pip" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_pip != 211")



        if(Data_Type not in ["gdf", "gen"] and "no_cut" != Cut_Choice):

            if("Complete" in Cut_Choice):

                cutname = "Complete Set of "

                if("smear" in Smearing_Q and Data_Type != "rdf"):
                    cutname = "".join([cutname, "(Smeared) "])

                if(Titles_or_DF == 'DF'):
                    if("smear" in Smearing_Q and Data_Type != "rdf"):
                        #        DF_Out.Filter("              y < 0.75 &&               xF > 0 &&               W > 2 &&              Q2 > 2 &&              pip > 1.25 &&              pip < 5 && 5 < elth             &&             elth < 35 && 5 < pipth            &&            pipth < 35")
                        DF_Out = DF_Out.Filter("smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 2 && smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
                        DF_Out = filter_Valerii(DF_Out, Cut_Choice)
                    else:
                        DF_Out = DF_Out.Filter("y < 0.75 && xF > 0 && W > 2 && Q2 > 2 && pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
                        DF_Out = filter_Valerii(DF_Out, Cut_Choice)


                if("EDIS" in Cut_Choice):
                    cutname = "".join([cutname, "Exclusive "])
                    if(Titles_or_DF == 'DF'):
                        DF_Out = DF_Out.Filter(str(Calculated_Exclusive_Cuts(Smearing_Q)))

                if("SIDIS" in Cut_Choice):
                    cutname = "".join([cutname, "SIDIS "])
                    if(Titles_or_DF == 'DF'):
                        if("smear" in Smearing_Q and Data_Type != "rdf"):
                            #       DF_Out.Filter("sqrt(MM2) > 1.5")
                            DF_Out = DF_Out.Filter("sqrt(smeared_vals[1]) > 1.5")
                        else:
                            DF_Out = DF_Out.Filter("sqrt(MM2) > 1.5")

                cutname = "".join([cutname, "Cuts"])

        else:
            # Generated Monte Carlo should not have cuts applied to it
            cutname = "No Cuts"
        ##################################################
        ##==========##  General Cuts (End)  ##==========##
        ##################################################




        ##====================================================##
        ##----------## Smearing Variables (Start) ##----------##
        ##====================================================##
        if((Variables not in ["Cuts Only", "Cuts_Only", "Cuts"]) and ("Combined_" not in Variables)):
            # If the above condition is FALSE, then the 'Variables' input does not specify a real variable that can be smeared or is already defined by another function (use to run this function for cuts only)
            # This information does not need to be run if titles are the only things of interest
            if((Data_Type in ["mdf", "pdf", "udf"] or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q and Titles_or_DF == 'DF'):
                if('str' in str(type(Variables))):
                    DF_Out = smear_frame_compatible(DF_Out, Variables, Smearing_Q)
                else:
                    for variable in Variables:
                        DF_Out = smear_frame_compatible(DF_Out, variable, Smearing_Q)
        ##====================================================##
        ##----------##  Smearing Variables (End)  ##----------##
        ##====================================================##



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
    
    
    ###################=======================================###################
    ##===============##   (Other) Histogram Functions Title   ##===============##
    ###################=======================================###################
        
    def Data_Type_Title(Data_Type, Smearing_Q=""):
        Data_Title = "Undefined Data (ERROR)"
        if(Data_Type == 'rdf'):
            Data_Title = "Experimental Data"
        if(Data_Type in ['mdf', 'pdf', 'udf'] or ("miss_idf" in Data_Type)):
            # Data_Title = "".join(["Monte Carlo Data (REC", " - Smeared)" if "smear" in Smearing_Q else ")"])
            Data_Title = "".join(["Monte Carlo Data (REC)"])
        if(Data_Type == 'pdf'):
            Data_Title = Data_Title.replace("REC", "Matched")
        if(Data_Type == 'miss_idf'):
            Data_Title = Data_Title.replace("REC", "Mis-Identified Match")
        if(Data_Type == 'miss_idf_el'):
            Data_Title = Data_Title.replace("REC", "Mis-Identified (Electron) Match")
        if(Data_Type == 'miss_idf_pip'):
            Data_Title = Data_Title.replace("REC", "Mis-Identified (Pi+ Pion) Match")
        if(Data_Type == 'udf'):
            Data_Title = Data_Title.replace("REC", "Unmatched")
        if(Data_Type == 'gdf'):
            Data_Title = "Monte Carlo Data (GEN)"
        if(Data_Type == 'gen'):
            Data_Title = "Monte Carlo Data (GEN - Matched)"

        return Data_Title

    
##########################################################################################################################################################################################

    def Cut_Choice_Title(Cut_Type="no_cut"):
        Cut_Name = "Undefined Cut (ERROR)"
        if(Cut_Type == "no_cut"):
            Cut_Name = "No Cuts"
        if("EDIS" in Cut_Type):
            Cut_Name = "Exclusive Cuts"
        if("SIDIS" in Cut_Type):
            Cut_Name = "SIDIS Cuts"
        if("Complete" in Cut_Type):
            Cut_Name = "".join(["Complete Set of ", str(Cut_Name)])

        return Cut_Name

##########################################################################################################################################################################################

    def Dimension_Name_Function(Histo_Var_D1, Histo_Var_D2="None", Histo_Var_D3="None"):
        Dimensions_Output = "Variable_Error"
        try:
            Histo_Var_D1_Name  = "".join(["Var-D1:'", str(Histo_Var_D1[0]), "'-[NumBins:", str(Histo_Var_D1[3]), ", MinBin:", str(Histo_Var_D1[1]), ", MaxBin:", str(Histo_Var_D1[2]), "]"])
            Dimensions_Output = Histo_Var_D1_Name
            if(Histo_Var_D2 != "None"):
                Histo_Var_D2_Name  = "".join(["Var-D2:'", str(Histo_Var_D2[0]), "'-[NumBins:", str(Histo_Var_D2[3]), ", MinBin:", str(Histo_Var_D2[1]), ", MaxBin:", str(Histo_Var_D2[2]), "]"])
                if(Histo_Var_D3 != "None"):
                    Histo_Var_D3_Name  = "".join(["Var-D3:'", str(Histo_Var_D3[0]), "'-[NumBins:", str(Histo_Var_D3[3]), ", MinBin:", str(Histo_Var_D3[1]), ", MaxBin:", str(Histo_Var_D3[2]), "]"])
                    Dimensions_Output = "".join([str(Histo_Var_D1_Name), "; ", str(Histo_Var_D2_Name), "; ", str(Histo_Var_D3_Name)])
                else:
                    Dimensions_Output = "".join([str(Histo_Var_D1_Name), "; ", str(Histo_Var_D2_Name)])

            Dimensions_Output = Dimensions_Output.replace(":", "=")
            Dimensions_Output = Dimensions_Output.replace("; ", "), (")
            
            # if(Histo_Var_D2 == "None" and Histo_Var_D3 == "None"):
            #     Dimensions_Output = Dimensions_Output.replace("_smeared", "")
            # try:
            #     if(Histo_Var_D2 != "None" and Histo_Var_D3 == "None" and ("smear" in str(Histo_Var_D1[0]) and "smear" in str(Histo_Var_D2[0]))):
            #         Dimensions_Output = Dimensions_Output.replace("_smeared", "")
            # except:
            #     print("".join([color.BOLD, color.RED, "ERROR IN REMOVING '_smeared' FROM VARIABLE NAME:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))
            
        except:
            print("".join([color.BOLD, color.RED, "ERROR IN DIMENSIONS:\n", color.END, color.RED, str(traceback.format_exc()), color.END]))

        return Dimensions_Output

    
    ###################=======================================###################
    ##===============##    Histogram Functions Title (End)    ##===============##
    ###################=======================================###################
    
    
    
    
    
    
    
    
    ##################################################################################################################################################################
    ###################################################          Done Making the Functions for Histograms          ###################################################
    ###                                              ##------------------------------------------------------------##                                              ###
    ###----------------------------------------------##------------------------------------------------------------##----------------------------------------------###
    ###                                              ##------------------------------------------------------------##                                              ###
    ##################################################################################################################################################################
    ###################################################                    Choices For Graphing                    ###################################################
    ##################################################################################################################################################################
    

    
    
    ###############################################################
    #####################     Bin Choices     #####################
    
    # For Q2_xB Bins:
            # A value of -2 --> Only Binned Events
            # A value of -1 --> All Events
            # A value of 0 --> Only Non-Binned Events (Events that do not correspond to a bin)
            
    # For z_pT Bins (relavent to later parts of the analysis):
            # A value of -2 --> Skip z-pT bins (This means that only the option for Q2-xB bins will matter for this value of z-pT)
            # A value of -1 --> Only Binned Events
            # A value of 0 --> Only Non-Binned Events (Events that do not correspond to a bin)

    # Q2_xB Bins have a maximum value of 10 (9 total bins)
    
    
    # The following list should include all the desired kinematic bins to be included.
    # # Only necessary for 3D->2D histograms (All binning is already built into the 3D->1D histograms)
    # # # z-pT bins are built into all 3D histograms that this code creates
    # If a Q2-xB bin is missing from this list, then that bin will be skipped when making the histograms


    # # The following are the maximum number of Q2-xB this code recognizes 
#     List_of_Q2_xB_Bins_to_include = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # List_of_Q2_xB_Bins_to_include = [-1, -2]
#     List_of_Q2_xB_Bins_to_include = [-1]


    List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8]
    # List_of_Q2_xB_Bins_to_include = [-1, 1]
    
    
    
    #####################     Bin Choices     #####################
    ###############################################################
    
    
    
    ##################################################################
    #####################     Sector Choices     #####################
    
    
    # Types_Of_Sectors = ['', 'esec', 'pipsec', 'esec_a', 'pipsec_a']
    # Types_Of_Sectors = ['', 'esec_a', 'pipsec_a']
    # Types_Of_Sectors = ['', 'esec', 'pipsec']
    Types_Of_Sectors = ['']

    # Types_Of_Sectors = '' --> No Sector Filter

    # Sector_Numbers = [-1, 1, 2, 3, 4, 5, 6]
    Sector_Numbers = [-1]

    # Sector_Numbers = -1 or Types_Of_Sectors = '' --> All Sectors
    # Sector_Numbers = 0 --> No Sectors (should have no events but if it does, those events exist as errors in the sector definitions)
    
    
    #####################     Sector Choices     #####################
    ##################################################################
    
    
    
    ###################################################################
    #####################       Cut Choices       #####################
    
    
    # # Cut Naming Conventions:
        # 1) 'no_cut' --> no new cuts are applied (only cuts are made during particle identification (PID))
        #
        # 2) 'Mom' --> (See below)
          # 1.25 < pip < 5
          # 5 < elth < 35
          # 5 < pipth < 35"
        #
        # 3) 'SIDIS' --> (See below)
          # y < 0.75
          # xF > 0
          # W > 2
          # Q2 > 1
        #
        # 4) 'all' --> Combination of 'Mom', 'SIDIS', with an additional Missing Mass cut of: "MM > 1.5"
          # Do not combine with "Mom" or "SIDIS" separately as doing so will be meaningless (combination is already built in) 
        #
        # 5) 'Valerii_Cut' --> Valerii's Fiducial cuts to remove bad detectors
        #
        # 6) 'Q2'  -> New Q2 cut of "Q2 > 2"
        
    # # Other than 'no_cut', all of the above cuts can be combined separately by adding them to the str in cut_list as a suffix of another cut
    # # # Example:
        # # cut_list = ["no_cut", "cut_all", "cut_Mom_SIDIS"]
          # # The first two cuts in the above list are the same as describles in entry (1) and (4) in the list above. The 3rd entry is a combination of "Mom" and "SIDIS" where both cuts are applied together (order doesn't matter). This combination can be done with any of the cuts given in the list above (except 'no_cut') and can be done with as many of them as desired (no limits to number of cuts that can be added to one entry).
    
    
    

    # cut_list = ['no_cut', 'cut_Complete', 'cut_Complete_EDIS', 'cut_Complete_SIDIS']
    cut_list = ['no_cut', 'cut_Complete_EDIS', 'cut_Complete_SIDIS']
    cut_list = ['no_cut', 'cut_Complete_SIDIS']
    # cut_list = ['cut_Complete_SIDIS']

    
    
    #####################       Cut Choices       #####################
    ###################################################################
    
    
    
    #####################################################################################################################
    ###############################################     3D Histograms     ###############################################
    

#     # Bin Set Option: 20 bins
# #     Q2_Binning = ['Q2', 0, 12.5, 25]
# #     Q2_Binning_Smeared = ['Q2_smeared', 0, 12.5, 25]
#     # Bin Set Option: 20 bins (Actual total bins = 27)
#     Q2_Binning = ['Q2', -0.3378, 12.2861, 27]
#     # Q2_Binning_Smeared = ['Q2_smeared', -0.3378, 12.2861, 27]
#     # Bin size: 0.46755 per bin
# #     xB_Binning = ['xB', -0.08, 0.92, 25]
# #     xB_Binning_Smeared = ['xB_smeared', -0.08, 0.92, 25]
#     # Bin Set Option: 20 bins (Actual total bins = 25)
#     xB_Binning = ['xB', -0.006, 0.8228, 25]
#     # xB_Binning_Smeared = ['xB_smeared', -0.006, 0.8228, 25]
#     # Bin size: 0.03315 per bin
#     z_Binning = ['z', 0.006, 1.014, 28]
#     # z_Binning_Smeared = ['z_smeared', 0.006, 1.014, 28]
#     pT_Binning = ['pT', -0.15, 1.8, 26]
#     # pT_Binning_Smeared = ['pT_smeared', -0.15, 1.8, 26]
#     y_Binning = ['y', -0.0075, 0.9975, 36]
#     # y_Binning_Smeared = ['y_smeared', -0.0075, 0.9975, 36]
#     # Bin size: 0.0275
#     phi_t_Binning = ['phi_t', 0, 360, 36]
#     # phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 36]
# #     # Reduced Phi Binning (as of 11-28-2022) -- 15˚ per bin
# #     phi_t_Binning = ['phi_t', 0, 360, 24]
# #     # phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 24]

# #     # Bin Set Option: GRC Poster binning
# #     Q2_Binning = ['Q2', 2, 11.351, 5]
# #     Q2_Binning_Smeared = ['Q2_smeared', 2, 11.351, 5]
# #     # Bin size: 1.8702 per bin
# #     xB_Binning = ['xB', 0.126602, 0.7896, 5]
# #     xB_Binning_Smeared = ['xB_smeared', 0.126602, 0.7896, 5]
# #     # Bin size: 0.1325996 per bin
# #     z_Binning = ['z', 0.15, 0.7, 5]
# #     z_Binning_Smeared = ['z_smeared', 0.15, 0.7, 5]
# #     # Bin size: 0.11 per bin
# #     pT_Binning = ['pT', 0.05, 1, 5]
# #     pT_Binning_Smeared = ['pT_smeared', 0.05, 1, 5]
# #     # Bin size: 0.19 per bin
# #     y_Binning = ['y', 0, 1, 5]
# #     y_Binning_Smeared = ['y_smeared', 0, 1, 5]
# #     # Bin size: 0.2 per bin
# #     phi_t_Binning = ['phi_t', 0, 360, 36]
# #     phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 36]
# #     # Bin size: 10 per bin
    
    # Post-GRC Binning
    Q2_Binning_Old = ['Q2', 1.4805, 11.8705, 20]
    # Q2_Binning_Smeared = ['Q2_smeared', 1.4805, 11.8705, 20]
    # Bin size: 0.5195 per bin
    xB_Binning_Old = ['xB', 0.08977, 0.82643, 20]
    # xB_Binning_Smeared = ['xB_smeared', 0.08977, 0.82643, 20]
    # Bin size: 0.03683 per bin
    z_Binning_Old = ['z', 0.11944, 0.73056, 20]
    # z_Binning_Smeared = ['z_smeared', 0.11944, 0.73056, 20]
    # Bin size: 0.03056 per bin
    pT_Binning_Old = ['pT', 0, 1.05, 20]
    # pT_Binning_Smeared = ['pT_smeared', 0, 1.05, 20]
    # Bin size: 0.05 per bin
    y_Binning_Old = ['y', 0, 1, 20]
    # y_Binning_Smeared = ['y_smeared', 0, 1, 20]
    # Bin size: 0.05 per bin

    
#     # Post-DNP Binning
#     Q2_Binning    = ['Q2',     1.48,  11.87,  20]
#     # Bin size: 0.5195 per bin
#     xB_Binning    = ['xB',     0.09,  0.826,  20]
#     # Bin size: 0.0368 per bin
#     z_Binning     = ['z',      0.119, 0.731,  20]
#     # Bin size: 0.0306 per bin
#     pT_Binning    = ['pT',     0,     1.05,   20]
#     # Bin size: 0.05 per bin
    y_Binning     = ['y',      0,     1,      20]
    # Bin size: 0.05 per bin
    
#     phi_t_Binning = ['phi_t',  0,     360,    36]
#     # Bin size: 10 per bin
    
    phi_t_Binning = ['phi_t',  0,     360,    24]
    # Bin size: 15 per bin
    
    MM_Binning    = ['MM',     0,     3.5,   500]
    # Bin size: 0.007 per bin
    W_Binning     = ['W',      0,     6,     200]
    # Bin size: 0.03 per bin
    Binning_4D    = ['Bin_4D', -1.5,  303.5, 305]
    # Binning_4D_OG = ['Bin_4D_OG', -1.5, 353.5, 355]
    # Binning_5D  = ['Bin_5D', -1.5, 11625.5, 11627]
    # Binning_5D_OG = ['Bin_5D_OG', -1.5, 13525.5, 13527]
    
    
    El_Binning      = ['el',    0, 8,   200]
    El_Th_Binning   = ['elth',  0, 40,  200]
    El_Phi_Binning  = ['elPhi', 0, 360, 200]
    
    Pip_Binning     = ['pip',    0, 6,   200]
    Pip_Th_Binning  = ['pipth',  0, 40,  200]
    Pip_Phi_Binning = ['pipPhi', 0, 360, 200]
    
    
     
    # New 2023 2D Binning
    Q2_Binning = ['Q2', 1.48,  11.87, 100]
    # Bin size: 0.1039  per bin
    xB_Binning = ['xB', 0.09,  0.826, 100]
    # Bin size: 0.00736 per bin
    z_Binning  = ['z',  0.017, 0.935, 100]
    # Bin size: 0.00918 per bin
    pT_Binning = ['pT', 0,     1.26,  120]
    # Bin size: 0.0105 per bin
    
    # Q2_Binning_Old = ['Q2', 0.0, 12.5, 25]
    # # Bin size: 0.5 per bin
    # xB_Binning_Old = ['xB', -0.003,  0.997, 25]
    # # Bin size: 0.04 per bin
    
    
    # List_of_Quantities_1D = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, MM_Binning, ['el', 0, 10, 200], ['pip', 0, 8, 200], phi_t_Binning, Binning_4D, W_Binning]
    List_of_Quantities_1D = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, phi_t_Binning]
    # List_of_Quantities_1D_smeared = [Q2_Binning_Smeared, xB_Binning_Smeared, z_Binning_Smeared, pT_Binning_Smeared, y_Binning_Smeared, MM_Binning_Smeared, ['el_smeared', 0, 10, 200], ['pip_smeared', 0, 8, 200], phi_t_Binning_Smeared, Binning_4D_Smeared, W_Binning_Smeared]
    
    List_of_Quantities_1D = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, phi_t_Binning]
    List_of_Quantities_1D = [Q2_Binning_Old, xB_Binning_Old, z_Binning_Old, pT_Binning_Old, phi_t_Binning]
#     List_of_Quantities_1D = [phi_t_Binning]
#     List_of_Quantities_1D = [Q2_Binning_Old, xB_Binning_Old]
#     List_of_Quantities_1D = [phi_t_Binning, Q2_Binning_Old, xB_Binning_Old]
    
    # List_of_Quantities_2D = [[['Q2', 0, 12, 200], ['xB', 0, 0.8, 200]], [['y', 0, 1, 200], ['xB', 0, 0.8, 200]], [['z', 0, 1, 200], ['pT', 0, 1.6, 200]], [['el', 0, 8, 200], ['elth', 0, 40, 200]], [['elth', 0, 40, 200], ['elPhi', 0, 360, 200]], [['pip', 0, 6, 200], ['pipth', 0, 40, 200]], [['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]]]
    # List_of_Quantities_2D = [[Q2_Binning,         xB_Binning],          [y_Binning,        xB_Binning],          [z_Binning,        pT_Binning],          [['el', 0, 8, 200], ['elth', 0, 40, 200]], [['elth', 0, 40, 200], ['elPhi', 0, 360, 200]], [['pip', 0, 6, 200], ['pipth', 0, 40, 200]], [['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]]]
    List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [y_Binning, xB_Binning], [z_Binning, pT_Binning], [El_Binning, El_Th_Binning], [El_Th_Binning, El_Phi_Binning], [Pip_Binning, Pip_Th_Binning], [Pip_Th_Binning, Pip_Phi_Binning]]
    
    
    # Reduced Variable Options
    # List_of_Quantities_1D = [Q2_Binning,  xB_Binning,  z_Binning,  pT_Binning, phi_t_Binning]
#     List_of_Quantities_1D = [Q2_Binning, El_Binning, El_Th_Binning, El_Phi_Binning, Pip_Binning, Pip_Th_Binning, Pip_Phi_Binning, phi_t_Binning]
    # List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [z_Binning, pT_Binning]]
    List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [z_Binning, pT_Binning], [El_Binning, El_Th_Binning], [El_Binning, El_Phi_Binning], [El_Th_Binning, El_Phi_Binning], [Pip_Binning, Pip_Th_Binning], [Pip_Binning, Pip_Phi_Binning], [Pip_Th_Binning, Pip_Phi_Binning]]
    
    # List_of_Quantities_2D         = [[['Q2',         0, 12, 200], ['xB',         0, 0.8, 200]], [['y',         0, 1, 200], ['xB',         0, 0.8, 200]], [['z',         0, 1, 200], ['pT',         0, 1.6, 200]], [['el',         0, 8, 200], ['elth',         0, 40, 200]], [['elth',         0, 40, 200], ['elPhi',         0, 360, 200]], [['pip',         0, 6, 200], ['pipth',         0, 40, 200]], [['pipth',         0, 40, 200], ['pipPhi',         0, 360, 200]]]
    # List_of_Quantities_2D_smeared = [[['Q2_smeared', 0, 12, 200], ['xB_smeared', 0, 0.8, 200]], [['y_smeared', 0, 1, 200], ['xB_smeared', 0, 0.8, 200]], [['z_smeared', 0, 1, 200], ['pT_smeared', 0, 1.6, 200]], [['el_smeared', 0, 8, 200], ['elth_smeared', 0, 40, 200]], [['elth_smeared', 0, 40, 200], ['elPhi_smeared', 0, 360, 200]], [['pip_smeared', 0, 6, 200], ['pipth_smeared', 0, 40, 200]], [['pipth_smeared', 0, 40, 200], ['pipPhi_smeared', 0, 360, 200]]]
    
    
    # List_of_Quantities_2D         = [[['Q2',         0, 12, 200], ['xB',         0, 0.8, 200]], [['z',         0, 1, 200], ['pT',         0, 1.6, 200]], [['y',         0, 1, 200], ['xF',         -1, 1, 200]], [['el',         0, 8, 200], ['elth',         0, 40, 200]], [['pip',         0, 6, 200], ['pipth',         0, 40, 200]]]
    # List_of_Quantities_2D_smeared = [[['Q2_smeared', 0, 12, 200], ['xB_smeared', 0, 0.8, 200]], [['z_smeared', 0, 1, 200], ['pT_smeared', 0, 1.6, 200]], [['y_smeared', 0, 1, 200], ['xF_smeared', -1, 1, 200]], [['el_smeared', 0, 8, 200], ['elth_smeared', 0, 40, 200]], [['pip_smeared', 0, 6, 200], ['pipth_smeared', 0, 40, 200]]]
    
    # # # 2D histograms are turned off with these options
#     List_of_Quantities_2D = []
    # List_of_Quantities_2D_smeared = []
    
    
    
    
    if(len(List_of_Quantities_2D) == 0):
        print("".join([color.BLUE, color.BOLD, "Not running 2D histograms...", color.END]))
    
    
    
    run_Mom_Cor_Code = "yes"
    run_Mom_Cor_Code = "no"

    if(run_Mom_Cor_Code == "yes"):
        print("".join([color.BLUE, color.BOLD, "\nRunning Histograms from Momentum Correction Code (i.e., Missing Mass and ∆P Histograms)", color.END]))
    else:
        print("".join([color.BLUE, "\nNOT Running Momentum Correction Histograms", color.END]))
    
    
    smearing_options_list = ["", "smear"]
    # smearing_options_list = [""]
    
    # binning_option_list = ["", "2"]
    binning_option_list = ["2"]
    # The option '2' uses the modified binning schemes developed for this analysis (instead of the binning used by Stephan)
    
    if(datatype in ["rdf", "gdf"]):
        # Do not smear data or generated MC
        for ii in smearing_options_list:
            if("smear" in ii):
                smearing_options_list.remove(ii)
    
    
    if(("ivec" in smearing_function) and ("smear" in smearing_options_list)):
        print("".join([color.BLUE, color.BOLD, "\nRunning Modified Smearing Funtion", color.END]))
    elif("smear" in smearing_options_list):
        print("".join([color.BLUE, color.BOLD, "\nRunning FX's Smearing Funtion", color.END]))
    else:
        print("".join([color.BLUE, "\nNot Smearing...", color.END]))
    
    
    def Print_Progress(Total, Increase, Rate):
        if((Rate == 1) or (((Total+Increase)%Rate) == 0) or (Rate < Increase) or ((Rate-((Total)%Rate)) < Increase)):
            print("".join([str(Total+Increase), " Histograms Have Been Made..."]))
    
    
    
    
    
    ##############################################################     End of Choices For Graphing     ##############################################################
    ##                                                                                                                                                             ##
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##                                                                                                                                                             ##
    ###########################################################     Graphing Results + Final ROOT File     ##########################################################
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    ###########################################################
    #################     Final ROOT File     #################
    
    
    # File to be saved
    if(str(file_location) != 'time' and output_type == "histo"):
        ROOT_File_Output = ROOT.TFile(str(ROOT_File_Output_Name), 'recreate')
        print("\nFinal ROOT file has been created...")
    
    
    #################     Final ROOT File     #################
    ###########################################################
    
    
    
    
    
    
    
    if(output_type in ["histo", "time"]):
        Histograms_All = {}
        count_of_histograms = 0
        print("".join([color.BOLD, color.BLUE, "\n\nMaking Histograms...\n", color.END]))

######################################################################
##=====##=====##=====##    Top of Main Loop    ##=====##=====##=====##
######################################################################

##======##     Data-Type Loop      ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
        datatype_list = ["mdf", "pdf", "gen"] if(datatype == "pdf") else ["mdf", "gen"] if(datatype == "mdf") else [datatype]

        for Histo_Data in datatype_list:

##======##======##     Cut Loop    ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
            for Histo_Cut in cut_list:

                if(Histo_Data == "gdf" and Histo_Cut != "no_cut"):
                    # Do not cut data from the MC GEN files
                    continue

##======##======##======##     Smearing Loop       ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
                for Histo_Smear in smearing_options_list:

                    if(Histo_Data not in ["mdf", "pdf"] and "smear" in Histo_Smear):
                        # Do not smear data that is not from the MC REC files
                        continue

##======##======##======##======##     Binning Loop        ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
                    for Binning in binning_option_list:

                        Histo_Binning = [Binning, "All", "All"]
                        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_xB_Bin", "z_pT_Bin"

                        if("2" in Binning):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_2"]), "".join([z_pT_Bin_Filter_str, "_2"])
                        else:
                            print("\n\nERROR\n\n")

                        Variable_Loop    = copy.deepcopy(List_of_Quantities_1D)
                        Variable_Loop_2D = copy.deepcopy(List_of_Quantities_2D)

                        if("smear" in Histo_Smear):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_smeared"]), "".join([z_pT_Bin_Filter_str, "_smeared"])
                            Variable_Loop = copy.deepcopy(List_of_Quantities_1D)
                            for list1 in Variable_Loop:
                                if(len(list1) == 4):
                                    list1[0] = "".join([str(list1[0]), "_smeared" if("_smeared" not in str(list1[0])) else ""])
                                else:
                                    # Smearing Combined 1D Variables
                                    for combined_vars in list1:
                                        combined_vars[0] = "".join([str(combined_vars[0]), "_smeared" if("_smeared" not in str(combined_vars[0])) else ""])

                            Variable_Loop_2D = copy.deepcopy(List_of_Quantities_2D)
                            for list2 in Variable_Loop_2D:
                                list2[0][0] = "".join([str(list2[0][0]), "_smeared" if("_smeared" not in str(list2[0][0])) else ""])
                                list2[1][0] = "".join([str(list2[1][0]), "_smeared" if("_smeared" not in str(list2[1][0])) else ""])

                        if("gen" in Histo_Data):
                            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_gen"]), "".join([z_pT_Bin_Filter_str, "_gen"])
                            Variable_Loop = copy.deepcopy(List_of_Quantities_1D)
                            for list1 in Variable_Loop:
                                if(len(list1) == 4):
                                    list1[0] = "".join([str(list1[0]), "_gen" if("_gen" not in str(list1[0])) else ""])
                                else:
                                    # Matched Gen Combined 1D Variables
                                    for combined_vars in list1:
                                        combined_vars[0] = "".join([str(combined_vars[0]), "_gen" if("_gen" not in str(combined_vars[0])) else ""])
                            Variable_Loop_2D = copy.deepcopy(List_of_Quantities_2D)
                            for list2 in Variable_Loop_2D:
                                list2[0][0] = "".join([str(list2[0][0]), "_gen" if("_gen" not in str(list2[0][0])) else ""])
                                list2[1][0] = "".join([str(list2[1][0]), "_gen" if("_gen" not in str(list2[1][0])) else ""])


##======##======##======##======##======##     Histogram Option Selection  ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##

                        # histo_options = ["Normal", "Response_Matrix", "Response_Matrix_Normal"]
                        histo_options = ["Normal", "Response_Matrix_Normal"]
                        # histo_options = ["Response_Matrix_Normal"]

                        # # Types of Histogram Groups (Histo_Group)
                          # # (*) "Normal"                 --> Makes normal 1D and 2D histograms
                          # # (*) "Response_Matrix"        --> Makes a 2D Response Matrix (or equivalent 1D histogram) using the Kinematic Bin Number plotted on each axis
                          # # (*) "Response_Matrix_Normal" --> Makes a 2D Response Matrix (or equivalent 1D histogram) using the Kinematic variable's regular value plotted on each axis (the plotted values will not necessarily be interger values as they would be in the other Response Matrix option)
                          # # (*) "Mom_Cor_Code"           --> Makes the plots used for Momentum Corrections/Smearing Functions

                        if(Histo_Data == 'pdf'):
                            histo_options = ["Has_Matched"]
                            histo_options.append("Bin_Purity")
                            histo_options.append("Delta_Matched")
                            # Meaning of the above options:
                                # # (*) 'Has_Matched'   --> Same as "Normal" but filters unmatched events
                                # # (*) 'Bin_Purity'    --> Filters events in which the reconstructed bin is different from the generated bin
                                # # (*) 'Delta_Matched' --> Makes histograms which plot the difference between the reconstructed and generated (∆val) versus the reconstructed value
                        elif(Histo_Data == "gen"):
                            histo_options = ["Normal"]
                            # Running 'Response_Matrix' options is unnecessary for the matched generated plots (only useful for 2D (or 1D) histograms)

                        if(run_Mom_Cor_Code == "yes" and Histo_Data not in ['pdf', 'gen']):
                            histo_options.append("Mom_Cor_Code")
                            # "Mom_Cor_Code" --> Makes the plots used for Momentum Corrections/Smearing Functions
                            
                            
##======##======##======##======##======##     Histogram Option Loop       ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
                        for Histo_Group in histo_options:
                            Histo_Group_Name   = "".join(["Histo-Group:'",  str(Histo_Group), "'"])
                            Histo_Data_Name    = "".join(["Data-Type:'",    str(Histo_Data),  "'"])
                            Histo_Cut_Name     = "".join(["Data-Cut:'",     str(Histo_Cut),   "'"])
                            Histo_Smear_Name   = "".join(["Smear-Type:'",   str(Histo_Smear), "'"])
                            Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-(Q2-xB-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), ")"])



##################################################=================================================##################################################################################################################################
##======##======##======##======##======##======##     Momentum Correction/Smearing Histograms     ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
##################################################=================================================##################################################################################################################################
                            if(Histo_Group == "Mom_Cor_Code"):

                                # Removed the "_smeared" from all variable names as of 11-29-2022
                                Histo_Var_MM_Dimension          = ['MM', 0, 3.5, 500]
                                Histo_Var_Dp_Ele_Dimension      = ['Delta_Pel_Cors', -3, 3, 500]
                                Histo_Var_Dp_Pip_Dimension      = ['Delta_Ppip_Cors', -3, 3, 500]
                                Histo_Var_DTheta_Ele_Dimension  = ['Delta_Theta_el_Cors', -3, 3, 500]
                                Histo_Var_DTheta_Pip_Dimension  = ['Delta_Theta_pip_Cors', -3, 3, 500]
                                Histo_Var_Ele_Dimension         = ['el', 0, 10, 200]
                                Histo_Var_Pip_Dimension         = ['pip', 0, 8, 200]
                                Histo_Var_Ele_Theta_Dimension   = ['elth', 0, 40, 200]
                                Histo_Var_Pip_Theta_Dimension   = ['pipth', 0, 40, 200]
                                Histo_Var_Ele_Phi_Dimension     = ['elPhi', 0, 360, 360]
                                Histo_Var_Pip_Phi_Dimension     = ['pipPhi', 0, 360, 360]

                            ###############################################################
                            ##==========##     Correction Histogram ID's     ##==========##
                            ###############################################################

                                Mom_Cor_Histo_Name_Main = ((("".join(["((", "), (".join([Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name])])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")

                                Mom_Cor_Histo_Name_MM_Ele            = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_MM_Dimension, Histo_Var_D2=Histo_Var_Ele_Dimension)), "))"])
                                Mom_Cor_Histo_Name_MM_Pip            = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_MM_Dimension, Histo_Var_D2=Histo_Var_Pip_Dimension)), "))"])

                                Mom_Cor_Histo_Name_DP_Ele            = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dp_Ele_Dimension, Histo_Var_D2=Histo_Var_Ele_Dimension)), "))"])
                                Mom_Cor_Histo_Name_DP_Pip            = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dp_Pip_Dimension, Histo_Var_D2=Histo_Var_Pip_Dimension)), "))"])

                                Mom_Cor_Histo_Name_DP_Ele_Theta      = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dp_Ele_Dimension, Histo_Var_D2=Histo_Var_Ele_Theta_Dimension)), "))"])
                                Mom_Cor_Histo_Name_DP_Pip_Theta      = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Dp_Pip_Dimension, Histo_Var_D2=Histo_Var_Pip_Theta_Dimension)), "))"])

                                Mom_Cor_Histo_Name_DTheta_Ele        = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DTheta_Ele_Dimension, Histo_Var_D2=Histo_Var_Ele_Dimension)), "))"])
                                Mom_Cor_Histo_Name_DTheta_Pip        = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DTheta_Pip_Dimension, Histo_Var_D2=Histo_Var_Pip_Dimension)), "))"])

                                Mom_Cor_Histo_Name_DTheta_Ele_Theta  = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DTheta_Ele_Dimension, Histo_Var_D2=Histo_Var_Ele_Theta_Dimension)), "))"])
                                Mom_Cor_Histo_Name_DTheta_Pip_Theta  = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_DTheta_Pip_Dimension, Histo_Var_D2=Histo_Var_Pip_Theta_Dimension)), "))"])

                                # Mom_Cor_Histo_Name_Angle_Ele         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Ele_Theta_Dimension, Histo_Var_D2=Histo_Var_Ele_Phi_Dimension)), "))"])
                                # Mom_Cor_Histo_Name_Angle_Pip         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Pip_Theta_Dimension, Histo_Var_D2=Histo_Var_Pip_Phi_Dimension)), "))"])
                                Mom_Cor_Histo_Name_Angle_Ele         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Ele_Theta_Dimension, Histo_Var_D2=Histo_Var_Ele_Phi_Dimension, Histo_Var_D3=Histo_Var_Ele_Dimension)), "))"])
                                Mom_Cor_Histo_Name_Angle_Pip         = ''.join([Mom_Cor_Histo_Name_Main, "), (", str(Dimension_Name_Function(Histo_Var_D1=Histo_Var_Pip_Theta_Dimension, Histo_Var_D2=Histo_Var_Pip_Phi_Dimension, Histo_Var_D3=Histo_Var_Pip_Dimension)), "))"])
                                
                                
                                Mom_Cor_Histo_Name_MM_Ele            = Mom_Cor_Histo_Name_MM_Ele.replace("; ", "), ")
                                Mom_Cor_Histo_Name_MM_Pip            = Mom_Cor_Histo_Name_MM_Pip.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DP_Ele            = Mom_Cor_Histo_Name_DP_Ele.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DP_Pip            = Mom_Cor_Histo_Name_DP_Pip.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DP_Ele_Theta      = Mom_Cor_Histo_Name_DP_Ele_Theta.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DP_Pip_Theta      = Mom_Cor_Histo_Name_DP_Pip_Theta.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DTheta_Ele        = Mom_Cor_Histo_Name_DTheta_Ele.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DTheta_Pip        = Mom_Cor_Histo_Name_DTheta_Pip.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DTheta_Ele_Theta  = Mom_Cor_Histo_Name_DTheta_Ele_Theta.replace("; ", "), ")
                                Mom_Cor_Histo_Name_DTheta_Pip_Theta  = Mom_Cor_Histo_Name_DTheta_Pip_Theta.replace("; ", "), ")
                                Mom_Cor_Histo_Name_Angle_Ele         = Mom_Cor_Histo_Name_Angle_Ele.replace("; ", "), ")
                                Mom_Cor_Histo_Name_Angle_Pip         = Mom_Cor_Histo_Name_Angle_Pip.replace("; ", "), ")


                            ###############################################################
                            ##==========##  Correction Histogram ID's (End)  ##==========##
                            ###############################################################


                            ###############################################################
                            ##==========##    Correction Histogram Titles    ##==========##
                            ###############################################################

                                
                                Mom_Cor_Histos_Name_MM_Ele_Title           = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "Missing Mass Histogram (Electron Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", "); p_{el};", "(Smeared) " if("smear" in Histo_Smear) else " ", "MM_{e#pi+(X)}; #theta_{el} Bins"])
                                Mom_Cor_Histos_Name_MM_Pip_Title           = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "Missing Mass Histogram (#pi^{+} Pion Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", "); p_{#pi+};", "(Smeared) " if("smear" in Histo_Smear) else " ", "MM_{e#pi+(X)}; #theta_{#pi+} Bins"])
                                
                                Mom_Cor_Histos_Name_Delta_Ele_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#DeltaP Histogram (Electron Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", "); p_{el};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{el}; #theta_{el} Bins"])
                                Mom_Cor_Histos_Name_Delta_Pip_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#DeltaP Histogram (#pi^{+} Pion Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", "); p_{#pi+};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{#pi+}; #theta_{#pi+} Bins"])
                                
                                Mom_Cor_Histos_Name_Delta_Ele_Theta_Title  = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#DeltaP Histogram vs #theta (Electron Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", "); #theta_{el};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{el}; El Sector"])
                                Mom_Cor_Histos_Name_Delta_Pip_Theta_Title  = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#DeltaP Histogram vs #theta (#pi^{+} Pion Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", "); #theta_{#pi+};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#DeltaP_{#pi+}; #pi^{+} Sector"])
                                
                                # Mom_Cor_Histos_Name_Angle_Ele_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#theta vs #phi vs p Histogram (Electron Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{el};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#phi_{el}; El Sector"])
                                # Mom_Cor_Histos_Name_Angle_Pip_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#theta vs #phi vs p Histogram (#pi^{+} Pion Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{#pi+};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#phi_{#pi+}; #pi^{+} Sector"])
                                Mom_Cor_Histos_Name_Angle_Ele_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#theta vs #phi vs p Histogram (Electron Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{el};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#phi_{el};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#p_{el}"])
                                Mom_Cor_Histos_Name_Angle_Pip_Title        = "".join(["(Smeared) " if("smear" in str(Histo_Smear)) else "", "#theta vs #phi vs p Histogram (#pi^{+} Pion Kinematics", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in Histo_Smear) else " ", "#theta_{#pi+};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#phi_{#pi+};", "(Smeared) " if("smear" in Histo_Smear) else " ", "#p_{#pi+}"])


                            ###############################################################
                            ##==========## Correction Histogram Titles (End) ##==========##
                            ###############################################################


                                variables_Mom_Cor     = ["MM", "Delta_Pel_Cors", "Delta_Ppip_Cors", "Delta_Theta_el_Cors", "Delta_Theta_pip_Cors", "el", "pip", "elth", "pipth", "elPhi", "pipPhi"]
                                if("smear" in Histo_Smear):
                                    variables_Mom_Cor = ["MM_smeared", "Delta_Pel_Cors_smeared", "Delta_Ppip_Cors_smeared", "Delta_Theta_el_Cors_smeared", "Delta_Theta_pip_Cors_smeared", "el_smeared", "pip_smeared", "elth_smeared", "pipth_smeared", "elPhi_smeared", "pipPhi_smeared", "el", "pip", "elth", "pipth"]

                                MCH_rdf = DF_Filter_Function_Full(DF=rdf, Variables=variables_Mom_Cor, Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1)
                                
                                if(MCH_rdf == "continue"):
                                    continue
                                    
                                
                            ###################################################################################
                            ##          ##          ##                               ##          ##          ##
                            ##==========##==========##     Correction Histograms     ##==========##==========##
                            ##          ##          ##                               ##          ##          ##
                            ###################################################################################

                                Histograms_All[Mom_Cor_Histo_Name_MM_Ele]            = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_MM_Ele, str(Mom_Cor_Histos_Name_MM_Ele_Title),    200, 0, 10, 500,  0, 3.5, 10, 0, 40), "el",  "MM" if("smear" not in Histo_Smear) else "MM_smeared", "elth")
                                Histograms_All[Mom_Cor_Histo_Name_MM_Pip]            = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_MM_Pip, str(Mom_Cor_Histos_Name_MM_Pip_Title),    200, 0, 8,  500,  0, 3.5, 10, 0, 40), "pip", "MM" if("smear" not in Histo_Smear) else "MM_smeared", "pipth")
                                Histograms_All[Mom_Cor_Histo_Name_DP_Ele]            = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Ele, str(Mom_Cor_Histos_Name_Delta_Ele_Title), 200, 0, 10, 500, -3, 3,   10, 0, 40), "el",  "Delta_Pel_Cors"  if("smear" not in Histo_Smear) else "Delta_Pel_Cors_smeared",  "elth")
                                Histograms_All[Mom_Cor_Histo_Name_DP_Pip]            = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Pip, str(Mom_Cor_Histos_Name_Delta_Pip_Title), 200, 0, 8,  500, -3, 3,   10, 0, 40), "pip", "Delta_Ppip_Cors" if("smear" not in Histo_Smear) else "Delta_Ppip_Cors_smeared", "pipth")
                                Histograms_All[Mom_Cor_Histo_Name_DTheta_Ele]        = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DTheta_Ele, str(Mom_Cor_Histos_Name_Delta_Ele_Title).replace("#DeltaP", "#Delta#theta"), 200, 0, 10, 500, -3, 3, 10, 0, 40), "el",  "Delta_Theta_el_Cors"  if("smear" not in Histo_Smear) else "Delta_Theta_el_Cors_smeared",  "elth")
                                Histograms_All[Mom_Cor_Histo_Name_DTheta_Pip]        = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DTheta_Pip, str(Mom_Cor_Histos_Name_Delta_Pip_Title).replace("#DeltaP", "#Delta#theta"), 200, 0, 8,  500, -3, 3, 10, 0, 40), "pip", "Delta_Theta_pip_Cors" if("smear" not in Histo_Smear) else "Delta_Theta_pip_Cors_smeared", "pipth")
                                
                                Histograms_All[Mom_Cor_Histo_Name_DP_Ele_Theta]      = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Ele_Theta, str(Mom_Cor_Histos_Name_Delta_Ele_Theta_Title), 200, 0, 40, 500, -3, 3, 8, -0.5, 7.5), "elth",  "Delta_Pel_Cors"  if("smear" not in Histo_Smear) else "Delta_Pel_Cors_smeared",  "esec")
                                Histograms_All[Mom_Cor_Histo_Name_DP_Pip_Theta]      = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DP_Pip_Theta, str(Mom_Cor_Histos_Name_Delta_Pip_Theta_Title), 200, 0, 40, 500, -3, 3, 8, -0.5, 7.5), "pipth", "Delta_Ppip_Cors" if("smear" not in Histo_Smear) else "Delta_Ppip_Cors_smeared", "pipsec")
                                Histograms_All[Mom_Cor_Histo_Name_DTheta_Ele_Theta]  = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DTheta_Ele_Theta, str(Mom_Cor_Histos_Name_Delta_Ele_Theta_Title).replace("#DeltaP", "#Delta#theta"), 200, 0, 40, 500, -3, 3, 8, -0.5, 7.5), "elth",  "Delta_Theta_el_Cors"  if("smear" not in Histo_Smear) else "Delta_Theta_el_Cors_smeared",  "esec")
                                Histograms_All[Mom_Cor_Histo_Name_DTheta_Pip_Theta]  = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_DTheta_Pip_Theta, str(Mom_Cor_Histos_Name_Delta_Pip_Theta_Title).replace("#DeltaP", "#Delta#theta"), 200, 0, 40, 500, -3, 3, 8, -0.5, 7.5), "pipth", "Delta_Theta_pip_Cors" if("smear" not in Histo_Smear) else "Delta_Theta_pip_Cors_smeared", "pipsec")
                                # Histograms_All[Mom_Cor_Histo_Name_Angle_Ele]         = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_Angle_Ele, str(Mom_Cor_Histos_Name_Angle_Ele_Title), 200, 0, 40, 360, 0, 360, 8, -0.5, 7.5), "elth"  if("smear" not in Histo_Smear) else "elth_smeared",  "elPhi"  if("smear" not in Histo_Smear) else "elPhi_smeared",  "esec")
                                # Histograms_All[Mom_Cor_Histo_Name_Angle_Pip]         = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_Angle_Pip, str(Mom_Cor_Histos_Name_Angle_Pip_Title), 200, 0, 40, 360, 0, 360, 8, -0.5, 7.5), "pipth" if("smear" not in Histo_Smear) else "pipth_smeared", "pipPhi" if("smear" not in Histo_Smear) else "pipPhi_smeared", "pipsec")
                                Histograms_All[Mom_Cor_Histo_Name_Angle_Ele]         = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_Angle_Ele, str(Mom_Cor_Histos_Name_Angle_Ele_Title), 200, 0, 40, 360, 0, 360, 200, 0, 10), "elth"  if("smear" not in Histo_Smear) else "elth_smeared",  "elPhi"  if("smear" not in Histo_Smear) else "elPhi_smeared",  "el"  if("smear" not in Histo_Smear) else "el_smeared")
                                Histograms_All[Mom_Cor_Histo_Name_Angle_Pip]         = MCH_rdf.Histo3D((Mom_Cor_Histo_Name_Angle_Pip, str(Mom_Cor_Histos_Name_Angle_Pip_Title), 200, 0, 40, 360, 0, 360, 200, 0, 8),  "pipth" if("smear" not in Histo_Smear) else "pipth_smeared", "pipPhi" if("smear" not in Histo_Smear) else "pipPhi_smeared", "pip" if("smear" not in Histo_Smear) else "pip_smeared")

                            ###################################################################################
                            ##          ##          ##                               ##          ##          ##
                            ##==========##==========##  Correction Histograms (End)  ##==========##==========##
                            ##          ##          ##                               ##          ##          ##
                            ###################################################################################


                                if(str(file_location) != 'time'):
                                    Histograms_All[Mom_Cor_Histo_Name_MM_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_MM_Pip].Write()

                                    Histograms_All[Mom_Cor_Histo_Name_DP_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DP_Pip].Write()

                                    Histograms_All[Mom_Cor_Histo_Name_DP_Ele_Theta].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DP_Pip_Theta].Write()

                                    Histograms_All[Mom_Cor_Histo_Name_DTheta_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DTheta_Pip].Write()

                                    Histograms_All[Mom_Cor_Histo_Name_DTheta_Ele_Theta].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_DTheta_Pip_Theta].Write()

                                    Histograms_All[Mom_Cor_Histo_Name_Angle_Ele].Write()
                                    Histograms_All[Mom_Cor_Histo_Name_Angle_Pip].Write()


                                Print_Progress(count_of_histograms, 12, 200 if(str(file_location) != 'time') else 50)
                                count_of_histograms += 12
                                

##################################################=========================================##########################################################################################################################################
##======##======##======##======##======##======##     Normal (1D/2D) Histograms           ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
##################################################=========================================##########################################################################################################################################
                            if(Histo_Group in ["Normal", "Has_Matched", "Bin_Purity", "Delta_Matched"]):

                                Histo_Binning      = [Binning, "All", "All"]
                                Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-[Q2-xB-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), "]"])

            ###################################################################################
            #####====================#####     1D Histograms     #####====================#####
            ###################################################################################

                                if(Histo_Group in ["Has_Matched", "Bin_Purity", "Delta_Matched"]):
                                    for Vars_1D_Test in Variable_Loop:
                                        if(len(Vars_1D_Test) == 4):
                                            # Normal 1D Variable
                                            Vars_1D = Vars_1D_Test
                                        else:
                                            Vars_1D = Multi_Dimensional_Bin_Construction(DF=rdf, Variables_To_Combine=Vars_1D_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="Bin")
                                            
                                        if("2" not in Binning and "Bin_4D" in str(Vars_1D[0]) and "OG" not in str(Vars_1D[0])):
                                            continue # These 4D bins have only been defined with my new binning schemes
                                        if("2" in Binning and "Bin_4D" in str(Vars_1D[0]) and "OG" in str(Vars_1D[0])):
                                            continue # These 4D bins were defined with the original binning scheme

                                        Histo_Var_D1_Name = Dimension_Name_Function(Histo_Var_D1=Vars_1D, Histo_Var_D2="None")

                                        Histo_Name = ((("".join(["((", "; ".join([Histo_Group_Name.replace("".join(["'", str(Histo_Group), "'"]), "".join(["'", str(Histo_Group), "_1D'"])), Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_D1_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")

                                        Normal_rdf = DF_Filter_Function_Full(DF=rdf, Variables=Vars_1D[0], Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1)
                                        if("Combined_" in Vars_1D[0]):
                                            Normal_rdf = Multi_Dimensional_Bin_Construction(DF=Normal_rdf, Variables_To_Combine=Vars_1D_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="DF")

                                        if(Normal_rdf == "continue"):
                                            continue

                                        Title_1D_L1   = "".join([str(Data_Type_Title(Data_Type=Histo_Data, Smearing_Q=Histo_Smear)), " ", str(variable_Title_name(Vars_1D[0]))])
                                        Title_1D_L2   = "".join(["Cut: ", str(Cut_Choice_Title(Cut_Type=Histo_Cut))])
                                        Title_1D_L3   = "" if(Histo_Group == "Normal") else "Matched" if(Histo_Group == "Has_Matched") else "Bin Purity" if(Histo_Group == "Bin_Purity") else "#Delta Between Matches" if(Histo_Group == "Delta_Matched") else "Error"

                                        Title_1D_Axis = "".join(["Q^{2}-x_{B} Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; z-P_{T} Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; ", str(variable_Title_name(Vars_1D[0]))])
                                        if(Histo_Group == "Delta_Matched"):
                                            Title_1D_Axis = "".join(["Q^{2}-x_{B} Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; z-P_{T} Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; ", "#Delta_{(REC - GEN)}", str(variable_Title_name(Vars_1D[0]))])

                                        Title_1D_Out  = "".join(["#splitline{", str(Title_1D_L1), "}{", str(Title_1D_L2), "};", str(Title_1D_Axis)])
                                        if(Title_1D_L3 != ""):
                                            Title_1D_Out  = "".join(["#splitline{#splitline{", str(Title_1D_L1), "}{", str(Title_1D_L2), "}}{", str(Title_1D_L3), "};", str(Title_1D_Axis)])

                                        Title_1D_Out  = Title_1D_Out.replace(") (", " - ")

                                        if(Histo_Group == "Delta_Matched"):
                                            D_Matched_rdf = Delta_Matched_DF(Normal_rdf, Vars_1D[0]) # Calculates the different between the matched reconstructed and generated events (rec - gen)
                                            if(Final_DF == "continue"):
                                                continue


                                        if(Histo_Group not in ["Bin_Purity", "Delta_Matched"]):
                                            Histograms_All[Histo_Name] = Normal_rdf.Histo3D((str(Histo_Name), str(Title_1D_Out), 15, -3.5, 11.5, 55, -3.5, 51.5, Vars_1D[3], Vars_1D[1], Vars_1D[2]), str(Q2_xB_Bin_Filter_str), str(z_pT_Bin_Filter_str), str(Vars_1D[0]))
                                        elif(Histo_Group == "Bin_Purity"):
                                            Histograms_All[Histo_Name] = Bin_Purity_Filter_Fuction(Normal_rdf, Vars_1D[0], Vars_1D[1], Vars_1D[2], Vars_1D[3]).Histo3D((str(Histo_Name), str(Title_1D_Out), 15, -3.5, 11.5, 55, -3.5, 51.5, Vars_1D[3], Vars_1D[1], Vars_1D[2]), str(Q2_xB_Bin_Filter_str), str(z_pT_Bin_Filter_str), str(Vars_1D[0]))
                                        elif(Histo_Group == "Delta_Matched"):
                                            if("el" not in Vars_1D[0] and "pip" not in Vars_1D[0]):
                                                continue # Don't need these extra ∆(REC-GEN) histograms (angles/momentum are the only criteria being considered)
                                            delta_bins = Delta_Matched_Bin_Calc(Vars_1D[0], Vars_1D[1], Vars_1D[2])
                                            if("continue" in delta_bins):
                                                continue
                                            Histograms_All[Histo_Name] = D_Matched_rdf.Histo3D((str(Histo_Name), str(Title_1D_Out), Vars_1D[3], Vars_1D[1], Vars_1D[2], delta_bins[0], delta_bins[1], delta_bins[2], 8, -0.5, 7.5), str(Vars_1D[0]), "Delta_Matched_Value", "pipsec" if("pip" in Vars_1D[0]) else "esec")
                                            if("Phi" in Vars_1D[0]):
                                                Histograms_All["".join([str(Histo_Name), "_Extra_3D"])] = DF_Filter_Function_Full(DF=D_Matched_rdf, Variables=str(Vars_1D[0].replace("Phi", "th")), Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1).Histo3D(("".join([str(Histo_Name), "_Extra_3D"]), "".join([Title_1D_Out.replace("".join(["; ", "#pi^{+} Pion" if("pip" in Vars_1D[0]) else "Electron", " Sector"]), ""), ";#theta_{", "el" if "el" in Vars_1D[0] else "#pi+" ,"}"]), Vars_1D[3], Vars_1D[1], Vars_1D[2], delta_bins[0], delta_bins[1], delta_bins[2], 34, 0, 40), str(Vars_1D[0]), "Delta_Matched_Value", str(Vars_1D[0].replace("Phi", "th")))


                                        if(str(file_location) != 'time'):
                                            Histograms_All[Histo_Name].Write()

                                            if("Phi" in Vars_1D[0] and Histo_Group == "Delta_Matched"):
                                                Histograms_All["".join([str(Histo_Name), "_Extra_3D"])].Write()

                                        # The 1D Histograms are being saved
                                        Print_Progress(count_of_histograms, 2 if("Phi" in Vars_1D[0] and Histo_Group == "Delta_Matched") else 1, 200 if(str(file_location) != 'time') else 50)
                                        count_of_histograms += 1
                                        if("Phi" in Vars_1D[0] and Histo_Group == "Delta_Matched"):
                                            count_of_histograms += 1
                                            
                                # else:
                                #     print("\tSkipping Normal 1D Histograms...")
                                #     # continue



            ###################################################################################
            #####====================#####  1D Histograms (End)  #####====================#####
            ###################################################################################
            ###################################################################################
            #####====================#####     2D Histograms     #####====================#####
            ###################################################################################


                                for Vars_2D in Variable_Loop_2D:

                                    Histo_Var_D2_Name = Dimension_Name_Function(Histo_Var_D1=Vars_2D[0], Histo_Var_D2=Vars_2D[1], Histo_Var_D3="None")
                                    Normal_rdf        = DF_Filter_Function_Full(DF=rdf, Variables=[Vars_2D[0][0], Vars_2D[1][0]], Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning, Sec_type="", Sec_num=-1)
                            
                                    if(Normal_rdf == "continue"):
                                        continue

                ###################################################################################
                #####====================#####     Q2-xB Bin Loop    #####====================#####
                ###################################################################################
                                    for Q2_xB_Bin_Num in List_of_Q2_xB_Bins_to_include:

                                        if(Q2_xB_Bin_Num > 8 and Binning == "2"):
                                            # This binning scheme only goes up to 8 Q2-xB bins
                                            continue

                                        Histo_Binning      = [Binning, "All" if(Q2_xB_Bin_Num == -1) else str(Q2_xB_Bin_Num), "All"]
                                        Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-[Q2-xB-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), "]"])
                                        
                                        Histo_Name    = ((("".join(["((", "; ".join([Histo_Group_Name.replace("".join(["'", str(Histo_Group), "'"]), "".join(["'", str(Histo_Group), "_2D'"])), Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_D2_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")
                                            
                                        Title_2D_L1   = "".join([str(Data_Type_Title(Data_Type=Histo_Data, Smearing_Q=Histo_Smear)), " ", str(variable_Title_name(Vars_2D[0][0])).replace(" (Smeared)", ""), " vs. ", str(variable_Title_name(Vars_2D[1][0]))])
                                        Title_2D_L2   = "".join(["Q^{2}-x_{B} Bin: ", str(Histo_Binning[1])])
                                        Title_2D_L3   = "".join(["Cut: ", str(Cut_Choice_Title(Cut_Type=Histo_Cut))])
                                        Title_2D_Axis = "".join(["z-P_{T} Bin", " (Smeared)" if("smear" in Histo_Smear) else "", "; ", str(variable_Title_name(Vars_2D[0][0])), "; ", str(variable_Title_name(Vars_2D[1][0]))])

                                        Title_2D_Out  = "".join(["#splitline{#splitline{", str(Title_2D_L1), "}{", str(Title_2D_L2), "}}{", str(Title_2D_L3), "};", str(Title_2D_Axis)])

                                        Title_2D_Out  = Title_2D_Out.replace(") (", " - ")
                                        
                                        Bin_Filter    = "esec != -2" if(Q2_xB_Bin_Num == -1) else "".join([str(Q2_xB_Bin_Filter_str), " != 0"]) if(Q2_xB_Bin_Num == -2) else "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Num)])
                                        
                                        Histograms_All[Histo_Name] = (Normal_rdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name), str(Title_2D_Out), 55, -3.5, 51.5, Vars_2D[0][3], Vars_2D[0][1], Vars_2D[0][2], Vars_2D[1][3], Vars_2D[1][1], Vars_2D[1][2]), str(z_pT_Bin_Filter_str), str(Vars_2D[0][0]), str(Vars_2D[1][0]))

                                        if(str(file_location) != 'time'):
                                            Histograms_All[Histo_Name].Write()

                                        # The 2D Histograms are being saved
                                        Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                        count_of_histograms += 1

            ###################################################################################
            #####====================#####  2D Histograms (End)  #####====================#####
            ###################################################################################



##################################################=========================================##########################################################################################################################################
##======##======##======##======##======##======##     Response Matrix (Both Types)        ##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##======##
##################################################=========================================##########################################################################################################################################
                            if(Histo_Group in ["Response_Matrix", "Response_Matrix_Normal"]):

                                if("EDIS" in Histo_Cut):
                                    # Do not need exclusive cuts for the response matrices
                                    continue
                                
                                
                                Res_Binning_2D_Q2_xB = [str(Q2_xB_Bin_Filter_str), -1.5, 10.5,  12]
                                Res_Binning_2D_z_pT  = [str(z_pT_Bin_Filter_str),  -1.5, 50.5,  52]
                                Res_Binning_4D       = ['Bin_Res_4D',              -1.5, 441.5, 443]
                                # Res_Binning_4D_OG  = ['Bin_Res_4D_OG',           -1.5, 441.5, 443]
                                
                                # Res_Binning_2D_Q2_xB = [str(Q2_xB_Bin_Filter_str), -3.5, 11.5,  15]
                                # Res_Binning_2D_z_pT  = [str(z_pT_Bin_Filter_str),  -3.5, 51.5,  55]
                                # Res_Binning_4D       = ['Bin_Res_4D',              -3.5, 442.5, 446]
                                
                                phi_t_Binning_New = copy.deepcopy(phi_t_Binning)
                                if("smear" in Histo_Smear):
                                    phi_t_Binning_New[0] = "".join([str(phi_t_Binning_New[0]), "_smeared" if("smear" not in phi_t_Binning_New[0]) else ""])

                                # Res_Binning_4D       = ['Bin_Res_4D', -1.5, 295 + 1.5, 295 + 4]
                                # # Res_Binning_4D_OG  = ['Bin_Res_4D_OG', -1.5, 344 + 1.5, 344 + 4]

                                # # Res_Var_List = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, W_Binning, Res_Binning_2D_Q2_xB, Res_Binning_2D_z_pT, Binning_4D, Binning_4D_OG, Res_Binning_4D, Res_Binning_4D_OG, Binning_5D, Binning_5D_OG]
                                # Res_Var_List = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, phi_t_Binning, y_Binning, W_Binning, Res_Binning_2D_Q2_xB, Res_Binning_2D_z_pT, Binning_4D, Res_Binning_4D]
                                
                                Res_Var_Add = []
                                # # Res_Var_Add = [[[str(Q2_xB_Bin_Filter_str), 0, 8, 8], phi_t_Binning_New], [[str(z_pT_Bin_Filter_str), 0, 49, 49], phi_t_Binning_New], [[str(Q2_xB_Bin_Filter_str), 0, 8, 8], [str(z_pT_Bin_Filter_str), 0, 49, 49], phi_t_Binning_New]]
                                # # Res_Var_Add = [[[str(Q2_xB_Bin_Filter_str), 0, 8, 8], phi_t_Binning_New], [[str(z_pT_Bin_Filter_str), 0, 49, 49], phi_t_Binning_New]]
                                # Res_Var_Add = [[phi_t_Binning_New, [str(Q2_xB_Bin_Filter_str), 0, 8, 8]], [str(Q2_xB_Bin_Filter_str), 0, 8, 8]]

                                Res_Var_List = copy.deepcopy(List_of_Quantities_1D)
                                if(Res_Var_Add != []):
                                    for Response_Added in Res_Var_Add:
                                        Res_Var_List.append(Response_Added)

                                for Var_List_Test in Res_Var_List:
                                    
                                    if(len(Var_List_Test) == 4):
                                        # Normal 1D Variable
                                        Var_List = Var_List_Test
                                    else:
                                        Var_List = Multi_Dimensional_Bin_Construction(DF=rdf, Variables_To_Combine=Var_List_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="Bin")

                                    variable = Var_List[0]
                                    if(("smear" in Histo_Smear) and ("smear" not in variable)):
                                        variable = "".join([variable, "_smeared"])

                                    Min_range, Max_range, Num_of_Bins = Var_List[1], Var_List[2], Var_List[3]

                                    BIN_SIZE  = round((Max_range - Min_range)/Num_of_Bins, 4)
                                    Bin_Range = "".join([str(Min_range), " #rightarrow ", str(Max_range)])

                                    # Histo_Var_RM_Name = Dimension_Name_Function(Histo_Var_D1=Var_List, Histo_Var_D2="None")
                                    Histo_Var_RM_Name = Dimension_Name_Function(Histo_Var_D1=Var_List, Histo_Var_D2=Res_Binning_2D_z_pT)
                                    
                                    sdf = Bin_Number_Variable_Function(DF_Filter_Function_Full(DF=rdf if(Histo_Data in ["rdf", "gdf"]) else rdf.Filter("PID_el != 0 && PID_pip != 0"), Variables=variable, Titles_or_DF="DF", Q2_xB_Bin_Filter=-1, z_pT_Bin_Filter=-2, Data_Type=Histo_Data, Cut_Choice=Histo_Cut, Smearing_Q=Histo_Smear, Binning_Q=Binning), Variable=variable, min_range=Min_range, max_range=Max_range, number_of_bins=Num_of_Bins, DF_Type=Histo_Data)
                                    if("Combined_" in variable):
                                        sdf = Multi_Dimensional_Bin_Construction(DF=sdf, Variables_To_Combine=Var_List_Test, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="DF_Res")

                                    if(sdf == "continue"):
                                        continue

                ###################################################################################
                #####====================#####     Q2-xB Bin Loop    #####====================#####
                ###################################################################################
                                    for Q2_xB_Bin_Num in List_of_Q2_xB_Bins_to_include:

                                        if((Q2_xB_Bin_Num > 8) and (Binning == "2")):
                                            # This binning scheme only goes up to 8 Q2-xB bins
                                            continue

                                        if((Q2_xB_Bin_Num > 0) and (str(Q2_xB_Bin_Filter_str) in str(variable))):
                                            # Making a response matrix with cuts on the Q2-xB bins is unnecessary for the Q2-xB bin response matrix
                                            continue
                                            
                                        if((Q2_xB_Bin_Num > 0) and (str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT"])):
                                            # Making a response matrix with cuts on the Q2-xB bins is unnecessary for these response matrices (just using as examples for analysis note)
                                            continue

                                        Histo_Binning      = [Binning, "All" if(Q2_xB_Bin_Num == -1) else str(Q2_xB_Bin_Num), "All"]
                                        Histo_Binning_Name = "".join(["Binning-Type:'", str(Histo_Binning[0]) if(str(Histo_Binning[0]) != "") else "Stefan", "'-[Q2-xB-Bin:", str(Histo_Binning[1]), ", z-PT-Bin:", str(Histo_Binning[2]), "]"])
                                        
                                        Histo_Name    = ((("".join(["((", "; ".join([Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_RM_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")
                                        Histo_Name_1D = ((("".join(["((", "; ".join([Histo_Group_Name.replace("".join(["'", str(Histo_Group), "'"]), "".join(["'", str(Histo_Group), "_1D'"])), Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name, Histo_Var_RM_Name]), "))"])).replace("; )", ")")).replace("; ", "), (")).replace(":", "=")

                                        Migration_Title_L1 = "".join(["#scale[1.5]{Response Matrix of ", str(variable_Title_name(variable)), "}"]) if(Histo_Data in ["mdf", "pdf"]) else "".join(["#scale[1.5]{", "Experimental" if(Histo_Data == "rdf") else "Generated" if(Histo_Data != "mdf") else "Reconstructed (MC)", " Distribution of ", str(variable_Title_name(variable)), "}"])                                            
                                        Migration_Title_L2 = "".join(["#scale[1.15]{Cut: ", str(Cut_Choice_Title(Cut_Type=Histo_Cut)), "}"])
                                        Migration_Title_L3 = "".join(["#scale[1.35]{Number of Bins: ", str(Num_of_Bins), " - Range (from Bin 1-", str(Num_of_Bins),"): ", str(Bin_Range), " - Size: ", str(BIN_SIZE), " per bin}"])
                                        
                                        if(Histo_Group == "Response_Matrix_Normal"):
                                            Migration_Title_L3 = "".join(["#scale[1.35]{Range: ", str(Bin_Range), " - Size: ", str(BIN_SIZE), " per bin}"])
                                        if("Bin" in variable):
                                            Migration_Title_L3 = "".join(["#scale[1.35]{Number of Bins: ", str(Num_of_Bins), "}"])

                                        if(Q2_xB_Bin_Num > 0):
                                            Migration_Title_L4 = "".join(["Q^{2}-x_{B} Bin: ", str(Histo_Binning[1])])
                                        else:
                                            Migration_Title_L4 = ""


                                        if(Histo_Group == "Response_Matrix"):
                                            Migration_Title     = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable.replace("_smeared", ""))), " GEN Bins; ", str(variable_Title_name(variable)), " REC Bins"])
                                            if(Histo_Data not in ["mdf", "pdf"]):
                                                Migration_Title = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable)), " REC" if("g" not in Histo_Data) else " GEN", " Bins; z-P_{T} Bins; Count"])
                                        else:
                                            Migration_Title     = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable.replace("_smeared", ""))), " (GEN); ", str(variable_Title_name(variable)), " (REC)"])
                                            if(Histo_Data not in ["mdf", "pdf"]):
                                                Migration_Title = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable)), " (REC" if("g" not in Histo_Data) else " (GEN", "); z-P_{T} Bins; Count"])


                                        if(Histo_Data == "mdf"):
                                            Migration_Title_L1_2  = "".join(["#scale[1.5]{Reconstructed (MC) Distribution of ", str(variable_Title_name(variable)), "}"])
                                            Migration_Title_2     = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1_2), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable)), " REC Bins; z-P_{T} Bins; Count"])
                                            if(Histo_Group == "Response_Matrix_Normal"):
                                                Migration_Title_2 = "".join(["#splitline{#splitline{#splitline{", str(Migration_Title_L1_2), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}}{", str(Migration_Title_L4), "}; ", str(variable_Title_name(variable)), "; z-P_{T} Bins; Count"])
                                        
                                        
                                        if((Histo_Group == "Response_Matrix") and ("Combined_" not in variable)):
                                            num_of_REC_bins, min_REC_bin, Max_REC_bin = (Num_of_Bins + 4), -0.5, (Num_of_Bins + 3.5) # Num of REC bins needs to equal Num of GEN bins for unfolding
                                            num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Num_of_Bins + 4), -0.5, (Num_of_Bins + 3.5)

                                            Variable_Gen = str("".join([str(variable), "_GEN_BIN"])) if("Bin" not in str(variable)) else str("".join([str(variable).replace("_smeared", ""), "_gen"]))
                                            Variable_Rec = str("".join([str(variable), "_REC_BIN"])) if("Bin" not in str(variable)) else str(variable)
                                        else:
                                            num_of_REC_bins, min_REC_bin, Max_REC_bin = Num_of_Bins, Min_range, Max_range
                                            num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = Num_of_Bins, Min_range, Max_range

                                            Variable_Gen = str("".join([str(variable).replace("_smeared", ""), "_gen"]))
                                            Variable_Rec = str(variable)
                                            
                                        # if("Combined_" in variable):
                                        #     print("".join([color.BOLD, "Variable_Gen = ", str(Variable_Gen), color.END]))
                                        #     print("".join([color.BOLD, "Variable_Rec = ", str(Variable_Rec), color.END]))
                                        #     print("\n")
                                        #     print("Printing the full list of variables (and their object types) in the DataFrame...")
                                        #     for ii in range(0, len(sdf.GetColumnNames()), 1):
                                        #         print("".join([str((sdf.GetColumnNames())[ii]), " ( type -> ", sdf.GetColumnType(sdf.GetColumnNames()[ii]), " )"]))
                                        #     print("".join(["\tTotal length= ", str(len(sdf.GetColumnNames()))]))
                                        #     print("\n\n\n\n\n")

                                          
                                        ## Filter for the Q2-xB Bins
                                        Bin_Filter = "esec != -2" if(Q2_xB_Bin_Num == -1) else "".join([str(Q2_xB_Bin_Filter_str), " != 0"]) if(Q2_xB_Bin_Num == -2) else "".join([str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Num)])
                                        
                                        ## Cut for 1D bin migration (don't use for the Q2, xB, z, and pT variables - will result in improper cuts within those plots)
                                        if(("Bin" not in str(variable)) and (Histo_Data in ["mdf", "pdf", "gen"]) and "'phi_t" in str(variable)):
                                            # 1D Unfolding requires events be generated and reconstructed in the same bin
                                            Bin_Filter = "".join(["".join([str(Bin_Filter), " && "]) if(Bin_Filter != "esec != -2") else "", str(Q2_xB_Bin_Filter_str), " == ", str(Q2_xB_Bin_Filter_str).replace("_smeared", "") , "_gen", " && ", str(z_pT_Bin_Filter_str), " == ", str(z_pT_Bin_Filter_str).replace("_smeared", "") , "_gen"])
                                            
                                            
                                        Migration_Title       = "".join([str(Migration_Title),   "; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))])
                                        if(Histo_Data == "mdf"):
                                            Migration_Title_2 = "".join([str(Migration_Title_2), "; ", str(variable_Title_name(Res_Binning_2D_z_pT[0]))])
                                        
                                        if(Histo_Data in ["mdf", "pdf"]):
                                            if(str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT"]):
                                                # Do not need to see the z-pT bins for these plots
                                                Histo_Name                        = str((Histo_Name.replace("'Response_Matrix", "'Response_Matrix")).replace(", (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")).replace(", (Var-D2='z_pT_Bin_2_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")
                                                Migration_Title_Simple            = str(Migration_Title.replace("; z-P_{T} Bin (New) (Smeared)", "")).replace("; z-P_{T} Bin (New)", "")
                                                Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name),    str(Migration_Title_Simple), num_of_GEN_bins, min_GEN_bin, Max_GEN_bin, num_of_REC_bins, min_REC_bin, Max_REC_bin), str(Variable_Gen), str(Variable_Rec))
                                            else:
                                                Histograms_All[Histo_Name]        = (sdf.Filter(Bin_Filter)).Histo3D((str(Histo_Name),    str(Migration_Title),        num_of_GEN_bins, min_GEN_bin, Max_GEN_bin, num_of_REC_bins, min_REC_bin, Max_REC_bin, Res_Binning_2D_z_pT[3], Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                            if(Histo_Data == "mdf"):
                                                if(str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT"]):
                                                    # Do not need to see the z-pT bins for these plots
                                                    Histo_Name_1D                 = str((Histo_Name_1D).replace(", (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")).replace(", (Var-D2='z_pT_Bin_2_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")
                                                    Migration_Title_Simple        = str(Migration_Title_2.replace("; z-P_{T} Bin (New) (Smeared)", "")).replace("; z-P_{T} Bin (New)", "")
                                                    Histograms_All[Histo_Name_1D] = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D), str(Migration_Title_Simple), num_of_REC_bins, min_REC_bin, Max_REC_bin), str(Variable_Rec))
                                                else:
                                                    Histograms_All[Histo_Name_1D] = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title_2),      num_of_REC_bins, min_REC_bin, Max_REC_bin, Res_Binning_2D_z_pT[3], Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                        else:
                                            Histograms_All[Histo_Name_1D]         = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        num_of_REC_bins, min_REC_bin, Max_REC_bin, Res_Binning_2D_z_pT[3], Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
                                            if(str(variable).replace("_smeared", "") in ["Q2", "xB", "z", "pT"]):
                                                # Do not need to see the z-pT bins for these plots
                                                Histo_Name_1D                     = str((Histo_Name_1D).replace(", (Var-D2='z_pT_Bin_2'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")).replace(", (Var-D2='z_pT_Bin_2_smeared'-[NumBins=52, MinBin=-1.5, MaxBin=50.5])", "")
                                                Migration_Title_Simple            = str(Migration_Title.replace("; z-P_{T} Bin (New) (Smeared)", "")).replace("; z-P_{T} Bin (New)", "")
                                                Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo1D((str(Histo_Name_1D), str(Migration_Title_Simple), num_of_REC_bins, min_REC_bin, Max_REC_bin), str(Variable_Rec))
                                            else:
                                                Histograms_All[Histo_Name_1D]     = (sdf.Filter(Bin_Filter)).Histo2D((str(Histo_Name_1D), str(Migration_Title),        num_of_REC_bins, min_REC_bin, Max_REC_bin, Res_Binning_2D_z_pT[3], Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))

                                        if(Histo_Data == "mdf"):
                                            if(str(file_location) != 'time'):
                                                Histograms_All[Histo_Name].Write()
                                                Histograms_All[Histo_Name_1D].Write()
                                            Print_Progress(count_of_histograms, 2, 200 if(str(file_location) != 'time') else 50)
                                            count_of_histograms += 2
                                        else:
                                            if(str(file_location) != 'time'):
                                                Histograms_All[Histo_Name_1D].Write()
                                            Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                            count_of_histograms += 1




######################################################################
##=====##=====##=====##    End of Main Loop    ##=====##=====##=====##
######################################################################




        ######################################===============================######################################
        ##==========##==========##==========##          End of Code          ##==========##==========##==========##
        ######################################===============================######################################

        if(str(file_location) != 'time'):
            ROOT_File_Output.Close()
        # File has been saved

        print("".join([color.BOLD, "\nTotal Number of Histograms Made: ", str(count_of_histograms), color.END]))
        
        
        # See beginning of code...
        if(output_all_histo_names_Q == "yes"):
            print("\nHistograms be made:")
            for ii in Histograms_All:
                print(str(ii))
                if(";" in str(ii)):
                    print("".join([color.RED, "SEMI-COLON ERROR: ", str(ii), color.END]))
            print("\n")
        elif(str(file_location) == "time"):
            print("\nChoose not to print list of final histograms...\nSet output_all_histo_names_Q = 'yes' or enter 'test' instead of a file name to print a list of histograms made while running...\n")
        
        
    elif(output_type not in ["histo", "test", "time"]):
        print("Taking Snapshot...")
        rdf.Snapshot("h22", ROOT_File_Output_Name)
        print("Done\n\n")
    
    # Getting current date
    datetime_object_end = datetime.now()

    endMin_full, endHr_full, endDay_full = datetime_object_end.minute, datetime_object_end.hour, datetime_object_end.day

    if(datetime_object_end.minute < 10):
        timeMin_end = ''.join(['0', str(datetime_object_end.minute)])
    else:
        timeMin_end = str(datetime_object_end.minute)
    
    # Printing current time
    if(datetime_object_end.hour > 12 and datetime_object_end.hour < 24):
        print("".join(["The time that this code finished is ", str((datetime_object_end.hour) - 12), ":", timeMin_end, " p.m."]))
    if(datetime_object_end.hour < 12 and datetime_object_end.hour > 0):
        print("".join(["The time that this code finished is ", str(datetime_object_end.hour), ":", timeMin_end, " a.m."]))
    if(datetime_object_end.hour == 12):
        print("".join(["The time that this code finished is ", str(datetime_object_end.hour), ":", timeMin_end, " p.m."]))
    if(datetime_object_end.hour == 0 or datetime_object_end.hour == 24):
        print("".join(["The time that this code finished is 12:", timeMin_end, " a.m."]))
        
    print("".join(["Made ", str(count_of_histograms), " histograms..."]))
        
    Num_of_Days, Num_of_Hrs, Num_of_Mins = 0, 0, 0
    
    
    if(startDay_full > endDay_full):
        Num_of_Days = endDay_full + (30 - startDay_full)
    else:
        Num_of_Days = endDay_full - startDay_full
        
    if(startHr_full > endHr_full):
        Num_of_Hrs = endHr_full + (24 - startHr_full)
    else:
        Num_of_Hrs = endHr_full - startHr_full
        
    if(startMin_full > endMin_full):
        Num_of_Mins = endMin_full + (60 - startMin_full)
    else:
        Num_of_Mins = endMin_full - startMin_full
        
        
    if(Num_of_Hrs > 0 and startMin_full >= endMin_full):
        Num_of_Hrs += -1
        
    if(Num_of_Days > 0 and startHr_full >= endHr_full):
        Num_of_Days += -1
        
        
    print("\nThe total time the code took to run the given files is:")
    print("".join([str(Num_of_Days), " Day(s), ", str(Num_of_Hrs), " Hour(s), and ", str(Num_of_Mins), " Minute(s)."]))
    
    
    if((((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins) != 0):
        rate_of_histos = count_of_histograms/(((Num_of_Days*24) + Num_of_Hrs)*60 + Num_of_Mins)
        print("".join(["Rate of Histos/Minute = ", str(rate_of_histos), " Histos/Min"]))
    

    # if(str(file_location) in ['time' , 'test'] and (datatype == "mdf")):
    if(str(file_location) in ['time' , 'test']):
        print("".join(["\nEstimated time to run: ", "".join([str(round(count_of_histograms/6, 4)), " mins"]) if(round(count_of_histograms/6, 4) < 60) else  "".join([str(int(round(count_of_histograms/6, 4)/60)), " hrs and ", str(round(((round(count_of_histograms/6, 4)/60)%1)*60, 3)), " mins (Total: ", str(round(count_of_histograms/6, 3)), " mins)"])]))
        # Estimate based on observations made on 12-2-2022 (estimates are very rough - based on the "mdf" run option)
    
    
    print("\n")
    
    ######################################===============================######################################
    ##==========##==========##==========##          End of Code          ##==========##==========##==========##
    ######################################===============================######################################
    
    
else:
    print("\nERROR: No valid datatype selected...\n")
    
# This Code was last updated on 2-13-2023