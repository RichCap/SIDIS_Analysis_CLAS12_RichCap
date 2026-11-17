# Run-local guide for ecthr_loose_el Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose first pass sat on a tight window. Starts are the wide-fit cosine. Shared files are untouched.
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2670, 'B_limits': [-0.4670, -0.0670], 'C_initial': -0.0313, 'C_limits': [-0.1813, 0.1187], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1780, 'B_limits': [-0.3780, 0.0220], 'C_initial': -0.0127, 'C_limits': [-0.1627, 0.1373], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2736, 'B_limits': [-0.4736, -0.0736], 'C_initial': 0.0099, 'C_limits': [-0.1401, 0.1599], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1386, 'B_limits': [-0.3386, 0.0614], 'C_initial': -0.0207, 'C_limits': [-0.1707, 0.1293], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3034, 'B_limits': [-0.5034, -0.1034], 'C_initial': -0.0169, 'C_limits': [-0.1669, 0.1331], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2457, 'B_limits': [-0.4457, -0.0457], 'C_initial': 0.0466, 'C_limits': [-0.1034, 0.1966], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3350, 'B_limits': [-0.5350, -0.1350], 'C_initial': 0.0628, 'C_limits': [-0.0872, 0.2128], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2491, 'B_limits': [-0.4491, -0.0491], 'C_initial': 0.0713, 'C_limits': [-0.0787, 0.2213], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2772, 'B_limits': [-0.4772, -0.0772], 'C_initial': 0.0218, 'C_limits': [-0.1282, 0.1718], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0628, 'B_limits': [-0.2628, 0.1372], 'C_initial': 0.0207, 'C_limits': [-0.1293, 0.1707], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4433, 'B_limits': [-0.6433, -0.2433], 'C_initial': 0.1107, 'C_limits': [-0.0393, 0.2607], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3091, 'B_limits': [-0.5091, -0.1091], 'C_initial': 0.1056, 'C_limits': [-0.0444, 0.2556], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1312, 'B_limits': [-0.3312, 0.0688], 'C_initial': 0.0013, 'C_limits': [-0.1487, 0.1513], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1714, 'B_limits': [-0.3714, 0.0286], 'C_initial': 0.0126, 'C_limits': [-0.1374, 0.1626], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2830, 'B_limits': [-0.4830, -0.0830], 'C_initial': 0.0645, 'C_limits': [-0.0855, 0.2145], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0936, 'B_limits': [-0.2936, 0.1064], 'C_initial': -0.0127, 'C_limits': [-0.1627, 0.1373], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0100, 'B_limits': [-0.1900, 0.2100], 'C_initial': 0.0544, 'C_limits': [-0.0956, 0.2044], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1002, 'B_limits': [-0.3002, 0.0998], 'C_initial': -0.0113, 'C_limits': [-0.1613, 0.1387], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3666, 'B_limits': [-0.5666, -0.1666], 'C_initial': 0.1067, 'C_limits': [-0.0433, 0.2567], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33')] = {'B_initial': -0.1116, 'B_limits': [-0.3116, 0.0884], 'C_initial': -0.0833, 'C_limits': [-0.2333, 0.0667], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0358, 'B_limits': [-0.2358, 0.1642], 'C_initial': 0.0345, 'C_limits': [-0.1155, 0.1845], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '2')] = {'B_initial': -0.1527, 'B_limits': [-0.3527, 0.0473], 'C_initial': 0.0231, 'C_limits': [-0.1269, 0.1731], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17')] = {'B_initial': -0.0722, 'B_limits': [-0.2722, 0.1278], 'C_initial': -0.0222, 'C_limits': [-0.1722, 0.1278], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0313, 'B_limits': [-0.2313, 0.1687], 'C_initial': 0.0404, 'C_limits': [-0.1096, 0.1904], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}

# Second-pass windows still excluded the wide-fit cosine.
special_fit_parameters_set[('1', '4')] = {'B_initial': -0.2322, 'B_limits': [-0.4322, -0.0322], 'C_initial': 0.0232, 'C_limits': [-0.1268, 0.1732], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2659, 'B_limits': [-0.4659, -0.0659], 'C_initial': 0.0732, 'C_limits': [-0.0768, 0.2232], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '2')] = {'B_initial': -0.1346, 'B_limits': [-0.3346, 0.0654], 'C_initial': 0.0309, 'C_limits': [-0.1191, 0.1809], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '7')] = {'B_initial': -0.0524, 'B_limits': [-0.2524, 0.1476], 'C_initial': 0.0380, 'C_limits': [-0.1120, 0.1880], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('12', '24')] = {'B_initial': -0.1070, 'B_limits': [-0.3070, 0.0930], 'C_initial': -0.0202, 'C_limits': [-0.1702, 0.1298], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16')] = {'B_initial': -0.0025, 'B_limits': [-0.2025, 0.1975], 'C_initial': 0.0181, 'C_limits': [-0.1319, 0.1681], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '3')] = {'B_initial': -0.2028, 'B_limits': [-0.4028, -0.0028], 'C_initial': 0.0194, 'C_limits': [-0.1306, 0.1694], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '24')] = {'B_initial': -0.2018, 'B_limits': [-0.4018, -0.0018], 'C_initial': 0.0436, 'C_limits': [-0.1064, 0.1936], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
