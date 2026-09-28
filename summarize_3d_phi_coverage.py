#!/usr/bin/env python3
# Count 3D reconstructed phi_h bins kept or removed by an acceptance cut.

import os
import re
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

PHI_N = 24
HEADER = os.path.join(_BOOT, "Cpp_Dedicated_5D_Unfold", "generated", "Dedicated_5D_Binning.h")


def load_unfold_skip_table(path=HEADER):
    # The 3D unfold calls skip_condition_z_pT_bins from this generated header.
    text = open(path).read()
    last_match = re.search(r"kZptLast\[18\] = \{([^}]+)\}", text)
    skip_match = re.search(r"kSkipZpT\[18\]\[41\] = \{([\s\S]*?)\};", text)
    lasts = [int(item) for item in last_match.group(1).split(",") if(item.strip())]
    rows = []
    for line in skip_match.group(1).splitlines():
        nums = [int(item) for item in re.findall(r"-?\d+", line)]
        if(len(nums) == 41):
            rows.append(nums)
    return lasts, rows


ZPT_LAST, SKIP_ROWS = load_unfold_skip_table()


def replace_all(text, src, dst):
    return text.replace(src, dst)


def apply_matrix_1d(name):
    name = replace_all(name, "'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")
    name = replace_all(name, "'Response_Matrix'", "'Response_Matrix_1D'")
    return name


def apply_background_1d(name):
    name = replace_all(name, "'Response_Matrix_1D'", "'Background_Response_Matrix_1D'")
    name = replace_all(name, "'Response_Matrix_Normal_1D'", "'Background_Response_Matrix_1D'")
    return name


def strip_weight_tags(name):
    for tag in ("_(AccSpline)", "_(AccJSON)", "_(Spline)", "_(JSON)", "_(Acc)", "_(Weighed)"):
        name = replace_all(name, tag, "")
    return name


def strip_smear_tags(name):
    name = replace_all(name, "_smeared", "")
    name = replace_all(name, "smear_", "")
    name = replace_all(name, "smear", "")
    return name


def prepare_gdf_name(name):
    name = replace_all(name, "(Data-Type='mdf')", "(Data-Type='gdf')")
    name = strip_weight_tags(name)
    name = replace_all(name, "cut_Complete_EDIS", "no_cut")
    for sector in range(1, 7):
        name = replace_all(name, "cut_Complete_SIDIS_eS" + str(sector) + "o", "no_cut")
    name = replace_all(name, "cut_Complete_SIDIS_Proton", "no_cut")
    name = replace_all(name, "cut_Complete_SIDIS", "no_cut")
    name = replace_all(name, "cut_Complete", "no_cut")
    name = strip_smear_tags(name)
    return apply_matrix_1d(name)


def prepare_rdf_name(name):
    name = replace_all(name, "(Data-Type='mdf')", "(Data-Type='rdf')")
    name = strip_weight_tags(name)
    name = strip_smear_tags(name)
    return apply_matrix_1d(name)


def extract_q2y(name):
    match = re.search(r"Q2-(?:y|xB)-Bin=(-?\d+),", name)
    if(match):
        return int(match.group(1))
    return -1


def is_3d_matrix(name):
    if("(Data-Type='mdf')" not in name):
        return False
    if("Response_Matrix_Normal" not in name):
        return False
    if("Response_Matrix_Normal_1D" in name):
        return False
    if("5D_Response" in name):
        return False
    if("Background" in name):
        return False
    if("no_cut" in name):
        return False
    if("cut_Complete_EDIS" in name):
        return False
    if("cut_Complete_SIDIS" not in name):
        return False
    if("cut_Complete_SIDIS_eS" in name):
        return False
    if("no_cut_eS" in name):
        return False
    if("_Proton" in name):
        return False
    if("Multi_Dim_" in name):
        return False
    if("phi_t" not in name):
        return False
    if("_(lundvpk)" in name or "_(lundrho)" in name):
        return False
    if("MultiDim_z_pT_Bin" not in name):
        return False
    if("(Smear-Type='smear')" not in name):
        return False
    if(any(tag in name for tag in ("_(Acc)", "_(JSON)", "_(Spline)", "_(AccJSON)", "_(AccSpline)", "_(Weighed)"))):
        return False
    return extract_q2y(name) > 0


def zpt_phi_slots(q2y):
    last = ZPT_LAST[q2y]
    slots = []
    slot = 1
    for zpt in range(1, last + 1):
        if(SKIP_ROWS[q2y][zpt]):
            continue
        slots.append((zpt, slot))
        slot += PHI_N
    return slots


def skip_reason(rdf_c, mdf_c, gdf_c, bdf_c, min_acc):
    rec_mc = mdf_c + bdf_c
    if(rdf_c == 0.0):
        return "data_zero"
    if(rec_mc == 0.0):
        return "mdf_bdf_zero"
    if(gdf_c == 0.0):
        return ""
    if((rec_mc / gdf_c) < min_acc):
        return "low_acceptance"
    return ""


def floor_subtract(rdf, rho):
    values = []
    for i in range(1, rdf.GetNbinsX() + 1):
        val = rdf.GetBinContent(i)
        if(rho is not None):
            val = val - rho.GetBinContent(i)
        if(val < 0.0):
            val = 0.0
        values.append(val)
    return values


def phi_gap(kept_flags):
    # Interior hole: a removed phi bin with a kept bin on both sides.
    for i in range(1, len(kept_flags) - 1):
        if((not kept_flags[i]) and any(kept_flags[:i]) and any(kept_flags[i + 1:])):
            return True
    return False


def analyze_cut(tfile, min_acc, matrices):
    rows = []
    for q2y, matrix_name in matrices:
        mdf_name = apply_matrix_1d(matrix_name)
        rdf_name = prepare_rdf_name(matrix_name)
        gdf_name = prepare_gdf_name(matrix_name)
        bdf_name = apply_background_1d(mdf_name)
        rdf = tfile.Get(rdf_name)
        mdf = tfile.Get(mdf_name)
        gdf = tfile.Get(gdf_name)
        bdf = tfile.Get(bdf_name)
        if((not rdf) or (not mdf) or (not gdf) or (not bdf)):
            rows.append((q2y, "MISSING_HIST"))
            continue
        rho = tfile.Get(rdf_name + "_(lundvpk)")
        if(not rho):
            rho = tfile.Get(mdf_name + "_(lundvpk)")
        rdf_vals = floor_subtract(rdf, rho if(rho) else None)
        slots = zpt_phi_slots(q2y)
        n_low = 0
        n_empty = 0
        n_kept = 0
        n_phi = 0
        n_gap = 0
        n_endpoint = 0
        n_unmapped_low = 0
        n_unmapped_empty = 0
        n_unmapped_kept = 0
        mapped_idx = set()
        z_lines = []
        for zpt, start in slots:
            for phi in range(PHI_N):
                mapped_idx.add(start + phi)
            flags = []
            low_here = 0
            for phi in range(PHI_N):
                idx = start + phi
                n_phi += 1
                if((idx < 1) or (idx > mdf.GetNbinsX())):
                    flags.append(False)
                    continue
                why = skip_reason(rdf_vals[idx - 1], mdf.GetBinContent(idx), gdf.GetBinContent(idx), bdf.GetBinContent(idx), min_acc)
                if(why == "low_acceptance"):
                    n_low += 1
                    low_here += 1
                    flags.append(False)
                elif(why):
                    n_empty += 1
                    flags.append(False)
                else:
                    n_kept += 1
                    flags.append(True)
            kept_n = sum(1 for flag in flags if flag)
            has_gap = phi_gap(flags)
            if(has_gap):
                n_gap += 1
            if((kept_n < PHI_N) and (not has_gap) and (kept_n > 0)):
                n_endpoint += 1
            z_lines.append((zpt, kept_n, low_here, "gap" if(has_gap) else ("endpoint" if((kept_n < PHI_N) and (kept_n > 0)) else ("empty" if(kept_n == 0) else "full"))))
        for idx in range(1, mdf.GetNbinsX() + 1):
            if(idx in mapped_idx):
                continue
            why = skip_reason(rdf_vals[idx - 1], mdf.GetBinContent(idx), gdf.GetBinContent(idx), bdf.GetBinContent(idx), min_acc)
            if(why == "low_acceptance"):
                n_unmapped_low += 1
            elif(why):
                n_unmapped_empty += 1
            else:
                n_unmapped_kept += 1
        rows.append((q2y, n_phi, n_kept, n_low, n_empty, n_gap, n_endpoint, n_unmapped_low, n_unmapped_empty, n_unmapped_kept, mdf.GetNbinsX(), z_lines))
    return rows


def main():
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError
    bank = sys.argv[1] if(len(sys.argv) > 1) else "Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_Final_Thesis_Response_Matrices_Final_Thesis_Files_All.root"
    out_path = sys.argv[2] if(len(sys.argv) > 2) else "Unfold_Iteration_Study_3D/acc_scan/phi_coverage.txt"
    cuts = [float(item) for item in sys.argv[3:]] if(len(sys.argv) > 3) else [0.005, 0.025, 0.100]
    tfile = ROOT.TFile.Open(bank, "READ")
    matrices = []
    for key in tfile.GetListOfKeys():
        name = key.GetName()
        if(not is_3d_matrix(name)):
            continue
        matrices.append((extract_q2y(name), name))
    matrices.sort()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as out:
        out.write("cut\tQ2y\tn_phi\tn_kept\tn_low_acceptance\tn_empty\tn_z_interior_gap\tn_z_endpoint_only\tkept_fraction\tn_unmapped_low\tn_unmapped_empty\tn_unmapped_kept\tn_hist\n")
        for min_acc in cuts:
            rows = analyze_cut(tfile, min_acc, matrices)
            cut_label = f"{min_acc:.3f}"
            out.write(f"# acceptance_cut {cut_label}\n")
            for row in rows:
                if(row[1] == "MISSING_HIST"):
                    out.write(f"{min_acc}\t{row[0]}\tMISSING_HIST\n")
                    continue
                q2y, n_phi, n_kept, n_low, n_empty, n_gap, n_endpoint, n_unmapped_low, n_unmapped_empty, n_unmapped_kept, n_hist, z_lines = row
                frac = (float(n_kept) / float(n_phi)) if(n_phi) else 0.0
                out.write(f"{cut_label}\t{q2y}\t{n_phi}\t{n_kept}\t{n_low}\t{n_empty}\t{n_gap}\t{n_endpoint}\t{frac:.6f}\t{n_unmapped_low}\t{n_unmapped_empty}\t{n_unmapped_kept}\t{n_hist}\n")
                for zpt, kept_n, low_here, kind in z_lines:
                    if(kind == "full"):
                        continue
                    out.write(f"#\t{cut_label}\tQ2y={q2y}\tzpt={zpt}\tkept_phi={kept_n}/{PHI_N}\tlow_acceptance={low_here}\t{kind}\n")
    tfile.Close()
    print(f"Wrote {out_path}")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
