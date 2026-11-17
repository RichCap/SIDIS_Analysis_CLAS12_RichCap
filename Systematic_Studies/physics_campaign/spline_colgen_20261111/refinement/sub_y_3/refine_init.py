# Run-local guide for sub_y_3 BC_RC_Bayesian. Shared manual and spline files are not edited.
# Spline selection for BC_RC falls through to untagged keys. Most of those B/C limits are [None, None], and the few tagged BC windows include a one-sided width of 0.02. This guide starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Histogram misses versus a wide cosine. None-valued limits, a negative-only C window, a C window capped at 0, or the one-sided ('1','9','BC') window.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.2219, 'B_limits': [-0.3219, -0.1219], 'C_initial': -0.0444, 'C_limits': [-0.1444, 0.0556], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.2690, 'B_limits': [-0.3690, -0.1690], 'C_initial': 0.0452, 'C_limits': [-0.0548, 0.1452], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'BC')] = {'B_initial': -0.2473, 'B_limits': [-0.3473, -0.1473], 'C_initial': -0.0287, 'C_limits': [-0.1287, 0.0713], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.0266, 'B_limits': [-0.0734, 0.1266], 'C_initial': 0.0511, 'C_limits': [-0.0489, 0.1511], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0574, 'B_limits': [-0.0426, 0.1574], 'C_initial': 0.0115, 'C_limits': [-0.0885, 0.1115], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
