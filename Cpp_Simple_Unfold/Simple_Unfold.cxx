#include "Dedicated_5D_Unfold_Helpers.h"
#include "RecBinReduction.h"

#include <cmath>
#include <iostream>
#include <map>
#include <regex>
#include <tuple>
#include <utility>
#include <vector>

#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TH2D.h"
#include "TKey.h"
#include "TList.h"
#include "TObjString.h"
#include "TProfile.h"
#include "TROOT.h"
#include "TString.h"
#include "TStyle.h"
#include "TSystem.h"

#include "RooUnfoldResponse.h"
#include "RooUnfoldBayes.h"
#include "RooUnfold.h"
#if defined(__has_include)
#if __has_include("RooUnfoldParms.h")
#include "RooUnfoldParms.h"
#define SIDIS5D_HAS_ROOUNFOLD_PARMS 1
#endif
#endif

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
using sidis5d::Get_Num_of_z_pT_Bins_w_Migrations;
using sidis5d::skip_condition_z_pT_bins;
using sidis5d::RecSkipMap;
using sidis5d::Build_Rec_Skip_Map;
using sidis5d::Print_Rec_Skip_Map;
using sidis5d::Compress_TH1_Rec;
using sidis5d::Compress_TH2_Rec_Axis;
using sidis5d::Mask_Full_To_Analysis;

namespace {

const int kPhiN = 24;
const int kPhiMin = 0;
const int kPhiMax = 360;
const int kPhiStep = 15;

// const std::map<std::string, int> kBayesIter3D = {
//     {"1", 10}, {"2", 6}, {"3", 10}, {"4", 13}, {"5", 8}, {"6", 8}, {"7", 12}, {"8", 9},
//     {"9", 8}, {"10", 9}, {"11", 7}, {"12", 9}, {"13", 9}, {"14", 5}, {"15", 10}, {"16", 7}, {"17", 9}
// }; // Replaced 9/16/2026: acc=0.025 study; mean residual pathological for all 17; chi2-flatten fallback k=3
const std::map<std::string, int> kBayesIter3D = {
    {"1", 3}, {"2", 3}, {"3", 3}, {"4", 3}, {"5", 3}, {"6", 3}, {"7", 3}, {"8", 3},
    {"9", 3}, {"10", 3}, {"11", 3}, {"12", 3}, {"13", 3}, {"14", 3}, {"15", 3}, {"16", 3}, {"17", 3}
};

std::vector<TH1*> gIterationStudyHists;
int gCloneSerial = 0;

void Stash_Iteration_Study_Hist(TH1* h, const std::string& name){
    if(h == nullptr){ return; }
    h->SetName(name.c_str());
    h->SetDirectory(0);
    gIterationStudyHists.push_back(h);
}

void Write_Iteration_Study_Hists(TFile* output_file, int* save_count_ref){
    if(output_file == nullptr){ return; }
    for(TH1* h : gIterationStudyHists){
        if(h == nullptr){ continue; }
        safe_write(h, output_file);
        if(save_count_ref != nullptr){ *save_count_ref += 1; }
    }
}

void Log_Root_And_Matrix_Linkage(){
    const char* rootsys = gSystem->Getenv("ROOTSYS");
    std::cout << Color::BOLD << "ROOT version: " << gROOT->GetVersion()
              << Color::END << "  ROOTSYS=" << ((rootsys != nullptr) ? rootsys : "(unset)") << std::endl;
    TString libm = gSystem->DynamicPathName("libMatrix");
    std::cout << "libMatrix: " << (libm.Length() ? libm.Data() : "(not found)") << std::endl;
}

RooUnfold::ErrorTreatment ErrorTreatmentFromMode(const std::string& mode){
    if(mode == "covariance"){ return RooUnfold::kCovariance; }
    if(mode == "errors"){ return RooUnfold::kErrors; }
    if(mode == "none"){ return RooUnfold::kNoError; }
    return RooUnfold::kCovToys;
}

TH1* CloneDetached(TH1* src, const std::string& tag){
    if(src == nullptr){ return nullptr; }
    std::string name = std::string(src->GetName()) + "_" + tag + "_" + std::to_string(++gCloneSerial);
    TH1* out = dynamic_cast<TH1*>(src->Clone(name.c_str()));
    if(out != nullptr){ out->SetDirectory(0); }
    return out;
}

TH2* CloneDetachedTH2(TH2* src, const std::string& tag){
    return dynamic_cast<TH2*>(CloneDetached(src, tag));
}

bool ArgWasPassed(int argc, char** argv, const std::vector<std::string>& names){
    for(int i = 1; i < argc; ++i){
        std::string arg = argv[i];
        for(const auto& name : names){
            if(arg == name){ return true; }
            if((arg.size() > name.size()) && (arg.compare(0, name.size(), name) == 0) && (arg[name.size()] == '=')){ return true; }
        }
    }
    return false;
}

int Extract_Q2y(const std::string& name){
    if(contains(name, "Q2-y-Bin=All") || contains(name, "Q2-xB-Bin=All")){ return 0; }
    std::smatch match;
    std::regex re(R"(Q2-(?:y|xB)-Bin=(-?\d+),)");
    if(std::regex_search(name, match, re) && (match.size() > 1)){
        return std::atoi(match[1].str().c_str());
    }
    return -1;
}

bool Passes_Weighed_Filter(const std::string& name, const UnfoldArgs& args){
    const std::vector<std::string> known_tags = {"_(Acc)", "_(JSON)", "_(Spline)", "_(AccJSON)", "_(AccSpline)", "_(Weighed)"};
    bool has_weight_tag = false;
    for(const auto& tag_str : known_tags){
        if(contains(name, tag_str)){ has_weight_tag = true; break; }
    }
    if(!args.weight_tag.empty()){
        return contains(name, "_(" + args.weight_tag + ")");
    }
    if(args.require_weighed){ return has_weight_tag; }
    return !has_weight_tag;
}

std::string Apply_Matrix_1D_Replacements(std::string name){
    name = replace_all(name, "'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'");
    name = replace_all(name, "'Response_Matrix'", "'Response_Matrix_1D'");
    return name;
}

std::string Apply_Background_1D_Replacements(std::string name){
    name = replace_all(name, "'Response_Matrix_1D'", "'Background_Response_Matrix_1D'");
    name = replace_all(name, "'Response_Matrix_Normal_1D'", "'Background_Response_Matrix_1D'");
    return name;
}

std::string Strip_Weight_Tags(std::string name){
    for(const char* tag_str : {"_(AccSpline)", "_(AccJSON)", "_(Spline)", "_(JSON)", "_(Acc)", "_(Weighed)"}){
        name = replace_all(name, tag_str, "");
    }
    return name;
}

std::string Strip_Smear_Tags(std::string name){
    name = replace_all(name, "_smeared", "");
    name = replace_all(name, "smear_", "");
    name = replace_all(name, "smear", "");
    return name;
}

std::string Prepare_Gdf_Name(std::string name, const UnfoldArgs& args){
    name = replace_all(name, "(Data-Type='mdf')", "(Data-Type='gdf')");
    const std::string& weight_tag = args.weight_tag;
    if((weight_tag == "Acc") || (weight_tag == "AccJSON") || (weight_tag == "AccSpline") || weight_tag.empty()){
        name = Strip_Weight_Tags(name);
        if(weight_tag == "AccJSON"){ name += "_(JSON)"; }
        else if(weight_tag == "AccSpline"){ name += "_(Spline)"; }
    }
    name = replace_all(name, "cut_Complete_EDIS", "no_cut");
    for(int sector_cut_remove = 1; sector_cut_remove <= 6; ++sector_cut_remove){
        name = replace_all(name, "cut_Complete_SIDIS_eS" + std::to_string(sector_cut_remove) + "o", "no_cut");
    }
    name = replace_all(name, "cut_Complete_SIDIS_Proton", "no_cut");
    name = replace_all(name, "cut_Complete_SIDIS", "no_cut");
    name = replace_all(name, "cut_Complete", "no_cut");
    name = Strip_Smear_Tags(name);
    return Apply_Matrix_1D_Replacements(name);
}

std::string Prepare_Rdf_Name(std::string name, const UnfoldArgs& args){
    name = replace_all(name, "(Data-Type='mdf')", args.sim ? "(Data-Type='mdf')" : "(Data-Type='rdf')");
    name = Strip_Weight_Tags(name);
    if(!args.sim){ name = Strip_Smear_Tags(name); }
    return Apply_Matrix_1D_Replacements(name);
}

bool Is_Simple_Matrix_Candidate(const std::string& name, const UnfoldArgs& args){
    if(!contains(name, "(Data-Type='mdf')")){ return false; }
    if(!contains(name, "Response_Matrix_Normal")){ return false; }
    if(contains(name, "Response_Matrix_Normal_1D")){ return false; }
    if(contains(name, "5D_Response")){ return false; }
    if(contains(name, "Background")){ return false; }
    if(contains(name, "no_cut")){ return false; }
    if(contains(name, "cut_Complete_EDIS")){ return false; }
    if(!contains(name, "cut_Complete_SIDIS")){ return false; }
    if(contains(name, "cut_Complete_SIDIS_eS")){ return false; }
    if(contains(name, "no_cut_eS")){ return false; }
    if(contains(name, "_Proton")){ return false; }
    if(contains(name, "Multi_Dim_")){ return false; }
    if(!contains(name, "phi_t")){ return false; }
    if(contains(name, "_(lundvpk)") || contains(name, "_(lundrho)")){ return false; }
    const bool want_3d = args.unfolding_3D && (!args.unfolding_1D);
    const bool want_1d = args.unfolding_1D && (!args.unfolding_3D);
    if(want_3d){
        if(!contains(name, "Multi")){ return false; }
        if(!contains(name, "MultiDim_z_pT_Bin")){ return false; }
    }
    if(want_1d){
        if(contains(name, "Multi")){ return false; }
    }
    if((args.smearing_options != "no_smear") && (args.smearing_options != "both") && contains(name, "(Smear-Type='')")){ return false; }
    if((args.smearing_options != "smear") && (args.smearing_options != "both") && contains(name, "(Smear-Type='smear')")){ return false; }
    if(!Passes_Weighed_Filter(name, args)){ return false; }
    int q2y = Extract_Q2y(name);
    if(q2y < 0){ return false; }
    bool in_list = false;
    for(const auto& b : args.Q2_y_Bin_List){
        if(b == std::to_string(q2y)){ in_list = true; break; }
    }
    if(!in_list){ return false; }
    return true;
}

int Convert_Dense_3D_Start(int q2y, int zpt){
    if((q2y < 1) || (zpt < 1)){ return -1; }
    int last = std::get<1>(Get_Num_of_z_pT_Bins_w_Migrations(q2y));
    int slot = 1;
    for(int z = 1; z <= last; ++z){
        if(skip_condition_z_pT_bins(q2y, z)){ continue; }
        if(z == zpt){ return slot; }
        slot += kPhiN;
    }
    return -1;
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

int Default_Bayes_Iterations(const std::string& name_main, int q2y, bool user_set_bi, int user_bi){
    if(user_set_bi){ return user_bi; }
    int bayes_iterations = 10;
    if(contains(name_main, "MultiDim_Q2_y_z_pT_phi_h")){ bayes_iterations = 4; }
    auto it = kBayesIter3D.find(std::to_string(q2y));
    int table = (it == kBayesIter3D.end()) ? (bayes_iterations + 2) : it->second;
    // return table + 1; // Removed +1 offset 9/16/2026; stored k is the k used
    return table;
}

TH1* Unfold_Function(TH2* Response_2D, TH1* ExREAL_1D, TH1* MC_REC_1D, TH1* MC_GEN_1D, TH1* MC_BGS_1D,
                     UnfoldArgs& args, bool user_set_bi, const std::string& study_tag, RecSkipMap* skip_map_out){
    std::cout << Color::BCYAN << "Starting " << Color::UNDERLINE << Color::GREEN << "RooUnfold" << Color::END_B
              << Color::CYAN << " Unfolding Procedure..." << Color::END << std::endl;
    std::string Name_Main = Response_2D->GetName();
    std::string Name_Main_Print = Name_Main;
    auto nb_pos = Name_Main.find("-[NumBins");
    if(nb_pos != std::string::npos){
        Name_Main_Print = Name_Main.substr(0, nb_pos) + "))";
    }
    std::string clean_name = replace_all(Name_Main_Print, "(Data-Type='mdf'), ", "");
    std::cout << "\t" << Color::BOLD << "Unfolding Histogram:" << Color::END << "\n\t" << clean_name << std::endl;

    RecSkipMap skip_map;
    TH1* ExREAL_use = ExREAL_1D;
    TH1* MC_REC_use = MC_REC_1D;
    TH1* MC_BGS_use = MC_BGS_1D;
    bool own_rec = false;
    if(!args.old_binning){
        skip_map = Build_Rec_Skip_Map(ExREAL_1D, MC_REC_1D, MC_GEN_1D, MC_BGS_1D, args.Min_Allowed_Acceptance_Cut);
        Print_Rec_Skip_Map(skip_map);
        if(skip_map_out != nullptr){ *skip_map_out = skip_map; }
        ExREAL_use = Compress_TH1_Rec(ExREAL_1D, skip_map, std::string(ExREAL_1D->GetName()) + "_rec_reduced");
        MC_REC_use = Compress_TH1_Rec(MC_REC_1D, skip_map, std::string(MC_REC_1D->GetName()) + "_rec_reduced");
        if(MC_BGS_1D != nullptr){
            MC_BGS_use = Compress_TH1_Rec(MC_BGS_1D, skip_map, std::string(MC_BGS_1D->GetName()) + "_rec_reduced");
        }
        own_rec = true;
    }

    int nBins_rec = ExREAL_use->GetNbinsX();
    int nBins_gen = MC_GEN_1D->GetNbinsX();
    double rec_width = ExREAL_use->GetBinWidth(1);
    double rec_min = ExREAL_use->GetBinCenter(0) + 0.5 * rec_width;
    double rec_max = ExREAL_use->GetBinCenter(nBins_rec) + 0.5 * rec_width;
    double gen_width = MC_GEN_1D->GetBinWidth(1);
    double gen_min = MC_GEN_1D->GetBinCenter(0) + 0.5 * gen_width;
    double gen_max = MC_GEN_1D->GetBinCenter(nBins_gen) + 0.5 * gen_width;

    TH2* Response_2D_Input = Response_2D;
    std::string Response_2D_Input_Title = std::string(Response_2D->GetTitle()) + ";" +
                                          Response_2D->GetXaxis()->GetTitle() + ";" +
                                          Response_2D->GetYaxis()->GetTitle();
    const bool is_5d = contains(Name_Main, "MultiDim_Q2_y_z_pT_phi_h");
    if(!is_5d){
        Response_2D_Input_Title = std::string(Response_2D->GetTitle()) + ";" +
                                  Response_2D->GetYaxis()->GetTitle() + ";" +
                                  Response_2D->GetXaxis()->GetTitle();
        TH2D* flipped = new TH2D((std::string(Response_2D->GetName()) + "_Flipped").c_str(),
                                 Response_2D_Input_Title.c_str(),
                                 Response_2D->GetNbinsY(), rec_min, rec_max,
                                 Response_2D->GetNbinsX(), gen_min, gen_max);
        flipped->SetDirectory(0);
        for(int gen_bin = 0; gen_bin <= nBins_gen; ++gen_bin){
            for(int rec_bin = 0; rec_bin <= Response_2D->GetNbinsY(); ++rec_bin){
                flipped->SetBinContent(rec_bin, gen_bin, Response_2D->GetBinContent(gen_bin, rec_bin));
                flipped->SetBinError(rec_bin, gen_bin, Response_2D->GetBinError(gen_bin, rec_bin));
            }
        }
        Response_2D_Input = flipped;
    }
    if(!args.old_binning){
        TH2D* compressed = Compress_TH2_Rec_Axis(Response_2D_Input, skip_map, true,
                                                 std::string(Response_2D_Input->GetName()) + "_rec_reduced");
        if(Response_2D_Input != Response_2D){ delete Response_2D_Input; }
        Response_2D_Input = compressed;
    }

    if(!((nBins_rec == MC_REC_use->GetNbinsX()) &&
         (nBins_gen == MC_GEN_1D->GetNbinsX()) &&
         (nBins_rec == Response_2D_Input->GetNbinsX()) &&
         (nBins_gen == Response_2D_Input->GetNbinsY()))){
        std::cout << Color::RED << "Unequal Bins..." << Color::END << std::endl;
        std::cout << "nBins_rec = " << nBins_rec << " nBins_gen = " << nBins_gen << std::endl;
        std::cout << "Response nx,ny = " << Response_2D_Input->GetNbinsX() << "," << Response_2D_Input->GetNbinsY() << std::endl;
        if(Response_2D_Input != Response_2D){ delete Response_2D_Input; }
        delete Response_2D;
        if(own_rec){
            delete ExREAL_use;
            delete MC_REC_use;
            if((MC_BGS_use != nullptr) && (MC_BGS_use != MC_BGS_1D)){ delete MC_BGS_use; }
        }
        return nullptr;
    }

    std::string resp_name = replace_all(Response_2D_Input->GetName(), "_Flipped", "") + "_RooUnfoldResponse_Object";
    RooUnfoldResponse Response_RooUnfold(MC_REC_use, MC_GEN_1D, Response_2D_Input, resp_name.c_str(), Response_2D_Input_Title.c_str());
    if(Response_2D_Input != Response_2D){ delete Response_2D_Input; }
    delete Response_2D;
    if(MC_BGS_use != nullptr){
        for(int rec_bin = 1; rec_bin <= MC_BGS_use->GetNbinsX(); ++rec_bin){
            Response_RooUnfold.Fake(MC_BGS_use->GetBinCenter(rec_bin), MC_BGS_use->GetBinContent(rec_bin));
        }
    }

    int q2y = Extract_Q2y(Name_Main);
    int bayes_iterations = Default_Bayes_Iterations(Name_Main, q2y, user_set_bi, args.bayes_iterations);
    args.bayes_iterations = bayes_iterations;
    std::cout << "\t" << Color::CYAN << "Using " << Color::BGREEN << "RooUnfold (Bayesian)" << Color::END_C
              << " method to unfold..." << Color::END << std::endl;
    std::cout << "\tError mode: " << args.error_mode << std::endl;
    std::cout << Color::BOLD << "Performing Unfolding with " << Color::UNDERLINE << bayes_iterations
              << Color::END_B << " iteration(s)..." << Color::END << std::endl;

    RooUnfold::ErrorTreatment err_treat = ErrorTreatmentFromMode(args.error_mode);
    RooUnfoldBayes Unfolding_Histo(&Response_RooUnfold, ExREAL_use, bayes_iterations);
    Unfolding_Histo.SetVerbose(1);
    if(args.error_mode == "toys"){ Unfolding_Histo.SetNToys(args.Num_Toys); }

#ifdef SIDIS5D_HAS_ROOUNFOLD_PARMS
    if(args.iteration_study){
        std::cout << Color::BBLUE << "Running RooUnfoldParms iteration study (" << args.error_mode << ")..." << Color::END << std::endl;
        RooUnfoldParms parms(&Unfolding_Histo, err_treat, MC_GEN_1D);
        if(args.has_parm_min){ parms.SetMinParm(args.parm_min); }
        if(args.has_parm_max){ parms.SetMaxParm(args.parm_max); }
        if(args.has_parm_step){ parms.SetStepSizeParm(args.parm_step); }
        Stash_Iteration_Study_Hist(parms.GetChi2(), "Iteration_Study_Chi2" + study_tag);
        Stash_Iteration_Study_Hist(parms.GetRMSError(), "Iteration_Study_RMSError" + study_tag);
        Stash_Iteration_Study_Hist(parms.GetMeanResiduals(), "Iteration_Study_MeanResiduals" + study_tag);
        Stash_Iteration_Study_Hist(parms.GetRMSResiduals(), "Iteration_Study_RMSResiduals" + study_tag);
    }
#else
    if(args.iteration_study){
        Crash_Report(args, "RooUnfoldParms.h was not found in this RooUnfold install; cannot run --iteration_study.");
    }
#endif

    // TH1* Unfolded_Histo = Unfolding_Histo.Hunfold(RooUnfold::kCovToys); // Changed to err_treat on 9/16/2026
    TH1* Unfolded_Histo = Unfolding_Histo.Hunfold(err_treat);
    if(Unfolded_Histo == nullptr){
        std::cout << "\n" << Color::Error << "FAILED TO UNFOLD A HISTOGRAM (RooUnfold)..." << Color::END << std::endl;
        return nullptr;
    }
    Unfolded_Histo->SetDirectory(0);
    if(args.old_binning){
        for(int bin_rec = 0; bin_rec <= MC_REC_1D->GetNbinsX(); ++bin_rec){
            if(MC_REC_1D->GetBinContent(bin_rec) == 0){
                Unfolded_Histo->SetBinError(bin_rec, Unfolded_Histo->GetBinContent(bin_rec) + Unfolded_Histo->GetBinError(bin_rec));
            }
        }
        if(!args.no_post_unfold_acc_cut){
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
        }
    }
    if(own_rec){
        delete ExREAL_use;
        delete MC_REC_use;
        if((MC_BGS_use != nullptr) && (MC_BGS_use != MC_BGS_1D)){ delete MC_BGS_use; }
    }
    std::string title = replace_all(replace_all(ExREAL_1D->GetTitle(), "Experimental", "RooUnfold (Bayesian)"),
                                    "Cut: Complete Set of SIDIS Cuts", "");
    Unfolded_Histo->SetTitle(replace_all(title, "Cut:  Complete Set of SIDIS Cuts", "").c_str());
    std::string xtitle = replace_all(ExREAL_1D->GetXaxis()->GetTitle(), "(REC)",
                                     (contains(Name_Main, "smeared") || contains(Name_Main, "smear")) ? "(Smeared)" : "");
    Unfolded_Histo->GetXaxis()->SetTitle(xtitle.c_str());
    std::cout << Color::BCYAN << "Finished " << Color::GREEN << "RooUnfold (Bayesian)" << Color::END_B
              << Color::CYAN << " Unfolding Procedure.\n" << Color::END << std::endl;
    return Unfolded_Histo;
}

void Color_Slice(TH1* hist, const std::string& Method){
    int col = RootColor::Black;
    if((Method == "rdf") || (Method == "Experimental")){ col = RootColor::Blue; }
    if((Method == "mdf") || (Method == "MC REC")){ col = RootColor::Red; }
    if((Method == "gdf") || (Method == "gen") || (Method == "MC GEN")){ col = RootColor::Green; }
    if((Method == "tdf") || (Method == "true")){ col = RootColor::Cyan; }
    if((Method == "bbb") || (Method == "Bin") || (Method == "Bin-by-Bin")){ col = RootColor::Brown; }
    if((Method == "bayes") || (Method == "bayesian") || (Method == "Bayesian")){ col = RootColor::Teal; }
    hist->SetLineColor(col);
    hist->SetMarkerColor(col);
    double ymax = hist->GetBinContent(hist->GetMaximumBin());
    hist->GetYaxis()->SetRangeUser(0, (ymax > 0) ? 1.5 * ymax : 1.0);
}

int Multi3D_Slice(TH1* Histo, TH1* Histo_Cut, const std::string& Name_In, const std::string& Method,
                  const std::string& Smear_In, const std::string& Q2_y_Bin_Select, UnfoldArgs& args,
                  TFile* output_file, int* save_count_ref){
    if(Histo == nullptr){ return -1; }
    std::string Name = Name_In;
    std::string Smear = Smear_In;
    std::string Variable = "MultiDim_z_pT_Bin_Y_bin_phi_t";
    if((Method == "rdf") || (Method == "Experimental") || (Method == "gdf") || (Method == "gen") ||
       (Method == "MC GEN") || (Method == "tdf") || (Method == "true")){
        if(!args.sim || (Method != "rdf" && Method != "Experimental")){
            if((Method != "mdf") && (Method != "MC REC") && (Method != "Bayesian") && (Method != "bayes") &&
               (Method != "Bin") && (Method != "Acceptance") && (Method != "Background")){
                Variable = replace_all(Variable, "_smeared", "");
                Smear = "";
            }
        }
        if(!args.sim && ((Method == "rdf") || (Method == "Experimental"))){
            Variable = replace_all(Variable, "_smeared", "");
            Smear = "";
        }
        if((Method == "gdf") || (Method == "gen") || (Method == "MC GEN") || (Method == "tdf") || (Method == "true")){
            Variable = replace_all(Variable, "_smeared", "");
            Smear = "";
        }
    }
    if(contains(Smear, "mear") && (!contains(Variable, "_smeared"))){ Variable += "_smeared"; }
    Name = Histogram_Name_Def(Name, "MultiDim_3D_Histo", Method, "Skip", Smear, Q2_y_Bin_Select,
                              "MultiDim_3D_z_pT_Bin_Info", "Default", "Default", args);
    int q2y = std::atoi(Q2_y_Bin_Select.c_str());
    int z_pT_Range = std::get<1>(Get_Num_of_z_pT_Bins_w_Migrations(q2y));
    TH1D* Name_All_Hist = nullptr;
    std::string Name_All;
    for(int z_pT = 0; z_pT <= z_pT_Range; ++z_pT){
        std::string zlab = ((z_pT == 0) ? "All" : std::to_string(z_pT));
        std::string Name_Out = replace_all(Name, "MultiDim_3D_z_pT_Bin_Info", zlab);
        std::string Bin_Title = std::string(RootColor::Bold) + "{#scale[1.25]{#color[" + std::to_string(RootColor::Red) +
                                "]{Q^{2}-y Bin: " + Q2_y_Bin_Select + "} #topbar #color[" + std::to_string(RootColor::Red) +
                                "]{z-P_{T} Bin: " + zlab + "}}}";
        std::string Title_Out = std::string("#splitline{") + RootColor::Bold + "{3-Dimensional Plot of" +
                                (contains(Smear, "mear") ? " (Smeared)" : "") + " #phi_{h}}{" + Bin_Title + "}";
        std::string xtitle = (contains(Smear, "mear") ? "(Smeared) " : "") + std::string("#phi_{h} [") + RootColor::Degrees + "]";
        if(z_pT == 0){
            Name_All = Name_Out;
            Name_All_Hist = new TH1D(Name_All.c_str(), (Title_Out + "; " + xtitle).c_str(), kPhiN, kPhiMin, kPhiMax);
            Name_All_Hist->SetDirectory(0);
            continue;
        }
        int Start_phi_h_bin = Convert_Dense_3D_Start(q2y, z_pT);
        if(Start_phi_h_bin < 0){ continue; }
        int End_phi_h_bin = Convert_Dense_3D_Start(q2y, z_pT + 1);
        if(End_phi_h_bin < 0){ End_phi_h_bin = Start_phi_h_bin + kPhiN; }
        if((End_phi_h_bin - Start_phi_h_bin) != kPhiN){ continue; }
        TH1D* Slice_Hist = new TH1D(Name_Out.c_str(), (Title_Out + "; " + xtitle).c_str(), kPhiN, kPhiMin, kPhiMax);
        Slice_Hist->SetDirectory(0);
        int ii_bin_num = Start_phi_h_bin;
        while(ii_bin_num < End_phi_h_bin){
            for(int phi_bin = kPhiMin; phi_bin < kPhiMax; phi_bin += kPhiStep){
                double center = phi_bin + 0.5 * kPhiStep;
                int bin_ii = Histo->FindBin(ii_bin_num);
                double content = 0.0;
                double err2 = 0.0;
                bool skip = false;
                if(Histo_Cut != nullptr){
                    double cut_num = Histo_Cut->GetBinContent(bin_ii);
                    double cut_err = Histo_Cut->GetBinError(bin_ii);
                    if((cut_num == 0) || (cut_num <= cut_err)){ skip = true; }
                }
                if(!skip){
                    content = Histo->GetBinContent(bin_ii);
                    double e = Histo->GetBinError(bin_ii);
                    err2 = e * e;
                }
                int out_bin = Slice_Hist->FindBin(center);
                Slice_Hist->SetBinContent(out_bin, Slice_Hist->GetBinContent(out_bin) + content);
                Slice_Hist->SetBinError(out_bin, std::sqrt(Slice_Hist->GetBinError(out_bin) * Slice_Hist->GetBinError(out_bin) + err2));
                if(Name_All_Hist != nullptr){
                    int all_bin = Name_All_Hist->FindBin(center);
                    Name_All_Hist->SetBinContent(all_bin, Name_All_Hist->GetBinContent(all_bin) + content);
                    double cur = Name_All_Hist->GetBinError(all_bin);
                    Name_All_Hist->SetBinError(all_bin, std::sqrt(cur * cur + err2));
                }
                ++ii_bin_num;
            }
        }
        Color_Slice(Slice_Hist, Method);
        if((output_file != nullptr) && (!args.test)){
            safe_write(Slice_Hist, output_file);
            if(save_count_ref != nullptr){ *save_count_ref += 1; }
        } else if(args.verbose){
            std::cout << Color::PINK << "Would save slice " << Name_Out << Color::END << std::endl;
            if(save_count_ref != nullptr){ *save_count_ref += 1; }
        }
        delete Slice_Hist;
    }
    if(Name_All_Hist != nullptr){
        Color_Slice(Name_All_Hist, Method);
        if((output_file != nullptr) && (!args.test)){
            safe_write(Name_All_Hist, output_file);
            if(save_count_ref != nullptr){ *save_count_ref += 1; }
        } else if(args.verbose){
            std::cout << Color::PINK << "Would save slice " << Name_All << Color::END << std::endl;
            if(save_count_ref != nullptr){ *save_count_ref += 1; }
        }
        delete Name_All_Hist;
    }
    return 0;
}

UnfoldArgs main_start(int argc, char** argv){
    UnfoldArgs args = sidis5d::parse_args(argc, argv);
    args.timer.start();
    Log_Root_And_Matrix_Linkage();
    args.smearing_options = args.no_smear ? "no_smear" : "smear";
    args.Q2_y_Bin_List = args.bins;
    // bool has_zero = false;
    // for(const auto& b : args.Q2_y_Bin_List){ if(b == "0"){ has_zero = true; } }
    // if(!has_zero){ args.Q2_y_Bin_List.push_back("0"); }
    if((!args.weight_tag.empty()) && (!contains(args.root, "_W" + args.weight_tag))){
        args.root = replace_all(args.root, ".root", "_W" + args.weight_tag + ".root");
    }
    if(!args.test){
        std::cout << "\n" << Color::BBLUE << "Will be saving results to " << Color::END_B << args.root << Color::END << "\n" << std::endl;
    } else {
        std::cout << "\n" << Color::RED << "Will " << Color::Error << "NOT" << Color::END_R
                  << " be saving results (running as a test)\n" << Color::END << std::endl;
    }
    std::cout << "\n" << Color::BOLD << "Starting Simple 3D/1D Unfolding Analysis\n" << Color::END << std::endl;
    return args;
}

int Unfold_One_Matrix(TFile* input_file, const std::string& out_print_main, UnfoldArgs& args,
                      bool user_set_bi, TFile* output_file, int* save_count_ref){
    std::string mdf_1d = Apply_Matrix_1D_Replacements(out_print_main);
    std::string rdf_name = Prepare_Rdf_Name(out_print_main, args);
    std::string gdf_name = Prepare_Gdf_Name(out_print_main, args);
    if(args.sim){ rdf_name = mdf_1d; }
    if(!key_in_file(input_file, out_print_main)){
        Crash_Report(args, "Missing response matrix: " + out_print_main);
    }
    if(!key_in_file(input_file, mdf_1d)){
        Crash_Report(args, "Missing mdf 1D histogram: " + mdf_1d);
    }
    if(!key_in_file(input_file, rdf_name)){
        Crash_Report(args, "Missing rdf 1D histogram: " + rdf_name);
    }
    if(!key_in_file(input_file, gdf_name)){
        Crash_Report(args, "Missing gdf 1D histogram: " + gdf_name);
    }
    TH2* Response_2D = CloneDetachedTH2(dynamic_cast<TH2*>(input_file->Get(out_print_main.c_str())), "resp");
    TH1* ExREAL_1D = CloneDetached(dynamic_cast<TH1*>(input_file->Get(rdf_name.c_str())), "rdf");
    TH1* MC_REC_1D = CloneDetached(dynamic_cast<TH1*>(input_file->Get(mdf_1d.c_str())), "mdf");
    TH1* MC_GEN_1D = CloneDetached(dynamic_cast<TH1*>(input_file->Get(gdf_name.c_str())), "gdf");
    if((Response_2D == nullptr) || (ExREAL_1D == nullptr) || (MC_REC_1D == nullptr) || (MC_GEN_1D == nullptr)){
        Crash_Report(args, "Failed to load histograms for " + out_print_main);
    }
    std::string bdf_1d = Apply_Background_1D_Replacements(mdf_1d);
    TH1* MC_BGS_1D = nullptr;
    if(key_in_file(input_file, bdf_1d) && contains(bdf_1d, "Background")){
        MC_BGS_1D = CloneDetached(dynamic_cast<TH1*>(input_file->Get(bdf_1d.c_str())), "bgs");
    } else {
        Crash_Report(args, "Missing Background Histogram (would be named: " + bdf_1d + ")");
    }
    if(args.sim && (MC_BGS_1D != nullptr)){ ExREAL_1D->Add(MC_BGS_1D); }
    TH1* ExREAL_1D_wExclusive_Background = nullptr;
    std::string rho_rdf = rdf_name + "_(" + args.background_source + ")";
    std::string rho_mdf = mdf_1d + "_(" + args.background_source + ")";
    if(key_in_file(input_file, rho_rdf) || key_in_file(input_file, rho_mdf)){
        std::string rho_key = key_in_file(input_file, rho_rdf) ? rho_rdf : rho_mdf;
        std::cout << Color::BGREEN << "Subtracting the '" << args.background_source << "' files to the 'ExREAL_1D' histogram" << Color::END << std::endl;
        TH1* Lundrho = dynamic_cast<TH1*>(input_file->Get(rho_key.c_str()));
        auto sub = subtract_bkg_with_zero_floor(ExREAL_1D, Lundrho);
        ExREAL_1D_wExclusive_Background = sub.first;
        delete ExREAL_1D;
        ExREAL_1D = sub.second;
    } else if(args.background_source != "None"){
        std::cout << Color::Error << "Cannot subtract the '" << args.background_source
                  << "' files to the 'ExREAL_1D' histogram" << Color::END << std::endl;
    }

    int q2y = Extract_Q2y(out_print_main);
    std::string smear_tag = contains(to_lower_copy(out_print_main), "smear") ? "_Smear" : "_NoSmear";
    std::string study_tag = "_Q2y_" + std::to_string(q2y) + smear_tag;
    std::cout << "\n" << Color::BGREEN << "Unfolding: " << out_print_main << Color::END << "\n" << std::endl;
    RecSkipMap skip_map;
    TH1* Unfold_raw = Unfold_Function(Response_2D, ExREAL_1D, MC_REC_1D, MC_GEN_1D, MC_BGS_1D, args, user_set_bi, study_tag, &skip_map);
    if(Unfold_raw == nullptr){ Crash_Report(args, "Unfold_Function returned ERROR"); }
    TH1* Unfold_1D = Unfold_raw;
    if(!args.old_binning){
        Unfold_1D = Mask_Full_To_Analysis(Unfold_raw, skip_map, std::string(Unfold_raw->GetName()) + "_analysis");
        delete Unfold_raw;
    }

    std::string Smear_Input = contains(to_lower_copy(out_print_main), "smear") ? "Smear" : "";
    std::string Histo_Name_General = Histogram_Name_Def(out_print_main, "1D", "METHOD", "Skip", Smear_Input,
                                                        std::to_string(q2y), "0", "Default", "Default", args);
    auto save_named = [&](TH1* h, const std::string& method){
        if(h == nullptr){ return; }
        std::string nm = replace_all(Histo_Name_General, "METHOD", method);
        if((method == "rdf") || (method == "gdf")){ nm = replace_all(nm, "Smear", "''"); }
        h->SetName(nm.c_str());
        if((output_file != nullptr) && (!args.test)){
            safe_write(h, output_file);
            if(save_count_ref != nullptr){ *save_count_ref += 1; }
        }
    };
    if(ExREAL_1D_wExclusive_Background != nullptr){ save_named(ExREAL_1D_wExclusive_Background, "rdf_wExclusive_Background"); }
    save_named(ExREAL_1D, "rdf");
    save_named(MC_REC_1D, "mdf");
    save_named(MC_GEN_1D, "gdf");
    if(MC_BGS_1D != nullptr){ save_named(MC_BGS_1D, "Background"); }
    save_named(Unfold_1D, "Bayesian");

    if(contains(out_print_main, "MultiDim_z_pT_Bin") && (q2y > 0)){
        std::string q2y_s = std::to_string(q2y);
        Multi3D_Slice(ExREAL_1D, nullptr, out_print_main, "rdf", args.sim ? Smear_Input : "", q2y_s, args, output_file, save_count_ref);
        Multi3D_Slice(MC_REC_1D, nullptr, out_print_main, "mdf", Smear_Input, q2y_s, args, output_file, save_count_ref);
        Multi3D_Slice(MC_GEN_1D, nullptr, out_print_main, "gdf", "", q2y_s, args, output_file, save_count_ref);
        if(MC_BGS_1D != nullptr){
            Multi3D_Slice(MC_BGS_1D, nullptr, out_print_main, "Background", Smear_Input, q2y_s, args, output_file, save_count_ref);
        }
        Multi3D_Slice(Unfold_1D, MC_REC_1D, out_print_main, "Bayesian", Smear_Input, q2y_s, args, output_file, save_count_ref);
    }
    delete ExREAL_1D;
    delete MC_REC_1D;
    delete MC_GEN_1D;
    delete MC_BGS_1D;
    delete Unfold_1D;
    delete ExREAL_1D_wExclusive_Background;
    return 0;
}

int main_simple_unfold(UnfoldArgs& args, bool user_set_bi){
    TFile* input_file = TFile::Open(args.single_file_input.c_str(), "READ");
    if((input_file == nullptr) || input_file->IsZombie()){
        Crash_Report(args, "Could not open input ROOT file: " + args.single_file_input);
    }
    std::cout << "The total number of histograms in '" << Color::BBLUE << args.single_file_input << Color::END
              << "' is " << Color::BOLD << input_file->GetListOfKeys()->GetSize() << Color::END << std::endl;
    std::vector<std::string> matrices;
    TIter next(input_file->GetListOfKeys());
    while(TKey* key = dynamic_cast<TKey*>(next())){
        std::string name = key->GetName();
        if(Is_Simple_Matrix_Candidate(name, args)){ matrices.push_back(name); }
    }
    if(matrices.empty()){
        Crash_Report(args, "No matching 3D/1D Response_Matrix_Normal entries found in the input file.");
    }
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
        Config_Tlist.SetName("Simple_Unfold_Config");
        Config_Tlist.Add(new TObjString(("error_mode=" + args.error_mode).c_str()));
        Config_Tlist.Add(new TObjString(("bayes_iterations=" + std::to_string(args.bayes_iterations)).c_str()));
        Config_Tlist.Add(new TObjString(args.unfolding_3D ? "unfolding_3D=1" : "unfolding_3D=0"));
        Config_Tlist.Add(new TObjString(args.unfolding_1D ? "unfolding_1D=1" : "unfolding_1D=0"));
        safe_write(&Config_Tlist, output_file);
    } else {
        std::cout << Color::PINK << "Would be saving to: " << Color::BCYAN << args.root << Color::END << std::endl;
    }
    for(const auto& name : matrices){
        Unfold_One_Matrix(input_file, name, args, user_set_bi, output_file, &to_be_saved_count);
        args.timer.time_elapsed();
    }
    Write_Iteration_Study_Hists(output_file, &to_be_saved_count);
    if(output_file != nullptr){
        std::cout << "\n" << Color::BBLUE << "Done Saving..." << Color::END << "\n" << std::endl;
        output_file->Close();
        delete output_file;
    }
    input_file->Close();
    delete input_file;
    return to_be_saved_count;
}

} // namespace

int main(int argc, char** argv){
    TH1::AddDirectory(kFALSE);
    gROOT->SetBatch(kTRUE);
    bool user_set_bi = ArgWasPassed(argc, argv, {"-bi", "-bayes-it", "--bayes_iterations"});
    UnfoldArgs args = main_start(argc, argv);
    int to_be_saved_count = 0;
    try {
        to_be_saved_count = main_simple_unfold(args, user_set_bi);
    } catch(const std::exception& exc){
        Crash_Report(args, std::string("The Simple Unfolding Code has CRASHED!\nERROR MESSAGE:\n\n") + exc.what());
    } catch(...){
        Crash_Report(args, "The Simple Unfolding Code has CRASHED!\nERROR MESSAGE:\n\nunknown exception");
    }
    Construct_Email(args, false, false, to_be_saved_count);
    return 0;
}
