# This Code was last updated on 9-22-2022
# # Note-to-self: Also always update this note at end of script


# Most recent update notes:

# # All Updates have been moved to the github page/README.md file

    
# # This Code has been coverted such that 3D histograms are made instead of filtering Q2-xB/z-pT bins






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




if(str(file_location) == 'all'):
    print("\nRunning all files together...\n")
if(str(file_location) == 'time'):
    print("\nRunning Count. Not saving results...\n")
    

if(datatype == 'rdf' or datatype == 'mdf' or datatype == 'gdf' or datatype == 'pdf'):
    
    file_num = str(file_location)

    if(datatype == "rdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00", "")).replace(".hipo.root", "")

    if(datatype == "mdf" or datatype == "pdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")
        
    if(datatype == "gdf"):
        file_num = str(file_num.replace("/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_", "")).replace(".hipo.root", "")

    
    
    ########################################################################################################################################################################
    ##==================================================================##============================##==================================================================##
    ##===============##===============##===============##===============##     Loading Data Files     ##===============##===============##===============##===============##
    ##==================================================================##============================##==================================================================##
    ########################################################################################################################################################################
    
    
    if(datatype == 'rdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*")
            files_used_for_data_frame = "Data_sidis_epip_richcap.inb.qa.skim4_00*"
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            files_used_for_data_frame = "".join(["Data_sidis_epip_richcap.inb.qa.skim4_00", str(file_num), "*"])
            
    if(datatype == 'mdf' or datatype == 'pdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*")
            files_used_for_data_frame = "MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*"
        else:
            rdf = ROOT.RDataFrame("h22", str(file_location))
            files_used_for_data_frame = "".join(["MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_", str(file_num), "*"])
            
    if(datatype == 'gdf'):
        if(str(file_location) == 'all' or str(file_location) == 'All' or str(file_location) == 'time'):
            rdf = ROOT.RDataFrame("h22", "/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*")
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
    
    Extra_Name = "Mom_Cor_Response_Matrix_V2_"
    # Removed everything except the the "Response Matrix" and "Momentum Correction" histograms from 'Mom_Cor_Response_Matrix_V2'
    
    Extra_Name = "Mom_Cor_Response_Matrix_V3_"
    # Needed the Matrices to be square for unfolding
        # Also changed :
        # (*) The reconstructed MC files do not produce 1D histograms anymore (only produce the ∆P histograms and the 2D Response Matrices)
        # (*) The ∆P histograms will now note (in the title) whether or not the momentums were being corrected when run (only affects the experimental files)
        
    Extra_Name = "Mom_Cor_Response_Matrix_V4_"
    # Testing new smearing functions (failed to update properly)
    
    Extra_Name = "Mom_Cor_Response_Matrix_V5_"
    # Modified FX's smearing function for momentum (pol2 function of electron momentum)
    # Changed datatype names so that the Matched MC REC data now runs with mdf
        # pdf is no specifically used for selecting ONLY matched events
        # mdf does not run the option for gen histograms (i.e., matched generated events) --> pdf option still runs these options
    # Added additional histograms for correction/smearing functions
    # Removed unnecessary options including:
      # 1) option = bin_2D_purity
      # 2) option = counts
      # 3) option = bin_migration_V2
      # 4) option = bin_migration_V4
    # Added option to run regular 2D histograms separately from regular 1D histograms (options "normal_1D" and "normal_2D")
    # Correction/Smearing Histograms (i.e., option == "Mom_Cor_Code") now requires either fully exclusive events or full SIDIS cuts (requirment for cuts)
        # Calculations are designed only for exclusive reactions, but SIDIS reactions are allowed here for comparison purposes
    # Removed cut option: cut_Complete
        # This option is missing final cuts to make the event selection either exclusive or propperly semi-inclusive. Not worth running at this time
    # Added phi_t Binning to response matrices
    
    
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
    
    print("".join(["File being made is: ", ROOT_File_Output_Name]))
    
    
    
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
                    dp = ((1.57e-06)*phi*phi + (5.021e-05)*phi + (-1.74089e-03))*pp*pp + ((-2.192e-05)*phi*phi + (-1.12528e-03)*phi + (0.0146476))*pp + ((8.504e-05)*phi*phi + (2.08012e-03)*phi + (-0.0122501));
                }
                if(sec == 2){
                    dp = ((-3.98e-06)*phi*phi + (1.66e-05)*phi + (-1.55918e-03))*pp*pp + ((2.136e-05)*phi*phi + (-5.7373e-04)*phi + (0.0143591))*pp + ((2.4e-06)*phi*phi + (1.6656e-03)*phi + (-0.0218711));
                }
                if(sec == 3){
                    dp = ((5.57e-06)*phi*phi + (2.3e-07)*phi + (-2.26999e-03))*pp*pp + ((-7.761e-05)*phi*phi + (4.1437e-04)*phi + (0.0152985))*pp + ((2.2542e-04)*phi*phi + (-9.442e-04)*phi + (-0.0231432));
                }
                if(sec == 4){
                    dp = ((3.48e-06)*phi*phi + (2.166e-05)*phi + (-2.29e-04))*pp*pp + ((-2.758e-05)*phi*phi + (7.226e-05)*phi + (-3.38e-03))*pp + ((3.166e-05)*phi*phi + (6.93e-05)*phi + (0.04767));
                }
                if(sec == 5){
                    dp = ((1.19e-06)*phi*phi + (-2.286e-05)*phi + (-1.6332e-04))*pp*pp + ((-1.05e-06)*phi*phi + (7.04e-05)*phi + (-5.0754e-03))*pp + ((-7.22e-06)*phi*phi + (4.1748e-04)*phi + (0.04441));
                }
                if(sec == 6){
                    dp = ((-5.97e-06)*phi*phi + (-3.689e-05)*phi + (5.782e-05))*pp*pp + ((6.573e-05)*phi*phi + (2.1376e-04)*phi + (-9.54576e-03))*pp + ((-1.7732e-04)*phi*phi + (-8.62e-04)*phi + (0.0618975));
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
                    dp = ((-5.2e-07)*phi*phi + (-1.383e-05)*phi + (4.7179e-04))*pp*pp + ((8.33e-06)*phi*phi + (3.8849e-04)*phi + (-6.81319e-03))*pp + ((-1.645e-05)*phi*phi + (-5.0057e-04)*phi + (1.9902e-02));
                }
                if(sec == 2){
                    dp = ((-1.88e-06)*phi*phi + (3.303e-05)*phi + (1.1331e-03))*pp*pp + ((1.569e-05)*phi*phi + (-3.974e-05)*phi + (-1.25869e-02))*pp + ((-2.903e-05)*phi*phi + (-1.0638e-04)*phi + (2.61529e-02));
                }
                if(sec == 3){
                    dp = ((2.4e-07)*phi*phi + (-1.04e-05)*phi + (7.0864e-04))*pp*pp + ((8.0e-06)*phi*phi + (-5.156e-05)*phi + (-8.12169e-03))*pp  + ((-2.42e-05)*phi*phi + (8.928e-05)*phi + (2.13223e-02));
                }
                if(sec == 4){
                    dp = ((-4.0e-08)*phi*phi + (-3.59e-05)*phi + (1.32146e-03))*pp*pp + ((1.023e-05)*phi*phi + (2.2199e-04)*phi + (-1.33043e-02))*pp + ((-2.801e-05)*phi*phi + (-1.576e-04)*phi + (3.27995e-02));
                }
                if(sec == 5){
                    dp = ((2.7e-06)*phi*phi + (5.03e-06)*phi + (1.59668e-03))*pp*pp + ((-1.28e-05)*phi*phi + (-1.99e-06)*phi + (-1.71578e-02))*pp + ((2.091e-05)*phi*phi + (-4.14e-05)*phi + (3.25434e-02));
                }
                if(sec == 6){
                    dp = ((2.13e-06)*phi*phi + (-7.49e-05)*phi + (1.75565e-03))*pp*pp + ((-7.37e-06)*phi*phi + (5.8222e-04)*phi + (-1.27969e-02))*pp + ((4.9e-07)*phi*phi + (-7.2253e-04)*phi + (3.11499e-02));
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
        print("\nNot running with Momentum Corrections\n")
    else:
        print("\nRunning with Momentum Corrections\n")
        

        
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

            // From ∆P(El) Sigma distributions:
            momR *= 0.08267*V4.P()*V4.P() + (-0.89415)*V4.P() + 3.73819;

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
    
    
    
    ##===============================================================================================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##=================================##     Applying the Smearing Functions     ##=================================##
    ##---------------------------------##=========================================##---------------------------------##
    ##===============================================================================================================##
    
    if(datatype == "mdf" or datatype == "pdf"):
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

        // smear_func(beam) //===// DO NOT SMEAR BEAM/TARGET -- ONLY SMEAR OUTGOING PARTICLES //===//
        // smear_func(targ) //===// DO NOT SMEAR BEAM/TARGET -- ONLY SMEAR OUTGOING PARTICLES //===//


        TLorentzVector ele_smeared = smear_func(ele);


        TLorentzVector pip0_smeared = smear_func(pip0);


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
        
        if("smear" not in Smearing_Q or (datatype != "mdf" and datatype != "pdf")):
            # Variable should already be defined/cannot smear real/generated data
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

            TLorentzVector ele_smeared = smear_func(ele);
            TLorentzVector pip0_smeared = smear_func(pip0);

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

            TLorentzVector ele_smeared = smear_func(ele);
            TLorentzVector pip0_smeared = smear_func(pip0);

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

            TLorentzVector ele_smeared = smear_func(ele);
            TLorentzVector pip0_smeared = smear_func(pip0);

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

            TLorentzVector ele_smeared = smear_func(ele);
            TLorentzVector pip0_smeared = smear_func(pip0);

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
        
        TLorentzVector ele_smeared = smear_func(eleS);
        TLorentzVector pip_smeared = smear_func(pipS);
        
        ele = ROOT::Math::PxPyPzMVector(ele_smeared.X(), ele_smeared.Y(), ele_smeared.Z(), 0);
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
            Bin_Res_4D = -1;
            return Bin_Res_4D;
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
    
    if(datatype == "mdf" or datatype == "pdf"):
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


    def bin_purity_filter_fuction(dataframe, variable, min_range, max_range, number_of_bins):

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




    def bin_purity_save_fuction(dataframe, variable, min_range, max_range, number_of_bins):

        variable = variable.replace("_gen", "")

        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])

        out_put_DF = dataframe


        if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable or "Bin_4D" in variable or "Bin_5D" in variable):
            # Already defined
            return dataframe

        else:

            bin_size = (max_range - min_range)/number_of_bins


            rec_bin = "".join(["(", str(variable), " - ", str(min_range), ")/", str(bin_size)])

            gen_bin = "".join(["(", str(gen_variable), " - ", str(min_range), ")/", str(bin_size)])

            out_put_DF = out_put_DF.Define("".join([str(variable), "_REC_BIN"]), rec_bin)
            out_put_DF = out_put_DF.Define("".join([str(variable), "_GEN_BIN"]), gen_bin)


        return out_put_DF



    def bin_purity_save_fuction_New(dataframe, variable, min_range, max_range, number_of_bins, DFrame):

        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])

        out_put_DF = dataframe


        if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable or "Bin_4D" in variable or "Bin_5D" in variable):
            # Already defined
            return dataframe

        else:

            bin_size = (max_range - min_range)/number_of_bins

            rec_bin = "".join(["""

            int rec_bin = ((""", str(variable), """ - """, str(min_range), """)/""", str(bin_size), """) + 1;

            if(""", str(variable), """ < """, str(min_range), """){
                // Below binning range
                rec_bin = 0;
            }

            if(""", str(variable), """ > """, str(max_range), """){
                // Above binning range
                rec_bin = """, str(number_of_bins + 1), """;
            }

            return rec_bin;

            """])


            gen_bin = "".join(["""

            int gen_bin = ((""", str(gen_variable), """ - """, str(min_range), """)/""", str(bin_size), """) + 1;

            if(""", str(gen_variable), """ < """, str(min_range), """){
                // Below binning range
                gen_bin = 0;
            }

            if(""", str(gen_variable), """ > """, str(max_range), """){
                // Above binning range
                gen_bin = """, str(number_of_bins + 1), """;
            }

            if(PID_el == 0 || PID_pip == 0){
                // Event is unmatched
                gen_bin = """, str(number_of_bins + 2), """;
            }

            return gen_bin;

            """])

            out_put_DF = out_put_DF.Define("".join([str(variable), "_REC_BIN"]), rec_bin)
            if(DFrame != "rdf" and DFrame != "gdf"):
                out_put_DF = out_put_DF.Define("".join([str(variable), "_GEN_BIN"]), gen_bin)


        return out_put_DF



    def bin_purity_save_filter_fuction(dataframe, variable, min_range, max_range, number_of_bins, REC_BIN_FILTER):

        variable = variable.replace("_gen", "")

        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])

        variable = variable.replace("_gen", "")

        out_put_DF = dataframe

        if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable):
            filter_name = "".join([variable, " == ", str(REC_BIN_FILTER), " && PID_el != 0 && PID_pip != 0"])

        else:

            bin_size = (max_range - min_range)/number_of_bins

            filter_name = "".join(["""

            int rec_bin = (""", str(variable), """ - """, str(min_range), """)/""", str(bin_size), """;

            bool filter_Q = (rec_bin == """, str(REC_BIN_FILTER), """ && PID_el != 0 && PID_pip != 0);

            return filter_Q;

            """])

            gen_bin = "".join(["(", str(gen_variable), " - ", str(min_range), ")/", str(bin_size)])

            out_put_DF = out_put_DF.Define("".join([str(variable), "_GEN_BIN"]), gen_bin)


        return out_put_DF.Filter(filter_name)




    def Delta_Matched_DF(dataframe, variable):
        output = "continue"
        gen_variable = "".join([variable.replace("_smeared", ""), "_gen"])
        if("Q2_xB_Bin" in variable or "z_pT_Bin" in variable or "sec" in variable or dataframe == "continue"):
            # Cannot uses these types of variables in this type of histogram
            return "continue"
        else:
            output = dataframe.Define("Delta_Matched_Value", "".join([str(variable), " - ", str(gen_variable)]))

        return output





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
    
    
    
    
    
    
    ###################################################################################################################################################################
    ###################################################                 Done With Kinematic Binning                 ###################################################
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###----------------------------------------------##-------------------------------------------------------------##----------------------------------------------###
    ###                                              ##-------------------------------------------------------------##                                              ###
    ###################################################          Defining Helpful Functions for Histograms          ###################################################
    ###################################################################################################################################################################

    
    
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
        if(variable == 'phi_t'):
            output = "#phi_{t}"
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
    
    
    
    
    
    ###################=======================================###################
    ##===============##     Full Filter + Histogram Title     ##===============##
    ###################=======================================###################
    
    def DF_Filter_Function_Full(DF, Sec_type, Sec_num, Q2_xB_Bin_Filter, z_pT_Bin_Filter, Variables, Smearing_Q, Data_Type, Cut_Choice, Titles_or_DF):

        if("2" not in Smearing_Q and "P2" in Cut_Choice):
            return "continue"
        
        if('str' in str(type(Variables)) and Q2_xB_Bin_Filter != -1 and Variables != "2D_Purity"):
            return "continue"

        ##============================================##
        ##----------## Setting Data Title ##----------##
        ##============================================##
        if(Titles_or_DF == 'Title'):
            if(Data_Type == 'rdf'):
                Data_Title = "Real Data"
            if(Data_Type == 'mdf' or Data_Type == 'pdf' or Data_Type == 'udf' or ("miss_idf" in Data_Type)):
                Data_Title = "".join(["Monte Carlo Data (REC", " - Smeared)" if "smear" in Smearing_Q else ")"])
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
        ##============================================##
        ##----------## Setting Data Title ##----------##
        ##============================================##


        ##===============================================##
        ##----------## Skipping Bad Requests ##----------##
        ##===============================================##
        # No smearing frames which are not the Monte Carlo Reconstructed
        if((Data_Type != "mdf" and Data_Type != "pdf" and Data_Type != "udf" and ("miss_idf" not in Data_Type)) and "smear" in Smearing_Q):
            return "continue"
        # No Cuts for Monte Carlo Generated events
        if((Data_Type == "gdf" or Data_Type == "gen") and "no_cut" not in Cut_Choice):
            return "continue"
        # No PID cuts except for matched MC events
        if((Data_Type != "pdf" and Data_Type != "gen") and "PID" in Cut_Choice):
            return "continue"
        ##===============================================##
        ##----------## Skipping Bad Requests ##----------##
        ##===============================================##

        
        ##=======================================================##
        ##----------## Smeared Binning (MC REC Only) ##----------##
        ##=======================================================##
        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_xB_Bin", "z_pT_Bin"
        if("2" in Smearing_Q):
            Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_2"]), "".join([z_pT_Bin_Filter_str, "_2"])
        # No smearing frames which are not the Monte Carlo Reconstructed
        if((Data_Type == "mdf" or Data_Type == "pdf" or Data_Type == "udf" or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q):
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
        if((Data_Type == "pdf" or Data_Type == "gen") and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el != 0 && PID_pip != 0")
            
        if(Data_Type == "udf" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("PID_el == 0 || PID_pip == 0")
            
        if(Data_Type == "miss_idf" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && (PID_el != 11 || PID_pip != 211)")
            
        if(Data_Type == "miss_idf_el" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_el != 11")
            
        if(Data_Type == "miss_idf_pip" and Titles_or_DF == 'DF'):
            DF_Out = DF_Out.Filter("(PID_el != 0 && PID_pip != 0) && PID_pip != 211")

            
            
        if(Data_Type != "gdf" and Data_Type != "gen" and "no_cut" != Cut_Choice):
            
            if("Complete" in Cut_Choice):
                
                cutname = " Complete Set of "
                
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
                if("exclusive" in Cut_Choice):
                    if(Titles_or_DF == 'DF'):
                        DF_Out = DF_Out.Filter(str(Calculated_Exclusive_Cuts(Smearing_Q)))
                    cutname = "".join([" Exclusive ", "(Smeared) " if("smear" in Smearing_Q) else "", "Cuts"])

                if((Data_Type == "mdf" or Data_Type == "pdf" or Data_Type == "udf" or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q):
                    if("Exclusive" not in cutname):
                        cutname = " (Smeared)"
                    #-----------------------------#
                    #-----# As of 3-10-2022 #-----#
                    #-----------------------------#
                    if("all" in Cut_Choice):
                        if(Titles_or_DF == 'DF'):
                            # DF_Out = DF_Out.Filter("y < 0.75             && xF > 0               && W > 2               && Q2 > 1              && MM > 1.5                    && pip > 1.25              && pip < 5              && 5 < elth             && elth < 35             && 5 < pipth            && pipth < 35")
                            DF_Out = DF_Out.Filter("smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 1 && sqrt(smeared_vals[1]) > 1.5 && smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
                        cutname = " All (Smeared) Cuts"
                    else:
                        if('SIDIS' in Cut_Choice):
                            if(Titles_or_DF == 'DF'):
                                # DF_Out = DF_Out.Filter("y < 0.75             && xF > 0               && W > 2               && Q2 > 1")
                                DF_Out = DF_Out.Filter("smeared_vals[7] < 0.75 && smeared_vals[12] > 0 && smeared_vals[6] > 2 && smeared_vals[2] > 1")
                            cutname = "".join([cutname, " " if cutname == " (Smeared)" else " + ", "SIDIS Cuts"])
                        if('Mom' in Cut_Choice):
                            if(Titles_or_DF == 'DF'):
                                # DF_Out = DF_Out.Filter("pip > 1.25            && pip < 5              && 5 < elth             && elth < 35             && 5 < pipth            && pipth < 35")
                                DF_Out = DF_Out.Filter("smeared_vals[19] > 1.25 && smeared_vals[19] < 5 && 5 < smeared_vals[17] && smeared_vals[17] < 35 && 5 < smeared_vals[21] && smeared_vals[21] < 35")
                            cutname = "".join([cutname, " " if cutname == " (Smeared)" else " + ", "Mom Cuts"])
                    if("Q2" in Cut_Choice):
                        if(Titles_or_DF == 'DF'):
                            # DF_Out = DF_Out.Filter("Q2 > 2")
                            DF_Out = DF_Out.Filter("smeared_vals[2] > 2")
                        cutname = "".join([cutname, " " if cutname == " (Smeared)" else " + ", "(New) Q^{2} Cut"])
                    if(Data_Type == "pdf" and 'PID' in Cut_Choice):
                        cutname = "".join([cutname, " " if cutname == " (Smeared)" else " + ", "Matched PID Cut"])
                        if(Titles_or_DF == 'DF'):
                            DF_Out = DF_Out.Filter("PID_el == 11 && PID_pip == 211")
                else:
                    if("all" in Cut_Choice):
                        if(Titles_or_DF == 'DF'):
                            DF_Out = DF_Out.Filter("y < 0.75 && xF > 0 && W > 2 && Q2 > 1 && sqrt(MM2) > 1.5 && pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
                        if("Exclusive" not in cutname):
                            cutname = " All Cuts"
                        else:
                            cutname = "".join([cutname, " " if cutname == " " else " + ", "All SIDIS Cuts"])
                    else:
                        if('SIDIS' in Cut_Choice):
                            if(Titles_or_DF == 'DF'):
                                DF_Out = DF_Out.Filter("y < 0.75 && xF > 0 && W > 2 && Q2 > 1")
                            cutname = "".join([cutname, "" if cutname == " " else " + ", "SIDIS Cuts"])
                        if('Mom' in Cut_Choice):
                            if(Titles_or_DF == 'DF'):
                                DF_Out = DF_Out.Filter("pip > 1.25 && pip < 5 && 5 < elth && elth < 35 && 5 < pipth && pipth < 35")
                            cutname = "".join([cutname, "" if cutname == " " else " + ", "Mom Cuts"])
                    if("Q2" in Cut_Choice):
                        if(Titles_or_DF == 'DF'):
                            DF_Out = DF_Out.Filter("Q2 > 2")
                        cutname = "".join([cutname, " " if cutname == " " else " + ", "(New) Q^{2} Cut"])
                    if(Data_Type == "pdf" and 'PID' in Cut_Choice):
                        cutname = "".join([cutname, " " if cutname == " " else " + ", "Matched PID Cut"])
                        if(Titles_or_DF == 'DF'):
                            DF_Out = DF_Out.Filter("PID_el == 11 && PID_pip == 211")
                if('Valerii_Cut' in Cut_Choice):
                    if(Titles_or_DF == 'DF'):
                        DF_Out = filter_Valerii(DF_Out, Cut_Choice)
                    cutname = "".join([cutname, "" if(" " == cutname or " (Smeared)" == cutname) else " + ", "Valerii Cuts"])

                if("P2" in Cut_Choice):
                    if(Titles_or_DF == 'DF'):
                        DF_Out = bin_purity_filter_fuction(DF_Out, Q2_xB_Bin_Filter_str, 0, 0, 20)
                    cutname = "".join([cutname, "" if(" " == cutname or " (Smeared)" == cutname) else " + ", "Binning Purity (New)"])
                    
        else:
            # Generated Monte Carlo should not have cuts applied to it
            cutname = " No Cuts"
        ##################################################
        ##==========##  General Cuts (End)  ##==========##
        ##################################################




        ##====================================================##
        ##----------## Smearing Variables (Start) ##----------##
        ##====================================================##
        # This information does not need to be run if titles are the only things of interest
        if((Data_Type == "mdf" or Data_Type == "pdf" or Data_Type == "udf" or ("miss_idf" in Data_Type)) and "smear" in Smearing_Q and Titles_or_DF == 'DF'):
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

        ##==========## Title Creation ##==========##
        if(Titles_or_DF == 'Title'):
            Title_out_put = "error"
            if('str' in str(type(Variables))):
                # This indicates that the title is for a 1D histogram
                Title_out_put = "".join(["#splitline{", str(Data_Title), " ", str(variable_Title_name(Variables)), "}{", str(Sector_Title_Name), str(cutname), "}; ", str(variable_Title_name(Q2_xB_Bin_Filter_str)), "; ", str(variable_Title_name(z_pT_Bin_Filter_str)), "; ", str(variable_Title_name(Variables))])
            else:
                # Variables = list of variables (for 2D histograms)
                Title_out_put = "".join(["#splitline{", str(Data_Title), " ", str(variable_Title_name(Variables[0])), " vs ", str(variable_Title_name(Variables[1])), "}{", str(Sector_Title_Name), Q2_xB_BinList_Name, str(cutname), "}; ", z_pT_Bin_Filter_str, "; ", str(variable_Title_name(Variables[0])), "; ", str(variable_Title_name(Variables[1]))])
            return Title_out_put
        ##==========## Title Creation ##==========##


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
    ##===============##     Full Filter + Histogram Title     ##===============##
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

    List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # List_of_Q2_xB_Bins_to_include = [-1, -2]
#     List_of_Q2_xB_Bins_to_include = [-1]


    List_of_Q2_xB_Bins_to_include = [-1, 1, 2, 3, 4, 5, 6, 7, 8]
    
    
    
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
    
    
    

    cut_list = ['no_cut', 'cut_Complete', 'cut_Complete_EDIS', 'cut_Complete_SIDIS']
    cut_list = ['no_cut', 'cut_Complete_EDIS', 'cut_Complete_SIDIS']

    
    
    #####################       Cut Choices       #####################
    ###################################################################
    
    
    
    #####################################################################################################################
    ###############################################     3D Histograms     ###############################################
    

    # Bin Set Option: 20 bins
#     Q2_Binning = ['Q2', 0, 12.5, 25]
#     Q2_Binning_Smeared = ['Q2_smeared', 0, 12.5, 25]
    
    # Bin Set Option: 20 bins (Actual total bins = 27)
    Q2_Binning = ['Q2', -0.3378, 12.2861, 27]
    Q2_Binning_Smeared = ['Q2_smeared', -0.3378, 12.2861, 27]
    # Bin size: 0.46755 per bin
    
#     xB_Binning = ['xB', -0.08, 0.92, 25]
#     xB_Binning_Smeared = ['xB_smeared', -0.08, 0.92, 25]
    
    # Bin Set Option: 20 bins (Actual total bins = 25)
    xB_Binning = ['xB', -0.006, 0.8228, 25]
    xB_Binning_Smeared = ['xB_smeared', -0.006, 0.8228, 25]
    # Bin size: 0.03315 per bin

    z_Binning = ['z', 0.006, 1.014, 28]
    z_Binning_Smeared = ['z_smeared', 0.006, 1.014, 28]
    
    pT_Binning = ['pT', -0.15, 1.8, 26]
    pT_Binning_Smeared = ['pT_smeared', -0.15, 1.8, 26]

    y_Binning = ['y', -0.0075, 0.9975, 36]
    y_Binning_Smeared = ['y_smeared', -0.0075, 0.9975, 36]
    # Bin size: 0.0275
    
    phi_t_Binning = ['phi_t', 0, 360, 36]
    phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 36]








    # Bin Set Option: GRC Poster binning
    Q2_Binning = ['Q2', 2, 11.351, 5]
    Q2_Binning_Smeared = ['Q2_smeared', 2, 11.351, 5]
    # Bin size: 1.8702 per bin
    
    xB_Binning = ['xB', 0.126602, 0.7896, 5]
    xB_Binning_Smeared = ['xB_smeared', 0.126602, 0.7896, 5]
    # Bin size: 0.1325996 per bin

    z_Binning = ['z', 0.15, 0.7, 5]
    z_Binning_Smeared = ['z_smeared', 0.15, 0.7, 5]
    # Bin size: 0.11 per bin
    
    pT_Binning = ['pT', 0.05, 1, 5]
    pT_Binning_Smeared = ['pT_smeared', 0.05, 1, 5]
    # Bin size: 0.19 per bin

    y_Binning = ['y', 0, 1, 5]
    y_Binning_Smeared = ['y_smeared', 0, 1, 5]
    # Bin size: 0.2 per bin
    
    phi_t_Binning = ['phi_t', 0, 360, 36]
    phi_t_Binning_Smeared = ['phi_t_smeared', 0, 360, 36]
    # Bin size: 10 per bin
    
    
    
    # Post-GRC Binning
    Q2_Binning = ['Q2', 1.4805, 11.8705, 20]
    Q2_Binning_Smeared = ['Q2_smeared', 1.4805, 11.8705, 20]
    # Bin size: 0.5195 per bin

    xB_Binning = ['xB', 0.08977, 0.82643, 20]
    xB_Binning_Smeared = ['xB_smeared', 0.08977, 0.82643, 20]
    # Bin size: 0.03683 per bin

    z_Binning = ['z', 0.11944, 0.73056, 20]
    z_Binning_Smeared = ['z_smeared', 0.11944, 0.73056, 20]
    # Bin size: 0.03056 per bin
    
    pT_Binning = ['pT', 0, 1.05, 20]
    pT_Binning_Smeared = ['pT_smeared', 0, 1.05, 20]
    # Bin size: 0.05 per bin

    y_Binning = ['y', 0, 1, 20]
    y_Binning_Smeared = ['y_smeared', 0, 1, 20]
    # Bin size: 0.05 per bin
    
    
    MM_Binning = ['MM', 0, 3.5, 500]
    MM_Binning_Smeared = ['MM_smeared', 0, 3.5, 500]
    
    W_Binning = ['W', 0, 6, 200]
    W_Binning_Smeared = ['W_smeared', 0, 6, 200]
    

    Binning_4D = ['Bin_4D', -1.5, 303.5, 306]
    Binning_4D_Smeared = ['Bin_4D_smeared', -1.5, 303.5, 306]
    
    Binning_4D_OG = ['Bin_4D_OG', -1.5, 353.5, 356]
    Binning_4D_OG_Smeared = ['Bin_4D_OG_smeared', -1.5, 353.5, 356]
    
    
    Binning_5D = ['Bin_5D', -1.5, 11625.5, 11628]
    Binning_5D_Smeared = ['Bin_5D_smeared', -1.5, 11625.5, 11628]
    
    Binning_5D_OG = ['Bin_5D_OG', -1.5, 13525.5, 13528]
    Binning_5D_OG_Smeared = ['Bin_5D_OG_smeared', -1.5, 13525.5, 13528]
    
    
    
    # List_of_Quantities_1D = [Q2_Binning, y_Binning, xB_Binning, z_Binning, pT_Binning, phi_t_Binning]
    # List_of_Quantities_1D_smeared = [Q2_Binning_Smeared, y_Binning_Smeared, xB_Binning_Smeared, z_Binning_Smeared, pT_Binning_Smeared, phi_t_Binning_Smeared]
    
    List_of_Quantities_1D = [Q2_Binning, y_Binning, xB_Binning, z_Binning, pT_Binning, phi_t_Binning, Binning_4D, Binning_4D_OG]
    List_of_Quantities_1D_smeared = [Q2_Binning_Smeared, y_Binning_Smeared, xB_Binning_Smeared, z_Binning_Smeared, pT_Binning_Smeared, phi_t_Binning_Smeared, Binning_4D_Smeared, Binning_4D_OG_Smeared]
    
    
    List_of_Quantities_1D = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, MM_Binning, ['el', 0, 10, 200], ['pip', 0, 8, 200], phi_t_Binning, Binning_4D, W_Binning]
    List_of_Quantities_1D_smeared = [Q2_Binning_Smeared, xB_Binning_Smeared, z_Binning_Smeared, pT_Binning_Smeared, y_Binning_Smeared, MM_Binning_Smeared, ['el_smeared', 0, 10, 200], ['pip_smeared', 0, 8, 200], phi_t_Binning_Smeared, Binning_4D_Smeared, W_Binning_Smeared]
    
    
#     List_of_Quantities_1D = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, ['el', 0, 10, 200], ['pip', 0, 8, 200]]
#     List_of_Quantities_1D_smeared = [Q2_Binning_Smeared, xB_Binning_Smeared, z_Binning_Smeared, pT_Binning_Smeared, y_Binning_Smeared, ['el_smeared', 0, 10, 200], ['pip_smeared', 0, 8, 200]]
    
    
    
    
    
    # List_of_Quantities_2D = [[Q2_Binning, xB_Binning], [y_Binning, xB_Binning], [z_Binning, pT_Binning]]
    # List_of_Quantities_2D_smeared = [[Q2_Binning_Smeared, xB_Binning_Smeared], [y_Binning_Smeared, xB_Binning_Smeared], [z_Binning_Smeared, pT_Binning_Smeared]]
    
    # List_of_Quantities_2D = [[['Q2', 0, 12, 200], ['xB', 0, 0.8, 200]], [['y', 0, 1, 200], ['xB', 0, 0.8, 200]], [['z', 0, 1, 200], ['pT', 0, 1.6, 200]], [['el', 0, 8, 200], ['elth', 0, 40, 200]], [['elth', 0, 40, 200], ['elPhi', 0, 360, 200]], [['pip', 0, 6, 200], ['pipth', 0, 40, 200]], [['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]], [MM_Binning, ['el', 0, 8, 200]], [MM_Binning, ['pip', 0, 6, 200]]]
    # List_of_Quantities_2D_smeared = [[['Q2_smeared', 0, 12, 200], ['xB_smeared', 0, 0.8, 200]], [['y_smeared', 0, 1, 200], ['xB_smeared', 0, 0.8, 200]], [['z_smeared', 0, 1, 200], ['pT_smeared', 0, 1.6, 200]], [['el_smeared', 0, 8, 200], ['elth_smeared', 0, 40, 200]], [['elth_smeared', 0, 40, 200], ['elPhi_smeared', 0, 360, 200]], [['pip_smeared', 0, 6, 200], ['pipth_smeared', 0, 40, 200]], [['pipth_smeared', 0, 40, 200], ['pipPhi_smeared', 0, 360, 200]], [MM_Binning_Smeared, ['el_smeared', 0, 8, 200]], [MM_Binning_Smeared, ['pip_smeared', 0, 6, 200]]]
    
    List_of_Quantities_2D = [[['Q2', 0, 12, 200], ['xB', 0, 0.8, 200]], [['y', 0, 1, 200], ['xB', 0, 0.8, 200]], [['z', 0, 1, 200], ['pT', 0, 1.6, 200]], [['el', 0, 8, 200], ['elth', 0, 40, 200]], [['elth', 0, 40, 200], ['elPhi', 0, 360, 200]], [['pip', 0, 6, 200], ['pipth', 0, 40, 200]], [['pipth', 0, 40, 200], ['pipPhi', 0, 360, 200]]]
    List_of_Quantities_2D_smeared = [[['Q2_smeared', 0, 12, 200], ['xB_smeared', 0, 0.8, 200]], [['y_smeared', 0, 1, 200], ['xB_smeared', 0, 0.8, 200]], [['z_smeared', 0, 1, 200], ['pT_smeared', 0, 1.6, 200]], [['el_smeared', 0, 8, 200], ['elth_smeared', 0, 40, 200]], [['elth_smeared', 0, 40, 200], ['elPhi_smeared', 0, 360, 200]], [['pip_smeared', 0, 6, 200], ['pipth_smeared', 0, 40, 200]], [['pipth_smeared', 0, 40, 200], ['pipPhi_smeared', 0, 360, 200]]]
    
    
        # # # 2D histograms are turned off with these options
    # List_of_Quantities_2D = []
    # List_of_Quantities_2D_smeared = []
    
    
    
    
    if(len(List_of_Quantities_2D) == 0):
        print("Not running 2D histograms...")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    run_Mom_Cor_Code = "yes"
    # run_Mom_Cor_Code = "no"

    if(run_Mom_Cor_Code == "yes"):
        print("\nRunning Histograms from Momentum Correction Code (i.e., Missing Mass and ∆P Histograms)\n")
    
    
    
    
    # smearing_options_list = ["", "smear", "2", "smear_2"]
    smearing_options_list = ["2", "smear_2"]
    
    # The '2' in the smearing option uses the binning schemes developed for this analysis (instead of the binning used by Stephan)
    
    if("rdf" in datatype or "gdf" in datatype):
        # Do not smear data or generated MC
        for ii in smearing_options_list:
            if("smear" in ii):
                smearing_options_list.remove(ii)
    
    
    
    
    
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
    
    
    
    
    
    
    
    
    
    
    if(output_type == "histo" or output_type == "time"):
        Mom_Cor_Histos, Kinetic_Histo_3D, histo_for_counts, histo_for_2D_Purity, histo_for_migration = {}, {}, {}, {}, {}
        count_of_histograms = 0

        print("Making Histograms...")
        ######################################################################
        ##=====##=====##=====##    Top of Main Loop    ##=====##=====##=====##
        ######################################################################

        ##=====##  Datatype Loop  ##=====##

        if(datatype == "pdf"):
            # datatype_list = ["mdf", "pdf", "gen", "udf", "miss_idf", "miss_idf_el", "miss_idf_pip"]
            # datatype_list = ["mdf", "pdf", "gen", "udf", "miss_idf"]
            datatype_list = ["mdf", "pdf", "gen"]
        else:
            datatype_list = [datatype]

        for datatype_2 in datatype_list:

            ##=====##    Smearing Loop    ##=====##
            

            for smearing_Q in smearing_options_list:

                Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "Q2_xB_Bin", "z_pT_Bin"

                if("2" in smearing_Q):
                    Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_2"]), "".join([z_pT_Bin_Filter_str, "_2"])

                if("smear" in smearing_Q and (datatype_2 == "mdf" or datatype_2 == "pdf" or datatype_2 == "udf" or ("miss_idf" in datatype_2))):
                    Variable_Loop, Variable_Loop_2D = List_of_Quantities_1D_smeared, List_of_Quantities_2D_smeared
                    Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_smeared"]), "".join([z_pT_Bin_Filter_str, "_smeared"])

                elif("smear" in smearing_Q and (datatype_2 != "mdf" and datatype_2 != "pdf" and datatype_2 != "udf" and ("miss_idf" not in datatype_2))):
                    # Do not smear anything except for the MC REC Data
                    continue

                else:
                    Variable_Loop, Variable_Loop_2D = List_of_Quantities_1D, List_of_Quantities_2D
                    if(datatype_2 == "gen"):
                        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = "".join([Q2_xB_Bin_Filter_str, "_gen"]), "".join([z_pT_Bin_Filter_str, "_gen"])
                        Variable_Loop = copy.deepcopy(List_of_Quantities_1D)
                        for list1 in Variable_Loop:
                            list1[0] = "".join([list1[0], "_gen"])

                ##=====##    Cut Loop     ##=====##

                for cut_choice in cut_list:

                    ##=====##    Sector Type Loop    ##=====##

                    for sec_type in Types_Of_Sectors:
                        if(sec_type == ''):
                            Sector_Numbers_List = [-1]
                        else:
                            Sector_Numbers_List = Sector_Numbers

                        ##=====##    Sector Number Loop    ##=====##

                        for sec_num in Sector_Numbers_List:
                            if(sec_num == -1 and sec_type != '' and '' in Types_Of_Sectors):
                                continue

                            ##=====##    Histogram Option Loop/Selection    ##=====##

                            if(datatype_2 == 'pdf'):
                                # histo_options = ["has_matched", "bin_purity", "delta_matched"]
                                # histo_options = ["has_matched", "bin_purity", "bin_migration_V3"]
                                # histo_options = ["delta_matched", "bin_migration_V3", "response_matrix"]
                                # histo_options = ["delta_matched", "response_matrix"]
                                histo_options = ["response_matrix"]
                                # Meaning of the above options:
                                    # # 'has_matched' --> runs 'pdf' normally (filters unmatched events but otherwise is the same as histo_option = "normal")
                                    # # 'bin_purity' --> filters events in which the reconstructed bin is different from the generated bin
                                    # # 'delta_matched' --> makes histograms which plot the difference between the reconstructed and generated (∆val) versus the reconstructed value
                                    # # 'bin_migration' --> shows where events are migrating from
                                    # # 'bin_migration_V3' --> similar to 'bin_migration' option but makes a single 2D plot to show the GEN Bin vs the REC Bin with extra information regarding bins outside the defined range AND regarding the unmatched events
                                    # # 'response_matrix' --> meant to replace the 'bin_migration' options for easier use in the unfolding procedures (uses the same binning schemes as given for the 1D histograms)
                            elif('miss_idf' in datatype_2):
                                histo_options = ["normal", "bin_purity", "delta_matched"]
                            elif(datatype_2 == 'rdf' or datatype_2 == 'gdf' or datatype_2 == "mdf"):
                                # histo_options = ["response_matrix"]
                                # histo_options = ["normal", "response_matrix"]
                                # histo_options = ["normal_1D", "response_matrix"]
                                histo_options = ["normal_2D", "response_matrix"]
                                # # Only runs normal 2D histograms and the response matrices
                            elif(datatype_2 == "gen"):
                                histo_options = []
                            else:
                                histo_options = ["normal"]
                                # runs code normally (i.e., normal 1D and 2D histograms)
                                
                                
                            if(run_Mom_Cor_Code == "yes" and datatype_2 != 'pdf'):
                                histo_options.append("Mom_Cor_Code")
                                
                                

                            for option in histo_options:
                                
                                if(option == "Mom_Cor_Code"):
                                    
                                    if("EDIS" not in cut_choice and "SIDIS" not in cut_choice):
                                        # Only run these histograms for exclusive event selections (allowing full SIDIS cuts for comparison only)
                                        continue
                                    
                                    cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, "MM", smearing_Q, datatype_2, cut_choice, "Cut")
                                    
                                    if(cutname == "continue"):
                                        continue
                                        
                                    ###############################################################
                                    ##==========##     Correction Histogram ID's     ##==========##
                                    ###############################################################
                                    
                                    Mom_Cor_Histos_Name_MM_Ele = (''.join(["(Mom_Cor_Histos - Missing Mass El - ", str(cut_choice), ", '", datatype_2, "', ", "MM" if("smear" not in smearing_Q) else "MM_smeared", ", '", smearing_Q, "')"]))
                                    Mom_Cor_Histos_Name_MM_Pip = (''.join(["(Mom_Cor_Histos - Missing Mass Pi+ - ", str(cut_choice), ", '", datatype_2, "', ", "MM" if("smear" not in smearing_Q) else "MM_smeared", ", '", smearing_Q, "')"]))
                                    
                                    Mom_Cor_Histos_Name_DP_Ele = (''.join(["(Mom_Cor_Histos - Delta P El - ", str(cut_choice), ", '", datatype_2, "', ", "Delta_Pel_Cors" if("smear" not in smearing_Q) else "Delta_Pel_Cors_smeared", ", '", smearing_Q, "')"]))
                                    Mom_Cor_Histos_Name_DP_Pip = (''.join(["(Mom_Cor_Histos - Delta P Pi+ -" , str(cut_choice), ", '", datatype_2, "', ", "Delta_Ppip_Cors" if("smear" not in smearing_Q) else "Delta_Ppip_Cors_smeared", ", '", smearing_Q, "')"]))
                                    
                                    Mom_Cor_Histos_Name_DP_Ele_Theta = (''.join(["(Mom_Cor_Histos - Delta P El v Theta - ", str(cut_choice), ", '", datatype_2, "', ", "Delta_Pel_Cors" if("smear" not in smearing_Q) else "Delta_Pel_Cors_smeared", ", '", smearing_Q, "')"]))
                                    Mom_Cor_Histos_Name_DP_Pip_Theta = (''.join(["(Mom_Cor_Histos - Delta P Pi+ v Theta - ", str(cut_choice), ", '", datatype_2, "', ", "Delta_Ppip_Cors" if("smear" not in smearing_Q) else "Delta_Ppip_Cors_smeared", ", '", smearing_Q, "')"]))
                                    
                                    Mom_Cor_Histos_Name_DTheta_Ele = (''.join(["(Mom_Cor_Histos - Delta Theta El - ", str(cut_choice), ", '", datatype_2, "', ", "Delta_Theta_el_Cors" if("smear" not in smearing_Q) else "Delta_Theta_el_Cors_smeared", ", '", smearing_Q, "')"]))
                                    Mom_Cor_Histos_Name_DTheta_Pip = (''.join(["(Mom_Cor_Histos - Delta Theta Pi+ - ", str(cut_choice), ", '", datatype_2, "', ", "Delta_Theta_pip_Cors" if("smear" not in smearing_Q) else "Delta_Theta_pip_Cors_smeared", ", '", smearing_Q, "')"]))
                                    
                                    Mom_Cor_Histos_Name_DTheta_Ele_Theta = (''.join(["(Mom_Cor_Histos - Delta Theta El v Theta - ", str(cut_choice), ", '", datatype_2, "', ", "Delta_Theta_el_Cors" if("smear" not in smearing_Q) else "Delta_Theta_el_Cors_smeared", ", '", smearing_Q, "')"]))
                                    Mom_Cor_Histos_Name_DTheta_Pip_Theta = (''.join(["(Mom_Cor_Histos - Delta Theta Pi+ v Theta - ", str(cut_choice), ", '", datatype_2, "', ", "Delta_Theta_pip_Cors" if("smear" not in smearing_Q) else "Delta_Theta_pip_Cors_smeared", ", '", smearing_Q, "')"]))
                                    
                                    Mom_Cor_Histos_Name_Angle_Ele = (''.join(["(Mom_Cor_Histos - Theta v Phi El - ", str(cut_choice), ", '", datatype_2, "', ", "elPhi" if("smear" not in smearing_Q) else "elPhi_smeared", ", '", smearing_Q, "')"]))
                                    Mom_Cor_Histos_Name_Angle_Pip = (''.join(["(Mom_Cor_Histos - Theta v Phi Pi+ - ", str(cut_choice), ", '", datatype_2, "', ", "pipPhi" if("smear" not in smearing_Q) else "pipPhi_smeared", ", '", smearing_Q, "')"]))
                                    
                                    ###############################################################
                                    ##==========##  Correction Histogram ID's (End)  ##==========##
                                    ###############################################################
                                    
                                    
                                    
                                    variables_Mom_Cor = ["MM", "Delta_Pel_Cors", "Delta_Ppip_Cors", "Delta_Theta_el_Cors", "Delta_Theta_pip_Cors", "el", "pip", "elth", "pipth", "elPhi", "pipPhi"]
                                    if("smear" in smearing_Q):
                                        variables_Mom_Cor = ["MM_smeared", "Delta_Pel_Cors_smeared", "Delta_Ppip_Cors_smeared", "Delta_Theta_el_Cors_smeared", "Delta_Theta_pip_Cors_smeared", "el_smeared", "pip_smeared", "elth_smeared", "pipth_smeared", "elPhi_smeared", "pipPhi_smeared"]
                                    
                                    MCH_rdf = DF_Filter_Function_Full(rdf, "", -1, -1, -2, variables_Mom_Cor, smearing_Q, datatype_2, cut_choice, "DF")
                                    
                                    
                                    
                                    #############################################################
                                    ##==========##     Correction Histo Titles     ##==========##
                                    #############################################################
                                    
                                    Mom_Cor_Histos_Name_MM_Ele_Title = "".join(["(Smeared) " if("smear" in smearing_Q) else "", "Missing Mass Histogram (Electron Kinematics/Sectors", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in smearing_Q) else " ", "p_{el};", "(Smeared) " if("smear" in smearing_Q) else " ", "MM_{e#pi+(X)}; El Sector"])
                                    Mom_Cor_Histos_Name_MM_Pip_Title = "".join(["(Smeared) " if("smear" in smearing_Q) else "", "Missing Mass Histogram (#pi^{+} Pion Kinematics/Sectors", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in smearing_Q) else " ", "p_{#pi+};", "(Smeared) " if("smear" in smearing_Q) else " ", "MM_{e#pi+(X)}; #pi^{+} Sector"])
                                    
                                    Mom_Cor_Histos_Name_Delta_Ele_Title = "".join(["(Smeared) " if("smear" in smearing_Q) else "", "#DeltaP Histogram (Electron Kinematics/Sectors", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in smearing_Q) else " ", "p_{el};", "(Smeared) " if("smear" in smearing_Q) else " ", "#DeltaP_{el}; El Sector"])
                                    Mom_Cor_Histos_Name_Delta_Pip_Title = "".join(["(Smeared) " if("smear" in smearing_Q) else "", "#DeltaP Histogram (#pi^{+} Pion Kinematics/Sectors", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in smearing_Q) else " ", "p_{#pi+};", "(Smeared) " if("smear" in smearing_Q) else " ", "#DeltaP_{#pi+}; #pi^{+} Sector"])
                                    
                                    Mom_Cor_Histos_Name_Delta_Ele_Theta_Title = "".join(["(Smeared) " if("smear" in smearing_Q) else "", "#DeltaP Histogram vs #theta (Electron Kinematics/Sectors", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in smearing_Q) else " ", "#theta_{el};", "(Smeared) " if("smear" in smearing_Q) else " ", "#DeltaP_{el}; El Sector"])
                                    Mom_Cor_Histos_Name_Delta_Pip_Theta_Title = "".join(["(Smeared) " if("smear" in smearing_Q) else "", "#DeltaP Histogram vs #theta (#pi^{+} Pion Kinematics/Sectors", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in smearing_Q) else " ", "#theta_{#pi+};", "(Smeared) " if("smear" in smearing_Q) else " ", "#DeltaP_{#pi+}; #pi^{+} Sector"])
                                    
                                    Mom_Cor_Histos_Name_Angle_Ele_Title = "".join(["(Smeared) " if("smear" in smearing_Q) else "", "#theta vs #phi Histogram (Electron Kinematics/Sectors", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in smearing_Q) else " ", "#theta_{el};", "(Smeared) " if("smear" in smearing_Q) else " ", "#phi_{el}; El Sector"])
                                    Mom_Cor_Histos_Name_Angle_Pip_Title = "".join(["(Smeared) " if("smear" in smearing_Q) else "", "#theta vs #phi Histogram (#pi^{+} Pion Kinematics/Sectors", " - Corrected" if(Mom_Correction_Q == "yes") else "", ");", "(Smeared) " if("smear" in smearing_Q) else " ", "#theta_{#pi+};", "(Smeared) " if("smear" in smearing_Q) else " ", "#phi_{#pi+}; #pi^{+} Sector"])
                                    
                                    #############################################################
                                    ##==========##  Correction Histo Titles (End)  ##==========##
                                    #############################################################
                                    

                                    ###################################################################################
                                    ##          ##          ##                               ##          ##          ##
                                    ##==========##==========##     Correction Histograms     ##==========##==========##
                                    ##          ##          ##                               ##          ##          ##
                                    ###################################################################################
                                    
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_MM_Ele] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_MM_Ele, str(Mom_Cor_Histos_Name_MM_Ele_Title), 200, 0, 10, 500, 0, 3.5, 9, -1, 7), "el" if("smear" not in smearing_Q) else "el_smeared", "MM" if("smear" not in smearing_Q) else "MM_smeared", "esec")
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_MM_Pip] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_MM_Pip, str(Mom_Cor_Histos_Name_MM_Pip_Title), 200, 0, 8, 500, 0, 3.5, 9, -1, 7), "pip" if("smear" not in smearing_Q) else "pip_smeared", "MM" if("smear" not in smearing_Q) else "MM_smeared", "pipsec")
                                    
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_DP_Ele] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_DP_Ele, str(Mom_Cor_Histos_Name_Delta_Ele_Title), 200, 0, 10, 500, -3, 3, 9, -1, 7), "el" if("smear" not in smearing_Q) else "el_smeared", "Delta_Pel_Cors" if("smear" not in smearing_Q) else "Delta_Pel_Cors_smeared", "esec")
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_DP_Pip] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_DP_Pip, str(Mom_Cor_Histos_Name_Delta_Pip_Title), 200, 0, 8, 500, -3, 3, 9, -1, 7), "pip" if("smear" not in smearing_Q) else "pip_smeared", "Delta_Ppip_Cors" if("smear" not in smearing_Q) else "Delta_Ppip_Cors_smeared", "pipsec")
                                    
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_DP_Ele_Theta] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_DP_Ele_Theta, str(Mom_Cor_Histos_Name_Delta_Ele_Theta_Title), 200, 0, 40, 500, -3, 3, 9, -1, 7), "elth" if("smear" not in smearing_Q) else "elth_smeared", "Delta_Pel_Cors" if("smear" not in smearing_Q) else "Delta_Pel_Cors_smeared", "esec")
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_DP_Pip_Theta] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_DP_Pip_Theta, str(Mom_Cor_Histos_Name_Delta_Pip_Theta_Title), 200, 0, 40, 500, -3, 3, 9, -1, 7), "pipth" if("smear" not in smearing_Q) else "pipth_smeared", "Delta_Ppip_Cors" if("smear" not in smearing_Q) else "Delta_Ppip_Cors_smeared", "pipsec")
                                    
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_DTheta_Ele] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_DTheta_Ele, str(Mom_Cor_Histos_Name_Delta_Ele_Title).replace("#DeltaP", "#Delta#theta"), 200, 0, 10, 500, -3, 3, 9, -1, 7), "el" if("smear" not in smearing_Q) else "el_smeared", "Delta_Theta_el_Cors" if("smear" not in smearing_Q) else "Delta_Theta_el_Cors_smeared", "esec")
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_DTheta_Pip] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_DTheta_Pip, str(Mom_Cor_Histos_Name_Delta_Pip_Title).replace("#DeltaP", "#Delta#theta"), 200, 0, 8, 500, -3, 3, 9, -1, 7), "pip" if("smear" not in smearing_Q) else "pip_smeared", "Delta_Theta_pip_Cors" if("smear" not in smearing_Q) else "Delta_Theta_pip_Cors_smeared", "pipsec")
                                    
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_DTheta_Ele_Theta] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_DTheta_Ele_Theta, str(Mom_Cor_Histos_Name_Delta_Ele_Theta_Title).replace("#DeltaP", "#Delta#theta"), 200, 0, 40, 500, -3, 3, 9, -1, 7), "elth" if("smear" not in smearing_Q) else "elth_smeared", "Delta_Theta_el_Cors" if("smear" not in smearing_Q) else "Delta_Theta_el_Cors_smeared", "esec")
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_DTheta_Pip_Theta] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_DTheta_Pip_Theta, str(Mom_Cor_Histos_Name_Delta_Pip_Theta_Title).replace("#DeltaP", "#Delta#theta"), 200, 0, 40, 500, -3, 3, 9, -1, 7), "pipth" if("smear" not in smearing_Q) else "pipth_smeared", "Delta_Theta_pip_Cors" if("smear" not in smearing_Q) else "Delta_Theta_pip_Cors_smeared", "pipsec")
                                    
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_Angle_Ele] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_Angle_Ele, str(Mom_Cor_Histos_Name_Angle_Ele_Title), 200, 0, 40, 360, 0, 360, 9, -1, 7), "elth" if("smear" not in smearing_Q) else "elth_smeared", "elPhi" if("smear" not in smearing_Q) else "elPhi_smeared", "esec")
                                    Mom_Cor_Histos[Mom_Cor_Histos_Name_Angle_Pip] = MCH_rdf.Histo3D((Mom_Cor_Histos_Name_Angle_Pip, str(Mom_Cor_Histos_Name_Angle_Pip_Title), 200, 0, 40, 360, 0, 360, 9, -1, 7), "pipth" if("smear" not in smearing_Q) else "pipth_smeared", "pipPhi" if("smear" not in smearing_Q) else "pipPhi_smeared", "pipsec")
                                    
                                    ###################################################################################
                                    ##          ##          ##                               ##          ##          ##
                                    ##==========##==========##  Correction Histograms (End)  ##==========##==========##
                                    ##          ##          ##                               ##          ##          ##
                                    ###################################################################################
                                    
                                    
                                    if(str(file_location) != 'time'):
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_MM_Ele].Write()
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_MM_Pip].Write()
                                        
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_DP_Ele].Write()
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_DP_Pip].Write()
                                        
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_DP_Ele_Theta].Write()
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_DP_Pip_Theta].Write()
                                        
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_DTheta_Ele].Write()
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_DTheta_Pip].Write()
                                        
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_DTheta_Ele_Theta].Write()
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_DTheta_Pip_Theta].Write()
                                        
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_Angle_Ele].Write()
                                        Mom_Cor_Histos[Mom_Cor_Histos_Name_Angle_Pip].Write()
                                        
                                        
                                    Print_Progress(count_of_histograms, 12, 200 if(str(file_location) != 'time') else 50)
                                    count_of_histograms += 12
                                    
                                    

                                if("normal" in option or option == "has_matched" or option == "bin_purity" or option == "delta_matched"):
                                    
                                    ###################################################################################################################################################################
                                    ###################################################################################################################################################################
                                    ###################################################################     STANDARD HISTOGRAMS     ###################################################################
                                    ###################################################################################################################################################################
                                    
                                    ###################################################################################################################################################################
                                    ##########==========##########==========##########==========##########                       ##########==========##########==========##########==========##########
                                    ##########==========##########==========##########==========##########     1D Histograms     ##########==========##########==========##########==========##########
                                    ##########==========##########==========##########==========##########                       ##########==========##########==========##########==========##########
                                    ###################################################################################################################################################################
                                    if(option != "normal_2D"):
                                        ##===================================##
                                        ##=====##    Variable Loop    ##=====##
                                        ##===================================##
                                        for list1 in Variable_Loop:
                                            cutname, Histo_Title = "continue", "continue"
                                            if(option == "normal_1D" or option == "normal" or option == "has_matched"):
                                                cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Cut")
                                                Histo_Title = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Title")

                                                Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))
                                                if("2" in smearing_Q):
                                                    Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - New 2D Binning - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))
                                                if("2" not in smearing_Q and "Bin_4D" in str(list1[0]) and "OG" not in str(list1[0])):
                                                    continue # These 4D bins have only been defined with my new binning schemes
                                                if("2" in smearing_Q and "Bin_4D" in str(list1[0]) and "OG" in str(list1[0])):
                                                    continue # These 4D bins were defined with the original binning scheme

                                            if(option == "bin_purity"):
                                                cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Cut")
                                                Histo_Title = (DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Title")).replace("Matched", "Purity Match")

                                                Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - Purity - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))
                                                if("2" in smearing_Q):
                                                    Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - New 2D Binning - Purity - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))

                                            if(option == "delta_matched"):
                                                final_df = Delta_Matched_DF(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF"), list1[0]) # Calculates the different between the matched reconstructed and generated events (rec - gen)
                                                if(final_df == "continue"):
                                                    continue
                                                cutname = DF_Filter_Function_Full(final_df, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Cut")
                                                Histo_Title = "".join([((DF_Filter_Function_Full(final_df, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Title")).replace("Matched", "Difference Between Match").replace("; Q^{2}-x_{B} Bin (Smeared); z-P_{T} Bin (Smeared)", "").replace("; Q^{2}-x_{B} Bin; z-P_{T} Bin", "")), "; #Delta(REC - GEN); ", "#pi^{+} Pion" if("pip" in list1[0]) else "Electron", " Sector"])

                                                Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - Dif Match - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))
                                                if("2" in smearing_Q):
                                                    Kinetic_Histo_3D_Name = (''.join(['3D -> 1D Histogram - New 2D Binning - Dif Match - ', str(cutname)]), datatype_2, sec_type, sec_num, str(list1[0]))

                                            if(cutname == "continue" or Histo_Title == "continue"):
                                                continue


                                            if(option != "delta_matched" and option != "bin_purity"):
                                                Kinetic_Histo_3D[Kinetic_Histo_3D_Name] = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF").Histo3D((str(Kinetic_Histo_3D_Name), str(Histo_Title), 14, -3, 10, 54, -3, 50, list1[3], list1[1], list1[2]), str(Q2_xB_Bin_Filter_str), str(z_pT_Bin_Filter_str), str(list1[0]))
                                            elif(option == "bin_purity"):
                                                Kinetic_Histo_3D[Kinetic_Histo_3D_Name] = bin_purity_filter_fuction(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF"), list1[0], list1[1], list1[2], list1[3]).Histo3D((str(Kinetic_Histo_3D_Name), str(Histo_Title), 14, -3, 10, 54, -3, 50, list1[3], list1[1], list1[2]), str(Q2_xB_Bin_Filter_str), str(z_pT_Bin_Filter_str), str(list1[0]))
                                            elif(option == "delta_matched"):
                                                if("el" not in list1[0] and "pip" not in list1[0]):
                                                    continue # Don't need these extra ∆(REC-GEN) histograms (angles/momentum are the only criteria being considered)
                                                delta_bins = Delta_Matched_Bin_Calc(list1[0], list1[1], list1[2])
                                                if("continue" in delta_bins):
                                                    continue
                                                Kinetic_Histo_3D[Kinetic_Histo_3D_Name] = final_df.Histo3D((str(Kinetic_Histo_3D_Name), str(Histo_Title), list1[3], list1[1], list1[2], delta_bins[0], delta_bins[1], delta_bins[2], 9, -1, 7), str(list1[0]), "Delta_Matched_Value", "pipsec" if("pip" in list1[0]) else "esec")
                                                if("Phi" in list1[0]):
                                                    Kinetic_Histo_3D["".join([str(Kinetic_Histo_3D_Name), "_Extra_3D"])] = DF_Filter_Function_Full(final_df, sec_type, sec_num, -1, -2, str(list1[0].replace("Phi", "th")), smearing_Q, datatype_2, cut_choice, "DF").Histo3D(("".join([str(Kinetic_Histo_3D_Name), "_Extra_3D"]), "".join([Histo_Title.replace("".join(["; ", "#pi^{+} Pion" if("pip" in list1[0]) else "Electron", " Sector"]), ""), ";#theta_{", "el" if "el" in list1[0] else "#pi+" ,"}"]), list1[3], list1[1], list1[2], delta_bins[0], delta_bins[1], delta_bins[2], 34, 0, 40), str(list1[0]), "Delta_Matched_Value", str(list1[0].replace("Phi", "th")))

                                            if(str(file_location) != 'time'):
                                                Kinetic_Histo_3D[Kinetic_Histo_3D_Name].Write()

                                                if("Phi" in list1[0] and option == "delta_matched"):
                                                    Kinetic_Histo_3D["".join([str(Kinetic_Histo_3D_Name), "_Extra_3D"])].Write()

                                            # 3D->1D Histogram is saved
                                            Print_Progress(count_of_histograms, 2 if("Phi" in list1[0] and option == "delta_matched") else 1, 200 if(str(file_location) != 'time') else 50)
                                            count_of_histograms += 1
                                            if("Phi" in list1[0] and option == "delta_matched"):
                                                count_of_histograms += 1

                                    ###################################################################################################################################################################
                                    ##########==========##########==========##########==========##########                       ##########==========##########==========##########==========##########
                                    ##########==========##########==========##########==========##########     1D Histograms     ##########==========##########==========##########==========##########
                                    ##########==========##########==========##########==========##########                       ##########==========##########==========##########==========##########
                                    ###################################################################################################################################################################
                                    ##########==========##########==========##########==========##########                       ##########==========##########==========##########==========##########
                                    ##########==========##########==========##########==========##########     2D Histograms     ##########==========##########==========##########==========##########
                                    ##########==========##########==========##########==========##########                       ##########==========##########==========##########==========##########
                                    ###################################################################################################################################################################
                                    
                                    if((option == "normal_2D" or option == "normal" or option == "has_matched") and datatype_2 != "gen"):
                                        ##===================================##
                                        ##=====##    Variable Loop    ##=====##
                                        ##===================================##
                                        for list2 in Variable_Loop_2D:
                                            for Q2_xB_Bin_Num in List_of_Q2_xB_Bins_to_include:
                                                if(Q2_xB_Bin_Num > 8 and "2" in smearing_Q):
                                                    continue
                                                    # 2nd definition of the Q2-xB bins do not go above bin 8

                                                # cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, [list2[0][0], list2[1][0]], smearing_Q, datatype_2, cut_choice, "Cut")
                                                Histo_Title = DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, [list2[0][0], list2[1][0]], smearing_Q, datatype_2, cut_choice, "Title")                                            

                                                # if(cutname == "continue" or Histo_Title == "continue"):
                                                if(Histo_Title == "continue" or DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, [list2[0][0], list2[1][0]], smearing_Q, datatype_2, cut_choice, "Cut") == "continue"):
                                                    continue
                                                    
                                                # Kinetic_Histo_3D_Name = (''.join(['3D -> 2D Histogram - ', str(cutname)]), datatype_2, sec_type, sec_num, Q2_xB_Bin_Num, str(list2[0][0]), str(list2[1][0]))
                                                # if("2" in smearing_Q):
                                                #     Kinetic_Histo_3D_Name = (''.join(['3D -> 2D Histogram - New 2D Binning - ', str(cutname)]), datatype_2, sec_type, sec_num, Q2_xB_Bin_Num, str(list2[0][0]), str(list2[1][0]))
                                                
                                                Kinetic_Histo_2D_Name = "".join(["(2D Histogram - '", "', '".join([str(cut_choice), str(smearing_Q), str(datatype_2), str(sec_type), str(sec_num), str(Q2_xB_Bin_Num), str(list2[0][0]), str(list2[1][0])]), "')"])
                                                
                                                Kinetic_Histo_3D[Kinetic_Histo_2D_Name] = DF_Filter_Function_Full(rdf, sec_type, sec_num, Q2_xB_Bin_Num, -2, [list2[0][0], list2[1][0]], smearing_Q, datatype_2, cut_choice, "DF").Histo3D((str(Kinetic_Histo_2D_Name), str(Histo_Title), 54, -3, 50, list2[0][3], list2[0][1], list2[0][2], list2[1][3], list2[1][1], list2[1][2]), str(z_pT_Bin_Filter_str), str(list2[0][0]), str(list2[1][0]))

                                                if(str(file_location) != 'time'):
                                                    Kinetic_Histo_3D[Kinetic_Histo_2D_Name].Write()
                                                
                                                # 3D->2D Histogram is saved
                                                Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                                count_of_histograms += 1

                                    ###################################################################################################################################################################
                                    ##########==========##########==========##########==========##########                       ##########==========##########==========##########==========##########
                                    ##########==========##########==========##########==========##########     2D Histograms     ##########==========##########==========##########==========##########
                                    ##########==========##########==========##########==========##########                       ##########==========##########==========##########==========##########
                                    ###################################################################################################################################################################
                                    ###################################################################################################################################################################
                                    #################################################################     END OF 1D/2D HISTOGRAMS     #################################################################
                                    ###################################################################################################################################################################
                                    
                            
                                elif(option == "bin_migration"):
                                    
                                    for list1 in Variable_Loop:
                                        # bin_purity_save_fuction
                                    
                                        cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "Cut")
                                        
                                        if("continue" in cutname):
                                            continue
                                            
                                        sdf = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, list1[0], smearing_Q, datatype_2, cut_choice, "DF")
  
                                        BIN_SIZE = (list1[2] - list1[1])/list1[3]
                                            
                                        for REC_Bin in range(0, list1[3] + 1, 1):
                                            
                                            Bin_Range = "".join([str(round(BIN_SIZE*(REC_Bin - 1), 3)), " -> ", str(round(BIN_SIZE*REC_Bin, 3))])
                                            
                                            Migration_Title = "".join(["#splitline{#splitline{Bin Migration of ", variable_Title_name(list1[0]), "}{Cut: ", str(cutname), "}}{#scale[1.5]{REC BIN: ", str(REC_Bin), " - Range: ", Bin_Range, "}}; ", variable_Title_name(list1[0]), " GEN Bin; Counts"])
                                            
                                            Migration_Histo_REF = ("Bin Migration", list1[0], "".join(["REC_Bin_", str(REC_Bin)]), smearing_Q, cut_choice, sec_type, sec_num)
                                    
                                            histo_for_migration[Migration_Histo_REF] = bin_purity_save_filter_fuction(sdf, str(list1[0]), list1[1], list1[2], list1[3], REC_Bin).Histo1D((str(Migration_Histo_REF), str(Migration_Title), list1[3] + 3, -1, list1[3] + 1), "".join([str(list1[0]), "_GEN_BIN"]))
                                        
                                            if(str(file_location) != 'time'):
                                                histo_for_migration[Migration_Histo_REF].Write()
                                                
                                            Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                            count_of_histograms += 1
                                        
                                    
                                elif(option == "bin_migration_V3"):
                                    
                                    for Var_List in Variable_Loop:
                                        
                                        variable = Var_List[0]

                                        cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, "mdf", cut_choice, "Cut")
                                        
                                        if("continue" in cutname):
                                            continue

                                        
                                        sdf = bin_purity_save_fuction_New(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, "mdf", cut_choice, "DF"), variable, Var_List[1], Var_List[2], Var_List[3], datatype_2)
                                        
                                        
                                        if("Bin_4D" not in variable):
                                            BIN_SIZE = round((Var_List[2] - Var_List[1])/Var_List[3], 5)
                                            Bin_Range = "".join([str(round((Var_List[1]), 3)), " -> ", str(round(Var_List[2], 3))])

                                            Migration_Title = "".join(["#splitline{#splitline{#splitline{Bin Migration of ", variable_Title_name(variable), "}{Cut: ", str(cutname), "}}{#scale[1.5]{Number of Bins: ", str(Var_List[3]), " - Range: ", str(Bin_Range), ", - Size: ", str(BIN_SIZE), " per bin}}}{Same Binning Scheme as Other (Standard) Histograms}; ", variable_Title_name(variable), " (GEN) Bins; ", variable_Title_name(variable), " (REC) Bins"])

                                            Migration_Histo_REF = ("Bin Migration V3", variable, smearing_Q, cut_choice, sec_type, sec_num)

                                            # num_of_REC_bins, min_REC_bin, Max_REC_bin = Var_List[3], 0, Var_List[3]
                                            # num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Var_List[3] + 3), -1, (Var_List[3] + 2)

                                            num_of_REC_bins, min_REC_bin, Max_REC_bin = (Var_List[3] + 3), -0.5, (Var_List[3] + 2.5)
                                            num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Var_List[3] + 4), -0.5, (Var_List[3] + 3.5)

                                            histo_for_migration[Migration_Histo_REF] = sdf.Histo2D((str(Migration_Histo_REF), str(Migration_Title), num_of_GEN_bins, min_GEN_bin, Max_GEN_bin, num_of_REC_bins, min_REC_bin, Max_REC_bin), str("".join([str(variable), "_GEN_BIN"])), str("".join([str(variable), "_REC_BIN"])))
                                            
                                        else:

                                            Migration_Title = "".join(["#splitline{#splitline{Bin Migration of ", variable_Title_name(variable), "}{Cut: ", str(cutname), "}}{#scale[1.5]{Number of Bins: ", "302" if("OG" not in variable) else "352", "}}; ", variable_Title_name(variable), " (GEN); ", variable_Title_name(variable), " (REC)"])

                                            Migration_Histo_REF = ("Bin Migration V3", variable, smearing_Q, cut_choice, sec_type, sec_num)

                                            # num_of_REC_bins, min_REC_bin, Max_REC_bin = Var_List[3], 0, Var_List[3]
                                            # num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Var_List[3] + 3), -1, (Var_List[3] + 2)

                                            min_REC_bin, max_REC_bin, num_of_REC_bins = Var_List[1], Var_List[2], Var_List[3]
                                            min_GEN_bin, max_GEN_bin, num_of_GEN_bins = (Var_List[1] - 1), Var_List[2], (Var_List[3] + 1)
                                            
                                            variable_gen = str("".join([str(variable.replace("smeared_", "")), "_gen"])).replace("smeared_", "")

                                            histo_for_migration[Migration_Histo_REF] = sdf.Histo2D((str(Migration_Histo_REF), str(Migration_Title), num_of_GEN_bins, min_GEN_bin, max_GEN_bin, num_of_REC_bins, min_REC_bin, max_REC_bin), variable_gen, str("".join([str(variable)])))
                                            
                                            

                                        if(str(file_location) != 'time'):
                                            histo_for_migration[Migration_Histo_REF].Write()

                                        Print_Progress(count_of_histograms, 1, 200 if(str(file_location) != 'time') else 50)
                                        count_of_histograms += 1   
                                        
                                                
                                elif(option == "response_matrix"):
                                    
                                    Res_Binning_2D_Q2_xB = [Q2_xB_Bin_Filter_str, -1.5, (8 + 1.5) if("_2" in Q2_xB_Bin_Filter_str) else (9 + 1.5), 9 + 4]
                                    Res_Binning_2D_z_pT = [z_pT_Bin_Filter_str, -1.5, 49 + 1.5, 49 + 4]
                                    
                                    Res_Binning_4D = ['Bin_Res_4D', -1.5, 295 + 1.5, 295 + 4]
                                    # Res_Binning_4D_OG = ['Bin_Res_4D_OG', -1.5, 344 + 1.5, 344 + 4]
                                    
                                    # Res_Var_List = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, W_Binning, Res_Binning_2D_Q2_xB, Res_Binning_2D_z_pT, Binning_4D, Binning_4D_OG, Res_Binning_4D, Res_Binning_4D_OG, Binning_5D, Binning_5D_OG]
                                    # Res_Var_List = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, y_Binning, W_Binning, Res_Binning_2D_Q2_xB, Res_Binning_2D_z_pT, Binning_4D, Res_Binning_4D, Binning_5D]
                                    Res_Var_List = [Q2_Binning, xB_Binning, z_Binning, pT_Binning, phi_t_Binning, y_Binning, W_Binning, Res_Binning_2D_Q2_xB, Res_Binning_2D_z_pT, Binning_4D, Res_Binning_4D]

                                    
                                    for Var_List in Res_Var_List:
                                        
                                        variable = Var_List[0]
                                
                                        # if(("smear" in smearing_Q) and ("Q2_xB_Bin" not in variable and "z_pT_Bin" not in variable) and ("smear" not in variable)):
                                        if(("smear" in smearing_Q) and ("smear" not in variable)):
                                            variable = "".join([variable, "_smeared"])
                                            
                                            
                                        # cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, "mdf" if(datatype_2 == "pdf") else datatype_2, cut_choice, "Cut")
                                        cutname = DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, datatype_2, cut_choice, "Cut")

                                        if("continue" in cutname):
                                            continue
                                            
                                        Min_range, Max_range, Num_of_Bins = Var_List[1], Var_List[2], Var_List[3]

                                        if("Bin" in variable):
                                            Min_range = 1
                                            Max_range += -1.5
                                            Num_of_Bins += -4
                                            
                                        if("Q2_xB_Bin" in variable and "2" in smearing_Q):
                                            Min_range = 1
                                            Max_range = (8 + 1.5)
                                            Num_of_Bins = 8

                                            
                                        BIN_SIZE = round((Max_range - Min_range)/Num_of_Bins, 4)
                                        Bin_Range = "".join([str(Min_range), " #rightarrow ", str(Max_range)])
                                        
                                        
                                        Migration_Title_L1 = "".join(["#scale[1.5]{Response Matrix of ", variable_Title_name(variable), "}"]) if(datatype_2 == "mdf" or datatype_2 == "pdf") else "".join(["#scale[1.5]{", "Experimental" if(datatype_2 == "rdf") else "Generated" if(datatype_2 != "mdf") else "Reconstructed (MC)", " Distribution of ", variable_Title_name(variable), "}"])                                            
                                        Migration_Title_L2 = "".join(["#scale[1.15]{Cut: ", str(cutname), "}"])
                                        Migration_Title_L3 = "".join(["#scale[1.35]{Number of Bins: ", str(Num_of_Bins), " - Range (from Bin 1-", str(Num_of_Bins),"): ", str(Bin_Range), " - Size: ", str(BIN_SIZE), " per bin}"])
                                        if("Bin" in variable):
                                            Migration_Title_L3 = "".join(["#scale[1.35]{Number of Bins: ", str(Num_of_Bins), "}"])

                                        Migration_Title = "".join(["#splitline{#splitline{", str(Migration_Title_L1), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}; ", variable_Title_name(variable.replace("_smeared", "")), " GEN Bins; ", variable_Title_name(variable), " REC Bins"])
                                        
                                        if(datatype_2 != "mdf" and datatype_2 != "pdf"):
                                            Migration_Title = "".join(["#splitline{#splitline{", str(Migration_Title_L1), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}; ", variable_Title_name(variable), " REC" if("g" not in datatype_2) else " GEN", " Bins; Count"])
                                            

                                        Migration_Histo_REF = ("Response_Matrix" if(datatype_2 == "mdf" or datatype_2 == "pdf") else "Response_Matrix_1D", variable, smearing_Q, cut_choice, sec_type, sec_num, datatype_2)
                                        
                                        if(datatype_2 == "mdf"):
                                            Migration_Title_L1_2 = "".join(["#scale[1.5]{Reconstructed (MC) Distribution of ", variable_Title_name(variable), "}"])
                                            Migration_Title_2 = "".join(["#splitline{#splitline{", str(Migration_Title_L1_2), "}{", str(Migration_Title_L2), "}}{", str(Migration_Title_L3), "}; ", variable_Title_name(variable), " REC Bins; Count"])
                                            Migration_Histo_REF_2 = ("Response_Matrix_1D", variable, smearing_Q, cut_choice, sec_type, sec_num, datatype_2)

                                        # sdf = bin_purity_save_fuction_New(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, "mdf" if(datatype_2 == "pdf") else datatype_2, cut_choice, "DF"), variable, Min_range, Max_range, Num_of_Bins, datatype_2)
                                        sdf = bin_purity_save_fuction_New(DF_Filter_Function_Full(rdf, sec_type, sec_num, -1, -2, variable, smearing_Q, datatype_2, cut_choice, "DF"), variable, Min_range, Max_range, Num_of_Bins, datatype_2)

                                        num_of_REC_bins, min_REC_bin, Max_REC_bin = (Num_of_Bins + 4), -0.5, (Num_of_Bins + 3.5) # Num of REC bins needs to equal Num of GEN bins for unfolding
                                        num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Num_of_Bins + 4), -0.5, (Num_of_Bins + 3.5)
                                        
                                        Variable_Gen = str("".join([str(variable), "_GEN_BIN"])) if("Bin" not in str(variable)) else str("".join([str(variable).replace("_smeared", ""), "_gen"]))
                                        Variable_Rec = str("".join([str(variable), "_REC_BIN"])) if("Bin" not in str(variable)) else str(variable)

                                        if(datatype_2 == "mdf" or datatype_2 == "pdf"):
                                            histo_for_migration[Migration_Histo_REF] = sdf.Histo2D((str(Migration_Histo_REF), str(Migration_Title), num_of_GEN_bins, min_GEN_bin, Max_GEN_bin, num_of_REC_bins, min_REC_bin, Max_REC_bin), str(Variable_Gen), str(Variable_Rec))
                                            if(datatype_2 == "mdf"):
                                                histo_for_migration[Migration_Histo_REF_2] = sdf.Histo1D((str(Migration_Histo_REF_2), str(Migration_Title_2), num_of_REC_bins, min_REC_bin, Max_REC_bin), str(Variable_Rec))                                                
                                        else:
                                            histo_for_migration[Migration_Histo_REF] = sdf.Histo1D((str(Migration_Histo_REF), str(Migration_Title), num_of_REC_bins, min_REC_bin, Max_REC_bin), str(Variable_Rec))

                                            
                                        if(datatype_2 == "mdf"):
                                            if(str(file_location) != 'time'):
                                                histo_for_migration[Migration_Histo_REF].Write()
                                                histo_for_migration[Migration_Histo_REF_2].Write()
                                            Print_Progress(count_of_histograms, 2, 200 if(str(file_location) != 'time') else 50)
                                            count_of_histograms += 2
                                        else:
                                            if(str(file_location) != 'time'):
                                                histo_for_migration[Migration_Histo_REF].Write()
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

        print("".join(["Total Number of Histograms Made: ", str(count_of_histograms)]))
        
        
        # See beginning of code...
        if(output_all_histo_names_Q == "yes"):
            print("\nHistograms be made:")
            for ii in [Mom_Cor_Histos, Kinetic_Histo_3D, histo_for_counts, histo_for_2D_Purity, histo_for_migration]:
                for ii2 in ii:
                    print(ii2)
            print("\n")
        elif(str(file_location) == 'time'):
            print("\nChoose not to print list of final histograms...\nSet output_all_histo_names_Q = 'yes' or enter 'test' instead of a file name to print a list of histograms made while running...\n")
        
        
    elif(output_type != "histo" and output_type != "test" and output_type != 'time'):
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
    

    
    
    print("\n")
    
    ######################################===============================######################################
    ##==========##==========##==========##          End of Code          ##==========##==========##==========##
    ######################################===============================######################################
    
    
else:
    print("\nERROR: No valid datatype selected...\n")
    
# This Code was last updated on 9-22-2022