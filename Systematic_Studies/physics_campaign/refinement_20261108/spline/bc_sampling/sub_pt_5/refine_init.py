# Run-local BC_RC guide for spline sub_pt_5. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17 and 5 of 452 are narrower than 0.05, so the windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_pt_5", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.17590807, "B_limits": [-0.37590807, 0.02409193], "C_initial": 0.02453343, "C_limits": [-0.17546657, 0.22453343], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.17564527, "B_limits": [-0.37564527, 0.02435473], "C_initial": -0.00898916, "C_limits": [-0.20898916, 0.19101084], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.12996541, "B_limits": [-0.32996541, 0.07003459], "C_initial": -0.06585656, "C_limits": [-0.26585656, 0.13414344], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.00893289, "B_limits": [-0.19106711, 0.20893289], "C_initial": -0.01515557, "C_limits": [-0.21515557, 0.18484443], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.01346504, "B_limits": [-0.18653496, 0.21346504], "C_initial": -0.00496403, "C_limits": [-0.20496403, 0.19503597], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03585785, "B_limits": [-0.23585785, 0.16414215], "C_initial": -0.02624812, "C_limits": [-0.22624812, 0.17375188], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("12", "24", "3D", "BC")] = {"B_initial": -0.10974745, "B_limits": [-0.30974745, 0.09025255], "C_initial": 0.02512574, "C_limits": [-0.17487426, 0.22512574], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.14831513, "B_limits": [-0.34831513, 0.05168487], "C_initial": 0.06020215, "C_limits": [-0.13979785, 0.26020215], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "15", "3D", "BC")] = {"B_initial": -0.06247481, "B_limits": [-0.26247481, 0.13752519], "C_initial": 0.01640514, "C_limits": [-0.18359486, 0.21640514], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.09788814, "B_limits": [-0.29788814, 0.10211186], "C_initial": 0.03575455, "C_limits": [-0.16424545, 0.23575455], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.21881710, "B_limits": [-0.41881710, -0.01881710], "C_initial": 0.09270582, "C_limits": [-0.10729418, 0.29270582], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07497219, "B_limits": [-0.27497219, 0.12502781], "C_initial": -0.00713228, "C_limits": [-0.20713228, 0.19286772], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19815833, "B_limits": [-0.39815833, 0.00184167], "C_initial": 0.00207296, "C_limits": [-0.19792704, 0.20207296], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.21794107, "B_limits": [-0.41794107, -0.01794107], "C_initial": 0.08758669, "C_limits": [-0.11241331, 0.28758669], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.23098551, "B_limits": [-0.43098551, -0.03098551], "C_initial": -0.04262925, "C_limits": [-0.24262925, 0.15737075], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24638407, "B_limits": [-0.44638407, -0.04638407], "C_initial": -0.03186136, "C_limits": [-0.23186136, 0.16813864], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.24089039, "B_limits": [-0.44089039, -0.04089039], "C_initial": 0.04731596, "C_limits": [-0.15268404, 0.24731596], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11820983, "B_limits": [-0.31820983, 0.08179017], "C_initial": -0.01306952, "C_limits": [-0.21306952, 0.18693048], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.15654717, "B_limits": [-0.35654717, 0.04345283], "C_initial": 0.03855817, "C_limits": [-0.16144183, 0.23855817], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.21173199, "B_limits": [-0.41173199, -0.01173199], "C_initial": 0.09441679, "C_limits": [-0.10558321, 0.29441679], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06718310, "B_limits": [-0.26718310, 0.13281690], "C_initial": -0.09437029, "C_limits": [-0.29437029, 0.10562971], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10503362, "B_limits": [-0.30503362, 0.09496638], "C_initial": -0.00489854, "C_limits": [-0.20489854, 0.19510146], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
