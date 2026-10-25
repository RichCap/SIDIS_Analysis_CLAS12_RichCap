# 1D phi response, kinematic distributions, and diagnostic histograms.
# Missing snapshot columns are reported and are not replaced with a different event sample.
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

# Live response-matrix ranges. nbins, low, high.
# xF is not in List_of_2D_Plots and is not given a new range.
KINEMATIC_COLUMNS = [
    ("Q2", 140, 0.0, 12.0),
    ("y", 100, 0.05, 1.05),
    ("xB", 100, 0.0, 1.0),
    ("z", 100, 0.0, 1.0),
    ("pT", 105, 0.0, 1.05),
    ("MM", 80, 0.5, 4.5),
    ("phi_t", 24, 0.0, 360.0),
    ("el", 200, 0.0, 8.0),
    ("pip", 150, 0.0, 6.0),
    ("elth", 200, 0.0, 40.0),
    ("pipth", 200, 0.0, 40.0),
    ("elPhi", 360, 0.0, 360.0),
    ("pipPhi", 360, 0.0, 360.0),
]

# Q2_Y_Bin and z_pT_Bin_Y_bin axes from make_TH2D_histos. Not the dense cell ordinal.
Q2Y_BINS = 18
Q2Y_MIN  = -0.5
Q2Y_MAX  = 17.5
ZPT_BINS = 38
ZPT_MIN  = -0.5
ZPT_MAX  = 37.5

# Physical ranges kept. Bin counts are the campaign diagnostic axes.
VAR_AXIS = {
    "Complete_Correction_Factor_Ele": (100, 0.9, 1.1),
    "Complete_Correction_Factor_Pip": (100, 0.9, 1.1),
    "Delta_Smear_El_P": (100, -0.5, 0.5),
    "Delta_Smear_Pip_P": (100, -0.5, 0.5),
    "Delta_phi_t": (125, -10.0, 10.0),
    "campaign_smear_dphi": (90, -180.0, 180.0),
}

DENSE_CELL = "campaign_dense_4d_cell"
_DENSE_READY = False


def column_names(df):
    names = []
    for item in df.GetColumnNames():
        names.append(str(item))
    return names


def report_missing(label, names):
    if(len(names) == 0):
        return
    print("unavailable %s: %s" % (label, ", ".join(names)))


def dense_cell_axis():
    # n comes from create_dense_5d_bin_mapping. Do not paste a fixed cell count here.
    global _DENSE_READY
    from Convert_MultiDim_Kinematic_Bins import create_dense_5d_bin_mapping
    mapping = create_dense_5d_bin_mapping()
    n_cells = int(mapping["total_kinematic_slots"])
    if(not _DENSE_READY):
        import ROOT
        ROOT.gInterpreter.Declare(mapping["cpp_dense_5d_code"])
        ROOT.gInterpreter.Declare("""
int Campaign_Dense_4D_Cell(int q2y, int zpt){
    if((q2y <= 0) || (zpt <= 0) || (q2y >= 18) || (zpt >= 40)){ return 0; }
    int start = kinematic_start_slot[q2y][zpt];
    if(start <= 0){ return 0; }
    return ((start - 1) / 24) + 1;
}
""")
        _DENSE_READY = True
    # Same edge rule as dense_5d_var_input: n + 2 bins from -1.5 to n + 0.5.
    return n_cells + 2, -1.5, float(n_cells) + 0.5


def attach_dense_cell(df, missing, sample):
    names = column_names(df)
    if(("Q2_Y_Bin" not in names) or ("z_pT_Bin_Y_bin" not in names)):
        missing.append("%s Q2_Y_Bin or z_pT_Bin_Y_bin" % sample)
        return None
    n_bins, z_min, z_max = dense_cell_axis()
    if(not df.HasColumn(DENSE_CELL)):
        df = df.Define(DENSE_CELL, "Campaign_Dense_4D_Cell(Q2_Y_Bin, z_pT_Bin_Y_bin)")
    return df, n_bins, z_min, z_max


def book_kinematic(df, sample, histograms, missing):
    # Nominal distributions use cut_Complete_SIDIS. Q2-only and y-only omissions need cut_Complete_NoKin, which these snapshots do not have.
    names = column_names(df)
    if("Event_Weight" in names):
        weight = "Event_Weight"
    else:
        df = df.Define("campaign_unit_weight", "1.0")
        weight = "campaign_unit_weight"
        names = column_names(df)
    if("cut_Complete_SIDIS" in names):
        nominal = df.Filter("cut_Complete_SIDIS == 1")
    else:
        nominal = df
        missing.append("%s cut_Complete_SIDIS" % sample)
    if(("Q2_Y_Bin" not in names) or ("z_pT_Bin_Y_bin" not in names)):
        missing.append("%s Q2_Y_Bin or z_pT_Bin_Y_bin" % sample)
        return
    for column, nbins, low, high in KINEMATIC_COLUMNS:
        if(column not in names):
            missing.append("%s %s" % (sample, column))
            continue
        model = ("%s_%s" % (sample, column), column, nbins, low, high, Q2Y_BINS, Q2Y_MIN, Q2Y_MAX, ZPT_BINS, ZPT_MIN, ZPT_MAX)
        histograms["%s_%s" % (sample, column)] = nominal.Histo3D(model, column, "Q2_Y_Bin", "z_pT_Bin_Y_bin", weight)
    if("cut_Complete_SIDIS_MM_None" in names):
        mm_frame = df.Filter("cut_Complete_SIDIS_MM_None == 1")
        if("MM" in names):
            model = ("%s_MM_cut_omitted" % sample, "MM", 80, 0.5, 4.5, Q2Y_BINS, Q2Y_MIN, Q2Y_MAX, ZPT_BINS, ZPT_MIN, ZPT_MAX)
            histograms["%s_MM_cut_omitted" % sample] = mm_frame.Histo3D(model, "MM", "Q2_Y_Bin", "z_pT_Bin_Y_bin", weight)
    else:
        missing.append("%s MM cut omitted" % sample)
    missing.append("%s Q2 cut omitted (cut_Complete_NoKin is not in this snapshot)" % sample)
    missing.append("%s y cut omitted (cut_Complete_NoKin is not in this snapshot)" % sample)


def book_phi_response(df, histograms, missing):
    names = column_names(df)
    if("Event_Weight" not in names):
        df = df.Define("campaign_unit_weight", "1.0")
        names = column_names(df)
    needed = ["phi_t", "phi_t_gen", "Q2_Y_Bin", "z_pT_Bin_Y_bin"]
    absent = [name for name in needed if(name not in names)]
    if(len(absent) > 0):
        missing.append("phi response " + ", ".join(absent))
        return
    attached = attach_dense_cell(df, missing, "mdf")
    if(attached is None):
        return
    frame, n_bins, z_min, z_max = attached
    if("cut_Complete_SIDIS" in names):
        frame = frame.Filter("cut_Complete_SIDIS == 1")
    weight = "Event_Weight" if("Event_Weight" in names) else "campaign_unit_weight"
    model = ("phi_response_4d", "phi_h response", 24, 0.0, 360.0, 24, 0.0, 360.0, n_bins, z_min, z_max)
    histograms["phi_response_4d"] = frame.Histo3D(model, "phi_t", "phi_t_gen", DENSE_CELL, weight)


def pid_columns_for_matching(matching):
    # Same suffix map as MATCHING_SOURCE_SUFFIX. Historical _gen keeps unsuffixed PID_el and PID_pip.
    from Histo_Files_ROOT.DataFrames.helper_functions_for_using_RDataFrames_python import MATCHING_SOURCE_SUFFIX, matching_source_column, normalize_matching_criteria
    mode = normalize_matching_criteria(matching)
    suffix = MATCHING_SOURCE_SUFFIX[mode]
    el_col = matching_source_column("PID_el", suffix)
    pip_col = matching_source_column("PID_pip", suffix)
    return el_col, pip_col


def match_category_expression(el_col, pip_col):
    # No local names. ROOT names the jit column arguments var0, var1, ... and rejects assignments to them.
    # 0 = matched (electron 11, pion 211), 1 = mismatched, 2 = unmatched (PID 0). Category is 3 * electron + pion.
    return "return (((%s == 11) ? 0 : ((%s == 0) ? 2 : 1)) * 3) + ((%s == 211) ? 0 : ((%s == 0) ? 2 : 1));" % (el_col, el_col, pip_col, pip_col)


def book_diagnostics(df, sample, histograms, missing, matching="Bank"):
    names = column_names(df)
    if("Event_Weight" in names):
        weight = "Event_Weight"
    else:
        df = df.Define("campaign_unit_weight", "1.0")
        weight = "campaign_unit_weight"
        names = column_names(df)
    if(("phi_t" in names) and ("phi_t_smeared" in names) and (not df.HasColumn("campaign_smear_dphi"))):
        df = df.Define("campaign_smear_dphi", """
            double dphi = phi_t_smeared - phi_t;
            while(dphi > 180.0){ dphi -= 360.0; }
            while(dphi <= -180.0){ dphi += 360.0; }
            return dphi;
        """)
        names = column_names(df)
        names.append("campaign_smear_dphi")
    pairs = [
        ("corr_el_vs_pip", "Complete_Correction_Factor_Ele", "Complete_Correction_Factor_Pip"),
        ("smear_el_vs_pip", "Delta_Smear_El_P", "Delta_Smear_Pip_P"),
        ("corr_el_vs_dphi", "Complete_Correction_Factor_Ele", "Delta_phi_t"),
        ("corr_pip_vs_dphi", "Complete_Correction_Factor_Pip", "Delta_phi_t"),
        ("smear_el_vs_dphi", "Delta_Smear_El_P", "campaign_smear_dphi"),
        ("smear_pip_vs_dphi", "Delta_Smear_Pip_P", "campaign_smear_dphi"),
    ]
    attached = None
    for name, xcol, ycol in pairs:
        if((xcol not in names) or (ycol not in names)):
            missing.append("%s %s" % (sample, name))
            continue
        if(attached is None):
            attached = attach_dense_cell(df, missing, sample)
        if(attached is None):
            continue
        df, n_bins, z_min, z_max = attached
        x_bins, x_min, x_max = VAR_AXIS[xcol]
        y_bins, y_min, y_max = VAR_AXIS[ycol]
        model = ("%s_%s" % (sample, name), name, x_bins, x_min, x_max, y_bins, y_min, y_max, n_bins, z_min, z_max)
        histograms["%s_%s" % (sample, name)] = df.Histo3D(model, xcol, ycol, DENSE_CELL, weight)
    index_pairs = [
        ("corr_el_index", "Complete_Correction_Factor_Ele"),
        ("corr_pip_index", "Complete_Correction_Factor_Pip"),
        ("smear_el_index", "Delta_Smear_El_P"),
        ("smear_pip_index", "Delta_Smear_Pip_P"),
    ]
    if(("Q2_Y_Bin" not in names) or ("z_pT_Bin_Y_bin" not in names)):
        missing.append("%s kinematic index" % sample)
        return
    for name, column in index_pairs:
        if(column not in names):
            missing.append("%s %s" % (sample, name))
            continue
        x_bins, x_min, x_max = VAR_AXIS[column]
        model = ("%s_%s" % (sample, name), name, x_bins, x_min, x_max, Q2Y_BINS, Q2Y_MIN, Q2Y_MAX, ZPT_BINS, ZPT_MIN, ZPT_MAX)
        histograms["%s_%s" % (sample, name)] = df.Histo3D(model, column, "Q2_Y_Bin", "z_pT_Bin_Y_bin", weight)
    el_col, pip_col = pid_columns_for_matching(matching)
    if((el_col in names) and (pip_col in names)):
        # frame = df.Define("match_category", """ int el = 2; int pip = 2; if(PID_el_Bank == 0){ el = 2; } ... """)
        frame = df.Define("match_category", match_category_expression(el_col, pip_col))
        model = ("%s_match_category" % sample, "match category", 9, -0.5, 8.5)
        histograms["%s_match_category" % sample] = frame.Histo1D(model, "match_category", weight)
        histograms["%s_el_source" % sample] = df.Histo1D(("%s_el_source" % sample, "electron generated PID", 40, -20.5, 19.5), el_col, weight)
        histograms["%s_pip_source" % sample] = df.Histo1D(("%s_pip_source" % sample, "pion generated PID", 80, -0.5, 79.5), pip_col, weight)
        counted = df.Define("campaign_one", "1.0")
        histograms["%s_source_denominator" % sample] = counted.Histo1D(("%s_source_denominator" % sample, "reconstructed count", 1, -0.5, 0.5), "campaign_one", weight)
    else:
        missing.append("%s PID columns %s %s" % (sample, el_col, pip_col))


def write_histograms(path, histograms):
    import ROOT
    out_dir = os.path.dirname(os.path.abspath(path))
    if((out_dir != "") and (not os.path.isdir(out_dir))):
        os.makedirs(out_dir, exist_ok=True)
    if(os.path.isfile(path) and (os.path.getsize(path) > 0)):
        print("1D output already exists and was not rewritten: %s" % path)
        return
    root_file = ROOT.TFile(str(path), "RECREATE")
    for name in histograms:
        hist = histograms[name].GetValue()
        hist.SetName(name)
        hist.Write()
    root_file.Close()
    print("wrote %d 1D histograms to %s" % (len(histograms), path))


def run_campaign_1d(args, all_root_files):
    import ROOT
    missing = []
    histograms = {}
    samples = [("rdf", "rdf"), ("mdf", "mdf_clasdis"), ("gdf", "gdf_clasdis")]
    for sample, key in samples:
        paths = all_root_files.get(key, [])
        if(len(paths) == 0):
            missing.append("%s input files" % sample)
            continue
        df = ROOT.RDataFrame("h22", paths)
        if(getattr(args, "only_1d", False)):
            book_kinematic(df, sample, histograms, missing)
            if(sample == "mdf"):
                book_phi_response(df, histograms, missing)
        if(getattr(args, "diagnostic_1d", False)):
            book_diagnostics(df, sample, histograms, missing, getattr(args, "matching_criteria", "Bank"))
    report_missing("1D", missing)
    if(len(histograms) == 0):
        raise SystemExit("1D mode booked no histograms")
    write_histograms(args.root, histograms)
