# Run-local guide for dcv_tight_el Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# First-pass windows sat on a bad moment or a narrow limit. Starts are the wide-fit cosine.
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2679, 'B_limits': [-0.4679, -0.0679], 'C_initial': -0.0340, 'C_limits': [-0.2340, 0.1660], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1774, 'B_limits': [-0.3774, 0.0226], 'C_initial': -0.0122, 'C_limits': [-0.2122, 0.1878], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2738, 'B_limits': [-0.4738, -0.0738], 'C_initial': 0.0091, 'C_limits': [-0.1909, 0.2091], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1373, 'B_limits': [-0.3373, 0.0627], 'C_initial': -0.0184, 'C_limits': [-0.2184, 0.1816], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3006, 'B_limits': [-0.5006, -0.1006], 'C_initial': -0.0192, 'C_limits': [-0.2192, 0.1808], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2466, 'B_limits': [-0.4466, -0.0466], 'C_initial': 0.0457, 'C_limits': [-0.1543, 0.2457], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3078, 'B_limits': [-0.5078, -0.1078], 'C_initial': 0.1053, 'C_limits': [-0.0947, 0.3053], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3315, 'B_limits': [-0.5315, -0.1315], 'C_initial': 0.0621, 'C_limits': [-0.1379, 0.2621], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2480, 'B_limits': [-0.4480, -0.0480], 'C_initial': 0.0712, 'C_limits': [-0.1288, 0.2712], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0637, 'B_limits': [-0.2637, 0.1363], 'C_initial': 0.0207, 'C_limits': [-0.1793, 0.2207], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4422, 'B_limits': [-0.6422, -0.2422], 'C_initial': 0.1109, 'C_limits': [-0.0891, 0.3109], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0910, 'B_limits': [-0.2910, 0.1090], 'C_initial': -0.0130, 'C_limits': [-0.2130, 0.1870], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2764, 'B_limits': [-0.4764, -0.0764], 'C_initial': 0.0230, 'C_limits': [-0.1770, 0.2230], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1683, 'B_limits': [-0.3683, 0.0317], 'C_initial': 0.0128, 'C_limits': [-0.1872, 0.2128], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2818, 'B_limits': [-0.4818, -0.0818], 'C_initial': 0.0627, 'C_limits': [-0.1373, 0.2627], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0093, 'B_limits': [-0.1907, 0.2093], 'C_initial': 0.0530, 'C_limits': [-0.1470, 0.2530], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '7')] = {'B_initial': -0.0518, 'B_limits': [-0.2518, 0.1482], 'C_initial': 0.0377, 'C_limits': [-0.1623, 0.2377], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1333, 'B_limits': [-0.3333, 0.0667], 'C_initial': -0.0026, 'C_limits': [-0.2026, 0.1974], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '24')] = {'B_initial': -0.1946, 'B_limits': [-0.3946, 0.0054], 'C_initial': 0.0381, 'C_limits': [-0.1619, 0.2381], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '3')] = {'B_initial': -0.1686, 'B_limits': [-0.3686, 0.0314], 'C_initial': 0.0212, 'C_limits': [-0.1788, 0.2212], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3678, 'B_limits': [-0.5678, -0.1678], 'C_initial': 0.1063, 'C_limits': [-0.0937, 0.3063], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33')] = {'B_initial': -0.1104, 'B_limits': [-0.3104, 0.0896], 'C_initial': -0.0849, 'C_limits': [-0.2849, 0.1151], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0353, 'B_limits': [-0.2353, 0.1647], 'C_initial': 0.0326, 'C_limits': [-0.1674, 0.2326], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '2')] = {'B_initial': -0.1097, 'B_limits': [-0.3097, 0.0903], 'C_initial': 0.0385, 'C_limits': [-0.1615, 0.2385], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17')] = {'B_initial': -0.0737, 'B_limits': [-0.2737, 0.1263], 'C_initial': -0.0225, 'C_limits': [-0.2225, 0.1775], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '2')] = {'B_initial': -0.1324, 'B_limits': [-0.3324, 0.0676], 'C_initial': 0.0325, 'C_limits': [-0.1675, 0.2325], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '4')] = {'B_initial': -0.2378, 'B_limits': [-0.4378, -0.0378], 'C_initial': 0.0206, 'C_limits': [-0.1794, 0.2206], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2675, 'B_limits': [-0.4675, -0.0675], 'C_initial': 0.0734, 'C_limits': [-0.1266, 0.2734], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0293, 'B_limits': [-0.2293, 0.1707], 'C_initial': 0.0435, 'C_limits': [-0.1565, 0.2435], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('12', '24')] = {'B_initial': -0.1084, 'B_limits': [-0.3084, 0.0916], 'C_initial': -0.0203, 'C_limits': [-0.2203, 0.1797], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '3')] = {'B_initial': -0.1754, 'B_limits': [-0.3754, 0.0246], 'C_initial': 0.0144, 'C_limits': [-0.1856, 0.2144], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '3')] = {'B_initial': -0.2087, 'B_limits': [-0.4087, -0.0087], 'C_initial': 0.0133, 'C_limits': [-0.1867, 0.2133], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16')] = {'B_initial': -0.0054, 'B_limits': [-0.2054, 0.1946], 'C_initial': 0.0158, 'C_limits': [-0.1842, 0.2158], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '9')] = {'B_initial': -0.1998, 'B_limits': [-0.3998, 0.0002], 'C_initial': -0.0056, 'C_limits': [-0.2056, 0.1944], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '29')] = {'B_initial': -0.2216, 'B_limits': [-0.4216, -0.0216], 'C_initial': 0.0545, 'C_limits': [-0.1455, 0.2545], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}

# Second pass still stopped on the expanded C limit.
special_fit_parameters_set[('6', '6')] = {'B_initial': -0.3953, 'B_limits': [-0.5953, -0.1953], 'C_initial': 0.0704, 'C_limits': [-0.1296, 0.2704], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
