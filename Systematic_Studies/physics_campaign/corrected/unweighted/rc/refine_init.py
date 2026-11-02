# RC_Bayesian guide for unweighted. The shared manual initializer is not edited.
# Only bins whose stored curve missed the histogram cosine are overridden.
import importlib.util
spec = importlib.util.spec_from_file_location('manual_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py')
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)
special_fit_parameters_set[('3', '16', '3D', 'RC')] = {'B_initial': -0.12279389, 'B_limits': [-0.28279389, 0.03720611], 'C_initial': -0.02024668, 'C_limits': [-0.10024668, 0.05975332], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'RC')] = {'B_initial': -0.19168642, 'B_limits': [-0.35168642, -0.03168642], 'C_initial': 0.05859250, 'C_limits': [-0.02140750, 0.13859250], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'RC')] = {'B_initial': -0.19920599, 'B_limits': [-0.35920599, -0.03920599], 'C_initial': -0.00762532, 'C_limits': [-0.08762532, 0.07237468], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20', '3D', 'RC')] = {'B_initial': -0.22060937, 'B_limits': [-0.38060937, -0.06060937], 'C_initial': 0.08474298, 'C_limits': [0.00474298, 0.16474298], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'RC')] = {'B_initial': -0.25296461, 'B_limits': [-0.41296461, -0.09296461], 'C_initial': -0.04317277, 'C_limits': [-0.12317277, 0.03682723], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'RC')] = {'B_initial': -0.26470307, 'B_limits': [-0.42470307, -0.10470307], 'C_initial': 0.05098370, 'C_limits': [-0.02901630, 0.13098370], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
