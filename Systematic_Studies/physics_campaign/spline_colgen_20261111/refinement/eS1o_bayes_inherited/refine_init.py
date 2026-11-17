# Run-local guide for eS1o Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass-2 windows. Starts are the wide cosine on the filled phi range for bins the manual window missed.
special_fit_parameters_set[('6', '23')] = {'B_initial': -0.2358, 'B_limits': [-0.4358, -0.0358], 'C_initial': 0.0332, 'C_limits': [-0.1168, 0.1832], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2378, 'B_limits': [-0.4378, -0.0378], 'C_initial': 0.0835, 'C_limits': [-0.0665, 0.2335], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '3')] = {'B_initial': -0.2211, 'B_limits': [-0.4211, -0.0211], 'C_initial': 0.1081, 'C_limits': [-0.0419, 0.2581], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '6')] = {'B_initial': -0.4250, 'B_limits': [-0.6250, -0.2250], 'C_initial': -0.0466, 'C_limits': [-0.1966, 0.1034], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9')] = {'B_initial': 0.3377, 'B_limits': [0.1377, 0.5377], 'C_initial': 0.1433, 'C_limits': [-0.0067, 0.2933], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.1871, 'B_limits': [-0.3871, 0.0129], 'C_initial': 0.0195, 'C_limits': [-0.1305, 0.1695], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '12')] = {'B_initial': -0.3355, 'B_limits': [-0.5355, -0.1355], 'C_initial': 0.0962, 'C_limits': [-0.0538, 0.2462], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '4')] = {'B_initial': -0.0882, 'B_limits': [-0.2882, 0.1118], 'C_initial': 0.1224, 'C_limits': [-0.0276, 0.2724], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17')] = {'B_initial': -0.1542, 'B_limits': [-0.3542, 0.0458], 'C_initial': -0.0869, 'C_limits': [-0.2369, 0.0631], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '14')] = {'B_initial': 0.1645, 'B_limits': [-0.0355, 0.3645], 'C_initial': 0.1222, 'C_limits': [-0.0278, 0.2722], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '25')] = {'B_initial': 0.2430, 'B_limits': [0.0430, 0.4430], 'C_initial': 0.1422, 'C_limits': [-0.0078, 0.2922], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '17')] = {'B_initial': -0.2353, 'B_limits': [-0.4353, -0.0353], 'C_initial': 0.0127, 'C_limits': [-0.1373, 0.1627], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '32')] = {'B_initial': -0.2113, 'B_limits': [-0.4113, -0.0113], 'C_initial': -0.0399, 'C_limits': [-0.1899, 0.1101], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '21')] = {'B_initial': -0.1009, 'B_limits': [-0.3009, 0.0991], 'C_initial': -0.0359, 'C_limits': [-0.1859, 0.1141], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '8')] = {'B_initial': -0.1200, 'B_limits': [-0.3200, 0.0800], 'C_initial': -0.0103, 'C_limits': [-0.1603, 0.1397], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
