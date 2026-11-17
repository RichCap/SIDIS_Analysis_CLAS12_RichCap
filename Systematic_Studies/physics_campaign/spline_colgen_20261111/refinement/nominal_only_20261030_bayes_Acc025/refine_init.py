# Run-local guide for nominal_only_20261030 Acc025 Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
# (1, 17) was left: the stored and wide curves overlap and the stored fit already follows the points.
special_fit_parameters_set[('11', '9')] = {'B_initial': -0.1933, 'B_limits': [-0.3933, 0.0067], 'C_initial': -0.0064, 'C_limits': [-0.1564, 0.1436], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1776, 'B_limits': [-0.3776, 0.0224], 'C_initial': -0.0126, 'C_limits': [-0.1626, 0.1374], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2671, 'B_limits': [-0.4671, -0.0671], 'C_initial': -0.0314, 'C_limits': [-0.1814, 0.1186], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2736, 'B_limits': [-0.4736, -0.0736], 'C_initial': 0.0103, 'C_limits': [-0.1397, 0.1603], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2733, 'B_limits': [-0.4733, -0.0733], 'C_initial': 0.0572, 'C_limits': [-0.0928, 0.2072], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3035, 'B_limits': [-0.5035, -0.1035], 'C_initial': -0.0175, 'C_limits': [-0.1675, 0.1325], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2458, 'B_limits': [-0.4458, -0.0458], 'C_initial': 0.0466, 'C_limits': [-0.1034, 0.1966], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3350, 'B_limits': [-0.5350, -0.1350], 'C_initial': 0.0635, 'C_limits': [-0.0865, 0.2135], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2776, 'B_limits': [-0.4776, -0.0776], 'C_initial': 0.0221, 'C_limits': [-0.1279, 0.1721], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0939, 'B_limits': [-0.2939, 0.1061], 'C_initial': -0.0130, 'C_limits': [-0.1630, 0.1370], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0102, 'B_limits': [-0.1898, 0.2102], 'C_initial': 0.0544, 'C_limits': [-0.0956, 0.2044], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1710, 'B_limits': [-0.3710, 0.0290], 'C_initial': 0.0130, 'C_limits': [-0.1370, 0.1630], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1311, 'B_limits': [-0.3311, 0.0689], 'C_initial': 0.0008, 'C_limits': [-0.1492, 0.1508], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4431, 'B_limits': [-0.6431, -0.2431], 'C_initial': 0.1109, 'C_limits': [-0.0391, 0.2609], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2495, 'B_limits': [-0.4495, -0.0495], 'C_initial': 0.0720, 'C_limits': [-0.0780, 0.2220], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3668, 'B_limits': [-0.5668, -0.1668], 'C_initial': 0.1062, 'C_limits': [-0.0438, 0.2562], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0365, 'B_limits': [-0.2365, 0.1635], 'C_initial': 0.0339, 'C_limits': [-0.1161, 0.1839], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3089, 'B_limits': [-0.5089, -0.1089], 'C_initial': 0.1055, 'C_limits': [-0.0445, 0.2555], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '3')] = {'B_initial': -0.1673, 'B_limits': [-0.3673, 0.0327], 'C_initial': 0.0232, 'C_limits': [-0.1268, 0.1732], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
