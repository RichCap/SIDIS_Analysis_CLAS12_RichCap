# Run-local BC_RC guide. The shared Phi_h files are not edited.
# start=auto chose the universal spline file: the keys a BC_RC histogram selects are mostly untagged, with median B width 0.17, not the tight 3D windows.
# Earlier acceptance and RC results may guide a later edit. They are not copied onto these histograms here.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2: the spline guide's second pass left these BC histograms off their own cosine.
# (1, 8) uses this histogram's cosine. The legacy BC limits [-0.03, 0.05] and [0, 0.1] cannot reach it.
# Acceptance and RC parameters are not copied onto these histograms.
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.20667169, "B_limits": [-0.32667169, -0.08667169], "C_initial": -0.00373954, "C_limits": [-0.08373954, 0.07626046], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "2", "3D", "BC")] = {"B_initial": -0.10099264, "B_limits": [-0.22099264, 0.01900736], "C_initial": 0.04324697, "C_limits": [-0.03675303, 0.12324697], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.21701102, "B_limits": [-0.33701102, -0.09701102], "C_initial": 0.08713105, "C_limits": [0.00713105, 0.16713105], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.22470842, "B_limits": [-0.34470842, -0.10470842], "C_initial": -0.03999767, "C_limits": [-0.15397088, 0.07397554], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.23909226, "B_limits": [-0.35909226, -0.11909226], "C_initial": 0.04474704, "C_limits": [-0.03525296, 0.12474704], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.12013774, "B_limits": [-0.24013774, -0.00013774], "C_initial": -0.01498042, "C_limits": [-0.09498042, 0.06501958], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.15586501, "B_limits": [-0.27586501, -0.03586501], "C_initial": 0.03578685, "C_limits": [-0.04421315, 0.11578685], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20844011, "B_limits": [-0.32844011, -0.08844011], "C_initial": 0.08770235, "C_limits": [0.00770235, 0.16770235], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06394192, "B_limits": [-0.18394192, 0.05605808], "C_initial": -0.09028923, "C_limits": [-0.17028923, -0.01028923], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.11596400, "B_limits": [-0.27596400, 0.04403600], "C_initial": -0.05166000, "C_limits": [-0.17166000, 0.06834000], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
