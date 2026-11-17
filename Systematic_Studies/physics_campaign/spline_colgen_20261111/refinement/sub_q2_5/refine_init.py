# Run-local guide for sub_q2_5 BC_RC_Bayesian. Shared manual and spline files are not edited.
# BC_RC selects BC then untagged keys. The spline file's selected limits are mostly None, not a usable window, so this pass starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Histogram misses versus a wide cosine. Pinned or one-sided windows that the points do not support were left unchanged.
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.175600, 'B_limits': [-0.275600, -0.075600], 'C_initial': 0.066700, 'C_limits': [-0.033300, 0.166700], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.027000, 'B_limits': [-0.073000, 0.127000], 'C_initial': 0.052800, 'C_limits': [-0.047200, 0.152800], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.057400, 'B_limits': [-0.042600, 0.157400], 'C_initial': 0.012100, 'C_limits': [-0.087900, 0.112100], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
