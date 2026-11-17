# Run-local guide for sub_pt_5 BC_RC_Bayesian. Shared manual and spline files are not edited.
# Spline untagged B/C windows are tight (median width about 0.020 and 0.009), so this guide starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# sub_pt_5 histograms whose stored cosine missed the points. None-valued untagged limits, a one-sided BC window, or a negative B window that the second pass walked to its edge.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.2321, 'B_limits': [-0.3321, -0.1321], 'C_initial': -0.0453, 'C_limits': [-0.1453, 0.0547], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'BC')] = {'B_initial': 0.0314, 'B_limits': [-0.0686, 0.1314], 'C_initial': 0.0124, 'C_limits': [-0.0876, 0.1124], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.0232, 'B_limits': [-0.1232, 0.0768], 'C_initial': -0.0264, 'C_limits': [-0.1264, 0.0736], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0558, 'B_limits': [-0.0442, 0.1558], 'C_initial': 0.0112, 'C_limits': [-0.0888, 0.1112], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
