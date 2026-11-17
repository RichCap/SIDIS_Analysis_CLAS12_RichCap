# Run-local guide for eS6o Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('7', '34')] = {'B_initial': -0.1205, 'B_limits': [-0.3205, 0.0795], 'C_initial': -0.2460, 'C_limits': [-0.3960, -0.0960], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '22')] = {'B_initial': -0.1615, 'B_limits': [-0.3615, 0.0385], 'C_initial': -0.0791, 'C_limits': [-0.2291, 0.0709], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '16')] = {'B_initial': -0.2391, 'B_limits': [-0.4391, -0.0391], 'C_initial': -0.0942, 'C_limits': [-0.2442, 0.0558], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '14')] = {'B_initial': -0.1874, 'B_limits': [-0.3874, 0.0126], 'C_initial': -0.0803, 'C_limits': [-0.2303, 0.0697], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.2215, 'B_limits': [-0.4215, -0.0215], 'C_initial': -0.0279, 'C_limits': [-0.1779, 0.1221], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '23')] = {'B_initial': -0.2417, 'B_limits': [-0.4417, -0.0417], 'C_initial': 0.0149, 'C_limits': [-0.1351, 0.1649], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '9')] = {'B_initial': -0.1811, 'B_limits': [-0.3811, 0.0189], 'C_initial': -0.0024, 'C_limits': [-0.1524, 0.1476], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '13')] = {'B_initial': -0.1879, 'B_limits': [-0.3879, 0.0121], 'C_initial': -0.0048, 'C_limits': [-0.1548, 0.1452], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '29')] = {'B_initial': -0.2577, 'B_limits': [-0.4577, -0.0577], 'C_initial': 0.0444, 'C_limits': [-0.1056, 0.1944], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '17')] = {'B_initial': -0.1513, 'B_limits': [-0.3513, 0.0487], 'C_initial': 0.0100, 'C_limits': [-0.1400, 0.1600], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '28')] = {'B_initial': -0.1237, 'B_limits': [-0.3237, 0.0763], 'C_initial': -0.0339, 'C_limits': [-0.1839, 0.1161], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '27')] = {'B_initial': -0.1326, 'B_limits': [-0.3326, 0.0674], 'C_initial': -0.0397, 'C_limits': [-0.1897, 0.1103], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('8', '13')] = {'B_initial': -0.2062, 'B_limits': [-0.4062, -0.0062], 'C_initial': -0.1021, 'C_limits': [-0.2521, 0.0479], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '4')] = {'B_initial': -0.1190, 'B_limits': [-0.3190, 0.0810], 'C_initial': 0.0910, 'C_limits': [-0.0590, 0.2410], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '11')] = {'B_initial': -0.2925, 'B_limits': [-0.4925, -0.0925], 'C_initial': -0.0197, 'C_limits': [-0.1697, 0.1303], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
