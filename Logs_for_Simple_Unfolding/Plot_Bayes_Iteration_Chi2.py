#!/usr/bin/env python3
"""Plot Bayesian-unfolding iteration χ² diagnostics from RooUnfold .out logs.

Module top is stdlib only so `from Plot_Bayes_Iteration_Chi2 import parse_unfold_log`
does not import ROOT or MyCommonAnalysisFunction_richcap.
"""

import argparse
import glob
import math
import os
import re
import statistics
import sys

_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

# ========================= USER DEFAULTS =========================
DEFAULT_Y_VARS          = ["chi2"]
DEFAULT_FORMATS         = ["pdf"]          # subset of {"pdf", "root"}
DEFAULT_OUTDIR          = os.path.join(_SCRIPT_DIR, "Plots")
DEFAULT_NAME            = "Bayes_Iteration_Chi2"
DEFAULT_CANVAS_WIDTH    = 1200
DEFAULT_CANVAS_HEIGHT   = 900
DEFAULT_DRAW_OPTION     = "HIST LP"        # user-facing; split per Drawing contract
DEFAULT_LEG             = [0.62, 0.74, 0.89, 0.89]  # compact upper-right; override with --leg for 17-bin overlays
DEFAULT_LINE_WIDTH      = 2
DEFAULT_MARKER_SIZE     = 1.1
DEFAULT_LOGY            = False
DEFAULT_BLOCK           = "first"          # first | last | all
DEFAULT_XTITLE          = "Number of Bayesian Iterations"
Y_AXIS_TITLES = {
    "chi2":             "#chi^{2} of change",
    "ratio":            "Ratio to last #chi^{2}",
    "reduced_chi2":     "Reduced #chi^{2} of change",
    "ratio_of_ratios":  "Ratio of ratios",
}
Y_VAR_CHOICES = tuple(Y_AXIS_TITLES.keys())
# =================================================================

KEEP = []
_ANSI_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
_VECTOR_RE = re.compile(r"^Vector \((\d+)\)\s+is as follows")


class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass


class UnfoldLogSeries:
    def __init__(self, path, label="", family="", dim="unknown", q2y_bin=None, n_bins=None,
                 n_bins_source="none", block_index=0, chi2=None):
        self.path = path
        self.label = label
        self.family = family
        self.dim = dim
        self.q2y_bin = q2y_bin
        self.n_bins = n_bins
        self.n_bins_source = n_bins_source
        self.block_index = block_index
        self.chi2 = chi2 if(chi2 is not None) else {}


def strip_ansi(text):
    return _ANSI_RE.sub("", text)


def extract_q2y_bin_from_filename(path):
    base = os.path.basename(path)
    if("Q2_y_Bin_" not in base):
        return None
    tail = base.split("Q2_y_Bin_")[-1]
    for ext in (".out", ".log"):
        tail = tail.replace(ext, "")
    try:
        return int(tail)
    except ValueError:
        m = re.match(r"(\d+)", tail)
        return int(m.group(1)) if(m) else None


def infer_family_and_dim(path):
    base = os.path.basename(path)
    name = re.sub(r"\.(out|log)$", "", base, flags=re.IGNORECASE)
    if("5D_Bins_All" in name):
        dim = "5D"
    elif("Q2_y_Bin_" in name):
        dim = "3D"
    else:
        dim = "unknown"
    family = re.sub(r"_Log_of_.*$", "", name)
    return family, dim


def auto_legend_label(path, mixed_families=False):
    family, dim = infer_family_and_dim(path)
    q2y_bin = extract_q2y_bin_from_filename(path)
    generic_family = (family == "Unfold")
    if(dim == "5D"):
        if(generic_family):
            return "5D"
        return f"5D ({family})"
    if(q2y_bin is not None):
        label = f"Q^{{2}}-y {q2y_bin}"
        if(mixed_families):
            return f"{family} {label}"
        return label
    base = os.path.basename(path)
    return re.sub(r"\.(out|log)$", "", base, flags=re.IGNORECASE)


def _parse_numbins_token(line):
    if("NumBins=" not in line):
        return None
    head = line.split("Var-D2")[0] if("Var-D2" in line) else line
    try:
        token = head.split("NumBins=", 1)[1]
        token = token.split(",")[0].split("]")[0].strip()
        return int(token)
    except (IndexError, ValueError):
        return None


def extract_num_bins(text_lines, q2y_bin=None, cli_n_bins=None):
    if(cli_n_bins not in [None, ""]):
        return int(cli_n_bins), "cli"
    unfolding_3d_fallback = None
    for line in text_lines:
        if(("Unfolding:" in line) and ("Histo-Group=" in line) and ("Var-D1='MultiDim_z_pT_Bin_Y_bin_phi_t'" in line)):
            if(q2y_bin is not None):
                needle = f"[Q2-y-Bin={q2y_bin}, z-PT-Bin=All]"
                if(needle not in line):
                    if(unfolding_3d_fallback is None):
                        unfolding_3d_fallback = _parse_numbins_token(line)
                    continue
            n = _parse_numbins_token(line)
            if(n is not None):
                return n, "unfolding_3d"
    if((q2y_bin is None) and (unfolding_3d_fallback is not None)):
        return unfolding_3d_fallback, "unfolding_3d"
    for line in text_lines:
        if(("Unfolding:" in line) and ("Var-D1='MultiDim_Q2_y_z_pT_phi_h'" in line)):
            n = _parse_numbins_token(line)
            if(n is not None):
                return n, "unfolding_5d"
    for line in text_lines:
        m = _VECTOR_RE.match(line.strip())
        if(m):
            return int(m.group(1)), "vector"
    return None, "none"


def parse_unfold_log(path, block="first", cli_n_bins=None, verbose=False):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            raw_lines = handle.readlines()
    except OSError as exc:
        print(f"WARNING: could not read '{path}': {exc}", file=sys.stderr)
        return []
    stripped_lines = [strip_ansi(line).strip() for line in raw_lines]
    blocks = []
    current_pairs = []
    current_iteration = None
    seen_now_unfolding = False
    for stripped in stripped_lines:
        if("Now unfolding" in stripped):
            if(current_pairs):
                blocks.append(current_pairs)
                current_pairs = []
            current_iteration = None
            seen_now_unfolding = True
            continue
        if("Iteration :" in stripped):
            try:
                iter_part = stripped.split(":", 1)[1].strip()
                current_iteration = int(iter_part)
            except (IndexError, ValueError):
                current_iteration = None
        elif(("Chi^2 of change" in stripped) and (current_iteration is not None)):
            try:
                chi_value = float(stripped.split()[-1])
                current_pairs.append((current_iteration, chi_value))
            except (IndexError, ValueError):
                pass
            current_iteration = None
    if(current_pairs):
        blocks.append(current_pairs)
    if(not blocks):
        print(f"WARNING: no Iteration / Chi^2 of change pairs in '{path}'", file=sys.stderr)
        return []
    if(block == "first"):
        selected = [blocks[0]]
        indices = [0]
    elif(block == "last"):
        selected = [blocks[-1]]
        indices = [len(blocks) - 1]
    else:
        selected = blocks
        indices = list(range(len(blocks)))
    family, dim = infer_family_and_dim(path)
    q2y_bin = extract_q2y_bin_from_filename(path)
    n_bins, n_bins_source = extract_num_bins(stripped_lines, q2y_bin=q2y_bin, cli_n_bins=cli_n_bins)
    out = []
    for sel, bidx in zip(selected, indices):
        chi2 = {}
        for iteration, value in sel:
            if((iteration in chi2) and verbose):
                print(f"WARNING: duplicate iteration {iteration} in '{path}' block {bidx}; last value wins")
            chi2[iteration] = value
        out.append(UnfoldLogSeries(
            path=os.path.abspath(path),
            family=family,
            dim=dim,
            q2y_bin=q2y_bin,
            n_bins=n_bins,
            n_bins_source=n_bins_source,
            block_index=bidx,
            chi2=chi2,
        ))
    if(verbose and (not seen_now_unfolding)):
        print(f"WARNING: '{path}' has χ² pairs but no 'Now unfolding' line")
    return out


def _natural_key(path):
    base = os.path.basename(path)
    m = re.search(r"Q2_y_Bin_(\d+)", base)
    bin_n = int(m.group(1)) if(m) else -1
    return (0 if("5D" in base) else 1, bin_n, base)


def expand_log_paths(tokens):
    out = []
    for tok in tokens:
        tok = os.path.expanduser(str(tok))
        if(os.path.isdir(tok)):
            matches = sorted(glob.glob(os.path.join(tok, "*.out")), key=_natural_key)
        elif(any(ch in tok for ch in "*?[]")):
            matches = sorted(glob.glob(tok), key=_natural_key)
        else:
            matches = [tok]
        if(not matches):
            raise FileNotFoundError(f"No log files matched: {tok}")
        out.extend(matches)
    seen = set()
    uniq = []
    for path in out:
        ap = os.path.abspath(path)
        if(ap in seen):
            continue
        if(not os.path.isfile(ap)):
            raise FileNotFoundError(ap)
        seen.add(ap)
        uniq.append(ap)
    return uniq


def parse_args():
    p = argparse.ArgumentParser(
        description="Plot Bayesian-unfolding iteration diagnostics from RooUnfold .out logs.\n"
                    "Reads 'Iteration : N' / 'Chi^2 of change <float>' pairs (same contract as\n"
                    "Check_Log_Files_for_Iteration_Changes.py), derives Excel-style metrics, and\n"
                    "overlays TH1D series on one canvas per --y_var.\n"
                    "-f/--log_file is the input log (not a fit flag).\n",
        formatter_class=RawDefaultsHelpFormatter,
    )
    p.add_argument("-f", "--log_file",
                   nargs="+",
                   type=str,
                   required=True,
                   help="Path(s) to `.out` log files (**not** a fit flag). Each token is glob-expanded (`*` `?` `[]`).\n"
                        "A directory is expanded to `*.out` inside it. Shell brace expansion\n"
                        "(`Unfold_*_Q2_y_Bin_{1..17}.out`) also works if the shell expands it before Python sees it.\n"
                        "Explicit files keep CLI order; globs/directories are natural-sorted within that token.\n")
    p.add_argument("-L", "--legend",
                   nargs="+",
                   type=str,
                   default=None,
                   help="Legend labels, one per **expanded** log file, in the same order.\n"
                        "If omitted, labels are auto-built from the filename (Q^{2}-y bin, 5D, unfolding family).\n")
    p.add_argument("--block",
                   choices=["first", "last", "all"],
                   default=DEFAULT_BLOCK,
                   help="Which `Now unfolding...` block to keep when a log contains more than one iteration series.\n"
                        "Default `first` matches current 3D/5D logs (one series). `all` overlays each block as its own series.\n")
    p.add_argument("-y", "--y_var",
                   nargs="+",
                   choices=list(Y_VAR_CHOICES),
                   default=list(DEFAULT_Y_VARS),
                   help="Y-axis metric(s). X is always iteration number. Each value produces its own canvas/PDF.\n"
                        "`chi2` = raw Chi^2 of change; `ratio` = χ²[i]/χ²[i-1] (undefined at first point);\n"
                        "`reduced_chi2` = χ²/n_bins; `ratio_of_ratios` = ratio[i]/ratio[i-1] (needs two previous points).\n")
    p.add_argument("--logy",
                   action="store_true",
                   default=DEFAULT_LOGY,
                   help="Draw the y-axis in log scale (`pad.SetLogy(1)`). Missing/non-positive points are omitted\n"
                        "from the TGraph (gaps, not zeros). `--ymin 0` is clamped to a positive floor when `--logy` is set.\n")
    p.add_argument("--add_average",
                   action="store_true",
                   help="Overlay the per-iteration mean of the selected y-var (Excel AVERAGE).\n"
                        "Requires ≥2 log files; with one file, warn and skip (do not error).\n")
    p.add_argument("--add_stddev",
                   action="store_true",
                   help="Overlay the per-iteration sample standard deviation (Excel STDEV, ddof=1) as its own TH1\n"
                        "named `h_{y_var}_StdDev`. Requires ≥2 log files; with one file, warn and skip.\n")
    p.add_argument("--stddev_as_errors",
                   action="store_true",
                   help="Put the sample stdev on the **average** hist via SetBinError **and paint those errors**\n"
                        "as a TGraphErrors (vertical bars), even when --draw_option is the default HIST LP.\n"
                        "Implies --add_average. Does **not** by itself draw a separate stddev hist.\n")
    p.add_argument("--n_bins",
                   type=int,
                   default=None,
                   help="Override NumBins used for `reduced_chi2` (applied to **every** file).\n"
                        "Use this to reproduce Excel’s global 915 / 11816 / 11258. If omitted, NumBins is parsed per file.\n")
    p.add_argument("--iter_max",
                   type=int,
                   default=None,
                   help="Crop the x-axis to this maximum iteration (inclusive). Default = max iteration among selected series.\n")
    p.add_argument("--iter_min",
                   type=int,
                   default=None,
                   help="Optional lower x crop (inclusive). **Default is 0.** Missing points are gaps, not zeros;\n"
                        "the axis does not auto-shift to the first defined iteration.\n")
    p.add_argument("-ti", "--title",
                   type=str,
                   default="",
                   help="Extra title text appended to the auto-built canvas title (`#chi^{2}` TLatex is already in the auto title).\n")
    p.add_argument("--xtitle",
                   type=str,
                   default=DEFAULT_XTITLE,
                   help="X-axis title. Excel used both `Iterations` and `Number of Bayesian Iterations`.\n")
    p.add_argument("--ytitle",
                   type=str,
                   default=None,
                   help="Override Y-axis title. Default is the TLatex title for the selected --y_var.\n")
    p.add_argument("-W", "--canvas_width",
                   type=int,
                   default=DEFAULT_CANVAS_WIDTH,
                   help="Canvas width in pixels.\n")
    p.add_argument("-H", "--canvas_height",
                   type=int,
                   default=DEFAULT_CANVAS_HEIGHT,
                   help="Canvas height in pixels.\n")
    p.add_argument("--ymin",
                   type=float,
                   default=None,
                   help="Y-axis minimum. Unset = automatic. With --logy, a user value <= 0 is clamped to a positive floor.\n")
    p.add_argument("--ymax",
                   type=float,
                   default=None,
                   help="Y-axis maximum. Unset = automatic (1.15 * max).\n")
    p.add_argument("--leg",
                   nargs=4,
                   type=float,
                   metavar=("X1", "Y1", "X2", "Y2"),
                   default=list(DEFAULT_LEG),
                   help="Legend box in NDC.\n")
    p.add_argument("--leg_cols",
                   type=int,
                   default=None,
                   help="TLegend.SetNColumns. Default: 1 if ≤8 series, 2 if 9–17, 3 if more.\n")
    p.add_argument("--draw_option",
                   type=str,
                   default=DEFAULT_DRAW_OPTION,
                   help="User-facing draw request, split per the Drawing contract.\n"
                        "Default `HIST LP` means line + markers on the TGraph (`LP SAME`).\n"
                        "TH1.Draw is only `AXIS` on the first series — never `HIST` / `HIST LP`.\n")
    p.add_argument("--line_width",
                   type=int,
                   default=DEFAULT_LINE_WIDTH,
                   help="SetLineWidth for per-file series. Average series uses this + 1.\n")
    p.add_argument("--marker_size",
                   type=float,
                   default=DEFAULT_MARKER_SIZE,
                   help="SetMarkerSize.\n")
    p.add_argument("--no_grid",
                   action="store_true",
                   help="Disable pad grid (grid is on by default to match Simple_RooUnfold).\n")
    p.add_argument("-n", "--name",
                   type=str,
                   default=DEFAULT_NAME,
                   help="Filename prefix (no extension, no os.sep). PDF: `{outdir}/{name}_{y_var}[_logy].pdf`.\n"
                        "ROOT: `{outdir}/{name}.root` (all y-vars in one file).\n")
    p.add_argument("-o", "--outdir",
                   type=str,
                   default=DEFAULT_OUTDIR,
                   help="Output directory. Created once before the first non-test save.\n")
    p.add_argument("-F", "--formats",
                   nargs="+",
                   choices=["pdf", "root"],
                   default=list(DEFAULT_FORMATS),
                   dest="formats",
                   help="Output format(s). `pdf` uses TCanvas.SaveAs. `root` writes the canvas, every TH1, and companion TGraphs.\n")
    p.add_argument("-t", "--test",
                   action="store_true",
                   help="Run the full parse + draw path without writing files (repo convention).\n"
                        "No os.makedirs, no TFile, no SaveAs. Print the paths that would have been written.\n")
    p.add_argument("-v", "--verbose",
                   action="store_true",
                   help="Extra prints: resolved paths, per-file n_bins source, iteration counts, derived values, output paths.\n")
    args = p.parse_args()
    try:
        args.log_file = expand_log_paths(args.log_file)
    except FileNotFoundError as exc:
        p.error(str(exc))
    if((args.legend is not None) and (len(args.legend) != len(args.log_file))):
        p.error(f"--legend has {len(args.legend)} label(s) but {len(args.log_file)} log file(s) after glob expansion")
    if(args.name and (os.sep in str(args.name))):
        p.error("--name is a filename prefix, not a path; use --outdir for the directory")
    return args


def y_at(series, y_var, i):
    c = series.chi2.get(i)
    if(y_var == "chi2"):
        return c
    if(y_var == "reduced_chi2"):
        if((c is None) or (series.n_bins in [None, 0])):
            return None
        return c / float(series.n_bins)
    if(y_var == "ratio"):
        prev = series.chi2.get(i - 1)
        if((c is None) or (prev in [None, 0.0])):
            return None
        return c / prev
    if(y_var == "ratio_of_ratios"):
        r_i = y_at(series, "ratio", i)
        r_im1 = y_at(series, "ratio", i - 1)
        if((r_i is None) or (r_im1 in [None, 0.0])):
            return None
        return r_i / r_im1
    raise ValueError(y_var)


def ensemble_at(file_series, y_var, i):
    vals = []
    for series in file_series:
        value = y_at(series, y_var, i)
        if(value is not None):
            vals.append(value)
    mean = statistics.fmean(vals) if(vals) else None
    stdev = statistics.stdev(vals) if(len(vals) >= 2) else None
    return mean, stdev


def is_drawable(value, logy):
    if((value is None) or (not math.isfinite(value))):
        return False
    if(logy and (value <= 0)):
        return False
    return True


def split_draw_option(opt):
    tokens = str(opt).upper().split()
    want_errors = any(t in {"E", "E1"} for t in tokens)
    want_markers = any(t in {"P", "LP", "PL"} for t in tokens)
    want_line = any(t in {"L", "LP", "PL", "HIST", "E1", "E"} for t in tokens) or (not tokens)
    if(want_errors and (not want_markers) and ("L" not in tokens)):
        want_markers = True
        want_line = True
    graph_opt = ""
    if(want_line):
        graph_opt += "L"
    if(want_markers):
        graph_opt += "P"
    if(graph_opt == ""):
        graph_opt = "L"
    th1_opt = "E1" if(want_errors) else "AXIS"
    return th1_opt, graph_opt


def paints_errors(is_average, args):
    return bool(is_average and args.stddev_as_errors)


def safe_root_name(label):
    s = re.sub(r"[^A-Za-z0-9_]+", "_", str(label))
    s = s.strip("_")
    if(s == ""):
        s = "series"
    if(s[0].isdigit()):
        s = "s_" + s
    return s


def unique_name(prefix, label, used):
    base = f"{prefix}_{safe_root_name(label)}"
    name = base
    n = 2
    while(name in used):
        name = f"{base}_{n}"
        n += 1
    used.add(name)
    return name


def sanitize_name(name):
    out = str(name).replace(" ", "_")
    for suffix in (".pdf", ".root", ".png"):
        if(out.lower().endswith(suffix)):
            out = out[: -len(suffix)]
    return out


def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        tfile.Delete(f"{obj.GetName()};*")
    obj.Write()


def init_root_and_style():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    if(repo_root not in sys.path):
        sys.path.insert(0, repo_root)
    from MyCommonAnalysisFunction_richcap import color, RuntimeTimer, root_color
    import ROOT
    ROOT.gROOT.SetBatch(1)
    ROOT.TH1.AddDirectory(0)
    ROOT.gStyle.SetTitleOffset(1.3, "y")
    ROOT.gStyle.SetGridColor(17)
    ROOT.gStyle.SetPadGridX(1)
    ROOT.gStyle.SetPadGridY(1)
    ROOT.gStyle.SetOptStat(0)
    return ROOT, color, RuntimeTimer, root_color


def autoscale_y(hists, logy, ymin, ymax):
    positives = []
    for hist in hists:
        for b in range(1, hist.GetNbinsX() + 1):
            v = hist.GetBinContent(b)
            if(v > 0):
                positives.append(v)
    if(not positives):
        return
    lo = min(positives)
    hi = max(positives)
    if(ymax is None):
        ymax = hi * 1.15
    floor = max(lo * 0.5, 1e-12)
    if(ymin is None):
        ymin = floor if(logy) else 0.0
    elif(logy):
        ymin = max(float(ymin), floor)
    hists[0].SetMinimum(ymin)
    hists[0].SetMaximum(ymax)


def copy_style(src, dest):
    dest.SetLineColor(src.GetLineColor())
    dest.SetMarkerColor(src.GetMarkerColor())
    dest.SetMarkerStyle(src.GetMarkerStyle())
    dest.SetLineWidth(src.GetLineWidth())
    dest.SetMarkerSize(src.GetMarkerSize())
    dest.SetLineStyle(src.GetLineStyle())


def assign_series_labels(series_list, file_legend_map, mixed_families):
    path_counts = {}
    for series in series_list:
        path_counts[series.path] = path_counts.get(series.path, 0) + 1
    for series in series_list:
        if(series.path in file_legend_map):
            label = file_legend_map[series.path]
        else:
            label = auto_legend_label(series.path, mixed_families=mixed_families)
        if(path_counts[series.path] > 1):
            label = f"{label} (block {series.block_index})"
        series.label = label


def _color_marker_cycles(ROOT):
    color_cycle = [
        ROOT.kRed, ROOT.kBlue, ROOT.kMagenta, ROOT.kGreen + 2, ROOT.kOrange + 7,
        ROOT.kAzure + 1, ROOT.kViolet + 1, ROOT.kTeal + 2, ROOT.kPink + 7, ROOT.kSpring + 5,
        ROOT.kCyan + 2, ROOT.kGray + 2, ROOT.kOrange + 3, ROOT.kAzure + 10, ROOT.kRed + 2,
        ROOT.kBlue + 2, ROOT.kMagenta + 2,
    ]
    marker_cycle = [
        ROOT.kFullCircle,
        ROOT.kFullSquare,
        ROOT.kFullTriangleUp,
        ROOT.kFullTriangleDown,
        ROOT.kOpenCircle,
        ROOT.kOpenSquare,
        ROOT.kOpenTriangleUp,
        ROOT.kOpenDiamond,
        ROOT.kFullCross,
        ROOT.kFullStar,
        ROOT.kOpenStar,
        ROOT.kOpenTriangleDown,
        ROOT.kFullDiamond,
        ROOT.kFullCrossX,
        ROOT.kFullThreeTriangles,
        41,
        45,
    ]
    return color_cycle, marker_cycle


def make_th1_and_graph(ROOT, args, y_var, label, y_getter, err_getter, i_min, i_max, used_names, is_average=False):
    nbins = i_max - i_min + 1
    xmin = i_min - 0.5
    xmax = i_max + 0.5
    hname = unique_name(f"h_{y_var}", label, used_names)
    gname = unique_name(f"g_{y_var}", label, used_names)
    hist = ROOT.TH1D(hname, "", nbins, xmin, xmax)
    hist.SetDirectory(0)
    hist.Sumw2(False)
    hist.SetName(hname)
    hist.SetStats(0)
    xs, ys, es = [], [], []
    for iteration in range(i_min, i_max + 1):
        value = y_getter(iteration)
        if(not is_drawable(value, args.logy)):
            continue
        bin_idx = hist.FindBin(float(iteration))
        hist.SetBinContent(bin_idx, float(value))
        err = 0.0
        if(is_average and args.stddev_as_errors):
            got = err_getter(iteration) if(err_getter is not None) else None
            err = float(got) if(got not in [None]) else 0.0
        hist.SetBinError(bin_idx, float(err))
        xs.append(float(iteration))
        ys.append(float(value))
        es.append(float(err))
    n = len(xs)
    if(n == 0):
        return hist, None
    if(paints_errors(is_average, args)):
        graph = ROOT.TGraphErrors(n)
        graph.SetName(gname)
        for i, (x, y, e) in enumerate(zip(xs, ys, es)):
            graph.SetPoint(i, x, y)
            graph.SetPointError(i, 0.0, e)
    else:
        graph = ROOT.TGraph(n)
        graph.SetName(gname)
        for i, (x, y) in enumerate(zip(xs, ys)):
            graph.SetPoint(i, x, y)
    graph.SetTitle("")
    return hist, graph


def style_series(ROOT, hist, graph, idx, args, color_cycle, marker_cycle, kind="file", root_color=None):
    if(kind == "average"):
        col = ROOT.kBlack
        mkr = ROOT.kFullCircle
        hist.SetLineWidth(args.line_width + 1)
    elif(kind == "stddev"):
        col = root_color.DGrey if(root_color is not None) else (ROOT.kGray + 2)
        mkr = ROOT.kOpenCircle
        hist.SetLineWidth(args.line_width)
        hist.SetLineStyle(2)
    else:
        col = color_cycle[idx % len(color_cycle)]
        mkr = marker_cycle[idx % len(marker_cycle)]
        hist.SetLineWidth(args.line_width)
    hist.SetLineColor(col)
    hist.SetMarkerColor(col)
    hist.SetMarkerStyle(mkr)
    hist.SetMarkerSize(args.marker_size)
    if(graph is not None):
        copy_style(hist, graph)


def output_paths(args, y_var):
    pdf_path = os.path.join(args.outdir, f"{args.name}_{y_var}{'_logy' if(args.logy) else ''}.pdf")
    root_path = os.path.join(args.outdir, f"{args.name}.root")
    return pdf_path, root_path


def run_plotter(args, ROOT, color, root_color):
    args.name = sanitize_name(args.name)
    if(args.no_grid):
        ROOT.gStyle.SetPadGridX(0)
        ROOT.gStyle.SetPadGridY(0)
    series_list = []
    for path in args.log_file:
        try:
            parsed = parse_unfold_log(path, block=args.block, cli_n_bins=args.n_bins, verbose=args.verbose)
        except Exception as exc:
            print(f"{color.Error}WARNING:{color.END} failed to parse '{path}': {exc}", file=sys.stderr)
            continue
        series_list.extend(parsed)
    if(not series_list):
        print(f"{color.Error}ERROR: no usable iteration series from the given log file(s).{color.END}", file=sys.stderr)
        sys.exit(1)
    mixed_families = (len({s.family for s in series_list}) > 1)
    file_legend_map = {}
    if(args.legend is not None):
        for path, lab in zip(args.log_file, args.legend):
            file_legend_map[path] = lab
    assign_series_labels(series_list, file_legend_map, mixed_families)
    if(args.verbose):
        for series in series_list:
            iters = sorted(series.chi2.keys())
            irange = f"[{iters[0]},{iters[-1]}]" if(iters) else "[]"
            chi0 = series.chi2.get(0)
            chi1 = series.chi2.get(1)
            print(f"{color.BBLUE}[INFO]{color.END} {os.path.basename(series.path)}")
            print(f"       label={series.label}  dim={series.dim}  q2y={series.q2y_bin}  "
                  f"n_bins={series.n_bins} ({series.n_bins_source})  n_iter={len(series.chi2)}  range={irange}")
            if(chi0 is not None):
                print(f"       chi2[0]={chi0}" + (f"  chi2[1]={chi1}" if(chi1 is not None) else ""))
    want_average = bool(args.add_average or args.stddev_as_errors)
    want_stddev = bool(args.add_stddev)
    n_files = len({s.path for s in series_list})
    skip_ensemble = False
    if((want_average or want_stddev) and (n_files < 2)):
        print(f"{color.BYELLOW}WARNING:{color.END} --add_average / --add_stddev / --stddev_as_errors need ≥2 log files; skipping ensemble hists.")
        skip_ensemble = True
        want_average = False
        want_stddev = False
    color_cycle, marker_cycle = _color_marker_cycles(ROOT)
    _, graph_opt = split_draw_option(args.draw_option)
    planned = []
    canvases = []
    all_write_objs = []
    for y_var in args.y_var:
        file_series = []
        for series in series_list:
            if((y_var == "reduced_chi2") and (series.n_bins in [None, 0])):
                print(f"{color.Error}WARNING:{color.END} skipping {os.path.basename(series.path)} for reduced_chi2 (n_bins={series.n_bins}).")
                continue
            if(not series.chi2):
                continue
            file_series.append(series)
        if(not file_series):
            print(f"{color.Error}WARNING:{color.END} no series for y_var={y_var}; skipping.")
            continue
        all_iters = []
        for series in file_series:
            all_iters.extend(series.chi2.keys())
        i_min = args.iter_min if(args.iter_min is not None) else 0
        i_max = args.iter_max if(args.iter_max is not None) else max(all_iters)
        if(i_max < i_min):
            print(f"{color.Error}WARNING:{color.END} empty iteration window for y_var={y_var}; skipping.")
            continue
        used_names = set()
        draw_items = []
        ytitle = args.ytitle if(args.ytitle not in [None, ""]) else Y_AXIS_TITLES[y_var]
        canvas_title = ytitle if(args.title in [None, ""]) else f"{ytitle}  {args.title}"
        idx = 0
        for series in file_series:
            hist, graph = make_th1_and_graph(
                ROOT, args, y_var, series.label,
                y_getter=lambda i, s=series, yv=y_var: y_at(s, yv, i),
                err_getter=None,
                i_min=i_min, i_max=i_max, used_names=used_names, is_average=False,
            )
            style_series(ROOT, hist, graph, idx, args, color_cycle, marker_cycle, kind="file", root_color=root_color)
            hist.SetTitle(canvas_title)
            hist.GetXaxis().SetTitle(args.xtitle)
            hist.GetYaxis().SetTitle(ytitle)
            hist.GetXaxis().SetTitleOffset(1.1)
            hist.GetYaxis().SetTitleOffset(1.3)
            if(graph is None):
                print(f"{color.BYELLOW}WARNING:{color.END} no drawable points for '{series.label}' ({y_var}); omitting from canvas.")
            else:
                draw_items.append((hist, graph, series.label, "file"))
            idx += 1
        stdev_by_iter = {}
        mean_by_iter = {}
        if((want_average or want_stddev) and (not skip_ensemble)):
            for iteration in range(i_min, i_max + 1):
                mean, stdev = ensemble_at(file_series, y_var, iteration)
                mean_by_iter[iteration] = mean
                stdev_by_iter[iteration] = stdev
        if(want_average and (not skip_ensemble)):
            hist, graph = make_th1_and_graph(
                ROOT, args, y_var, "Average",
                y_getter=lambda i: mean_by_iter.get(i),
                err_getter=lambda i: stdev_by_iter.get(i),
                i_min=i_min, i_max=i_max, used_names=used_names, is_average=True,
            )
            style_series(ROOT, hist, graph, idx, args, color_cycle, marker_cycle, kind="average", root_color=root_color)
            hist.SetTitle(canvas_title)
            hist.GetXaxis().SetTitle(args.xtitle)
            hist.GetYaxis().SetTitle(ytitle)
            if(graph is None):
                print(f"{color.BYELLOW}WARNING:{color.END} no drawable points for Average ({y_var}); omitting.")
            else:
                draw_items.append((hist, graph, "Average", "average"))
            idx += 1
        if(want_stddev and (not skip_ensemble)):
            hist, graph = make_th1_and_graph(
                ROOT, args, y_var, "StdDev",
                y_getter=lambda i: stdev_by_iter.get(i),
                err_getter=None,
                i_min=i_min, i_max=i_max, used_names=used_names, is_average=False,
            )
            style_series(ROOT, hist, graph, idx, args, color_cycle, marker_cycle, kind="stddev", root_color=root_color)
            hist.SetTitle(canvas_title)
            hist.GetXaxis().SetTitle(args.xtitle)
            hist.GetYaxis().SetTitle(ytitle)
            if(graph is None):
                print(f"{color.BYELLOW}WARNING:{color.END} no drawable points for Std. Dev. ({y_var}); omitting.")
            else:
                draw_items.append((hist, graph, "Std. Dev.", "stddev"))
        drawable = [(h, g, lab, kind) for (h, g, lab, kind) in draw_items if(g is not None)]
        if(not drawable):
            print(f"{color.Error}WARNING:{color.END} no drawable points for y_var={y_var}; skipping.")
            continue
        hists = [item[0] for item in drawable]
        nbins = i_max - i_min + 1
        autoscale_y(hists, args.logy, args.ymin, args.ymax)
        axis = hists[0].GetXaxis()
        if(nbins <= 25):
            for iteration in range(i_min, i_max + 1):
                axis.SetBinLabel(hists[0].FindBin(float(iteration)), str(iteration))
            axis.LabelsOption("h")
            axis.SetLabelSize(0.045)
        else:
            axis.SetNdivisions(510, False)
        cname = f"c_{y_var}"
        canvas = ROOT.TCanvas(cname, cname, args.canvas_width, args.canvas_height)
        canvas.SetFillColor(0)
        canvas.SetLeftMargin(0.12)
        canvas.SetRightMargin(0.08)
        canvas.SetBottomMargin(0.12)
        canvas.SetTopMargin(0.08)
        if(args.logy):
            canvas.SetLogy(1)
        canvas._keepalive = []
        hists[0].Draw("AXIS")
        for hist, graph, label, kind in drawable:
            graph.Draw(f"{graph_opt} SAME")
            canvas._keepalive.append(hist)
            canvas._keepalive.append(graph)
        n_series = len(drawable)
        x1, y1, x2, y2 = args.leg
        if((list(args.leg) == list(DEFAULT_LEG)) and (y_var in ["ratio", "ratio_of_ratios"])):
            x1, y1, x2, y2 = 0.14, 0.15, 0.45, 0.32
        legend = ROOT.TLegend(x1, y1, x2, y2)
        legend.SetBorderSize(1)
        legend.SetFillStyle(1001)
        legend.SetFillColor(ROOT.kWhite)
        legend.SetTextFont(42)
        legend.SetTextSize(0.028)
        ncols = args.leg_cols if(args.leg_cols) else (1 if(n_series <= 8) else 2 if(n_series <= 17) else 3)
        legend.SetNColumns(ncols)
        for hist, graph, label, kind in drawable:
            legend.AddEntry(hist, label, graph_opt.lower())
        legend.Draw()
        canvas._keepalive.append(legend)
        KEEP.append(canvas)
        canvases.append((y_var, canvas, drawable))
        pdf_path, root_path = output_paths(args, y_var)
        planned.append(("pdf", pdf_path, y_var, canvas))
        for hist, graph, label, kind in drawable:
            all_write_objs.append(hist)
            all_write_objs.append(graph)
        all_write_objs.append(canvas)
        if(args.verbose):
            print(f"{color.BBLUE}[INFO]{color.END} canvas {cname}: {n_series} series, iters {i_min}–{i_max}, graph_opt={graph_opt}")
    if(not canvases):
        print(f"{color.Error}ERROR: nothing to plot.{color.END}", file=sys.stderr)
        sys.exit(1)
    pdf_paths = [path for (kind, path, y_var, canvas) in planned]
    root_path = os.path.join(args.outdir, f"{args.name}.root")
    if(args.test):
        if("pdf" in args.formats):
            for path in pdf_paths:
                print(f"{color.GREEN}Would save: {path}{color.END}")
        if("root" in args.formats):
            print(f"{color.GREEN}Would save: {root_path}{color.END}")
        return
    os.makedirs(args.outdir, exist_ok=True)
    if("pdf" in args.formats):
        for path, canvas in [(path, canvas) for (kind, path, y_var, canvas) in planned]:
            canvas.SaveAs(path)
            print(f"{color.GREEN}Saved: {path}{color.END}")
    if("root" in args.formats):
        if(os.path.isfile(root_path)):
            print(f"{color.BYELLOW}Overwriting existing ROOT file: {root_path}{color.END}")
        tfile = ROOT.TFile(root_path, "RECREATE")
        written = set()
        for y_var, canvas, drawable in canvases:
            if(canvas.GetName() not in written):
                safe_write(canvas, tfile)
                written.add(canvas.GetName())
            for hist, graph, label, kind in drawable:
                if(hist.GetName() not in written):
                    safe_write(hist, tfile)
                    written.add(hist.GetName())
                if(graph.GetName() not in written):
                    safe_write(graph, tfile)
                    written.add(graph.GetName())
        tfile.Close()
        print(f"{color.GREEN}Saved: {root_path}{color.END}")


def main(args):
    ROOT, color, RuntimeTimer, root_color = init_root_and_style()
    timer = RuntimeTimer()
    timer.start()
    try:
        run_plotter(args, ROOT=ROOT, color=color, root_color=root_color)
    finally:
        timer.stop()
    print(f"\n{color.BOLD}Finished running 'Plot_Bayes_Iteration_Chi2.py'{color.END}\n")


if(__name__ == "__main__"):
    args = parse_args()
    main(args)
