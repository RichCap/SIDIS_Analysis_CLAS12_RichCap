# Run-local guide for nominal_only_20261030 Phi12 Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
# Left because the curves overlap: (1, 17), (1, 26), (5, 3), (9, 13), (1, 16), (5, 7), (3, 8).
special_fit_parameters_set[('9', '14')] = {'B_initial': -0.5064, 'B_limits': [-0.7064, -0.3064], 'C_initial': 0.1613, 'C_limits': [0.0113, 0.3113], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '14')] = {'B_initial': -0.4751, 'B_limits': [-0.6751, -0.2751], 'C_initial': 0.1604, 'C_limits': [0.0104, 0.3104], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '18')] = {'B_initial': -0.3898, 'B_limits': [-0.5898, -0.1898], 'C_initial': 0.0980, 'C_limits': [-0.0520, 0.2480], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3296, 'B_limits': [-0.5296, -0.1296], 'C_initial': 0.0613, 'C_limits': [-0.0887, 0.2113], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2462, 'B_limits': [-0.4462, -0.0462], 'C_initial': 0.0661, 'C_limits': [-0.0839, 0.2161], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': -0.0043, 'B_limits': [-0.2043, 0.1957], 'C_initial': 0.0461, 'C_limits': [-0.1039, 0.1961], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '1')] = {'B_initial': -0.0879, 'B_limits': [-0.2879, 0.1121], 'C_initial': 0.0007, 'C_limits': [-0.1493, 0.1507], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4367, 'B_limits': [-0.6367, -0.2367], 'C_initial': 0.1115, 'C_limits': [-0.0385, 0.2615], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3609, 'B_limits': [-0.5609, -0.1609], 'C_initial': 0.1018, 'C_limits': [-0.0482, 0.2518], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2592, 'B_limits': [-0.4592, -0.0592], 'C_initial': 0.0752, 'C_limits': [-0.0748, 0.2252], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('12', '24')] = {'B_initial': -0.1123, 'B_limits': [-0.3123, 0.0877], 'C_initial': -0.0114, 'C_limits': [-0.1614, 0.1386], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '24')] = {'B_initial': -0.2048, 'B_limits': [-0.4048, -0.0048], 'C_initial': 0.0481, 'C_limits': [-0.1019, 0.1981], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '6')] = {'B_initial': -0.0261, 'B_limits': [-0.2261, 0.1739], 'C_initial': 0.0270, 'C_limits': [-0.1230, 0.1770], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
