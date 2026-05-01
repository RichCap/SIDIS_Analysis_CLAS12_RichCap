#!/usr/bin/env python3

import ROOT
import sys
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, root_color, variable_Title_name
from ExtraAnalysisCodeValues          import New_z_pT_and_MultiDim_Binning_Code
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

def Cut_Flag_to_Title(cut_flag="no_cut"):
    if((cut_flag is None) or (str(cut_flag).strip() == "")):
        return ""
    cut_flag_str = str(cut_flag).strip()
    cut_title_map = {
        "no_cut"                              : "No Cuts",
        "cut_Complete_SIDIS"                  : "Default SIDIS Cuts",
        "cut_Complete_SIDIS_MM_loose"         : "Missing Mass > 1.25 GeV (Loose)",
        "cut_Complete_SIDIS_MM_tight"         : "Missing Mass > 1.75 GeV (Tight)",

        "cut_Complete_SIDIS_chi2_strict_pip"  : "Strict Pion #chi^{2} Cut",

        "cut_Complete_SIDIS_dcfid_loose_el"   : "Loose Electron DC Fiducial",
        "cut_Complete_SIDIS_dcfid_tight_el"   : "Tight Electron DC Fiducial",
        "cut_Complete_SIDIS_dcfid_pass1_el"   : "Pass 1 Electron DC Fiducial",

        "cut_Complete_SIDIS_dcfid_loose_pip"  : "Loose Pion DC Fiducial",
        "cut_Complete_SIDIS_dcfid_tight_pip"  : "Tight Pion DC Fiducial",
        "cut_Complete_SIDIS_dcfid_pass1_pip"  : "Pass 1 Pion DC Fiducial",

        "cut_Complete_SIDIS_dcfidref_loose_el": "Loose Electron DC Refinement",
        "cut_Complete_SIDIS_dcfidref_tight_el": "Tight Electron DC Refinement",

        "cut_Complete_SIDIS_dcv_loose_el"     : "Loose Electron DC Vertex",
        "cut_Complete_SIDIS_dcv_tight_el"     : "Tight Electron DC Vertex",
        "cut_Complete_SIDIS_dcv_pass1_el"     : "Pass 1 Electron DC Vertex",

        "cut_Complete_SIDIS_dvz_loose_pip"    : "Loose Pion #Delta V_{z}",
        "cut_Complete_SIDIS_dvz_tight_pip"    : "Tight Pion #Delta V_{z}",
        "cut_Complete_SIDIS_dvz_pass1_pip"    : "Pass 1 Pion #Delta V_{z}",

        "cut_Complete_SIDIS_ecband_loose_el"  : "Loose EC Sampling Band (Electron)",
        "cut_Complete_SIDIS_ecband_tight_el"  : "Tight EC Sampling Band (Electron)",

        "cut_Complete_SIDIS_ecthr_loose_el"   : "Loose EC Sampling Threshold (Electron)",
        "cut_Complete_SIDIS_ecthr_tight_el"   : "Tight EC Sampling Threshold (Electron)",

        "cut_Complete_SIDIS_ecoi_pass1_el"    : "Pass 1 EC Outer vs Inner (Electron)",
        "cut_Complete_SIDIS_ectri_pass1_el"   : "Pass 1 EC Sampling Triangle (Electron)",

        "cut_Complete_SIDIS_pid_full_pass1"   : "Full Pass 1 PID Cuts",

        "cut_Complete_SIDIS_noSmear"          : "Unsmeared SIDIS Cuts",

        "cut_Complete_SIDIS_no_pip_testdc"    : "No Pion Test DC Cut",
        "cut_Complete_SIDIS_no_sector_pcal"   : "No Sector PCal Cut",
        "cut_Complete_SIDIS_no_valerii_knockout": "No Valerii Knockout Cut",

        "cut_Complete_SIDIS_pcalvol_loose"    : "Loose PCal Volume Cut",
        "cut_Complete_SIDIS_pcalvol_tight"    : "Tight PCal Volume Cut",

        "cut_Complete_SIDIS_eS1o"             : "Electron Sector 1 Only",
        "cut_Complete_SIDIS_eS2o"             : "Electron Sector 2 Only",
        "cut_Complete_SIDIS_eS3o"             : "Electron Sector 3 Only",
        "cut_Complete_SIDIS_eS4o"             : "Electron Sector 4 Only",
        "cut_Complete_SIDIS_eS5o"             : "Electron Sector 5 Only",
        "cut_Complete_SIDIS_eS6o"             : "Electron Sector 6 Only",

        "cut_Complete_SIDIS_pipS1o"           : "Pion Sector 1 Only",
        "cut_Complete_SIDIS_pipS2o"           : "Pion Sector 2 Only",
        "cut_Complete_SIDIS_pipS3o"           : "Pion Sector 3 Only",
        "cut_Complete_SIDIS_pipS4o"           : "Pion Sector 4 Only",
        "cut_Complete_SIDIS_pipS5o"           : "Pion Sector 5 Only",
        "cut_Complete_SIDIS_pipS6o"           : "Pion Sector 6 Only",
    }
    if(cut_flag_str in cut_title_map):
        return cut_title_map[cut_flag_str] if(cut_flag_str in ["cut_Complete_SIDIS", "no_cut"]) else f"Cut Variation #topbar {cut_title_map[cut_flag_str]}"
    else:
        old_title = Cut_Choice_Title(Cut_Type=cut_flag_str)
    if("Undefined Cut (ERROR)" in old_title):
        return old_title.replace("ERROR", cut_flag_str)
    else:
        return old_title

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


def build_titles_5d(Histo_Group, Histo_Data, var_title, num_bins_text, custom_line=None, Ver="Y_Bin"):
    label = "Response Matrix" if(Histo_Data in ["mdf"]) else ("Experimental Distribution" if(Histo_Data == "rdf") else "Generated Distribution")
    if(("Background" in Histo_Group) and (Histo_Data in ["mdf"])):
        label = f"Background {label}"
    t1 = f"#scale[1.5]{{{label} of {var_title}}}"
    t3 = f"#scale[1.35]{{Number of Bins: {num_bins_text}}}"
    t4 = "All Q^{2}-y-z-P_{T}-#phi_{h} Bins" if("Valerii" not in Ver) else "All Q^{2}-x_{B}-z-P_{T}-#phi_{h} Bins"
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



def _filter_fieldnames(Histo_Smear, Ver="Y_bin"):
    Q2_xB_Bin_Filter_str = "Q2_Y_Bin"       if("Valerii" not in str(Ver)) else "Q2_xB_Bin_Valerii"
    z_pT_Bin_Filter_str  = "z_pT_Bin_Y_bin" if("Valerii" not in str(Ver)) else "z_pT_Bin_Valerii"
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

# def make_rm5d_single(sdf, Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Binning, Q2_y_z_pT_phi_h_5D_Binning, Use_Weight, Sliced_5D_Increment, Histograms_All, file_location, output_type):
def make_rm5d_single(sdf, Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Binning, Q2_y_z_pT_phi_h_5D_Binning, Use_Weight, Sliced_5D_Increment, Histograms_All, custom_title=None):
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

    Histo_Binning_Name = f"Binning-Type:'{Binning}'-[Q2-{'y' if('Valerii' not in Binning) else 'xB'}-Bin:All, z-PT-Bin:All]"
    Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name = build_group_tags(Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Histo_Binning_Name)

    base_title, rec_title_mdf = build_titles_5d(Histo_Group, Histo_Data, var_title, num_bins_text=Num_of_Bins, custom_line=custom_title, Ver=Binning)

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
        
    # _write_and_tick(Histograms_All, Histo_Name_1D, file_location, output_type)
    # # print(Histo_Name_1D)
    # if((Histo_Data in ["mdf"]) and ("Background" not in Histo_Group)):
    #     Start_Bin = Min_range
    #     Num_Slice = int(Num_of_Bins/Sliced_5D_Increment)
    #     for Slice in range(1, Num_Slice + 1):
    #         Histo_Name_Slice = f"{Histo_Name}_Slice_{Slice}_(Increment='{Sliced_5D_Increment}')"
    #         _write_and_tick(Histograms_All, Histo_Name_Slice, file_location, output_type)
    #         # print(Histo_Name_Slice)
    #         Start_Bin += Sliced_5D_Increment

    return Histograms_All


# --- 1D/3D Response Matrix: make exactly one request for one variable and one Q2-y bin ---


def apply_weight_norm(df_in, bin_filter, use_weight=False, histo_data=None):
    # Only MC REC should ever be renormalized
    # if((not use_weight) or (histo_data != "mdf")):
    if(not use_weight):
        return df_in.Filter(bin_filter)
    # Apply the cut first
    df_cut = df_in.Filter(bin_filter)
    # Check that weighting columns exist
    if((not df_cut.HasColumn("W_pre")) or (not df_cut.HasColumn("W_acc"))):
        print(f"{color.Error}WARNING: RDataframe is missing either `W_pre` or `W_acc`. Skipping weight renormalization.{color.END}")
        return df_cut
    # Number of events after the cut (unweighted integral)
    n_events = df_cut.Count().GetValue()
    # Compute sums for normalization
    sum_pre = df_cut.Sum("W_pre").GetValue()
    print(f"n_events  = {n_events}")
    print(f"sum_pre   = {sum_pre}")
    if(not df_cut.HasColumn("Event_Weight_raw")):
        df_cut  = df_cut.Define("Event_Weight_raw", "W_pre * W_acc")
        sum_acc = df_cut.Sum("Event_Weight_raw").GetValue()
    else:
        # print("Event_Weight_raw already exists")
        sum_acc = df_cut.Sum("Event_Weight_raw").GetValue()

    # Safety check
    if(sum_acc == 0):
        print(f"{color.Error}WARNING: sum_acc == 0 inside apply_weight_norm() after cut:\n    {bin_filter}\nSkipping weight renormalization.{color.END}")
        return df_cut

    # Renormalization factor
    renorm = sum_pre / sum_acc

    # (Re)define Event_Weight with renormalization
    if(df_cut.HasColumn("Event_Weight")):
        df_cut = df_cut.Redefine("Event_Weight", f"(W_pre * W_acc) * ({renorm})")
    else:
        df_cut = df_cut.Define("Event_Weight",   f"(W_pre * W_acc) * ({renorm})")

    print(f"sum_final = {df_cut.Sum("Event_Weight").GetValue()}\n")
        
    return df_cut

_weight_norm_by_bins_call_idx   = 0
_weight_norm_by_bins_cpp_ready  = False
def weight_norm_by_bins(df_in, Histo_Data_In, verbose=False, Do_not_use_Smeared=False, Valerii_binning=False):
    global _weight_norm_by_bins_call_idx
    global _weight_norm_by_bins_cpp_ready

    # Check weighting columns
    if((not df_in.HasColumn("W_pre")) or (not df_in.HasColumn("W_acc"))):
        print(f"{color.Error}ERROR: RDataframe is missing either `W_pre` or `W_acc`. Skipping weight renormalization.{color.END}")
        return df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in

    if(not df_in.HasColumn("Event_Weight_raw")):
        if(verbose):
            print(f"{color.RED}WARNING: RDataframe is missing `Event_Weight_raw`. Defining with `W_pre` and `W_acc`.{color.END}")
        df_in = df_in.Define("Event_Weight_raw", "W_pre * W_acc")

    Bin4D_name  = "Q2_y_z_pT_4D_Bins" if(not Valerii_binning) else "Q2_xB_z_pT_4D_Bin_Valerii"
    Use_Smeared = ((Histo_Data_In == "mdf") and (df_in.HasColumn(f"{Bin4D_name}_smeared")) and (not Do_not_use_Smeared))

    if((not Use_Smeared) and (not df_in.HasColumn(Bin4D_name))):
        print(f"{color.Error}ERROR: RDataframe is missing `{Bin4D_name}`. Skipping weight renormalization.{color.END}")
        return df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in

    bin_rec  = f"{Bin4D_name}_smeared" if(Use_Smeared) else Bin4D_name
    bin_min  = 0
    bin_max  = 546 if(not Valerii_binning) else 960
    num_bins = bin_max - bin_min + 1

    # --- mdf: 2D renorm on (REC-bin, GEN-bin) ---
    if((Histo_Data_In == "mdf")):
        bin_gen = f"{Bin4D_name}_gen"
        if(not df_in.HasColumn(bin_gen)):
            print(f"{color.Error}ERROR: mdf RDataframe is missing `{bin_gen}` required for 2D weight renormalization. Skipping.{color.END}")
            return df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in

        # Declare C++ helper once (needed so RDF JIT can fetch the TH2D renorm map by name)
        if(not _weight_norm_by_bins_cpp_ready):
            try:
                ROOT.gInterpreter.Declare(r"""
                #include "TH2D.h"
                #include "TROOT.h"
                #include "TSeqCollection.h"
                #include "TObject.h"

                TH2D* _wn_get_h2(const char* name){
                    if(!gROOT) return nullptr;
                    TSeqCollection* lst = gROOT->GetListOfSpecials();
                    if(!lst) return nullptr;
                    TObject* obj = lst->FindObject(name);
                    return dynamic_cast<TH2D*>(obj);
                }

                double _wn_get_renorm2d(const char* name, int rec_bin, int gen_bin, int bin_min, int bin_max){
                    TH2D* h = _wn_get_h2(name);
                    if(!h) return 1.0;
                    if((rec_bin < bin_min) || (rec_bin > bin_max) || (gen_bin < bin_min) || (gen_bin > bin_max)) return 1.0;
                    const int bx = rec_bin - bin_min + 1;
                    const int by = gen_bin - bin_min + 1;
                    return h->GetBinContent(bx, by);
                }
                """)
                _weight_norm_by_bins_cpp_ready = True
            except Exception as err:
                print(f"{color.Error}ERROR: failed to declare C++ helpers for 2D weight renormalization.{color.END}\n{err}")
                _weight_norm_by_bins_cpp_ready = False
                return df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in

        _weight_norm_by_bins_call_idx += 1
        tag = f"WN2D_{_weight_norm_by_bins_call_idx}"

        renorm_names = {}

        for group in ["Response_Matrix_Normal", "Background_Response_Matrix"]:
            group_filter = apply_background_filter(Histo_Data=Histo_Data_In, Histo_Group=group, base_filter="")
            if((group_filter is None) or (str(group_filter).strip() == "")):
                group_filter = "1"

            df_group = df_in.Filter(group_filter)

            hpre_name = f"h_pre2d_{group}_{tag}"
            hacc_name = f"h_acc2d_{group}_{tag}"
            hren_name = f"renorm2d_{group}_{tag}"

            h_pre_ptr = df_group.Histo2D((hpre_name, f"{bin_rec} vs {bin_gen} Unweighed (Base); {bin_rec}; {bin_gen}", num_bins, bin_min-0.5, bin_max+0.5, num_bins, bin_min-0.5, bin_max+0.5), bin_rec, bin_gen, "W_pre")
            h_acc_ptr = df_group.Histo2D((hacc_name, f"{bin_rec} vs {bin_gen} Weighed (with Acceptance); {bin_rec}; {bin_gen}", num_bins, bin_min-0.5, bin_max+0.5, num_bins, bin_min-0.5, bin_max+0.5), bin_rec, bin_gen, "Event_Weight_raw")

            h_pre = h_pre_ptr.GetValue()
            h_acc = h_acc_ptr.GetValue()

            h_ren = h_pre.Clone(hren_name)
            h_ren.SetTitle(f"Renorm factors; {bin_rec}; {bin_gen}")
            h_ren.SetDirectory(0)
            ROOT.SetOwnership(h_ren, False)

            h_ren.Divide(h_acc)

            # Patch denom==0 cells to 1.0
            zero_cells = 0
            for ix in range(1, num_bins + 1):
                for iy in range(1, num_bins + 1):
                    if(h_acc.GetBinContent(ix, iy) == 0.0):
                        h_ren.SetBinContent(ix, iy, 1.0)
                        zero_cells += 1

            if(zero_cells > 0):
                print(f"{color.RED}WARNING: sum_acc==0 in {zero_cells} cells for {group} (2D) -> renorm set to 1.0{color.END}")

            ROOT.gROOT.GetListOfSpecials().Add(h_ren)
            renorm_names[group] = hren_name

        has_bg  = ("Background_Response_Matrix" in renorm_names)
        bg_cond = ""
        if(has_bg):
            bg_cond = apply_background_filter(Histo_Data=Histo_Data_In, Histo_Group="Background_Response_Matrix", base_filter="")
            if((bg_cond is None) or (str(bg_cond).strip() == "")):
                has_bg  = False
                bg_cond = ""

        normal_name = renorm_names["Response_Matrix_Normal"]
        if(has_bg):
            bg_name = renorm_names["Background_Response_Matrix"]
            expr = f"""
            const int rec_bin = static_cast<int>({bin_rec});
            const int gen_bin = static_cast<int>({bin_gen});
            if({bg_cond}){{ return (W_pre * W_acc) * _wn_get_renorm2d("{bg_name}", rec_bin, gen_bin, {bin_min}, {bin_max}); }}
            return (W_pre * W_acc) * _wn_get_renorm2d("{normal_name}", rec_bin, gen_bin, {bin_min}, {bin_max});
            """
        else:
            expr = f"""
            const int rec_bin = static_cast<int>({bin_rec});
            const int gen_bin = static_cast<int>({bin_gen});
            return (W_pre * W_acc) * _wn_get_renorm2d("{normal_name}", rec_bin, gen_bin, {bin_min}, {bin_max});
            """

        df_in = df_in.Redefine("Event_Weight", expr) if(df_in.HasColumn("Event_Weight")) else df_in.Define("Event_Weight", expr)
        return df_in

    # --- non-mdf: keep your existing 1D logic unchanged ---
    if((not df_in.HasColumn(bin_rec))):
        print(f"{color.Error}ERROR: RDataframe is missing `{bin_rec}`. Skipping weight renormalization.{color.END}")
        return df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in

    renorm_dict = {}
    for group in ["Response_Matrix_Normal", "Background_Response_Matrix"]:
        if((Histo_Data_In != "mdf") and (group == "Background_Response_Matrix")):
            continue
        group_filter = apply_background_filter(Histo_Data=Histo_Data_In, Histo_Group=group, base_filter="")
        df_group = df_in.Filter(group_filter)
        h_pre = df_group.Histo1D(("h_pre", f"{bin_rec} Unweighed (Base); {bin_rec}", num_bins, bin_min-0.5, bin_max+0.5), bin_rec, "W_pre")
        h_acc = df_group.Histo1D(("h_acc", f"{bin_rec} Weighed (with Acceptance); {bin_rec}", num_bins, bin_min-0.5, bin_max+0.5), bin_rec, "Event_Weight_raw")

        renorms = []
        for idx in range(bin_min, bin_max + 1):
            bin_content_pre = h_pre.GetBinContent(idx + 1)
            bin_content_acc = h_acc.GetBinContent(idx + 1)
            if(bin_content_acc == 0):
                renorm = 1.0
                print(f"{color.Error}sum_acc=0 in {group} bin {idx} -> renorm=1.0{color.END}")
            else:
                renorm = bin_content_pre / bin_content_acc
            renorms.append(renorm)
        renorm_dict[group] = renorms

    cpp_code  = "#include <array>\n"
    cpp_code += f"const std::array<double,{num_bins}> renorms_normal {{{','.join(f'{x:.12g}' for x in renorm_dict['Response_Matrix_Normal'])}}};\n"
    has_bg    = ("Background_Response_Matrix" in renorm_dict)
    if(has_bg):
        cpp_code += f"const std::array<double,{num_bins}> renorms_bg {{{','.join(f'{x:.12g}' for x in renorm_dict['Background_Response_Matrix'])}}};\n"

    ROOT.gInterpreter.Declare(cpp_code)

    bg_cond = ""
    if(has_bg):
        bg_cond = apply_background_filter(Histo_Data=Histo_Data_In, Histo_Group="Background_Response_Matrix", base_filter="")
        expr = f"""
        if({bg_cond}){{ return (W_pre * W_acc) * renorms_bg[{bin_rec} - {bin_min}]; }}
        else {{ return (W_pre * W_acc) * renorms_normal[{bin_rec} - {bin_min}]; }}"""
    else:
        expr = f"return (W_pre * W_acc) * renorms_normal[{bin_rec} - {bin_min}];"

    df_in = df_in.Redefine("Event_Weight", expr) if(df_in.HasColumn("Event_Weight")) else df_in.Define("Event_Weight", expr)
    return df_in

def weight_norm_by_bins_wHisto(df_in, Histo_Data_In, args, Do_not_use_Smeared=False, Valerii_binning=False):
    global _weight_norm_by_bins_call_idx
    global _weight_norm_by_bins_cpp_ready

    # Check weighting columns
    if((not df_in.HasColumn("W_pre")) or (not df_in.HasColumn("W_acc"))):
        # print(f"{color.Error}ERROR: RDataframe is missing either `W_pre` or `W_acc`. Skipping weight renormalization.{color.END}")
        return (df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in, args, f"{color.Error}ERROR: RDataframe is missing either `W_pre` or `W_acc`. Skipping weight renormalization.{color.END}")

    if(not df_in.HasColumn("Event_Weight_raw")):
        if(args.verbose):
            print(f"{color.RED}WARNING: RDataframe is missing `Event_Weight_raw`. Defining with `W_pre` and `W_acc`.{color.END}")
        args.email_message = f"{args.email_message}\n{color.RED}WARNING FROM 'weight_norm_by_bins_wHisto()': RDataframe is missing `Event_Weight_raw`. Defining with `W_pre` and `W_acc`.{color.END}"
        df_in = df_in.Define("Event_Weight_raw", "W_pre * W_acc")

    Bin4D_name  = "Q2_y_z_pT_4D_Bins" if(not Valerii_binning) else "Q2_xB_z_pT_4D_Bin_Valerii"
    Use_Smeared = ((Histo_Data_In == "mdf") and (df_in.HasColumn(f"{Bin4D_name}_smeared")) and (not Do_not_use_Smeared))

    if((not Use_Smeared) and (not df_in.HasColumn(Bin4D_name))):
        # print(f"{color.Error}ERROR: RDataframe is missing `{Bin4D_name}`. Skipping weight renormalization.{color.END}")
        return (df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in, args, f"{color.Error}ERROR: RDataframe is missing `{Bin4D_name}`. Skipping weight renormalization.{color.END}")

    bin_rec  = f"{Bin4D_name}_smeared" if(Use_Smeared) else Bin4D_name
    bin_min  = 0
    bin_max  = 546 if(not Valerii_binning) else 960
    num_bins = bin_max - bin_min + 1

    # --- mdf: 2D renorm on (REC-bin, GEN-bin) ---
    if((Histo_Data_In == "mdf")):
        bin_gen = f"{Bin4D_name}_gen"
        if(not df_in.HasColumn(bin_gen)):
            # print(f"{color.Error}ERROR: mdf RDataframe is missing `{bin_gen}` required for 2D weight renormalization. Skipping.{color.END}")
            return (df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in, args, f"{color.Error}ERROR: mdf RDataframe is missing `{bin_gen}` required for 2D weight renormalization. Skipping.{color.END}")

        # Declare C++ helper once (needed so RDF JIT can fetch the TH2D renorm map by name)
        if(not _weight_norm_by_bins_cpp_ready):
            try:
                ROOT.gInterpreter.Declare(r"""
                #include "TH2D.h"
                #include "TROOT.h"
                #include "TSeqCollection.h"
                #include "TObject.h"
                TH2D* _wn_get_h2(const char* name){
                    if(!gROOT) return nullptr;
                    TSeqCollection* lst = gROOT->GetListOfSpecials();
                    if(!lst) return nullptr;
                    TObject* obj = lst->FindObject(name);
                    return dynamic_cast<TH2D*>(obj);
                }
                double _wn_get_renorm2d(const char* name, int rec_bin, int gen_bin, int bin_min, int bin_max){
                    TH2D* h = _wn_get_h2(name);
                    if(!h) return 1.0;
                    if((rec_bin < bin_min) || (rec_bin > bin_max) || (gen_bin < bin_min) || (gen_bin > bin_max)) return 1.0;
                    const int bx = rec_bin - bin_min + 1;
                    const int by = gen_bin - bin_min + 1;
                    return h->GetBinContent(bx, by);
                }
                """)
                _weight_norm_by_bins_cpp_ready = True
            except Exception as err:
                # print(f"{color.Error}ERROR: failed to declare C++ helpers for 2D weight renormalization.{color.END}\n{err}")
                _weight_norm_by_bins_cpp_ready = False
                return (df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in, args, f"{color.Error}ERROR: failed to declare C++ helpers for 2D weight renormalization.{color.END}\n{err}")
        _weight_norm_by_bins_call_idx += 1
        tag = f"WN2D_{_weight_norm_by_bins_call_idx}"
        renorm_names, histos_to_save = {}, {}
        for group in ["Response_Matrix_Normal", "Background_Response_Matrix"]:
            group_filter = apply_background_filter(Histo_Data=Histo_Data_In, Histo_Group=group, base_filter="")
            if((group_filter is None) or (str(group_filter).strip() == "")):
                group_filter = "1"
            df_group = df_in.Filter(group_filter)
            hpre_name = f"h_pre2d_{group}_{tag}"
            hacc_name = f"h_acc2d_{group}_{tag}"
            hren_name = f"renorm2d_{group}_{tag}"
            h_pre_ptr = df_group.Histo2D((hpre_name, f"{bin_rec} vs {bin_gen} Unweighed (Base); {bin_rec}; {bin_gen}", num_bins, bin_min-0.5, bin_max+0.5, num_bins, bin_min-0.5, bin_max+0.5), bin_rec, bin_gen, "W_pre")
            h_acc_ptr = df_group.Histo2D((hacc_name, f"{bin_rec} vs {bin_gen} Weighed (with Acceptance); {bin_rec}; {bin_gen}", num_bins, bin_min-0.5, bin_max+0.5, num_bins, bin_min-0.5, bin_max+0.5), bin_rec, bin_gen, "Event_Weight_raw")
            h_pre = h_pre_ptr.GetValue()
            h_acc = h_acc_ptr.GetValue()
            h_ren = h_pre.Clone(hren_name)
            h_ren.SetTitle(f"Renorm factors; {bin_rec}; {bin_gen}")
            h_ren.SetDirectory(0)
            ROOT.SetOwnership(h_ren, False)
            h_ren.Divide(h_acc)
            # Patch denom==0 cells to 1.0
            zero_cells = 0
            for ix in range(1, num_bins + 1):
                for iy in range(1, num_bins + 1):
                    if(h_acc.GetBinContent(ix, iy) == 0.0):
                        h_ren.SetBinContent(ix, iy, 1.0)
                        zero_cells += 1
            if(zero_cells > 0):
                print(f"{color.RED}WARNING: sum_acc==0 in {zero_cells} cells for {group} (2D) -> renorm set to 1.0{color.END}")
                args.email_message = f"{args.email_message}\n{color.RED}WARNING FROM 'weight_norm_by_bins_wHisto()': sum_acc==0 in {zero_cells} cells for {group} (2D) -> renorm set to 1.0{color.END}"
            ROOT.gROOT.GetListOfSpecials().Add(h_ren)
            histos_to_save[hpre_name] = h_pre_ptr
            histos_to_save[hacc_name] = h_acc_ptr
            histos_to_save[hren_name] = h_ren
            renorm_names[group] = hren_name
        has_bg  = ("Background_Response_Matrix" in renorm_names)
        bg_cond = ""
        if(has_bg):
            bg_cond = apply_background_filter(Histo_Data=Histo_Data_In, Histo_Group="Background_Response_Matrix", base_filter="")
            if((bg_cond is None) or (str(bg_cond).strip() == "")):
                has_bg  = False
                bg_cond = ""

        normal_name = renorm_names["Response_Matrix_Normal"]
        if(has_bg):
            bg_name = renorm_names["Background_Response_Matrix"]
            expr = f"""
            const int rec_bin = static_cast<int>({bin_rec});
            const int gen_bin = static_cast<int>({bin_gen});
            if({bg_cond}){{ return (W_pre * W_acc) * _wn_get_renorm2d("{bg_name}", rec_bin, gen_bin, {bin_min}, {bin_max}); }}
            return (W_pre * W_acc) * _wn_get_renorm2d("{normal_name}", rec_bin, gen_bin, {bin_min}, {bin_max});
            """
        else:
            expr = f"""
            const int rec_bin = static_cast<int>({bin_rec});
            const int gen_bin = static_cast<int>({bin_gen});
            return (W_pre * W_acc) * _wn_get_renorm2d("{normal_name}", rec_bin, gen_bin, {bin_min}, {bin_max});
            """
        df_in = df_in.Redefine("Event_Weight", expr) if(df_in.HasColumn("Event_Weight")) else df_in.Define("Event_Weight", expr)
        return df_in, args, histos_to_save

    # --- non-mdf: keep your existing 1D logic unchanged ---
    if((not df_in.HasColumn(bin_rec))):
        # print(f"{color.Error}ERROR: RDataframe is missing `{bin_rec}`. Skipping weight renormalization.{color.END}")
        return (df_in.Define("Event_Weight", "1.0") if(not df_in.HasColumn("Event_Weight")) else df_in, args, f"{color.Error}ERROR: RDataframe is missing `{bin_rec}`. Skipping weight renormalization.{color.END}")

    renorm_dict, histos_to_save = {}, {}
    for group in ["Response_Matrix_Normal", "Background_Response_Matrix"]:
        if((Histo_Data_In != "mdf") and (group == "Background_Response_Matrix")):
            continue
        group_filter = apply_background_filter(Histo_Data=Histo_Data_In, Histo_Group=group, base_filter="")
        df_group = df_in.Filter(group_filter)
        h_pre = df_group.Histo1D(("h_pre", f"{bin_rec} Unweighed (Base); {bin_rec}", num_bins, bin_min-0.5, bin_max+0.5), bin_rec, "W_pre")
        h_acc = df_group.Histo1D(("h_acc", f"{bin_rec} Weighed (with Acceptance); {bin_rec}", num_bins, bin_min-0.5, bin_max+0.5), bin_rec, "Event_Weight_raw")
        renorms = []
        for idx in range(bin_min, bin_max + 1):
            bin_content_pre = h_pre.GetBinContent(idx + 1)
            bin_content_acc = h_acc.GetBinContent(idx + 1)
            if(bin_content_acc == 0):
                renorm = 1.0
                print(f"{color.Error}sum_acc=0 in {group} bin {idx} -> renorm=1.0{color.END}")
            else:
                renorm = bin_content_pre / bin_content_acc
            renorms.append(renorm)
        histos_to_save["h_pre"] = h_pre
        histos_to_save["h_acc"] = h_acc
        renorm_dict[group] = renorms

    cpp_code  = "#include <array>\n"
    cpp_code += f"const std::array<double,{num_bins}> renorms_normal {{{','.join(f'{x:.12g}' for x in renorm_dict['Response_Matrix_Normal'])}}};\n"
    has_bg    = ("Background_Response_Matrix" in renorm_dict)
    if(has_bg):
        cpp_code += f"const std::array<double,{num_bins}> renorms_bg {{{','.join(f'{x:.12g}' for x in renorm_dict['Background_Response_Matrix'])}}};\n"
    ROOT.gInterpreter.Declare(cpp_code)
    bg_cond = ""
    if(has_bg):
        bg_cond = apply_background_filter(Histo_Data=Histo_Data_In, Histo_Group="Background_Response_Matrix", base_filter="")
        expr = f"""
        if({bg_cond}){{ return (W_pre * W_acc) * renorms_bg[{bin_rec} - {bin_min}]; }}
        else {{ return (W_pre * W_acc) * renorms_normal[{bin_rec} - {bin_min}]; }}"""
    else:
        expr = f"return (W_pre * W_acc) * renorms_normal[{bin_rec} - {bin_min}];"
    df_in = df_in.Redefine("Event_Weight", expr) if(df_in.HasColumn("Event_Weight")) else df_in.Define("Event_Weight", expr)
    return df_in, args, histos_to_save


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
    if(sdf == "continue"):
        return Histograms_All

    Q2_xB_Bin_Filter_str, z_pT_Bin_Filter_str = _filter_fieldnames(Histo_Smear, Ver=Binning)
    # if((Q2_y_bin_num > 0) and ((Q2_xB_Bin_Filter_str in variable) or (("Bin" in variable) and ("Multi_Dim_z_pT_Bin" not in variable) and ("MultiDim_z_pT_Bin" not in variable)))):
    #     return Histograms_All

    Histo_Binning = [Binning, "All" if(Q2_y_bin_num == -1) else str(Q2_y_bin_num), "All"]
    Histo_Binning_Name = f"Binning-Type:'{Histo_Binning[0]}'-[Q2-{'y' if('Valerii' not in Binning) else 'xB'}-Bin:{Histo_Binning[1]}, z-PT-Bin:{Histo_Binning[2]}]"
    Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name = build_group_tags(Histo_Group, Histo_Data, Histo_Cut, Histo_Smear, Histo_Binning_Name)

    Histo_Name    =    finalize_histo_name((Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name), Histo_Var_RM_Name)
    Histo_Name_1D = finalize_histo_name_1d((Histo_Group_Name, Histo_Data_Name, Histo_Cut_Name, Histo_Smear_Name, Histo_Binning_Name), Histo_Var_RM_Name, Histo_Group)

    # Cut_Line_l2 = f"#scale[1.15]{{Cut: {Cut_Choice_Title(Cut_Type=Histo_Cut)}}}"
    Cut_Line_l2 = f"#scale[1.15]{{Cut: {Cut_Flag_to_Title(cut_flag=Histo_Cut)}}}"
    Bin_Line_l4 = f"Q^{{2}}-{'y' if('Valerii' not in Binning) else 'xB'} Bin: {Histo_Binning[1]}" # if(Q2_y_bin_num > 0) else ""
    var_t = variable_Title_name(variable)
    if((Histo_Group    == "Response_Matrix") and (("Combined_" not in variable) and ("Multi_Dim" not in variable) and ("MultiDim" not in variable) and ("Q2_y_z_pT_4D_Bins" not in variable) and ("Valerii" not in variable))):
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
            left_label  = f"{variable_Title_name(variable.replace('_smeared', ''))} GEN Bins" if(Histo_Group == "Response_Matrix") else f"{variable_Title_name(variable.replace('_smeared',''))} (GEN)"
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
        Bin_Filter = f"({Bin_Filter}) && ({Q2_xB_Bin_Filter_str} != 0{f' && {extra})' if(extra != '') else ')'}"

    if(Use_Weight):
        Histo_Name_Weighed = f"{Histo_Name}_(Weighed)"
        Histo_Name_1D_Weighed = f"{Histo_Name_1D}_(Weighed)"
    else:
        Histo_Name_Weighed, Histo_Name_1D_Weighed = None, None

    Bin_Filter = apply_background_filter(Histo_Data, Histo_Group, Bin_Filter)
    sdf_cut = sdf.Filter(Bin_Filter)
    # print(f"Histo_Group = {Histo_Group}")
    # sdf_cut    = apply_weight_norm(df_in=sdf, bin_filter=Bin_Filter, use_weight=Use_Weight, histo_data=Histo_Data)
    if(Histo_Data in ["mdf"]):
        if(is_scalar_or_multidim(variable)):
            if(Use_Weight):
                title_weight = f"#splitline{{{title.split(';')[0]}}}{{Weighted}};{';'.join(title.split(';')[1:])}"
                Histograms_All[Histo_Name_Weighed]        = sdf_cut.Histo2D((str(Histo_Name_Weighed),    title_weight,  int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Gen), str(Variable_Rec), "Event_Weight")
            Histograms_All[Histo_Name]                    = sdf_cut.Histo2D((str(Histo_Name),              str(title),  int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin,  int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Gen), str(Variable_Rec))
            if(title2 is not None):
                if(Use_Weight):
                    title2_weight = f"#splitline{{{title2.split(';')[0]}}}{{Weighted}};{';'.join(title2.split(';')[1:])}"
                    Histograms_All[Histo_Name_1D_Weighed] = sdf_cut.Histo1D((str(Histo_Name_1D_Weighed), title2_weight, int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec), "Event_Weight")
                Histograms_All[Histo_Name_1D]             = sdf_cut.Histo1D((str(Histo_Name_1D),           str(title2), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec))
        else:
            if(Use_Weight):
                title_weight = f"#splitline{{{title.split(';')[0]}}}{{Weighted}};{';'.join(title.split(';')[1:])}"
                Histograms_All[Histo_Name_Weighed]        = sdf_cut.Histo3D((str(Histo_Name_Weighed),    title_weight, int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Gen),      str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
                Histograms_All[Histo_Name_1D_Weighed]     = sdf_cut.Histo2D((str(Histo_Name_1D_Weighed), title_weight.replace(f"; {variable_Title_name(Res_Binning_2D_z_pT[0])}", "; Counts"), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
            Histograms_All[Histo_Name]                    = sdf_cut.Histo3D((str(Histo_Name),              str(title), int(num_of_GEN_bins), min_GEN_bin, Max_GEN_bin, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Gen),      str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
            Histograms_All[Histo_Name_1D]                 = sdf_cut.Histo2D((str(Histo_Name_1D),           str(title).replace(f"; {variable_Title_name(Res_Binning_2D_z_pT[0])}", "; Counts"), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))
    else:
        if(is_scalar_or_multidim(variable)):
            if(Use_Weight):
                title_weight = f"#splitline{{{title.split(';')[0]}}}{{Weighted}};{';'.join(title.split(';')[1:])}"
                Histograms_All[Histo_Name_1D_Weighed]     = sdf_cut.Histo1D((str(Histo_Name_1D_Weighed), title_weight.replace(f"; {variable_Title_name(Res_Binning_2D_z_pT[0])}", ""), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec), "Event_Weight")
            Histograms_All[Histo_Name_1D]                 = sdf_cut.Histo1D((str(Histo_Name_1D),           str(title).replace(f"; {variable_Title_name(Res_Binning_2D_z_pT[0])}", ""), int(num_of_REC_bins), min_REC_bin, Max_REC_bin), str(Variable_Rec))
        else:
            if(Use_Weight):
                title_weight = f"#splitline{{{title.split(';')[0]}}}{{Weighted}};{';'.join(title.split(';')[1:])}"
                Histograms_All[Histo_Name_1D_Weighed]     = sdf_cut.Histo2D((str(Histo_Name_1D_Weighed), title_weight, int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]), "Event_Weight")
            Histograms_All[Histo_Name_1D]                 = sdf_cut.Histo2D((str(Histo_Name_1D),           str(title), int(num_of_REC_bins), min_REC_bin, Max_REC_bin, int(Res_Binning_2D_z_pT[3]), Res_Binning_2D_z_pT[1], Res_Binning_2D_z_pT[2]), str(Variable_Rec), str(Res_Binning_2D_z_pT[0]))

    # # targets = []
    # # if(Histo_Name in Histograms_All):
    # #     targets.append(Histo_Name)
    # # if(Histo_Name_1D in Histograms_All):
    # #     targets.append(Histo_Name_1D)
    # if(Histo_Name_Weighed in Histograms_All):
    # #     targets.append(Histo_Name_Weighed)
    #     Histograms_All[Histo_Name_Weighed].SetTitle(f"#splitline{{{Histograms_All[Histo_Name_Weighed].GetTitle()}}}{{Weighted}}")
    # if(Histo_Name_1D_Weighed in Histograms_All):
    # #     targets.append(Histo_Name_1D_Weighed)
    #     Histograms_All[Histo_Name_1D_Weighed].SetTitle(f"#splitline{{{Histograms_All[Histo_Name_1D_Weighed].GetTitle()}}}{{Weighted}}")
    # # for key in targets:
    # #     # _write_and_tick(Histograms_All, key, file_location, output_type)
    # #     safe_write(obj=Histograms_All[key], tfile=file_location)
    return Histograms_All


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


def make_TH2D_histos(sdf, Histo_Data, Histo_Cut, Histo_Smear, Binning, Vars_Input, Use_Weight, Histograms_All={}, Histo_Group="Normal_2D", custom_title=None):
    if(not _guard_datatype_and_smear(Histo_Data, Histo_Smear)):
        return Histograms_All
    if(not _guard_gdf_cut(Histo_Data, Histo_Cut)):
        return Histograms_All
    if(not _guard_rm_group_background(Histo_Group, Histo_Data)):
        return Histograms_All
    if(("EDIS" in Histo_Cut)):
        return Histograms_All
    Res_Binning_4D = ["Q2_y_z_pT_4D_Bins", -0.5, 546.5, 547] if('Valerii' not in Binning) else ["Q2_xB_z_pT_4D_Bin_Valerii", -0.5, 960.5, 961]
    Var_X,  Var_Y  = Vars_Input
    if("mear" in str(Histo_Smear)):
        if("smeared" not in str(Res_Binning_4D[0])):
            Res_Binning_4D[0] = f"{Res_Binning_4D[0]}_smeared"
        if("smeared" not in str(Var_X[0])):
            Var_X[0] = f"{Var_X[0]}_smeared"
        if("smeared" not in str(Var_Y[0])):
            Var_Y[0] = f"{Var_Y[0]}_smeared"
    else:
        if("smeared" in str(Res_Binning_4D[0])):
            Res_Binning_4D[0] = Res_Binning_4D[0].replace("_smeared", "")
        if("smeared" in str(Var_X[0])):
            Var_X[0] = Var_X[0].replace("_smeared", "")
        if("smeared" in str(Var_Y[0])):
            Var_Y[0] = Var_Y[0].replace("_smeared", "")
    TH2D_Name  = f"""({Histo_Group})_({Histo_Data})_({Histo_Cut})_(SMEAR={Histo_Smear if(Histo_Smear not in ['']) else "''"})_(Q2_{'y' if('Valerii' not in Binning) else 'xB'}_z_pT_Bin_All)_({Var_X[0]})_({Var_Y[0]}){'_(Weighed)' if(Use_Weight) else ''}"""
    Data_Title = f"#color[{root_color.Blue}]{{Experimental}}" if('rdf' in Histo_Data) else f"#color[{root_color.Red}]{{Reconstructed MC}}" if('mdf' in Histo_Data) else f"#color[{root_color.Green}]{{Generated MC}}"
    if("mear" in str(Histo_Smear)):
        Data_Title = f"Smeared {Data_Title}"
    Main_Title = f"#scale[1.25]{{{variable_Title_name(Var_X[0])} vs {variable_Title_name(Var_Y[0])} ({Data_Title})}}"
    Cut__Title = f"#scale[1.15]{{Cut: {Cut_Flag_to_Title(cut_flag=Histo_Cut)}}}"
    if(custom_title not in ["", None]):
        Main_Title =f"#splitline{{{Main_Title}}}{{{custom_title}}}"
    Full_Title = f"#splitline{{{Main_Title}}}{{{Cut__Title}}}; {variable_Title_name(Var_X[0])}; {variable_Title_name(Var_Y[0])}; {variable_Title_name(Res_Binning_4D[0])}"
    # print(f"DEBUG - Columns in {Histo_Data} dataframe: {[c for c in sdf.GetColumnNames() if('smeared' in c)]}")
    # print(f"\tDEBUG - TH2D_Name = {TH2D_Name}")
    if(Use_Weight):
        Histograms_All[f"{TH2D_Name}_Weighed"] = sdf.Histo3D((f"{TH2D_Name}_Weighed", f"{Full_Title}; Weighed",  Var_X[3], Var_X[1], Var_X[2], Var_Y[3], Var_Y[1], Var_Y[2], Res_Binning_4D[3], Res_Binning_4D[1], Res_Binning_4D[2]), str(Var_X[0]), str(Var_Y[0]), str(Res_Binning_4D[0]), "Event_Weight")
    Histograms_All[TH2D_Name]                  = sdf.Histo3D((TH2D_Name,                 Full_Title,             Var_X[3], Var_X[1], Var_X[2], Var_Y[3], Var_Y[1], Var_Y[2], Res_Binning_4D[3], Res_Binning_4D[1], Res_Binning_4D[2]), str(Var_X[0]), str(Var_Y[0]), str(Res_Binning_4D[0]))
    return Histograms_All
    



import os
def Evaluate_And_Write_Histograms(hist_ptrs, out_path, test, timer):
    # Evaluate all booked histograms in ONE trigger, then write them all at once
    # hist_ptrs can be either:
    #   (A) dict: {"Histogram Bin (Q2y-zpt)": RResultPtr<TH2D>, ...}
    #   (B) list/tuple: [RResultPtr<TH2D>, ...]
    if(test):
        print(f"\n{color.BLUE}Would have saved the ROOT file as: {color.ERROR}{out_path}{color.END}")
        return len(hist_ptrs)
    if(isinstance(hist_ptrs, dict)):
        ptr_list = [hist_ptrs[key] for key in sorted(hist_ptrs.keys())]
    else:
        ptr_list = list(hist_ptrs)
    if((ptr_list is None) or (len(ptr_list) == 0)):
        raise ValueError("Evaluate_And_Write_Histograms(...): hist_ptrs is empty")
    out_dir  = os.path.dirname(os.path.abspath(out_path))
    if((out_dir != "") and (not os.path.exists(out_dir))):
        os.makedirs(out_dir, exist_ok=True)
    write_mode = "UPDATE" if(os.path.exists(out_path)) else "RECREATE"
    print(f"\n{color.BBLUE}{'Updating the' if(write_mode == 'UPDATE') else 'Creating a new'} ROOT file: {color.BPINK}{out_path}{color.END}")
    print(f"\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
    ROOT.RDF.RunGraphs(ptr_list)
    print(f"{color.BLUE}Time After 'RunGraphs':{color.END}\n\t{timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")
    fout = ROOT.TFile(out_path, write_mode)
    if((fout is None) or (fout.IsZombie())):
        raise RuntimeError(f"Evaluate_And_Write_Histograms(...): failed to open ROOT file: {out_path}")
    fout.cd()
    for ptr in ptr_list:
        hist = ptr.GetValue()
        # hist.Sumw2(True)
        hist.Write("", ROOT.TObject.kOverwrite)
    fout.Close()
    print(f"\n{color.BGREEN}ROOT FILE HAS BEEN SAVED{color.END}\n")
    return len(hist_ptrs)


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

