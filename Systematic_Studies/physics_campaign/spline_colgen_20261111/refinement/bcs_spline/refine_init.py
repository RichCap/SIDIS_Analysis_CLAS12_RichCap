# BC_RC_Bayesian guide for the spline bin-centering cache. The shared spline initializer is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location('spline_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py')
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Spline-BC histograms whose stored cosine missed the points. Untagged None limits or a one-sided C window.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.2198, 'B_limits': [-0.34, -0.10], 'C_initial': -0.0403, 'C_limits': [-0.14, 0.06], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.1156, 'B_limits': [-0.24, 0.00], 'C_initial': -0.0205, 'C_limits': [-0.12, 0.08], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.2754, 'B_limits': [-0.40, -0.15], 'C_initial': 0.0469, 'C_limits': [-0.05, 0.15], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D', 'BC')] = {'B_initial': -0.0834, 'B_limits': [-0.20, 0.04], 'C_initial': -0.0295, 'C_limits': [-0.13, 0.07], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.2026, 'B_limits': [-0.32, -0.08], 'C_initial': -0.0058, 'C_limits': [-0.11, 0.09], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'BC')] = {'B_initial': -0.2505, 'B_limits': [-0.37, -0.13], 'C_initial': -0.0295, 'C_limits': [-0.13, 0.07], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.1712, 'B_limits': [-0.30, -0.05], 'C_initial': 0.0591, 'C_limits': [-0.04, 0.16], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'BC')] = {'B_initial': 0.0337, 'B_limits': [-0.09, 0.15], 'C_initial': 0.0157, 'C_limits': [-0.08, 0.12], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.0297, 'B_limits': [-0.09, 0.15], 'C_initial': 0.0509, 'C_limits': [-0.05, 0.15], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.0224, 'B_limits': [-0.12, 0.08], 'C_initial': -0.0277, 'C_limits': [-0.13, 0.07], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.1834, 'B_limits': [-0.30, -0.06], 'C_initial': 0.0475, 'C_limits': [-0.05, 0.15], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '5', '3D', 'BC')] = {'B_initial': -0.1870, 'B_limits': [-0.31, -0.07], 'C_initial': -0.0155, 'C_limits': [-0.12, 0.08], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0547, 'B_limits': [-0.07, 0.18], 'C_initial': 0.0112, 'C_limits': [-0.08, 0.10], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7', '3D', 'BC')] = {'B_initial': -0.0160, 'B_limits': [-0.12, 0.08], 'C_initial': 0.0396, 'C_limits': [-0.06, 0.14], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
