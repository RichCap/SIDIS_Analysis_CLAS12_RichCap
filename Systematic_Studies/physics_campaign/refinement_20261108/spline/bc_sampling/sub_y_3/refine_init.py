# Run-local BC_RC guide for spline sub_y_3. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17 and 5 of 452 are narrower than 0.05, so the windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_y_3", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.19220078, "B_limits": [-0.39220078, 0.00779922], "C_initial": 0.00881070, "C_limits": [-0.19118930, 0.20881070], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.17966299, "B_limits": [-0.37966299, 0.02033701], "C_initial": -0.01534896, "C_limits": [-0.21534896, 0.18465104], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.12592185, "B_limits": [-0.32592185, 0.07407815], "C_initial": -0.05691842, "C_limits": [-0.25691842, 0.14308158], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.01273432, "B_limits": [-0.18726568, 0.21273432], "C_initial": -0.01288272, "C_limits": [-0.21288272, 0.18711728], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.00628300, "B_limits": [-0.19371700, 0.20628300], "C_initial": -0.01047923, "C_limits": [-0.21047923, 0.18952077], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03338006, "B_limits": [-0.23338006, 0.16661994], "C_initial": -0.02485385, "C_limits": [-0.22485385, 0.17514615], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.00620236, "B_limits": [-0.19379764, 0.20620236], "C_initial": 0.03998407, "C_limits": [-0.16001593, 0.23998407], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.14408391, "B_limits": [-0.34408391, 0.05591609], "C_initial": 0.05560671, "C_limits": [-0.14439329, 0.25560671], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11632344, "B_limits": [-0.31632344, 0.08367656], "C_initial": -0.01734606, "C_limits": [-0.21734606, 0.18265394], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14490782, "B_limits": [-0.34490782, 0.05509218], "C_initial": 0.04241797, "C_limits": [-0.15758203, 0.24241797], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20858816, "B_limits": [-0.40858816, -0.00858816], "C_initial": 0.08527644, "C_limits": [-0.11472356, 0.28527644], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06953808, "B_limits": [-0.26953808, 0.13046192], "C_initial": -0.09268768, "C_limits": [-0.29268768, 0.10731232], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10556545, "B_limits": [-0.30556545, 0.09443455], "C_initial": -0.00957870, "C_limits": [-0.20957870, 0.19042130], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "4", "3D", "BC")] = {"B_initial": -0.17457241, "B_limits": [-0.37457241, 0.02542759], "C_initial": 0.01175394, "C_limits": [-0.18824606, 0.21175394], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "9", "3D", "BC")] = {"B_initial": -0.06138810, "B_limits": [-0.26138810, 0.13861190], "C_initial": 0.01644562, "C_limits": [-0.18355438, 0.21644562], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "15", "3D", "BC")] = {"B_initial": -0.06396982, "B_limits": [-0.26396982, 0.13603018], "C_initial": 0.01432991, "C_limits": [-0.18567009, 0.21432991], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02285812, "B_limits": [-0.17714188, 0.22285812], "C_initial": 0.03792086, "C_limits": [-0.16207914, 0.23792086], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "1", "3D", "BC")] = {"B_initial": -0.04226535, "B_limits": [-0.24226535, 0.15773465], "C_initial": 0.01804726, "C_limits": [-0.18195274, 0.21804726], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.09933349, "B_limits": [-0.29933349, 0.10066651], "C_initial": 0.03849785, "C_limits": [-0.16150215, 0.23849785], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.20793901, "B_limits": [-0.40793901, -0.00793901], "C_initial": 0.08013226, "C_limits": [-0.11986774, 0.28013226], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "5", "3D", "BC")] = {"B_initial": -0.22992755, "B_limits": [-0.42992755, -0.02992755], "C_initial": -0.03211168, "C_limits": [-0.23211168, 0.16788832], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07529203, "B_limits": [-0.27529203, 0.12470797], "C_initial": -0.00684010, "C_limits": [-0.20684010, 0.19315990], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19778573, "B_limits": [-0.39778573, 0.00221427], "C_initial": -0.00220197, "C_limits": [-0.20220197, 0.19779803], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20825448, "B_limits": [-0.40825448, -0.00825448], "C_initial": 0.08080136, "C_limits": [-0.11919864, 0.28080136], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.22051345, "B_limits": [-0.42051345, -0.02051345], "C_initial": -0.04181185, "C_limits": [-0.24181185, 0.15818815], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24369388, "B_limits": [-0.44369388, -0.04369388], "C_initial": -0.03558505, "C_limits": [-0.23558505, 0.16441495], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.23981033, "B_limits": [-0.43981033, -0.03981033], "C_initial": 0.04128588, "C_limits": [-0.15871412, 0.24128588], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "12", "3D", "BC")] = {"B_initial": -0.28234346, "B_limits": [-0.48234346, -0.08234346], "C_initial": 0.08121406, "C_limits": [-0.11878594, 0.28121406], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
