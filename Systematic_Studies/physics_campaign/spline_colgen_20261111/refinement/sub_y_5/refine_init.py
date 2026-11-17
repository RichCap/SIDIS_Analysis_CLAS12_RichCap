# Run-local guide for sub_y_5 BC_RC_Bayesian. Shared manual and spline files are not edited.
# BC_RC selects BC then untagged keys. The spline file's selected limits are mostly None, not a usable window, so this pass starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Histogram misses versus a wide cosine. Pinned or one-sided windows that the points do not support were left unchanged.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.220984, 'B_limits': [-0.320984, -0.120984], 'C_initial': -0.044249, 'C_limits': [-0.144249, 0.055751], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.269096, 'B_limits': [-0.369096, -0.169096], 'C_initial': 0.045139, 'C_limits': [-0.054861, 0.145139], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'BC')] = {'B_initial': -0.247184, 'B_limits': [-0.347184, -0.147184], 'C_initial': -0.028258, 'C_limits': [-0.128258, 0.071742], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.203056, 'B_limits': [-0.303056, -0.103056], 'C_initial': -0.002634, 'C_limits': [-0.102634, 0.097366], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.175944, 'B_limits': [-0.275944, -0.075944], 'C_initial': 0.064749, 'C_limits': [-0.035251, 0.164749], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D', 'BC')] = {'B_initial': -0.084457, 'B_limits': [-0.184457, 0.015543], 'C_initial': -0.029883, 'C_limits': [-0.129883, 0.070117], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.110929, 'B_limits': [-0.210929, -0.010929], 'C_initial': -0.021119, 'C_limits': [-0.121119, 0.078881], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.025660, 'B_limits': [-0.074340, 0.125660], 'C_initial': 0.049939, 'C_limits': [-0.050061, 0.149939], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.183465, 'B_limits': [-0.283465, -0.083465], 'C_initial': 0.048266, 'C_limits': [-0.051734, 0.148266], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22', '3D', 'BC')] = {'B_initial': -0.008507, 'B_limits': [-0.108507, 0.091493], 'C_initial': 0.040799, 'C_limits': [-0.059201, 0.140799], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.056737, 'B_limits': [-0.043263, 0.156737], 'C_initial': 0.011797, 'C_limits': [-0.088203, 0.111797], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
