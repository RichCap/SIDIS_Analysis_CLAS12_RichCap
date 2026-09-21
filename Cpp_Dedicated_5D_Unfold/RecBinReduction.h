#ifndef SIDIS_REC_BIN_REDUCTION_H
#define SIDIS_REC_BIN_REDUCTION_H

#include <iostream>
#include <string>
#include <vector>

#include "TH1.h"
#include "TH2.h"
#include "TH1D.h"
#include "TH2D.h"

namespace sidis5d {

struct RecSkipMap {
    int orig_n = 0;
    double xmin = 0.0;
    double xmax = 1.0;
    std::vector<int> kept;
    std::vector<int> skipped;
    std::vector<std::string> reason;
    std::vector<int> orig_to_reduced;

    int n_kept() const { return static_cast<int>(kept.size()); }
    bool is_skipped(int orig) const {
        return (orig >= 1) && (orig <= orig_n) && (orig_to_reduced[static_cast<size_t>(orig)] < 0);
    }
    int reduced_index(int orig) const {
        if((orig < 1) || (orig > orig_n)){ return -1; }
        return orig_to_reduced[static_cast<size_t>(orig)];
    }
};

inline RecSkipMap Build_Rec_Skip_Map(TH1* rdf, TH1* mdf, TH1* gdf, TH1* bdf, double min_acc){
    RecSkipMap skip_map;
    skip_map.orig_n = rdf->GetNbinsX();
    skip_map.xmin = rdf->GetXaxis()->GetXmin();
    skip_map.xmax = rdf->GetXaxis()->GetXmax();
    skip_map.reason.assign(static_cast<size_t>(skip_map.orig_n + 1), "");
    skip_map.orig_to_reduced.assign(static_cast<size_t>(skip_map.orig_n + 1), -1);
    int reduced = 0;
    for(int i = 1; i <= skip_map.orig_n; ++i){
        const double rdf_c = rdf->GetBinContent(i);
        const double mdf_c = mdf->GetBinContent(i);
        const double gdf_c = gdf->GetBinContent(i);
        const double bdf_c = (bdf == nullptr) ? 0.0 : bdf->GetBinContent(i);
        const double rec_mc = mdf_c + bdf_c;
        std::string why;
        if(rdf_c == 0.0){
            why = "data_zero";
        } else if(rec_mc == 0.0){
            why = "mdf_bdf_zero";
        } else if(gdf_c == 0.0){
            std::cout << "WARNING: gdf == 0 in reconstructed/generated bin " << i
                      << "; skipping (mdf+bdf)/gdf test for this bin." << std::endl;
        } else if((rec_mc / gdf_c) < min_acc){
            why = "low_acceptance";
        }
        if(!why.empty()){
            skip_map.skipped.push_back(i);
            skip_map.reason[static_cast<size_t>(i)] = why;
        } else {
            ++reduced;
            skip_map.kept.push_back(i);
            skip_map.orig_to_reduced[static_cast<size_t>(i)] = reduced;
        }
    }
    return skip_map;
}

inline void Print_Rec_Skip_Map(const RecSkipMap& skip_map){
    std::cout << "original reconstructed bins: " << skip_map.orig_n << std::endl;
    std::cout << "reduced reconstructed bins: " << skip_map.n_kept() << std::endl;
    std::cout << "skipped reconstructed bins: " << skip_map.skipped.size() << std::endl;
    std::cout << "skipped original indices: ";
    if(skip_map.skipped.empty()){
        std::cout << "(none)" << std::endl;
        return;
    }
    for(size_t i = 0; i < skip_map.skipped.size(); ++i){
        if(i){ std::cout << ","; }
        std::cout << skip_map.skipped[i];
    }
    std::cout << std::endl;
}

inline TH1D* Compress_TH1_Rec(TH1* hist, const RecSkipMap& skip_map, const std::string& name){
    if(hist == nullptr){ return nullptr; }
    TH1D* out = new TH1D(name.c_str(), hist->GetTitle(), skip_map.n_kept(), 0.5, skip_map.n_kept() + 0.5);
    out->SetDirectory(0);
    out->Sumw2();
    for(int orig : skip_map.kept){
        const int red = skip_map.reduced_index(orig);
        out->SetBinContent(red, hist->GetBinContent(orig));
        out->SetBinError(red, hist->GetBinError(orig));
    }
    out->GetXaxis()->SetTitle(hist->GetXaxis()->GetTitle());
    out->GetYaxis()->SetTitle(hist->GetYaxis()->GetTitle());
    return out;
}

inline TH1D* Restore_TH1_From_Reduced(TH1* reduced, const RecSkipMap& skip_map, const std::string& name){
    if(reduced == nullptr){ return nullptr; }
    TH1D* out = new TH1D(name.c_str(), reduced->GetTitle(), skip_map.orig_n, skip_map.xmin, skip_map.xmax);
    out->SetDirectory(0);
    out->Sumw2();
    for(int orig : skip_map.kept){
        const int red = skip_map.reduced_index(orig);
        out->SetBinContent(orig, reduced->GetBinContent(red));
        out->SetBinError(orig, reduced->GetBinError(red));
    }
    return out;
}

inline TH1* Mask_Full_To_Analysis(TH1* full_hist, const RecSkipMap& skip_map, const std::string& name){
    if(full_hist == nullptr){ return nullptr; }
    TH1* out = dynamic_cast<TH1*>(full_hist->Clone(name.c_str()));
    if(out == nullptr){ return nullptr; }
    out->SetDirectory(0);
    for(int orig : skip_map.skipped){
        if((orig >= 1) && (orig <= out->GetNbinsX())){
            out->SetBinContent(orig, 0);
            out->SetBinError(orig, 0);
        }
    }
    return out;
}

inline TH2D* Compress_TH2_Rec_Axis(TH2* th2, const RecSkipMap& skip_map, bool rec_is_x, const std::string& name){
    if(th2 == nullptr){ return nullptr; }
    const int n_kept = skip_map.n_kept();
    TH2D* out = nullptr;
    if(rec_is_x){
        const int ny = th2->GetNbinsY();
        out = new TH2D(name.c_str(), th2->GetTitle(), n_kept, 0.5, n_kept + 0.5,
                       ny, th2->GetYaxis()->GetXmin(), th2->GetYaxis()->GetXmax());
        out->SetDirectory(0);
        out->Sumw2();
        for(int orig : skip_map.kept){
            const int red = skip_map.reduced_index(orig);
            for(int y = 0; y <= ny + 1; ++y){
                out->SetBinContent(red, y, th2->GetBinContent(orig, y));
                out->SetBinError(red, y, th2->GetBinError(orig, y));
            }
        }
    } else {
        const int nx = th2->GetNbinsX();
        out = new TH2D(name.c_str(), th2->GetTitle(), nx, th2->GetXaxis()->GetXmin(), th2->GetXaxis()->GetXmax(),
                       n_kept, 0.5, n_kept + 0.5);
        out->SetDirectory(0);
        out->Sumw2();
        for(int orig : skip_map.kept){
            const int red = skip_map.reduced_index(orig);
            for(int x = 0; x <= nx + 1; ++x){
                out->SetBinContent(x, red, th2->GetBinContent(x, orig));
                out->SetBinError(x, red, th2->GetBinError(x, orig));
            }
        }
    }
    out->GetXaxis()->SetTitle(th2->GetXaxis()->GetTitle());
    out->GetYaxis()->SetTitle(th2->GetYaxis()->GetTitle());
    return out;
}

} // namespace sidis5d

#endif
