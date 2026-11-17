# Run-local guide for sub_q2_7 BC_RC_Bayesian. Shared manual and spline files are not edited.
# BC_RC selects BC then untagged keys. The spline file's selected limits are mostly None, not a usable window, so this pass starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Histogram misses versus a wide cosine. One-sided windows and a near-zero second-pass trap were opened around that cosine.
special_fit_parameters_set[('1', '5', '3D', 'BC')] = {'B_initial': -0.176000, 'B_limits': [-0.276000, -0.076000], 'C_initial': -0.012900, 'C_limits': [-0.112900, 0.087100], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.056500, 'B_limits': [-0.043500, 0.156500], 'C_initial': 0.011500, 'C_limits': [-0.088500, 0.111500], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.182400, 'B_limits': [-0.282400, -0.082400], 'C_initial': 0.050200, 'C_limits': [-0.049800, 0.150200], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.174900, 'B_limits': [-0.274900, -0.074900], 'C_initial': 0.066000, 'C_limits': [-0.034000, 0.166000], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.027500, 'B_limits': [-0.072500, 0.127500], 'C_initial': 0.053500, 'C_limits': [-0.046500, 0.153500], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
