# BC_RC_Bayesian guide for spline. The shared spline initializer is not edited.
# Only bins whose stored curve missed the histogram cosine are overridden.
import importlib.util
spec = importlib.util.spec_from_file_location('spline_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py')
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.22470706, 'B_limits': [-0.34470706, -0.10470706], 'C_initial': -0.03999661, 'C_limits': [-0.11999661, 0.04000339], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.20841643, 'B_limits': [-0.32841643, -0.08841643], 'C_initial': 0.08771279, 'C_limits': [0.00771279, 0.16771279], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '2', '3D', 'BC')] = {'B_initial': -0.10099189, 'B_limits': [-0.22099189, 0.01900811], 'C_initial': 0.04324641, 'C_limits': [-0.03675359, 0.12324641], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33', '3D', 'BC')] = {'B_initial': -0.06393631, 'B_limits': [-0.18393631, 0.05606369], 'C_initial': -0.09028606, 'C_limits': [-0.17028606, -0.01028606], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.20667259, 'B_limits': [-0.32667259, -0.08667259], 'C_initial': -0.00374147, 'C_limits': [-0.08374147, 0.07625853], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.23911011, 'B_limits': [-0.35911011, -0.11911011], 'C_initial': 0.04473944, 'C_limits': [-0.03526056, 0.12473944], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.15586563, 'B_limits': [-0.27586563, -0.03586563], 'C_initial': 0.03578834, 'C_limits': [-0.04421166, 0.11578834], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20', '3D', 'BC')] = {'B_initial': -0.21701390, 'B_limits': [-0.33701390, -0.09701390], 'C_initial': 0.08713289, 'C_limits': [0.00713289, 0.16713289], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.12013287, 'B_limits': [-0.24013287, -0.00013287], 'C_initial': -0.01497167, 'C_limits': [-0.09497167, 0.06502833], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}

# Column-generation BC histograms whose guide pinned C on the wrong side of zero.
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.0170, 'B_limits': [-0.1170, 0.0830], 'C_initial': -0.0250, 'C_limits': [-0.1250, 0.0750], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.0221, 'B_limits': [-0.0779, 0.1221], 'C_initial': 0.0437, 'C_limits': [-0.0563, 0.1437], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
