# Run-local guide for nominal_only_20261030 BayesPlus1 Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
# (1, 17) was left: the stored and wide curves overlap and the stored fit already follows the points.
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1791, 'B_limits': [-0.3791, 0.0209], 'C_initial': -0.0122, 'C_limits': [-0.1622, 0.1378], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2675, 'B_limits': [-0.4675, -0.0675], 'C_initial': -0.0315, 'C_limits': [-0.1815, 0.1185], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2736, 'B_limits': [-0.4736, -0.0736], 'C_initial': 0.0098, 'C_limits': [-0.1402, 0.1598], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1396, 'B_limits': [-0.3396, 0.0604], 'C_initial': -0.0196, 'C_limits': [-0.1696, 0.1304], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2467, 'B_limits': [-0.4467, -0.0467], 'C_initial': 0.0459, 'C_limits': [-0.1041, 0.1959], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3035, 'B_limits': [-0.5035, -0.1035], 'C_initial': -0.0177, 'C_limits': [-0.1677, 0.1323], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3344, 'B_limits': [-0.5344, -0.1344], 'C_initial': 0.0634, 'C_limits': [-0.0866, 0.2134], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0630, 'B_limits': [-0.2630, 0.1370], 'C_initial': 0.0204, 'C_limits': [-0.1296, 0.1704], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1304, 'B_limits': [-0.3304, 0.0696], 'C_initial': 0.0004, 'C_limits': [-0.1496, 0.1504], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0947, 'B_limits': [-0.2947, 0.1053], 'C_initial': -0.0122, 'C_limits': [-0.1622, 0.1378], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2780, 'B_limits': [-0.4780, -0.0780], 'C_initial': 0.0218, 'C_limits': [-0.1282, 0.1718], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0103, 'B_limits': [-0.1897, 0.2103], 'C_initial': 0.0546, 'C_limits': [-0.0954, 0.2046], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4433, 'B_limits': [-0.6433, -0.2433], 'C_initial': 0.1109, 'C_limits': [-0.0391, 0.2609], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1718, 'B_limits': [-0.3718, 0.0282], 'C_initial': 0.0132, 'C_limits': [-0.1368, 0.1632], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2524, 'B_limits': [-0.4524, -0.0524], 'C_initial': 0.0726, 'C_limits': [-0.0774, 0.2226], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3669, 'B_limits': [-0.5669, -0.1669], 'C_initial': 0.1067, 'C_limits': [-0.0433, 0.2567], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2840, 'B_limits': [-0.4840, -0.0840], 'C_initial': 0.0647, 'C_limits': [-0.0853, 0.2147], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3090, 'B_limits': [-0.5090, -0.1090], 'C_initial': 0.1057, 'C_limits': [-0.0443, 0.2557], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1002, 'B_limits': [-0.3002, 0.0998], 'C_initial': -0.0117, 'C_limits': [-0.1617, 0.1383], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2655, 'B_limits': [-0.4655, -0.0655], 'C_initial': 0.0729, 'C_limits': [-0.0771, 0.2229], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
