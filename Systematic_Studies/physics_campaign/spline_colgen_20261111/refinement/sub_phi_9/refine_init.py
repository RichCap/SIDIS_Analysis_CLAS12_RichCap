# BC_RC_Bayesian guide for sub_phi_9. The shared spline initializer is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("spline_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py")
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Histograms whose stored cosine missed the points. Untagged or one-sided windows.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.223324, 'B_limits': [-0.343324, -0.103324], 'C_initial': -0.043703, 'C_limits': [-0.163703, 0.076297], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.116267, 'B_limits': [-0.236267, 0.003733], 'C_initial': -0.019792, 'C_limits': [-0.139792, 0.100208], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'BC')] = {'B_initial': -0.250308, 'B_limits': [-0.370308, -0.130308], 'C_initial': -0.031237, 'C_limits': [-0.151237, 0.088763], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.205739, 'B_limits': [-0.325739, -0.085739], 'C_initial': -0.005554, 'C_limits': [-0.125554, 0.114446], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.269754, 'B_limits': [-0.389754, -0.149754], 'C_initial': 0.045409, 'C_limits': [-0.074591, 0.165409], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.173924, 'B_limits': [-0.293924, -0.053924], 'C_initial': 0.060247, 'C_limits': [-0.059753, 0.180247], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D', 'BC')] = {'B_initial': -0.083029, 'B_limits': [-0.203029, 0.036971], 'C_initial': -0.027017, 'C_limits': [-0.147017, 0.092983], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'BC')] = {'B_initial': 0.032246, 'B_limits': [-0.087754, 0.152246], 'C_initial': 0.016642, 'C_limits': [-0.103358, 0.136642], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.028876, 'B_limits': [-0.091124, 0.148876], 'C_initial': 0.051755, 'C_limits': [-0.068245, 0.171755], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.185675, 'B_limits': [-0.305675, -0.065675], 'C_initial': 0.048397, 'C_limits': [-0.071603, 0.168397], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.024369, 'B_limits': [-0.144369, 0.095631], 'C_initial': -0.027042, 'C_limits': [-0.147042, 0.092958], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '5', '3D', 'BC')] = {'B_initial': -0.186450, 'B_limits': [-0.306450, -0.066450], 'C_initial': -0.017834, 'C_limits': [-0.137834, 0.102166], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.050738, 'B_limits': [-0.069262, 0.170738], 'C_initial': 0.008505, 'C_limits': [-0.111495, 0.128505], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7', '3D', 'BC')] = {'B_initial': -0.016335, 'B_limits': [-0.136335, 0.103665], 'C_initial': 0.038409, 'C_limits': [-0.081591, 0.158409], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
