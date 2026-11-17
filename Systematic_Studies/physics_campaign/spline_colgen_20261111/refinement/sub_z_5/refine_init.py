# Run-local guide for sub_z_5 BC_RC_Bayesian. Shared manual and spline files are not edited.
# BC_RC selects ('q','z','3D','BC'), then ('q','z','BC'), then untagged ('q','z').
# The spline file resolves 393 of 503 pairs to None limits and 87 to windows narrower than 0.15, so this pass starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Histogram misses versus a wide cosine. The one-sided C windows and the collapsed second pass were opened only for those bins.
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.180357, 'B_limits': [-0.280357, -0.080357], 'C_initial': 0.072236, 'C_limits': [-0.027764, 0.172236], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.186466, 'B_limits': [-0.286466, -0.086466], 'C_initial': 0.051089, 'C_limits': [-0.048911, 0.151089], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.026617, 'B_limits': [-0.073383, 0.126617], 'C_initial': 0.050933, 'C_limits': [-0.049067, 0.150933], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
