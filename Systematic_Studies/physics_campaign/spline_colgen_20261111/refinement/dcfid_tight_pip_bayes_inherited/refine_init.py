# Run-local guide for dcfid_tight_pip Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 1 sat on a narrow moment window or a tight manual limit. Starts are the wide-fit cosine.
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2677, 'B_limits': [-0.4677, -0.0677], 'C_initial': -0.0315, 'C_limits': [-0.2315, 0.1685], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '9')] = {'B_initial': -0.1917, 'B_limits': [-0.3917, 0.0083], 'C_initial': -0.0063, 'C_limits': [-0.2063, 0.1937], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1785, 'B_limits': [-0.3785, 0.0215], 'C_initial': -0.0136, 'C_limits': [-0.2136, 0.1864], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2722, 'B_limits': [-0.4722, -0.0722], 'C_initial': 0.0110, 'C_limits': [-0.1890, 0.2110], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3025, 'B_limits': [-0.5025, -0.1025], 'C_initial': -0.0172, 'C_limits': [-0.2172, 0.1828], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1390, 'B_limits': [-0.3390, 0.0610], 'C_initial': -0.0197, 'C_limits': [-0.2197, 0.1803], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2461, 'B_limits': [-0.4461, -0.0461], 'C_initial': 0.0467, 'C_limits': [-0.1533, 0.2467], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3354, 'B_limits': [-0.5354, -0.1354], 'C_initial': 0.0635, 'C_limits': [-0.1365, 0.2635], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2504, 'B_limits': [-0.4504, -0.0504], 'C_initial': 0.0713, 'C_limits': [-0.1287, 0.2713], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4428, 'B_limits': [-0.6428, -0.2428], 'C_initial': 0.1114, 'C_limits': [-0.0886, 0.3114], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2753, 'B_limits': [-0.4753, -0.0753], 'C_initial': 0.0225, 'C_limits': [-0.1775, 0.2225], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1324, 'B_limits': [-0.3324, 0.0676], 'C_initial': 0.0006, 'C_limits': [-0.1994, 0.2006], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2827, 'B_limits': [-0.4827, -0.0827], 'C_initial': 0.0649, 'C_limits': [-0.1351, 0.2649], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0919, 'B_limits': [-0.2919, 0.1081], 'C_initial': -0.0114, 'C_limits': [-0.2114, 0.1886], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0090, 'B_limits': [-0.1910, 0.2090], 'C_initial': 0.0554, 'C_limits': [-0.1446, 0.2554], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0632, 'B_limits': [-0.2632, 0.1368], 'C_initial': 0.0220, 'C_limits': [-0.1780, 0.2220], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1696, 'B_limits': [-0.3696, 0.0304], 'C_initial': 0.0145, 'C_limits': [-0.1855, 0.2145], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3668, 'B_limits': [-0.5668, -0.1668], 'C_initial': 0.1067, 'C_limits': [-0.0933, 0.3067], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0343, 'B_limits': [-0.2343, 0.1657], 'C_initial': 0.0377, 'C_limits': [-0.1623, 0.2377], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3075, 'B_limits': [-0.5075, -0.1075], 'C_initial': 0.1067, 'C_limits': [-0.0933, 0.3067], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
