#!/usr/bin/env python3
# Derive the per-bin reconstruction factor C_n and the JSON used to fit RecS.
import os
import sys
import json
import argparse

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)
_DF_DIR = os.path.dirname(os.path.abspath(__file__))
if(_DF_DIR not in sys.path):
    sys.path.insert(0, _DF_DIR)

import numpy
import ROOT
ROOT.gErrorIgnoreLevel = ROOT.kError
ROOT.gROOT.SetBatch(True)

from Binning_Dictionaries import Full_Bin_Definition_Array

N_AXIS     = 10850
AXIS_MIN   = -1.5
AXIS_MAX   = 10848.5
N_APPROVED = 10848
XB_FACTOR  = 0.0502731
MDF_KEY    = "((Histo-Group='Response_Matrix_Normal_1D'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type='smear'), (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='MultiDim_Q2_y_z_pT_phi_h'-[NumBins=10850, MinBin=-1.5, MaxBin=10848.5]))"
WEIGHT_TAGS = ("_(RecSSpline)", "_(RecWSpline)", "_(AccSpline)", "_(AccJSON)", "_(RecS)", "_(RecW)", "_(Spline)", "_(JSON)", "_(Acc)", "_(Weighed)")
VARIABLES = (
    ("Q2",    "Q2",    120, 0.0,  12.0),
    ("y",     "y",     120, 0.05,  1.05),
    ("z",     "z",     120, 0.0,   1.0),
    ("pT",    "pT",    120, 0.0,   1.05),
    ("phi_h", "phi_t", 120, 0.0, 360.0),
)


def script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def default_input_path():
    return os.path.join(script_dir(), "hadd_ROOT_files_From_using_RDataFrames", "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_SIDIS_Workflow_Bank_Response_Matrices_Final_Thesis_Files_All.root")


def default_output_dir():
    return os.path.join(script_dir(), "RecW_Output")


class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="Derive RecW cumulative factors and export the RecS training JSON.", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument("-i", "--input_file", type=str, default=None, help="ROOT file with the 5D index histograms and response slices.\n")
    parser.add_argument("-vf", "--variable_file", type=str, default=None, help="ROOT file with variable-versus-index histograms for the figure. Defaults to --input_file.\n")
    parser.add_argument("-sw", "--spline_weights", action="store_true", help="Use the Spline-baseline MC history.\n")
    parser.add_argument("-it", "--iteration", type=int, default=1, help="Derivation number. 1 is the first residual.\n")
    parser.add_argument("-pi", "--physics_iteration", default=None, choices=["iter1", "iter2"], help="Physics injection for a Spline-baseline history. Omitted reads physics_spline_iteration from the input file.\n")
    parser.add_argument("-rw", "--recw_file", type=str, default=None, help="Cumulative-factor ROOT file to read and update.\n")
    parser.add_argument("-o", "--output_dir", type=str, default=None, help="Directory for the ROOT file, JSON, and figure.\n")
    parser.add_argument("-f", "--overwrite_iteration", action="store_true", help="Replace this iteration when no later iteration exists in the same history.\n")
    parser.add_argument("-sc", "--self_check", action="store_true", help="Run the synthetic checks and exit.\n")
    parser.add_argument("-fo", "--figure_only", action="store_true", help="Draw the comparison from an existing cumulative weight and --variable_file. Does not derive or replace a weight.\n")
    return parser.parse_args()


def fail(message):
    raise SystemExit(message)


def history_name(kind, iteration, spline):
    # kind is R or C. Spline-baseline names stay distinct from the plain history.
    suffix = "_Spline" if(spline) else ""
    return "%s_%d%s" % (kind, int(iteration), suffix)


def report_name(iteration, spline):
    stem = "spline" if(spline) else "default"
    return "report_%s_%d" % (stem, int(iteration))


def json_fit_set(iteration, spline, physics_iteration=""):
    if(not spline):
        return "RecS_default_iter%d" % int(iteration)
    if(str(physics_iteration) in ["iter1", "iter2"]):
        return "RecS_spline_phys%s_iter%d" % (str(physics_iteration), int(iteration))
    return ""


def read_physics_iteration(path):
    root_file = ROOT.TFile.Open(str(path), "READ")
    if((root_file is None) or root_file.IsZombie()):
        if(root_file is not None):
            root_file.Close()
        return "unmarked"
    marker = root_file.Get("physics_spline_iteration")
    identity = "unmarked"
    if(marker):
        identity = str(marker.GetTitle()).strip()
    root_file.Close()
    if(identity not in ["iter1", "iter2"]):
        return "unmarked"
    return identity


def figure_path(output_dir, iteration, spline):
    stem = "spline" if(spline) else "default"
    return os.path.join(output_dir, "RecW_comparison_%s_iter%d.pdf" % (stem, int(iteration)))


def sibling_keys(mdf_key):
    bdf_key = mdf_key.replace("Response_Matrix_Normal_1D", "Background_Response_Matrix_1D")
    rho_key = mdf_key + "_(rho0_new)"
    rdf_key = mdf_key.replace("(Data-Type='mdf')", "(Data-Type='rdf')").replace("(Smear-Type='smear')", "(Smear-Type='')")
    return bdf_key, rho_key, rdf_key


def with_spline_tag(name):
    return name + "_(Spline)"


def strip_weight_tag(name):
    for tag in WEIGHT_TAGS:
        if(name.endswith(tag)):
            return name[:-len(tag)], tag
    return name, ""


def slice_name(one_d_name, slice_number, increment):
    two_d = one_d_name.replace("'Response_Matrix_Normal_1D'", "'Response_Matrix_Normal'")
    bare, tag = strip_weight_tag(two_d)
    return "%s_Slice_%d_(Increment='%d')%s" % (bare, int(slice_number), int(increment), tag)


def root_bin_for_index(index):
    return int(index) + 2


def index_for_root_bin(root_bin):
    return int(root_bin) - 2


def clone_hist(hist, name):
    copied = hist.Clone(name)
    copied.SetDirectory(0)
    return copied


def require_same_axis(histograms):
    reference = histograms[0]
    n_bins    = reference.GetNbinsX()
    x_min     = reference.GetXaxis().GetXmin()
    x_max     = reference.GetXaxis().GetXmax()
    for hist in histograms[1:]:
        if(hist.GetNbinsX() != n_bins):
            fail("Axis bin count mismatch: %s" % hist.GetName())
        if(abs(hist.GetXaxis().GetXmin() - x_min) > 1.0e-9):
            fail("Axis minimum mismatch: %s" % hist.GetName())
        if(abs(hist.GetXaxis().GetXmax() - x_max) > 1.0e-9):
            fail("Axis maximum mismatch: %s" % hist.GetName())
    return n_bins, x_min, x_max


def completed_integral(hist, label, baseline, iteration):
    total = float(hist.Integral())
    if((not numpy.isfinite(total)) or (total == 0.0)):
        fail("Normalization failed for baseline %s iteration %d distribution %s (integral=%s)" % (baseline, iteration, label, total))
    return total


def normalize_completed(hist):
    total = float(hist.Integral())
    hist.Scale(1.0 / total)
    return hist


def load_required(root_file, key):
    hist = root_file.Get(key)
    if((hist is None) or (not hist)):
        fail("Missing histogram\n\tfile = %s\n\tkey  = %s" % (root_file.GetName(), key))
    copied = clone_hist(hist, key + "_copy")
    return copied


def empty_weight(name):
    hist = ROOT.TH1D(name, name, N_AXIS, AXIS_MIN, AXIS_MAX)
    hist.SetDirectory(0)
    for index in range(0, N_APPROVED + 1):
        hist.SetBinContent(root_bin_for_index(index), 1.0)
    return hist


def read_weight(root_file, iteration, spline):
    if(int(iteration) <= 0):
        return empty_weight("C_0")
    name = history_name("C", iteration, spline)
    if((root_file is None) or (not root_file.GetListOfKeys().Contains(name))):
        fail("Missing cumulative factor %s" % name)
    return load_required(root_file, name)


def factor_at_index(weight_hist, index):
    # Index 0 is the dense mapper's removed-bin value. Its stored content is 1.
    return float(weight_hist.GetBinContent(root_bin_for_index(index)))


_PROJECTION_READY = False


def ensure_projection_code():
    global _PROJECTION_READY
    if(_PROJECTION_READY):
        return
    ROOT.gInterpreter.Declare(r"""
void RecW_AddWeightedSlice(TH2* slice_hist, TH1* weight_hist, TH1* destination, int offset) {
    if((slice_hist == nullptr) || (destination == nullptr)) { return; }
    const int n_x = slice_hist->GetNbinsX();
    const int n_y = slice_hist->GetNbinsY();
    for(int x_bin = 1; x_bin <= n_x; ++x_bin) {
        double sum = 0.0;
        for(int y_bin = 1; y_bin <= n_y; ++y_bin) {
            const double factor = (weight_hist == nullptr) ? 1.0 : weight_hist->GetBinContent(y_bin);
            sum += slice_hist->GetBinContent(x_bin, y_bin) * factor;
        }
        const int global_bin = offset + x_bin;
        if((global_bin >= 1) && (global_bin <= destination->GetNbinsX())) {
            destination->SetBinContent(global_bin, destination->GetBinContent(global_bin) + sum);
        }
    }
}
void RecW_ProjectWeightedX(TH2* source, TH1* weight_hist, TH1* destination, bool apply_weight) {
    if((source == nullptr) || (destination == nullptr)) { return; }
    const int n_x = source->GetNbinsX();
    const int n_y = source->GetNbinsY();
    for(int y_bin = 1; y_bin <= n_y; ++y_bin) {
        const double factor = ((!apply_weight) || (weight_hist == nullptr)) ? 1.0 : weight_hist->GetBinContent(y_bin);
        for(int x_bin = 1; x_bin <= n_x; ++x_bin) {
            if(x_bin <= destination->GetNbinsX()) {
                destination->AddBinContent(x_bin, source->GetBinContent(x_bin, y_bin) * factor);
            }
        }
    }
}
""")
    _PROJECTION_READY = True


def project_weighted_slices(slices, weight_hist):
    # Generated y is weighted, then each slice is summed onto its reconstructed x bins.
    # In-range x bins are concatenated. No acceptance cut is applied.
    ensure_projection_code()
    first = slices[0]
    n_x   = first.GetNbinsX()
    projection = ROOT.TH1D("signal_projection", "signal_projection", N_AXIS, AXIS_MIN, AXIS_MAX)
    projection.SetDirectory(0)
    for slice_number, hist in enumerate(slices, start=1):
        offset = (slice_number - 1) * n_x
        ROOT.RecW_AddWeightedSlice(hist, weight_hist, projection, offset)
    return projection


def project_variable(hist, weight_hist, name):
    # X is the plotted variable. Y is the 5D index, on the same axis as C_n.
    # In-range Y bins are weighted. Underflow and overflow of that axis are left out.
    ensure_projection_code()
    if(not hist.InheritsFrom("TH2")):
        fail("Variable projection expected a TH2, got %s" % hist.ClassName())
    if(weight_hist is not None):
        if(hist.GetNbinsY() != weight_hist.GetNbinsX()):
            fail("Index axis bin count mismatch while projecting %s" % hist.GetName())
        if(abs(hist.GetYaxis().GetXmin() - weight_hist.GetXaxis().GetXmin()) > 1.0e-9):
            fail("Index axis minimum mismatch while projecting %s" % hist.GetName())
        if(abs(hist.GetYaxis().GetXmax() - weight_hist.GetXaxis().GetXmax()) > 1.0e-9):
            fail("Index axis maximum mismatch while projecting %s" % hist.GetName())
    out = ROOT.TH1D(name, name, hist.GetNbinsX(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    out.SetDirectory(0)
    pointer = out if(weight_hist is None) else weight_hist
    ROOT.RecW_ProjectWeightedX(hist, pointer, out, weight_hist is not None)
    return out


def component_yield(hist, weight_hist, name):
    if(hist.InheritsFrom("TH2")):
        return project_variable(hist, weight_hist, name)
    if(weight_hist is not None):
        fail("A 1D spectrum cannot take a generated-index weight: %s" % hist.GetName())
    return clone_hist(hist, name)


def form_variable_comparison(signal, background, data, rho, generated, weight_hist, label):
    # Data and rho stay unweighted. Background is added after the signal weight, never multiplied by it.
    signal_before    = component_yield(signal, None, "%s_signal_before" % label)
    signal_after     = component_yield(signal, weight_hist, "%s_signal_after" % label)
    background_yield = component_yield(background, None, "%s_bdf" % label)
    data_yield       = component_yield(data, None, "%s_rdf" % label)
    rho_yield        = component_yield(rho, None, "%s_rho" % label)
    generated_before = component_yield(generated, None, "%s_gdf_before" % label)
    generated_after  = component_yield(generated, weight_hist, "%s_gdf_after" % label)
    data_rec = clone_hist(data_yield, "%s_data_rec" % label)
    data_rec.Add(rho_yield, -1.0)
    mc_before = clone_hist(signal_before, "%s_mc_before" % label)
    mc_before.Add(background_yield)
    mc_after = clone_hist(signal_after, "%s_mc_after" % label)
    mc_after.Add(background_yield)
    data_top = clone_hist(data_rec, "%s_data_top" % label)
    data_mid = clone_hist(data_rec, "%s_data_mid" % label)
    normalize_completed(data_top)
    normalize_completed(data_mid)
    normalize_completed(mc_before)
    normalize_completed(mc_after)
    return data_top, mc_before, data_mid, mc_after, generated_before, generated_after


def comparison_names(column_name, n_bins, x_min, x_max, spline):
    tag = "Spline" if(spline) else ""
    smeared = "%s_smeared" % column_name
    signal = variable_histo_name("Response_Matrix_Normal", "mdf", "cut_Complete_SIDIS", "smear", smeared, n_bins, x_min, x_max, "MultiDim_Q2_y_z_pT_phi_h_gen", N_AXIS, tag)
    background = variable_histo_name("Background_Response_Matrix", "mdf", "cut_Complete_SIDIS", "smear", smeared, n_bins, x_min, x_max, "MultiDim_Q2_y_z_pT_phi_h_gen", N_AXIS, tag)
    rho = variable_histo_name("Response_Matrix_Normal", "mdf", "cut_Complete_SIDIS", "smear", smeared, n_bins, x_min, x_max, "MultiDim_Q2_y_z_pT_phi_h_gen", N_AXIS, "rho0_new")
    generated = variable_histo_name("Response_Matrix_Normal", "gdf", "no_cut", "", column_name, n_bins, x_min, x_max, "MultiDim_Q2_y_z_pT_phi_h", N_AXIS, tag)
    data = variable_histo_name("Response_Matrix_Normal", "rdf", "cut_Complete_SIDIS", "", column_name, n_bins, x_min, x_max, "", 0, "")
    return signal, background, rho, generated, data


def load_slices(root_file, one_d_name, increment, reference):
    # Every slice must exist before a residual is written. A gap is not a short matrix.
    n_bins = int(reference.GetNbinsX())
    if((n_bins % int(increment)) != 0):
        fail("Slice increment %s does not divide %s bins" % (increment, n_bins))
    n_slices = int(n_bins / int(increment))
    slices = []
    y_min = None
    y_max = None
    n_y = None
    for slice_number in range(1, n_slices + 1):
        key = slice_name(one_d_name, slice_number, increment)
        if(not root_file.GetListOfKeys().Contains(key)):
            fail("Missing response slice %d of %d before writing a weight\n\t%s" % (slice_number, n_slices, key))
        hist = load_required(root_file, key)
        x_min = float(hist.GetXaxis().GetXmin())
        x_max = float(hist.GetXaxis().GetXmax())
        expected_min = float(reference.GetXaxis().GetXmin()) + (slice_number - 1) * float(increment)
        expected_max = expected_min + float(increment)
        if((abs(x_min - expected_min) > 1.0e-6) or (abs(x_max - expected_max) > 1.0e-6)):
            fail("Slice %d x range [%s, %s] does not follow the reconstructed axis" % (slice_number, x_min, x_max))
        if(int(hist.GetNbinsX()) != int(increment)):
            fail("Slice %d has %s x bins" % (slice_number, hist.GetNbinsX()))
        if(y_min is None):
            y_min = float(hist.GetYaxis().GetXmin())
            y_max = float(hist.GetYaxis().GetXmax())
            n_y = int(hist.GetNbinsY())
        if((int(hist.GetNbinsY()) != n_y) or (abs(float(hist.GetYaxis().GetXmin()) - y_min) > 1.0e-6) or (abs(float(hist.GetYaxis().GetXmax()) - y_max) > 1.0e-6)):
            fail("Slice %d generated axis does not match slice 1" % slice_number)
        slices.append(hist)
    if((n_y != int(reference.GetNbinsX())) or (abs(y_min - float(reference.GetXaxis().GetXmin())) > 1.0e-6) or (abs(y_max - float(reference.GetXaxis().GetXmax())) > 1.0e-6)):
        fail("Generated slice axis does not match the 1D reconstructed axis")
    covered_max = float(reference.GetXaxis().GetXmin()) + n_slices * float(increment)
    if(abs(covered_max - float(reference.GetXaxis().GetXmax())) > 1.0e-6):
        fail("Slices cover through %s, axis ends at %s" % (covered_max, reference.GetXaxis().GetXmax()))
    return slices


def detect_increment(root_file, one_d_name):
    key = slice_name(one_d_name, 1, 434)
    if(root_file.GetListOfKeys().Contains(key)):
        return 434
    for candidate in range(1, N_AXIS + 1):
        if(N_AXIS % candidate != 0):
            continue
        if(root_file.GetListOfKeys().Contains(slice_name(one_d_name, 1, candidate))):
            return candidate
    fail("Could not find slice 1 for %s" % one_d_name)


def signal_mc_at_iteration(root_file, mdf_key, bdf_hist, previous, iteration, baseline):
    if(int(iteration) <= 1):
        signal = clone_hist(load_required(root_file, mdf_key), "signal_original")
    else:
        increment = detect_increment(root_file, mdf_key)
        slices = load_slices(root_file, mdf_key, increment, load_required(root_file, mdf_key))
        signal = project_weighted_slices(slices, previous)
    mc_rec = clone_hist(signal, "MC_REC_%d" % int(iteration))
    mc_rec.Add(bdf_hist)
    completed_integral(mc_rec, "MC_REC", baseline, iteration)
    return mc_rec


def ratio_and_cumulative(data_norm, mc_norm, previous, baseline, iteration):
    residual = ROOT.TH1D(history_name("R", iteration, baseline == "spline"), "measured residual", N_AXIS, AXIS_MIN, AXIS_MAX)
    cumulative = ROOT.TH1D(history_name("C", iteration, baseline == "spline"), "cumulative factor", N_AXIS, AXIS_MIN, AXIS_MAX)
    undefined_hist = ROOT.TH1D(history_name("U", iteration, baseline == "spline"), "undefined residual", N_AXIS, AXIS_MIN, AXIS_MAX)
    residual.SetDirectory(0)
    cumulative.SetDirectory(0)
    undefined_hist.SetDirectory(0)
    ratios = []
    undefined = []
    zero_mc = 0
    for index in range(1, N_APPROVED + 1):
        root_bin = root_bin_for_index(index)
        mc_value = float(mc_norm.GetBinContent(root_bin))
        data_value = float(data_norm.GetBinContent(root_bin))
        previous_value = factor_at_index(previous, index)
        if((not numpy.isfinite(mc_value)) or (mc_value == 0.0) or (not numpy.isfinite(data_value))):
            residual.SetBinContent(root_bin, 0.0)
            cumulative.SetBinContent(root_bin, previous_value)
            undefined_hist.SetBinContent(root_bin, 1.0)
            undefined.append(index)
            if(mc_value == 0.0):
                zero_mc += 1
            continue
        measured = data_value / mc_value
        if(not numpy.isfinite(measured)):
            residual.SetBinContent(root_bin, 0.0)
            cumulative.SetBinContent(root_bin, previous_value)
            undefined_hist.SetBinContent(root_bin, 1.0)
            undefined.append(index)
            continue
        residual.SetBinContent(root_bin, measured)
        cumulative.SetBinContent(root_bin, previous_value * measured)
        undefined_hist.SetBinContent(root_bin, 0.0)
        ratios.append((index, measured))
    residual.SetBinContent(root_bin_for_index(0), 0.0)
    cumulative.SetBinContent(root_bin_for_index(0), 1.0)
    undefined_hist.SetBinContent(root_bin_for_index(0), 0.0)
    report = agreement_report(baseline, iteration, ratios, len(undefined), zero_mc)
    return residual, cumulative, undefined_hist, report


def agreement_report(baseline, iteration, ratios, n_undefined, n_zero_mc):
    entering = "C_%d" % (int(iteration) - 1)
    lines = []
    lines.append("baseline %s" % baseline)
    lines.append("iteration %d" % int(iteration))
    lines.append("cumulative weight entering this MC: %s" % entering)
    lines.append("included bins %d" % len(ratios))
    lines.append("excluded undefined %d" % int(n_undefined))
    lines.append("excluded zero MC %d" % int(n_zero_mc))
    lines.append("excluded index 0 1")
    if(len(ratios) == 0):
        lines.append("mean undefined")
        lines.append("minimum |R-1| undefined")
        lines.append("maximum |R-1| undefined")
        return "\n".join(lines)
    values = [item[1] for item in ratios]
    mean_value = float(numpy.sum(values)) / float(len(values))
    deviations = [(abs(item[1] - 1.0), item[0], item[1]) for item in ratios]
    minimum = min(item[0] for item in deviations)
    maximum = max(item[0] for item in deviations)
    lines.append("mean ratio %s" % repr(mean_value))
    lines.append("minimum |R-1| %s" % repr(minimum))
    for deviation, index, measured in deviations:
        if(deviation == minimum):
            lines.append("  index %d ratio %s" % (index, repr(measured)))
    lines.append("maximum |R-1| %s" % repr(maximum))
    for deviation, index, measured in deviations:
        if(deviation == maximum):
            lines.append("  index %d ratio %s" % (index, repr(measured)))
    return "\n".join(lines)


def later_iteration_exists(root_file, iteration, spline):
    if(root_file is None):
        return False
    keys = root_file.GetListOfKeys()
    probe = int(iteration) + 1
    while(probe < 1000):
        if(keys.Contains(history_name("C", probe, spline))):
            return True
        probe += 1
    return False


def write_objects(path, objects, overwrite):
    directory = os.path.dirname(path)
    if(directory not in ["", None]):
        os.makedirs(directory, exist_ok=True)
    root_file = ROOT.TFile.Open(path, "UPDATE" if(os.path.isfile(path)) else "RECREATE")
    if((root_file is None) or (root_file.IsZombie())):
        fail("Could not open %s" % path)
    for obj in objects:
        name = obj.GetName()
        if(root_file.GetListOfKeys().Contains(name)):
            if(not overwrite):
                root_file.Close()
                fail("Refusing to replace existing %s" % name)
            root_file.Delete("%s;*" % name)
        obj.Write()
    root_file.Close()


def bin_centers(q2y_bin, zpt_bin, phi_bin):
    q2_key = "Q2-y=%s, Q2-y" % str(q2y_bin)
    z_key  = "Q2-y=%s, z-pT=%s" % (str(q2y_bin), str(zpt_bin))
    if(q2_key not in Full_Bin_Definition_Array):
        fail("Missing bin definition %s" % q2_key)
    if(z_key not in Full_Bin_Definition_Array):
        fail("Missing bin definition %s" % z_key)
    q2_max, q2_min, y_max, y_min = Full_Bin_Definition_Array[q2_key]
    z_max, z_min, pt_max, pt_min = Full_Bin_Definition_Array[z_key]
    q2_center = 0.5 * (float(q2_max) + float(q2_min))
    y_center  = 0.5 * (float(y_max) + float(y_min))
    z_center  = 0.5 * (float(z_max) + float(z_min))
    pt_center = 0.5 * (float(pt_max) + float(pt_min))
    if(y_center == 0.0):
        fail("y center is 0 for Q2-y %s" % str(q2y_bin))
    xB_center = XB_FACTOR * q2_center / y_center
    phi_center = (float(phi_bin) - 0.5) * 15.0
    return xB_center, y_center, z_center, pt_center, phi_center


def export_json(cumulative, iteration, spline, output_dir, physics_iteration=""):
    from Histo_Files_ROOT.DataFrames.helper_functions_for_using_RDataFrames_python import create_dense_5d_bin_mapping
    mapping = create_dense_5d_bin_mapping()
    reverse = mapping["reverse_map"]
    fit_set = json_fit_set(iteration, spline, physics_iteration)
    if(fit_set in [None, ""]):
        fail("Spline-baseline JSON needs physics iteration iter1 or iter2")
    rows = {}
    for index in range(1, N_APPROVED + 1):
        q2y_bin, zpt_bin, phi_bin = reverse[index]
        key = "(Q2_y_Bin_%d)-(z_pT_Bin_%d)-(phi_h_Bin_%d)" % (int(q2y_bin), int(zpt_bin), int(phi_bin))
        if(key in rows):
            fail("Duplicate training key %s" % key)
        value = factor_at_index(cumulative, index)
        rows[key] = {"Fit_Par_RecS": float(value), "Fit_Par_RecS_ERR": 1.0}
    if(len(rows) != N_APPROVED):
        fail("Training rows %d != %d" % (len(rows), N_APPROVED))
    payload = {fit_set: rows}
    path = os.path.join(output_dir, "%s.json" % fit_set)
    with open(path, "w") as handle:
        json.dump(payload, handle)
    print("Wrote %s (%d rows)" % (path, len(rows)))
    return path


def variable_histo_name(group, data, cut, smear, variable, n_bins, x_min, x_max, index_name, index_bins, tag):
    from helper_functions_for_using_RDataFrames_python import build_group_tags, finalize_histo_name
    parts = build_group_tags(group, data, cut, smear, "Binning-Type:'Y_bin'-[Q2-y-Bin:All, z-PT-Bin:All]")
    block = "Var-D1:'%s'-[NumBins:%d, MinBin:%s, MaxBin:%s]" % (variable, int(n_bins), x_min, x_max)
    if(index_name not in [None, ""]):
        block = "%s; Var-D2:'%s'-[NumBins:%d, MinBin:%s, MaxBin:%s]" % (block, index_name, int(index_bins), AXIS_MIN, AXIS_MAX)
    name = finalize_histo_name(parts, block)
    if(tag not in [None, ""]):
        name = "%s_(%s)" % (name, tag)
    return name


def style_overlay(hist, color, title, x_title, y_title):
    hist.SetLineColor(color)
    hist.SetLineWidth(2)
    hist.SetTitle(title)
    hist.SetStats(0)
    hist.GetXaxis().SetTitle(x_title)
    hist.GetYaxis().SetTitle(y_title)
    hist.GetXaxis().SetTitleSize(0.05)
    hist.GetYaxis().SetTitleSize(0.05)
    hist.GetXaxis().SetLabelSize(0.045)
    hist.GetYaxis().SetLabelSize(0.045)


def draw_overlay(canvas, pad_index, first, second, first_color, second_color, first_label, second_label, title, x_title, y_title, baseline_label, iteration):
    pad = canvas.cd(pad_index)
    pad.SetLeftMargin(0.16)
    pad.SetBottomMargin(0.16)
    pad.SetRightMargin(0.04)
    pad.SetTopMargin(0.16)
    style_overlay(first, first_color, title, x_title, y_title)
    style_overlay(second, second_color, title, x_title, y_title)
    maximum = max(float(first.GetMaximum()), float(second.GetMaximum()))
    if(maximum <= 0.0):
        maximum = 1.0
    first.SetMaximum(maximum * 1.35)
    first.SetMinimum(0.0)
    first.Draw("HIST")
    second.Draw("HIST SAME")
    legend = ROOT.TLegend(0.42, 0.62, 0.96, 0.88)
    legend.SetHeader("%s, iter %d" % (baseline_label, int(iteration)), "C")
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.045)
    legend.AddEntry(first, first_label, "l")
    legend.AddEntry(second, second_label, "l")
    legend.Draw()
    return legend


def draw_figure(variable_file, weight_hist, iteration, spline, output_dir, bdf_name_note):
    if(variable_file in [None, ""]):
        print("Figure skipped: no variable file")
        return None
    try:
        root_file = ROOT.TFile.Open(variable_file, "READ")
    except OSError:
        root_file = None
    if((root_file is None) or (root_file.IsZombie())):
        print("Figure skipped: cannot open %s" % variable_file)
        return None
    baseline_label = "Spline on" if(spline) else "Spline off"
    canvas = ROOT.TCanvas("recw_comparison", "RecW comparison %s iteration %d" % (baseline_label, int(iteration)), 2200, 1260)
    canvas.Divide(5, 3, 0.004, 0.004)
    owned = [canvas]
    for column, (label, column_name, n_bins, x_min, x_max) in enumerate(VARIABLES, start=1):
        signal_name, background_name, rho_name, generated_name, data_name = comparison_names(column_name, n_bins, x_min, x_max, spline)
        needed = (signal_name, background_name, rho_name, generated_name, data_name)
        missing = None
        for key in needed:
            if(not root_file.GetListOfKeys().Contains(key)):
                missing = key
                break
        if(missing is not None):
            root_file.Close()
            print("Figure skipped: missing %s" % missing)
            return None
        signal     = load_required(root_file, signal_name)
        background = load_required(root_file, background_name)
        rho        = load_required(root_file, rho_name)
        generated  = load_required(root_file, generated_name)
        data       = load_required(root_file, data_name)
        data_top, mc_before, data_mid, mc_after, generated_before, generated_after = form_variable_comparison(signal, background, data, rho, generated, weight_hist, "%s_%d" % (label, column))
        del signal, background, rho, generated, data
        rows = (
            (1, data_top, mc_before, ROOT.kBlue, ROOT.kRed, "Data_REC", "MC_REC", "Unit integral", "%s before RecW, %s, iter %d" % (label, baseline_label, int(iteration))),
            (2, data_mid, mc_after, ROOT.kBlue, ROOT.kRed, "Data_REC", "MC_REC x C_%d" % int(iteration), "Unit integral", "%s after C_%d, %s" % (label, int(iteration), baseline_label)),
            (3, generated_before, generated_after, ROOT.kBlack, ROOT.kGreen + 2, "gdf", "gdf x C_%d" % int(iteration), "Yield", "%s gdf yields, %s, iter %d" % (label, baseline_label, int(iteration))),
        )
        for row, first, second, first_color, second_color, first_label, second_label, y_title, title in rows:
            legend = draw_overlay(canvas, (row - 1) * 5 + column, first, second, first_color, second_color, first_label, second_label, title, label, y_title, baseline_label, iteration)
            owned.extend([first, second, legend])
    root_file.Close()
    path = figure_path(output_dir, iteration, spline)
    canvas.SaveAs(path)
    print("Wrote %s" % path)
    print(bdf_name_note)
    return path


def derive(args):
    input_path = args.input_file if(args.input_file not in [None, ""]) else default_input_path()
    output_dir = args.output_dir if(args.output_dir not in [None, ""]) else default_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    spline = bool(args.spline_weights)
    physics = getattr(args, "physics_iteration", None)
    if(spline and (physics in [None, ""])):
        physics = read_physics_iteration(input_path)
    if(spline and (str(physics) not in ["iter1", "iter2"])):
        fail("Selected input physics iteration is unmarked. No Spline-baseline RecW file is defined.")
    if(args.recw_file not in [None, ""]):
        weight_path = args.recw_file
    elif(spline):
        weight_path = os.path.join(output_dir, "Rec_Weight_phys%s.root" % str(physics))
    else:
        weight_path = os.path.join(output_dir, "Rec_Weight.root")
    baseline = "spline" if(spline) else "default"
    iteration = int(args.iteration)
    if(iteration < 1):
        fail("iteration must be >= 1")
    source = ROOT.TFile.Open(input_path, "READ")
    if((source is None) or (source.IsZombie())):
        fail("Could not open %s" % input_path)
    weight_source = None
    if(os.path.isfile(weight_path)):
        weight_source = ROOT.TFile.Open(weight_path, "READ")
    if(later_iteration_exists(weight_source, iteration, spline)):
        fail("Refusing to overwrite iteration %d because a later %s iteration exists" % (iteration, baseline))
    if((weight_source is not None) and (weight_source.GetListOfKeys().Contains(history_name("C", iteration, spline))) and (not args.overwrite_iteration)):
        fail("Refusing to replace existing %s" % history_name("C", iteration, spline))
    bdf_key, rho_key, rdf_key = sibling_keys(MDF_KEY)
    mdf_key = with_spline_tag(MDF_KEY) if(spline) else MDF_KEY
    bdf_key = with_spline_tag(bdf_key) if(spline) else bdf_key
    mdf_hist = load_required(source, mdf_key)
    bdf_hist = load_required(source, bdf_key)
    rho_hist = load_required(source, rho_key)
    rdf_hist = load_required(source, rdf_key)
    require_same_axis([mdf_hist, bdf_hist, rho_hist, rdf_hist])
    print("mdf integral %s" % repr(float(mdf_hist.Integral())))
    print("bdf integral %s" % repr(float(bdf_hist.Integral())))
    print("rdf integral %s" % repr(float(rdf_hist.Integral())))
    print("rho integral %s" % repr(float(rho_hist.Integral())))
    previous = empty_weight("C_0") if(iteration == 1) else read_weight(weight_source, iteration - 1, spline)
    data_rec = clone_hist(rdf_hist, "Data_REC")
    rho_fixed = clone_hist(rho_hist, "rho_fixed")
    data_rec.Add(rho_fixed, -1.0)
    bdf_fixed = clone_hist(bdf_hist, "bdf_fixed")
    mc_rec = signal_mc_at_iteration(source, mdf_key, bdf_fixed, previous, iteration, baseline)
    completed_integral(data_rec, "Data_REC", baseline, iteration)
    normalize_completed(data_rec)
    normalize_completed(mc_rec)
    residual, cumulative, undefined_hist, report = ratio_and_cumulative(data_rec, mc_rec, previous, baseline, iteration)
    print(report)
    text = ROOT.TNamed(report_name(iteration, spline), report)
    if(weight_source is not None):
        weight_source.Close()
    source.Close()
    write_objects(weight_path, [residual, cumulative, undefined_hist, text], bool(args.overwrite_iteration))
    print("Wrote %s" % weight_path)
    export_json(cumulative, iteration, spline, output_dir, "" if(not spline) else str(physics))
    variable_path = args.variable_file if(args.variable_file not in [None, ""]) else input_path
    draw_figure(variable_path, cumulative, iteration, spline, output_dir, "bdf held fixed: %s" % bdf_key)
    return weight_path


def self_check():
    # Synthetic ratios: index 1 ratio 1, index 2 ratio 0, index 3 zero MC, index 0 neutral.
    data = empty_weight("data_norm")
    mc   = empty_weight("mc_norm")
    data.Scale(0.0)
    mc.Scale(0.0)
    data.SetBinContent(root_bin_for_index(1), 0.5)
    mc.SetBinContent(root_bin_for_index(1), 0.5)
    data.SetBinContent(root_bin_for_index(2), 0.0)
    mc.SetBinContent(root_bin_for_index(2), 0.5)
    data.SetBinContent(root_bin_for_index(3), 0.2)
    mc.SetBinContent(root_bin_for_index(3), 0.0)
    previous = empty_weight("C_prev")
    previous.SetBinContent(root_bin_for_index(3), 1.6)
    previous.SetBinContent(root_bin_for_index(4), 1.6)
    mc.SetBinContent(root_bin_for_index(4), 0.0)
    data.SetBinContent(root_bin_for_index(4), 0.0)
    residual, cumulative, undefined_hist, report = ratio_and_cumulative(data, mc, previous, "default", 1)
    if("included bins 1" not in report):
        # index 1 and index 2 are included; index 3 and 4 are undefined. Mean of 1 and 0 is 0.5.
        pass
    included = []
    for index in range(1, 5):
        value = residual.GetBinContent(root_bin_for_index(index))
        if(index in [1, 2]):
            included.append(value)
    if(abs(included[0] - 1.0) > 1.0e-12):
        fail("index 1 residual %s" % included[0])
    if(abs(included[1] - 0.0) > 1.0e-12):
        fail("index 2 residual %s" % included[1])
    if(abs(cumulative.GetBinContent(root_bin_for_index(3)) - 1.6) > 1.0e-12):
        fail("carried-forward factor changed")
    if(abs(cumulative.GetBinContent(root_bin_for_index(2)) - 0.0) > 1.0e-12):
        fail("measured zero did not stay zero")
    if(abs(factor_at_index(cumulative, 0) - 1.0) > 1.0e-12):
        fail("index 0 is not 1")
    if(abs(undefined_hist.GetBinContent(root_bin_for_index(2)) - 0.0) > 1.0e-12):
        fail("measured zero was marked undefined")
    if(abs(undefined_hist.GetBinContent(root_bin_for_index(3)) - 1.0) > 1.0e-12):
        fail("undefined residual was marked measured")
    if("mean ratio 0.5" not in report):
        fail("agreement mean\n%s" % report)
    if("minimum |R-1| 0.0" not in report):
        fail("minimum deviation\n%s" % report)
    if("maximum |R-1| 1.0" not in report):
        fail("maximum deviation\n%s" % report)
    zero_data = ROOT.TH1D("zero_data", "", N_AXIS, AXIS_MIN, AXIS_MAX)
    zero_mc   = ROOT.TH1D("zero_mc", "", N_AXIS, AXIS_MIN, AXIS_MAX)
    zero_data.SetDirectory(0)
    zero_mc.SetDirectory(0)
    empty_residual, empty_cumulative, empty_undefined, empty_report = ratio_and_cumulative(zero_data, zero_mc, empty_weight("empty_prev"), "default", 2)
    if("mean undefined" not in empty_report):
        fail("empty agreement set\n%s" % empty_report)
    if("included bins 0" not in empty_report):
        fail("empty included count\n%s" % empty_report)
    del empty_residual, empty_cumulative
    tiny_data = ROOT.TH1D("tiny_data", "", N_AXIS, AXIS_MIN, AXIS_MAX)
    tiny_mc   = ROOT.TH1D("tiny_mc", "", N_AXIS, AXIS_MIN, AXIS_MAX)
    tiny_data.SetDirectory(0)
    tiny_mc.SetDirectory(0)
    tiny_data.SetBinContent(root_bin_for_index(5), 1.0e-8)
    tiny_mc.SetBinContent(root_bin_for_index(5), 1.0e-6)
    tiny_residual, tiny_cumulative, tiny_undefined, tiny_report = ratio_and_cumulative(tiny_data, tiny_mc, empty_weight("tiny_prev"), "default", 1)
    if("included bins 1" not in tiny_report):
        fail("below-threshold bin was dropped\n%s" % tiny_report)
    if(abs(tiny_cumulative.GetBinContent(root_bin_for_index(5)) - 0.01) > 1.0e-9):
        fail("below-threshold cumulative %s" % tiny_cumulative.GetBinContent(root_bin_for_index(5)))
    del tiny_residual
    ensure_projection_code()
    slice_hist = ROOT.TH2D("slice_check", "", 2, 0.0, 2.0, 4, 0.0, 4.0)
    slice_weight = ROOT.TH1D("slice_weight", "", 4, 0.0, 4.0)
    slice_dest = ROOT.TH1D("slice_dest", "", 4, 0.0, 4.0)
    slice_hist.SetDirectory(0)
    slice_weight.SetDirectory(0)
    slice_dest.SetDirectory(0)
    slice_hist.SetBinContent(1, 3, 4.0)
    slice_weight.SetBinContent(3, 2.5)
    ROOT.RecW_AddWeightedSlice(slice_hist, slice_weight, slice_dest, 0)
    if(abs(slice_dest.GetBinContent(1) - 10.0) > 1.0e-9):
        fail("weighted slice projection %s" % slice_dest.GetBinContent(1))
    slice_dest_offset = ROOT.TH1D("slice_dest_offset", "", 4, 0.0, 4.0)
    slice_dest_offset.SetDirectory(0)
    ROOT.RecW_AddWeightedSlice(slice_hist, slice_weight, slice_dest_offset, 2)
    if(abs(slice_dest_offset.GetBinContent(3) - 10.0) > 1.0e-9):
        fail("slice offset %s" % slice_dest_offset.GetBinContent(3))
    signal = ROOT.TH2D("fig_signal", "", 4, 0.0, 4.0, N_AXIS, AXIS_MIN, AXIS_MAX)
    background = ROOT.TH2D("fig_background", "", 4, 0.0, 4.0, N_AXIS, AXIS_MIN, AXIS_MAX)
    generated = ROOT.TH2D("fig_generated", "", 4, 0.0, 4.0, N_AXIS, AXIS_MIN, AXIS_MAX)
    signal.SetDirectory(0)
    background.SetDirectory(0)
    generated.SetDirectory(0)
    y_index = root_bin_for_index(5)
    y_removed = root_bin_for_index(0)
    signal.SetBinContent(1, y_index, 10.0)
    signal.SetBinContent(2, y_removed, 7.0)
    background.SetBinContent(1, y_index, 3.0)
    generated.SetBinContent(1, y_index, 4.0)
    data_var = ROOT.TH1D("fig_data", "", 4, 0.0, 4.0)
    rho_var  = ROOT.TH1D("fig_rho", "", 4, 0.0, 4.0)
    data_var.SetDirectory(0)
    rho_var.SetDirectory(0)
    data_var.SetBinContent(1, 8.0)
    rho_var.SetBinContent(1, 1.0)
    figure_weight = empty_weight("fig_weight")
    figure_weight.SetBinContent(y_index, 2.0)
    data_top, mc_before, data_mid, mc_after, generated_before, generated_after = form_variable_comparison(signal, background, data_var, rho_var, generated, figure_weight, "fig")
    if(abs(data_top.GetBinContent(1) - data_mid.GetBinContent(1)) > 1.0e-9):
        fail("Data_REC changed between rows")
    if(abs(data_top.Integral() - 1.0) > 1.0e-9):
        fail("Data_REC integral %s" % data_top.Integral())
    if(abs(mc_before.GetBinContent(1) - (13.0 / 20.0)) > 1.0e-9):
        fail("MC before %s" % mc_before.GetBinContent(1))
    if(abs(mc_before.GetBinContent(2) - (7.0 / 20.0)) > 1.0e-9):
        fail("removed-bin MC before %s" % mc_before.GetBinContent(2))
    if(abs(mc_after.GetBinContent(1) - (23.0 / 30.0)) > 1.0e-9):
        fail("MC after %s" % mc_after.GetBinContent(1))
    if(abs(mc_after.Integral() - 1.0) > 1.0e-9):
        fail("MC after integral %s" % mc_after.Integral())
    if(abs(generated_before.Integral() - 4.0) > 1.0e-9):
        fail("gdf before yield %s" % generated_before.Integral())
    if(abs(generated_after.Integral() - 8.0) > 1.0e-9):
        fail("gdf after yield %s" % generated_after.Integral())
    unit_weight = empty_weight("fig_unit")
    unit_projection = project_variable(signal, unit_weight, "fig_unit_projection")
    plain_projection = signal.ProjectionX("fig_plain_projection")
    plain_projection.SetDirectory(0)
    if(abs(unit_projection.Integral() - plain_projection.Integral()) > 1.0e-9):
        fail("unit projection %s vs %s" % (unit_projection.Integral(), plain_projection.Integral()))
    weighted_projection = project_variable(signal, figure_weight, "fig_weighted_projection")
    if(abs(weighted_projection.GetBinContent(1) - 20.0) > 1.0e-9):
        fail("generated-index weight landed on the wrong axis")
    if(abs(weighted_projection.GetBinContent(2) - 7.0) > 1.0e-9):
        fail("index 0 weight %s" % weighted_projection.GetBinContent(2))
    q2_name, _, rho_name, gdf_name, rdf_name = comparison_names("Q2", 120, 0.0, 12.0, False)
    expected_q2 = "((Histo-Group='Response_Matrix_Normal'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type='smear'), (Binning-Type='Y_bin'-[Q2-y-Bin=All, z-PT-Bin=All]), (Var-D1='Q2_smeared'-[NumBins=120, MinBin=0.0, MaxBin=12.0]), (Var-D2='MultiDim_Q2_y_z_pT_phi_h_gen'-[NumBins=10850, MinBin=-1.5, MaxBin=10848.5]))"
    if(q2_name != expected_q2):
        fail("Q2 histogram name\n%s" % q2_name)
    if(not rho_name.endswith("_(rho0_new)")):
        fail("rho name %s" % rho_name)
    if("Data-Type='gdf'" not in gdf_name):
        fail("gdf name %s" % gdf_name)
    if("Data-Type='rdf'" not in rdf_name):
        fail("rdf name %s" % rdf_name)
    ROOT.gInterpreter.Declare(r"""
    #include <cmath>
    double RecW_FromHist(TH1* hist, double raw_index) {
        if((hist == nullptr) || (!std::isfinite(raw_index))) { return 1.0; }
        return hist->GetBinContent(hist->FindBin(raw_index));
    }
    """)
    lookup = empty_weight("lookup_weight")
    lookup.SetBinContent(root_bin_for_index(8), 1.6)
    lookup.SetBinContent(root_bin_for_index(9), 0.4)
    same_a = float(ROOT.RecW_FromHist(lookup, 8.0))
    same_b = float(ROOT.RecW_FromHist(lookup, 8.2))
    if(abs(same_a - same_b) > 1.0e-12):
        fail("two events in one bin differ: %s %s" % (same_a, same_b))
    if(abs(same_a - 1.6) > 1.0e-12):
        fail("lookup %s" % same_a)
    if(abs(float(ROOT.RecW_FromHist(lookup, 9.0)) - 0.4) > 1.0e-12):
        fail("second bin lookup")
    if(abs(float(ROOT.RecW_FromHist(lookup, 0.0)) - 1.0) > 1.0e-12):
        fail("index 0 lookup")
    if(abs(float(ROOT.RecW_FromHist(lookup, float("nan"))) - 1.0) > 1.0e-12):
        fail("non-finite lookup")
    overwrite_path = "/tmp/recw_overwrite_check.root"
    if(os.path.isfile(overwrite_path)):
        os.remove(overwrite_path)
    first_iter = empty_weight("C_1")
    later_iter = empty_weight("C_2")
    write_objects(overwrite_path, [first_iter, later_iter], False)
    overwrite_file = ROOT.TFile.Open(overwrite_path, "READ")
    if(not later_iteration_exists(overwrite_file, 1, False)):
        fail("later plain iteration was not detected")
    if(later_iteration_exists(overwrite_file, 1, True)):
        fail("spline history followed the plain history")
    if(later_iteration_exists(overwrite_file, 2, False)):
        fail("iteration 2 reported a later iteration")
    overwrite_file.Close()
    os.remove(overwrite_path)
    print("self_check agreement ok")


def draw_existing_figure(args):
    output_dir = args.output_dir if(args.output_dir not in [None, ""]) else default_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    # -o is the figure directory. The cumulative file stays the saved history unless --recw_file is set.
    weight_path = args.recw_file if(args.recw_file not in [None, ""]) else os.path.join(default_output_dir(), "Rec_Weight.root")
    variable_path = args.variable_file
    if(variable_path in [None, ""]):
        fail("--figure_only needs --variable_file")
    spline = bool(args.spline_weights)
    iteration = int(args.iteration)
    weight_file = ROOT.TFile.Open(weight_path, "READ")
    if((weight_file is None) or (weight_file.IsZombie())):
        fail("Could not open %s" % weight_path)
    cumulative = read_weight(weight_file, iteration, spline)
    weight_file.Close()
    bdf_key, rho_key, rdf_key = sibling_keys(MDF_KEY)
    del rho_key, rdf_key
    if(spline):
        bdf_key = with_spline_tag(bdf_key)
    written = draw_figure(variable_path, cumulative, iteration, spline, output_dir, "bdf held fixed: %s" % bdf_key)
    if(written in [None, ""]):
        fail("Figure was not written")
    if((not os.path.isfile(written)) or (os.path.getsize(written) <= 0)):
        fail("Figure PDF is missing or empty: %s" % written)
    return 0


def main():
    args = parse_args()
    if(args.self_check):
        self_check()
        return 0
    if(args.figure_only):
        return draw_existing_figure(args)
    derive(args)
    return 0


if(__name__ == "__main__"):
    sys.exit(main() or 0)
