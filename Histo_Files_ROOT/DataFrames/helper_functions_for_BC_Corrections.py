#!/usr/bin/env python3

import ROOT
import sys
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import * #color, variable_Title_name
# from ExtraAnalysisCodeValues import New_z_pT_and_MultiDim_Binning_Code
sys.path.remove(script_dir)
del script_dir

import traceback

from pathlib import Path

import json
def load_json_file(path):
    # Load a JSON file and return its contents.
    # Args: Path to the JSON file
    # Returns: Parsed JSON data (into a dict | list)
    file_path = Path(path)
    if(not file_path.exists()):  # Check existence
        raise FileNotFoundError(f"Path does not exist: {file_path}")
    if(not file_path.is_file()): # Check that it is a file
        raise ValueError(f"Path is not a file: {file_path}")
    try:                         # Load JSON
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON format in {file_path}: {e}") from e
        
import re
def Build_BC_Table_From_JSON(json_path, value_key="BC_Factor", default_val=1.0, nQ2=17, nZ=36, nPhi=24):
    dat = load_json_file(json_path)
    results = dat["results"] if("results" in dat) else dat
    NZ   = nZ + 1
    NPHI = nPhi + 1
    size = (nQ2 + 1) * NZ * NPHI
    tab = [float(default_val)] * size
    pat = re.compile(r"Bin\s*\((\d+)-(\d+)-(\d+)\)")
    for k, v in results.items():
        mm = pat.search(str(k))
        if(not mm):
            continue
        q2y = int(mm.group(1))
        zpt = int(mm.group(2))
        phi = int(mm.group(3))
        if((q2y < 1) or (q2y > nQ2) or (zpt < 1) or (zpt > nZ) or (phi < 1) or (phi > nPhi)):
            continue
        if(not isinstance(v, dict)):
            continue
        val = v.get(value_key, default_val)
        try:
            val = float(val)
        except Exception:
            val = float(default_val)
        idx = (q2y * NZ + zpt) * NPHI + phi
        tab[idx] = val

    return tab, nQ2, nZ, nPhi

def Declare_BC_Lookup(tab, nQ2=17, nZ=36, nPhi=24, tag="BC"):
    NZ   = nZ + 1
    NPHI = nPhi + 1
    init = ",".join([f"{x:.17g}" if((x == x) and (abs(x) != float("inf"))) else "1.0" for x in tab])
    ROOT.gInterpreter.Declare(f"""
#include <vector>
static const int {tag}_NQ2  = {int(nQ2)};
static const int {tag}_NZ   = {int(nZ)};
static const int {tag}_NPHI = {int(nPhi)};
static const int {tag}_NZP1   = {int(NZ)};
static const int {tag}_NPHIP1 = {int(NPHI)};
static const std::vector<double> {tag}_TAB = std::vector<double>{{{init}}};

static inline double {tag}_Lookup(int Q2y, int Zpt, int Phi) {{
  if((Q2y < 1) || (Q2y > {tag}_NQ2))  return 1.0;
  if((Zpt < 1) || (Zpt > {tag}_NZ))   return 1.0;
  if((Phi < 1) || (Phi > {tag}_NPHI)) return 1.0;
  int idx = (Q2y * {tag}_NZP1 + Zpt) * {tag}_NPHIP1 + Phi;
  if((idx < 0) || (idx >= (int){tag}_TAB.size())) return 1.0;
  if({tag}_TAB[idx] == 0) return 1.0; 
  return (1/{tag}_TAB[idx]);
}}
""")

def _safe_norm(hh, Normalize_Q):
    if(not Normalize_Q):
        return
    try:
        integral = hh.Integral(0, hh.GetNbinsX() + 1)
        if(integral != 0.0):
            hh.Scale(1.0/integral)
    except:
        pass

def _make_h1(df_in, name_in, title_in, weighted_q, Weight_Expr="BC_Factor", PhiT_Var="phi_t"):
    if(weighted_q):
        return df_in.Histo1D((name_in, title_in, 24, 0.0, 360), PhiT_Var, Weight_Expr)
    elif(Weight_Expr in ["Event_Weight_WithBC"]):
        return df_in.Histo1D((name_in, title_in, 24, 0.0, 360), PhiT_Var, "Event_Weight")
    return     df_in.Histo1D((name_in, title_in, 24, 0.0, 360), PhiT_Var)
    

def BC_Corrections_Compare_in_z_pT_Images_Together(rdf_in, args, Q2_Y_Bin_Range=range(1,18), PhiT_Var="phi_t", Q2y_Bin_Var="Q2_Y_Bin", z_pT_Bin_Var="z_pT_Bin_Y_bin", Normalize_Q=False, Plot_Orientation="z_pT"):
    Weight_Expr = "BC_Factor"
    if(not rdf_in.HasColumn("BC_Factor")):
        if(not rdf_in.HasColumn(f"{PhiT_Var}_bin")):
            rdf_in = rdf_in.Define(f"{PhiT_Var}_bin", f"""
if({PhiT_Var} < 360){{ return int({PhiT_Var}/15) + 1; }}
else {{ return 1; }} """)
        tab, nQ2, nZ, nPhi = Build_BC_Table_From_JSON(args.json_file_BC, value_key="BC_Factor")
        Declare_BC_Lookup(tab, nQ2=nQ2, nZ=nZ, nPhi=nPhi, tag="BC")
        rdf_in = rdf_in.Define("BC_Factor", f"BC_Lookup({Q2y_Bin_Var}, {z_pT_Bin_Var}, {PhiT_Var}_bin)")
        if(not rdf_in.HasColumn("Event_Weight")):
            rdf_in = rdf_in.Define("Event_Weight", "weight" if(rdf_in.HasColumn("weight")) else "1.0")
            Weight_Expr = "BC_Factor"
        else:
            rdf_in      = rdf_in.Define("Event_Weight_WithBC", "Event_Weight*BC_Factor")
            Weight_Expr = "Event_Weight_WithBC"
    PhiT_Title = variable_Title_name(PhiT_Var) # Automatically adds the 'smearing' or 'gen' title as appropriate
    All_z_pT_Canvas = {}
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Canvas (Main) Creation  ##################################################################################################################################################################################################################################################################################################################################################################################
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"BC_Comparison_for_Q2_Y_Bin_{Q2_Y_Bin}"
        All_z_pT_Canvas[Save_Name] = Canvas_Create(Name=Save_Name, Num_Columns=2, Num_Rows=1, Size_X=int(1800*2), Size_Y=int(1500*2), cd_Space=0.01)
        All_z_pT_Canvas[Save_Name].SetFillColor(ROOT.kGray)
        if(args.verbose):
            print(f"{color.BBLUE}Creating TCanvas: {color.END_B}{Save_Name}{color.BBLUE}...{color.END}")
        All_z_pT_Canvas_cd_1 = All_z_pT_Canvas[Save_Name].cd(1)
        All_z_pT_Canvas_cd_1.SetFillColor(ROOT.kGray)
        All_z_pT_Canvas_cd_1.SetPad(xlow=0.005, ylow=0.015, xup=0.27, yup=0.985)
        All_z_pT_Canvas_cd_1.Divide(1, 2, 0, 0)
        
        All_z_pT_Canvas_cd_1_Upper = All_z_pT_Canvas_cd_1.cd(1)
        All_z_pT_Canvas_cd_1_Upper.SetPad(xlow=0, ylow=0.425, xup=1, yup=1)
        All_z_pT_Canvas_cd_1_Upper.Divide(1, 2, 0, 0)
        
        All_z_pT_Canvas_cd_1_Lower = All_z_pT_Canvas_cd_1.cd(2)
        All_z_pT_Canvas_cd_1_Lower.SetPad(xlow=0, ylow=0, xup=1, yup=0.42)
        All_z_pT_Canvas_cd_1_Lower.Divide(1, 1, 0, 0)
        All_z_pT_Canvas_cd_1_Lower.cd(1).SetPad(xlow=0.035, ylow=0.025, xup=0.95, yup=0.975)
        
        All_z_pT_Canvas_cd_2 = All_z_pT_Canvas[Save_Name].cd(2)
        All_z_pT_Canvas_cd_2.SetPad(xlow=0.28, ylow=0.015, xup=0.995, yup=0.9975)
        All_z_pT_Canvas_cd_2.SetFillColor(ROOT.kGray)
        
        number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
        if((Plot_Orientation in ["z_pT"])):
            All_z_pT_Canvas_cd_2.Divide(number_of_cols, number_of_rows, 0.0001, 0.0001)
        else:
            All_z_pT_Canvas_cd_2.Divide(1, number_of_cols, 0.0001, 0.0001)
            for ii in range(1, number_of_cols + 1, 1):
                All_z_pT_Canvas_cd_2_cols = All_z_pT_Canvas_cd_2.cd(ii)
                All_z_pT_Canvas_cd_2_cols.Divide(number_of_rows, 1, 0.0001, 0.0001)
    if(args.verbose):
        print(f"\t{color.BOLD}Created {len(All_z_pT_Canvas)} TCanvases...{color.END}")
    ####  Canvas (Main) Creation End ###############################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    
    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Histogram Creation (Batch)  ##############################################################################################################################################################################################################################################################################################################################################################################
    rptr_store_by_q2 = {}
    rptr_list_all    = []

    for Q2_Y_Bin in Q2_Y_Bin_Range:
        rdf_Q2 = rdf_in
        if((str(Q2_Y_Bin) not in ["All", "0"])):
            rdf_Q2 = rdf_Q2.Filter(f"({Q2y_Bin_Var}=={int(Q2_Y_Bin)})")

        q2_tag = str(Q2_Y_Bin)
        
        if(Q2_Y_Bin not in rptr_store_by_q2):
            rptr_store_by_q2[Q2_Y_Bin] = {}

        z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1]
        for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin)):
                continue

            rdf_bin = rdf_Q2.Filter(f"({z_pT_Bin_Var}=={int(z_pT_Bin)})")

            key_unw = f"BC {PhiT_Var} NoWeight Bin ({q2_tag}-{z_pT_Bin})"
            key_wgt = f"BC {PhiT_Var} Weighted Bin ({q2_tag}-{z_pT_Bin})"

            titleNW = f"{PhiT_Title} Normal (Q^{{2}}-y Bin = {q2_tag} #topbar z-P_{{T}} Bin = {z_pT_Bin})"
            title_W = f"{PhiT_Title} BC Corrected (Q^{{2}}-y Bin = {q2_tag} #topbar z-P_{{T}} Bin = {z_pT_Bin})"

            titleNW = f"#splitline{{Made from the {'Experimental' if('rdf' in args.dataframe_BC) else 'MC (clasdis) Generated' if('gdf' in args.dataframe_BC) else 'MC (clasdis-Matched) Generated' if('mdf_gen' in args.dataframe_BC) else 'MC (clasdis) Reconstructed'} Data}}{{{titleNW}}}"
            title_W = f"#splitline{{Made from the {'Experimental' if('rdf' in args.dataframe_BC) else 'MC (clasdis) Generated' if('gdf' in args.dataframe_BC) else 'MC (clasdis-Matched) Generated' if('mdf_gen' in args.dataframe_BC) else 'MC (clasdis) Reconstructed'} Data}}{{{title_W}}}"

            full_titleNW = f"{titleNW if(args.title in [None, '']) else f'#splitline{{{titleNW}}}{{{args.title}}}'}; {PhiT_Title}"
            full_title_W = f"{title_W if(args.title in [None, '']) else f'#splitline{{{title_W}}}{{{args.title}}}'}; {PhiT_Title}"

            rptr_store_by_q2[Q2_Y_Bin][key_unw] = _make_h1(rdf_bin, key_unw, full_titleNW, False, Weight_Expr, PhiT_Var)
            rptr_store_by_q2[Q2_Y_Bin][key_wgt] = _make_h1(rdf_bin, key_wgt, full_title_W, True,  Weight_Expr, PhiT_Var)

            rptr_list_all.append(rptr_store_by_q2[Q2_Y_Bin][key_unw])
            rptr_list_all.append(rptr_store_by_q2[Q2_Y_Bin][key_wgt])

    print(f"{color.BCYAN}Triggering Event Evaluation on {color.END_B}{len(rptr_list_all)}{color.BCYAN} Histograms...{color.END}\n")
    try:
        ROOT.RDF.RunGraphs(rptr_list_all)
    except:
        for rr in rptr_list_all:
            rr.GetValue()
    print(f"{color.BGREEN}Evaluations are Complete{color.END}")
    print(f"{args.timer.time_elapsed(return_Q=True)[-1].replace('\n', ' ')}")

    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"BC_Comparison_for_Q2_Y_Bin_{Q2_Y_Bin}"

        if((not hasattr(All_z_pT_Canvas[Save_Name], "phi_rptr_store"))):
            All_z_pT_Canvas[Save_Name].phi_rptr_store = {}
        All_z_pT_Canvas[Save_Name].phi_rptr_store.update(rptr_store_by_q2[Q2_Y_Bin])

        hist_store = {}
        for kk in rptr_store_by_q2[Q2_Y_Bin]:
            try:
                hist_store[kk] = rptr_store_by_q2[Q2_Y_Bin][kk].GetValue()
            except:
                hist_store[kk] = None

        for kk in hist_store:
            if((hist_store[kk] != None)):
                _safe_norm(hist_store[kk], Normalize_Q)

        All_z_pT_Canvas[Save_Name].phi_hist_store = hist_store

    ####  Histogram Creation (Batch) End  ##########################################################################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################

    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Left)  ###################################################################################################################################################################################################################################################################################################################################################################################
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"BC_Comparison_for_Q2_Y_Bin_{Q2_Y_Bin}"
        canvas = All_z_pT_Canvas[Save_Name]

        pad_leg = canvas.cd(1).cd(2).cd(1)
        pad_leg.SetFillColor(ROOT.kGray)
        pad_leg.cd()
        ROOT.gStyle.SetOptStat(0)

        if((not hasattr(canvas, "legend_store"))):
            canvas.legend_store = {}

        dummy_unw = ROOT.TH1F(f"dummy_unw_{Q2_Y_Bin}", "", 1, 0, 1)
        dummy_wgt = ROOT.TH1F(f"dummy_wgt_{Q2_Y_Bin}", "", 1, 0, 1)
        dummy_unw.SetLineColor(ROOT.kAzure+1)
        dummy_unw.SetLineWidth(3)
        dummy_wgt.SetLineColor(ROOT.kRed+1)
        dummy_wgt.SetLineWidth(3)

        leg = ROOT.TLegend(0.10, 0.15, 0.90, 0.85, "", "NDC")
        leg.SetNColumns(1)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.10)
        leg.AddEntry(dummy_unw, "Normal (No Weight)", "l")
        leg.AddEntry(dummy_wgt, "BC Corrected (Weighted)", "l")
        leg.Draw("same")

        canvas.legend_store["dummy_unw"] = dummy_unw
        canvas.legend_store["dummy_wgt"] = dummy_wgt
        canvas.legend_store["legend"]    = leg

        pad_leg.Modified()
        pad_leg.Update()
    ################################################################################################################################################################################################################################################################################################################################################################################################################

    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Filling Canvas (Right) - Individual z-pT Bins  ###############################################################################################################################################################################################################################################################################################################
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"BC_Comparison_for_Q2_Y_Bin_{Q2_Y_Bin}"
        canvas = All_z_pT_Canvas[Save_Name]
        hist_store = canvas.phi_hist_store
        q2_tag = str(Q2_Y_Bin)

        All_z_pT_Canvas_cd_2 = canvas.cd(2)
        number_of_rows, number_of_cols = Get_Num_of_z_pT_Rows_and_Columns(Q2_Y_Bin_Input=Q2_Y_Bin)
        z_pT_Bin_Range = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=Q2_Y_Bin)[1]

        for z_pT_Bin in range(1, z_pT_Bin_Range + 1, 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=Q2_Y_Bin, Z_PT_BIN=z_pT_Bin)):
                continue

            cd_number_of_z_pT_all_together = z_pT_Bin
            try:
                if((Plot_Orientation in ["z_pT"])):
                    All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2.cd(cd_number_of_z_pT_all_together)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(ROOT.kGray)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)
                else:
                    cd_row = int(cd_number_of_z_pT_all_together/number_of_cols) + 1
                    if((0 == (cd_number_of_z_pT_all_together%number_of_cols))):
                        cd_row += -1
                    cd_col = cd_number_of_z_pT_all_together - ((cd_row - 1)*number_of_cols)
                    All_z_pT_Canvas_cd_2_z_pT_Bin_Row = All_z_pT_Canvas_cd_2.cd((number_of_cols - cd_col) + 1)
                    All_z_pT_Canvas_cd_2_z_pT_Bin = All_z_pT_Canvas_cd_2_z_pT_Bin_Row.cd((number_of_rows + 1) - cd_row)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.SetFillColor(ROOT.kGray)
                    All_z_pT_Canvas_cd_2_z_pT_Bin.Divide(1, 1, 0, 0)

                Draw_Canvas(All_z_pT_Canvas_cd_2_z_pT_Bin, 1, 0.15)
                ROOT.gStyle.SetOptStat(0)

                key_unw = f"BC {PhiT_Var} NoWeight Bin ({q2_tag}-{z_pT_Bin})"
                key_wgt = f"BC {PhiT_Var} Weighted Bin ({q2_tag}-{z_pT_Bin})"
                hh_unw = hist_store.get(key_unw, None)
                hh_wgt = hist_store.get(key_wgt, None)

                if(None not in [hh_unw, hh_wgt]):
                    hh_unw.SetLineColor(ROOT.kAzure+1)
                    hh_unw.SetLineWidth(2)
                    hh_wgt.SetLineColor(ROOT.kRed+1)
                    hh_wgt.SetLineWidth(2)

                    y_max = max([hh_unw.GetMaximum(), hh_wgt.GetMaximum()])
                    hh_unw.GetYaxis().SetRangeUser(0.0, 1.2*y_max if(y_max > 0.0) else 1.0)
                    if(Normalize_Q):
                        hh_unw.GetYaxis().SetTitle("Normalized Counts")
                    hh_unw.Draw("hist")
                    hh_wgt.Draw("hist same")
                    ROOT.gPad.Update()
                # else:
                #     pv_miss = ROOT.TPaveText(0.10, 0.40, 0.90, 0.60, "NDC")
                #     pv_miss.SetFillStyle(0)
                #     pv_miss.SetBorderSize(0)
                #     pv_miss.SetTextAlign(22)
                #     pv_miss.SetTextFont(42)
                #     pv_miss.SetTextSize(0.08)
                #     pv_miss.AddText("Missing hists")
                #     pv_miss.Draw("same")
                #     ROOT.gPad.Update()
            except:
                print(f"{color.Error}Error in Drawing phi_t Plots for Bin ({q2_tag}-{z_pT_Bin}):\n{color.END_R}{str(traceback.format_exc())}{color.END}")

        canvas.cd()
        canvas.Modified()
        canvas.Update()
    ####  Filling Canvas (Right) End #######################################################################################################################################################################################################################################################################################################################
    ################################################################################################################################################################################################################################################################################################################################################################################################################

    ################################################################################################################################################################################################################################################################################################################################################################################################################
    ####  Saving Canvases  ##################################################################################################################################################################################################################################################################################################################################################################################
    for Q2_Y_Bin in Q2_Y_Bin_Range:
        Save_Name = f"BC_Comparison_for_Q2_Y_Bin_{Q2_Y_Bin}"
        out_name = Save_Name.replace("son_for", f"son_with_{PhiT_Var}_for_{args.dataframe_BC}_in")
        if(args.name):
            out_name = f"{out_name}_{args.name}{args.File_Save_Format}"
        else:
            out_name = f"{out_name}{args.File_Save_Format}"
        if(not args.dry_run):
            All_z_pT_Canvas[Save_Name].SaveAs(out_name)
            print(f"{color.BOLD}Saved: {color.BBLUE}{out_name}{color.END}")
        else:
            print(f"{color.Error}Would be Saving: {color.BCYAN}{out_name}{color.END}")
    ################################################################################################################################################################################################################################################################################################################################################################################################################

    return All_z_pT_Canvas



