#include "Dedicated_5D_Unfold_Helpers.h"

#include <cmath>
#include <iostream>
#include <map>
#include <memory>
#include <regex>
#include <stdexcept>
#include <utility>

#include "TCanvas.h"
#include "TCollection.h"
#include "TH1.h"
#include "TH2.h"
#include "TKey.h"
#include "TList.h"
#include "TObjString.h"
#include "TROOT.h"
#include "TStyle.h"

#include "RooUnfoldResponse.h"
#include "RooUnfoldBayes.h"
#include "RooUnfold.h"

using sidis5d::UnfoldArgs;
namespace Color = sidis5d::Color;
namespace ColorBg = sidis5d::ColorBg;
namespace RootColor = sidis5d::RootColor;
using sidis5d::contains;
using sidis5d::replace_all;
using sidis5d::to_lower_copy;
using sidis5d::key_in_file;
using sidis5d::safe_write;
using sidis5d::Crash_Report;
using sidis5d::Construct_Email;
using sidis5d::Update_Email;
using sidis5d::Histogram_Name_Def;
using sidis5d::Find_Bins_From_Histo_Name;
using sidis5d::ConvertResult;
using sidis5d::Convert_All_Kinematic_Bins;
using sidis5d::skip_condition_z_pT_bins;
using sidis5d::Get_Num_of_z_pT_Bins_w_Migrations;
using sidis5d::coerce_bin_value;

namespace {

const std::regex kSliceIncrementRe(R"(_Slice_1_\(Increment='(\d+)'\))");

int extract_slice_increment(const std::string& name){
    std::smatch match;
    if(std::regex_search(name, match, kSliceIncrementRe) && (match.size() > 1)){
        return std::atoi(match[1].str().c_str());
    }
    return -1;
}

std::string Strip_Slice_Increment(const std::string& name){
    return std::regex_replace(name, kSliceIncrementRe, "");
}

std::string Apply_Matrix_1D_Replacements(std::string name){
    name = replace_all(name, "'5D_Response_Matrix'", "'5D_Response_Matrix_1D'");
    name = replace_all(name, "'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'");
    return name;
}

std::string Apply_Background_1D_Replacements(std::string name){
    name = replace_all(name, "'5D_Response_Matrix_1D'", "'Background_5D_Response_Matrix_1D'");
    name = replace_all(name, "'Response_Matrix_Normal_1D'", "'Background_Response_Matrix_1D'");
    return name;
}

bool Passes_Weighed_Filter(const std::string& name, const UnfoldArgs& args){
    const std::vector<std::string> known_tags = {"_(Acc)", "_(JSON)", "_(Spline)", "_(AccJSON)", "_(AccSpline)", "_(Weighed)"};
    bool has_weight_tag = false;
    for(const auto& tag_str : known_tags){
        if(contains(name, tag_str)){ has_weight_tag = true; break; }
    }
    if(!args.weight_tag.empty()){
        if(!contains(name, "_(" + args.weight_tag + ")")){ return false; }
        return true;
    }
    if(args.require_weighed){
        if(!has_weight_tag){ return false; }
    } else {
        if(has_weight_tag){ return false; }
    }
    return true;
}

bool Is_5D_Matrix_Slice_Candidate(const std::string& name, const UnfoldArgs& args){
    if(!contains(name, "MultiDim_Q2_y_z_pT_phi_h")){ return false; }
    if(!contains(name, "_Slice_1_(Increment='")){ return false; }
    if(contains(name, "5D_Response_Matrix_1D")){ return false; }
    if(contains(name, "Response_Matrix_Normal_1D")){ return false; }
    if(contains(name, "Background")){ return false; }
    if(!contains(name, "cut_Complete_SIDIS")){ return false; }
    if(contains(name, "cut_Complete_SIDIS_eS")){ return false; }
    if(contains(name, "cut_Complete_EDIS")){ return false; }
    if(contains(name, "no_cut_eS")){ return false; }
    if(contains(name, "_(lundvpk)") || contains(name, "_(lundrho)")){ return false; }
    if(!Passes_Weighed_Filter(name, args)){ return false; }
    if(contains(name, "5D_Response_Matrix") && contains(name, "_Slice_")){
        // keep
    } else if(contains(name, "Response_Matrix_Normal") && contains(name, "_Slice_")){
        // keep
    } else {
        return false;
    }
    if((args.smearing_options != "no_smear") && (args.smearing_options != "both") && contains(name, "(Smear-Type='')")){
        return false;
    }
    if((args.smearing_options != "smear") && (args.smearing_options != "both") && contains(name, "(Smear-Type='smear')")){
        return false;
    }
    return true;
}

struct MatrixCandidate {
    std::string out_print_main;
    std::string out_print_main_mdf;
    std::string out_print_main_mdf_base;
    std::string out_print_main_mdf_1D;
    std::map<std::string, TH2*> Histo_List;
    int increment = 0;
    int num_bins = 0;
    int num_slices = 0;
    double Min_Range = 0;
    double Max_Range = 0;
    bool ok = false;
};

MatrixCandidate Build_5D_Matrix_Candidate(TFile* mdf, const std::string& out_print_main){
    MatrixCandidate cand;
    std::string out_print_main_mdf = out_print_main;
    int detected_increment = extract_slice_increment(out_print_main_mdf);
    if(detected_increment < 0){ return cand; }
    std::string Base_Name = replace_all(out_print_main_mdf, "_Slice_1_", "_Slice_NUMBER_");
    int Slice_Num = 1;
    while(Slice_Num < 800){
        std::string slice_name = replace_all(Base_Name, "_Slice_NUMBER_", "_Slice_" + std::to_string(Slice_Num) + "_");
        TH2* histo_sliced = dynamic_cast<TH2*>(mdf->Get(slice_name.c_str()));
        if(histo_sliced != nullptr){
            cand.Histo_List[slice_name] = histo_sliced;
            ++Slice_Num;
        } else {
            break;
        }
    }
    int num_slices = static_cast<int>(cand.Histo_List.size());
    if(num_slices < 1){ return cand; }
    std::string slice1_name = replace_all(Base_Name, "_Slice_NUMBER_", "_Slice_1_");
    TH2* slice1 = cand.Histo_List[slice1_name];
    if((slice1 != nullptr) && (detected_increment != slice1->GetNbinsX())){
        detected_increment = slice1->GetNbinsX();
    }
    auto bins = Find_Bins_From_Histo_Name(out_print_main_mdf);
    cand.out_print_main = out_print_main;
    cand.out_print_main_mdf = out_print_main_mdf;
    cand.out_print_main_mdf_base = Strip_Slice_Increment(out_print_main_mdf);
    cand.out_print_main_mdf_1D = Apply_Matrix_1D_Replacements(cand.out_print_main_mdf_base);
    cand.increment = detected_increment;
    cand.num_bins = bins.ok ? bins.num_bins : 0;
    cand.num_slices = num_slices;
    cand.Min_Range = bins.min_bin;
    cand.Max_Range = bins.max_bin;
    cand.ok = true;
    return cand;
}

MatrixCandidate Select_5D_Matrix_Candidate(std::vector<MatrixCandidate> candidates, TFile* mdf, UnfoldArgs& args){
    MatrixCandidate none;
    if(candidates.empty()){ return none; }
    std::vector<MatrixCandidate> filtered = candidates;
    if(args.has_increment){
        std::vector<MatrixCandidate> keep;
        for(const auto& c : filtered){
            if(c.increment == args.increment){ keep.push_back(c); }
        }
        if(keep.empty()){
            Crash_Report(args, "No 5D matrix found with --increment=" + std::to_string(args.increment));
        }
        filtered = keep;
    }
    if(args.has_num_bins){
        std::vector<MatrixCandidate> keep;
        for(const auto& c : filtered){
            if(c.num_bins == args.num_bins){ keep.push_back(c); }
        }
        if(keep.empty()){
            Crash_Report(args, "No 5D matrix found with --num_bins=" + std::to_string(args.num_bins));
        }
        filtered = keep;
    }
    if(filtered.size() == 1){ return filtered[0]; }
    std::vector<MatrixCandidate> consistent;
    for(const auto& c : filtered){
        if(c.increment * c.num_slices == c.num_bins){ consistent.push_back(c); }
    }
    if(!consistent.empty()){ filtered = consistent; }
    std::vector<MatrixCandidate> verified;
    for(const auto& c : filtered){
        if(!key_in_file(mdf, c.out_print_main_mdf_1D)){ continue; }
        TH1* MC_REC_1D_test = dynamic_cast<TH1*>(mdf->Get(c.out_print_main_mdf_1D.c_str()));
        if((MC_REC_1D_test != nullptr) && (MC_REC_1D_test->GetNbinsX() == c.num_bins)){
            verified.push_back(c);
        }
    }
    if(!verified.empty()){ filtered = verified; }
    if(filtered.size() > 1){
        std::sort(filtered.begin(), filtered.end(), [](const MatrixCandidate& a, const MatrixCandidate& b){
            return a.num_bins > b.num_bins;
        });
        std::cout << "\n" << Color::BYELLOW << "Multiple 5D matrix configurations found; using increment="
                  << filtered[0].increment << ", num_bins=" << filtered[0].num_bins
                  << ", num_slices=" << filtered[0].num_slices << Color::END << "\n" << std::endl;
    }
    return filtered.empty() ? none : filtered[0];
}

MatrixCandidate Detect_5D_Matrix_Config(TFile* mdf, UnfoldArgs& args){
    std::vector<MatrixCandidate> candidates;
    TIter next(mdf->GetListOfKeys());
    while(TKey* key = dynamic_cast<TKey*>(next())){
        std::string out_print_main = key->GetName();
        if(!Is_5D_Matrix_Slice_Candidate(out_print_main, args)){ continue; }
        MatrixCandidate candidate = Build_5D_Matrix_Candidate(mdf, out_print_main);
        if(candidate.ok){ candidates.push_back(candidate); }
    }
    return Select_5D_Matrix_Candidate(candidates, mdf, args);
}

void Validate_And_Record_5D_Dimensions(UnfoldArgs& args, const MatrixCandidate& detected, TH1* MC_REC_1D){
    args.increment_5d = detected.increment;
    args.num_bins_5d = detected.num_bins;
    args.num_slices_5d = detected.num_slices;
    if(MC_REC_1D != nullptr){
        if(MC_REC_1D->GetNbinsX() != args.num_bins_5d){
            Crash_Report(args, "MC_REC_1D.GetNbinsX()=" + std::to_string(MC_REC_1D->GetNbinsX()) +
                         " != auto-detected num_bins=" + std::to_string(args.num_bins_5d));
        }
        if(args.increment_5d * args.num_slices_5d != args.num_bins_5d){
            Crash_Report(args, "increment*num_slices (" + std::to_string(args.increment_5d) + "*" +
                         std::to_string(args.num_slices_5d) + ") != num_bins (" + std::to_string(args.num_bins_5d) + ")");
        }
    }
    if(args.has_increment){
        if(args.increment != args.increment_5d){
            Crash_Report(args, "User --increment=" + std::to_string(args.increment) +
                         " != auto-detected " + std::to_string(args.increment_5d));
        }
        args.increment_5d = args.increment;
    } else {
        args.increment = args.increment_5d;
        args.has_increment = true;
    }
    if(args.has_num_bins){
        if(args.num_bins != args.num_bins_5d){
            Crash_Report(args, "User --num_bins=" + std::to_string(args.num_bins) +
                         " != auto-detected " + std::to_string(args.num_bins_5d));
        }
        args.num_bins_5d = args.num_bins;
    } else {
        args.num_bins = args.num_bins_5d;
        args.has_num_bins = true;
    }
    std::cout << "\n" << Color::BOLD << "Auto-detected 5D configuration:" << Color::END
              << " increment=" << args.increment_5d
              << ", num_bins=" << args.num_bins_5d
              << ", num_slices=" << args.num_slices_5d << "\n" << std::endl;
}

TH2D* Rebuild_Matrix_5D(const std::map<std::string, TH2*>& List_of_Sliced_Histos,
                        const std::string& Standard_Name,
                        int Increment,
                        const std::string& Title){
    auto bins = Find_Bins_From_Histo_Name(Standard_Name);
    int Num__Bins = bins.num_bins;
    double Min_Range = bins.min_bin;
    double Max_Range = bins.max_bin;
    if(Increment <= 0){
        Increment = extract_slice_increment(Standard_Name);
        if(Increment <= 0){
            for(const auto& kv : List_of_Sliced_Histos){
                int found = extract_slice_increment(kv.first);
                if(found > 0){ Increment = found; break; }
            }
        }
        if((Increment <= 0) && (!List_of_Sliced_Histos.empty())){
            Increment = List_of_Sliced_Histos.begin()->second->GetNbinsX();
        }
    }
    std::string Slicing_Name = Standard_Name + "_Slice_SLICE-NUM_(Increment='" + std::to_string(Increment) + "')";
    std::cout << "\n" << Color::BBLUE << "Running Rebuild_Matrix_5D(...)" << Color::END << "\n" << std::endl;
    int Num_Slices = (Increment == 0) ? 0 : (Num__Bins / Increment);
    for(const std::string& test : std::vector<std::string>{"1", std::to_string(Num_Slices)}){
        std::string missing_name = replace_all(Slicing_Name, "SLICE-NUM", test);
        if(List_of_Sliced_Histos.find(missing_name) == List_of_Sliced_Histos.end()){
            std::cout << Color::Error << "ERROR IN Rebuild_Matrix_5D(...): " << Color::END_R
                      << "'Slicing_Name' is missing from 'List_of_Sliced_Histos'" << Color::END_B
                      << "\n\tSlicing_Name = " << missing_name << std::endl;
            return nullptr;
        }
    }
    std::string Histo_Title = Title;
    if(Title == "Default"){
        auto it = List_of_Sliced_Histos.find(replace_all(Slicing_Name, "SLICE-NUM", "1"));
        TH2* first = it->second;
        Histo_Title = std::string(first->GetTitle()) + ";" + first->GetXaxis()->GetTitle() + ";" + first->GetYaxis()->GetTitle();
    }
    TH2D* Rebuilt_5D_Matrix = new TH2D(Standard_Name.c_str(), Histo_Title.c_str(),
                                       Num__Bins, Min_Range, Max_Range, Num__Bins, Min_Range, Max_Range);
    Rebuilt_5D_Matrix->SetDirectory(0);
    int X_Bin_5D = 0;
    for(int slice_num = 1; slice_num <= Num_Slices; ++slice_num){
        TH2* Histo_Add = List_of_Sliced_Histos.at(replace_all(Slicing_Name, "SLICE-NUM", std::to_string(slice_num)));
        X_Bin_5D += -1;
        for(int x_bin = 0; x_bin <= Histo_Add->GetNbinsX(); ++x_bin){
            X_Bin_5D += 1;
            for(int y_bin = 0; y_bin <= Histo_Add->GetNbinsY(); ++y_bin){
                Rebuilt_5D_Matrix->SetBinContent(X_Bin_5D, y_bin, Histo_Add->GetBinContent(x_bin, y_bin));
                Rebuilt_5D_Matrix->SetBinError(X_Bin_5D, y_bin, Histo_Add->GetBinError(x_bin, y_bin));
            }
        }
    }
    std::cout << "\n" << Color::BGREEN << "Finished running Rebuild_Matrix_5D(...)" << Color::END << "\n" << std::endl;
    return Rebuilt_5D_Matrix;
}

int q2y_as_int(const std::string& Q2_y){
    try { return std::stoi(Q2_y); }
    catch(...) { return 0; }
}

int First_Valid_MultiDim_Start(int Q2_y, int z_pT_min, int z_pT_max){
    for(int z_pT = z_pT_min; z_pT <= z_pT_max; ++z_pT){
        ConvertResult start_bin = Convert_All_Kinematic_Bins("Q2-y=" + std::to_string(Q2_y) + ", z-pT=" + std::to_string(z_pT),
                                                             "MultiDim_Q2_y_z_pT_phi_h");
        int coerced = coerce_bin_value(start_bin);
        if(coerced >= 0){ return coerced; }
    }
    return -1;
}

bool Resolve_Phi_h_Slice_Range(const std::string& Q2_y, int z_pT, const int phi_h_Binning[4], int& Start_phi_h_bin, int& End_phi_h_bin){
    int q2y = q2y_as_int(Q2_y);
    if(z_pT != 0){
        if(skip_condition_z_pT_bins(q2y, z_pT)){ return false; }
        ConvertResult start = Convert_All_Kinematic_Bins("Q2-y=" + Q2_y + ", z-pT=" + std::to_string(z_pT),
                                                         "MultiDim_Q2_y_z_pT_phi_h");
        int coerced = coerce_bin_value(start);
        if(coerced < 0){ return false; }
        Start_phi_h_bin = coerced;
        End_phi_h_bin = Start_phi_h_bin + phi_h_Binning[2];
    } else {
        int z_pT_Range = std::get<1>(Get_Num_of_z_pT_Bins_w_Migrations(q2y));
        Start_phi_h_bin = First_Valid_MultiDim_Start(q2y, 1, z_pT_Range);
        if(Start_phi_h_bin < 0){ return false; }
        End_phi_h_bin = First_Valid_MultiDim_Start(q2y + 1, 1, std::get<1>(Get_Num_of_z_pT_Bins_w_Migrations(q2y + 1)));
        if(End_phi_h_bin < 0){
            int last_start = Start_phi_h_bin;
            for(int z_test = 1; z_test <= z_pT_Range; ++z_test){
                ConvertResult start_test = Convert_All_Kinematic_Bins("Q2-y=" + std::to_string(q2y) + ", z-pT=" + std::to_string(z_test),
                                                                      "MultiDim_Q2_y_z_pT_phi_h");
                int coerced = coerce_bin_value(start_test);
                if(coerced >= 0){ last_start = coerced; }
            }
            End_phi_h_bin = last_start + phi_h_Binning[2];
        }
    }
    return true;
}

struct SliceEntry {
    std::string Q2_y;
    int z_pT = 0;
    int Start_phi_h_bin = 0;
    int End_phi_h_bin = 0;
    std::string Bin_Title;
};

struct SliceMetadata {
    int phi_h_Binning[4] = {0, 360, 24, 15};
    std::vector<SliceEntry> entries;
};

SliceMetadata Build_Multi5D_Slice_Metadata(const UnfoldArgs& args){
    SliceMetadata meta;
    for(const auto& Q2_y : args.Q2_y_Bin_List){
        if((Q2_y == "0") || (Q2_y == "All")){ continue; }
        int z_pT_Range = std::get<1>(Get_Num_of_z_pT_Bins_w_Migrations(q2y_as_int(Q2_y)));
        for(int z_pT = 0; z_pT <= z_pT_Range; ++z_pT){
            std::ostringstream title;
            title << RootColor::Bold << "{#scale[1.25]{#color[" << RootColor::Red << "]{Q^{2}-y Bin: "
                  << ((Q2_y != "0") ? Q2_y : "All") << "} #topbar #color[" << RootColor::Red
                  << "]{z-P_{T} Bin: " << ((z_pT != 0) ? std::to_string(z_pT) : "All") << "}}}";
            int start_bin = 0, end_bin = 0;
            if(!Resolve_Phi_h_Slice_Range(Q2_y, z_pT, meta.phi_h_Binning, start_bin, end_bin)){ continue; }
            SliceEntry entry;
            entry.Q2_y = Q2_y;
            entry.z_pT = z_pT;
            entry.Start_phi_h_bin = start_bin;
            entry.End_phi_h_bin = end_bin;
            entry.Bin_Title = title.str();
            meta.entries.push_back(entry);
        }
    }
    return meta;
}

bool Stream_Write_Slice_Hist(TH1* hist, TFile* output_file, bool stream_write, int* save_count_ref, bool test_mode, const UnfoldArgs& args){
    if(!stream_write){ return false; }
    hist->GetYaxis()->SetTitle("");
    if((!test_mode) && (output_file != nullptr)){
        safe_write(hist, output_file);
    }
    if(save_count_ref != nullptr){
        *save_count_ref += 1;
        if(args.verbose){
            char prefix[128];
            if(!test_mode){
                std::snprintf(prefix, sizeof(prefix), "%sSaved Histo %4.0f)", Color::BGREEN, static_cast<double>(*save_count_ref));
            } else {
                std::snprintf(prefix, sizeof(prefix), "%sWould have saved Histo %4.0f)", Color::PINK, static_cast<double>(*save_count_ref));
            }
            std::cout << prefix << "\n\t" << Color::BBLUE << hist->GetName() << Color::END << std::endl;
        }
    }
    hist->SetDirectory(0);
    return true;
}

int Multi5D_Slice(TH1* Histo, TH1* Histo_Cut, const std::string& Title_In, const std::string& Name_In,
                  const std::string& Method, std::string Variable, std::string Smear,
                  UnfoldArgs& args, const SliceMetadata* slice_metadata,
                  TFile* output_file, bool stream_write, int* save_count_ref, bool test_mode){
    (void)Title_In;
    std::cout << "\n" << Color::BLUE << "Running Multi5D_Slice(...)" << Color::END << "\n" << std::endl;
    try {
        std::string Name = Name_In;
        if(Name != "none"){
            if((Name == "histo") || (Name == "Histo") || (Name == "input") || (Name == "default")){
                Name = Histo->GetName();
            }
            if(!contains(Name, "MultiDim_Q2_y_z_pT_phi_h")){
                std::cout << Color::RED << "ERROR: WRONG TYPE OF HISTOGRAM\nName = " << Color::END << Name
                          << "\nMulti5D_Slice() should be used on the histograms with the 'MultiDim_Q2_y_z_pT_phi_h' bin variable\n\n";
                return -1;
            }
        }
        if(replace_all(Variable, "_smeared", "") != "MultiDim_Q2_y_z_pT_phi_h"){
            std::cout << Color::RED << "ERROR in Multi5D_Slice(): Not set up for other variables (yet)\n"
                      << Color::END << "Variable = " << Variable << "\n\n";
            return -1;
        }
        if(contains(Smear, "mear") && (!contains(Variable, "_smeared"))){
            Variable = Variable + "_smeared";
        }
        if((!contains(Smear, "mear")) && contains(Variable, "_smeared")){
            Smear = "Smear";
        }

        std::string Method_Title;
        if((Method == "rdf") || (Method == "Experimental")){
            Method_Title = std::string(" #color[") + std::to_string(RootColor::Blue) + "]{" +
                           (args.sim ? "(MC REC - Pre-Unfolded)}" : "(Experimental)}");
            if(!args.sim){
                Variable = replace_all(Variable, "_smeared", "");
                Smear = "";
            }
        }
        if((Method == "mdf") || (Method == "MC REC")){
            Method_Title = std::string(" #color[") + std::to_string(RootColor::Red) + "]{(MC REC)}";
        }
        if((Method == "gdf") || (Method == "gen") || (Method == "MC GEN")){
            Method_Title = std::string(" #color[") + std::to_string(RootColor::Green) + "]{(MC GEN" +
                           ((Method == "gen") ? " - Matched" : "") + ")}";
            Variable = replace_all(Variable, "_smeared", "");
            Smear = "";
        }
        if((Method == "tdf") || (Method == "true")){
            Method_Title = std::string(" #color[") + std::to_string(RootColor::Cyan) + "]{(MC TRUE)}";
            Variable = replace_all(Variable, "_smeared", "");
            Smear = "";
        }
        if((Method == "bbb") || (Method == "Bin") || (Method == "Bin-by-Bin") || (Method == "Bin-by-bin")){
            Method_Title = std::string(" #color[") + std::to_string(RootColor::Brown) + "]{(Bin-by-Bin)}";
        }
        if((Method == "bayes") || (Method == "bayesian") || (Method == "Bayesian")){
            Method_Title = std::string(" #color[") + std::to_string(RootColor::Teal) + "]{(Bayesian Unfolded)}";
        }
        if((Method == "Acceptance") || (Method == "Background")){
            Method_Title = std::string("(") + RootColor::Bold + "{" + Method + "})";
        }

        int phi_h_Binning[4] = {0, 360, 24, 15};
        if(slice_metadata != nullptr){
            for(int i = 0; i < 4; ++i){ phi_h_Binning[i] = slice_metadata->phi_h_Binning[i]; }
        }

        if(Name != "none"){
            Name = Histogram_Name_Def(Name, "MultiDim_5D_Histo", Method, "Skip", Smear,
                                      "MultiDim_5D_Q2_y_Bin_Info", "MultiDim_5D_z_pT_Bin_Info",
                                      "Default", replace_all(Variable, "_smeared", ""), args);
            if((Method == "tdf") || (Method == "true")){
                Name = replace_all(replace_all(Name, "mdf", "tdf"), "gdf", "tdf");
            }
        }

        auto Process_One_Slice_Entry = [&](const std::string& Q2_y, int z_pT, int Start_phi_h_bin, int End_phi_h_bin, const std::string& Bin_Title){
            std::string Title_Out = std::string("#splitline{") + RootColor::Bold + "{5D #phi_{h}" + Method_Title + " Plot}}{" + Bin_Title + "}";
            if((!args.pass_version.empty()) && (!contains(Title_Out, args.pass_version))){
                Title_Out = std::string("#splitline{") + Title_Out + "}{" + RootColor::Bold + "{" + args.pass_version + "}}";
            }
            std::string Name_Out = replace_all(Name, "MultiDim_5D_Q2_y_Bin_Info", ((Q2_y != "0") && (Q2_y != "All")) ? Q2_y : "All");
            Name_Out = replace_all(Name_Out, "MultiDim_5D_z_pT_Bin_Info", (z_pT != 0) ? std::to_string(z_pT) : "All");
            std::string hist_title = Title_Out + "; #phi_{h} [" + RootColor::Degrees + "]";
            TH1D* Slice_Hist = new TH1D(Name_Out.c_str(), hist_title.c_str(), phi_h_Binning[2], phi_h_Binning[0], phi_h_Binning[1]);
            Slice_Hist->SetDirectory(0);
            int ii_bin_num = Start_phi_h_bin;
            int ii_LastNum = Start_phi_h_bin;
            std::map<double, double> phi_Content;
            std::map<double, double> phi___Error;
            for(int phi_bin = phi_h_Binning[0]; phi_bin < phi_h_Binning[1]; phi_bin += phi_h_Binning[3]){
                phi_Content[phi_bin + 0.5 * phi_h_Binning[3]] = 0;
                phi___Error[phi_bin + 0.5 * phi_h_Binning[3]] = 0;
            }
            while(ii_bin_num < End_phi_h_bin){
                bool OverFlow_Con = false;
                if((End_phi_h_bin - Start_phi_h_bin) != phi_h_Binning[2]){
                    ConvertResult Q2_y_bin_0 = (ii_bin_num != 0)
                        ? Convert_All_Kinematic_Bins("MultiDim_Q2_y_z_pT_phi_h=" + std::to_string(ii_bin_num - 1), "Q2-y")
                        : ConvertResult{true, 1};
                    ConvertResult Q2_y_bin_1 = Convert_All_Kinematic_Bins("MultiDim_Q2_y_z_pT_phi_h=" + std::to_string(ii_bin_num), "Q2-y");
                    ConvertResult z_pT_bin_0 = (ii_bin_num != 0)
                        ? Convert_All_Kinematic_Bins("MultiDim_Q2_y_z_pT_phi_h=" + std::to_string(ii_bin_num - 1), "z-pT")
                        : ConvertResult{true, 1};
                    ConvertResult z_pT_bin_1 = Convert_All_Kinematic_Bins("MultiDim_Q2_y_z_pT_phi_h=" + std::to_string(ii_bin_num), "z-pT");
                    if((z_pT_bin_0 != z_pT_bin_1) && (Q2_y_bin_0 == Q2_y_bin_1)){
                        if(ii_LastNum + 1 == ii_bin_num){ OverFlow_Con = true; }
                        ii_LastNum = ii_bin_num;
                    } else if(Q2_y_bin_0 != Q2_y_bin_1){
                        ii_LastNum = Start_phi_h_bin;
                    } else if(Q2_y_bin_1.ok && z_pT_bin_1.ok && skip_condition_z_pT_bins(Q2_y_bin_1.value, z_pT_bin_1.value)){
                        OverFlow_Con = true;
                        ii_LastNum = ii_bin_num;
                    }
                }
                if(OverFlow_Con){
                    ii_bin_num += 1;
                    continue;
                }
                for(int phi_bin = phi_h_Binning[0]; phi_bin < phi_h_Binning[1]; phi_bin += phi_h_Binning[3]){
                    int bin_ii = Histo->FindBin(ii_bin_num);
                    if(Histo_Cut != nullptr){
                        double MultiDim_cut_num = Histo_Cut->GetBinContent(bin_ii);
                        double MultiDim_cut_err = Histo_Cut->GetBinError(bin_ii);
                        if((MultiDim_cut_num == 0) || (MultiDim_cut_num <= MultiDim_cut_err)){
                            phi_Content[phi_bin + 0.5 * phi_h_Binning[3]] += 0;
                            phi___Error[phi_bin + 0.5 * phi_h_Binning[3]] += 0;
                        } else {
                            phi_Content[phi_bin + 0.5 * phi_h_Binning[3]] += Histo->GetBinContent(bin_ii);
                            phi___Error[phi_bin + 0.5 * phi_h_Binning[3]] += (Histo->GetBinError(bin_ii)) * (Histo->GetBinError(bin_ii));
                        }
                    } else {
                        phi_Content[phi_bin + 0.5 * phi_h_Binning[3]] += Histo->GetBinContent(bin_ii);
                        phi___Error[phi_bin + 0.5 * phi_h_Binning[3]] += (Histo->GetBinError(bin_ii)) * (Histo->GetBinError(bin_ii));
                    }
                    ii_bin_num += 1;
                }
            }
            for(int phi_bin = phi_h_Binning[0]; phi_bin < phi_h_Binning[1]; phi_bin += phi_h_Binning[3]){
                double center = phi_bin + 0.5 * phi_h_Binning[3];
                Slice_Hist->Fill(center, phi_Content[center]);
                Slice_Hist->SetBinError(Slice_Hist->FindBin(center), std::sqrt(phi___Error[center]));
            }
            double ymin = Slice_Hist->GetBinContent(Slice_Hist->GetMinimumBin());
            double ymax = Slice_Hist->GetBinContent(Slice_Hist->GetMaximumBin());
            Slice_Hist->GetYaxis()->SetRangeUser((ymin < 0) ? 1.5 * ymin : 0, 1.5 * ymax);
            auto set_color = [&](int col){
                Slice_Hist->SetLineColor(col);
                Slice_Hist->SetMarkerColor(col);
            };
            if((Method == "rdf") || (Method == "Experimental")){ set_color(RootColor::Blue); }
            if((Method == "mdf") || (Method == "MC REC")){ set_color(RootColor::Red); }
            if((Method == "gdf") || (Method == "gen") || (Method == "MC GEN")){ set_color(RootColor::Green); }
            if((Method == "tdf") || (Method == "true")){ set_color(RootColor::Cyan); }
            if((Method == "bbb") || (Method == "Bin") || (Method == "Bin-by-Bin") || (Method == "Bin-by-bin")){ set_color(RootColor::Brown); }
            if((Method == "bayes") || (Method == "bayesian") || (Method == "Bayesian")){ set_color(RootColor::Teal); }
            if(Method == "Background"){ set_color(RootColor::Black); }
            Stream_Write_Slice_Hist(Slice_Hist, output_file, stream_write, save_count_ref, test_mode, args);
        };

        if(slice_metadata != nullptr){
            for(const auto& entry : slice_metadata->entries){
                Process_One_Slice_Entry(entry.Q2_y, entry.z_pT, entry.Start_phi_h_bin, entry.End_phi_h_bin, entry.Bin_Title);
            }
        }
        return 0;
    } catch(const std::exception& exc){
        std::cout << Color::Error << "Multi5D_Slice(...) ERROR:" << Color::END << "\n" << exc.what() << "\n";
        return -1;
    } catch(...){
        std::cout << Color::Error << "Multi5D_Slice(...) ERROR:" << Color::END << "\n";
        return -1;
    }
}

TH1* Unfold_Function(TH2* Response_2D, TH1* ExREAL_1D, TH1* MC_REC_1D, TH1* MC_GEN_1D, TH1* MC_BGS_1D, UnfoldArgs& args){
    std::cout << Color::BCYAN << "Starting " << Color::UNDERLINE << Color::GREEN << "RooUnfold" << Color::END_B
              << Color::CYAN << " Unfolding Procedure..." << Color::END << std::endl;
    std::string Name_Main = Response_2D->GetName();
    std::string Name_Main_Print = Name_Main;
    auto nb_pos = Name_Main.find("-[NumBins");
    if(nb_pos != std::string::npos){
        Name_Main_Print = Name_Main.substr(0, nb_pos) + "))";
    }
    std::string clean_name = replace_all(Name_Main_Print, "(Data-Type='mdf'), ", "");
    if(contains(Name_Main, "MultiDim_")){
        Update_Email(args, "", std::string("\n\t") + Color::BOLD + "Began Unfolding Histogram:" + Color::END + "\n\t" + clean_name, true);
    } else {
        std::cout << "\t" << Color::BOLD << "Unfolding Histogram:" << Color::END << "\n\t" << clean_name << std::endl;
    }

    int nBins_CVM = ExREAL_1D->GetNbinsX();
    double bin_Width = ExREAL_1D->GetBinWidth(1);
    double MinBinCVM = ExREAL_1D->GetBinCenter(0);
    double MaxBinCVM = ExREAL_1D->GetBinCenter(nBins_CVM);
    MinBinCVM += 0.5 * bin_Width;
    MaxBinCVM += 0.5 * bin_Width;
    ExREAL_1D->GetXaxis()->SetRange(0, nBins_CVM);
    MC_REC_1D->GetXaxis()->SetRange(0, nBins_CVM);
    MC_GEN_1D->GetXaxis()->SetRange(0, nBins_CVM);
    Response_2D->GetXaxis()->SetRange(0, nBins_CVM);
    Response_2D->GetYaxis()->SetRange(0, nBins_CVM);
    if(MC_BGS_1D != nullptr){
        MC_BGS_1D->GetXaxis()->SetRange(0, nBins_CVM);
    }

    TH2* Response_2D_Input = Response_2D;
    std::string Response_2D_Input_Title = std::string(Response_2D->GetTitle()) + ";" +
                                          Response_2D->GetXaxis()->GetTitle() + ";" +
                                          Response_2D->GetYaxis()->GetTitle();
    if(!contains(Name_Main, "MultiDim_Q2_y_z_pT_phi_h")){
        Response_2D_Input_Title = std::string(Response_2D->GetTitle()) + ";" +
                                  Response_2D->GetYaxis()->GetTitle() + ";" +
                                  Response_2D->GetXaxis()->GetTitle();
        TH2D* flipped = new TH2D((std::string(Response_2D->GetName()) + "_Flipped").c_str(),
                                 Response_2D_Input_Title.c_str(),
                                 Response_2D->GetNbinsY(), MinBinCVM, MaxBinCVM,
                                 Response_2D->GetNbinsX(), MinBinCVM, MaxBinCVM);
        flipped->SetDirectory(0);
        for(int gen_bin = 0; gen_bin <= nBins_CVM; ++gen_bin){
            for(int rec_bin = 0; rec_bin <= nBins_CVM; ++rec_bin){
                flipped->SetBinContent(rec_bin, gen_bin, Response_2D->GetBinContent(gen_bin, rec_bin));
                flipped->SetBinError(rec_bin, gen_bin, Response_2D->GetBinError(gen_bin, rec_bin));
            }
        }
        Response_2D_Input = flipped;
    }

    if(!((nBins_CVM == MC_REC_1D->GetNbinsX()) &&
         (MC_REC_1D->GetNbinsX() == MC_GEN_1D->GetNbinsX()) &&
         (MC_GEN_1D->GetNbinsX() == Response_2D_Input->GetNbinsX()) &&
         (Response_2D_Input->GetNbinsX() == Response_2D_Input->GetNbinsY()))){
        std::cout << Color::RED << "Unequal Bins..." << Color::END << std::endl;
        std::cout << "nBins_CVM = " << nBins_CVM << std::endl;
        std::cout << "MC_REC_1D.GetNbinsX() = " << MC_REC_1D->GetNbinsX() << std::endl;
        std::cout << "MC_GEN_1D.GetNbinsX() = " << MC_GEN_1D->GetNbinsX() << std::endl;
        std::cout << "Response_2D.GetNbinsX() = " << Response_2D->GetNbinsX() << std::endl;
        std::cout << "Response_2D.GetNbinsY() = " << Response_2D->GetNbinsY() << std::endl;
        args.timer.time_elapsed();
        return nullptr;
    }

    try {
        std::string resp_name = replace_all(Response_2D_Input->GetName(), "_Flipped", "") + "_RooUnfoldResponse_Object";
        RooUnfoldResponse Response_RooUnfold(MC_REC_1D, MC_GEN_1D, Response_2D_Input, resp_name.c_str(), Response_2D_Input_Title.c_str());
        if(MC_BGS_1D != nullptr){
            for(int rec_bin = 0; rec_bin <= nBins_CVM; ++rec_bin){
                double rec_val = MC_BGS_1D->GetBinCenter(rec_bin);
                double rec_con = MC_BGS_1D->GetBinContent(rec_bin);
                Response_RooUnfold.Fake(rec_val, rec_con);
            }
        }

        std::string Unfold_Title = "RooUnfold (Bayesian)";
        std::cout << "\t" << Color::CYAN << "Using " << Color::BGREEN << Unfold_Title << Color::END_C
                  << " method to unfold..." << Color::END << std::endl;

        int bayes_iterations = 10;
        if(contains(Name_Main, "MultiDim_Q2_y_z_pT_phi_h")){
            bayes_iterations = 4;
            std::cout << Color::BOLD << "Performing 5D Unfolding with " << Color::UNDERLINE << bayes_iterations
                      << Color::END_B << " iteration(s)..." << Color::END << std::endl;
        }
        if(args.bayes_iterations){
            if(args.bayes_iterations != bayes_iterations){
                bayes_iterations = args.bayes_iterations;
                std::cout << Color::BOLD << "Performing Unfolding with " << Color::UNDERLINE << bayes_iterations
                          << Color::END_B << " iteration(s)..." << Color::END << std::endl;
            }
        } else {
            args.bayes_iterations = bayes_iterations;
        }

        RooUnfoldBayes Unfolding_Histo(&Response_RooUnfold, ExREAL_1D, bayes_iterations);
        Unfolding_Histo.SetNToys(args.Num_Toys);
        TH1* Unfolded_Histo = Unfolding_Histo.Hunfold(RooUnfold::kCovToys);
        if(Unfolded_Histo == nullptr){
            std::cout << "\n" << Color::Error << "FAILED TO UNFOLD A HISTOGRAM (RooUnfold)..." << Color::END << std::endl;
            return nullptr;
        }
        Unfolded_Histo->SetDirectory(0);

        for(int bin_rec = 0; bin_rec <= MC_REC_1D->GetNbinsX(); ++bin_rec){
            if(MC_REC_1D->GetBinContent(bin_rec) == 0){
                Unfolded_Histo->SetBinError(bin_rec, Unfolded_Histo->GetBinContent(bin_rec) + Unfolded_Histo->GetBinError(bin_rec));
            }
        }

        TH1* Bin_Acceptance = dynamic_cast<TH1*>(MC_REC_1D->Clone());
        Bin_Acceptance->SetDirectory(0);
        Bin_Acceptance->Sumw2();
        Bin_Acceptance->Divide(MC_GEN_1D);
        for(int bin_acceptance = 0; bin_acceptance <= Bin_Acceptance->GetNbinsX(); ++bin_acceptance){
            bool no_sector = (!contains(Name_Main_Print, "_eS1o")) && (!contains(Name_Main_Print, "_eS2o")) &&
                             (!contains(Name_Main_Print, "_eS3o")) && (!contains(Name_Main_Print, "_eS4o")) &&
                             (!contains(Name_Main_Print, "_eS5o")) && (!contains(Name_Main_Print, "_eS6o"));
            double acc = Bin_Acceptance->GetBinContent(bin_acceptance);
            if((no_sector && (acc < args.Min_Allowed_Acceptance_Cut)) || (acc < 0.5 * args.Min_Allowed_Acceptance_Cut)){
                Unfolded_Histo->SetBinError(bin_acceptance, 0);
                Unfolded_Histo->SetBinContent(bin_acceptance, 0);
            }
        }
        delete Bin_Acceptance;

        std::string title = replace_all(replace_all(ExREAL_1D->GetTitle(), "Experimental", Unfold_Title),
                                        "Cut: Complete Set of SIDIS Cuts", "");
        title = replace_all(title, "Cut:  Complete Set of SIDIS Cuts", "");
        Unfolded_Histo->SetTitle(title.c_str());
        std::string xtitle = replace_all(ExREAL_1D->GetXaxis()->GetTitle(), "(REC)",
                                         (contains(Name_Main, "smeared") || contains(Name_Main, "smear")) ? "(Smeared)" : "");
        Unfolded_Histo->GetXaxis()->SetTitle(xtitle.c_str());
        std::string smear_tag = contains(to_lower_copy(Name_Main), "smear") ? "Smear" : "''";
        std::string unf_name = std::string("(MultiDim_5D_Histo)_(Bayesian)_(SMEAR=") + smear_tag +
                               ")_(Q2_y_z_pT_Bin_All)_(MultiDim_Q2_y_z_pT_phi_h)";
        Unfolded_Histo->SetName(unf_name.c_str());

        if(contains(Name_Main, "MultiDim_")){
            Update_Email(args, "", "\tFinished Unfolding the histogram at:");
            args.timer.time_elapsed();
        }
        std::cout << Color::BCYAN << "Finished " << Color::GREEN << Unfold_Title << Color::END_B
                  << Color::CYAN << " Unfolding Procedure.\n" << Color::END << std::endl;
        if(Response_2D_Input != Response_2D){ delete Response_2D_Input; }
        return Unfolded_Histo;
    } catch(const std::exception& exc){
        std::cout << "\n" << Color::Error << "FAILED TO UNFOLD A HISTOGRAM (RooUnfold)...\nERROR:\n"
                  << Color::END << exc.what() << std::endl;
        return nullptr;
    }
}

std::pair<TH1*, TH1*> subtract_bkg_with_zero_floor(TH1* hist_data, TH1* hist_background){
    std::string original_name = hist_data->GetName();
    TH1* original_histo = dynamic_cast<TH1*>(hist_data->Clone((original_name + "_(wExclusive_Background)").c_str()));
    original_histo->SetDirectory(0);
    std::string orig_title = std::string("#splitline{") + original_histo->GetTitle() +
                             "}{#scale[2]{Before the Exclusive #rho^{0} Background Subtraction}}";
    original_histo->SetTitle(orig_title.c_str());
    TH1* result_histogram = dynamic_cast<TH1*>(hist_data->Clone(original_name.c_str()));
    result_histogram->SetDirectory(0);
    result_histogram->Add(hist_background, -1.0);
    for(int global_bin = 0; global_bin < result_histogram->GetNcells(); ++global_bin){
        if(result_histogram->GetBinContent(global_bin) < 0){
            result_histogram->SetBinContent(global_bin, 0.0);
        }
    }
    return {original_histo, result_histogram};
}

std::string Smear_For_Histo(TH1* histo){
    std::string name = histo->GetName();
    if(contains(name, "'smear'") || contains(name, "'Smear'") || contains(name, "smeared") || contains(name, "SMEAR=Smear")){
        return "Smear";
    }
    return "";
}

void Run_Slice_Category(TH1* Pre_Sliced_1Ds, const std::string& method, UnfoldArgs& args, TFile* output_file,
                        int* save_count_ref, TH1* MC_BGS_1D, const SliceMetadata& meta){
    if((method == "Background") && (MC_BGS_1D == nullptr)){ return; }
    int result = Multi5D_Slice(Pre_Sliced_1Ds, nullptr, Pre_Sliced_1Ds->GetTitle(), Pre_Sliced_1Ds->GetName(),
                               method, "MultiDim_Q2_y_z_pT_phi_h", Smear_For_Histo(Pre_Sliced_1Ds),
                               args, &meta, output_file, true, save_count_ref, args.test);
    if(result < 0){
        std::cout << Color::Error << "ERROR: Sliced_1Ds = Error" << Color::END << std::endl;
    }
}

UnfoldArgs main_start(int argc, char** argv){
    UnfoldArgs args = sidis5d::parse_args(argc, argv);
    args.timer.start();
    for(const char* attr : {"root", "single_file_input", "pdf_name"}){
        std::string* target = nullptr;
        if(std::string(attr) == "root"){ target = &args.root; }
        else if(std::string(attr) == "single_file_input"){ target = &args.single_file_input; }
        else { target = &args.pdf_name; }
        std::string cleaned = sidis5d::strip_quotes(*target);
        if(cleaned != *target){
            std::cout << Color::BYELLOW << "Cleaned quotes from --" << attr << ": '" << *target
                      << "' -> '" << cleaned << "'" << Color::END << std::endl;
            *target = cleaned;
        }
    }
    if((!args.weight_tag.empty()) && (!contains(args.root, "_W" + args.weight_tag))){
        args.root = replace_all(args.root, ".root", "_W" + args.weight_tag + ".root");
    }
    args.pass_version = "Pass 2";
    args.closure = false;
    args.mod = args.mod && (!args.closure);
    args.smearing_options = args.no_smear ? "no_smear" : "smear";
    if(args.sim){
        std::cout << "\n" << Color::BLUE << "Running Simulated Test\n" << Color::END << std::endl;
        args.standard_histogram_title_addition = "Closure Test - Unfolding Simulation";
    }
    if(args.mod){
        std::cout << "\n" << Color::BLUE << "Using " << Color::BOLD << "Modulated " << Color::END_b
                  << " Monte Carlo Files\n" << Color::END << std::endl;
        if(!args.standard_histogram_title_addition.empty()){
            args.standard_histogram_title_addition = args.standard_histogram_title_addition + " - Using Modulated Response Matrix";
        } else {
            args.standard_histogram_title_addition = "Closure Test - Using Modulated Response Matrix";
        }
    }
    args.Q2_y_Bin_List = args.bins;
    bool has_zero = false;
    for(const auto& b : args.Q2_y_Bin_List){ if(b == "0"){ has_zero = true; } }
    if(!has_zero){ args.Q2_y_Bin_List.push_back("0"); }

    if(args.matrix_pdf){
        std::cout << "\n" << Color::BOLD << "Starting Dedicated 5D Response Matrix PDF Mode\n" << Color::END << std::endl;
        if(!args.test){
            std::cout << "\n" << Color::BBLUE << "Will be saving matrix PDF to " << Color::END_B << args.pdf_name << Color::END << "\n" << std::endl;
        } else {
            std::cout << "\n" << Color::RED << "Will " << Color::Error << "NOT" << Color::END_R
                      << " be saving results (running as a test)\n" << Color::END_b << "Would have saved to "
                      << Color::END_B << args.pdf_name << Color::END << "\n" << std::endl;
        }
    } else if(args.recover_slices){
        std::cout << "\n" << Color::BOLD << "Starting Dedicated 5D Bayesian Slice Recovery Mode\n" << Color::END << std::endl;
        if(!args.test){
            std::cout << "\n" << Color::BBLUE << "Will recover Bayesian slices into " << Color::END_B << args.root << Color::END << "\n" << std::endl;
        } else {
            std::cout << "\n" << Color::RED << "Will " << Color::Error << "NOT" << Color::END_R
                      << " be saving results (running as a test)\n" << Color::END_b
                      << "Would have recovered Bayesian slices into " << Color::END_B << args.root << Color::END << "\n" << std::endl;
        }
    } else {
        if(!args.test){
            std::cout << "\n" << Color::BBLUE << "Will be saving results to " << Color::END_B << args.root << Color::END << "\n" << std::endl;
        } else {
            std::cout << "\n" << Color::RED << "Will " << Color::Error << "NOT" << Color::END_R
                      << " be saving results (running as a test)\n" << Color::END_b << "Would have saved to "
                      << Color::END_B << args.root << Color::END << "\n" << std::endl;
        }
        std::cout << "\n" << Color::BOLD << "Starting Dedicated 5D Unfolding Analysis\n" << Color::END << std::endl;
    }
    std::string smear_print = ((args.smearing_options == "") || (args.smearing_options == "no_smear"))
        ? "No Smear"
        : replace_all(replace_all(args.smearing_options, "_s", "S"), "s", "S");
    std::cout << "\n" << Color::BBLUE << "Smear option selected is: " << smear_print << Color::END << "\n" << std::endl;
    return args;
}

std::pair<TH2D*, MatrixCandidate> Load_And_Rebuild_5D_Response_Matrix(TFile* input_file, UnfoldArgs& args){
    MatrixCandidate detected = Detect_5D_Matrix_Config(input_file, args);
    if(!detected.ok){
        Crash_Report(args, "Could not find a 5D response matrix slice-1 entry in the input file.");
    }
    if(!key_in_file(input_file, detected.out_print_main_mdf_1D)){
        Crash_Report(args, "Missing mdf 1D histogram: " + detected.out_print_main_mdf_1D);
    }
    TH1* MC_REC_1D = dynamic_cast<TH1*>(input_file->Get(detected.out_print_main_mdf_1D.c_str()));
    Validate_And_Record_5D_Dimensions(args, detected, MC_REC_1D);
    std::cout << "\n" << Color::BGREEN << "(5D) Rebuilding Response Matrix: " << detected.out_print_main << Color::END << "\n" << std::endl;
    TH2D* Response_2D = Rebuild_Matrix_5D(detected.Histo_List, detected.out_print_main_mdf_base, args.increment_5d, "Default");
    if(Response_2D == nullptr){
        Crash_Report(args, "Rebuild_Matrix_5D returned ERROR");
    }
    return {Response_2D, detected};
}

int Save_Rebuilt_Matrix_As_Pdf(TH2* Response_2D, const std::string& pdf_path, UnfoldArgs& args){
    if(args.test){
        std::cout << Color::PINK << "Would be saving matrix PDF to: " << Color::BCYAN << pdf_path << Color::END << std::endl;
        Response_2D->SetDirectory(0);
        return 0;
    }
    std::cout << Color::BBLUE << "Saving matrix PDF to: " << Color::BGREEN << pdf_path << Color::END << std::endl;
    TCanvas canvas("Rebuilt_5D_Response_Matrix", "Rebuilt 5D Response Matrix", 1300, 725);
    canvas.SetRightMargin(0.15);
    canvas.SetLeftMargin(0.15);
    canvas.SetBottomMargin(0.15);
    canvas.SetTopMargin(0.175);
    gStyle->SetOptStat("i");
    gStyle->SetStatX(0.900);
    gStyle->SetStatY(0.875);
    gStyle->SetStatW(0.150);
    gStyle->SetStatH(0.200);
    Response_2D->SetDirectory(0);
    Response_2D->SetTitle("5D Response Matrix of Q^{2}-y-z-P_{T}-#phi_{h} Bins");
    Response_2D->GetXaxis()->SetTitle("Q^{2}-y-z-P_{T}-#phi_{h} - REC Bins");
    Response_2D->GetYaxis()->SetTitle("Q^{2}-y-z-P_{T}-#phi_{h} - GEN Bins");
    Response_2D->Draw("colz");
    if(args.logz){ canvas.SetLogz(kTRUE); }
    canvas.Update();
    canvas.SaveAs(pdf_path.c_str());
    if(args.verbose){
        std::cout << Color::BGREEN << "Saved matrix PDF:\n\t" << Color::BBLUE << pdf_path << Color::END << std::endl;
    }
    return 1;
}

int main_5D_matrix_pdf(UnfoldArgs& args){
    TFile* input_file = TFile::Open(args.single_file_input.c_str(), "READ");
    if((input_file == nullptr) || input_file->IsZombie()){
        Crash_Report(args, "Could not open input ROOT file: " + args.single_file_input);
    }
    std::cout << "The total number of histograms in '" << Color::BBLUE << args.single_file_input << Color::END
              << "' is " << Color::BOLD << input_file->GetListOfKeys()->GetSize() << Color::END << std::endl;
    auto rebuilt = Load_And_Rebuild_5D_Response_Matrix(input_file, args);
    args.timer.time_elapsed();
    int saved_count = Save_Rebuilt_Matrix_As_Pdf(rebuilt.first, args.pdf_name, args);
    delete rebuilt.first;
    input_file->Close();
    delete input_file;
    return saved_count;
}

int main_5D_unfold(UnfoldArgs& args, SliceMetadata& meta){
    TFile* input_file = TFile::Open(args.single_file_input.c_str(), "READ");
    if((input_file == nullptr) || input_file->IsZombie()){
        Crash_Report(args, "Could not open input ROOT file: " + args.single_file_input);
    }
    std::cout << "The total number of histograms in '" << Color::BBLUE << args.single_file_input << Color::END
              << "' is " << Color::BOLD << input_file->GetListOfKeys()->GetSize() << Color::END << std::endl;
    MatrixCandidate detected = Detect_5D_Matrix_Config(input_file, args);
    if(!detected.ok){
        Crash_Report(args, "Could not find a 5D response matrix slice-1 entry in the input file.");
    }
    std::string out_print_main_mdf_1D = detected.out_print_main_mdf_1D;
    std::string out_print_main_rdf = replace_all(detected.out_print_main_mdf_base, "(Data-Type='mdf')", "(Data-Type='rdf')");
    std::string out_print_main_gdf = replace_all(detected.out_print_main_mdf_base, "(Data-Type='mdf')", "(Data-Type='gdf')");
    for(const char* tag_str : {"_(AccSpline)", "_(AccJSON)", "_(Spline)", "_(JSON)", "_(Acc)", "_(Weighed)"}){
        out_print_main_rdf = replace_all(out_print_main_rdf, tag_str, "");
    }
    const std::string& weight_tag = args.weight_tag;
    if((weight_tag == "Acc") || (weight_tag == "AccJSON") || (weight_tag == "AccSpline") || weight_tag.empty()){
        for(const char* tag_str : {"_(AccSpline)", "_(AccJSON)", "_(Spline)", "_(JSON)", "_(Acc)", "_(Weighed)"}){
            out_print_main_gdf = replace_all(out_print_main_gdf, tag_str, "");
        }
        if(weight_tag == "AccJSON"){ out_print_main_gdf = out_print_main_gdf + "_(JSON)"; }
        else if(weight_tag == "AccSpline"){ out_print_main_gdf = out_print_main_gdf + "_(Spline)"; }
    }
    out_print_main_gdf = replace_all(out_print_main_gdf, "cut_Complete_EDIS", "no_cut");
    for(int sector_cut_remove = 1; sector_cut_remove <= 6; ++sector_cut_remove){
        out_print_main_gdf = replace_all(out_print_main_gdf, "cut_Complete_SIDIS_eS" + std::to_string(sector_cut_remove) + "o", "no_cut");
    }
    out_print_main_gdf = replace_all(out_print_main_gdf, "cut_Complete_SIDIS", "no_cut");
    out_print_main_gdf = replace_all(out_print_main_gdf, "cut_Complete", "no_cut");
    if(!args.sim){
        out_print_main_rdf = replace_all(out_print_main_rdf, "smear", "");
    }
    out_print_main_gdf = replace_all(out_print_main_gdf, "smear", "");
    out_print_main_rdf = Apply_Matrix_1D_Replacements(out_print_main_rdf);
    out_print_main_gdf = Apply_Matrix_1D_Replacements(out_print_main_gdf);
    if(!key_in_file(input_file, out_print_main_mdf_1D)){
        Crash_Report(args, "Missing mdf 1D histogram: " + out_print_main_mdf_1D);
    }
    TH1* MC_REC_1D = dynamic_cast<TH1*>(input_file->Get(out_print_main_mdf_1D.c_str()));
    Validate_And_Record_5D_Dimensions(args, detected, MC_REC_1D);
    if(args.sim){ out_print_main_rdf = out_print_main_mdf_1D; }
    if(!key_in_file(input_file, out_print_main_rdf)){
        Crash_Report(args, "Missing rdf 1D histogram: " + out_print_main_rdf);
    }
    if(!key_in_file(input_file, out_print_main_gdf)){
        Crash_Report(args, "Missing gdf 1D histogram: " + out_print_main_gdf);
    }
    std::cout << "\n" << Color::BGREEN << "(5D) Unfolding: " << detected.out_print_main << Color::END << "\n" << std::endl;
    TH1* ExREAL_1D = dynamic_cast<TH1*>(input_file->Get(out_print_main_rdf.c_str()));
    TH1* MC_GEN_1D = dynamic_cast<TH1*>(input_file->Get(out_print_main_gdf.c_str()));
    std::string out_print_main_bdf_1D = Apply_Background_1D_Replacements(out_print_main_mdf_1D);
    TH1* MC_BGS_1D = nullptr;
    if(key_in_file(input_file, out_print_main_bdf_1D) && contains(out_print_main_bdf_1D, "Background")){
        MC_BGS_1D = dynamic_cast<TH1*>(input_file->Get(out_print_main_bdf_1D.c_str()));
        std::string bgs_title = std::string("#splitline{BACKGROUND}{") + MC_REC_1D->GetTitle() + "};" +
                                MC_REC_1D->GetXaxis()->GetTitle() + ";" + MC_REC_1D->GetYaxis()->GetTitle();
        MC_BGS_1D->SetTitle(bgs_title.c_str());
    } else {
        std::cout << Color::Error << "\nERROR: Missing Background Histogram " << Color::END_R << "(would be named: "
                  << Color::END_B << out_print_main_bdf_1D << Color::END_R << ")" << Color::END << std::endl;
        throw std::runtime_error("Missing (5D) Background Histogram");
    }
    if(args.sim && (MC_BGS_1D != nullptr)){
        ExREAL_1D->Add(MC_BGS_1D);
    }
    TH1* ExREAL_1D_wExclusive_Background = nullptr;
    std::string out_print_main_rdf_1D_bgs = out_print_main_rdf;
    std::string rho_rdf = out_print_main_rdf_1D_bgs + "_(" + args.background_source + ")";
    std::string rho_mdf = out_print_main_mdf_1D + "_(" + args.background_source + ")";
    if(key_in_file(input_file, rho_rdf)){
        std::cout << Color::BGREEN << "Subtracting the '" << args.background_source << "' files to the 'ExREAL_1D' histogram" << Color::END << std::endl;
        TH1* LundrhoHist_rdf = dynamic_cast<TH1*>(input_file->Get(rho_rdf.c_str()));
        auto sub = subtract_bkg_with_zero_floor(ExREAL_1D, LundrhoHist_rdf);
        ExREAL_1D_wExclusive_Background = sub.first;
        ExREAL_1D = sub.second;
    } else if(key_in_file(input_file, rho_mdf)){
        std::cout << Color::BGREEN << "Subtracting the '" << args.background_source << "' files to the 'ExREAL_1D' histogram" << Color::END << std::endl;
        TH1* LundrhoHist_rdf = dynamic_cast<TH1*>(input_file->Get(rho_mdf.c_str()));
        auto sub = subtract_bkg_with_zero_floor(ExREAL_1D, LundrhoHist_rdf);
        ExREAL_1D_wExclusive_Background = sub.first;
        ExREAL_1D = sub.second;
    } else if(args.background_source != "None"){
        std::cout << Color::Error << "Cannot subtract the '" << args.background_source
                  << "' files to the 'ExREAL_1D' histogram" << Color::END << std::endl;
    }
    TH2D* Response_2D = Rebuild_Matrix_5D(detected.Histo_List, detected.out_print_main_mdf_base, args.increment_5d, "Default");
    if(Response_2D == nullptr){
        Crash_Report(args, "Rebuild_Matrix_5D returned ERROR");
    }
    args.timer.time_elapsed();
    TH1* Unfold_1D = Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, MC_BGS_1D, args);
    if(Unfold_1D == nullptr){
        Crash_Report(args, "Unfold_Function returned ERROR");
    }
    Unfold_1D->SetDirectory(0);
    delete Response_2D;
    detected.Histo_List.clear();
    std::cout << "\n" << Color::BGREEN << "Finished Unfolding" << Color::END << "\n" << std::endl;
    args.timer.time_elapsed();

    std::vector<std::pair<TH1*, std::string> > Histos_To_Slice = {
        {ExREAL_1D, "rdf"}, {MC_REC_1D, "mdf"}, {MC_GEN_1D, "gdf"}
    };
    if(MC_BGS_1D != nullptr){ Histos_To_Slice.push_back({MC_BGS_1D, "Background"}); }
    Histos_To_Slice.push_back({Unfold_1D, "Bayesian"});

    int to_be_saved_count = 0;
    TFile* output_file = nullptr;
    if(!args.test){
        std::cout << Color::BBLUE << "Saving to: " << Color::BGREEN << args.root << Color::END << std::endl;
        output_file = new TFile(args.root.c_str(), "UPDATE");
        TList File_Name_Tlist;
        File_Name_Tlist.SetOwner(kTRUE);
        File_Name_Tlist.SetName("Latest_List_of_File_Names");
        File_Name_Tlist.Add(new TObjString(args.single_file_input.c_str()));
        safe_write(&File_Name_Tlist, output_file);
        TList Config_Tlist;
        Config_Tlist.SetOwner(kTRUE);
        Config_Tlist.SetName("Detected_5D_Config");
        Config_Tlist.Add(new TObjString(("increment=" + std::to_string(args.increment_5d)).c_str()));
        Config_Tlist.Add(new TObjString(("num_bins=" + std::to_string(args.num_bins_5d)).c_str()));
        Config_Tlist.Add(new TObjString(("num_slices=" + std::to_string(args.num_slices_5d)).c_str()));
        safe_write(&Config_Tlist, output_file);
        if(ExREAL_1D_wExclusive_Background != nullptr){
            ExREAL_1D_wExclusive_Background->SetDirectory(0);
            safe_write(ExREAL_1D_wExclusive_Background, output_file);
            to_be_saved_count += 1;
        }
        try {
            safe_write(Unfold_1D, output_file);
            to_be_saved_count += 1;
        } catch(const std::exception& exc){
            std::cout << "\n" << Color::Error << "ERROR: Tried to save Unfold_1D\n" << Color::END << exc.what() << "\n";
        }
        int save_count_ref = to_be_saved_count;
        for(const auto& item : Histos_To_Slice){
            Run_Slice_Category(item.first, item.second, args, output_file, &save_count_ref, MC_BGS_1D, meta);
        }
        to_be_saved_count = save_count_ref;
        std::cout << "\n" << Color::BBLUE << "Done Saving..." << Color::END << "\n" << std::endl;
        output_file->Close();
        delete output_file;
    } else {
        std::cout << Color::PINK << "Would be saving to: " << Color::BCYAN << args.root << Color::END << std::endl;
        int save_count_ref = to_be_saved_count;
        for(const auto& item : Histos_To_Slice){
            Run_Slice_Category(item.first, item.second, args, nullptr, &save_count_ref, MC_BGS_1D, meta);
        }
        to_be_saved_count = save_count_ref;
    }
    input_file->Close();
    delete input_file;
    return to_be_saved_count;
}

int main_5D_recover_slices(UnfoldArgs& args, const SliceMetadata& meta){
    std::string smear_tag = ((args.smearing_options != "") && (args.smearing_options != "no_smear")) ? "Smear" : "''";
    std::string proper_name = std::string("(MultiDim_5D_Histo)_(Bayesian)_(SMEAR=") + smear_tag +
                              ")_(Q2_y_z_pT_Bin_All)_(MultiDim_Q2_y_z_pT_phi_h)";
    int to_be_saved_count = 0;
    TFile* output_file = nullptr;
    if(!args.test){
        std::cout << Color::BBLUE << "Recovering Bayesian slices into: " << Color::BGREEN << args.root << Color::END << std::endl;
        output_file = new TFile(args.root.c_str(), "UPDATE");
        if((output_file == nullptr) || output_file->IsZombie()){
            Crash_Report(args, "Could not open output ROOT file for recovery: " + args.root);
        }
    } else {
        std::cout << Color::PINK << "Would be recovering Bayesian slices into: " << Color::BCYAN << args.root << Color::END << std::endl;
        output_file = TFile::Open(args.root.c_str(), "READ");
        if((output_file == nullptr) || output_file->IsZombie()){
            Crash_Report(args, "Could not open output ROOT file for recovery (test mode): " + args.root);
        }
    }
    std::cout << "The total number of histograms in '" << Color::BBLUE << args.root << Color::END
              << "' is " << Color::BOLD << output_file->GetListOfKeys()->GetSize() << Color::END << std::endl;
    TH1* Unfold_1D = nullptr;
    if(key_in_file(output_file, proper_name)){
        std::cout << Color::BGREEN << "Found properly named Bayesian 1D histogram:\n\t" << Color::BBLUE
                  << proper_name << Color::END << std::endl;
        Unfold_1D = dynamic_cast<TH1*>(output_file->Get(proper_name.c_str()));
    } else if(key_in_file(output_file, "unfolded")){
        std::cout << Color::BYELLOW << "Found raw 'unfolded' histogram; renaming to proper MultiDim Bayesian name..." << Color::END << std::endl;
        Unfold_1D = dynamic_cast<TH1*>(output_file->Get("unfolded"));
        Unfold_1D->SetName(proper_name.c_str());
        if(!args.test){
            try {
                safe_write(Unfold_1D, output_file);
                to_be_saved_count += 1;
                std::cout << Color::BGREEN << "Resaved renamed Bayesian 1D histogram as:\n\t" << Color::BBLUE
                          << proper_name << Color::END << std::endl;
            } catch(const std::exception& exc){
                std::cout << "\n" << Color::Error << "ERROR: Tried to save renamed Unfold_1D\n" << Color::END << exc.what() << "\n";
            }
        } else {
            std::cout << Color::PINK << "Would have resaved renamed Bayesian 1D histogram as:\n\t" << Color::BCYAN
                      << proper_name << Color::END << std::endl;
            to_be_saved_count += 1;
        }
    } else {
        output_file->Close();
        delete output_file;
        Crash_Report(args, "Recovery mode could not find '" + proper_name + "' or 'unfolded' in " + args.root);
    }
    Unfold_1D->SetDirectory(0);
    args.timer.time_elapsed();
    int save_count_ref = to_be_saved_count;
    if(!args.test){
        Run_Slice_Category(Unfold_1D, "Bayesian", args, output_file, &save_count_ref, nullptr, meta);
        to_be_saved_count = save_count_ref;
        std::cout << "\n" << Color::BBLUE << "Done Saving Bayesian slices..." << Color::END << "\n" << std::endl;
        output_file->Close();
        delete output_file;
    } else {
        Run_Slice_Category(Unfold_1D, "Bayesian", args, nullptr, &save_count_ref, nullptr, meta);
        to_be_saved_count = save_count_ref;
        output_file->Close();
        delete output_file;
    }
    return to_be_saved_count;
}

} // namespace

int main(int argc, char** argv){
    TH1::AddDirectory(kFALSE);
    gROOT->SetBatch(kTRUE);
    gStyle->SetTitleOffset(1.3, "y");
    gStyle->SetGridColor(17);
    gStyle->SetPadGridX(1);
    gStyle->SetPadGridY(1);
    gStyle->SetStatX(0.80);
    gStyle->SetStatY(0.45);
    gStyle->SetStatW(0.3);
    gStyle->SetStatH(0.2);

    UnfoldArgs args = main_start(argc, argv);
    int to_be_saved_count = 0;
    try {
        SliceMetadata meta = Build_Multi5D_Slice_Metadata(args);
        if(args.recover_slices){
            to_be_saved_count = main_5D_recover_slices(args, meta);
        } else if(args.matrix_pdf){
            to_be_saved_count = main_5D_matrix_pdf(args);
        } else {
            to_be_saved_count = main_5D_unfold(args, meta);
        }
    } catch(const std::exception& exc){
        std::string mode_label = args.recover_slices ? "Bayesian Slice Recovery" : (args.matrix_pdf ? "Matrix PDF" : "5D Unfolding");
        Crash_Report(args, "The " + mode_label + " Code has CRASHED!\nERROR MESSAGE:\n\n" + exc.what());
    } catch(...){
        std::string mode_label = args.recover_slices ? "Bayesian Slice Recovery" : (args.matrix_pdf ? "Matrix PDF" : "5D Unfolding");
        Crash_Report(args, "The " + mode_label + " Code has CRASHED!\nERROR MESSAGE:\n\nunknown exception");
    }
    Construct_Email(args, false, false, to_be_saved_count);
    return 0;
}
