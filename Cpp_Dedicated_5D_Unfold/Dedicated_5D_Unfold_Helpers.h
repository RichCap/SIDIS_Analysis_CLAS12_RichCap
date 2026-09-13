#pragma once

#include "generated/Dedicated_5D_Binning.h"

#include <algorithm>
#include <chrono>
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

#include "TFile.h"
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
    int bayes_iterations = 6;
    int Num_Toys = 10;
    std::vector<std::string> bins = {"1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17"};
    bool verbose = false;
    double Min_Allowed_Acceptance_Cut = 0.0005;
    std::string single_file_input = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_1st_Order_V2_Response_Matrices_Final_Analysis_Iterations_I0_All.root";
    bool email = false;
    std::string email_message = "";
    std::string background_source = "lundvpk";
    bool require_weighed = false;
    std::string weight_tag = "";
    bool has_increment = false;
    int increment = 0;
    bool has_num_bins = false;
    int num_bins = 0;
    bool matrix_pdf = false;
    std::string pdf_name = "Rebuilt_5D_Response_Matrix.pdf";
    bool logz = false;
    bool recover_slices = false;
    std::string data_root = "work";

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

inline void print_help(){
    std::cout <<
        "Dedicated_5D_Unfold (C++): 5D Bayesian unfolding.\n"
        "Same flags as Dedicated_5D_Unfold.py.\n\n"
        "  -t, --test                 Run without saving files\n"
        "  -r, --root NAME            Output ROOT file\n"
        "  --no_smear                 Unsmeared MC only\n"
        "  -sim, --simulation         Use reconstructed MC as data\n"
        "  -mod, --modulation         Modulated MC response matrices\n"
        "  -bi, --bayes_iterations N  Bayesian iterations (default 6)\n"
        "  -nt, --Num_Toys N          Toy count for unfolding errors (default 10)\n"
        "  -b, --bins 1 2 ...         Q2-y bin indices\n"
        "  -v, --verbose              Print saved histogram names\n"
        "  -ac, --Min_Allowed_Acceptance_Cut X\n"
        "  -sfin, --single_file_input PATH\n"
        "  -e, --email                Mail when finished\n"
        "  -em, --email_message TEXT\n"
        "  -bgs, --background_source lundvpk|lundrho|None\n"
        "  -rw, --require_weighed\n"
        "  -wt, --weight_tag ''|Acc|JSON|Spline|AccJSON|AccSpline\n"
        "  -i, --increment N          Force slice increment\n"
        "  -nb, --num_bins N          Force flattened 5D bin count\n"
        "  -mpdf, --matrix_pdf        Rebuild matrix and save PDF only\n"
        "  -pdf, --pdf_name PATH\n"
        "  -lz, --logz\n"
        "  -rs, --recover_slices      Slice an existing unfolded 1D\n"
        "  -droot, --data_root work|work_b\n";
}

inline UnfoldArgs parse_args(int argc, char** argv){
    UnfoldArgs args;
    for(int i = 1; i < argc; ++i){
        std::string arg = argv[i];
        if((arg == "-h") || (arg == "--help")){
            print_help();
            std::exit(0);
        } else if(match_opt(arg, {"-t", "-ns", "--test", "--time", "--no-save"})){
            args.test = true;
        } else if(match_opt(arg, {"-r", "--root"})){
            args.root = opt_value(i, argc, argv, arg, "--root");
        } else if(match_opt(arg, {"-no-smear", "--no_smear"})){
            args.no_smear = true;
        } else if(match_opt(arg, {"-sim", "--simulation"})){
            args.sim = true;
        } else if(match_opt(arg, {"-mod", "--modulation"})){
            args.mod = true;
        } else if(match_opt(arg, {"-bi", "-bayes-it", "--bayes_iterations"})){
            args.bayes_iterations = std::atoi(opt_value(i, argc, argv, arg, "--bayes_iterations").c_str());
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
        } else {
            std::cerr << "Unknown argument: " << arg << std::endl;
            print_help();
            std::exit(2);
        }
    }
    if((args.background_source != "lundvpk") && (args.background_source != "lundrho") && (args.background_source != "None")){
        std::cerr << "Invalid --background_source: " << args.background_source << std::endl;
        std::exit(2);
    }
    const std::vector<std::string> ok_tags = {"", "Acc", "JSON", "Spline", "AccJSON", "AccSpline"};
    if(std::find(ok_tags.begin(), ok_tags.end(), args.weight_tag) == ok_tags.end()){
        std::cerr << "Invalid --weight_tag: " << args.weight_tag << std::endl;
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
    add_arg("increment", args.has_increment ? std::to_string(args.increment) : "None");
    add_arg("num_bins", args.has_num_bins ? std::to_string(args.num_bins) : "None");
    add_arg("matrix_pdf", format_arg_value_bool(args.matrix_pdf));
    add_arg("logz", format_arg_value_bool(args.logz));
    add_arg("recover_slices", format_arg_value_bool(args.recover_slices));
    add_arg("data_root", "'" + args.data_root + "'");
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

} // namespace sidis5d
