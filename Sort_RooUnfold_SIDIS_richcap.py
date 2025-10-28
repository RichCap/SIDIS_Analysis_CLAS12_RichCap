#!/usr/bin/env python3

from MyCommonAnalysisFunction_richcap import color, color_bg
print(f"\n{color.BOLD}Starting RG-A SIDIS Analysis (File Sorting){color.END}\n")

import traceback
from datetime import datetime

import shutil
import os

import argparse
import sys

# Capture and print start time
datetime_object_full = datetime.now()
time_formatted = datetime_object_full.strftime("%m-%d-%Y at %I:%M %p").lstrip("0").replace(" 0", " ")
print(f"{color.BOLD}Started running on {time_formatted}{color.END}\n")



################################################################################################################################################################
##==========##==========##     Names of Requested File(s)     ##==========##==========##==========##==========##==========##==========##==========##==========##
################################################################################################################################################################
# Set up the argument parser
parser = argparse.ArgumentParser(description='This script will take the available PNG and text files in the directory it is located in and organize them into a series of folders.\n\tWhen running, the script will ask for confirmation before creating a new folder/moving any files.\n\tIf --use-existing is specified, files will be sorted into an existing folder without creating a new one.', epilog="""
    """, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('Common_Name', type=str,                       help='Name used for folder creation or folder to sort into if using --use-existing')
parser.add_argument('-u', '--use-existing',   action='store_true', help='Sort files into an existing folder without creating a new one')
parser.add_argument('-r', '--auto-replace',   action='store_true', help='If a file already exists in a directory with the same name as the file being moved to that directory, this option will assume that the user will always want to replace the older image')

# Parse the arguments
args = parser.parse_args()
use_existing = args.use_existing
auto_replace = args.auto_replace
# Assign the argument value to the Common_Name variable
Common_Name = args.Common_Name
print(f"The provided common name is: {Common_Name}")

if(auto_replace):
    print(f"\n{color.BOLD}Will automatically replace older images if a newer one with the same name is found.\n{color.END}")



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

# Date_of_Save = "".join([str(datetime_object_full.month), "_", str(datetime_object_full.day), "_", str(datetime_object_full.year)])
Date_of_Save = datetime_object_full.strftime("%m_%d_%Y")


##========================================##
##=====##   Main Folder Creation   ##=====##
# destination = "".join(["/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_From_", str(Common_Name).replace("_All", ""), "_", str(Date_of_Save)])
destination = f"/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_From_{Common_Name.replace('_All', '')}_{Date_of_Save}"
if(use_existing):
    if(not os.path.exists(destination)):
        if(not os.path.exists(Common_Name)):
            print(f"{color.Error}Error: Specified folder {destination} does not exist. Ensure the folder was created in a previous run.{color.END}")
            sys.exit()
        else:
            destination = Common_Name
    print(f"{color.BBLUE}Using existing directory:\n\t{destination}{color.END}")
else:
    version = 2
    while(destination.replace("/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/", "") in os.listdir()):
        print(f"{color.BOLD}Error: {color.END_R}{destination}{color.END_B} already exists...{color.END}\n\tChecking for new version ({version - 1})")
        destination = f"/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/SIDIS_python_Images_V{version}_From_{Common_Name.replace('_All', '')}_{Date_of_Save}"
        version += 1
        if(version > 11):
            print(f"{color.Error}\nWARNING: Too many folders with the same name/date. This loop stops after 10 versions.\n{color.END}")
            raise TypeError("Too many folders with the same name/date")
    print(f"\nWill create a new directory called:\n\t{color.BBLUE}{destination}{color.END}")

user_approval = input("\nDo you approve to continue? (yes/no): ").lower()
if(user_approval not in ['yes', 'y', 'Yes', 'Y']):
    print(f"{color.Error}User did not approve. Exiting the script.{color.END}\n\n")
    sys.exit()  # Exit the script if the user does not approve

print(f"User approved.\n\n{color.BBLUE}Starting final folder creation/image sorting...{color.END}\n")
        
if(not use_existing):
    os.mkdir(destination)
##=====##   Main Folder Creation   ##=====##
##========================================##

##============================================##
##=====##   Category Folder Creation   ##=====##
destination_main = "".join([str(destination), "/Unfolding_Images"])
destination_Pars = "".join([str(destination), "/Fit_Pars"])

if(not use_existing):
    os.mkdir(destination_main)
    os.mkdir(destination_Pars)


# destination_Par_A = "".join([str(destination_Pars), "/Fit_Par_A"])
destination_Par_B = "".join([str(destination_Pars), "/Fit_Par_B"])
destination_Par_C = "".join([str(destination_Pars), "/Fit_Par_C"])

if(not use_existing):
    # os.mkdir(destination_Par_A)
    os.mkdir(destination_Par_B)
    os.mkdir(destination_Par_C)


##=====##   Category Folder Creation   ##=====##
##============================================##


##===================================================##
##=====##   z-pT Unfolding Folders Creation   ##=====##
destination_z_pT_Bin_All        = "".join([str(destination_main), "/z_pT_Bin_All"])
destination_z_pT_Bin_Individual = "".join([str(destination_main), "/z_pT_Bin_Individual"])
if(not use_existing):
    os.mkdir(destination_z_pT_Bin_All)
    os.mkdir(destination_z_pT_Bin_Individual)
##=====##   z-pT Unfolding Folders Creation   ##=====##
##===================================================##


##=============================================================##
##=====##   z-pT (Smeared) Unfolding Folders Creation   ##=====##
destination_Smeared                     = "".join([str(destination_main), "/Smeared"])
destination_Smeared_z_pT_Bin_All        = "".join([str(destination_main), "/Smeared/z_pT_Bin_All"])
destination_Smeared_z_pT_Bin_Individual = "".join([str(destination_main), "/Smeared/z_pT_Bin_Individual"])
if(not use_existing):
    os.mkdir(destination_Smeared)
    os.mkdir(destination_Smeared_z_pT_Bin_All)
    os.mkdir(destination_Smeared_z_pT_Bin_Individual)
##=====##   z-pT (Smeared) Unfolding Folders Creation   ##=====##
##=============================================================##


##=========================================================##
##=====##   Q2-xB/Q2-y Unfolding Folders Creation   ##=====##
if(not use_existing):
    # for folder in [destination_z_pT_Bin_All, destination_z_pT_Bin_Individual, destination_Smeared_z_pT_Bin_All, destination_Smeared_z_pT_Bin_Individual, destination_Par_A, destination_Par_B, destination_Par_C]:
    for folder in [destination_z_pT_Bin_All, destination_z_pT_Bin_Individual, destination_Smeared_z_pT_Bin_All, destination_Smeared_z_pT_Bin_Individual, destination_Par_B, destination_Par_C]:
        for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
            if((Q2_xB_Bin != 0) or (str(folder) not in [str(destination_Par_A), str(destination_Par_B), str(destination_Par_C)])):
                os.mkdir("".join([str(folder), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
##=====##   Q2-xB/Q2-y Unfolding Folders Creation   ##=====##
##=========================================================##


# Handle file move with overwrite check
def handle_file_move(src, dest_folder, AUTO=auto_replace):
    # Construct the full destination path, including the filename
    dest_file_path = os.path.join(dest_folder, os.path.basename(src))
    # Check if a file with the same name exists in the destination folder
    if(os.path.exists(dest_file_path)):
        print(f"{color.Error}Warning: {dest_file_path} already exists...{color.END}")
        if(not AUTO):
            print(f"{color.BOLD}Do you want to overwrite it?{color.END}")
            choice = input("Type 'yes'|'y'|'replace' to overwrite, 'new'|'rename' to rename, or 'no'|'n'|'skip' to skip: ").strip().lower()
            print("\n")
        else:
            choice = "replace"
        if(choice in ['yes', 'y', 'replace', '']):
            shutil.move(src, dest_file_path)
            print(f"{color.BGREEN}File {src} replaced in {dest_file_path}{color.END}\n")
        elif(choice in ['new', 'rename']):
            version = 1
            new_dest_file_path = dest_file_path
            # Find a new filename with an incrementing version number
            while(os.path.exists(new_dest_file_path)):
                base, ext = os.path.splitext(dest_file_path)
                new_dest_file_path = f"{base}_V{version}{ext}"
                version += 1
            shutil.move(src, new_dest_file_path)
            print(f"{color.BGREEN}File {src} renamed and moved to {new_dest_file_path}{color.END}\n")
        elif(choice in ['no', 'n', 'skip']):
            print(f"{color.Error}Skipping file: {src}{color.END}\n")
    else:
        shutil.move(src, dest_file_path)
        print(f"{color.BGREEN}File {src} moved to {dest_file_path}{color.END}")



##=================================##
##=====##   Image Sorting   ##=====##
for Entry in os.listdir():
    try:
        if('.txt'          in str(Entry)):
            if("".join([str(Common_Name).replace("_All", ""), "_", str(Date_of_Save)]) in str(Entry)):
                # shutil.move(Entry, destination)
                handle_file_move(Entry, destination)
        if('.png'          in str(Entry)):
            # if("Sim_Test_" in str(Entry)):
            #     os.rename(Entry, str(Entry).replace("Sim_Test_", ""))
            #     Entry = str(Entry).replace("Sim_Test_", "")
            Moved_Q = False
            if("Fit_Par" in str(Entry)):
                # if("Fit_Par_A" in str(Entry)):
                #     for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                #         if("".join([str(Binning_Option), "_", str(Q2_xB_Bin), "_"]) in str(Entry)):
                #             shutil.move(Entry, "".join([str(destination_Par_A), "/", str(Binning_Option), "_", str(Q2_xB_Bin)]))
                #             Moved_Q = True
                #             break
                if("Fit_Par_B" in str(Entry)):
                    for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                        if("".join([str(Binning_Option), "_", str(Q2_xB_Bin), "_"]) in str(Entry)):
                            # shutil.move(Entry, "".join([str(destination_Par_B), "/", str(Binning_Option), "_", str(Q2_xB_Bin)]))
                            handle_file_move(Entry, os.path.join(destination_Par_B, f"{Binning_Option}_{Q2_xB_Bin}"))
                            Moved_Q = True
                            break
                if("Fit_Par_C" in str(Entry)):
                    for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                        if("".join([str(Binning_Option), "_", str(Q2_xB_Bin), "_"]) in str(Entry)):
                            # shutil.move(Entry, "".join([str(destination_Par_C), "/", str(Binning_Option), "_", str(Q2_xB_Bin)]))
                            handle_file_move(Entry, os.path.join(destination_Par_C, f"{Binning_Option}_{Q2_xB_Bin}"))
                            Moved_Q = True
                            break
                if(not Moved_Q):
                    # shutil.move(Entry, str(destination_Pars))
                    handle_file_move(Entry, str(destination_Pars))
                    Moved_Q = True
                
            if((("Response_Matrix_" in str(Entry)) or ("Kinematic_Comparison_" in str(Entry))) and ("_z_pT_Bin_"   in str(Entry))):
                for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                    if("".join([str(Binning_Option), "_", str(Q2_xB_Bin), "_"])  in str(Entry)):
                        if(("Smear" not in str(Entry))                                           and ("smear"    not in str(Entry))):
                            try:
                                # shutil.move(Entry, "".join([str(destination_z_pT_Bin_Individual),         "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                                handle_file_move(Entry, os.path.join(destination_z_pT_Bin_Individual, f"{str(Binning_Option)}_{str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else 'All'}"))
                                Moved_Q = True
                            except:
                                print(f"{color.Error}ERROR in Unsmeared 'Response_Matrix': {color.END}\n{traceback.format_exc()}\n")
                        else:
                            try:
                                # shutil.move(Entry, "".join([str(destination_Smeared_z_pT_Bin_Individual), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                                handle_file_move(Entry, os.path.join(destination_Smeared_z_pT_Bin_Individual, f"{str(Binning_Option)}_{str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else 'All'}"))
                                Moved_Q = True
                            except:
                                print(f"{color.Error}ERROR in Smeared 'Response_Matrix': {color.END}\n{traceback.format_exc()}\n")
            elif(("Unfolded_Histos"      in str(Entry)) and ("_z_pT_Bin_"    not in str(Entry))):
                for Q2_xB_Bin in range(9 if("xB" in Binning_Option) else 17, 0, -1):
                    if("".join([str(Binning_Option), "_", str(Q2_xB_Bin), "_"])  in str(Entry)):
                        if(("Smear" not in str(Entry))  and ("smear"         not in str(Entry))):
                            try:
                                # shutil.move(Entry, "".join([str(destination_z_pT_Bin_All),         "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                                handle_file_move(Entry, os.path.join(destination_z_pT_Bin_All, f"{str(Binning_Option)}_{str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else 'All'}"))
                                Moved_Q = True
                            except:
                                print(f"{color.Error}ERROR in Unsmeared 'Unfolded_Histos': {color.END}\n{traceback.format_exc()}\n")
                        else:
                            try:
                                # shutil.move(Entry, "".join([str(destination_Smeared_z_pT_Bin_All), "/", str(Binning_Option), "_", str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else "All"]))
                                handle_file_move(Entry, os.path.join(destination_Smeared_z_pT_Bin_All, f"{str(Binning_Option)}_{str(Q2_xB_Bin) if(Q2_xB_Bin != 0) else 'All'}"))
                                Moved_Q = True
                            except:
                                print(f"{color.Error}ERROR in Smeared 'Unfolded_Histos': {color.END}\n{traceback.format_exc()}\n")
                                
            elif(not Moved_Q):
                # shutil.move(Entry, destination)
                handle_file_move(Entry, destination)
                Moved_Q = True
            if(not Moved_Q):
                print(f"\nNo folder found to move '{Entry}' to...\n")
                # shutil.move(Entry, destination)
                handle_file_move(Entry, destination)
                
    except:
        print(f"\n\n{color.Error}ERROR IN ENTRY OF THE listdir():{color.END_R}\n\n{str(traceback.format_exc())}{color.END}\n\n")
        
##=====##   Image Sorting   ##=====##
##=================================##


#############################################################################
#############################################################################
##====================##                             ##====================##
##====================##     Final Image Sorting     ##====================##
##====================##                             ##====================##
#############################################################################
#############################################################################
    

print(f"""\n\n{color.BGREEN}{color_bg.YELLOW}
\t                                   \t   
\t                                   \t   
\tThis code has now finished running.\t   
\t                                   \t   
\t                                   \t   
{color.END}""")

