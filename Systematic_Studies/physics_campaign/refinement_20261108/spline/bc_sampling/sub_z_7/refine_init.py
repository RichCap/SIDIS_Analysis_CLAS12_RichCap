# Run-local BC_RC guide for spline kinematic-sampling sub_z_7.
# The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17, 5 of 452 are narrower than 0.05, and 305 leave B unlimited, so the windows are not tight.
# --use_spline_init is not also passed. Nominal parameters are not copied onto these histograms.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_z_7", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.13427538, "B_limits": [-0.33427538, 0.06572462], "C_initial": -0.06053083, "C_limits": [-0.26053083, 0.13946917], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.00098732, "B_limits": [-0.19901268, 0.20098732], "C_initial": -0.01096863, "C_limits": [-0.21096863, 0.18903137], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03436187, "B_limits": [-0.23436187, 0.16563813], "C_initial": -0.02475017, "C_limits": [-0.22475017, 0.17524983], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.00394953, "B_limits": [-0.19605047, 0.20394953], "C_initial": 0.03766686, "C_limits": [-0.16233314, 0.23766686], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.14636651, "B_limits": [-0.34636651, 0.05363349], "C_initial": 0.05642449, "C_limits": [-0.14357551, 0.25642449], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "9", "3D", "BC")] = {"B_initial": -0.06874223, "B_limits": [-0.26874223, 0.13125777], "C_initial": 0.01919667, "C_limits": [-0.18080333, 0.21919667], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02159859, "B_limits": [-0.17840141, 0.22159859], "C_initial": 0.03709566, "C_limits": [-0.16290434, 0.23709566], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.21324988, "B_limits": [-0.41324988, -0.01324988], "C_initial": 0.08720991, "C_limits": [-0.11279009, 0.28720991], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07295981, "B_limits": [-0.27295981, 0.12704019], "C_initial": -0.00213884, "C_limits": [-0.20213884, 0.19786116], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19886098, "B_limits": [-0.39886098, 0.00113902], "C_initial": 0.00024984, "C_limits": [-0.19975016, 0.20024984], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.21261364, "B_limits": [-0.41261364, -0.01261364], "C_initial": 0.08611677, "C_limits": [-0.11388323, 0.28611677], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.24938066, "B_limits": [-0.44938066, -0.04938066], "C_initial": -0.04853119, "C_limits": [-0.24853119, 0.15146881], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24682952, "B_limits": [-0.44682952, -0.04682952], "C_initial": -0.02121780, "C_limits": [-0.22121780, 0.17878220], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.23827440, "B_limits": [-0.43827440, -0.03827440], "C_initial": 0.04587304, "C_limits": [-0.15412696, 0.24587304], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11846910, "B_limits": [-0.31846910, 0.08153090], "C_initial": -0.01595435, "C_limits": [-0.21595435, 0.18404565], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14861952, "B_limits": [-0.34861952, 0.05138048], "C_initial": 0.04015999, "C_limits": [-0.15984001, 0.24015999], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.21232119, "B_limits": [-0.41232119, -0.01232119], "C_initial": 0.09337653, "C_limits": [-0.10662347, 0.29337653], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.07196031, "B_limits": [-0.27196031, 0.12803969], "C_initial": -0.09189080, "C_limits": [-0.29189080, 0.10810920], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10739596, "B_limits": [-0.30739596, 0.09260404], "C_initial": -0.00791974, "C_limits": [-0.20791974, 0.19208026], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
