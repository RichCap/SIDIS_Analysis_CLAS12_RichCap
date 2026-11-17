# Run-local guide for sub_pt_3 BC_RC_Bayesian. Shared manual and spline files are not edited.
# Spline untagged B/C windows are tight enough to pin fits, so this guide starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# sub_pt_3 histograms whose stored cosine missed the points. Untagged None values or a one-sided BC window.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.2347, 'B_limits': [-0.3347, -0.1347], 'C_initial': -0.0456, 'C_limits': [-0.1456, 0.0544], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.0224, 'B_limits': [-0.1224, 0.0776], 'C_initial': -0.0270, 'C_limits': [-0.1270, 0.0730], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0581, 'B_limits': [-0.0419, 0.1581], 'C_initial': 0.0118, 'C_limits': [-0.0882, 0.1118], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
