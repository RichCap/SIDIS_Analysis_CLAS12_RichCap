# Run-local guide for dcfid_loose_el Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1778, 'B_limits': [-0.3778, 0.0222], 'C_initial': -0.0125, 'C_limits': [-0.1625, 0.1375], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2671, 'B_limits': [-0.4671, -0.0671], 'C_initial': -0.0314, 'C_limits': [-0.1814, 0.1186], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2736, 'B_limits': [-0.4736, -0.0736], 'C_initial': 0.0102, 'C_limits': [-0.1398, 0.1602], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1385, 'B_limits': [-0.3385, 0.0615], 'C_initial': -0.0205, 'C_limits': [-0.1705, 0.1295], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3035, 'B_limits': [-0.5035, -0.1035], 'C_initial': -0.0175, 'C_limits': [-0.1675, 0.1325], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2458, 'B_limits': [-0.4458, -0.0458], 'C_initial': 0.0466, 'C_limits': [-0.1034, 0.1966], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3350, 'B_limits': [-0.5350, -0.1350], 'C_initial': 0.0635, 'C_limits': [-0.0865, 0.2135], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0629, 'B_limits': [-0.2629, 0.1371], 'C_initial': 0.0204, 'C_limits': [-0.1296, 0.1704], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2778, 'B_limits': [-0.4778, -0.0778], 'C_initial': 0.0219, 'C_limits': [-0.1281, 0.1719], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1310, 'B_limits': [-0.3310, 0.0690], 'C_initial': 0.0007, 'C_limits': [-0.1493, 0.1507], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0939, 'B_limits': [-0.2939, 0.1061], 'C_initial': -0.0130, 'C_limits': [-0.1630, 0.1370], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0102, 'B_limits': [-0.1898, 0.2102], 'C_initial': 0.0544, 'C_limits': [-0.0956, 0.2044], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1710, 'B_limits': [-0.3710, 0.0290], 'C_initial': 0.0129, 'C_limits': [-0.1371, 0.1629], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4431, 'B_limits': [-0.6431, -0.2431], 'C_initial': 0.1109, 'C_limits': [-0.0391, 0.2609], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2495, 'B_limits': [-0.4495, -0.0495], 'C_initial': 0.0715, 'C_limits': [-0.0785, 0.2215], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2834, 'B_limits': [-0.4834, -0.0834], 'C_initial': 0.0648, 'C_limits': [-0.0852, 0.2148], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1002, 'B_limits': [-0.3002, 0.0998], 'C_initial': -0.0111, 'C_limits': [-0.1611, 0.1389], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3668, 'B_limits': [-0.5668, -0.1668], 'C_initial': 0.1062, 'C_limits': [-0.0438, 0.2562], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0366, 'B_limits': [-0.2366, 0.1634], 'C_initial': 0.0339, 'C_limits': [-0.1161, 0.1839], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3089, 'B_limits': [-0.5089, -0.1089], 'C_initial': 0.1055, 'C_limits': [-0.0445, 0.2555], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0309, 'B_limits': [-0.2309, 0.1691], 'C_initial': 0.0402, 'C_limits': [-0.1098, 0.1902], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2660, 'B_limits': [-0.4660, -0.0660], 'C_initial': 0.0732, 'C_limits': [-0.0768, 0.2232], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
