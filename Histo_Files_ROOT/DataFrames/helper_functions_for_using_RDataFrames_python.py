#!/usr/bin/env python3

import sys
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, variable_Title_name
from ExtraAnalysisCodeValues import New_z_pT_and_MultiDim_Binning_Code
sys.path.remove(script_dir)
del script_dir


def Cut_Choice_Title(Cut_Type="no_cut"):
    Cut_Name = "Undefined Cut (ERROR)"
    if("no_cut"   in str(Cut_Type)):
        Cut_Name = "No Cuts"
    if("EDIS"     in str(Cut_Type)):
        Cut_Name = "Exclusive Cuts"
    if("SIDIS"    in str(Cut_Type)):
        Cut_Name = "SIDIS Cuts"
    if("MM"       in str(Cut_Type)):
        Cut_Name = "Cuts with Inverted MM Cut"
    if("Gen"      in str(Cut_Type)):
        Cut_Name = "Cuts with Generated MM Cut"
    if("Exgen"    in str(Cut_Type)):
        Cut_Name = "Cuts with Inverted Generated MM Cut"
    if("Binned"   in str(Cut_Type)):
        Cut_Name = f"{Cut_Name} with Kinematic Binning"
    if("Proton"   in str(Cut_Type)):
        Cut_Name = f"{Cut_Name} with Proton Cuts"
    if("RevPro"   in str(Cut_Type)):
        Cut_Name = f"{Cut_Name} with Inverted Proton Cuts"
    if("Complete" in str(Cut_Type)):
        Cut_Name = f"Complete Set of {Cut_Name}"
    if("eS" in str(Cut_Type)):
        for sec in range(1, 7, 1):
            if(f"eS{sec}a" in str(Cut_Type)):
                Cut_Name = f"{Cut_Name} (Excluding Sector {sec} Electrons)"
            if(f"eS{sec}o" in str(Cut_Type)):
                Cut_Name = f"{Cut_Name} (Sector {sec} Electrons Only)"
    return Cut_Name

def BG_Cut_Function(dataframe="mdf"):
    if(dataframe in ["rdf"]):
        return ""
    else:
        Background_Cuts_MC = ""
        List_of_Cuts = []
        List_of_Cuts.append("MM_gen < 1.5")
        List_of_Cuts.append("PID_el  != 11  && PID_el  != 0") # Identifies the particles that were matched but to the wrong particle
        List_of_Cuts.append("PID_pip != 211 && PID_pip != 0") # Identifies the particles that were matched but to the wrong particle
        List_of_Cuts.append("PID_el  == 0")                   # Identifies unmatched particles
        List_of_Cuts.append("PID_pip == 0")                   # Identifies unmatched particles
        for cuts in List_of_Cuts:
            if(dataframe in ["gdf"]):
                if("PID" in str(cuts)):
                    continue
                else:
                    cuts = str(cuts.replace("_gen", ""))
            Background_Cuts_MC = f"({cuts})" if(Background_Cuts_MC in [""]) else f"{Background_Cuts_MC} || ({cuts})"
        return Background_Cuts_MC
    return "ERROR"

# def Multi_Dim_Bin_Def(DF, Variables_To_Combine, Smearing_Q="", Data_Type="rdf", return_option="DF"):
#     if(DF == "continue"):
#         return "continue"
#     if(list is not type(Variables_To_Combine) or len(Variables_To_Combine) <= 1):
#         print(f"{color.Error}ERROR IN Multi_Dim_Bin_Def...\nImproper information was provided to combine multidimensional bins\n{color.END_R}Must provide a list of variables to combine with the input parameter: 'Variables_To_Combine'{color.END}")
#         if(return_option == "DF"):
#             return DF
#         else:
#             return Variables_To_Combine
#     Vars_Data_Type_Output = [""] if((return_option != "DF_Res") or (Data_Type in ["rdf", "gdf"])) else ["" if("mear" not in Smearing_Q) else "_smeared", "_gen"]
#     var_name, var_mins, var_maxs, var_bins = zip(*Variables_To_Combine)
#     var_name, var_mins, var_maxs, var_bins = list(var_name), list(var_mins), list(var_maxs), list(var_bins)
#     for list_invert in [var_name, var_mins, var_maxs, var_bins]:
#         list_invert.reverse()
#     Multi_Dim_Bin_Title, combined_bin_formula = {}, {}
#     DF_Final = DF
#     for var_type in Vars_Data_Type_Output:
#         Multi_Dim_Bin_Title[var_type] = "Multi_Dim"
#         for ii, var in enumerate(var_name):
#             Multi_Dim_Bin_Title[var_type] += str("".join(["_", str(var).replace("_smeared", "")])).replace("_gen", "")
#             if(var_type not in str(var)):
#                 var_name[ii] = "".join([str(var), str(var_type)])
#             if(var_type in [""]):
#                 var_name[ii] = str((var).replace("_smeared", "")).replace("_gen", "")
#             else:
#                 var_name[ii] = str((var).replace("_smeared" if("gen" in str(var_type)) else "_gen", ""))
#                 if(Smearing_Q != ""):
#                     if(("_smeared" not in str(var_name[ii])) and ("_gen" not in str(var_name[ii]))):
#                         var_name[ii] = "".join([str(var_name[ii]), "_smeared"])
#             if((str(var_name[ii]) not in list(DF_Final.GetColumnNames())) and (str(var_name[ii]) not in DF_Final.GetColumnNames())):
#                 print(f"\n{color.RED}ERROR IN 'Multi_Dim_Bin_Def': Variable '{var_name[ii]}' is not in the DataFrame (check code for errors){color.END}")
#                 print(f"{color.RED}Available Variables include:\n{DF_Final.GetColumnNames()}{color.END}")
#                 for column_name in DF_Final.GetColumnNames():
#                     print(f"str(var_name[ii]) == str(column_name) --> {(str(var_name[ii]) == str(column_name))} {str(var_name[ii]) if(str(var_name[ii]) == str(column_name)) else ''}")

#         Multi_Dim_Bin_Title[var_type] += str(var_type)
#         combined_bin_formula[var_type] = f"int combined_bin{var_type} = "

#         for ii, var in enumerate(var_name):
#             if(combined_bin_formula[var_type]  != f"int combined_bin{var_type} = "):
#                 combined_bin_formula[var_type] += " + "
#             if("_Bin" not in str(var)):
#                 norm_var = "int(((({0}{1} - {2})/({3} - {2}))*{4}))".format(var, var_type, var_mins[ii], var_maxs[ii], var_bins[ii])
#             else:
#                 norm_var = f"{var}{var_type}"
#             var_bin_product = ""
#             for jj in range(ii + 1, len(var_name)):
#                 if(var_bins[jj] not in ["", 0]):
#                     var_bin_product += f"*{var_bins[jj]}"
#             combined_bin_formula[var_type] += "".join(["int({0}{1})"]).format(norm_var, var_bin_product)

#         combined_bin_formula[var_type] += """ + 1;
#         if("""
#         for ii, var in enumerate(var_name):
#             combined_bin_formula[var_type] += "".join([str(var), str(var_type), " < ", str(var_mins[ii]), " || ", str(var), str(var_type), " > ", str(var_maxs[ii])])
#             if(ii != (len(var_name) - 1)):
#                 combined_bin_formula[var_type] += " || "
#         combined_bin_formula[var_type]     += "".join(["""){combined_bin""", str(var_type), """ = -1;}
#         return combined_bin""", str(var_type), """;
#         """])

#         combined_bin_formula[var_type] = str(combined_bin_formula[var_type]).replace(" +  + ", " + ")
#         combined_bin_formula[var_type] = str(combined_bin_formula[var_type]).replace("_smeared_gen",     "_gen")
#         combined_bin_formula[var_type] = str(combined_bin_formula[var_type]).replace("_smeared_smeared", "_smeared")

#         if(return_option == "DF"):
#             try:
#                 DF_Final = DF_Final.Define(str(Multi_Dim_Bin_Title[var_type]), str(combined_bin_formula[var_type]))
#             except:
#                 print(f"\n{color.Error}ERROR IN FINAL STEP OF Multi_Dim_Bin_Def:\n{color.END_R}{traceback.format_exc()}{color.END}\n\n")

#         elif(return_option == "DF_Res"):
#             try:
#                 DF_Final = DF_Final.Define(str(Multi_Dim_Bin_Title[var_type]), str(combined_bin_formula[var_type]))
#             except:
#                 print(f"\n{color.Error}ERROR IN FINAL STEP OF Multi_Dim_Bin_Def:\n{color.END_R}{traceback.format_exc()}{color.END}\n\n")

#         else:
#             return [str(Multi_Dim_Bin_Title[var_type]), -1.5, (math.prod(var_bins)) + 1.5, (math.prod(var_bins)) + 3]
#     return DF_Final


def Bin_Number_Variable_Function(DF, Variable, min_range, max_range, number_of_bins, DF_Type="rdf"):
    if(str(Variable) in DF.GetColumnNames()): # Already defined
        return DF
    else:
        bin_size = (max_range - min_range)/number_of_bins
        rec_bin = f"""
int rec_bin = (({Variable} - {min_range})/{bin_size}) + 1;
if({Variable} < {min_range}){{ // Below binning range
    rec_bin = 0;
}}
if({Variable} > {max_range}){{ // Above binning range
    rec_bin = {number_of_bins + 1};
}}
return rec_bin;"""
        out_put_DF = DF.Define(f"{Variable}_REC_BIN", rec_bin)
        if(DF_Type not in ["rdf", "gdf"]):
            GEN_Variable = f'{Variable.replace("_smeared", "")}_gen'
            gen_bin = f"""
int gen_bin = (({GEN_Variable} - {min_range})/{bin_size}) + 1;
if({GEN_Variable} < {min_range}){{ // Below binning range
    gen_bin = 0;
}}
if({GEN_Variable} > {max_range}){{ // Above binning range
    gen_bin = {number_of_bins + 1};
}}
if(PID_el == 0 || PID_pip == 0){{ // Event is unmatched
    gen_bin = {number_of_bins + 2};
}}
return gen_bin;"""
            out_put_DF = out_put_DF.Define(f"{Variable}_GEN_BIN", gen_bin)
    return out_put_DF
    


def Dimension_Name_Function(Histo_Var_D1, Histo_Var_D2="None", Histo_Var_D3="None"):
    Dimensions_Output = "Variable_Error"
    try:
        Dimensions_Output = f"Var-D1:'{Histo_Var_D1[0]}'-[NumBins:{Histo_Var_D1[3]}, MinBin:{Histo_Var_D1[1]}, MaxBin:{Histo_Var_D1[2]}]"
        if(Histo_Var_D2  != "None"):
            Dimensions_Output = f"{Dimensions_Output}; Var-D2:'{Histo_Var_D2[0]}'-[NumBins:{Histo_Var_D2[3]}, MinBin:{Histo_Var_D2[1]}, MaxBin:{Histo_Var_D2[2]}]"
            if(Histo_Var_D3 != "None"):
                Dimensions_Output = f"{Dimensions_Output}; Var-D3:'{Histo_Var_D3[0]}'-[NumBins:{Histo_Var_D3[3]}, MinBin:{Histo_Var_D3[1]}, MaxBin:{Histo_Var_D3[2]}]"
        Dimensions_Output = (Dimensions_Output.replace(":", "=")).replace("; ", "), (")
    except:
        print(f"{color.Error}ERROR IN DIMENSIONS:\n{color.END_R}{traceback.format_exc()}{color.END}")
    return Dimensions_Output


# --- tiny helpers to keep single-call API clean (no line-wrapped calls) ---


# ---------- helpers required by make_rm5d_single / make_rm_single ----------

def is_scalar_or_multidim(variable_name):
    base = ["Q2", "xB", "z", "pT", "Q2_y_z_pT_4D_Bin", "y"]
    if(variable_name.replace("_smeared", "") in base):
        return True
    if(("Multi_Dim_" in variable_name) or ("MultiDim" in variable_name)):
        return True
    return False


def build_group_tags(Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Histo_Binning_str):
    Histo_Group_Name   = "".join(["Histo-Group:'",  str(Histo_Group), "'"])
    Histo_Data_Name    = "".join(["Data-Type:'",    str(Histo_Data),  "'"])
    Histo_Cut_Name     = "".join(["Data-Cut:'",     str(Histo_Cut),   "'"])
    Histo_Smear_Name   = "".join(["Smear-Type:'",   str(Histo_Smear), "'"])
    Histo_Binning_Name = Histo_Binning_str
    return Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name


def finalize_histo_name(parts, var_name_block):
    joined = f'(({"; ".join([parts[0], parts[1], parts[2], parts[3], parts[4], var_name_block])}))'
    return joined.replace("; )", ")").replace("; ", "), (").replace(":", "=")


def finalize_histo_name_1d(parts, var_name_block, Histo_Group):
    grp_1d = parts[0].replace(f"'{Histo_Group}'", f"'{Histo_Group}_1D'")
    joined = f'(({"; ".join([grp_1d, parts[1], parts[2], parts[3], parts[4], var_name_block])}))'
    return joined.replace("; )", ")").replace("; ", "), (").replace(":", "=")


def build_titles_5d(Histo_Group, Histo_Data, var_title, num_bins_text, custom_line=None):
    label = "Response Matrix" if(Histo_Data in ["mdf"]) else ("Experimental Distribution" if(Histo_Data == "rdf") else "Generated Distribution")
    if(("Background" in Histo_Group) and (Histo_Data in ["mdf"])):
        label = f"Background {label}"
    t1 = f"#scale[1.5]{{{label} of {var_title}}}"
    t3 = f"#scale[1.35]{{Number of Bins: {num_bins_text}}}"
    t4 = "All Q^{2}-y-z-P_{T} Bins"
    t2 = custom_line if(custom_line) else ''
    if(Histo_Data in ["mdf"]):
        base = f"#scale[1.5]{{(Background) Reconstructed (MC) Distribution of {var_title}}}" if("Background" in Histo_Group) else f"#scale[1.5]{{Reconstructed (MC) Distribution of {var_title}}}"
        t2 = f"#splitline{{#splitline{{#splitline{{{base}}}{{{t2}}}}}{{{t3}}}}}{{{t4}}}; {var_title} REC Bins"
    main = f"#splitline{{#splitline{{#splitline{{{t1}}}{{{t2}}}}}{{{t3}}}}}{{{t4}}}; {var_title} REC Bins"
    return main, t2


def build_titles_rm(Histo_Group, Histo_Data, variable_title, bin_text, Cut_Line, q2y_text, left_label, right_label, attach_zpt=False, mdf_title2=False, custom_line=None):
    if(Histo_Data in ["mdf"]):
        l1 = f"#scale[1.5]{{Background Response Matrix of {variable_title}}}" if(Histo_Group in ["Background_Response_Matrix"]) else f"#scale[1.5]{{Response Matrix of {variable_title}}}"
    else:
        l1 = f"#scale[1.5]{{{'Experimental' if(Histo_Data == 'rdf') else 'Generated'} Distribution of {variable_title}}}"
    l3   = f"#scale[1.35]{{{bin_text}}}"
    head = f"#splitline{{#splitline{{#splitline{{{l1}}}{{{Cut_Line}}}}}{{{l3}}}}}{{{q2y_text}}}"
    if(custom_line):
        head = f"#splitline{{{head}}}{{{custom_line}}}"
    axis = f"; {left_label}; {right_label}" if(not attach_zpt) else f"; {left_label}; {right_label}; z-P_{{T}} Bins"
    title = f"{head}{axis}"
    t2 = None
    if(mdf_title2 and (Histo_Data in ['mdf'])):
        t2 = f"#splitline{{#splitline{{#splitline{{#scale[1.5]{{Reconstructed (MC) Distribution of {variable_title}}}}}{{{Cut_Line}}}}}{{{l3}}}}}{{{q2y_text}}}"
        if(custom_line):
            t2 = f"#splitline{{{t2}}}{{{custom_line}}}"
        t2 = f"{t2}; {right_label}"
    return title, t2


def apply_background_filter(Histo_Data, Histo_Group, base_filter):
    Background_Cuts_MC = BG_Cut_Function(dataframe=Histo_Data)
    current_filter = base_filter
    if(str(Background_Cuts_MC) not in ["", "ERROR"]):
        if("Background" in Histo_Group):
            current_filter = f"({current_filter}) && ({Background_Cuts_MC})" if(current_filter not in [""]) else f"({Background_Cuts_MC})"
        else:
            current_filter = f"({current_filter}) && !({Background_Cuts_MC})" if(current_filter not in [""]) else f"!({Background_Cuts_MC})"
            if((Histo_Data not in ["rdf", "gdf"]) and ("PID" not in current_filter)):
                print(f"\n{color.Error}WARNING: {color.END_R}Even if PID is not being considered as background, unmatched events must always be removed to plot the TH2D/TH3D response matrices{color.END}")
                current_filter = f"({current_filter}) && (PID_el != 0 && PID_pip != 0)" if(current_filter not in [""]) else "(PID_el != 0 && PID_pip != 0)"
        if((Histo_Data in ["gdf"]) and ("MM_gen" in current_filter)):
            current_filter = str(current_filter).replace("MM_gen", "MM")
    elif(str(Background_Cuts_MC) in ["ERROR"]):
        print(f"\n\n{color.Error}ERROR IN BG_Cut_Function(dataframe={Histo_Data}).\n\t{color.END_R}Check ExtraAnalysisCodeValues.py for details{color.END}\n\n")
    return current_filter



def _filter_fieldnames(Histo_Smear):
    Q2_xB_Bin_Filter_str = "Q2_Y_Bin"
    z_pT_Bin_Filter_str  = "z_pT_Bin_Y_bin"
    if("smear" in Histo_Smear):
        Q2_xB_Bin_Filter_str = f"{Q2_xB_Bin_Filter_str}_smeared"
        z_pT_Bin_Filter_str  = f"{z_pT_Bin_Filter_str}_smeared"
    return Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str


def _guard_datatype_and_smear(Histo_Data, Histo_Smear):
    if((Histo_Data not in ["mdf"]) and ("smear" in Histo_Smear)):
        print(f"{color.Error}SKIP:{color.END_R} smearing is only valid for mdf; requested Data-Type='{Histo_Data}', Smear='{Histo_Smear}'{color.END}")
        return False
    return True


def _guard_gdf_cut(Histo_Data, Histo_Cut):
    if(Histo_Data != "gdf"):
        return True
    allowed = (["no_cut", "cut_Gen", "cut_Exgen", "no_cut_Integrate"] + [f"no_cut_eS{n}{s}" for n in range(1, 7) for s in ("a", "o")] + [f"no_cut_Integrate_eS{n}{s}" for n in range(1, 7) for s in ("a", "o")])
    if(Histo_Cut in allowed):
        return True
    print(f"{color.Error}SKIP:{color.END_R} cut '{Histo_Cut}' is not allowed for gdf{color.END}")
    return False


def _guard_rm_group_background(Histo_Group, Histo_Data):
    if((Histo_Group in ["Background_Response_Matrix", "Background_5D_Response_Matrix"]) and (Histo_Data != "mdf")):
        print(f"{color.Error}SKIP:{color.END_R} '{Histo_Group}' only valid for mdf; Data-Type='{Histo_Data}'{color.END}")
        return False
    return True


def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        tfile.Delete(f"{obj.GetName()};*")  # delete all versions of the object
    obj.Write()

def _write_and_tick(obj, key, file_location, output_type):
    if(key in obj):
        if((str(file_location) not in ["time"]) and (str(output_type) not in ["time"])):
            obj[key].Write()
    else:
        print(f"\n{color.Error}ERROR WHILE SAVING HISTOGRAM:\n{color.END_B} Histograms_All[{key}] was not found{color.END}\n")


# --- 5D Response Matrix: make exactly one request (single variable setup, one Histo_Group at a time) ---

def make_rm5d_single(sdf, Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Binning, Q2_y_z_pT_phi_h_5D_Binning, Use_Weight, Sliced_5D_Increment, Histograms_All, file_location, output_type):
    if(not _guard_datatype_and_smear(Histo_Data, Histo_Smear)):
        return Histograms_All
    if(("EDIS" in Histo_Cut)):
        return Histograms_All
    if(not _guard_rm_group_background(Histo_Group, Histo_Data)):
        return Histograms_All

    variable, Min_range, Max_range, Num_of_Bins = Q2_y_z_pT_phi_h_5D_Binning
    if(("smear" in Histo_Smear) and ("mear" not in variable)):
        variable = f"{variable}_smeared"
    var_title = variable_Title_name(variable)
    Histo_Var_RM_Name = Dimension_Name_Function(Histo_Var_D1=Q2_y_z_pT_phi_h_5D_Binning, Histo_Var_D2="None")

    Histo_Binning_Name = f"Binning-Type:'{Binning}'-[Q2-y-Bin:All, z-PT-Bin:All]"
    Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name = build_group_tags(Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Histo_Binning_Name)

    base_title, rec_title_mdf = build_titles_5d(Histo_Group, Histo_Data, var_title, Num_of_Bins)

    Histo_Name    = finalize_histo_name(   (Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name), Histo_Var_RM_Name)
    Histo_Name_1D = finalize_histo_name_1d((Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name), Histo_Var_RM_Name, Histo_Group)

    Variable_Gen = f"{variable.replace('_smeared', '')}_gen"
    Variable_Rec = variable

    base_filter = "esec != -2"
    Background_Filter = apply_background_filter(Histo_Data, Histo_Group, base_filter)

    if(Histo_Data not in ["rdf", "gdf"]):
        if("Background" not in Histo_Group):
            Start_Bin = Min_range
            Num_Slice = int(Num_of_Bins / Sliced_5D_Increment)
            for Slice in range(1, Num_Slice + 1):
                Histo_Name_Slice = f"{Histo_Name}_Slice_{Slice}_(Increment='{Sliced_5D_Increment}')"
                filt = f"{Background_Filter} && (({Variable_Rec} >= {Start_Bin}) && ({Variable_Rec} <= {Start_Bin + Sliced_5D_Increment}))"
                if(Use_Weight):
                    Histograms_All[Histo_Name_Slice] = sdf.Filter(filt).Histo2D((str(Histo_Name_Slice), str(base_title), Sliced_5D_Increment, Start_Bin, Start_Bin + Sliced_5D_Increment, int(Num_of_Bins), Min_range, Max_range), str(Variable_Rec), str(Variable_Gen), "Event_Weight")
                else:
                    Histograms_All[Histo_Name_Slice] = sdf.Filter(filt).Histo2D((str(Histo_Name_Slice), str(base_title), Sliced_5D_Increment, Start_Bin, Start_Bin + Sliced_5D_Increment, int(Num_of_Bins), Min_range, Max_range), str(Variable_Rec), str(Variable_Gen))
                Start_Bin += Sliced_5D_Increment
    if(Use_Weight):
        Histograms_All[Histo_Name_1D] = sdf.Filter(Background_Filter).Histo1D((str(Histo_Name_1D), str(rec_title_mdf) if((rec_title_mdf is not None) and (Histo_Data in ["mdf"])) else str(base_title), int(Num_of_Bins), Min_range, Max_range), str(Variable_Rec), "Event_Weight")
    else:
        Histograms_All[Histo_Name_1D] = sdf.Filter(Background_Filter).Histo1D((str(Histo_Name_1D), str(rec_title_mdf) if((rec_title_mdf is not None) and (Histo_Data in ["mdf"])) else str(base_title), int(Num_of_Bins), Min_range, Max_range), str(Variable_Rec))
        
    _write_and_tick(Histograms_All, Histo_Name_1D, file_location, output_type)
    # print(Histo_Name_1D)

    if((Histo_Data in ["mdf"]) and ("Background" not in Histo_Group)):
        Start_Bin = Min_range
        Num_Slice = int(Num_of_Bins/Sliced_5D_Increment)
        for Slice in range(1, Num_Slice + 1):
            Histo_Name_Slice = f"{Histo_Name}_Slice_{Slice}_(Increment='{Sliced_5D_Increment}')"
            _write_and_tick(Histograms_All, Histo_Name_Slice, file_location, output_type)
            # print(Histo_Name_Slice)
            Start_Bin += Sliced_5D_Increment

    return Histograms_All


# --- 1D/3D Response Matrix: make exactly one request for one variable and one Q2-y bin ---


def apply_weight_norm(df_in, bin_filter, use_weight=False, histo_data=None):
    # Only MC REC should ever be renormalized
    if((not use_weight) or (histo_data != "mdf")):
        return df_in.Filter(bin_filter)

    # Apply the cut first
    df_cut = df_in.Filter(bin_filter)

    # Check that weighting columns exist
    if((not df_cut.HasColumn("W_pre")) or (not df_cut.HasColumn("W_acc"))):
        return df_cut

    # Compute sums for normalization
    sum_pre = df_cut.Sum("W_pre").GetValue()
    if(not df_cut.HasColumn("Event_Weight_raw")):
        df_cut  = df_cut.Define("Event_Weight_raw", "W_pre * W_acc")
        sum_acc = df_cut.Sum("Event_Weight_raw").GetValue()
    else:
        sum_acc = df_cut.Sum("Event_Weight_raw").GetValue()

    # Safety check
    if(sum_acc == 0):
        print(f"{color.Error}WARNING: sum_acc == 0 inside apply_weight_norm() after cut:\n"
              f"    {bin_filter}\n"
              f"Skipping weight renormalization.{color.END}")
        return df_cut

    # Renormalization factor
    renorm = sum_pre / sum_acc

    # (Re)define Event_Weight with renormalization
    if(df_cut.HasColumn("Event_Weight")):
        df_cut = df_cut.Redefine("Event_Weight", f"(W_pre * W_acc) * ({renorm})")
    else:
        df_cut = df_cut.Define("Event_Weight",   f"(W_pre * W_acc) * ({renorm})")
        
    return df_cut



def make_rm_single(sdf, Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Binning, Var_Input, Q2_y_bin_num, Use_Weight, Histograms_All, file_location, output_type, Res_Binning_2D_z_pT=["z_pT_Bin_Y_bin", -0.5, 37.5, 38], custom_title=None):
    if(not _guard_datatype_and_smear(Histo_Data, Histo_Smear)):
        return Histograms_All
    if(not _guard_gdf_cut(Histo_Data, Histo_Cut)):
        return Histograms_All
    if(not _guard_rm_group_background(Histo_Group, Histo_Data)):
        return Histograms_All
    if(("EDIS" in Histo_Cut)):
        return Histograms_All

    if(len(Var_Input) == 4):
        Var_List = Var_Input[:]
    # else:
    #     Var_List = Multi_Dim_Bin_Def(DF=sdf, Variables_To_Combine=Var_Input, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="Bin")

    variable, Min_range, Max_range, Num_of_Bins = Var_List
    if(("smear" in Histo_Smear) and ("mear" not in variable)):
        variable = f"{variable}_smeared"
    if(("smear" in Histo_Smear) and ("mear" not in Res_Binning_2D_z_pT[0])):
        Res_Binning_2D_z_pT[0] = f"{Res_Binning_2D_z_pT[0]}_smeared"
    elif(("smear" not in Histo_Smear) and ("mear" in Res_Binning_2D_z_pT[0])):
        Res_Binning_2D_z_pT[0] = Res_Binning_2D_z_pT[0].replace("_smeared", "")
    BIN_SIZE   = round((Max_range - Min_range)/Num_of_Bins, 4)
    use_normal = (Histo_Group == "Response_Matrix_Normal")
    Bin_Range  = f"Number of Bins: {Num_of_Bins} - Range (from Bin 1-{Num_of_Bins}): {Min_range} #rightarrow {Max_range} - Size: {BIN_SIZE} per bin" if(not use_normal) else f"Range: {Min_range} #rightarrow {Max_range} - Size: {BIN_SIZE} per bin"

    Histo_Var_RM_Name = Dimension_Name_Function(Histo_Var_D1=Var_List, Histo_Var_D2=Res_Binning_2D_z_pT)

    sdf = Bin_Number_Variable_Function(sdf, Variable=variable, min_range=Min_range, max_range=Max_range, number_of_bins=Num_of_Bins, DF_Type=Histo_Data)
    # if(("Combined_" in variable) or ("Multi_Dim" in variable) or ("MultiDim" in variable)):
    #     sdf = Multi_Dim_Bin_Def(DF=sdf, Variables_To_Combine=Var_Input, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="DF_Res")
    if(sdf == "continue"):
        return # Histograms_All

    Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = _filter_fieldnames(Histo_Smear)
    if((Q2_y_bin_num > 0) and ((Q2_xB_Bin_Filter_str in variable) or (("Bin" in variable) and ("Multi_Dim_z_pT_Bin" not in variable) and ("MultiDim_z_pT_Bin" not in variable)))):
        return # Histograms_All

    Histo_Binning = [Binning, "All" if(Q2_y_bin_num == -1) else str(Q2_y_bin_num), "All"]
    Histo_Binning_Name = f"Binning-Type:'{Histo_Binning[0]}'-[Q2-y-Bin:{Histo_Binning[1]}, z-PT-Bin:{Histo_Binning[2]}]"
    Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name = build_group_tags(Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Histo_Binning_Name)

    Histo_Name    = finalize_histo_name((Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name), Histo_Var_RM_Name)
    Histo_Name_1D = finalize_histo_name_1d((Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name), Histo_Var_RM_Name, Histo_Group)

    Cut_Line_l2 = f"#scale[1.15]{{Cut: {Cut_Choice_Title(Cut_Type=Histo_Cut)}}}"
    Bin_Line_l4 = f"Q^{{2}}-y Bin: {Histo_Binning[1]}" if(Q2_y_bin_num > 0) else ""
    var_t = variable_Title_name(variable)
    if((Histo_Group    == "Response_Matrix") and (("Combined_" not in variable) and ("Multi_Dim" not in variable) and ("MultiDim" not in variable))):
        num_of_REC_bins, min_REC_bin, Max_REC_bin = (Num_of_Bins + 5), -1.5, (Num_of_Bins + 3.5)
        num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Num_of_Bins + 5), -1.5, (Num_of_Bins + 3.5)
        Variable_Gen    = f"{variable}_GEN_BIN" if("Bin" not in variable) else f"{variable.replace('_smeared','')}_gen"
        Variable_Rec    = f"{variable}_REC_BIN" if("Bin" not in variable) else variable
        title, title2   = build_titles_rm(Histo_Group, Histo_Data, variable_title=var_t, bin_text=Bin_Range, Cut_Line=Cut_Line_l2, q2y_text=Bin_Line_l4, left_label=f"{variable_Title_name(variable.replace('_smeared',''))} GEN Bins", right_label=f"{variable_Title_name(variable)} REC Bins", attach_zpt=False, mdf_title2=(Histo_Data == "mdf"), custom_line=custom_title)
    else:
        num_of_REC_bins, min_REC_bin, Max_REC_bin = Num_of_Bins, Min_range, Max_range
        num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = Num_of_Bins, Min_range, Max_range
        Variable_Gen    = f"{variable.replace('_smeared','')}_gen"
        Variable_Rec    = variable
        if(Histo_Data in ["mdf"]):
            left_label  = f"{variable_Title_name(variable.replace('_smeared',''))} GEN Bins" if(Histo_Group == "Response_Matrix") else f"{variable_Title_name(variable.replace('_smeared',''))} (GEN)"
            right_label = f"{variable_Title_name(variable)} REC Bins" if(Histo_Group == "Response_Matrix") else f"{variable_Title_name(variable)} (REC)"
        else:
            left_label  = f"{variable_Title_name(variable)}"
            right_label = "REC Bins" if("g" not in Histo_Data) else "GEN Bins"
        attach_zpt_axis = (Histo_Group != "Response_Matrix") and (not is_scalar_or_multidim(variable) if(True) else False)
        title, title2   = build_titles_rm(Histo_Group, Histo_Data, variable_title=var_t, bin_text=Bin_Range, Cut_Line=Cut_Line_l2, q2y_text=Bin_Line_l4, left_label=left_label, right_label=right_label, attach_zpt=attach_zpt_axis, mdf_title2=(Histo_Data == "mdf"), custom_line=custom_title)

    Bin_Filter = "esec != -2" if(Q2_y_bin_num == -1) else f"{Q2_xB_Bin_Filter_str} != 0" if(Q2_y_bin_num == -2) else f"{Q2_xB_Bin_Filter_str} == {Q2_y_bin_num}"
    if((Histo_Data in ["mdf", "gdf"]) and (("Combined" in variable) or ("Multi_Dim" in variable) or ("MultiDim" in variable)) and (Q2_xB_Bin_Filter_str.replace("_smeared","") in variable)):
        eq = f"{z_pT_Bin_Filter_str} == {z_pT_Bin_Filter_str.replace('_smeared','')}_gen"
        Bin_Filter = f"({Bin_Filter}) && ({eq})" if(Bin_Filter != "esec != -2") else eq
    if((("Combined" in variable) or ("Multi_Dim" in variable) or ("MultiDim" in variable)) and (Q2_xB_Bin_Filter_str.replace("_smeared","") in variable)):
        extra = f"{Q2_xB_Bin_Filter_str.replace('_smeared','').replace('_gen','')}_gen != 0" if(Histo_Data in ["mdf", "gdf"]) else ""
        Bin_Filter = "".join([f"({Bin_Filter}) && ({Q2_xB_Bin_Filter_str} != 0", f" && {extra})" if(extra != "" ) else ")"])

    if(Use_Weight):
        Histo_Name_Weighed = f"{Histo_Name}_(Weighed)"
        Histo_Name_1D_Weighed = f"{Histo_Name_1D}_(Weighed)"
    else:
        Histo_Name_Weighed, Histo_Name_1D_Weighed = None, None

    Bin_Filter = apply_background_filter(Histo_Data, Histo_Group, Bin_Filter)
    sdf_cut    = apply_weight_norm(df_in=sdf, bin_filter=Bin_Filter, use_weight=Use_Weight, histo_data=Histo_Data)
    if(Histo_Data in ["mdf"]):
        if(is_scalar_or_multidim(variable)):
            if(Use_Weight):
                Histograms_All[Histo_Name_Weighed]        = sdf_cut.Histo2D((str(Histo_Name_Weighed),    str(title),  int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Gen), str(Variable_Rec), "Event_Weight")
            Histograms_All[Histo_Name]                    = sdf_cut.Histo2D((str(Histo_Name),            str(title),  int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Gen), str(Variable_Rec))
            if(title2 is not None):
                if(Use_Weight):
                    Histograms_All[Histo_Name_1D_Weighed] = sdf_cut.Histo1D((str(Histo_Name_1D_Weighed), str(title2), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec), "Event_Weight")
                Histograms_All[Histo_Name_1D]             = sdf_cut.Histo1D((str(Histo_Name_1D),         str(title2), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec))
        else:
            if(Use_Weight):
                Histograms_All[Histo_Name_Weighed]        = sdf_cut.Histo3D((str(Histo_Name_Weighed),    str(title), int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Gen),      str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
                Histograms_All[Histo_Name_1D_Weighed]     = sdf_cut.Histo2D((str(Histo_Name_1D_Weighed), str(title).replace("; " + variable_Title_name(Res_Binning_2D_z_pT[0]), "; Counts"), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
            Histograms_All[Histo_Name]                    = sdf_cut.Histo3D((str(Histo_Name),            str(title), int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Gen),      str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
            Histograms_All[Histo_Name_1D]                 = sdf_cut.Histo2D((str(Histo_Name_1D),         str(title).replace("; " + variable_Title_name(Res_Binning_2D_z_pT[0]), "; Counts"), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
    else:
        if(is_scalar_or_multidim(variable)):
            if(Use_Weight):
                Histograms_All[Histo_Name_1D_Weighed]     = sdf_cut.Histo1D((str(Histo_Name_1D_Weighed), str(title).replace("; " + variable_Title_name(Res_Binning_2D_z_pT[0]), ""), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec), "Event_Weight")
            Histograms_All[Histo_Name_1D]                 = sdf_cut.Histo1D((str(Histo_Name_1D),         str(title).replace("; " + variable_Title_name(Res_Binning_2D_z_pT[0]), ""), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec))
        else:
            if(Use_Weight):
                Histograms_All[Histo_Name_1D_Weighed]     = sdf_cut.Histo2D((str(Histo_Name_1D_Weighed), str(title), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
            Histograms_All[Histo_Name_1D]                 = sdf_cut.Histo2D((str(Histo_Name_1D),         str(title), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))

    targets = []
    if(Histo_Name in Histograms_All):
        targets.append(Histo_Name)
    if(Histo_Name_1D in Histograms_All):
        targets.append(Histo_Name_1D)
    if(Histo_Name_Weighed in Histograms_All):
        targets.append(Histo_Name_Weighed)
        Histograms_All[Histo_Name_Weighed].SetTitle(f"#splitline{{{Histograms_All[Histo_Name_Weighed].GetTitle()}}}{{Weighted}}")
    if(Histo_Name_1D_Weighed in Histograms_All):
        targets.append(Histo_Name_1D_Weighed)
        Histograms_All[Histo_Name_1D_Weighed].SetTitle(f"#splitline{{{Histograms_All[Histo_Name_1D_Weighed].GetTitle()}}}{{Weighted}}")
    for key in targets:
        # _write_and_tick(Histograms_All, key, file_location, output_type)
        safe_write(obj=Histograms_All[key], tfile=file_location)
    # return Histograms_All


def Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="3D"):
    if(str(Variable_Type) not in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared", "GEN", "Gen", "gen", "_GEN", "_Gen", "_gen", "", "norm", "normal", "default"]):
        print(f"The input: {color.RED}{Variable_Type}{color.END} was not recognized by the function Multi_Bin_Standard_Def_Function(Variable_Type='{Variable_Type}').\nFix input to use anything other than the default calculations of z and pT.")
        Variable_Type  = ""
        
    Q2_xB_Bin_event_name = "".join(["Q2_Y_Bin",       "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])
    z_pT_Bin_event_name  = "".join(["z_pT_Bin_Y_bin", "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else ""])

    z_pT_Bin_Standard_Def = "".join([str(New_z_pT_and_MultiDim_Binning_Code), """
double z_event_val  =  z""", "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
double pT_event_val = pT""", "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """;
int z_pT_Bin_event_val = 0;
int Phih_Bin_event_val = 0;
int MultiDim3D_Bin_val = 0;
int MultiDim5D_Bin_val = 0;
if(""", Q2_xB_Bin_event_name, """ != 0){
    z_pT_Bin_event_val = Find_z_pT_Bin(""",           str(Q2_xB_Bin_event_name), """, z_event_val, pT_event_val);
    if(z_pT_Bin_event_val == 0){
        MultiDim3D_Bin_val = 0;
        MultiDim5D_Bin_val = 0;
    }
    else{
        if(Phi_h_Bin_Values[""",                      str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][0] == 1){Phih_Bin_event_val = 1;}
        else{Phih_Bin_event_val = Find_phi_h_Bin(""", str(Q2_xB_Bin_event_name), """, z_pT_Bin_event_val, phi_t""", "_smeared" if(str(Variable_Type) in ["smear", "smeared", "_smeared", "Smear", "Smeared", "_Smeared"]) else "_gen" if(str(Variable_Type) in ["GEN", "Gen", "gen", "_GEN", "_Gen", "_gen"]) else "", """);}
        MultiDim3D_Bin_val = Phi_h_Bin_Values[""",    str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][1] + Phih_Bin_event_val;
        MultiDim5D_Bin_val = Phi_h_Bin_Values[""",    str(Q2_xB_Bin_event_name), """][z_pT_Bin_event_val][2] + Phih_Bin_event_val;
    }
}
else{
    z_pT_Bin_event_val = 0;
    MultiDim3D_Bin_val = 0;
    MultiDim5D_Bin_val = 0;
}
""", f"""
// Refinement of Migration/Overflow Bins
if((({Q2_xB_Bin_event_name} == 1) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 2) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 3) && ((z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 4) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 5) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 6) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 7) && ((z_pT_Bin_event_val == 6) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 8) && ((z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 9) && ((z_pT_Bin_event_val == 21) || (z_pT_Bin_event_val == 27) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 33) || (z_pT_Bin_event_val == 34) || (z_pT_Bin_event_val == 35))) || (({Q2_xB_Bin_event_name} == 10) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 11) && ((z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 12) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 13) && ((z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 14) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 30) || (z_pT_Bin_event_val == 35) || (z_pT_Bin_event_val == 36))) || (({Q2_xB_Bin_event_name} == 15) && ((z_pT_Bin_event_val == 5) || (z_pT_Bin_event_val == 20) || (z_pT_Bin_event_val == 25))) || (({Q2_xB_Bin_event_name} == 16) && ((z_pT_Bin_event_val == 18) || (z_pT_Bin_event_val == 23) || (z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 28) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30))) || (({Q2_xB_Bin_event_name} == 17) && ((z_pT_Bin_event_val == 24) || (z_pT_Bin_event_val == 29) || (z_pT_Bin_event_val == 30)))){{
    z_pT_Bin_event_val = 0;
    MultiDim3D_Bin_val = 0;
    MultiDim5D_Bin_val = 0;
}}
// std::vector<int> z_pT_and_MultiDim_Bins = {{z_pT_Bin_event_val, MultiDim3D_Bin_val, MultiDim5D_Bin_val}};
// return z_pT_and_MultiDim_Bins;""", """
return MultiDim3D_Bin_val;
""" if(Dimension in ["3D"]) else """
return MultiDim5D_Bin_val;
""" if(Dimension in ["5D"]) else """
return z_pT_Bin_event_val;
"""])
    
    return z_pT_Bin_Standard_Def


if(__name__ == "__main__"):
    def make_rm_single_test(sdf, Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Binning, Var_Input, Q2_y_bin_num, Use_Weight, Histograms_All, file_location, output_type, Res_Binning_2D_z_pT=["z_pT_Bin_Y_bin", -1.5, 50.5, 52], custom_title=None):
        if(not _guard_datatype_and_smear(Histo_Data, Histo_Smear)):
            return Histograms_All
        if(not _guard_gdf_cut(Histo_Data, Histo_Cut)):
            return Histograms_All
        if(not _guard_rm_group_background(Histo_Group, Histo_Data)):
            return Histograms_All
        if(("EDIS" in Histo_Cut)):
            return Histograms_All
    
        if(len(Var_Input) == 4):
            Var_List = Var_Input[:]
        # else:
        #     Var_List = Multi_Dim_Bin_Def(DF=sdf, Variables_To_Combine=Var_Input, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="Bin")
    
        variable, Min_range, Max_range, Num_of_Bins = Var_List
        if(("smear" in Histo_Smear) and ("mear" not in variable)):
            variable = f"{variable}_smeared"
        if(("smear" in Histo_Smear) and ("mear" not in Res_Binning_2D_z_pT[0])):
            Res_Binning_2D_z_pT[0] = f"{Res_Binning_2D_z_pT[0]}_smeared"
        elif(("smear" not in Histo_Smear) and ("mear" in Res_Binning_2D_z_pT[0])):
            Res_Binning_2D_z_pT[0] = Res_Binning_2D_z_pT[0].replace("_smeared", "")
        
        BIN_SIZE   = round((Max_range - Min_range)/Num_of_Bins, 4)
        use_normal = (Histo_Group == "Response_Matrix_Normal")
        Bin_Range  = f"Number of Bins: {Num_of_Bins} - Range (from Bin 1-{Num_of_Bins}): {Min_range} #rightarrow {Max_range} - Size: {BIN_SIZE} per bin" if(not use_normal) else f"Range: {Min_range} #rightarrow {Max_range} - Size: {BIN_SIZE} per bin"
    
        Histo_Var_RM_Name = Dimension_Name_Function(Histo_Var_D1=Var_List, Histo_Var_D2=Res_Binning_2D_z_pT)
    
        # sdf = Bin_Number_Variable_Function(sdf, Variable=variable, min_range=Min_range, max_range=Max_range, number_of_bins=Num_of_Bins, DF_Type=Histo_Data)
        # if(("Combined_" in variable) or ("Multi_Dim" in variable) or ("MultiDim" in variable)):
        #     sdf = Multi_Dim_Bin_Def(DF=sdf, Variables_To_Combine=Var_Input, Smearing_Q=Histo_Smear, Data_Type=Histo_Data, return_option="DF_Res")
        # if(sdf == "continue"):
        #     return Histograms_All
    
        Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = _filter_fieldnames(Histo_Smear)
        if((Q2_y_bin_num > 0) and ((Q2_xB_Bin_Filter_str in variable) or (("Bin" in variable) and ("Multi_Dim_z_pT_Bin" not in variable) and ("MultiDim_z_pT_Bin" not in variable)))):
            return Histograms_All
    
        Histo_Binning = [Binning, "All" if(Q2_y_bin_num == -1) else str(Q2_y_bin_num), "All"]
        Histo_Binning_Name = f"Binning-Type:'{Histo_Binning[0]}'-[Q2-y-Bin:{Histo_Binning[1]}, z-PT-Bin:{Histo_Binning[2]}]"
        Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name = build_group_tags(Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Histo_Binning_Name)
    
        Histo_Name    = finalize_histo_name((Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name), Histo_Var_RM_Name)
        Histo_Name_1D = finalize_histo_name_1d((Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name), Histo_Var_RM_Name, Histo_Group)
    
        Cut_Line_l2 = f"#scale[1.15]{{Cut: {Cut_Choice_Title(Cut_Type=Histo_Cut)}}}"
        Bin_Line_l4 = f"Q^{{2}}-y Bin: {Histo_Binning[1]}" if(Q2_y_bin_num > 0) else ""
        var_t = variable_Title_name(variable)
        if((Histo_Group    == "Response_Matrix") and (("Combined_" not in variable) and ("Multi_Dim" not in variable) and ("MultiDim" not in variable))):
            num_of_REC_bins, min_REC_bin, Max_REC_bin = (Num_of_Bins + 5), -1.5, (Num_of_Bins + 3.5)
            num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = (Num_of_Bins + 5), -1.5, (Num_of_Bins + 3.5)
            Variable_Gen    = f"{variable}_GEN_BIN" if("Bin" not in variable) else f"{variable.replace('_smeared','')}_gen"
            Variable_Rec    = f"{variable}_REC_BIN" if("Bin" not in variable) else variable
            title, title2   = build_titles_rm(Histo_Group, Histo_Data, variable_title=var_t, bin_text=Bin_Range, Cut_Line=Cut_Line_l2, q2y_text=Bin_Line_l4, left_label=f"{variable_Title_name(variable.replace('_smeared',''))} GEN Bins", right_label=f"{variable_Title_name(variable)} REC Bins", attach_zpt=False, mdf_title2=(Histo_Data == "mdf"), custom_line=custom_title)
        else:
            num_of_REC_bins, min_REC_bin, Max_REC_bin = Num_of_Bins, Min_range, Max_range
            num_of_GEN_bins, min_GEN_bin, Max_GEN_bin = Num_of_Bins, Min_range, Max_range
            Variable_Gen    = f"{variable.replace('_smeared','')}_gen"
            Variable_Rec    = variable
            if(Histo_Data in ["mdf"]):
                left_label  = f"{variable_Title_name(variable.replace('_smeared',''))} GEN Bins" if(Histo_Group == "Response_Matrix") else f"{variable_Title_name(variable.replace('_smeared',''))} (GEN)"
                right_label = f"{variable_Title_name(variable)} REC Bins" if(Histo_Group == "Response_Matrix") else f"{variable_Title_name(variable)} (REC)"
            else:
                left_label  = f"{variable_Title_name(variable)}"
                right_label = "REC Bins" if("g" not in Histo_Data) else "GEN Bins"
            attach_zpt_axis = (Histo_Group != "Response_Matrix") and (not is_scalar_or_multidim(variable) if(True) else False)
            title, title2   = build_titles_rm(Histo_Group, Histo_Data, variable_title=var_t, bin_text=Bin_Range, Cut_Line=Cut_Line_l2, q2y_text=Bin_Line_l4, left_label=left_label, right_label=right_label, attach_zpt=attach_zpt_axis, mdf_title2=(Histo_Data == "mdf"), custom_line=custom_title)
    
        Bin_Filter = "esec != -2" if(Q2_y_bin_num == -1) else f"{Q2_xB_Bin_Filter_str} != 0" if(Q2_y_bin_num == -2) else f"{Q2_xB_Bin_Filter_str} == {Q2_y_bin_num}"
        if((Histo_Data in ["mdf", "gdf"]) and (("Combined" in variable) or ("Multi_Dim" in variable) or ("MultiDim" in variable)) and (Q2_xB_Bin_Filter_str.replace("_smeared","") in variable)):
            eq = f"{z_pT_Bin_Filter_str} == {z_pT_Bin_Filter_str.replace('_smeared','')}_gen"
            Bin_Filter = f"({Bin_Filter}) && ({eq})" if(Bin_Filter != "esec != -2") else eq
        if((("Combined" in variable) or ("Multi_Dim" in variable) or ("MultiDim" in variable)) and (Q2_xB_Bin_Filter_str.replace("_smeared","") in variable)):
            extra = f"{Q2_xB_Bin_Filter_str.replace('_smeared','').replace('_gen','')}_gen != 0" if(Histo_Data in ["mdf", "gdf"]) else ""
            Bin_Filter = "".join([f"({Bin_Filter}) && ({Q2_xB_Bin_Filter_str} != 0", f" && {extra})" if(extra != "" ) else ")"])
    
        if(Use_Weight):
            Histo_Name_Weighed = f"{Histo_Name}_(Weighed)"
            Histo_Name_1D_Weighed = f"{Histo_Name_1D}_(Weighed)"
        else:
            Histo_Name_Weighed, Histo_Name_1D_Weighed = None, None
    
        Bin_Filter = apply_background_filter(Histo_Data, Histo_Group, Bin_Filter)
        # if(Histo_Data in ["mdf"]):
        #     if(is_scalar_or_multidim(variable)):
        #         if(Use_Weight):
        #             Histograms_All[Histo_Name_Weighed]        = sdf.Filter(Bin_Filter).Histo2D((str(Histo_Name_Weighed),    str(title),  int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Gen), str(Variable_Rec), "Event_Weight")
        #         Histograms_All[Histo_Name]                    = sdf.Filter(Bin_Filter).Histo2D((str(Histo_Name),            str(title),  int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Gen), str(Variable_Rec))
        #         if(title2 is not None):
        #             if(Use_Weight):
        #                 Histograms_All[Histo_Name_1D_Weighed] = sdf.Filter(Bin_Filter).Histo1D((str(Histo_Name_1D_Weighed), str(title2), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec), "Event_Weight")
        #             Histograms_All[Histo_Name_1D]             = sdf.Filter(Bin_Filter).Histo1D((str(Histo_Name_1D),         str(title2), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec))
        #     else:
        #         if(Use_Weight):
        #             Histograms_All[Histo_Name_Weighed]        = sdf.Filter(Bin_Filter).Histo3D((str(Histo_Name_Weighed),    str(title), int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
        #             Histograms_All[Histo_Name_1D_Weighed]     = sdf.Filter(Bin_Filter).Histo2D((str(Histo_Name_1D_Weighed), str(title).replace("; " + variable_Title_name(Res_Binning_2D_z_pT[0]), "; Counts"), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
        #         Histograms_All[Histo_Name]                    = sdf.Filter(Bin_Filter).Histo3D((str(Histo_Name),            str(title), int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Gen), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
        #         Histograms_All[Histo_Name_1D]                 = sdf.Filter(Bin_Filter).Histo2D((str(Histo_Name_1D),         str(title).replace("; " + variable_Title_name(Res_Binning_2D_z_pT[0]), "; Counts"), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
        # else:
        #     if(is_scalar_or_multidim(variable)):
        #         if(Use_Weight):
        #             Histograms_All[Histo_Name_1D_Weighed]     = sdf.Filter(Bin_Filter).Histo1D((str(Histo_Name_1D_Weighed), str(title).replace("; " + variable_Title_name(Res_Binning_2D_z_pT[0]), ""), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec), "Event_Weight")
        #         Histograms_All[Histo_Name_1D]                 = sdf.Filter(Bin_Filter).Histo1D((str(Histo_Name_1D),         str(title).replace("; " + variable_Title_name(Res_Binning_2D_z_pT[0]), ""), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec))
        #     else:
        #         if(Use_Weight):
        #             Histograms_All[Histo_Name_1D_Weighed]     = sdf.Filter(Bin_Filter).Histo2D((str(Histo_Name_1D_Weighed), str(title), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
        #         Histograms_All[Histo_Name_1D]                 = sdf.Filter(Bin_Filter).Histo2D((str(Histo_Name_1D),         str(title), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))

        print("")
        print(f"title                 = {title}\n")
        print(f"Bin_Filter            = {Bin_Filter}\n")
        print(f"\nHisto_Name            =\n{Histo_Name}")
        # print("((Histo-Group='Response_Matrix_Normal'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type='smear'), (Binning-Type='Y_bin'-[Q2-y-Bin=1, z-PT-Bin=All]), (Var-D1='MultiDim_z_pT_Bin_Y_bin_phi_t'-[NumBins=915, MinBin=-1.5, MaxBin=913.5]), (Var-D2='z_pT_Bin_Y_bin_smeared'-[NumBins=38, MinBin=-0.5, MaxBin=37.5]))")
        print(f"\nHisto_Name_1D         =\n{Histo_Name_1D}")
        print(f"\nHisto_Name_Weighed    =\n{Histo_Name_Weighed}")
        print(f"\nHisto_Name_1D_Weighed =\n{Histo_Name_1D_Weighed}")
        if(is_scalar_or_multidim(variable)):
            print(f"""
Histograms_All["{Histo_Name}"] = 
    sdf.Filter("{Bin_Filter}").Histo2D((str(Histo_Name), "{title}", int({num_of_GEN_bins}), {min_GEN_bin}, {Max_GEN_bin}, int({num_of_REC_bins}), {min_REC_bin}, {Max_REC_bin}), "{Variable_Gen}", "{Variable_Rec}")""")
        else:
            print(f"""
Histograms_All["{Histo_Name}"] = 
    sdf.Filter("{Bin_Filter}").Histo3D((str(Histo_Name), "{title}", int({num_of_GEN_bins}), {min_GEN_bin}, {Max_GEN_bin}, int({num_of_REC_bins}), {min_REC_bin}, {Max_REC_bin}, int({Res_Binning_2D_z_pT[3]}), {Res_Binning_2D_z_pT[1]}, {Res_Binning_2D_z_pT[2]}), "{Variable_Gen}", "{Variable_Rec}", "{Res_Binning_2D_z_pT[0]}")""")
        print("")
        # targets = []
        # if(Histo_Name in Histograms_All):
        #     targets.append(Histo_Name)
        # if(Histo_Name_1D in Histograms_All):
        #     targets.append(Histo_Name_1D)
        # if(Histo_Name_Weighed in Histograms_All):
        #     targets.append(Histo_Name_Weighed)
        # if(Histo_Name_1D_Weighed in Histograms_All):
        #     targets.append(Histo_Name_1D_Weighed)
        # for key in targets:
        #     # print(key)
        #     _write_and_tick(Histograms_All, key, file_location, output_type)
    
        # return Histograms_All

    script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
    sys.path.append(script_dir)
    from MyCommonAnalysisFunction_richcap import variable_Title_name
    # from MyCommonAnalysisFunction_richcap import color
    # from ExtraAnalysisCodeValues import New_z_pT_and_MultiDim_Binning_Code
    sys.path.remove(script_dir)
    del script_dir
    Res_Binning_2D_z_pT_In = ["z_pT_Bin_Y_bin_smeared", -0.5, 37.5, 38]
    z_pT_phi_h_Binning     = ['MultiDim_z_pT_Bin_Y_bin_phi_t', -1.5, 913.5, 915]
    z_pT_phi_h_Binning     = ['phi_t', 0, 360, 24]
    # z_pT_phi_h_Binning     = ['Q2',    0,    14, 280]
    z_pT_phi_h_Binning     = ['xB', 0.09, 0.826,  50]
    # z_pT_phi_h_Binning     = ['y',     0,   1.0, 100]
    # z_pT_phi_h_Binning     = ['z',     0,   1.2, 120]
    # z_pT_phi_h_Binning     = ['pT',    0,   2.0, 200]
    # make_rm_single_test(sdf=None, Histo_Group="Response_Matrix_Normal", Histo_Data="mdf", Histo_Cut="cut_Complete_SIDIS", Histo_Smear="smear", Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=1, Use_Weight=False, Histograms_All=[], file_location=None, output_type=None, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=None)
    make_rm_single_test(sdf=None, Histo_Group="Response_Matrix_Normal", Histo_Data="rdf", Histo_Cut="cut_Complete_SIDIS", Histo_Smear="", Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=-1, Use_Weight=False, Histograms_All=[], file_location=None, output_type=None, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=None)
    # make_rm_single_test(sdf=None, Histo_Group="Response_Matrix_Normal", Histo_Data="mdf", Histo_Cut="cut_Complete_SIDIS", Histo_Smear="smear", Binning="Y_bin", Var_Input=z_pT_phi_h_Binning, Q2_y_bin_num=-1, Use_Weight=True, Histograms_All=[], file_location=None, output_type=None, Res_Binning_2D_z_pT=Res_Binning_2D_z_pT_In, custom_title=None)

