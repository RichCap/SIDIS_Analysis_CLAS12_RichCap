# Run-local guide for pcalvol_loose Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose first pass sat on a bad local start or a limit that excluded the histogram cosine.
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1776, 'B_limits': [-0.3776, 0.0224], 'C_initial': -0.0132, 'C_limits': [-0.1632, 0.1368], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2671, 'B_limits': [-0.4671, -0.0671], 'C_initial': -0.0314, 'C_limits': [-0.1814, 0.1186], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2736, 'B_limits': [-0.4736, -0.0736], 'C_initial': 0.0102, 'C_limits': [-0.1398, 0.1602], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1369, 'B_limits': [-0.3369, 0.0631], 'C_initial': -0.0240, 'C_limits': [-0.1740, 0.1260], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2464, 'B_limits': [-0.4464, -0.0464], 'C_initial': 0.0469, 'C_limits': [-0.1031, 0.1969], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3035, 'B_limits': [-0.5035, -0.1035], 'C_initial': -0.0175, 'C_limits': [-0.1675, 0.1325], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '2')] = {'B_initial': -0.1516, 'B_limits': [-0.3516, 0.0484], 'C_initial': 0.0156, 'C_limits': [-0.1344, 0.1656], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3350, 'B_limits': [-0.5350, -0.1350], 'C_initial': 0.0635, 'C_limits': [-0.0865, 0.2135], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33')] = {'B_initial': -0.1111, 'B_limits': [-0.3111, 0.0889], 'C_initial': -0.0828, 'C_limits': [-0.2328, 0.0672], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '7')] = {'B_initial': -0.0524, 'B_limits': [-0.2524, 0.1476], 'C_initial': 0.0297, 'C_limits': [-0.1203, 0.1797], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0629, 'B_limits': [-0.2629, 0.1371], 'C_initial': 0.0204, 'C_limits': [-0.1296, 0.1704], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2778, 'B_limits': [-0.4778, -0.0778], 'C_initial': 0.0219, 'C_limits': [-0.1281, 0.1719], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1310, 'B_limits': [-0.3310, 0.0690], 'C_initial': 0.0007, 'C_limits': [-0.1493, 0.1507], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0940, 'B_limits': [-0.2940, 0.1060], 'C_initial': -0.0130, 'C_limits': [-0.1630, 0.1370], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0102, 'B_limits': [-0.1898, 0.2102], 'C_initial': 0.0544, 'C_limits': [-0.0956, 0.2044], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1711, 'B_limits': [-0.3711, 0.0289], 'C_initial': 0.0129, 'C_limits': [-0.1371, 0.1629], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4431, 'B_limits': [-0.6431, -0.2431], 'C_initial': 0.1109, 'C_limits': [-0.0391, 0.2609], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2478, 'B_limits': [-0.4478, -0.0478], 'C_initial': 0.0716, 'C_limits': [-0.0784, 0.2216], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1002, 'B_limits': [-0.3002, 0.0998], 'C_initial': -0.0111, 'C_limits': [-0.1611, 0.1389], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3668, 'B_limits': [-0.5668, -0.1668], 'C_initial': 0.1062, 'C_limits': [-0.0438, 0.2562], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0327, 'B_limits': [-0.2327, 0.1673], 'C_initial': 0.0361, 'C_limits': [-0.1139, 0.1861], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2831, 'B_limits': [-0.4831, -0.0831], 'C_initial': 0.0649, 'C_limits': [-0.0851, 0.2149], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17')] = {'B_initial': -0.0727, 'B_limits': [-0.2727, 0.1273], 'C_initial': -0.0226, 'C_limits': [-0.1726, 0.1274], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0310, 'B_limits': [-0.2310, 0.1690], 'C_initial': 0.0403, 'C_limits': [-0.1097, 0.1903], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
