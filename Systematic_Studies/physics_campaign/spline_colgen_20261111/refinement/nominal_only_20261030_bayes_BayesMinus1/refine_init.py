# Run-local guide for nominal_only_20261030 BayesMinus1. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2664, 'B_limits': [-0.4664, -0.0664], 'C_initial': -0.0311, 'C_limits': [-0.1811, 0.1189], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1758, 'B_limits': [-0.3758, 0.0242], 'C_initial': -0.0129, 'C_limits': [-0.1629, 0.1371], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2738, 'B_limits': [-0.4738, -0.0738], 'C_initial': 0.0109, 'C_limits': [-0.1391, 0.1609], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1362, 'B_limits': [-0.3362, 0.0638], 'C_initial': -0.0222, 'C_limits': [-0.1722, 0.1278], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3034, 'B_limits': [-0.5034, -0.1034], 'C_initial': -0.0170, 'C_limits': [-0.1670, 0.1330], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2444, 'B_limits': [-0.4444, -0.0444], 'C_initial': 0.0477, 'C_limits': [-0.1023, 0.1977], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3360, 'B_limits': [-0.5360, -0.1360], 'C_initial': 0.0634, 'C_limits': [-0.0866, 0.2134], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2776, 'B_limits': [-0.4776, -0.0776], 'C_initial': 0.0219, 'C_limits': [-0.1281, 0.1719], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2443, 'B_limits': [-0.4443, -0.0443], 'C_initial': 0.0695, 'C_limits': [-0.0805, 0.2195], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2832, 'B_limits': [-0.4832, -0.0832], 'C_initial': 0.0650, 'C_limits': [-0.0850, 0.2150], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1006, 'B_limits': [-0.3006, 0.0994], 'C_initial': -0.0100, 'C_limits': [-0.1600, 0.1400], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3085, 'B_limits': [-0.5085, -0.1085], 'C_initial': 0.1051, 'C_limits': [-0.0449, 0.2551], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4427, 'B_limits': [-0.6427, -0.2427], 'C_initial': 0.1105, 'C_limits': [-0.0395, 0.2605], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1698, 'B_limits': [-0.3698, 0.0302], 'C_initial': 0.0126, 'C_limits': [-0.1374, 0.1626], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0627, 'B_limits': [-0.2627, 0.1373], 'C_initial': 0.0204, 'C_limits': [-0.1296, 0.1704], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0100, 'B_limits': [-0.1900, 0.2100], 'C_initial': 0.0540, 'C_limits': [-0.0960, 0.2040], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1323, 'B_limits': [-0.3323, 0.0677], 'C_initial': 0.0013, 'C_limits': [-0.1487, 0.1513], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0284, 'B_limits': [-0.2284, 0.1716], 'C_initial': 0.0382, 'C_limits': [-0.1118, 0.1882], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0311, 'B_limits': [-0.2311, 0.1689], 'C_initial': 0.0407, 'C_limits': [-0.1093, 0.1907], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
