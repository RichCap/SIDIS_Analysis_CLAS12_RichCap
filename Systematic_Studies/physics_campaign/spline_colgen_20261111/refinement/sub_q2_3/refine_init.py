# Run-local guide for sub_q2_3 BC_RC_Bayesian. Shared manual and spline files are not edited.
# Spline B/C windows have median widths 0.020 and 0.009, tight enough to pin fits, so this guide starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# sub_q2_3 histograms whose stored cosine missed the points. One-sided windows or a second-pass shrink.
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.0274, 'B_limits': [-0.0726, 0.1274], 'C_initial': 0.0523, 'C_limits': [-0.0477, 0.1523], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0592, 'B_limits': [-0.0408, 0.1592], 'C_initial': 0.0130, 'C_limits': [-0.0870, 0.1130], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.1764, 'B_limits': [-0.2764, -0.0764], 'C_initial': 0.0671, 'C_limits': [-0.0329, 0.1671], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.1842, 'B_limits': [-0.2842, -0.0842], 'C_initial': 0.0518, 'C_limits': [-0.0482, 0.1518], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D', 'BC')] = {'B_initial': -0.0838, 'B_limits': [-0.1838, 0.0162], 'C_initial': -0.0307, 'C_limits': [-0.1307, 0.0693], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22', '3D', 'BC')] = {'B_initial': -0.0017, 'B_limits': [-0.1017, 0.0983], 'C_initial': 0.0443, 'C_limits': [-0.0557, 0.1443], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'BC')] = {'B_initial': 0.0157, 'B_limits': [-0.0843, 0.1157], 'C_initial': 0.0012, 'C_limits': [-0.0988, 0.1012], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1', '3D', 'BC')] = {'B_initial': -0.0473, 'B_limits': [-0.1473, 0.0527], 'C_initial': 0.0318, 'C_limits': [-0.0682, 0.1318], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
