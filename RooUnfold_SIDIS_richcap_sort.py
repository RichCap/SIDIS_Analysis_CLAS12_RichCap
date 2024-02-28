#!/usr/bin/env python

from MyCommonAnalysisFunction_richcap import color, color_bg
print(f"{color.BOLD}\nStarting RG-A SIDIS Analysis (File Sorting)\n{color.END}")

import traceback
from datetime import datetime

import shutil
import os

import argparse
import sys

# getting current date
datetime_object_full = datetime.now()
# print(datetime_object)

startMin_full = datetime_object_full.minute
startHr_full  = datetime_object_full.hour

if(datetime_object_full.minute <10):
    timeMin_full = "".join(["0", str(datetime_object_full.minute)])
else:
    timeMin_full = str(datetime_object_full.minute)

    
Date_Day = "".join(["Started running on ", color.BOLD, str(datetime_object_full.month), "-", str(datetime_object_full.day), "-", str(datetime_object_full.year), color.END, " at "])
# printing current time
if(datetime_object_full.hour > 12 and datetime_object_full.hour < 24):
    print("".join([Date_Day, color.BOLD, str((datetime_object_full.hour)-12), ":", timeMin_full, " p.m.", color.END]))
if(datetime_object_full.hour < 12 and datetime_object_full.hour > 0):
    print("".join([Date_Day, color.BOLD, str(datetime_object_full.hour), ":", timeMin_full, " a.m.", color.END]))
if(datetime_object_full.hour == 12):
    print("".join([Date_Day, color.BOLD, str(datetime_object_full.hour), ":", timeMin_full, " p.m.", color.END]))
if(datetime_object_full.hour == 0 or datetime_object_full.hour == 24):
    print("".join([Date_Day, color.BOLD, "12:", str(timeMin_full), " a.m.", color.END]))        
print("")



################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################
# Common_Name = "Unfolding_Tests_V13_All"
# Common_Name = "Analysis_Note_Update_V6_All"
# Common_Name = "Multi_Dimension_Unfold_V3_All"
# Common_Name = "Multi_Dimension_Unfold_V3_Simulated_Test_All"

# Common_Name = "New_Binning_Schemes_V8_All"

# Common_Name = "Gen_Cuts_V2_Sim_All"
# Common_Name = "Gen_Cuts_V7_Modulated_All"


Common_Name = "Gen_Cuts_V8_All"
# # Common_Name = "Gen_Cuts_V7_Sim_Modulated_All"
# Common_Name = "Gen_Cuts_V8_Closure_All"
# Common_Name = "Gen_Cuts_V8_Sim_All"

# Common_Name = "New_Bin_Tests_V5_All"

Common_Name = "Pass_2_CrossCheck_V3_All"

Common_Name = "CrossCheck_V3_All"

Common_Name = "Q2_Y_Bins_V2_All"
Common_Name = "Pass_2_New_Q2_Y_Bins_V2_All"

# Set up the argument parser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('Common_Name', type=str, help='A common name to be used in the script')

# Parse the arguments
args = parser.parse_args()

# Assign the argument value to the Common_Name variable
Common_Name = args.Common_Name
print(f"The provided common name is: {Common_Name}")



################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################


# Binning_Option = "Q2_xB_Bin"
Binning_Option = "Q2_y_Bin"


#############################################################################
#############################################################################
##====================##                             ##====================##
##====================##     Final Image Sorting     ##====================##
##====================##                             ##====================##
#############################################################################
#############################################################################

Date_of_Save = "".join([str(datetime_object_full.month), "_", str(datetime_object_full.day), "_", str(datetime_object_full.year)])


##========================================##
##=====##   Main Folder Creation   ##=====##
destination = "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_From_", str(Common_Name).replace("_All", ""), "_", str(Date_of_Save)])
version = 2
while(str(destination).replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/", "") in os.listdir()):
    print(f"{color.BOLD}Error: {color.END}{color.RED}{destination}{color.END}{color.BOLD} already exists...{color.END}\n\tChecking for new version ({version - 1})")
    destination = "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_V", str(version), "_From_", str(Common_Name).replace("_All", ""), "_", str(Date_of_Save)])
    version += 1
    if(version > 11):
        print("".join([color.Error, "\nWARNING: Many folders are being saved from the same date. This loop is automatically closed after 10 versions for the same folder.\n\n\tPlease overide this decision manually if this many folders are desired...\n\n", color.END]))
        fail

print(f"\nWill create a new directory called:\n\t{color.BOLD}{color.BLUE}{destination}{color.END}")
user_approval = input("\nDo you approve to continue? (yes/no): ").lower()
if(user_approval not in ['yes', 'y', 'Yes', 'Y']):
    print(f"{color.Error}User did not approve. Exiting the script.{color.END}\n\n")
    sys.exit()  # Exit the script if the user does not approve

print(f"User approved.\n\n{color.BOLD}{color.BLUE}Starting final folder creation/image sorting...{color.END}\n")
        

os.mkdir(destination)
##=====##   Main Folder Creation   ##=====##
##========================================##

##============================================##
##=====##   Category Folder Creation   ##=====##
destination_main = "".join([str(destination), "/Unfolding_Images"])
# destination_pars = "".join([str(destination), "/Parameter_Images"])
# destination_mult = "".join([str(destination), "/Multi_Dim_Histo_Combined"])
destination_mult = "".join([str(destination), "/Multi_Dim_Histo"])
destination_Pars = "".join([str(destination), "/Fit_Pars"])
# destination_txt  = "".join([str(destination), "/Text_Files"])

os.mkdir(destination_main)
# os.mkdir(destination_pars)
os.mkdir(destination_mult)
os.mkdir(destination_Pars)
# os.mkdir(destination_txt)

# destination_mult_Q2_phi_h       = "".join([str(destination_mult), "/Multi_Dim_Q2_phi_h"])
destination_mult_Q2_y_Bin_phi_h = "".join([str(destination_mult), "/Multi_Dim_Q2_y_Bin_phi_h"])
destination_mult_z_pT_Bin_phi_h = "".join([str(destination_mult), "/Multi_Dim_z_pT_Bin_phi_h"])

# os.mkdir(destination_mult_Q2_phi_h)
os.mkdir(destination_mult_Q2_y_Bin_phi_h)
os.mkdir(destination_mult_z_pT_Bin_phi_h)

# os.mkdir("".join([str(destination_mult_Q2_phi_h),       "/Response_Matrix"]))
# os.mkdir("".join([str(destination_mult_Q2_y_Bin_phi_h), "/Response_Matrix"]))
# os.mkdir("".join([str(destination_mult_z_pT_Bin_phi_h), "/Response_Matrix"]))


destination_Par_A = "".join([str(destination_Pars), "/Fit_Par_A"])
destination_Par_B = "".join([str(destination_Pars), "/Fit_Par_B"])
destination_Par_C = "".join([str(destination_Pars), "/Fit_Par_C"])

# os.mkdir(destination_Par_A)
os.mkdir(destination_Par_B)
os.mkdir(destination_Par_C)


##=====##   Category Folder Creation   ##=====##
##============================================##


##===================================================##
##=====##   z-pT Unfolding Folders Creation   ##=====##
destination_z_pT_Bin_All        = "".join([str(destination_main), "/z_pT_Bin_All"])
destination_z_pT_Bin_Individual = "".join([str(destination_main), "/z_pT_Bin_Individual"])
os.mkdir(destination_z_pT_Bin_All)
os.mkdir(destination_z_pT_Bin_Individual)
##=====##   z-pT Unfolding Folders Creation   ##=====##
##===================================================##


##=============================================================##
##=====##   z-pT (Smeared) Unfolding Folders Creation   ##=====##
destination_Smeared                     = "".join([str(destination_main), "/Smeared"])
destination_Smeared_z_pT_Bin_All        = "".join([str(destination_main), "/Smeared/z_pT_Bin_All"])
destination_Smeared_z_pT_Bin_Individual = "".join([str(destination_main), "/Smeared/z_pT_Bin_Individual"])
os.mkdir(destination_Smeared)
os.mkdir(destination_Smeared_z_pT_Bin_All)
os.mkdir(destination_Smeared_z_pT_Bin_Individual)
##=====##   z-pT (Smeared) Unfolding Folders Creation   ##=====##
##=============================================================##


##=========================================================##
##=====##   Q2-xB/Q2-y Unfolding Folders Creation   ##=====##
# for folder in [destination_z_pT_Bin_All, destination_z_pT_Bin_Individual, destination_Smeared_z_pT_Bin_All, destination_Smeared_z_pT_Bin_Individual, destination_Par_A, destination_Par_B, destination_Par_C]:
for folder in [destination_z_pT_Bin_All, destination_z_pT_Bin_Individual, destination_Smeared_z_pT_Bin_All, destination_Smeared_z_pT_Bin_Individual, destination_Par_B, destination_Par_C]:
    # for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, -1, -1):
    for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
        if((Q2_xB_Bin != 0) or (str(folder) not in [str(destination_Par_A), str(destination_Par_B), str(destination_Par_C)])):
            os.mkdir("".join([str(folder), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))

##=====##   Q2-xB/Q2-y Unfolding Folders Creation   ##=====##
##=========================================================##


##=================================##
##=====##   Image Sorting   ##=====##
for Entry in os.listdir():
    try:
        if("Sim_Test_" in str(Entry)):
            os.rename(Entry, str(Entry).replace("Sim_Test_", ""))
            Entry = str(Entry).replace("Sim_Test_", "")
        # if('.txt'      in str(Entry)):
        #     shutil.move(Entry, destination_txt)
        if('.png'      in str(Entry)):
            # print("\n"+str(Entry))
            # if("_Pars_" in str(Entry)):
            #     shutil.move(Entry, destination_pars)
            if("Fit_Par" in str(Entry)):
                # if("Fit_Par_A" in str(Entry)):
                #     # for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, -1, -1):
                #     for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                #         if("".join([str(Binning_Option), "_", str(Q2_xB_Bin), "_"]) in str(Entry)):
                #             shutil.move(Entry, "".join([str(destination_Par_A), "/", str(Binning_Option), "_", str(Q2_xB_Bin)]))
                #             break
                if("Fit_Par_B" in str(Entry)):
                    # for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, -1, -1):
                    for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                        if("".join([str(Binning_Option), "_", str(Q2_xB_Bin), "_"]) in str(Entry)):
                            shutil.move(Entry, "".join([str(destination_Par_B), "/", str(Binning_Option), "_", str(Q2_xB_Bin)]))
                            break
                if("Fit_Par_C" in str(Entry)):
                    # for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, -1, -1):
                    for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                        if("".join([str(Binning_Option), "_", str(Q2_xB_Bin), "_"]) in str(Entry)):
                            shutil.move(Entry, "".join([str(destination_Par_C), "/", str(Binning_Option), "_", str(Q2_xB_Bin)]))
                            break
                shutil.move(Entry, str(destination_Pars))
                
            if("Multi_Dim_Histo_" in str(Entry)):
                try:
                    # if("Response_Matrix_Normal_Multi_Dim_" in str(Entry)):
                    #     if("Q2_phi_h" in str(Entry)):
                    #         shutil.move(Entry, "".join([str(destination_mult_Q2_phi_h),       "/Response_Matrix"]))
                    #     elif(("Q2_y_Bin_phi_h" in str(Entry)) or ("Q2_y_phi_h" in str(Entry))):
                    #         shutil.move(Entry, "".join([str(destination_mult_Q2_y_Bin_phi_h), "/Response_Matrix"]))
                    #     elif(("z_pT_Bin_phi_h" in str(Entry)) or ("z_pT_phi_h" in str(Entry)) or ("z_pT_Bin_y_bin_phi_h" in str(Entry)) or ("z_pT_y_bin_phi_h" in str(Entry))):
                    #         shutil.move(Entry, "".join([str(destination_mult_z_pT_Bin_phi_h), "/Response_Matrix"]))
                    #     else:
                    #         shutil.move(Entry, destination_mult)
                    # else:
                    # if("Q2_phi_h" in str(Entry)):
                    #     shutil.move(Entry, destination_mult_Q2_phi_h)
                    if(("Q2_y_Bin_phi_h"   in str(Entry)) or ("Q2_y_phi_h" in str(Entry))):
                        shutil.move(Entry, destination_mult_Q2_y_Bin_phi_h)
                    elif(("z_pT_Bin_phi_h" in str(Entry)) or ("z_pT_phi_h" in str(Entry)) or ("z_pT_Bin_y_bin_phi_h" in str(Entry)) or ("z_pT_y_bin_phi_h" in str(Entry))):
                        shutil.move(Entry, destination_mult_z_pT_Bin_phi_h)
                    else:
                        shutil.move(Entry, destination_mult)
                except:
                    print("".join([color.RED, "ERROR in 'Multi_Dim_Histo': \n", color.END, str(traceback.format_exc()), "\n"]))
                    try:
                        shutil.move(Entry, destination_mult)
                    except:
                        print("".join([color.RED, color.BOLD, "\n2nd ERROR in 'Multi_Dim_Histo': \n", color.END, str(traceback.format_exc()), "\n"]))
            elif((("Response_Matrix_" in str(Entry)) or ("Kinematic_Comparison_" in str(Entry)))    and ("_z_pT_Bin_"   in str(Entry))):
                # for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, -1, -1):
                for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                    if("".join([str(Binning_Option), "_", str(Q2_xB_Bin)]) in str(Entry)):
                        if(("Smear" not in str(Entry))                                              and ("smear"    not in str(Entry))):
                            try:
                                shutil.move(Entry, "".join([str(destination_z_pT_Bin_Individual),         "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                            except:
                                print("".join([color.RED, color.BOLD, "ERROR in Unsmeared 'Response_Matrix': \n", color.END, str(traceback.format_exc()), "\n"]))
                        else:
                            try:
                                shutil.move(Entry, "".join([str(destination_Smeared_z_pT_Bin_Individual), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                            except:
                                print("".join([color.RED, color.BOLD, "ERROR in Smeared 'Response_Matrix': \n", color.END, str(traceback.format_exc()), "\n"]))

            elif(("Unfolded_Histos"      in str(Entry)) and ("_z_pT_Bin_" not in str(Entry))):
                # for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, -1, -1):
                for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                    if("".join([str(Binning_Option), "_", str(Q2_xB_Bin)])    in str(Entry)):
                        if(("Smear" not in str(Entry))  and ("smear"      not in str(Entry))):
                            try:
                                shutil.move(Entry, "".join([str(destination_z_pT_Bin_All),         "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                            except:
                                print("".join([color.RED, color.BOLD, "ERROR in Unsmeared 'Unfolded_Histos': \n", color.END, str(traceback.format_exc()), "\n"]))
                        else:
                            try:
                                shutil.move(Entry, "".join([str(destination_Smeared_z_pT_Bin_All), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                            except:
                                print("".join([color.RED, color.BOLD, "ERROR in Smeared 'Unfolded_Histos': \n", color.END, str(traceback.format_exc()), "\n"]))
            else:
                # print(destination)
                shutil.move(Entry, destination)
                
    except:
        print("".join([color.RED, color.BOLD, "\n\nERROR IN ENTRY OF THE listdir():\n\n", color.END, color.RED, str(traceback.format_exc()), color.END, "\n\n"]))
        
##=====##   Image Sorting   ##=====##
##=================================##


#############################################################################
#############################################################################
##====================##                             ##====================##
##====================##     Final Image Sorting     ##====================##
##====================##                             ##====================##
#############################################################################
#############################################################################
    

print("".join([color.BOLD, color.GREEN, color_bg.YELLOW, """
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
""", color.END]))

