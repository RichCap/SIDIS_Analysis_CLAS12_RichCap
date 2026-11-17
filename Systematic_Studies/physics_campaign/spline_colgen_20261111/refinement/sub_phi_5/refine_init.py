# Run-local guide for sub_phi_5 BC_RC_Bayesian. The shared manual file is not edited.
# Spline B/C windows are tight (median width about 0.013), so this pass starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Histogram misses versus a wide cosine. (1,4) overlaps and is not overridden.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.224022, 'B_limits': [-0.324022, -0.124022], 'C_initial': -0.044460, 'C_limits': [-0.144460, 0.055540], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.205302, 'B_limits': [-0.305302, -0.105302], 'C_initial': -0.005643, 'C_limits': [-0.105643, 0.094357], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.116222, 'B_limits': [-0.216222, -0.016222], 'C_initial': -0.019382, 'C_limits': [-0.119382, 0.080618], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.269491, 'B_limits': [-0.369491, -0.169491], 'C_initial': 0.046082, 'C_limits': [-0.053918, 0.146082], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'BC')] = {'B_initial': -0.250587, 'B_limits': [-0.350587, -0.150587], 'C_initial': -0.030016, 'C_limits': [-0.130016, 0.069984], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.174708, 'B_limits': [-0.274708, -0.074708], 'C_initial': 0.061989, 'C_limits': [-0.038011, 0.161989], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D', 'BC')] = {'B_initial': -0.083315, 'B_limits': [-0.183315, 0.016685], 'C_initial': -0.026991, 'C_limits': [-0.126991, 0.073009], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'BC')] = {'B_initial': 0.031366, 'B_limits': [-0.068634, 0.131366], 'C_initial': 0.015357, 'C_limits': [-0.084643, 0.115357], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.028886, 'B_limits': [-0.071114, 0.128886], 'C_initial': 0.051996, 'C_limits': [-0.048004, 0.151996], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.185830, 'B_limits': [-0.285830, -0.085830], 'C_initial': 0.049487, 'C_limits': [-0.050513, 0.149487], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.023640, 'B_limits': [-0.123640, 0.076360], 'C_initial': -0.026348, 'C_limits': [-0.126348, 0.073652], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '5', '3D', 'BC')] = {'B_initial': -0.183970, 'B_limits': [-0.283970, -0.083970], 'C_initial': -0.015902, 'C_limits': [-0.115902, 0.084098], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.050884, 'B_limits': [-0.049116, 0.150884], 'C_initial': 0.009955, 'C_limits': [-0.090045, 0.109955], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7', '3D', 'BC')] = {'B_initial': -0.013725, 'B_limits': [-0.113725, 0.086275], 'C_initial': 0.039510, 'C_limits': [-0.060490, 0.139510], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
