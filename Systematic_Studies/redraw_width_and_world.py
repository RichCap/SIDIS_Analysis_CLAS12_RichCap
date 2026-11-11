#!/usr/bin/env python3
# Stepped width canvases and the Harrison/Osipenko comparison.
# Hall C and HERMES points are not drawn.

import csv
import json
import math
import os

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTitleFontSize(0.0)

CAMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "physics_campaign")
THESIS = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis"
WIDTH = os.path.join(CAMP, "kt2/spline/run_20261106_quad_12_23/kt2_results.tsv")
POINTS = os.path.join(CAMP, "kt2/spline/run_20261106_quad_12_23/kt2_points.tsv")
NORM = os.path.join(CAMP, "corrected/spline/normalized_bc.json")
OVERLAP = "/Users/richardcapobianco/Desktop/World_Data_Tables/overlap_richard_vs_world.csv"
MOMENT = os.path.join(THESIS, "Results/Moment_Images")
WORLD_OUT = os.path.join(THESIS, "Conclusions/Comparison_Images/World_Moments_vs_PT.pdf")

LAYOUT = [4, 4, 4, 3, 2]
SERIES_COLORS = [ROOT.kBlue + 1, ROOT.kRed + 1, ROOT.kGreen + 2, ROOT.kMagenta + 1, ROOT.kCyan + 2, ROOT.kOrange + 7, ROOT.kViolet + 1, ROOT.kSpring + 4]
WINDOWS = [
    (8, "Present: 2.40 < Q^{2} < 2.90 GeV^{2},  0.35 < y < 0.45"),
    (12, "Present: 2.90 < Q^{2} < 3.70 GeV^{2},  0.35 < y < 0.45"),
    (3, "Present: 2.00 < Q^{2} < 2.40 GeV^{2},  0.45 < y < 0.55"),
]


def layout_map():
    mapping = {}
    number = 1
    max_cols = max(LAYOUT)
    for row_index, ncol in enumerate(LAYOUT):
        col_start = max_cols - ncol
        for ii in range(ncol):
            mapping[number] = (row_index, (max_cols - 1) - ii, col_start)
            number += 1
    return mapping, max_cols, len(LAYOUT)


def read_tsv(path):
    return list(csv.DictReader(open(path), delimiter="\t"))


def new_canvas(name, width, height):
    canvas = ROOT.TCanvas(name, name, width, height)
    canvas.SetFillColor(0)
    canvas.SetMargin(0, 0, 0, 0)
    canvas.keep = []
    return canvas


def style_frame(frame, x_title, y_title, is_left, is_bottom):
    frame.SetTitle("")
    frame.GetXaxis().SetTitle(x_title if(is_bottom) else "")
    frame.GetYaxis().SetTitle(y_title if(is_left) else "")
    frame.GetXaxis().SetTitleSize(0.070 if(is_bottom) else 0.0)
    frame.GetYaxis().SetTitleSize(0.070 if(is_left) else 0.0)
    frame.GetXaxis().SetLabelSize(0.055 if(is_bottom) else 0.0)
    frame.GetYaxis().SetLabelSize(0.055 if(is_left) else 0.0)
    frame.GetXaxis().SetTitleOffset(0.95)
    frame.GetYaxis().SetTitleOffset(1.05)
    frame.GetXaxis().SetNdivisions(505)
    frame.GetYaxis().SetNdivisions(505)


def draw_bin_label(host, q2y_bin):
    text = ROOT.TLatex()
    text.SetNDC(True)
    text.SetTextAlign(22)
    text.SetTextFont(42)
    text.SetTextSize(0.065)
    text.DrawLatex(0.55, 0.94, "Q^{2}--y bin %d" % q2y_bin)
    host.keep.append(text)


def draw_width_panel_label(host, q2y_bin, example):
    q2_center = (float(example["q2_min"]) + float(example["q2_max"])) / 2.0
    y_center = (float(example["y_min"]) + float(example["y_max"])) / 2.0
    text = ROOT.TLatex()
    text.SetNDC(True)
    text.SetTextAlign(22)
    text.SetTextFont(42)
    text.SetTextSize(0.050)
    text.DrawLatex(0.58, 0.955, "Q^{2}-y bin %d" % q2y_bin)
    text.DrawLatex(0.58, 0.895, "Q^{2} = %.2f, y = %.2f" % (q2_center, y_center))
    host.keep.append(text)


def shared_width_range(results):
    y_low = None
    y_high = None
    for row in results:
        if(row["kt2"] == ""):
            continue
        center = float(row["kt2"])
        error = float(row["kt2_err"])
        lo = center - error
        hi = center + error
        if((y_low is None) or (lo < y_low)):
            y_low = lo
        if((y_high is None) or (hi > y_high)):
            y_high = hi
    span = y_high - y_low
    if(span < 0.05):
        span = 0.05
    return y_low - 0.08 * span, y_high + 0.08 * span


QUADRATURE_WIDTH_RANGE = (-0.020577356628, 0.454536350028)


def fit_width_range(results, base_low, base_high):
    # Keep the quadrature limits unless a bar would cross them. Any expansion is the same on both ends.
    data_low = None
    data_high = None
    for row in results:
        if(row["kt2"] == ""):
            continue
        center = float(row["kt2"])
        error = float(row["kt2_err"])
        lo = center - error
        hi = center + error
        if((data_low is None) or (lo < data_low)):
            data_low = lo
        if((data_high is None) or (hi > data_high)):
            data_high = hi
    extra = 0.0
    if(data_low < base_low):
        extra = base_low - data_low
    if((base_high < data_high) and ((data_high - base_high) > extra)):
        extra = data_high - base_high
    if(extra > 0.0):
        margin = 0.02 * (base_high - base_low)
        return base_low - extra - margin, base_high + extra + margin
    return base_low, base_high


def ordinary_result(row):
    status = row["status"]
    if(("unsuccessful" in status) or ("unreliable_covariance" in status) or ("insufficient_points" in status)):
        return False
    if((row["kt2"] == "") or (row["kt2_err"] == "")):
        return False
    return True


def shared_ln_range(points, results):
    by_q2y = {}
    for row in results:
        by_q2y.setdefault(int(row["q2y_bin"]), []).append(row)
    point_map = {}
    for row in points:
        if(row["used"] != "1"):
            continue
        point_map.setdefault(int(row["q2y_bin"]), {}).setdefault(round(float(row["z"]), 3), []).append(row)
    y_values = []
    for q2y_bin, series in point_map.items():
        for z_value, raw_points in series.items():
            pts = sorted(raw_points, key=lambda item: float(item["pT2"]))
            for point in pts:
                y_value = math.log(float(point["A"]))
                y_error = float(point["ln_rel_err"])
                y_values.append(y_value - y_error)
                y_values.append(y_value + y_error)
            fit = None
            for row in by_q2y.get(q2y_bin, []):
                if(abs(float(row["z"]) - z_value) < 0.002):
                    fit = row
            if((fit is not None) and ordinary_result(fit) and (fit["a"] != "") and (fit["b"] != "")):
                x_lo = float(pts[0]["pT2"])
                x_hi = float(pts[-1]["pT2"])
                y_values.append(float(fit["a"]) * x_lo + float(fit["b"]))
                y_values.append(float(fit["a"]) * x_hi + float(fit["b"]))
    if(len(y_values) == 0):
        raise SystemExit("no ln A0 values to scale")
    y_low = min(y_values)
    y_high = max(y_values)
    span = y_high - y_low
    if(span < 0.2):
        span = 0.2
    return y_low - 0.08 * span, y_high + 0.22 * span, y_low, y_high


def draw_width(results_path=None, points_path=None, output_path=None, ln_output_path=None, note="", write_width=True):
    results = read_tsv(WIDTH if(results_path is None) else results_path)
    points = read_tsv(POINTS if(points_path is None) else points_path)
    by_q2y = {}
    for row in results:
        by_q2y.setdefault(int(row["q2y_bin"]), []).append(row)
    point_map = {}
    for row in points:
        if(row["used"] != "1"):
            continue
        point_map.setdefault(int(row["q2y_bin"]), {}).setdefault(round(float(row["z"]), 3), []).append(row)
    ln_ymin, ln_ymax, ln_data_low, ln_data_high = shared_ln_range(points, results)
    if((ln_data_low < ln_ymin) or (ln_data_high > ln_ymax)):
        raise SystemExit("ln A0 content is outside the shared range")
    ln_canvas = new_canvas("lnA0", 1500, 1900)
    width_canvas = new_canvas("width", 2800, 3200) if(write_width) else None
    plotted = [row for row in results if(ordinary_result(row))]
    if(note == ""):
        width_ymin, width_ymax = shared_width_range(plotted)
        title_space = 0.055
    else:
        width_ymin, width_ymax = fit_width_range(plotted, QUADRATURE_WIDTH_RANGE[0], QUADRATURE_WIDTH_RANGE[1])
        title_space = 0.090
    mapping, max_cols, nrows = layout_map()
    for q2y_bin in range(1, 18):
        row_index, col, col_start = mapping[q2y_bin]
        x0 = float(col) / float(max_cols)
        x1 = float(col + 1) / float(max_cols)
        y0 = float(row_index) / float(nrows)
        y1 = float(row_index + 1) / float(nrows)
        is_left = (col == col_start)
        is_bottom = (row_index == 0)
        series = point_map.get(q2y_bin, {})
        z_values = sorted(series.keys(), reverse=True)
        ln_canvas.cd()
        ln_pad = ROOT.TPad("ln_%d" % q2y_bin, "", x0, y0, x1, y1)
        ln_pad.SetLeftMargin(0.16 if(is_left) else 0.04)
        ln_pad.SetBottomMargin(0.16 if(is_bottom) else 0.04)
        ln_pad.SetRightMargin(0.03)
        ln_pad.SetTopMargin(0.10)
        ln_pad.SetGrid(1, 1)
        ln_pad.Draw()
        ln_pad.cd()
        ln_canvas.keep.append(ln_pad)
        if(len(z_values) > 0):
            x_values = []
            for z_value in z_values:
                for point in series[z_value]:
                    x_values.append(float(point["pT2"]))
            x_high = max(x_values) * 1.12
            ln_frame = ln_pad.DrawFrame(0.0, ln_ymin, x_high, ln_ymax)
            style_frame(ln_frame, "P_{T}^{2} [GeV^{2}]", "ln A_{0}", is_left, is_bottom)
            ln_canvas.keep.append(ln_frame)
            legend = ROOT.TLegend(0.46, 0.50, 0.96, 0.88)
            legend.SetBorderSize(0)
            legend.SetFillStyle(0)
            legend.SetTextFont(42)
            legend.SetTextSize(0.055)
            for index, z_value in enumerate(z_values):
                color = SERIES_COLORS[index % len(SERIES_COLORS)]
                pts = sorted(series[z_value], key=lambda item: float(item["pT2"]))
                graph = ROOT.TGraphErrors(len(pts))
                for point_index, point in enumerate(pts):
                    graph.SetPoint(point_index, float(point["pT2"]), math.log(float(point["A"])))
                    graph.SetPointError(point_index, 0.0, float(point["ln_rel_err"]))
                graph.SetMarkerStyle(20)
                graph.SetMarkerSize(0.70)
                graph.SetMarkerColor(color)
                graph.SetLineColor(color)
                graph.SetLineWidth(2)
                graph.Draw("P")
                ln_canvas.keep.append(graph)
                x_lo = float(pts[0]["pT2"])
                x_hi = float(pts[-1]["pT2"])
                fit = None
                for row in by_q2y.get(q2y_bin, []):
                    if(abs(float(row["z"]) - z_value) < 0.002):
                        fit = row
                if((fit is not None) and ordinary_result(fit) and (fit["a"] != "") and (fit["b"] != "")):
                    y_lo = float(fit["a"]) * x_lo + float(fit["b"])
                    y_hi = float(fit["a"]) * x_hi + float(fit["b"])
                    segment = ROOT.TGraph(2)
                    segment.SetPoint(0, x_lo, y_lo)
                    segment.SetPoint(1, x_hi, y_hi)
                    segment.SetLineColor(color)
                    segment.SetLineWidth(2)
                    segment.Draw("L")
                    ln_canvas.keep.append(segment)
                legend.AddEntry(graph, "z = %.3f" % z_value, "PL")
            legend.Draw()
            ln_canvas.keep.append(legend)
        draw_bin_label(ln_canvas, q2y_bin)
        if(not write_width):
            continue
        width_canvas.cd()
        wy0 = (float(row_index) / float(nrows)) * (1.0 - title_space)
        wy1 = (float(row_index + 1) / float(nrows)) * (1.0 - title_space)
        width_pad = ROOT.TPad("w_%d" % q2y_bin, "", x0, wy0, x1, wy1)
        width_pad.SetLeftMargin(0.22 if(is_left) else 0.04)
        width_pad.SetBottomMargin(0.18 if(is_bottom) else 0.04)
        width_pad.SetRightMargin(0.03)
        width_pad.SetTopMargin(0.18)
        width_pad.SetGrid(1, 1)
        width_pad.Draw()
        width_pad.cd()
        width_canvas.keep.append(width_pad)
        fits = sorted([row for row in by_q2y.get(q2y_bin, []) if(ordinary_result(row))], key=lambda item: float(item["z"]))
        if(len(fits) > 0):
            z_axis = [float(fit["z"]) for fit in fits]
            width_frame = width_pad.DrawFrame(min(z_axis) - 0.04, width_ymin, max(z_axis) + 0.06, width_ymax)
            style_frame(width_frame, "z", "#kappa_{T}^{2}(z) [GeV^{2}]", is_left, is_bottom)
            width_frame.GetYaxis().SetTitleSize(0.055 if(is_left) else 0.0)
            width_frame.GetYaxis().SetTitleOffset(1.35)
            width_canvas.keep.append(width_frame)
            graph = ROOT.TGraphErrors(len(fits))
            for index, fit in enumerate(fits):
                graph.SetPoint(index, float(fit["z"]), float(fit["kt2"]))
                graph.SetPointError(index, 0.0, float(fit["kt2_err"]))
            graph.SetMarkerStyle(20)
            graph.SetMarkerSize(1.15)
            graph.SetMarkerColor(ROOT.kBlue + 1)
            graph.SetLineColor(ROOT.kBlue + 1)
            graph.SetLineWidth(2)
            graph.Draw("P")
            width_canvas.keep.append(graph)
            for fit in fits:
                if("large_relative_uncertainty" not in fit["status"]):
                    continue
                mark = ROOT.TMarker(float(fit["z"]), float(fit["kt2"]), 29)
                mark.SetMarkerColor(ROOT.kRed + 1)
                mark.SetMarkerSize(2.8)
                mark.Draw()
                width_canvas.keep.append(mark)
                print("large relative uncertainty Q2-y %d z %s value %s err %s" % (q2y_bin, fit["z"], fit["kt2"], fit["kt2_err"]))
            draw_width_panel_label(width_canvas, q2y_bin, fits[0])
        width_canvas.cd()
    if(write_width):
        width_canvas.cd()
        page_title = ROOT.TLatex()
        page_title.SetNDC(True)
        page_title.SetTextAlign(23)
        page_title.SetTextFont(42)
        page_title.SetTextSize(0.028)
        page_title.DrawLatex(0.50, 0.985, "#kappa_{T}^{2}(z) vs z")
        width_canvas.keep.append(page_title)
        if(note != ""):
            page_note = ROOT.TLatex()
            page_note.SetNDC(True)
            page_note.SetTextAlign(23)
            page_note.SetTextFont(42)
            page_note.SetTextSize(0.022)
            page_note.DrawLatex(0.50, 0.952, note)
            width_canvas.keep.append(page_note)
        if(output_path is None):
            output_path = os.path.join(MOMENT, "kT2_vs_z_all_Q2y.pdf")
        width_canvas.SaveAs(output_path)
        print("shared width range", width_ymin, width_ymax)
        print("wrote", output_path)
    if(ln_output_path is not None):
        ln_canvas.SaveAs(ln_output_path)
        print("wrote", ln_output_path)
    print("shared ln range", ln_ymin, ln_ymax)


def published_rows(overlap, q2y_bin):
    selected = []
    for row in overlap:
        source = row["world_source"]
        if(("Harrison" not in source) and ("Osipenko" not in source)):
            continue
        if(not row["richard_bin"].startswith("(Q2_y_Bin_%d)" % q2y_bin)):
            continue
        selected.append(row)
    return selected


def finite_moment(text):
    try:
        value = float(text)
    except ValueError:
        return None
    if(value != value):
        return None
    return value


def draw_world():
    payload = json.load(open(NORM))["Fit_Pars_from_3D_BC_RC_Bayesian"]
    groups = {}
    for key, cell in payload.items():
        q2y_bin = int(key.split("(Q2_y_Bin_")[1].split(")")[0])
        zpt_bin = int(key.split("(z_pT_Bin_")[1].split(")")[0])
        groups.setdefault(q2y_bin, []).append((zpt_bin, cell))
    centers = {}
    for row in read_tsv(POINTS):
        centers[(int(row["q2y_bin"]), int(row["zpt_bin"]))] = (round(float(row["z"]), 3), float(row["pT"]))
    overlap = list(csv.DictReader(line for line in open(OVERLAP) if(not line.startswith("#"))))
    ROOT.gStyle.SetPaperSize(29.7, 21.0)
    canvas = new_canvas("world", 1600, 1131)
    canvas.Divide(3, 2, 0.004, 0.004)
    observables = (
        ("B", "Fit_Par_B", "Fit_Par_B_ERR", "world_cosphi", "world_cosphi_stat", "A_{UU}^{cos #phi}", -0.48, 0.28),
        ("C", "Fit_Par_C", "Fit_Par_C_ERR", "world_cos2phi", "world_cos2phi_stat", "A_{UU}^{cos 2#phi}", -0.22, 0.18),
    )
    omitted = []
    for column, (q2y_bin, title) in enumerate(WINDOWS):
        world = published_rows(overlap, q2y_bin)
        published_z = []
        for row in world:
            z_value = finite_moment(row["z"])
            if(z_value is not None):
                published_z.append(z_value)
        z_low = min(published_z) - 0.02
        z_high = max(published_z) + 0.02
        by_z = {}
        for zpt_bin, cell in groups[q2y_bin]:
            if((q2y_bin, zpt_bin) not in centers):
                continue
            z_value, pT = centers[(q2y_bin, zpt_bin)]
            if((z_value < z_low) or (z_value > z_high)):
                continue
            by_z.setdefault(z_value, []).append((pT, cell))
        z_values = sorted(by_z.keys())
        color_of = {}
        for index, z_value in enumerate(z_values):
            color_of[z_value] = SERIES_COLORS[index % len(SERIES_COLORS)]
        print("window", q2y_bin, "measurement z", z_values, "published span", round(z_low, 3), round(z_high, 3))
        for row_index, (letter, value_key, err_key, world_key, world_err, y_title, y_low, y_high) in enumerate(observables):
            pad_index = row_index * 3 + column + 1
            canvas.cd(pad_index)
            pad = canvas.GetPad(pad_index)
            pad.SetGrid(1, 1)
            pad.SetLeftMargin(0.20)
            pad.SetRightMargin(0.12)
            pad.SetBottomMargin(0.14)
            pad.SetTopMargin(0.10)
            frame = pad.DrawFrame(0.0, y_low, 0.98, y_high)
            frame.SetTitle("")
            frame.GetXaxis().SetTitle("P_{T} (GeV)")
            frame.GetYaxis().SetTitle(y_title)
            frame.GetXaxis().SetTitleSize(0.050)
            frame.GetYaxis().SetTitleSize(0.050)
            frame.GetXaxis().SetLabelSize(0.042)
            frame.GetYaxis().SetLabelSize(0.042)
            frame.GetYaxis().SetTitleOffset(1.35)
            canvas.keep.append(frame)
            heading = ROOT.TLatex()
            heading.SetNDC(True)
            heading.SetTextAlign(22)
            heading.SetTextFont(42)
            heading.SetTextSize(0.038)
            heading.DrawLatex(0.50, 0.955, title)
            canvas.keep.append(heading)
            for z_value in z_values:
                drawn = []
                for pT, cell in sorted(by_z[z_value], key=lambda item: item[0]):
                    value = float(cell[value_key])
                    error = float(cell[err_key])
                    if((error != error) or (value != value) or (abs(value) > 2.0)):
                        continue
                    drawn.append((pT, value, error))
                if(len(drawn) == 0):
                    continue
                graph = ROOT.TGraphErrors(len(drawn))
                for index, (pT, value, error) in enumerate(drawn):
                    graph.SetPoint(index, pT, value)
                    graph.SetPointError(index, 0.0, error)
                graph.SetMarkerStyle(20)
                graph.SetMarkerSize(0.75)
                graph.SetMarkerColor(color_of[z_value])
                graph.SetLineColor(color_of[z_value])
                graph.SetLineWidth(2)
                graph.Draw("LP")
                canvas.keep.append(graph)
            for source_name, marker in (("Harrison", 25), ("Osipenko", 26)):
                grouped_world = {}
                for row in world:
                    if(source_name not in row["world_source"]):
                        continue
                    value = finite_moment(row[world_key])
                    error = finite_moment(row[world_err])
                    pT = finite_moment(row["PT"])
                    z_raw = finite_moment(row["z"])
                    if((value is None) or (error is None) or (pT is None) or (z_raw is None)):
                        continue
                    if(abs(value) > 2.0):
                        continue
                    nearest = min(z_values, key=lambda item: abs(item - z_raw))
                    grouped_world.setdefault(round(z_raw, 3), []).append((pT, value, error, nearest))
                for z_raw, selected in grouped_world.items():
                    nearest = selected[0][3]
                    graph = ROOT.TGraphErrors(len(selected))
                    for index, (pT, value, error, near_z) in enumerate(selected):
                        graph.SetPoint(index, pT, value)
                        graph.SetPointError(index, 0.0, error)
                    graph.SetMarkerStyle(marker)
                    graph.SetMarkerSize(0.95)
                    graph.SetMarkerColor(color_of[nearest])
                    graph.SetLineColor(color_of[nearest])
                    graph.Draw("P")
                    canvas.keep.append(graph)
            z_legend = ROOT.TLegend(0.72, 0.52, 0.98, 0.90)
            z_legend.SetTextSize(0.034)
            z_legend.SetFillStyle(1001)
            z_legend.SetFillColor(ROOT.kWhite)
            z_legend.SetBorderSize(0)
            z_proxies = []
            for z_value in z_values:
                proxy = ROOT.TGraph(1)
                proxy.SetMarkerStyle(20)
                proxy.SetMarkerColor(color_of[z_value])
                proxy.SetLineColor(color_of[z_value])
                z_legend.AddEntry(proxy, "z = %.3f" % z_value, "P")
                z_proxies.append(proxy)
            z_legend.Draw()
            canvas.keep.append(z_legend)
            canvas.keep.extend(z_proxies)
            if((column == 0) and (row_index == 0)):
                legend = ROOT.TLegend(0.28, 0.70, 0.62, 0.90)
                legend.SetTextSize(0.038)
                legend.SetFillStyle(1001)
                legend.SetFillColor(ROOT.kWhite)
                legend.SetBorderSize(0)
                proxy_m = ROOT.TGraph(1)
                proxy_m.SetMarkerStyle(20)
                proxy_m.SetMarkerColor(ROOT.kBlack)
                proxy_h = ROOT.TGraph(1)
                proxy_h.SetMarkerStyle(25)
                proxy_h.SetMarkerColor(ROOT.kBlack)
                proxy_o = ROOT.TGraph(1)
                proxy_o.SetMarkerStyle(26)
                proxy_o.SetMarkerColor(ROOT.kBlack)
                legend.AddEntry(proxy_m, "This measurement", "P")
                legend.AddEntry(proxy_h, "Harrison, 5.498 GeV", "P")
                legend.AddEntry(proxy_o, "Osipenko, 5.75 GeV", "P")
                legend.Draw()
                canvas.keep.extend([legend, proxy_m, proxy_h, proxy_o])
            pad.Update()
            canvas.cd()
    canvas.SaveAs(WORLD_OUT)
    print("omitted undetermined coefficients", len(omitted))
    for item in omitted:
        print(" omit", item)
    print("wrote", WORLD_OUT)


if(__name__ == "__main__"):
    draw_width()
    draw_world()
