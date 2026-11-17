# Run-local guide for no_pip_testdc Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2708, 'B_limits': [-0.4708, -0.0708], 'C_initial': 0.0122, 'C_limits': [-0.1378, 0.1622], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.2930, 'B_limits': [-0.4930, -0.0930], 'C_initial': -0.0093, 'C_limits': [-0.1593, 0.1407], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3115, 'B_limits': [-0.5115, -0.1115], 'C_initial': 0.1023, 'C_limits': [-0.0477, 0.2523], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '2')] = {'B_initial': -0.1562, 'B_limits': [-0.3562, 0.0438], 'C_initial': 0.0271, 'C_limits': [-0.1229, 0.1771], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '15')] = {'B_initial': -0.1085, 'B_limits': [-0.3085, 0.0915], 'C_initial': -0.0031, 'C_limits': [-0.1531, 0.1469], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '3')] = {'B_initial': -0.1593, 'B_limits': [-0.3593, 0.0407], 'C_initial': -0.0078, 'C_limits': [-0.1578, 0.1422], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '16')] = {'B_initial': -0.1687, 'B_limits': [-0.3687, 0.0313], 'C_initial': 0.0054, 'C_limits': [-0.1446, 0.1554], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4445, 'B_limits': [-0.6445, -0.2445], 'C_initial': 0.1090, 'C_limits': [-0.0410, 0.2590], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '2')] = {'B_initial': -0.1260, 'B_limits': [-0.3260, 0.0740], 'C_initial': 0.0204, 'C_limits': [-0.1296, 0.1704], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '24')] = {'B_initial': -0.0503, 'B_limits': [-0.2503, 0.1497], 'C_initial': -0.0732, 'C_limits': [-0.2232, 0.0768], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3667, 'B_limits': [-0.5667, -0.1667], 'C_initial': 0.1083, 'C_limits': [-0.0417, 0.2583], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1099, 'B_limits': [-0.3099, 0.0901], 'C_initial': -0.0192, 'C_limits': [-0.1692, 0.1308], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1668, 'B_limits': [-0.3668, 0.0332], 'C_initial': 0.0120, 'C_limits': [-0.1380, 0.1620], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.2876, 'B_limits': [-0.4876, -0.0876], 'C_initial': 0.0181, 'C_limits': [-0.1319, 0.1681], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': -0.0183, 'B_limits': [-0.2183, 0.1817], 'C_initial': 0.0438, 'C_limits': [-0.1062, 0.1938], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.1026, 'B_limits': [-0.3026, 0.0974], 'C_initial': -0.0240, 'C_limits': [-0.1740, 0.1260], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '9')] = {'B_initial': -0.2038, 'B_limits': [-0.4038, -0.0038], 'C_initial': -0.0132, 'C_limits': [-0.1632, 0.1368], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0292, 'B_limits': [-0.2292, 0.1708], 'C_initial': 0.0528, 'C_limits': [-0.0972, 0.2028], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '4')] = {'B_initial': -0.2438, 'B_limits': [-0.4438, -0.0438], 'C_initial': -0.0399, 'C_limits': [-0.1899, 0.1101], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '24')] = {'B_initial': -0.0624, 'B_limits': [-0.2624, 0.1376], 'C_initial': -0.0525, 'C_limits': [-0.2025, 0.0975], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '1')] = {'B_initial': -0.0725, 'B_limits': [-0.2725, 0.1275], 'C_initial': 0.0339, 'C_limits': [-0.1161, 0.1839], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
