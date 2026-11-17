# RC_Bayesian guide for cached-scale rc_sf2. The shared manual initializer is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# rc_sf2 bins whose manual window missed the histogram cosine.
special_fit_parameters_set[("13", "4", "3D", "RC")] = {"B_initial": -0.2235, "B_limits": [-0.3235, -0.1235], "C_initial": -0.0414, "C_limits": [-0.1414, 0.0586], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16", "3D", "RC")] = {"B_initial": -0.1326, "B_limits": [-0.2326, -0.0326], "C_initial": -0.0187, "C_limits": [-0.1187, 0.0813], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "RC")] = {"B_initial": -0.1010, "B_limits": [-0.2010, -0.0010], "C_initial": -0.0234, "C_limits": [-0.1234, 0.0766], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11", "3D", "RC")] = {"B_initial": -0.2135, "B_limits": [-0.3135, -0.1135], "C_initial": -0.0039, "C_limits": [-0.1039, 0.0961], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15", "3D", "RC")] = {"B_initial": -0.2756, "B_limits": [-0.3756, -0.1756], "C_initial": 0.0505, "C_limits": [-0.0495, 0.1505], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "29", "3D", "RC")] = {"B_initial": -0.1972, "B_limits": [-0.2972, -0.0972], "C_initial": 0.0640, "C_limits": [-0.0360, 0.1640], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5", "3D", "RC")] = {"B_initial": -0.2521, "B_limits": [-0.3521, -0.1521], "C_initial": -0.0303, "C_limits": [-0.1303, 0.0697], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "24", "3D", "RC")] = {"B_initial": -0.2146, "B_limits": [-0.3146, -0.1146], "C_initial": 0.0513, "C_limits": [-0.0487, 0.1513], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "16", "3D", "RC")] = {"B_initial": 0.0143, "B_limits": [-0.0857, 0.1143], "C_initial": 0.0160, "C_limits": [-0.0840, 0.1160], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "31", "3D", "RC")] = {"B_initial": 0.0274, "B_limits": [-0.0726, 0.1274], "C_initial": 0.0358, "C_limits": [-0.0642, 0.1358], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "17", "3D", "RC")] = {"B_initial": -0.0427, "B_limits": [-0.1427, 0.0573], "C_initial": -0.0236, "C_limits": [-0.1236, 0.0764], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
