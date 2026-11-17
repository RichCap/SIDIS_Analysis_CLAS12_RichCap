# Run-local guide for sub_pt_7 BC_RC_Bayesian. Shared manual and spline files are not edited.
# Spline untagged B/C windows are tight enough to pin fits, so this guide starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# sub_pt_7 histograms whose stored cosine missed the points. Untagged or one-sided windows.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.2298, 'B_limits': [-0.3298, -0.1298], 'C_initial': -0.0444, 'C_limits': [-0.1444, 0.0556], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'BC')] = {'B_initial': 0.0322, 'B_limits': [-0.0678, 0.1322], 'C_initial': 0.0129, 'C_limits': [-0.0871, 0.1129], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.0237, 'B_limits': [-0.1237, 0.0763], 'C_initial': -0.0261, 'C_limits': [-0.1261, 0.0739], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0557, 'B_limits': [-0.0443, 0.1557], 'C_initial': 0.0111, 'C_limits': [-0.0889, 0.1111], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
