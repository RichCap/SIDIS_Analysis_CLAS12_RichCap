# Run-local guide for eS2o Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 1 was trapped by a narrow guide or a collapsed moment window. Starts are the wide-fit cosine.
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3572, 'B_limits': [-0.5572, -0.1572], 'C_initial': 0.0888, 'C_limits': [-0.1112, 0.2888], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '19')] = {'B_initial': -0.2152, 'B_limits': [-0.4152, -0.0152], 'C_initial': 0.0288, 'C_limits': [-0.1712, 0.2288], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2022, 'B_limits': [-0.4022, -0.0022], 'C_initial': 0.0435, 'C_limits': [-0.1565, 0.2435], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '11')] = {'B_initial': -0.2932, 'B_limits': [-0.4932, -0.0932], 'C_initial': 0.0270, 'C_limits': [-0.173, 0.227], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '22')] = {'B_initial': -0.2481, 'B_limits': [-0.4481, -0.0481], 'C_initial': 0.0495, 'C_limits': [-0.1505, 0.2495], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '17')] = {'B_initial': -0.2576, 'B_limits': [-0.4576, -0.0576], 'C_initial': -0.0022, 'C_limits': [-0.2022, 0.1978], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '9')] = {'B_initial': -0.1837, 'B_limits': [-0.3837, 0.0163], 'C_initial': 0.0141, 'C_limits': [-0.1859, 0.2141], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '34')] = {'B_initial': -0.1608, 'B_limits': [-0.3608, 0.0392], 'C_initial': -0.0245, 'C_limits': [-0.2245, 0.1755], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '13')] = {'B_initial': -0.0455, 'B_limits': [-0.2455, 0.1545], 'C_initial': 0.1888, 'C_limits': [-0.0112, 0.3888], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '20')] = {'B_initial': -0.1938, 'B_limits': [-0.3938, 0.0062], 'C_initial': -0.0283, 'C_limits': [-0.2283, 0.1717], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '14')] = {'B_initial': 0.1504, 'B_limits': [-0.0496, 0.3504], 'C_initial': 0.1383, 'C_limits': [-0.0617, 0.3383], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '21')] = {'B_initial': -0.0865, 'B_limits': [-0.2865, 0.1135], 'C_initial': 0.0526, 'C_limits': [-0.1474, 0.2526], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
