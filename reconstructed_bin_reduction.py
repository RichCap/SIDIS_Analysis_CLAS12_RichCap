"""Skip and compress reconstructed bins before unfolding. Generated space is not reduced."""

import sys


class RecSkipMap:
    def __init__(self, orig_n, xmin, xmax):
        self.orig_n = int(orig_n)
        self.xmin = float(xmin)
        self.xmax = float(xmax)
        self.kept = []
        self.skipped = []
        self.reason = {}
        self.orig_to_reduced = {}

    @property
    def n_kept(self):
        return len(self.kept)

    def is_skipped(self, orig_index):
        return int(orig_index) in self.reason

    def reduced_index(self, orig_index):
        return self.orig_to_reduced.get(int(orig_index))

    def report_lines(self):
        skip_txt = ",".join(str(i) for i in self.skipped) if(self.skipped) else "(none)"
        return [
            f"original reconstructed bins: {self.orig_n}",
            f"reduced reconstructed bins: {self.n_kept}",
            f"skipped reconstructed bins: {len(self.skipped)}",
            f"skipped original indices: {skip_txt}",
        ]


# def build_rec_skip_map(rdf, mdf, gdf, bdf=None, min_acc=0.0005, warn=None):  # Changed min_acc to 0.025 on 9/16/2026
def build_rec_skip_map(rdf, mdf, gdf, bdf=None, min_acc=0.025, warn=None):
    if(warn is None):
        warn = lambda msg: print(msg, file=sys.stderr)
    n = int(rdf.GetNbinsX())
    xmin = rdf.GetXaxis().GetXmin()
    xmax = rdf.GetXaxis().GetXmax()
    skip_map = RecSkipMap(n, xmin, xmax)
    reduced = 0
    for i in range(1, n + 1):
        rdf_c = rdf.GetBinContent(i)
        mdf_c = mdf.GetBinContent(i)
        gdf_c = gdf.GetBinContent(i)
        bdf_c = 0.0 if(bdf is None) else bdf.GetBinContent(i)
        rec_mc = mdf_c + bdf_c
        reason = None
        if(rdf_c == 0):
            reason = "data_zero"
        elif(rec_mc == 0):
            reason = "mdf_bdf_zero"
        elif(gdf_c == 0):
            warn(f"WARNING: gdf == 0 in reconstructed/generated bin {i}; skipping (mdf+bdf)/gdf test for this bin.")
        elif((rec_mc / gdf_c) < min_acc):
            reason = "low_acceptance"
        if(reason is not None):
            skip_map.skipped.append(i)
            skip_map.reason[i] = reason
        else:
            reduced += 1
            skip_map.kept.append(i)
            skip_map.orig_to_reduced[i] = reduced
    return skip_map


def compress_th1_rec(hist, skip_map, name=None):
    if(hist is None):
        return None
    import ROOT
    out_name = name if(name is not None) else (str(hist.GetName()) + "_rec_reduced")
    n_kept = skip_map.n_kept
    if(n_kept < 1):
        raise RuntimeError("compress_th1_rec: no reconstructed bins kept")
    out = ROOT.TH1D(out_name, hist.GetTitle(), n_kept, 0.5, n_kept + 0.5)
    out.SetDirectory(0)
    out.Sumw2()
    for orig in skip_map.kept:
        red = skip_map.orig_to_reduced[orig]
        out.SetBinContent(red, hist.GetBinContent(orig))
        out.SetBinError(red, hist.GetBinError(orig))
    if(hist.GetXaxis().GetTitle()):
        out.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    if(hist.GetYaxis().GetTitle()):
        out.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
    return out


def restore_th1_from_reduced(reduced, skip_map, name=None, title=None):
    if(reduced is None):
        return None
    import ROOT
    out_name = name if(name is not None) else str(reduced.GetName()).replace("_rec_reduced", "")
    out = ROOT.TH1D(out_name, title if(title is not None) else reduced.GetTitle(),
                    skip_map.orig_n, skip_map.xmin, skip_map.xmax)
    out.SetDirectory(0)
    out.Sumw2()
    for orig in skip_map.kept:
        red = skip_map.orig_to_reduced[orig]
        out.SetBinContent(orig, reduced.GetBinContent(red))
        out.SetBinError(orig, reduced.GetBinError(red))
    return out


def mask_full_to_analysis(full_hist, skip_map, name=None):
    """Copy a full-length (gen-space) hist and zero skipped original rec indices for downstream analysis."""
    if(full_hist is None):
        return None
    out = full_hist.Clone(name if(name is not None) else full_hist.GetName())
    out.SetDirectory(0)
    for orig in skip_map.skipped:
        if((orig >= 1) and (orig <= out.GetNbinsX())):
            out.SetBinContent(orig, 0)
            out.SetBinError(orig, 0)
    return out


def compress_th2_rec_axis(th2, skip_map, rec_is_x, name=None):
    if(th2 is None):
        return None
    import ROOT
    out_name = name if(name is not None) else (str(th2.GetName()) + "_rec_reduced")
    n_kept = skip_map.n_kept
    if(n_kept < 1):
        raise RuntimeError("compress_th2_rec_axis: no reconstructed bins kept")
    if(rec_is_x):
        ny = th2.GetNbinsY()
        ymin, ymax = th2.GetYaxis().GetXmin(), th2.GetYaxis().GetXmax()
        out = ROOT.TH2D(out_name, th2.GetTitle(), n_kept, 0.5, n_kept + 0.5, ny, ymin, ymax)
        out.SetDirectory(0)
        out.Sumw2()
        for orig in skip_map.kept:
            red = skip_map.orig_to_reduced[orig]
            for y in range(0, ny + 2):
                out.SetBinContent(red, y, th2.GetBinContent(orig, y))
                out.SetBinError(red, y, th2.GetBinError(orig, y))
    else:
        nx = th2.GetNbinsX()
        xmin, xmax = th2.GetXaxis().GetXmin(), th2.GetXaxis().GetXmax()
        out = ROOT.TH2D(out_name, th2.GetTitle(), nx, xmin, xmax, n_kept, 0.5, n_kept + 0.5)
        out.SetDirectory(0)
        out.Sumw2()
        for orig in skip_map.kept:
            red = skip_map.orig_to_reduced[orig]
            for x in range(0, nx + 2):
                out.SetBinContent(x, red, th2.GetBinContent(x, orig))
                out.SetBinError(x, red, th2.GetBinError(x, orig))
    out.GetXaxis().SetTitle(th2.GetXaxis().GetTitle())
    out.GetYaxis().SetTitle(th2.GetYaxis().GetTitle())
    return out
