# Only_1D kinematics and Diagnostic_1D corrections, smearing, and bank matching.
# Names follow finalize_histo_name. Distinct sources and weights are never added together.
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

# Live kinematic ranges. xF uses the commented makeROOT axis, not List_of_2D_Plots.
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
    ("xF", 200, -1.0, 1.0),
]

Q2Y_BINS = 18
Q2Y_MIN = -0.5
Q2Y_MAX = 17.5
ZPT_BINS = 38
ZPT_MIN = -0.5
ZPT_MAX = 37.5

VAR_AXIS = {
    "Complete_Correction_Factor_Ele": (100, 0.9, 1.1),
    "Complete_Correction_Factor_Pip": (100, 0.9, 1.1),
    "Delta_Smear_El_P": (100, -0.5, 0.5),
    "Delta_Smear_Pip_P": (100, -0.5, 0.5),
    "Delta_phi_t": (125, -10.0, 10.0),
    "campaign_smear_dphi": (90, -180.0, 180.0),
}

MATCH_LABELS = [
    "Correct / Correct",
    "Correct / Wrong PID",
    "Correct / Unmatched",
    "Wrong PID / Correct",
    "Wrong PID / Wrong PID",
    "Wrong PID / Unmatched",
    "Unmatched / Correct",
    "Unmatched / Wrong PID",
    "Unmatched / Unmatched",
]
STATUS_LABELS = ["Correct", "Wrong PID", "Unmatched"]

DENSE_CELL = "campaign_dense_4d_cell"
_DENSE_READY = False
_CORR_READY = False


def column_names(df):
    names = []
    for item in df.GetColumnNames():
        names.append(str(item))
    return names


def report_missing(label, names):
    if(len(names) == 0):
        return
    print("unavailable %s: %s" % (label, ", ".join(names)))


def campaign_histo_name(group, data, cut, smear, var, rho_tag, weight_tag):
    from Histo_Files_ROOT.DataFrames.helper_functions_for_using_RDataFrames_python import build_group_tags, finalize_histo_name
    parts = build_group_tags(group, data, cut, smear, "Binning-Type:'Y_bin'")
    name = finalize_histo_name(parts, "Var:'%s'" % var)
    if(rho_tag not in [None, ""]):
        name = "%s_(%s)" % (name, rho_tag)
    if(weight_tag not in [None, ""]):
        name = "%s_(%s)" % (name, weight_tag)
    return name


def weighted_title(base, weight_tag):
    if(weight_tag in [None, ""]):
        return base
    if(";" in base):
        head, rest = base.split(";", 1)
        return "#splitline{%s}{Weighted (%s)};%s" % (head, weight_tag, rest)
    return "#splitline{%s}{Weighted (%s)}" % (base, weight_tag)


def store_histogram(histograms, name, pointer, missing):
    if(name in histograms):
        missing.append("duplicate histogram name %s" % name)
        return
    histograms[name] = pointer


def variable_title(column):
    if(column == "campaign_smear_dphi"):
        return "#Delta#phi_{h} from smearing"
    try:
        from MyCommonAnalysisFunction_richcap import variable_Title_name
        title = variable_Title_name(column)
        if(title not in [None, ""]):
            return title
    except Exception:
        pass
    return column


def dense_cell_axis():
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


def weight_variants(args, data_kind, names, missing, label):
    # rdf is never acceptance-weighted or spline-weighted. MC follows enabled_weight_specs.
    variants = [("", None)]
    if(data_kind == "rdf"):
        return variants
    from Histo_Files_ROOT.DataFrames.helper_functions_for_using_RDataFrames_python import enabled_weight_specs
    for tag, column in enabled_weight_specs(args, data_kind):
        if(tag in [None, ""]):
            continue
        if(column not in names):
            missing.append("%s requested weight %s column %s is absent" % (label, tag, column))
            continue
        variants.append((tag, column))
    if("exclusive_rho_weight" in names):
        variants.append(("exclusive_rho_weight", "exclusive_rho_weight"))
    return variants


def book_th3(frame, histograms, missing, name, title, x_spec, y_spec, z_spec, xcol, ycol, zcol, weight_col):
    nx, x0, x1 = x_spec
    ny, y0, y1 = y_spec
    nz, z0, z1 = z_spec
    model = (name, title, nx, x0, x1, ny, y0, y1, nz, z0, z1)
    if(weight_col in [None, ""]):
        pointer = frame.Histo3D(model, xcol, ycol, zcol)
    else:
        pointer = frame.Histo3D(model, xcol, ycol, zcol, weight_col)
    store_histogram(histograms, name, pointer, missing)


def book_th2(frame, histograms, missing, name, title, x_spec, y_spec, xcol, ycol, weight_col):
    nx, x0, x1 = x_spec
    ny, y0, y1 = y_spec
    model = (name, title, nx, x0, x1, ny, y0, y1)
    if(weight_col in [None, ""]):
        pointer = frame.Histo2D(model, xcol, ycol)
    else:
        pointer = frame.Histo2D(model, xcol, ycol, weight_col)
    store_histogram(histograms, name, pointer, missing)


def book_th1(frame, histograms, missing, name, title, spec, column, weight_col):
    nbins, low, high = spec
    model = (name, title, nbins, low, high)
    if(weight_col in [None, ""]):
        pointer = frame.Histo1D(model, column)
    else:
        pointer = frame.Histo1D(model, column, weight_col)
    store_histogram(histograms, name, pointer, missing)


def filtered_frame(df, names, cut, missing, label):
    if(cut not in names):
        missing.append("%s %s" % (label, cut))
        return None
    return df.Filter("%s == 1" % cut)


def book_kinematic_family(df, histograms, missing, args, data_kind, rho_tag, label, column_suffix, smear):
    names = column_names(df)
    frame = filtered_frame(df, names, "cut_Complete_SIDIS", missing, label)
    if(frame is None):
        return
    if(("Q2_Y_Bin" not in names) or ("z_pT_Bin_Y_bin" not in names)):
        missing.append("%s Q2_Y_Bin or z_pT_Bin_Y_bin" % label)
        return
    y_spec = (Q2Y_BINS, Q2Y_MIN, Q2Y_MAX)
    z_spec = (ZPT_BINS, ZPT_MIN, ZPT_MAX)
    for tag, weight_col in weight_variants(args, data_kind, names, missing, label):
        for column, nbins, low, high in KINEMATIC_COLUMNS:
            source_column = column if(column_suffix in [None, ""]) else "%s%s" % (column, column_suffix)
            if(source_column not in names):
                missing.append("%s %s" % (label, source_column))
                continue
            var = source_column
            name = campaign_histo_name("Only_1D", data_kind, "cut_Complete_SIDIS", smear, var, rho_tag, tag)
            title = weighted_title("%s;Q^{2}-y bin;z-p_{T} bin" % variable_title(source_column), tag)
            book_th3(frame, histograms, missing, name, title, (nbins, low, high), y_spec, z_spec, source_column, "Q2_Y_Bin", "z_pT_Bin_Y_bin", weight_col)
        if((column_suffix in [None, ""]) and ("cut_Complete_SIDIS_MM_None" in names) and ("MM" in names)):
            mm_frame = df.Filter("cut_Complete_SIDIS_MM_None == 1")
            name = campaign_histo_name("Only_1D", data_kind, "cut_Complete_SIDIS_MM_None", smear, "MM", rho_tag, tag)
            title = weighted_title("%s, missing-mass cut removed;Q^{2}-y bin;z-p_{T} bin" % variable_title("MM"), tag)
            book_th3(mm_frame, histograms, missing, name, title, (80, 0.5, 4.5), y_spec, z_spec, "MM", "Q2_Y_Bin", "z_pT_Bin_Y_bin", weight_col)
    if("cut_Complete_NoKin" not in names):
        missing.append("%s Q2 cut omitted and y cut omitted (cut_Complete_NoKin is not in this snapshot)" % label)


def book_phi_response(df, histograms, missing, args, rho_tag, label):
    names = column_names(df)
    needed = ["phi_t", "phi_t_gen", "Q2_Y_Bin", "z_pT_Bin_Y_bin", "cut_Complete_SIDIS"]
    absent = [name for name in needed if(name not in names)]
    if(len(absent) > 0):
        missing.append("%s phi response %s" % (label, ", ".join(absent)))
        return
    attached = attach_dense_cell(df, missing, label)
    if(attached is None):
        return
    frame, n_bins, z_min, z_max = attached
    frame = frame.Filter("cut_Complete_SIDIS == 1")
    for tag, weight_col in weight_variants(args, "mdf", names, missing, label):
        name = campaign_histo_name("Only_1D", "mdf", "cut_Complete_SIDIS", "no_smear", "phi_response_4d", rho_tag, tag)
        title = weighted_title("Reconstructed #phi_{h} vs matched generated #phi_{h} vs 4D cell;#phi_{h} rec [deg];#phi_{h} gen [deg];4D cell", tag)
        book_th3(frame, histograms, missing, name, title, (24, 0.0, 360.0), (24, 0.0, 360.0), (n_bins, z_min, z_max), "phi_t", "phi_t_gen", DENSE_CELL, weight_col)


def ensure_smear_dphi(df, names):
    if(("phi_t" in names) and ("phi_t_smeared" in names) and (not df.HasColumn("campaign_smear_dphi"))):
        df = df.Define("campaign_smear_dphi", """
            double dphi = phi_t_smeared - phi_t;
            while(dphi > 180.0){ dphi -= 360.0; }
            while(dphi <= -180.0){ dphi += 360.0; }
            return dphi;
        """)
    return df


def ensure_correction_dphi(df, names, missing, label):
    # Delta_phi_t is phi_t minus the phi_h computed after undoing the pion correction.
    # Run_Uncorrected_phi_t_Info_Q is false, so the column is usually absent from snapshots.
    if("Delta_phi_t" in names):
        return df
    needed = ["pipx", "pipy", "pipz", "pipsec", "Complete_Correction_Factor_Pip", "phi_t", "ex", "ey", "ez"]
    absent = [name for name in needed if(name not in names)]
    if(len(absent) > 0):
        missing.append("%s Delta_phi_t %s" % (label, ", ".join(absent)))
        return df
    global _CORR_READY
    if(not _CORR_READY):
        import ROOT
        from ExtraAnalysisCodeValues import Correction_Code_Full_In, Rotation_Matrix
        ROOT.gInterpreter.Declare(Correction_Code_Full_In)
        ROOT.gInterpreter.Declare(Rotation_Matrix)
        _CORR_READY = True
    df = df.Define("Delta_phi_t", """
        auto fpip = (dppC(pipx, pipy, pipz, pipsec, 1, 3) + 1)/(Complete_Correction_Factor_Pip);
        auto beamM = ROOT::Math::PxPyPzMVector(0, 0, 10.6, 0);
        auto eleM = ROOT::Math::PxPyPzMVector(ex, ey, ez, 0);
        auto pip0M = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);
        TLorentzVector beam(0, 0, 10.6, beamM.E());
        TLorentzVector ele(ex, ey, ez, eleM.E());
        TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());
        TLorentzVector lv_q = beam - ele;
        auto pip0_Clone = Rot_Matrix(pip0, -1, lv_q.Theta(), ele.Phi());
        double phi_h_uncorrected = pip0_Clone.Phi()*TMath::RadToDeg();
        if(phi_h_uncorrected < 0){ phi_h_uncorrected += 360; }
        return phi_t - phi_h_uncorrected;
    """)
    return df


def book_correction_and_smear(df, histograms, missing, args, data_kind, rho_tag, label):
    names = column_names(df)
    df = ensure_smear_dphi(df, names)
    if(data_kind == "rdf"):
        df = ensure_correction_dphi(df, names, missing, label)
    names = column_names(df)
    attached = attach_dense_cell(df, missing, label)
    if(attached is None):
        return
    df, n_bins, z_min, z_max = attached
    y_q2 = (Q2Y_BINS, Q2Y_MIN, Q2Y_MAX)
    z_pt = (ZPT_BINS, ZPT_MIN, ZPT_MAX)
    dense = (n_bins, z_min, z_max)
    pairs = []
    index_pairs = []
    if(data_kind == "rdf"):
        pairs = [
            ("corr_el_vs_pip", "Complete_Correction_Factor_Ele", "Complete_Correction_Factor_Pip"),
            ("corr_el_vs_dphi", "Complete_Correction_Factor_Ele", "Delta_phi_t"),
            ("corr_pip_vs_dphi", "Complete_Correction_Factor_Pip", "Delta_phi_t"),
        ]
        index_pairs = [
            ("corr_el_index", "Complete_Correction_Factor_Ele"),
            ("corr_pip_index", "Complete_Correction_Factor_Pip"),
        ]
    else:
        pairs = [
            ("smear_el_vs_pip", "Delta_Smear_El_P", "Delta_Smear_Pip_P"),
            ("smear_el_vs_dphi", "Delta_Smear_El_P", "campaign_smear_dphi"),
            ("smear_pip_vs_dphi", "Delta_Smear_Pip_P", "campaign_smear_dphi"),
        ]
        index_pairs = [
            ("smear_el_index", "Delta_Smear_El_P"),
            ("smear_pip_index", "Delta_Smear_Pip_P"),
        ]
    for tag, weight_col in weight_variants(args, data_kind, names, missing, label):
        for var, xcol, ycol in pairs:
            if((xcol not in names) or (ycol not in names)):
                missing.append("%s %s" % (label, var))
                continue
            name = campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", var, rho_tag, tag)
            title = weighted_title("%s vs %s vs 4D cell;%s;%s;4D cell" % (variable_title(xcol), variable_title(ycol), variable_title(xcol), variable_title(ycol)), tag)
            book_th3(df, histograms, missing, name, title, VAR_AXIS[xcol], VAR_AXIS[ycol], dense, xcol, ycol, DENSE_CELL, weight_col)
        for var, column in index_pairs:
            if(column not in names):
                missing.append("%s %s" % (label, var))
                continue
            name = campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", var, rho_tag, tag)
            title = weighted_title("%s by Q^{2}-y and z-p_{T};%s;Q^{2}-y bin;z-p_{T} bin" % (variable_title(column), variable_title(column)), tag)
            book_th3(df, histograms, missing, name, title, VAR_AXIS[column], y_q2, z_pt, column, "Q2_Y_Bin", "z_pT_Bin_Y_bin", weight_col)


def pid_columns_for_matching(matching):
    from Histo_Files_ROOT.DataFrames.helper_functions_for_using_RDataFrames_python import MATCHING_SOURCE_SUFFIX, matching_source_column, normalize_matching_criteria
    mode = normalize_matching_criteria(matching)
    suffix = MATCHING_SOURCE_SUFFIX[mode]
    return matching_source_column("PID_el", suffix), matching_source_column("PID_pip", suffix)


def match_category_expression(el_col, pip_col):
    # 0 = correct PID, 1 = wrong nonzero PID, 2 = unmatched. Category is 3 * electron + pion.
    return "return (((%s == 11) ? 0 : ((%s == 0) ? 2 : 1)) * 3) + ((%s == 211) ? 0 : ((%s == 0) ? 2 : 1));" % (el_col, el_col, pip_col, pip_col)


def status_expression(column, correct_pid):
    return "return (%s == %d) ? 0 : ((%s == 0) ? 2 : 1);" % (column, correct_pid, column)


def book_matching(df, histograms, missing, args, data_kind, rho_tag, label, matching):
    names = column_names(df)
    el_col, pip_col = pid_columns_for_matching(matching)
    if((el_col not in names) or (pip_col not in names)):
        missing.append("%s PID columns %s %s" % (label, el_col, pip_col))
        return
    if(not df.HasColumn("campaign_match_category")):
        df = df.Define("campaign_match_category", match_category_expression(el_col, pip_col))
    if(not df.HasColumn("campaign_el_status")):
        df = df.Define("campaign_el_status", status_expression(el_col, 11))
    if(not df.HasColumn("campaign_pip_status")):
        df = df.Define("campaign_pip_status", status_expression(pip_col, 211))
    if(not df.HasColumn("campaign_one")):
        df = df.Define("campaign_one", "1.0")
    attached = attach_dense_cell(df, missing, label)
    has_index = ("Q2_Y_Bin" in names) and ("z_pT_Bin_Y_bin" in names)
    cat_axis = (9, -0.5, 8.5)
    status_axis = (3, -0.5, 2.5)
    ones_axis = (1, -0.5, 0.5)
    y_q2 = (Q2Y_BINS, Q2Y_MIN, Q2Y_MAX)
    z_pt = (ZPT_BINS, ZPT_MIN, ZPT_MAX)
    for tag, weight_col in weight_variants(args, data_kind, names, missing, label):
        name = campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "match_category", rho_tag, tag)
        title = weighted_title("Bank match category;electron / pion;Counts", tag)
        book_th1(df, histograms, missing, name, title, cat_axis, "campaign_match_category", weight_col)
        book_th1(df, histograms, missing, campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "el_status", rho_tag, tag), weighted_title("Electron match status;status;Counts", tag), status_axis, "campaign_el_status", weight_col)
        book_th1(df, histograms, missing, campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "pip_status", rho_tag, tag), weighted_title("Pion match status;status;Counts", tag), status_axis, "campaign_pip_status", weight_col)
        book_th1(df, histograms, missing, campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "el_pid", rho_tag, tag), weighted_title("Electron generated PID;PID;Counts", tag), (40, -20.5, 19.5), el_col, weight_col)
        book_th1(df, histograms, missing, campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "pip_pid", rho_tag, tag), weighted_title("Pion generated PID;PID;Counts", tag), (80, -0.5, 79.5), pip_col, weight_col)
        book_th1(df, histograms, missing, campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "match_denominator", rho_tag, tag), weighted_title("Match denominator;count;Counts", tag), ones_axis, "campaign_one", weight_col)
        if(has_index):
            book_th3(df, histograms, missing, campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "match_category_q2y_zpt", rho_tag, tag), weighted_title("Match category by Q^{2}-y and z-p_{T};category;Q^{2}-y bin;z-p_{T} bin", tag), cat_axis, y_q2, z_pt, "campaign_match_category", "Q2_Y_Bin", "z_pT_Bin_Y_bin", weight_col)
            book_th3(df, histograms, missing, campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "match_denominator_q2y_zpt", rho_tag, tag), weighted_title("Match denominator by Q^{2}-y and z-p_{T};count;Q^{2}-y bin;z-p_{T} bin", tag), ones_axis, y_q2, z_pt, "campaign_one", "Q2_Y_Bin", "z_pT_Bin_Y_bin", weight_col)
        if(attached is not None):
            dense_frame, n_bins, z_min, z_max = attached
            book_th2(dense_frame, histograms, missing, campaign_histo_name("Diagnostic_1D", data_kind, "cut_Complete_SIDIS", "no_smear", "match_category_dense", rho_tag, tag), weighted_title("Match category vs 4D cell;category;4D cell", tag), cat_axis, (n_bins, z_min, z_max), "campaign_match_category", DENSE_CELL, weight_col)


def label_match_axes(hist):
    name = str(hist.GetName())
    if("match_category" in name):
        axis = hist.GetXaxis()
        for index, text in enumerate(MATCH_LABELS):
            axis.SetBinLabel(index + 1, text)
    elif(("el_status" in name) or ("pip_status" in name)):
        axis = hist.GetXaxis()
        for index, text in enumerate(STATUS_LABELS):
            axis.SetBinLabel(index + 1, text)


def write_category_figure(hist, root_path):
    import ROOT
    canvas = ROOT.TCanvas("campaign_match_category", "match category", 900, 500)
    draw = hist.Clone("campaign_match_category_draw")
    draw.SetDirectory(0)
    label_match_axes(draw)
    draw.Draw("hist")
    pdf_path = os.path.splitext(root_path)[0] + "_match_category.pdf"
    canvas.SaveAs(pdf_path)
    print("wrote match category figure %s" % pdf_path)


def write_histograms(path, histograms):
    import ROOT
    from Histo_Files_ROOT.DataFrames.helper_functions_for_using_RDataFrames_python import safe_write
    out_dir = os.path.dirname(os.path.abspath(path))
    if((out_dir != "") and (not os.path.isdir(out_dir))):
        os.makedirs(out_dir, exist_ok=True)
    if(os.path.isfile(path) and (os.path.getsize(path) > 0)):
        print("1D output already exists and was not rewritten: %s" % path)
        return
    root_file = ROOT.TFile(str(path), "RECREATE")
    category_hist = None
    for name in histograms:
        hist = histograms[name].GetValue()
        hist.SetName(name)
        label_match_axes(hist)
        if((category_hist is None) and ("match_category" in name) and ("dense" not in name) and ("q2y" not in name)):
            category_hist = hist
        safe_write(hist, root_file)
    root_file.Close()
    print("wrote %d 1D histograms to %s" % (len(histograms), path))
    if(category_hist is not None):
        write_category_figure(category_hist, path)


def split_rho_files(paths):
    from Campaign.ifarm_inputs import classify_rho_name
    groups = {"clasdis": [], "lundvpk": [], "lundrho": [], "rho0_new": []}
    for path in paths:
        label = classify_rho_name(path)
        if(label in ["lundvpk", "lundrho", "rho0_new"]):
            groups[label].append(path)
        else:
            groups["clasdis"].append(path)
    return groups


def source_jobs(all_root_files, missing):
    jobs = []
    rdf_paths = list(all_root_files.get("rdf", []))
    if(len(rdf_paths) == 0):
        missing.append("rdf input files")
    else:
        jobs.append(("rdf", "rdf", "", rdf_paths))
    for key, data_kind in [("mdf_clasdis", "mdf"), ("gdf_clasdis", "gdf")]:
        paths = list(all_root_files.get(key, []))
        if(len(paths) == 0):
            missing.append("%s input files" % key)
            continue
        groups = split_rho_files(paths)
        for rho_tag, files in groups.items():
            if(len(files) == 0):
                missing.append("%s %s files" % (key, rho_tag))
                continue
            tag = "" if(rho_tag == "clasdis") else rho_tag
            jobs.append((data_kind, "%s_%s" % (data_kind, rho_tag), tag, files))
    return jobs


def run_campaign_1d(args, all_root_files):
    import ROOT
    missing = []
    histograms = {}
    for data_kind, label, rho_tag, paths in source_jobs(all_root_files, missing):
        df = ROOT.RDataFrame("h22", paths)
        if(getattr(args, "only_1d", False)):
            book_kinematic_family(df, histograms, missing, args, data_kind, rho_tag, label, "", "no_smear")
            if(data_kind == "mdf"):
                names = column_names(df)
                if("Q2_gen" in names):
                    book_kinematic_family(df, histograms, missing, args, data_kind, rho_tag, label + "_gen", "_gen", "matched_gen")
                book_phi_response(df, histograms, missing, args, rho_tag, label)
        if(getattr(args, "diagnostic_1d", False)):
            if(data_kind == "rdf"):
                book_correction_and_smear(df, histograms, missing, args, data_kind, rho_tag, label)
            elif(data_kind == "mdf"):
                book_correction_and_smear(df, histograms, missing, args, data_kind, rho_tag, label)
            book_matching(df, histograms, missing, args, data_kind, rho_tag, label, getattr(args, "matching_criteria", "Bank"))
    report_missing("1D", missing)
    if(len(histograms) == 0):
        raise SystemExit("1D mode booked no histograms")
    write_histograms(args.root, histograms)
