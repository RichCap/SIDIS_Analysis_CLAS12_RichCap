#pragma once

#include "generated/Dedicated_5D_Binning.h"

#include <algorithm>
#include <chrono>
#include <cctype>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

#include "TArrayD.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TObject.h"
#include "TDirectory.h"

namespace sidis5d {

namespace Color {
    const char CYAN[] = "\033[96m";
    const char PURPLE[] = "\033[95m";
    const char PINK[] = "\033[35m";
    const char BLUE[] = "\033[94m";
    const char YELLOW[] = "\033[93m";
    const char GREEN[] = "\033[92m";
    const char RED[] = "\033[91m";
    const char DARKCYAN[] = "\033[36m";
    const char BOLD[] = "\033[1m";
    const char LIGHT[] = "\033[2m";
    const char ITALIC[] = "\033[3m";
    const char UNDERLINE[] = "\033[4m";
    const char BLINK[] = "\033[5m";
    const char END[] = "\033[0m";
    const char ERROR[] = "\033[91m\033[1m\033[4m";
    const char Error[] = "\033[91m\033[1m";
    const char BBLUE[] = "\033[1m\033[94m";
    const char BCYAN[] = "\033[1m\033[96m";
    const char BGREEN[] = "\033[1m\033[92m";
    const char BYELLOW[] = "\033[1m\033[93m";
    const char BPINK[] = "\033[1m\033[35m";
    const char BPURPLE[] = "\033[1m\033[95m";
    const char BUNDERLINE[] = "\033[1m\033[4m";
    const char END_B[] = "\033[0m\033[1m";
    const char END_R[] = "\033[0m\033[91m";
    const char END_C[] = "\033[0m\033[96m";
    const char END_G[] = "\033[0m\033[92m";
    const char END_b[] = "\033[0m\033[94m";
    const char END_E[] = "\033[0m\033[91m\033[1m\033[4m";
    const char END_e[] = "\033[0m\033[91m\033[1m";
    const char END_U[] = "\033[0m\033[4m";
}

namespace ColorBg {
    const char BLACK[] = "\033[40m";
    const char RED[] = "\033[41m";
    const char GREEN[] = "\033[42m";
    const char YELLOW[] = "\033[43m";
    const char BLUE[] = "\033[44m";
    const char MAGENTA[] = "\033[45m";
    const char CYAN[] = "\033[46m";
    const char WHITE[] = "\033[47m";
    const char RESET[] = "\033[49m";
    const char END[] = "\033[0m";
}

namespace RootColor {
    const int White = 0;
    const int Black = 1;
    const int Red = 2;
    const int Green = 3;
    const int Blue = 4;
    const int Yellow = 5;
    const int Pink = 6;
    const int Cyan = 7;
    const int DGreen = 8;
    const int Purple = 9;
    const int DGrey = 13;
    const int Grey = 15;
    const int LGrey = 17;
    const int Brown = 28;
    const int Teal = 30;
    const int Gold = 41;
    const int Rust = 46;
    const char Bold[] = "#font[22]";
    const char Italic[] = "#font[12]";
    const char Delta[] = "#Delta";
    const char Phi[] = "#phi";
    const char Degrees[] = "#circ";
    const char Hline[] = "#topbar";
    const char Line[] = "#splitline";
}

inline bool contains(const std::string& hay, const std::string& needle){
    return hay.find(needle) != std::string::npos;
}

inline std::string replace_all(std::string s, const std::string& from, const std::string& to){
    if(from.empty()){ return s; }
    size_t pos = 0;
    while((pos = s.find(from, pos)) != std::string::npos){
        s.replace(pos, from.size(), to);
        pos += to.size();
    }
    return s;
}

inline std::string to_lower_copy(std::string s){
    for(char& c : s){ c = static_cast<char>(std::tolower(static_cast<unsigned char>(c))); }
    return s;
}

inline bool key_in_file(TFile* file, const std::string& name){
    if((file == nullptr) || (file->GetListOfKeys() == nullptr)){ return false; }
    return file->GetListOfKeys()->FindObject(name.c_str()) != nullptr;
}

inline void safe_write(TObject* obj, TFile* tfile){
    if((obj == nullptr) || (tfile == nullptr)){ return; }
    TObject* existing = tfile->GetListOfKeys()->FindObject(obj->GetName());
    if(existing){
        std::string del = std::string(obj->GetName()) + ";*";
        tfile->Delete(del.c_str());
    }
    obj->Write();
}

class RuntimeTimer {
public:
    std::chrono::system_clock::time_point start_time;
    std::chrono::system_clock::time_point end_time;
    bool started = false;

    static std::string format_time(const std::chrono::system_clock::time_point& tp){
        std::time_t t = std::chrono::system_clock::to_time_t(tp);
        std::tm local_tm{};
#if defined(_WIN32)
        localtime_s(&local_tm, &t);
#else
        localtime_r(&t, &local_tm);
#endif
        int hour = local_tm.tm_hour;
        int minute = local_tm.tm_min;
        const char* am_pm = ((hour < 12) || (hour == 0)) ? "a.m." : "p.m.";
        int hour_display = (hour % 12);
        if(hour_display == 0){ hour_display = 12; }
        char buf[32];
        std::snprintf(buf, sizeof(buf), "%02d:%02d %s", hour_display, minute, am_pm);
        return std::string(buf);
    }

    static void ymd(const std::chrono::system_clock::time_point& tp, int& month, int& day, int& year){
        std::time_t t = std::chrono::system_clock::to_time_t(tp);
        std::tm local_tm{};
#if defined(_WIN32)
        localtime_s(&local_tm, &t);
#else
        localtime_r(&t, &local_tm);
#endif
        month = local_tm.tm_mon + 1;
        day = local_tm.tm_mday;
        year = local_tm.tm_year + 1900;
    }

    void start(){
        start_time = std::chrono::system_clock::now();
        started = true;
        int month = 0, day = 0, year = 0;
        ymd(start_time, month, day, year);
        std::cout << "\nStarted running on " << Color::BOLD << month << "-" << day << "-" << year
                  << Color::END << " at " << Color::BOLD << format_time(start_time) << Color::END << "\n";
    }

    std::string start_find() const {
        int month = 0, day = 0, year = 0;
        ymd(start_time, month, day, year);
        std::ostringstream oss;
        oss << "Ran on " << Color::BOLD << month << "-" << day << "-" << year
            << Color::END << " at " << Color::BOLD << format_time(start_time) << Color::END;
        return oss.str();
    }

    std::vector<std::string> time_elapsed(bool return_Q=false){
        end_time = std::chrono::system_clock::now();
        std::ostringstream current;
        current << "\nCurrent Time: " << Color::BOLD << format_time(end_time) << Color::END;
        auto delta = end_time - start_time;
        long total_seconds = static_cast<long>(std::chrono::duration_cast<std::chrono::seconds>(delta).count());
        if(total_seconds < 0){ total_seconds = 0; }
        long days = total_seconds / 86400;
        long rem = total_seconds - days * 86400;
        long hours = rem / 3600;
        rem = rem % 3600;
        long minutes = rem / 60;
        long seconds = rem % 60;
        std::ostringstream elapse;
        elapse << "Time Elapsed Up To Now:\n" << days << " Day(s), " << hours << " Hour(s), "
               << minutes << " Minute(s), and " << seconds << " Second(s).\n";
        if(return_Q){
            return {current.str(), elapse.str()};
        }
        std::cout << current.str() << "\n" << elapse.str() << std::endl;
        return {};
    }

    std::vector<std::string> stop(const std::string& count_label="", int count_value=-1){
        end_time = std::chrono::system_clock::now();
        std::ostringstream end_ss;
        end_ss << "\nThe time that this code finished is " << Color::BOLD << format_time(end_time) << Color::END;
        auto delta = end_time - start_time;
        long total_seconds = static_cast<long>(std::chrono::duration_cast<std::chrono::seconds>(delta).count());
        if(total_seconds < 0){ total_seconds = 0; }
        long days = total_seconds / 86400;
        long rem = total_seconds - days * 86400;
        long hours = rem / 3600;
        rem = rem % 3600;
        long minutes = rem / 60;
        long seconds = rem % 60;
        std::ostringstream total;
        total << "The total time the code took to run is:\n" << days << " Day(s), " << hours << " Hour(s), "
              << minutes << " Minute(s), and " << seconds << " Second(s).";
        std::string rate_line = "";
        if((!count_label.empty()) && (count_value >= 0) && (total_seconds > 0)){
            double rate = static_cast<double>(count_value) / static_cast<double>(total_seconds);
            std::ostringstream rate_ss;
            rate_ss.setf(std::ios::fixed);
            rate_ss.precision(2);
            rate_ss << "Saved " << count_value << " " << count_label << "...\nRate = " << rate << " " << count_label << "/Seconds";
            rate_line = rate_ss.str();
        }
        return {end_ss.str(), total.str(), rate_line};
    }
};

struct UnfoldArgs {
    bool test = false;
    std::string root = "Unfolded_5D_Histos_From_Dedicated_5D_Unfold.root";
    bool no_smear = false;
    bool sim = false;
    bool mod = false;
    bool closure = false;
    int bayes_iterations = 5;
    int phi_bins = 24;
    int Num_Toys = 10;
    std::vector<std::string> bins = {"1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17"};
    bool verbose = false;
    // double Min_Allowed_Acceptance_Cut = 0.0005; // Changed to 0.025 on 9/16/2026
    // double Min_Allowed_Acceptance_Cut = 0.025; // Changed to 0.020 on 10/26/2026
    double Min_Allowed_Acceptance_Cut = 0.020;
    std::string single_file_input = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_1st_Order_V2_Response_Matrices_Final_Analysis_Iterations_I0_All.root";
    bool email = false;
    std::string email_message = "";
    // std::string background_source = "lundvpk";  // 10/25/2026
    std::string background_source = "rho0_new";
    bool require_weighed = false;
    std::string weight_tag = "";
    // auto divides only for Spline. on requires Spline. off keeps the original product.
    std::string spline_amplitude_correction = "auto";
    bool divide_spline_by_unweighted = false;
    bool spline_divide_self_test = false;
    // bayesian is RooUnfold. bin is the existing acceptance ratio on the same corrected MC.
    std::string unfold_method = "bayesian";
    bool skip_acceptance_mask = false;
    std::string physical_bin_map = "";
    // Simple_Unfold only. Weighted pseudo-data on the nominal response. 9/26/2026
    std::string closure_weight = "";
    // Simple_Unfold only. Replace the measured histogram. Response and fakes stay as for data. 9/28/2026
    std::string pseudo_data = "";
    bool has_increment = false;
    int increment = 0;
    bool has_num_bins = false;
    int num_bins = 0;
    bool matrix_pdf = false;
    std::string pdf_name = "Rebuilt_5D_Response_Matrix.pdf";
    bool logz = false;
    bool recover_slices = false;
    std::string data_root = "work";
    // std::string error_mode = "toys";
    std::string error_mode = "covariance";
    bool iteration_study = false;
    bool study_only = false;
    bool unfolding_1D = false;
    bool unfolding_3D = false;
    bool old_binning = false;
    bool no_post_unfold_acc_cut = false;
    bool has_parm_min = false;
    bool has_parm_max = false;
    bool has_parm_step = false;
    double parm_min = 1.0;
    double parm_max = 15.0;
    double parm_step = 1.0;

    std::string pass_version = "Pass 2";
    std::string smearing_options = "smear";
    std::string standard_histogram_title_addition = "";
    std::vector<std::string> Q2_y_Bin_List;
    int increment_5d = 0;
    int num_bins_5d = 0;
    int num_slices_5d = 0;
    RuntimeTimer timer;
};

inline bool is_flag(const std::string& arg){
    return (!arg.empty()) && (arg[0] == '-');
}

inline bool match_opt(const std::string& arg, const std::vector<std::string>& names){
    for(const auto& name : names){
        if(arg == name){ return true; }
        if((arg.size() > name.size()) && (arg.compare(0, name.size(), name) == 0) && (arg[name.size()] == '=')){ return true; }
    }
    return false;
}

inline std::string opt_value(int& i, int argc, char** argv, const std::string& arg, const std::string& name_for_eq){
    auto eq = arg.find('=');
    if(eq != std::string::npos){ return arg.substr(eq + 1); }
    if(i + 1 >= argc){
        std::cerr << "Missing value for " << name_for_eq << std::endl;
        std::exit(2);
    }
    ++i;
    return argv[i];
}

inline bool DivideSplineActive(const std::string& mode, const std::string& weight_tag, std::string& error){
    error.clear();
    if((mode != "auto") && (mode != "on") && (mode != "off")){
        error = "Invalid --spline_amplitude_correction: " + mode + " (expected auto|on|off)";
        return false;
    }
    if(mode == "on"){
        if(weight_tag != "Spline"){
            error = "--spline_amplitude_correction on requires --weight_tag Spline";
            return false;
        }
        return true;
    }
    if(mode == "off"){ return false; }
    return weight_tag == "Spline";
}

inline void Apply_Weight_Output_Suffix(UnfoldArgs& args, bool generated_column_mode = false){
    if(args.weight_tag.empty()){ return; }
    const bool divide = args.divide_spline_by_unweighted && (args.weight_tag == "Spline");
    const std::string weighted = "_W" + args.weight_tag;
    const std::string correction_suffix = generated_column_mode ? "_ColGenRatio.root" : "_DivUnw.root";
    const std::string suffix = divide ? (weighted + correction_suffix) : (weighted + ".root");
    if((args.root.size() >= suffix.size()) && (args.root.compare(args.root.size() - suffix.size(), suffix.size(), suffix) == 0)){
        return;
    }
    const std::string weighted_root = weighted + ".root";
    if(divide && (args.root.size() >= weighted_root.size()) && (args.root.compare(args.root.size() - weighted_root.size(), weighted_root.size(), weighted_root) == 0)){
        args.root.replace(args.root.size() - 5, 5, correction_suffix);
        return;
    }
    if((args.root.size() >= 5) && (args.root.compare(args.root.size() - 5, 5, ".root") == 0)){
        args.root.replace(args.root.size() - 5, 5, suffix);
    }
}

inline const char* SplineAmplitudeCorrectionLabel(const UnfoldArgs& args, bool generated_column_mode = false){
    if(args.divide_spline_by_unweighted && generated_column_mode){ return "spline_amplitude_correction=generated_column_target_ratio"; }
    if(args.divide_spline_by_unweighted){ return "spline_amplitude_correction=divided_by_unweighted"; }
    return "spline_amplitude_correction=off";
}

inline const char* AcceptanceMaskLabel(const UnfoldArgs& args){
    if(args.skip_acceptance_mask){ return "acceptance_mask=not_applied"; }
    if(args.divide_spline_by_unweighted && !args.old_binning){
        return "acceptance_mask=preserved_original_spline_before_column_correction";
    }
    return "acceptance_mask=legacy";
}

inline const char* UnfoldMethodLabel(const UnfoldArgs& args){
    if(args.unfold_method == "bin"){ return "unfold_method=bin_by_bin"; }
    return "unfold_method=bayesian";
}

inline std::string UnweightedSplineCounterpart(const std::string& name){
    const std::string suffix = "_(Spline)";
    if((name.size() >= suffix.size()) && (name.compare(name.size() - suffix.size(), suffix.size(), suffix) == 0)){
        return name.substr(0, name.size() - suffix.size());
    }
    return "";
}

inline bool AxisEdgesMatch(const TAxis* left, const TAxis* right){
    if((left == nullptr) || (right == nullptr)){ return false; }
    if(left->GetNbins() != right->GetNbins()){ return false; }
    const TArrayD* left_edges = left->GetXbins();
    const TArrayD* right_edges = right->GetXbins();
    const int left_n = (left_edges == nullptr) ? 0 : left_edges->GetSize();
    const int right_n = (right_edges == nullptr) ? 0 : right_edges->GetSize();
    if((left_n > 0) || (right_n > 0)){
        if(left_n != right_n){ return false; }
        for(int edge = 0; edge < left_n; ++edge){
            if(std::abs(left_edges->At(edge) - right_edges->At(edge)) > 1e-6){ return false; }
        }
        return true;
    }
    if(std::abs(left->GetXmin() - right->GetXmin()) > 1e-6){ return false; }
    if(std::abs(left->GetXmax() - right->GetXmax()) > 1e-6){ return false; }
    return true;
}

inline bool HistogramsMatchForDivide(const TH1* weighted, const TH1* unweighted){
    if((weighted == nullptr) || (unweighted == nullptr)){ return false; }
    if(std::string(weighted->ClassName()) != std::string(unweighted->ClassName())){ return false; }
    if(!AxisEdgesMatch(weighted->GetXaxis(), unweighted->GetXaxis())){ return false; }
    if(weighted->GetDimension() >= 2){
        if(!AxisEdgesMatch(weighted->GetYaxis(), unweighted->GetYaxis())){ return false; }
    }
    if(weighted->GetDimension() >= 3){
        if(!AxisEdgesMatch(weighted->GetZaxis(), unweighted->GetZaxis())){ return false; }
    }
    return true;
}

inline TH1* DivideSplineClone(TH1* weighted, TH1* unweighted, std::string& error){
    error.clear();
    if((weighted == nullptr) || (unweighted == nullptr)){
        error = "missing histogram for spline division";
        return nullptr;
    }
    const std::string weighted_name = weighted->GetName();
    const std::string unweighted_name = unweighted->GetName();
    if(!HistogramsMatchForDivide(weighted, unweighted)){
        error = "incompatible spline counterpart\n\tnumerator = " + weighted_name + "\n\tdenominator = " + unweighted_name;
        return nullptr;
    }
    TH1* clone = dynamic_cast<TH1*>(weighted->Clone((weighted_name + "_DivUnw").c_str()));
    if(clone == nullptr){
        error = "could not clone " + weighted_name;
        return nullptr;
    }
    clone->SetDirectory(nullptr);
    if(!clone->Divide(unweighted)){
        error = "ROOT Divide failed\n\tnumerator = " + weighted_name + "\n\tdenominator = " + unweighted_name;
        delete clone;
        return nullptr;
    }
    return clone;
}

inline TH1* LoadSplineCounterpart(TFile* file, const std::string& weighted_name, std::string& error){
    error.clear();
    const std::string denom = UnweightedSplineCounterpart(weighted_name);
    if(denom.empty()){
        error = "spline numerator does not end with _(Spline): " + weighted_name;
        return nullptr;
    }
    if(!key_in_file(file, denom)){
        error = "missing unweighted counterpart\n\tnumerator = " + weighted_name + "\n\tdenominator = " + denom;
        return nullptr;
    }
    TH1* histo = dynamic_cast<TH1*>(file->Get(denom.c_str()));
    if(histo == nullptr){
        error = "unweighted counterpart is not a histogram: " + denom;
        return nullptr;
    }
    return histo;
}

struct SplineColumnDiagnostics {
    double max_rec_projection_abs = 0.0;
    double max_rec_projection_rel = 0.0;
    double max_migration_fraction_change = 0.0;
    double max_efficiency_change = 0.0;
    double weighted_fake_overflow_sum = 0.0;
    double unweighted_fake_overflow_sum = 0.0;
    double corrected_fake_overflow_sum = 0.0;
    int empty_generated_bins = 0;
};

// Histogram-level correction for the 3D response layout used before its RooUnfold axis flip:
// X is generated and Y is reconstructed. For generated bin j, N_j is the unweighted full
// generated population and W_j is its weighted sum. The target is T_j=W_j/N_j, while every
// matched response entry receives the one common factor 1/N_j. This preserves both the
// within-column migration fractions and matched/full efficiency. It is a binned mean-weight
// correction, not an event-level removal of a weight that varies inside the generated bin.
inline bool CorrectSplineGeneratedColumns3D(const TH2* weighted_response,
                                            const TH2* unweighted_response,
                                            const TH1* weighted_reconstructed,
                                            const TH1* weighted_generated,
                                            const TH1* unweighted_generated,
                                            TH2*& corrected_response,
                                            TH1*& rebuilt_reconstructed,
                                            TH1*& target_generated,
                                            std::string& error,
                                            SplineColumnDiagnostics* diagnostics = nullptr){
    corrected_response = nullptr;
    rebuilt_reconstructed = nullptr;
    target_generated = nullptr;
    error.clear();
    SplineColumnDiagnostics local;
    if((weighted_response == nullptr) || (unweighted_response == nullptr) || (weighted_reconstructed == nullptr) ||
       (weighted_generated == nullptr) || (unweighted_generated == nullptr)){
        error = "missing histogram for the generated-column spline correction";
        return false;
    }
    if((weighted_response->GetNbinsX() != weighted_generated->GetNbinsX()) ||
       (weighted_response->GetNbinsY() != weighted_reconstructed->GetNbinsX()) ||
       !AxisEdgesMatch(weighted_response->GetXaxis(), unweighted_response->GetXaxis()) ||
       !AxisEdgesMatch(weighted_response->GetYaxis(), unweighted_response->GetYaxis()) ||
       !AxisEdgesMatch(weighted_response->GetXaxis(), weighted_generated->GetXaxis()) ||
       !AxisEdgesMatch(weighted_response->GetXaxis(), unweighted_generated->GetXaxis()) ||
       !AxisEdgesMatch(weighted_response->GetYaxis(), weighted_reconstructed->GetXaxis())){
        error = "incompatible axes for the generated-column spline correction";
        return false;
    }

    // Refuse to erase a material unmatched/fake component hidden in the supplied reconstructed
    // histogram. Tiny floating-point summation differences are expected for weighted inputs.
    for(int rec_bin = 0; rec_bin <= weighted_response->GetNbinsY() + 1; ++rec_bin){
        double projected = 0.0;
        for(int gen_bin = 0; gen_bin <= weighted_response->GetNbinsX() + 1; ++gen_bin){
            projected += weighted_response->GetBinContent(gen_bin, rec_bin);
        }
        const double supplied = weighted_reconstructed->GetBinContent(rec_bin);
        const double abs_diff = std::abs(supplied - projected);
        const double scale = std::max(1.0, std::max(std::abs(supplied), std::abs(projected)));
        local.max_rec_projection_abs = std::max(local.max_rec_projection_abs, abs_diff);
        local.max_rec_projection_rel = std::max(local.max_rec_projection_rel, abs_diff / scale);
        if(abs_diff > (1e-9 * scale)){
            error = "weighted reconstructed MC contains a material component outside the response projection at bin " +
                    std::to_string(rec_bin);
            return false;
        }
    }

    corrected_response = dynamic_cast<TH2*>(weighted_response->Clone((std::string(weighted_response->GetName()) + "_ColGenRatio").c_str()));
    rebuilt_reconstructed = dynamic_cast<TH1*>(weighted_reconstructed->Clone((std::string(weighted_reconstructed->GetName()) + "_FromCorrectedColumns").c_str()));
    target_generated = dynamic_cast<TH1*>(weighted_generated->Clone((std::string(weighted_generated->GetName()) + "_MeanSplineTarget").c_str()));
    if((corrected_response == nullptr) || (rebuilt_reconstructed == nullptr) || (target_generated == nullptr)){
        error = "could not clone histograms for the generated-column spline correction";
        delete corrected_response;
        delete rebuilt_reconstructed;
        delete target_generated;
        corrected_response = nullptr;
        rebuilt_reconstructed = nullptr;
        target_generated = nullptr;
        return false;
    }
    corrected_response->SetDirectory(nullptr);
    rebuilt_reconstructed->SetDirectory(nullptr);
    target_generated->SetDirectory(nullptr);
    rebuilt_reconstructed->Reset("ICES");
    target_generated->Reset("ICES");

    // Bins 0..N are the bins copied by the existing 3D axis flip. Bin N+1 is the generated
    // overflow that the flip intentionally leaves out, so RooUnfold infers it from reconstructed
    // minus matrix projection as an MC fake component.
    for(int gen_bin = 0; gen_bin <= weighted_response->GetNbinsX(); ++gen_bin){
        const double unweighted_full = unweighted_generated->GetBinContent(gen_bin);
        const double weighted_full = weighted_generated->GetBinContent(gen_bin);
        double weighted_matched = 0.0;
        for(int rec_bin = 0; rec_bin <= weighted_response->GetNbinsY() + 1; ++rec_bin){
            weighted_matched += weighted_response->GetBinContent(gen_bin, rec_bin);
        }
        if(unweighted_full < 0.0){
            error = "negative unweighted generated population at bin " + std::to_string(gen_bin);
            delete corrected_response;
            delete rebuilt_reconstructed;
            delete target_generated;
            corrected_response = nullptr;
            rebuilt_reconstructed = nullptr;
            target_generated = nullptr;
            return false;
        }
        if(unweighted_full == 0.0){
            ++local.empty_generated_bins;
            if((std::abs(weighted_full) > 1e-12) || (std::abs(weighted_matched) > 1e-12)){
                error = "nonzero weighted content with zero unweighted generated population at bin " + std::to_string(gen_bin);
                delete corrected_response;
                delete rebuilt_reconstructed;
                delete target_generated;
                corrected_response = nullptr;
                rebuilt_reconstructed = nullptr;
                target_generated = nullptr;
                return false;
            }
            target_generated->SetBinContent(gen_bin, 0.0);
            target_generated->SetBinError(gen_bin, 0.0);
            for(int rec_bin = 0; rec_bin <= weighted_response->GetNbinsY() + 1; ++rec_bin){
                corrected_response->SetBinContent(gen_bin, rec_bin, 0.0);
                corrected_response->SetBinError(gen_bin, rec_bin, 0.0);
            }
            continue;
        }

        const double factor = 1.0 / unweighted_full;
        const double target = weighted_full * factor;
        target_generated->SetBinContent(gen_bin, target);
        // The denominator is the population defining the sample mean, not an independent random
        // histogram. Scale the stored weighted-sum uncertainty by the same fixed common factor.
        target_generated->SetBinError(gen_bin, weighted_generated->GetBinError(gen_bin) * std::abs(factor));
        double corrected_matched = 0.0;
        for(int rec_bin = 0; rec_bin <= weighted_response->GetNbinsY() + 1; ++rec_bin){
            const double before = weighted_response->GetBinContent(gen_bin, rec_bin);
            const double after = before * factor;
            corrected_response->SetBinContent(gen_bin, rec_bin, after);
            corrected_response->SetBinError(gen_bin, rec_bin, weighted_response->GetBinError(gen_bin, rec_bin) * std::abs(factor));
            corrected_matched += after;
            if((weighted_matched != 0.0) && (corrected_matched != 0.0)){
                const double before_fraction = before / weighted_matched;
                const double after_fraction = after / (weighted_matched * factor);
                local.max_migration_fraction_change = std::max(local.max_migration_fraction_change,
                                                                 std::abs(before_fraction - after_fraction));
            }
        }
        if((weighted_full != 0.0) && (target != 0.0)){
            local.max_efficiency_change = std::max(local.max_efficiency_change,
                                                    std::abs((weighted_matched / weighted_full) -
                                                             (corrected_matched / target)));
        }
    }

    const int fake_gen_bin = weighted_response->GetNbinsX() + 1;
    for(int rec_bin = 0; rec_bin <= weighted_response->GetNbinsY() + 1; ++rec_bin){
        local.weighted_fake_overflow_sum += weighted_response->GetBinContent(fake_gen_bin, rec_bin);
        local.unweighted_fake_overflow_sum += unweighted_response->GetBinContent(fake_gen_bin, rec_bin);
    }
    if(local.unweighted_fake_overflow_sum < 0.0){
        error = "negative unweighted generated-overflow fake population";
        delete corrected_response;
        delete rebuilt_reconstructed;
        delete target_generated;
        corrected_response = nullptr;
        rebuilt_reconstructed = nullptr;
        target_generated = nullptr;
        return false;
    }
    if(local.unweighted_fake_overflow_sum == 0.0 && std::abs(local.weighted_fake_overflow_sum) > 1e-12){
        error = "nonzero weighted generated-overflow fakes with zero unweighted fake population";
        delete corrected_response;
        delete rebuilt_reconstructed;
        delete target_generated;
        corrected_response = nullptr;
        rebuilt_reconstructed = nullptr;
        target_generated = nullptr;
        return false;
    }
    const double fake_factor = (local.unweighted_fake_overflow_sum > 0.0)
                                 ? (1.0 / local.unweighted_fake_overflow_sum) : 0.0;
    for(int rec_bin = 0; rec_bin <= weighted_response->GetNbinsY() + 1; ++rec_bin){
        const double corrected_fake = weighted_response->GetBinContent(fake_gen_bin, rec_bin) * fake_factor;
        corrected_response->SetBinContent(fake_gen_bin, rec_bin, corrected_fake);
        corrected_response->SetBinError(fake_gen_bin, rec_bin,
                                        weighted_response->GetBinError(fake_gen_bin, rec_bin) * std::abs(fake_factor));
        local.corrected_fake_overflow_sum += corrected_fake;
    }
    target_generated->SetBinContent(fake_gen_bin, 0.0);
    target_generated->SetBinError(fake_gen_bin, 0.0);

    for(int rec_bin = 0; rec_bin <= corrected_response->GetNbinsY() + 1; ++rec_bin){
        double sum = 0.0;
        double error2 = 0.0;
        for(int gen_bin = 0; gen_bin <= corrected_response->GetNbinsX() + 1; ++gen_bin){
            sum += corrected_response->GetBinContent(gen_bin, rec_bin);
            const double bin_error = corrected_response->GetBinError(gen_bin, rec_bin);
            error2 += bin_error * bin_error;
        }
        rebuilt_reconstructed->SetBinContent(rec_bin, sum);
        rebuilt_reconstructed->SetBinError(rec_bin, std::sqrt(error2));
    }
    if(diagnostics != nullptr){ *diagnostics = local; }
    return true;
}

inline void print_help(){
    std::cout <<
        "Dedicated_5D_Unfold (C++): 5D Bayesian unfolding.\n"
        "Same flags as Dedicated_5D_Unfold.py.\n\n"
        "  -t, --test                 Run without saving files\n"
        "  -r, --root NAME            Output ROOT file\n"
        "  --no_smear                 Unsmeared MC only\n"
        "  -sim, --simulation         Use reconstructed MC as data\n"
        "  -mod, --modulation         Modulated MC response matrices\n"
        "  -bi, --bayes_iterations N  Bayesian iterations (default 5; 3D uses its bin map unless this flag is passed)\n"
        "  -nt, --Num_Toys N          Toy count for unfolding errors (default 10)\n"
        "  -b, --bins 1 2 ...         Q2-y bin indices\n"
        "  -v, --verbose              Print saved histogram names\n"
        "  -ac, --Min_Allowed_Acceptance_Cut X\n"
        "  -sfin, --single_file_input PATH\n"
        "  -e, --email                Mail when finished\n"
        "  -em, --email_message TEXT\n"
        // "  -bgs, --background_source lundvpk|lundrho|None\n"  // 10/25/2026
        "  -bgs, --background_source rho0_new|lundvpk|lundrho|None\n"
        "  -rw, --require_weighed\n"
        "  -wt, --weight_tag ''|Acc|JSON|Spline|AccJSON|AccSpline\n"
        "  -sac, --spline_amplitude_correction auto|on|off\n"
        "                             3D Spline generated-column correction (default auto)\n"
        "  -um, --unfold_method bayesian|bin\n"
        "                             bayesian uses RooUnfold. bin is acceptance correction on the same MC\n"
        "  -sam, --skip_acceptance_mask\n"
        "                             Leave the acceptance mask unapplied, for the correction-off comparison\n"
        "  -cw, --closure_weight Acc|AccSpline\n"
        "                             Simple_Unfold only: weighted pseudo-data, nominal response\n"
        "  -pd, --pseudo_data nominal|Acc|Spline|AccSpline\n"
        "                             Simple_Unfold only: replace the measured histogram on the data configuration\n"
        "  -i, --increment N          Force slice increment\n"
        "  -nb, --num_bins N          Force flattened 5D bin count\n"
        "  -mpdf, --matrix_pdf        Rebuild matrix and save PDF only\n"
        "  -pdf, --pdf_name PATH\n"
        "  -lz, --logz\n"
        "  -rs, --recover_slices      Slice an existing unfolded 1D\n"
        "  -droot, --data_root work|work_b\n"
        "  -err, --error_mode toys|covariance|errors|none\n"
        "                             Unfolding error treatment (default covariance; toys still selects kCovToys)\n"
        "  -ist, --iteration_study    Optional RooUnfoldParms scan (not the default path)\n"
        "  -so, --study_only          With --iteration_study, skip the extra nominal unfold\n"
        "  -pmin, --parm_min X  -pmax, --parm_max Y  -pstep, --parm_step Z\n"
        "  -u1D, --unfolding_1D       1D unfolding only\n"
        "  -u3D, --unfolding_3D       3D unfolding only\n"
        "  -ob, --old_binning         Keep full reconstructed binning (previous behavior)\n"
        "  -npac, --no_post_unfold_acc_cut\n"
        "                             Disable the legacy acceptance cut applied after unfolding\n";
}

inline UnfoldArgs parse_args(int argc, char** argv){
    UnfoldArgs args;
    bool saw_positional_bins = false;
    for(int i = 1; i < argc; ++i){
        std::string arg = argv[i];
        if((arg == "-h") || (arg == "--help")){
            print_help();
            std::exit(0);
        } else if(match_opt(arg, {"-t", "-ns", "--test", "--time", "--no-save"})){
            args.test = true;
        } else if(match_opt(arg, {"-r", "--root"})){
            args.root = opt_value(i, argc, argv, arg, "--root");
        } else if(match_opt(arg, {"-no-smear", "--no_smear", "-nos"})){
            args.no_smear = true;
        } else if(match_opt(arg, {"-smear", "--smear"})){
            args.no_smear = false;
        } else if(match_opt(arg, {"-sim", "--simulation"})){
            args.sim = true;
        } else if(match_opt(arg, {"-mod", "--modulation"})){
            args.mod = true;
        } else if(match_opt(arg, {"-bi", "-bayes-it", "--bayes_iterations"})){
            args.bayes_iterations = std::atoi(opt_value(i, argc, argv, arg, "--bayes_iterations").c_str());
        } else if(match_opt(arg, {"-ph", "--phi_bins"})){
            args.phi_bins = std::atoi(opt_value(i, argc, argv, arg, "--phi_bins").c_str());
            if((args.phi_bins != 12) && (args.phi_bins != 24)){
                std::cerr << "--phi_bins must be 12 or 24" << std::endl;
                std::exit(2);
            }
        } else if(match_opt(arg, {"-nt", "-ntoys", "--Num_Toys"})){
            args.Num_Toys = std::atoi(opt_value(i, argc, argv, arg, "--Num_Toys").c_str());
        } else if(match_opt(arg, {"-b", "--bins"})){
            args.bins.clear();
            if(arg.find('=') != std::string::npos){
                args.bins.push_back(opt_value(i, argc, argv, arg, "--bins"));
            }
            while((i + 1 < argc) && (!is_flag(argv[i + 1]))){
                ++i;
                args.bins.push_back(argv[i]);
            }
            if(args.bins.empty()){
                std::cerr << "Missing value for --bins" << std::endl;
                std::exit(2);
            }
        } else if(match_opt(arg, {"-v", "--verbose"})){
            args.verbose = true;
        } else if(match_opt(arg, {"-ac", "-acceptance-cut", "--Min_Allowed_Acceptance_Cut"})){
            args.Min_Allowed_Acceptance_Cut = std::atof(opt_value(i, argc, argv, arg, "--Min_Allowed_Acceptance_Cut").c_str());
        } else if(match_opt(arg, {"-sfin", "--single_file_input"})){
            args.single_file_input = opt_value(i, argc, argv, arg, "--single_file_input");
        } else if(match_opt(arg, {"-e", "--email"})){
            args.email = true;
        } else if(match_opt(arg, {"-em", "--email_message"})){
            args.email_message = opt_value(i, argc, argv, arg, "--email_message");
        } else if(match_opt(arg, {"-bgs", "--background_source"})){
            args.background_source = opt_value(i, argc, argv, arg, "--background_source");
        } else if(match_opt(arg, {"-rw", "--require_weighed"})){
            args.require_weighed = true;
        } else if(match_opt(arg, {"-wt", "--weight_tag"})){
            args.weight_tag = opt_value(i, argc, argv, arg, "--weight_tag");
        } else if(match_opt(arg, {"-sac", "--spline_amplitude_correction"})){
            args.spline_amplitude_correction = opt_value(i, argc, argv, arg, "--spline_amplitude_correction");
        } else if(match_opt(arg, {"-um", "--unfold_method"})){
            args.unfold_method = opt_value(i, argc, argv, arg, "--unfold_method");
        } else if(match_opt(arg, {"-sam", "--skip_acceptance_mask"})){
            args.skip_acceptance_mask = true;
        } else if(match_opt(arg, {"-sds", "--spline_divide_self_test"})){
            args.spline_divide_self_test = true;
        } else if(match_opt(arg, {"-cw", "--closure_weight"})){
            args.closure_weight = opt_value(i, argc, argv, arg, "--closure_weight");
        } else if(match_opt(arg, {"-pd", "--pseudo_data"})){
            args.pseudo_data = opt_value(i, argc, argv, arg, "--pseudo_data");
        } else if(match_opt(arg, {"-i", "--increment"})){
            args.has_increment = true;
            args.increment = std::atoi(opt_value(i, argc, argv, arg, "--increment").c_str());
        } else if(match_opt(arg, {"-nb", "--num_bins"})){
            args.has_num_bins = true;
            args.num_bins = std::atoi(opt_value(i, argc, argv, arg, "--num_bins").c_str());
        } else if(match_opt(arg, {"-mpdf", "--matrix_pdf"})){
            args.matrix_pdf = true;
        } else if(match_opt(arg, {"-pdf", "--pdf_name"})){
            args.pdf_name = opt_value(i, argc, argv, arg, "--pdf_name");
        } else if(match_opt(arg, {"-lz", "--logz"})){
            args.logz = true;
        } else if(match_opt(arg, {"-rs", "--recover_slices"})){
            args.recover_slices = true;
        } else if(match_opt(arg, {"-droot", "--data_root"})){
            args.data_root = opt_value(i, argc, argv, arg, "--data_root");
        } else if(match_opt(arg, {"-err", "--error_mode"})){
            args.error_mode = opt_value(i, argc, argv, arg, "--error_mode");
        } else if(match_opt(arg, {"-ist", "--iteration_study"})){
            args.iteration_study = true;
        } else if(match_opt(arg, {"-so", "--study_only"})){
            args.study_only = true;
        } else if(match_opt(arg, {"-pmin", "--parm_min"})){
            args.has_parm_min = true;
            args.parm_min = std::atof(opt_value(i, argc, argv, arg, "--parm_min").c_str());
        } else if(match_opt(arg, {"-pmax", "--parm_max"})){
            args.has_parm_max = true;
            args.parm_max = std::atof(opt_value(i, argc, argv, arg, "--parm_max").c_str());
        } else if(match_opt(arg, {"-pstep", "--parm_step"})){
            args.has_parm_step = true;
            args.parm_step = std::atof(opt_value(i, argc, argv, arg, "--parm_step").c_str());
        } else if(match_opt(arg, {"-u1D", "--unfolding_1D"})){
            args.unfolding_1D = true;
        } else if(match_opt(arg, {"-ob", "--old_binning"})){
            args.old_binning = true;
        } else if(match_opt(arg, {"-npac", "--no_post_unfold_acc_cut"})){
            args.no_post_unfold_acc_cut = true;
        } else if(match_opt(arg, {"-u3D", "--unfolding_3D"})){
            args.unfolding_3D = true;
        } else if(!is_flag(arg)){
            if(!saw_positional_bins){
                args.bins.clear();
                saw_positional_bins = true;
            }
            args.bins.push_back(arg);
        } else {
            std::cerr << "Unknown argument: " << arg << std::endl;
            print_help();
            std::exit(2);
        }
    }
    // 10/25/2026: rho0_new joins lundvpk, lundrho, and None.
    if((args.background_source != "rho0_new") && (args.background_source != "lundvpk") && (args.background_source != "lundrho") && (args.background_source != "None")){
        std::cerr << "Invalid --background_source: " << args.background_source << std::endl;
        std::exit(2);
    }
    const std::vector<std::string> ok_tags = {"", "Acc", "JSON", "Spline", "AccJSON", "AccSpline"};
    if(std::find(ok_tags.begin(), ok_tags.end(), args.weight_tag) == ok_tags.end()){
        std::cerr << "Invalid --weight_tag: " << args.weight_tag << std::endl;
        std::exit(2);
    }
    if((args.closure_weight != "") && (args.closure_weight != "Acc") && (args.closure_weight != "AccSpline")){
        std::cerr << "Invalid --closure_weight: " << args.closure_weight << " (expected Acc|AccSpline)" << std::endl;
        std::exit(2);
    }
    if(!args.closure_weight.empty()){
        if(!args.sim){
            std::cerr << "--closure_weight requires --simulation" << std::endl;
            std::exit(2);
        }
        if(!args.weight_tag.empty()){
            std::cerr << "--closure_weight uses the nominal response; do not set --weight_tag" << std::endl;
            std::exit(2);
        }
    }
    if((args.pseudo_data != "") && (args.pseudo_data != "nominal") && (args.pseudo_data != "Acc")
       && (args.pseudo_data != "Spline") && (args.pseudo_data != "AccSpline")){
        std::cerr << "Invalid --pseudo_data: " << args.pseudo_data << " (expected nominal|Acc|Spline|AccSpline)" << std::endl;
        std::exit(2);
    }
    if(!args.pseudo_data.empty()){
        if(args.sim){
            std::cerr << "--pseudo_data uses the data configuration; do not set --simulation" << std::endl;
            std::exit(2);
        }
        if(!args.closure_weight.empty() || !args.weight_tag.empty()){
            std::cerr << "--pseudo_data replaces only the measured histogram; do not set --closure_weight or --weight_tag" << std::endl;
            std::exit(2);
        }
    }
    if((args.error_mode != "toys") && (args.error_mode != "covariance") &&
       (args.error_mode != "errors") && (args.error_mode != "none")){
        std::cerr << "Invalid --error_mode: " << args.error_mode
                  << " (expected toys|covariance|errors|none)" << std::endl;
        std::exit(2);
    }
    std::string spline_error;
    args.divide_spline_by_unweighted = DivideSplineActive(args.spline_amplitude_correction, args.weight_tag, spline_error);
    if(!spline_error.empty()){
        std::cerr << spline_error << std::endl;
        std::exit(2);
    }
    if((args.unfold_method != "bayesian") && (args.unfold_method != "bin")){
        std::cerr << "Invalid --unfold_method: " << args.unfold_method << " (expected bayesian|bin)" << std::endl;
        std::exit(2);
    }
    return args;
}

inline std::string strip_quotes(const std::string& s){
    return replace_all(replace_all(s, "\"", ""), "'", "");
}

inline std::string ansi_to_plain(std::string text){
    static const std::regex ansi(R"(\x1B\[[0-?]*[ -/]*[@-~])");
    return std::regex_replace(text, ansi, "");
}

inline void send_email(const std::string& subject, const std::string& body, const std::string& recipient){
    std::string html_body = ansi_to_plain(body);
    FILE* pipe = popen(("mail -s " + std::string("'") + replace_all(subject, "'", "") + "' " + recipient).c_str(), "w");
    if(pipe == nullptr){ return; }
    fwrite(html_body.data(), 1, html_body.size(), pipe);
    pclose(pipe);
}

inline void Update_Email(UnfoldArgs& args, const std::string& update_name="", const std::string& update_message="", bool verbose_override=false){
    std::string update_email;
    auto elapsed = args.timer.time_elapsed(true);
    std::string elapsed_line = elapsed.empty() ? "" : replace_all(elapsed.back(), "\n", " ");
    if(!update_message.empty()){
        update_email = update_message + "\n" + elapsed_line;
    } else if(!update_name.empty()){
        std::ostringstream oss;
        oss << "\n" << Color::BCYAN << update_name << Color::END_B << " is done running..." << Color::END << "\n"
            << elapsed_line << "\n\n";
        update_email = oss.str();
    }
    if(!update_email.empty()){
        args.email_message = args.email_message + "\n" + update_email;
        if(args.verbose || verbose_override){
            std::cout << update_email << std::endl;
        }
    }
}

inline std::string format_arg_value_bool(bool v){ return v ? "True" : "False"; }

inline void Construct_Email(UnfoldArgs& args, bool Crashed=false, bool Warning=false, int final_count=-1){
    std::string start_time = replace_all(args.timer.start_find(), "Ran", "Started running");
    std::vector<std::string> stopped;
    if(final_count < 0){
        stopped = args.timer.stop();
    } else {
        stopped = args.timer.stop("Histograms", final_count);
    }
    std::ostringstream args_list;
    auto add_arg = [&](const std::string& name, const std::string& value){
        char buf[80];
        std::snprintf(buf, sizeof(buf), "--%-50s--> ", name.c_str());
        args_list << "\n" << buf << value;
    };
    add_arg("test", format_arg_value_bool(args.test));
    add_arg("no_smear", format_arg_value_bool(args.no_smear));
    add_arg("sim", format_arg_value_bool(args.sim));
    add_arg("mod", format_arg_value_bool(args.mod));
    add_arg("bayes_iterations", std::to_string(args.bayes_iterations));
    add_arg("Num_Toys", std::to_string(args.Num_Toys));
    std::ostringstream bins_ss;
    bins_ss << "[";
    for(size_t i = 0; i < args.bins.size(); ++i){
        if(i){ bins_ss << ", "; }
        bins_ss << "'" << args.bins[i] << "'";
    }
    bins_ss << "]";
    add_arg("bins", bins_ss.str());
    add_arg("verbose", format_arg_value_bool(args.verbose));
    add_arg("Min_Allowed_Acceptance_Cut", std::to_string(args.Min_Allowed_Acceptance_Cut));
    add_arg("background_source", "'" + args.background_source + "'");
    add_arg("require_weighed", format_arg_value_bool(args.require_weighed));
    add_arg("weight_tag", "'" + args.weight_tag + "'");
    add_arg("closure_weight", "'" + args.closure_weight + "'");
    add_arg("pseudo_data", "'" + args.pseudo_data + "'");
    add_arg("increment", args.has_increment ? std::to_string(args.increment) : "None");
    add_arg("num_bins", args.has_num_bins ? std::to_string(args.num_bins) : "None");
    add_arg("matrix_pdf", format_arg_value_bool(args.matrix_pdf));
    add_arg("logz", format_arg_value_bool(args.logz));
    add_arg("recover_slices", format_arg_value_bool(args.recover_slices));
    add_arg("data_root", "'" + args.data_root + "'");
    add_arg("error_mode", "'" + args.error_mode + "'");
    add_arg("iteration_study", format_arg_value_bool(args.iteration_study));
    add_arg("old_binning", format_arg_value_bool(args.old_binning));
    add_arg("no_post_unfold_acc_cut", format_arg_value_bool(args.no_post_unfold_acc_cut));
    add_arg("pass_version", "'" + args.pass_version + "'");
    add_arg("closure", format_arg_value_bool(args.closure));
    add_arg("smearing_options", "'" + args.smearing_options + "'");

    std::string status;
    if(!(Crashed || Warning)){
        status = "finished running.";
    } else if(!Warning){
        status = std::string(Color::ERROR) + "CRASHED!" + Color::END;
    } else {
        status = std::string(Color::BYELLOW) + "GIVEN A WARNING MESSAGE" + Color::END;
    }
    std::ostringstream email_body;
    email_body << "\nThe 'Dedicated_5D_Unfold.py' script has " << status << "\n"
               << start_time << "\n\n"
               << "Input File:\n\t" << args.single_file_input << "\n"
               << "Output File:\n\t" << (args.matrix_pdf ? args.pdf_name : args.root) << "\n\n"
               << args.email_message << "\n\n"
               << "Detected 5D Configuration:\n"
               << "\tincrement  = " << args.increment << "\n"
               << "\tnum_bins   = " << args.num_bins << "\n"
               << "\tnum_slices = " << args.num_slices_5d << "\n\n"
               << "Arguments:" << args_list.str() << "\n\n"
               << stopped[0] << "\n"
               << stopped[1] << "\n"
               << stopped[2] << "\n    ";
    if(args.email){
        std::string subject = "Finished Running the 'Dedicated_5D_Unfold.py' Code";
        if(Crashed || Warning){
            subject = std::string(Crashed ? "CRASH" : "ERROR") + " REPORT: 'Dedicated_5D_Unfold.py' Code " + (Crashed ? "Failed" : "is still running...");
        }
        send_email(subject, email_body.str(), "richard.capobianco@uconn.edu");
    }
    std::cout << "\n\n\n\n" << Color::BOLD << ColorBg::YELLOW << "EMAIL MESSAGE TO SEND:" << Color::END
              << "\n\n" << email_body.str() << "\n" << std::endl;
    if(Warning){
        std::cout << "\n\n" << Color::BOLD << "CONTNUE RUNNING..." << Color::END << "\n\n" << std::endl;
    } else if(!Crashed){
        std::cout << Color::BGREEN << ColorBg::YELLOW
                  << "\n    \t                                   \t   "
                  << "\n    \tThis code has now finished running.\t   "
                  << "\n    \t                                   \t   " << Color::END << "\n\n    \n";
    } else {
        std::cout << Color::BYELLOW << ColorBg::RED
                  << "\n    \t                                   \t   "
                  << "\n    \t       This code has CRASHED!      \t   "
                  << "\n    \t                                   \t   " << Color::END << "\n\n    \n";
    }
}

inline void Crash_Report(UnfoldArgs& args, const std::string& crash_message_in="The Code has CRASHED!", bool continue_run=false){
    std::string crash_message;
    if(continue_run){
        crash_message = std::string("\n") + Color::BYELLOW + "ERROR WARNING!" + Color::END + "\n" + crash_message_in + "\n\nCONTINUED RUNNING...\n";
    } else {
        crash_message = std::string("\n") + Color::Error + "CRASH WARNING!" + Color::END + "\n" + crash_message_in + "\n";
    }
    std::cerr << crash_message << std::endl;
    args.email_message = args.email_message + "\n" + crash_message + "\n";
    Construct_Email(args, !continue_run, continue_run);
    if(!continue_run){
        std::exit(1);
    }
    std::cout << "\n\n" << Color::ERROR << "WILL CONTINUE RUNNING THROUGH THE ERROR" << Color::END << "\n\n" << std::endl;
}

inline bool regex_search_group(const std::string& text, const std::string& pattern, std::string& group){
    try {
        std::regex re(pattern);
        std::smatch match;
        if(std::regex_search(text, match, re) && (match.size() > 1)){
            group = match[1].str();
            return true;
        }
    } catch(...) {}
    return false;
}

inline std::string Histogram_Name_Def(const std::string& out_print,
                                      const std::string& Histo_General,
                                      const std::string& Data_Type,
                                      const std::string& Cut_Type,
                                      const std::string& Smear_Type,
                                      const std::string& Q2_y_Bin,
                                      const std::string& z_pT_Bin,
                                      const std::string& Bin_Extra,
                                      const std::string& Variable,
                                      const UnfoldArgs& args){
    std::vector<std::string> Pattern_List;
    const std::string Pattern_Histo_General = R"(\(Histo-Group='([^']+)')";
    const std::string Pattern_Data_Type     = R"(\(Data-Type='([^']+)')";
    const std::string Pattern_Cut_Type      = R"(\(Data-Cut='([^']+)')";
    const std::string Pattern_Smear_Type    = R"(\(Smear-Type='([^']+)')";
    const std::string Pattern_Q2_y_Bin      = R"(\[Q2-y-Bin=([^,]+),)";
    const std::string Pattern_Var_1         = R"(\(Var-D1='([^']+)')";
    const std::string Pattern_Var_2         = R"(\(Var-D2='([^']+)')";

    if(Histo_General == "Find"){ Pattern_List.push_back(Pattern_Histo_General); }
    else { Pattern_List.push_back(Histo_General); }
    if(Data_Type == "Find"){ Pattern_List.push_back(Pattern_Data_Type); }
    else { Pattern_List.push_back(Data_Type); }
    if(Cut_Type == "Find"){ Pattern_List.push_back(Pattern_Cut_Type); }
    else if((Cut_Type != "Skip") && (Cut_Type != "skip")){ Pattern_List.push_back(Cut_Type); }
    if(Smear_Type == "Find"){ Pattern_List.push_back(Pattern_Smear_Type); }
    else { Pattern_List.push_back(Smear_Type); }

    if(Bin_Extra == "Default"){
        if(Q2_y_Bin != "Find"){
            Pattern_List.push_back(std::string("Q2_y_Bin_") + ((Q2_y_Bin != "0") ? Q2_y_Bin : "All"));
        } else {
            Pattern_List.push_back(Pattern_Q2_y_Bin);
        }
        Pattern_List.push_back(std::string("z_pT_Bin_") + ((z_pT_Bin != "0") ? z_pT_Bin : "All"));
    } else if((Bin_Extra != "Skip") && (Bin_Extra != "skip")){
        Pattern_List.push_back(std::string("Kinematic_Bin_") + ((Bin_Extra != "0") ? Bin_Extra : "All"));
    }

    if(Variable == "Default"){
        Pattern_List.push_back(Pattern_Var_1);
        if(contains(out_print, "2D") || contains(out_print, "3D")){
            Pattern_List.push_back(Pattern_Var_2);
        }
    } else if((Variable == "Find") || (Variable == "FindAll") || (Variable == "FindOnly")){
        Pattern_List = {Pattern_Var_1};
        if(contains(out_print, "2D") || contains(out_print, "3D")){
            Pattern_List.push_back(Pattern_Var_2);
        }
    } else {
        Pattern_List.push_back(Variable);
    }
    if(Q2_y_Bin == "FindOnly"){
        Pattern_List = {Pattern_Q2_y_Bin};
    }

    std::string Name_Output;
    const std::vector<std::string> regex_patterns = {
        Pattern_Histo_General, Pattern_Data_Type, Pattern_Cut_Type, Pattern_Smear_Type,
        Pattern_Q2_y_Bin, Pattern_Var_1, Pattern_Var_2
    };
    for(const auto& pattern : Pattern_List){
        std::string histo_group;
        bool is_regex = std::find(regex_patterns.begin(), regex_patterns.end(), pattern) != regex_patterns.end();
        if(is_regex){
            std::string search_in = replace_all(out_print, "''", "' '");
            if(regex_search_group(search_in, pattern, histo_group)){
                if(histo_group == " "){ histo_group = "''"; }
                if(pattern == Pattern_Smear_Type){
                    histo_group = std::string("SMEAR=") + ((histo_group != "''") ? ("'" + histo_group + "'") : histo_group);
                }
                if(pattern == Pattern_Q2_y_Bin){
                    histo_group = "Q2_y_Bin_" + histo_group;
                }
            }
        } else {
            histo_group = pattern;
            if(pattern == Smear_Type){
                histo_group = std::string("SMEAR=") + ((pattern != "") ? pattern : "''");
            }
        }
        Name_Output = Name_Output + (Name_Output.empty() ? "(" : "_(") + histo_group + ")";
    }
    if(((Variable == "Find") || (Variable == "FindAll") || (Variable == "FindOnly")) && (!contains(Name_Output, ")_("))){
        Name_Output = replace_all(replace_all(Name_Output, "(", ""), ")", "");
    }
    Name_Output = replace_all(Name_Output, "cut_Complete_SIDIS_Proton", "Proton");
    Name_Output = replace_all(Name_Output, "cut_Complete_SIDIS_Integrate", "Integrate");
    if((args.closure || args.mod || args.sim) && contains(Name_Output, ")_(") &&
       (!contains(Name_Output, "Mod_Test")) && (!contains(Name_Output, "Closure_Test")) && (!contains(Name_Output, "Sim_Test"))){
        std::string tag = args.mod ? "Mod_Test" : (args.closure ? "Closure_Test" : "Sim_Test");
        Name_Output = Name_Output + "_(" + tag + ")";
    }
    return Name_Output;
}

struct HistoBins {
    bool ok = false;
    int num_bins = 0;
    double min_bin = 0;
    double max_bin = 0;
};

inline HistoBins Find_Bins_From_Histo_Name(const std::string& data_string){
    HistoBins out;
    std::regex pattern(R"(NumBins=(\d+),\s*MinBin=([-+]?\d*\.?\d+),\s*MaxBin=([-+]?\d*\.?\d+))");
    std::smatch match;
    if(std::regex_search(data_string, match, pattern) && (match.size() > 3)){
        out.ok = true;
        out.num_bins = std::atoi(match[1].str().c_str());
        out.min_bin = std::atof(match[2].str().c_str());
        out.max_bin = std::atof(match[3].str().c_str());
    } else {
        std::cout << Color::Error << "No matching data found." << Color::END << std::endl;
    }
    return out;
}

inline int coerce_bin_value(const ConvertResult& result){
    return result.ok ? result.value : -1;
}

inline bool Near(double left, double right){
    return std::abs(left - right) < 1e-6;
}

inline int SplineDivideSelfTest(){
    std::string error;
    if(UnweightedSplineCounterpart("response_(Spline)") != "response"){ std::cerr << "Spline suffix was not removed" << std::endl; return 1; }
    if(!UnweightedSplineCounterpart("response_(AccSpline)").empty()){ std::cerr << "AccSpline was treated as Spline" << std::endl; return 1; }
    if(DivideSplineActive("auto", "Spline", error) != true){ std::cerr << "auto Spline was off" << std::endl; return 1; }
    if(DivideSplineActive("auto", "AccSpline", error) != false){ std::cerr << "auto AccSpline was on" << std::endl; return 1; }
    if(DivideSplineActive("off", "Spline", error) != false){ std::cerr << "off still divided" << std::endl; return 1; }
    if(DivideSplineActive("on", "AccSpline", error) || error.empty()){ std::cerr << "on accepted AccSpline" << std::endl; return 1; }

    TH2D response("response", "response", 2, 0, 2, 2, 0, 2);
    response.SetBinContent(1, 1, 60.0); response.SetBinError(1, 1, 6.0);
    response.SetBinContent(1, 2, 20.0); response.SetBinError(1, 2, 2.0);
    response.SetBinContent(2, 1, 30.0); response.SetBinError(2, 1, 3.0);
    response.SetBinContent(2, 2, 30.0); response.SetBinError(2, 2, 3.0);
    response.SetBinContent(3, 1, 40.0); response.SetBinError(3, 1, 4.0);
    TH2D unweighted_response("unweighted_response", "unweighted_response", 2, 0, 2, 2, 0, 2);
    unweighted_response.SetBinContent(3, 1, 4.0);
    TH1D reconstructed("reconstructed", "reconstructed", 2, 0, 2);
    reconstructed.SetBinContent(1, 130.0); reconstructed.SetBinContent(2, 50.0);
    TH1D weighted_generated("weighted_generated", "weighted_generated", 2, 0, 2);
    weighted_generated.SetBinContent(1, 100.0); weighted_generated.SetBinError(1, 10.0);
    weighted_generated.SetBinContent(2, 120.0); weighted_generated.SetBinError(2, 12.0);
    TH1D unweighted_generated("unweighted_generated", "unweighted_generated", 2, 0, 2);
    unweighted_generated.SetBinContent(1, 10.0);
    unweighted_generated.SetBinContent(2, 20.0);

    TH2* corrected_response = nullptr;
    TH1* corrected_rec = nullptr;
    TH1* target_gen = nullptr;
    SplineColumnDiagnostics diagnostics;
    if(!CorrectSplineGeneratedColumns3D(&response, &unweighted_response, &reconstructed, &weighted_generated,
                                        &unweighted_generated, corrected_response, corrected_rec,
                                        target_gen, error, &diagnostics)){
        std::cerr << error << std::endl;
        return 1;
    }
    if((!Near(corrected_response->GetBinContent(1, 1), 6.0)) ||
       (!Near(corrected_response->GetBinContent(1, 2), 2.0)) ||
       (!Near(corrected_response->GetBinContent(2, 1), 1.5)) ||
       (!Near(corrected_response->GetBinContent(2, 2), 1.5))){
        std::cerr << "generated columns did not receive one common factor" << std::endl;
        return 1;
    }
    if((!Near(target_gen->GetBinContent(1), 10.0)) || (!Near(target_gen->GetBinContent(2), 6.0))){
        std::cerr << "generated mean-weight target mismatch" << std::endl;
        return 1;
    }
    if((!Near(corrected_rec->GetBinContent(1), 17.5)) || (!Near(corrected_rec->GetBinContent(2), 3.5))){
        std::cerr << "reconstructed projection was not rebuilt" << std::endl;
        return 1;
    }
    if((!Near(diagnostics.corrected_fake_overflow_sum, 10.0)) ||
       (!Near(corrected_response->GetBinContent(3, 1), 10.0))){
        std::cerr << "generated-overflow fake component was not preserved with one common factor" << std::endl;
        return 1;
    }
    if((diagnostics.max_migration_fraction_change > 1e-12) || (diagnostics.max_efficiency_change > 1e-12)){
        std::cerr << "migration shape or matched/full efficiency changed" << std::endl;
        return 1;
    }
    delete corrected_response;
    delete corrected_rec;
    delete target_gen;

    TH1D unmatched(reconstructed);
    unmatched.SetBinContent(1, 131.0);
    corrected_response = nullptr;
    corrected_rec = nullptr;
    target_gen = nullptr;
    error.clear();
    if(CorrectSplineGeneratedColumns3D(&response, &unweighted_response, &unmatched, &weighted_generated,
                                       &unweighted_generated, corrected_response, corrected_rec,
                                       target_gen, error, nullptr) || error.empty()){
        std::cerr << "material unmatched reconstructed content was accepted" << std::endl;
        return 1;
    }
    TH1D untouched("untouched", "untouched", 1, 0, 1);
    untouched.SetBinContent(1, 9); untouched.SetBinError(1, 3);
    if(DivideSplineActive("off", "Spline", error)){ std::cerr << "off mode would divide" << std::endl; return 1; }
    if((!Near(untouched.GetBinContent(1), 9.0)) || (!Near(untouched.GetBinError(1), 3.0))){ std::cerr << "off mode changed the histogram" << std::endl; return 1; }
    std::cout << "spline generated-column self-test ok" << std::endl;
    return 0;
}

} // namespace sidis5d
