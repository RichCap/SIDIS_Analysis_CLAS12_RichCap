#include "generated/Dedicated_5D_Binning.h"

#include <iostream>
#include <string>

int main(){
    using namespace sidis5d;
    int fails = 0;
    auto check_start = [&](int q2y, int zpt, bool expect_ok){
        ConvertResult r = Convert_All_Kinematic_Bins("Q2-y=" + std::to_string(q2y) + ", z-pT=" + std::to_string(zpt),
                                                     "MultiDim_Q2_y_z_pT_phi_h");
        if(r.ok != expect_ok){
            std::cerr << "start mismatch Q2-y=" << q2y << " z-pT=" << zpt
                      << " ok=" << r.ok << " value=" << r.value << "\n";
            ++fails;
        }
        if(r.ok){
            ConvertResult q = Convert_All_Kinematic_Bins("MultiDim_Q2_y_z_pT_phi_h=" + std::to_string(r.value), "Q2-y");
            ConvertResult z = Convert_All_Kinematic_Bins("MultiDim_Q2_y_z_pT_phi_h=" + std::to_string(r.value), "z-pT");
            if((!q.ok) || (!z.ok) || (q.value != q2y) || (z.value != zpt)){
                std::cerr << "reverse mismatch start=" << r.value << "\n";
                ++fails;
            }
            ConvertResult mid = Convert_All_Kinematic_Bins("MultiDim_Q2_y_z_pT_phi_h=" + std::to_string(r.value + 1), "Q2-y");
            if(mid.ok){
                std::cerr << "mid-slot should be missing for python-dict lookup: slot=" << (r.value + 1) << "\n";
                ++fails;
            }
        }
    };
    check_start(1, 1, true);
    check_start(4, 1, false); // skipped by skip_condition / absent from live map
    check_start(4, 7, true);
    std::cout << "Q2-y=1 last z-pT = " << std::get<1>(Get_Num_of_z_pT_Bins_w_Migrations(1)) << "\n";
    std::cout << "skip(4,1) = " << skip_condition_z_pT_bins(4, 1) << "\n";
    std::cout << "skip(1,1) = " << skip_condition_z_pT_bins(1, 1) << "\n";
    ConvertResult s = Convert_All_Kinematic_Bins("Q2-y=1, z-pT=1", "MultiDim_Q2_y_z_pT_phi_h");
    std::cout << "start Q2-y=1,z-pT=1 -> " << (s.ok ? std::to_string(s.value) : std::string("ERROR")) << "\n";
    if(fails == 0){
        std::cout << "binning_check passed\n";
        return 0;
    }
    std::cout << "binning_check failed (" << fails << ")\n";
    return 1;
}
