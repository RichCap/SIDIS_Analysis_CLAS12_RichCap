# Run-local guide for nominal_only_20261030 BinByBin. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass-1 windows missed the histogram cosine. Starts are the wide fit on the filled phi range.
# Left on the wide-fit boundary: (1, 15) and (1, 8), where free B sits at -0.95.
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.7126, 'B_limits': [-0.9126, -0.5126], 'C_initial': -0.2355, 'C_limits': [-0.3855, -0.0855], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.6537, 'B_limits': [-0.8537, -0.4537], 'C_initial': -0.2810, 'C_limits': [-0.4310, -0.1310], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '15')] = {'B_initial': -0.7224, 'B_limits': [-0.9224, -0.5224], 'C_initial': -0.2389, 'C_limits': [-0.3889, -0.0889], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '12')] = {'B_initial': -0.6890, 'B_limits': [-0.8890, -0.4890], 'C_initial': -0.2979, 'C_limits': [-0.4479, -0.1479], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '29')] = {'B_initial': -0.5900, 'B_limits': [-0.7900, -0.3900], 'C_initial': -0.2427, 'C_limits': [-0.3927, -0.0927], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '25')] = {'B_initial': -0.8816, 'B_limits': [-0.9500, -0.6816], 'C_initial': -0.3455, 'C_limits': [-0.4955, -0.1955], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '26')] = {'B_initial': -0.4820, 'B_limits': [-0.6820, -0.2820], 'C_initial': -0.2222, 'C_limits': [-0.3722, -0.0722], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '19')] = {'B_initial': -0.8471, 'B_limits': [-0.9500, -0.6471], 'C_initial': -0.4776, 'C_limits': [-0.6276, -0.3276], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '31')] = {'B_initial': -0.3587, 'B_limits': [-0.5587, -0.1587], 'C_initial': -0.2005, 'C_limits': [-0.3505, -0.0505], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.7457, 'B_limits': [-0.9457, -0.5457], 'C_initial': -0.2287, 'C_limits': [-0.3787, -0.0787], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '24')] = {'B_initial': 0.5050, 'B_limits': [0.3050, 0.7050], 'C_initial': 0.1194, 'C_limits': [-0.0306, 0.2694], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '31')] = {'B_initial': -0.2573, 'B_limits': [-0.4573, -0.0573], 'C_initial': -0.2135, 'C_limits': [-0.3635, -0.0635], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '25')] = {'B_initial': -0.4101, 'B_limits': [-0.6101, -0.2101], 'C_initial': -0.2642, 'C_limits': [-0.4142, -0.1142], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('12', '24')] = {'B_initial': 0.5898, 'B_limits': [0.3898, 0.7898], 'C_initial': 0.0381, 'C_limits': [-0.1119, 0.1881], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '24')] = {'B_initial': 0.5391, 'B_limits': [0.3391, 0.7391], 'C_initial': 0.1483, 'C_limits': [-0.0017, 0.2983], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '21')] = {'B_initial': -0.3809, 'B_limits': [-0.5809, -0.1809], 'C_initial': -0.2807, 'C_limits': [-0.4307, -0.1307], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '12')] = {'B_initial': -0.5917, 'B_limits': [-0.7917, -0.3917], 'C_initial': -0.2101, 'C_limits': [-0.3601, -0.0601], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '23')] = {'B_initial': -0.2252, 'B_limits': [-0.4252, -0.0252], 'C_initial': -0.1580, 'C_limits': [-0.3080, -0.0080], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '5')] = {'B_initial': -0.0047, 'B_limits': [-0.2047, 0.1953], 'C_initial': 0.0441, 'C_limits': [-0.1059, 0.1941], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': -0.4983, 'B_limits': [-0.6983, -0.2983], 'C_initial': -0.1442, 'C_limits': [-0.2942, 0.0058], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '13')] = {'B_initial': -0.2471, 'B_limits': [-0.4471, -0.0471], 'C_initial': 0.0096, 'C_limits': [-0.1404, 0.1596], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '19')] = {'B_initial': 0.3140, 'B_limits': [0.1140, 0.5140], 'C_initial': -0.0683, 'C_limits': [-0.2183, 0.0817], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '13')] = {'B_initial': -0.5349, 'B_limits': [-0.7349, -0.3349], 'C_initial': -0.2571, 'C_limits': [-0.4071, -0.1071], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '8')] = {'B_initial': -0.2341, 'B_limits': [-0.4341, -0.0341], 'C_initial': -0.2050, 'C_limits': [-0.3550, -0.0550], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '32')] = {'B_initial': -0.2172, 'B_limits': [-0.4172, -0.0172], 'C_initial': -0.2107, 'C_limits': [-0.3607, -0.0607], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '12')] = {'B_initial': -0.2285, 'B_limits': [-0.4285, -0.0285], 'C_initial': -0.1581, 'C_limits': [-0.3081, -0.0081], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('8', '34')] = {'B_initial': 0.4435, 'B_limits': [0.2435, 0.6435], 'C_initial': -0.0453, 'C_limits': [-0.1953, 0.1047], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '14')] = {'B_initial': -0.1985, 'B_limits': [-0.3985, 0.0015], 'C_initial': -0.1773, 'C_limits': [-0.3273, -0.0273], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16')] = {'B_initial': -0.3698, 'B_limits': [-0.5698, -0.1698], 'C_initial': -0.2744, 'C_limits': [-0.4244, -0.1244], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '34')] = {'B_initial': 0.2543, 'B_limits': [0.0543, 0.4543], 'C_initial': -0.0016, 'C_limits': [-0.1516, 0.1484], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '12')] = {'B_initial': -0.1630, 'B_limits': [-0.3630, 0.0370], 'C_initial': -0.0107, 'C_limits': [-0.1607, 0.1393], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '16')] = {'B_initial': -0.4485, 'B_limits': [-0.6485, -0.2485], 'C_initial': -0.3295, 'C_limits': [-0.4795, -0.1795], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '14')] = {'B_initial': -0.1170, 'B_limits': [-0.3170, 0.0830], 'C_initial': -0.1407, 'C_limits': [-0.2907, 0.0093], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': 0.1397, 'B_limits': [-0.0603, 0.3397], 'C_initial': -0.1192, 'C_limits': [-0.2692, 0.0308], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '15')] = {'B_initial': -0.4984, 'B_limits': [-0.6984, -0.2984], 'C_initial': -0.3574, 'C_limits': [-0.5074, -0.2074], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '35')] = {'B_initial': 0.2177, 'B_limits': [0.0177, 0.4177], 'C_initial': -0.2718, 'C_limits': [-0.4218, -0.1218], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': 0.0181, 'B_limits': [-0.1819, 0.2181], 'C_initial': -0.2547, 'C_limits': [-0.4047, -0.1047], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '15')] = {'B_initial': -0.2473, 'B_limits': [-0.4473, -0.0473], 'C_initial': -0.2280, 'C_limits': [-0.3780, -0.0780], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '18')] = {'B_initial': -0.3898, 'B_limits': [-0.5898, -0.1898], 'C_initial': -0.2863, 'C_limits': [-0.4363, -0.1363], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '7')] = {'B_initial': -0.0317, 'B_limits': [-0.2317, 0.1683], 'C_initial': -0.0630, 'C_limits': [-0.2130, 0.0870], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '6')] = {'B_initial': -0.0440, 'B_limits': [-0.2440, 0.1560], 'C_initial': 0.0865, 'C_limits': [-0.0635, 0.2365], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '3')] = {'B_initial': 0.0619, 'B_limits': [-0.1381, 0.2619], 'C_initial': 0.0177, 'C_limits': [-0.1323, 0.1677], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('17', '28')] = {'B_initial': 0.3698, 'B_limits': [0.1698, 0.5698], 'C_initial': 0.0505, 'C_limits': [-0.0995, 0.2005], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '29')] = {'B_initial': 0.2687, 'B_limits': [0.0687, 0.4687], 'C_initial': -0.4483, 'C_limits': [-0.5983, -0.2983], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '6')] = {'B_initial': -0.1306, 'B_limits': [-0.3306, 0.0694], 'C_initial': 0.0746, 'C_limits': [-0.0754, 0.2246], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '29')] = {'B_initial': -0.0078, 'B_limits': [-0.2078, 0.1922], 'C_initial': -0.0733, 'C_limits': [-0.2233, 0.0767], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '28')] = {'B_initial': -0.0997, 'B_limits': [-0.2997, 0.1003], 'C_initial': 0.1334, 'C_limits': [-0.0166, 0.2834], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '29')] = {'B_initial': -0.3900, 'B_limits': [-0.5900, -0.1900], 'C_initial': -0.1156, 'C_limits': [-0.2656, 0.0344], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '11')] = {'B_initial': -0.0316, 'B_limits': [-0.2316, 0.1684], 'C_initial': 0.0428, 'C_limits': [-0.1072, 0.1928], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '10')] = {'B_initial': 0.0782, 'B_limits': [-0.1218, 0.2782], 'C_initial': -0.0076, 'C_limits': [-0.1576, 0.1424], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
