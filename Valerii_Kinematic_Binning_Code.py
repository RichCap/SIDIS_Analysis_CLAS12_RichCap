import ROOT

Run_this_str_with_gInterpreter_for_Valeriis_Bins = r"""
#include <vector>
#include "TH2Poly.h"

static constexpr int N_Zbins  = 8;
static constexpr int N_pTbins = 10;
static constexpr int N_pTbins_with_overflow = N_pTbins + 1;

// (xB, Q2) mosaic (Mars / Valerii)
TH2Poly* makeTH2PolyMars_Valerii_py(){
  auto poly = new TH2Poly();

  // 1st row
  double x1[] = {0.126,  0.18,    0.18,     0.126};
  double y1[] = {2,      2.658,   2,        2};

  double x2[] = {0.18,   0.18,    0.21,     0.21,   0.18};
  double y2[] = {2,      2.658,   2.658,    2,      2};

  double x3[] = {0.21,   0.21,    0.24,     0.24,   0.21};
  double y3[] = {2,      2.658,   2.658,    2,      2};

  double x4[] = {0.24,   0.28,    0.28,     0.24};
  double y4[] = {2.658,  2.658,   2.00,     2};

  // Split 0.28–0.45 into three bins
  double x5_a[] = {0.28,   0.28,    0.34,   0.34};
  double y5_a[] = {2.00,   2.658,   2.658,  2};

  double x5_b[] = {0.34,   0.34,    0.39,   0.39};
  double y5_b[] = {2.00,   2.658,   2.658,  2};

  double x5_c[] = {0.39,   0.39,    0.45,   0.39};
  double y5_c[] = {2.00,   2.658,   2.658,  2};

  // 2nd row
  double x6[] = {0.18,   0.24,    0.24,     0.18};
  double y6[] = {2.658,  3.625,   2.658,    2.658};

  double x7[] = {0.24,   0.24,    0.28,     0.28,   0.24};
  double y7[] = {2.658,  3.625,   3.625,    2.658,  2.658};

  double x8[] = {0.28,   0.28,    0.34,     0.34,   0.28};
  double y8[] = {2.658,  3.625,   3.625,    2.658,  2.658};

  double x9_a[] = {0.34,   0.34,    0.39,  0.39};
  double y9_a[] = {2.658,  3.625,   3.625,    2.658};

  double x9_b[] = {0.39,   0.39,    0.54025,  0.45};
  double y9_b[] = {2.658,  3.625,   3.625,    2.658};

  // 3rd row
  double x10[] = {0.24,  0.34,    0.34,     0.24};
  double y10[] = {3.625, 5.12,    3.625,    3.625};

  double x11[] = {0.34,  0.34,    0.39,     0.39,   0.34};
  double y11[] = {3.625, 5.12,    5.12,     3.625,  3.625};

  double x12[] = {0.39,  0.39,    0.6234,   0.57,   0.54025,  0.39};
  double y12[] = {3.625, 5.12,    5.12,     4.05,   3.625,    3.625};

  // 4th row
  double x13[] = {0.34,  0.677,   0.7896,   0.75,   0.708,    0.64,  0.6234, 0.34};
  double y13[] = {5.12,  10.185,  11.351,   9.52,   7.42,     5.4,   5.12,   5.12};

  // 0-row for bin migration (low Q²)
  double x0_1[] = {0.,   0.,    0.1,  0.1};
  double y0_1[] = {1.5,  2.0,   2.0,  1.5};

  double x0_2[] = {0.1,   0.1,    0.2,  0.2};
  double y0_2[] = {1.5,  2.0,   2.0,   1.5};

  double x0_3[] = {0.2,   0.2,    0.3,  0.3};
  double y0_3[] = {1.5,  2.0,   2.0,   1.5};

  double x0_4[] = {0.3,   0.3,    0.4,  0.4};
  double y0_4[] = {1.5,  2.0,   2.0,   1.5};

  poly->AddBin(4, x1, y1);
  poly->AddBin(5, x2, y2);
  poly->AddBin(5, x3, y3);
  poly->AddBin(4, x4, y4);
  poly->AddBin(4, x5_a, y5_a);
  poly->AddBin(4, x5_b, y5_b);
  poly->AddBin(4, x5_c, y5_c);
  poly->AddBin(4, x6, y6);
  poly->AddBin(5, x7, y7);
  poly->AddBin(5, x8, y8);
  poly->AddBin(4, x9_a, y9_a);
  poly->AddBin(4, x9_b, y9_b);
  poly->AddBin(4, x10, y10);
  poly->AddBin(5, x11, y11);
  poly->AddBin(6, x12, y12);
  poly->AddBin(8, x13, y13);

  // Low Q² migration
  poly->AddBin(4, x0_1, y0_1);
  poly->AddBin(4, x0_2, y0_2);
  poly->AddBin(4, x0_3, y0_3);
  poly->AddBin(4, x0_4, y0_4);

  poly->SetLineStyle(1);
  poly->SetLineWidth(2);

  return poly;
}

// z edges (same as zbins_Valerii)
std::vector<double> zbins_Valerii_py(){
  return {0.,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0};
}

// z × pT^2 mosaic
TH2Poly* makeTH2PolyZpt2_Valerii_py(){
  std::vector<double> z = zbins_Valerii_py();

  std::vector<std::vector<double>> p(N_Zbins + 1);

  const std::vector<double> pt2_base = {
    0.00, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.65, 0.80, 1.00
  }; // 10 bins up to 1.0 => 11 edges

  for(int z_bin_i = 0; z_bin_i < N_Zbins; ++z_bin_i){
    p[z_bin_i] = pt2_base;
  }
  p[N_Zbins] = pt2_base;

  for(auto &pi : p){
    pi.push_back(1.50); // overflow edge => 11 bins total
  }

  auto poly = new TH2Poly();
  poly->Sumw2();
  poly->SetLineStyle(1);
  poly->SetLineWidth(2);

  const int NzEdges = (int)z.size();
  for(int iz = 0; iz < NzEdges - 1; ++iz){
    const auto &pz = p[iz];
    const int nPtEdges = (int)pz.size();
    for(int j = 0; j < nPtEdges - 1; ++j){
      poly->AddBin(z[iz], pz[j], z[iz+1], pz[j+1]);
    }
  }

  return poly;
}

// Singleton getters
TH2Poly* get_valerii_xq2_poly(){
  static TH2Poly* poly = nullptr;
  if(poly == nullptr){
    poly = makeTH2PolyMars_Valerii_py();
  }
  return poly;
}

TH2Poly* get_valerii_zpt2_poly(){
  static TH2Poly* poly = nullptr;
  if(poly == nullptr){
    poly = makeTH2PolyZpt2_Valerii_py();
  }
  return poly;
}

int Q2_xB_bin_valerii(double xB_in, double Q2_in){
  TH2Poly* poly = get_valerii_xq2_poly();
  if(!poly){
    return -1;
  }
  return poly->FindBin(xB_in, Q2_in);
}

int z_pT_bin_valerii(double z_in, double pT_in){
  TH2Poly* poly = get_valerii_zpt2_poly();
  if(!poly){
    return -1;
  }
  const double pt2 = pT_in * pT_in;
  return poly->FindBin(z_in, pt2);
}
"""

def draw_valerii_binning_tlines(pad=None, projection="Q2_vs_xB", selected_bin=None, line_color=ROOT.kBlack, line_width=1, highlight_color=ROOT.kRed, highlight_width=3):
    # pad        : TPad or TCanvas with a 2D histogram already drawn.
    # projection : "Q2_vs_xB", "xB_vs_Q2", "Q2_vs_y", "y_vs_Q2", "z_vs_pT", "pT_vs_z"
    # selected_bin:
    #   - None         -> draw all bin outlines with (line_color, line_width)
    #   - int          -> TH2Poly bin index (1..N_bins) to highlight
    #   - (iz, ipTbin) -> only for z/pT projections, 1-based (z-bin, pT-bin)
    #
    # Returns: list of ROOT.TLine objects that were drawn.
    
    # These are hard-coded from Valerii_binning_params.cxx
    N_ZBINS_VALERII              = 8
    N_PT_BINS_WITH_OVERFLOW_VAL  = 11   # 10 bins up to 1.0 + 1 overflow bin

    # For y calculation:  Constant = 0.5/(0.938272*10.6)
    Y_CONST = (0.5/(0.938272*10.6))

    if(pad is None):
        pad = ROOT.gPad
    if(pad is None):
        raise RuntimeError("draw_valerii_binning_tlines: no pad/canvas and gPad is None.")

    pad.cd()

    proj = str(projection)

    # Decide which TH2Poly we use and initial mapping flags
    if(proj == "Q2_vs_xB"):
        poly      = ROOT.get_valerii_xq2_poly()
        geom_type = "xQ2"    # bins in xB–Q2 space
        swap_axes = False    # draw (xB, Q2)
        use_sqrt  = False
    elif(proj == "xB_vs_Q2"):
        poly      = ROOT.get_valerii_xq2_poly()
        geom_type = "xQ2"
        swap_axes = True     # draw (Q2, xB)
        use_sqrt  = False
    elif(proj == "Q2_vs_y"):
        poly      = ROOT.get_valerii_xq2_poly()
        geom_type = "xQ2_y"  # bins in xB–Q2, but we map xB->y
        swap_axes = False    # draw (y, Q2)
        use_sqrt  = False
    elif(proj == "y_vs_Q2"):
        poly      = ROOT.get_valerii_xq2_poly()
        geom_type = "xQ2_y"
        swap_axes = True     # draw (Q2, y)
        use_sqrt  = False
    elif(proj == "z_vs_pT"):
        poly      = ROOT.get_valerii_zpt2_poly()
        geom_type = "z_pT"   # bins in z–pT^2 space, we will sqrt
        swap_axes = False    # draw (z, pT)
        use_sqrt  = True
    elif(proj == "pT_vs_z"):
        poly      = ROOT.get_valerii_zpt2_poly()
        geom_type = "z_pT"
        swap_axes = True     # draw (pT, z)
        use_sqrt  = True
    else:
        raise ValueError("draw_valerii_binning_tlines: unsupported projection '%s'." % proj)

    if(poly is None):
        raise RuntimeError("draw_valerii_binning_tlines: underlying TH2Poly pointer is null.")

    # For pure xB–Q2 geometry, auto-detect axis orientation only for xB projections
    if((geom_type == "xQ2") and ((proj == "Q2_vs_xB") or (proj == "xB_vs_Q2"))):
        prims = pad.GetListOfPrimitives()
        hist_on_pad = None
        if(prims is not None):
            for obj in prims:
                if(obj.InheritsFrom("TH2")):
                    hist_on_pad = obj
                    break
        if(hist_on_pad is not None):
            xax = hist_on_pad.GetXaxis()
            yax = hist_on_pad.GetYaxis()
            xmin = xax.GetXmin()
            xmax = xax.GetXmax()
            ymin = yax.GetXmin()
            ymax = yax.GetXmax()

            # Rough classification:
            #  - xB range: ~[0, 1]
            #  - Q2 range: ~[1.5, 12]
            x_looks_like_xB = ((xmin >= 0.0) and (xmax <= 1.2))
            y_looks_like_xB = ((ymin >= 0.0) and (ymax <= 1.2))

            if(x_looks_like_xB and (not y_looks_like_xB)):
                swap_axes = False   # (xB,Q2)
            elif((not x_looks_like_xB) and y_looks_like_xB):
                swap_axes = True    # (Q2,xB)
            # else: keep initial guess

    # Build a map: TH2Poly bin number -> TH2PolyBin*
    bins_array = poly.GetBins()
    if(bins_array is None):
        raise RuntimeError("draw_valerii_binning_tlines: TH2Poly::GetBins() returned null.")

    nbins_obj = bins_array.GetEntries()
    binnum_to_binobj = {}

    for idx in range(nbins_obj):
        bin_obj = bins_array.At(idx)
        if(not bin_obj):
            continue
        bin_num = bin_obj.GetBinNumber()
        binnum_to_binobj[bin_num] = bin_obj

    # Map selected_bin -> TH2Poly bin number if needed
    target_bin_number = None

    if(selected_bin is not None):
        if(isinstance(selected_bin, int)):
            target_bin_number = selected_bin
        elif((geom_type == "z_pT") and isinstance(selected_bin, (tuple, list)) and (len(selected_bin) == 2)):
            iz_idx, ipt_idx = selected_bin

            if((iz_idx < 1) or (iz_idx > N_ZBINS_VALERII)):
                raise ValueError("draw_valerii_binning_tlines: z-bin index out of range (1..%d)." % N_ZBINS_VALERII)
            if((ipt_idx < 1) or (ipt_idx > N_PT_BINS_WITH_OVERFLOW_VAL)):
                raise ValueError("draw_valerii_binning_tlines: pT-bin index out of range (1..%d)." % N_PT_BINS_WITH_OVERFLOW_VAL)

            # Same ordering as makeTH2PolyZpt2_Valerii_py: iz outer, pT^2 inner, bins numbered from 1
            target_bin_number = (iz_idx - 1)*N_PT_BINS_WITH_OVERFLOW_VAL + ipt_idx
        else:
            raise TypeError("draw_valerii_binning_tlines: selected_bin must be int or (z_bin, pT_bin) for z/pT projections.")

    # Helper to map one polygon point
    def map_point(x_poly, y_poly):
        # x_poly = xB (for xQ2 / xQ2_y),  y_poly = Q2
        # For z/pT, x_poly = z, y_poly = pT^2

        if(geom_type == "z_pT"):
            # y_poly is pT^2; convert to pT
            if(use_sqrt):
                if(y_poly < 0.0):
                    y_poly = 0.0
                y_val = math.sqrt(y_poly)
            else:
                y_val = y_poly
            x_val = x_poly

            if(swap_axes):
                return (y_val, x_val)
            else:
                return (x_val, y_val)

        elif(geom_type == "xQ2"):
            # Standard xB–Q2 representation
            x_val = x_poly    # xB
            y_val = y_poly    # Q2

            if(swap_axes):
                return (y_val, x_val)   # (Q2,xB)
            else:
                return (x_val, y_val)   # (xB,Q2)

        elif(geom_type == "xQ2_y"):
            # Map (xB,Q2) -> (y,Q2) or (Q2,y)
            xB_val = x_poly
            Q2_val = y_poly

            if(xB_val <= 0.0):
                # Avoid division by zero; put it off-plot if something weird happens
                y_var = -1.0
            else:
                y_var = Y_CONST*(Q2_val/xB_val)

            if(proj == "Q2_vs_y"):
                # x-axis: y,  y-axis: Q2
                return (y_var, Q2_val)
            elif(proj == "y_vs_Q2"):
                # x-axis: Q2, y-axis: y
                return (Q2_val, y_var)
            else:
                # Fallback (should not be reached)
                return (xB_val, Q2_val)

        else:
            # Should not reach here
            return (x_poly, y_poly)

    tlines = []

    # Decide which bin numbers to draw
    if(target_bin_number is not None):
        if(target_bin_number in binnum_to_binobj):
            bin_numbers_to_draw = [target_bin_number]
        else:
            return []
    else:
        bin_numbers_to_draw = sorted(binnum_to_binobj.keys())

    for bin_num in bin_numbers_to_draw:
        bin_obj = binnum_to_binobj[bin_num]
        poly_obj = bin_obj.GetPolygon()
        if(poly_obj is None):
            continue

        gr = poly_obj
        if(not gr.InheritsFrom("TGraph")):
            continue

        npoints = gr.GetN()
        xarr = gr.GetX()
        yarr = gr.GetY()

        for ip in range(npoints):
            jp = ip + 1
            if(jp >= npoints):
                jp = 0

            x0 = xarr[ip]
            y0 = yarr[ip]
            x1 = xarr[jp]
            y1 = yarr[jp]

            xA, yA = map_point(x0, y0)
            xB, yB = map_point(x1, y1)

            line = ROOT.TLine(xA, yA, xB, yB)

            if(target_bin_number is not None):
                line.SetLineColor(highlight_color)
                line.SetLineWidth(highlight_width)
            else:
                line.SetLineColor(line_color)
                line.SetLineWidth(line_width)

            line.Draw("same")
            tlines.append(line)

    # Keep references so the lines are not garbage-collected
    if(not hasattr(pad, "_valerii_binning_tlines")):
        pad._valerii_binning_tlines = []
    pad._valerii_binning_tlines.extend(tlines)

    # Also attach to the pad's primitive list so ROOT owns them
    for line in tlines:
        pad.GetListOfPrimitives().Add(line)

    pad.Modified()
    pad.Update()

    return tlines


def add_valerii_bins(rdf_in, var_type=""):
    xB_col    = f"xB{var_type}"
    Q2_col    = f"Q2{var_type}"
    z_col     = f"z{var_type}"
    pT_col    = f"pT{var_type}"
    phi_t_col = f"phi_t{var_type}"
    
    rdf_tmp =  rdf_in.Define(f"Q2_xB_Bin_Valerii{var_type}", f"Q2_xB_bin_valerii({xB_col}, {Q2_col})")
    rdf_tmp = rdf_tmp.Define(f"z_pT_Bin_Valerii{var_type}",  f"z_pT_bin_valerii({z_col}, {pT_col})")
    
    rdf_tmp = rdf_tmp.Define(f"{phi_t_col}_Bin", f"""
    int Num_PHI_BINS = 24;
    double bin_size  = 360.0/Num_PHI_BINS;
    int PHI_BIN      = (int)({phi_t_col}/bin_size) + 1;
    if({phi_t_col} == 360.0){{PHI_BIN = Num_PHI_BINS;}} // Include 360 in the last phi_h bin
    return PHI_BIN;""")
    
    rdf_tmp = rdf_tmp.Redefine(f"Q2_xB_Bin_Valerii{var_type}", f"""
    if((Q2_xB_Bin_Valerii{var_type} > 16) || (Q2_xB_Bin_Valerii{var_type} < 1)){{
        // There are only 16 physical Q2-xB bins; all other events go to bin 0
        return 0;
    }}
    return Q2_xB_Bin_Valerii{var_type};""")
    
    rdf_tmp = rdf_tmp.Redefine(f"z_pT_Bin_Valerii{var_type}", f"""
    // Original Valerii scheme has 88 z-pT bins (8 z bins × 11 pT^2 bins). I keep only the inner z-bins (iz = 2..7) and pT^2 bins 1..10 for each of them, and reindex those surviving bins to be contiguous from 1..60.
    int bin_old = z_pT_Bin_Valerii{var_type};
    if(bin_old <= 0){{
        return 0;
    }}
    // Decode (z index, pT index) in the original 8×11 layout
    int iz  = (bin_old - 1)/11 + 1; // 1..8
    int ipT = (bin_old - 1)%11 + 1; // 1..11

    // Migration bins in z (iz = 1 or 8) or in pT (ipT = 11) are mapped to 0
    if((iz < 2) || (iz > 7) || (ipT < 1) || (ipT > 10)){{
        return 0;
    }}

    // Compact index: for each of the 6 kept z-bins (iz = 2..7) we have 10 pT bins (ipT = 1..10)
    // New index = ipT + 10*(iz - 2) ∈ [1,60]
    int bin_new = (iz - 2)*10 + ipT;
    return bin_new;""")

    rdf_tmp = rdf_tmp.Define(f"Q2_xB_z_pT_4D_Bin_Valerii{var_type}",  f"""
    if((Q2_xB_Bin_Valerii{var_type} == 0) || (z_pT_Bin_Valerii{var_type} == 0)){{
        return 0;
    }}
    // After compaction there are 60 z-pT bins per physical Q2-xB bin
    int Q2_xB_z_pT_4D_Bin_Valerii_temp = z_pT_Bin_Valerii{var_type} + ((Q2_xB_Bin_Valerii{var_type} - 1) * 60);
    return Q2_xB_z_pT_4D_Bin_Valerii_temp; // Has up to 960+1 total bins 
    """)

    rdf_tmp = rdf_tmp.Define(f"Q2_xB_phi_t_3D_Bin_Valerii{var_type}",  f"""
    if(Q2_xB_Bin_Valerii{var_type} == 0){{
        return 0;
    }}
    int Q2_xB_phi_t_3D_Bin_Valerii_temp = {phi_t_col}_Bin;
    Q2_xB_phi_t_3D_Bin_Valerii_temp = Q2_xB_phi_t_3D_Bin_Valerii_temp + ((Q2_xB_Bin_Valerii{var_type} - 1) * 24);
    return Q2_xB_phi_t_3D_Bin_Valerii_temp; // Has up to 384+1 total bins 
    """)
    
    rdf_tmp = rdf_tmp.Define(f"z_pT_phi_t_3D_Bin_Valerii{var_type}",  f"""
    if(z_pT_Bin_Valerii{var_type} == 0){{
        return 0;
    }}
    int z_pT_phi_t_3D_Bin_Valerii_temp = {phi_t_col}_Bin;
    z_pT_phi_t_3D_Bin_Valerii_temp = z_pT_phi_t_3D_Bin_Valerii_temp + ((z_pT_Bin_Valerii{var_type} - 1) * 24);
    return z_pT_phi_t_3D_Bin_Valerii_temp; // Has up to 1440+1 total bins (60 z-pT × 24 φ-bins)
    """)

    rdf_tmp = rdf_tmp.Define(f"Q2_xB_z_pT_phi_t_5D_Bin_Valerii{var_type}",  f"""
    if((Q2_xB_Bin_Valerii{var_type} == 0) || (z_pT_Bin_Valerii{var_type} == 0)){{
        return 0;
    }}
    int Q2_xB_z_pT_phi_t_5D_Bin_Valerii_temp = {phi_t_col}_Bin + ((Q2_xB_z_pT_4D_Bin_Valerii{var_type} - 1) * 24);
    return Q2_xB_z_pT_phi_t_5D_Bin_Valerii_temp; // Has up to 23040+1 total bins (16 × 60 × 24)
    """)

    return rdf_tmp

