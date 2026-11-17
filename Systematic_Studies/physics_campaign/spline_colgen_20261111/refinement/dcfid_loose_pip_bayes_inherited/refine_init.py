# Run-local guide for dcfid_loose_pip Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 moment window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2771, 'B_limits': [-0.4771, -0.0771], 'C_initial': 0.0074, 'C_limits': [-0.1426, 0.1574], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1774, 'B_limits': [-0.3774, 0.0226], 'C_initial': -0.0122, 'C_limits': [-0.1622, 0.1378], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3035, 'B_limits': [-0.5035, -0.1035], 'C_initial': -0.0174, 'C_limits': [-0.1674, 0.1326], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1385, 'B_limits': [-0.3385, 0.0615], 'C_initial': -0.0205, 'C_limits': [-0.1705, 0.1295], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '16')] = {'B_initial': -0.1660, 'B_limits': [-0.3660, 0.0340], 'C_initial': 0.0096, 'C_limits': [-0.1404, 0.1596], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '15')] = {'B_initial': -0.1081, 'B_limits': [-0.3081, 0.0919], 'C_initial': 0.0001, 'C_limits': [-0.1499, 0.1501], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2458, 'B_limits': [-0.4458, -0.0458], 'C_initial': 0.0466, 'C_limits': [-0.1034, 0.1966], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3351, 'B_limits': [-0.5351, -0.1351], 'C_initial': 0.0633, 'C_limits': [-0.0867, 0.2133], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2787, 'B_limits': [-0.4787, -0.0787], 'C_initial': 0.0214, 'C_limits': [-0.1286, 0.1714], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2495, 'B_limits': [-0.4495, -0.0495], 'C_initial': 0.0715, 'C_limits': [-0.0785, 0.2215], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0630, 'B_limits': [-0.2630, 0.1370], 'C_initial': 0.0203, 'C_limits': [-0.1297, 0.1703], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4444, 'B_limits': [-0.6444, -0.2444], 'C_initial': 0.1099, 'C_limits': [-0.0401, 0.2599], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1702, 'B_limits': [-0.3702, 0.0298], 'C_initial': 0.0136, 'C_limits': [-0.1364, 0.1636], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3093, 'B_limits': [-0.5093, -0.1093], 'C_initial': 0.1053, 'C_limits': [-0.0447, 0.2553], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2834, 'B_limits': [-0.4834, -0.0834], 'C_initial': 0.0648, 'C_limits': [-0.0852, 0.2148], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0132, 'B_limits': [-0.1868, 0.2132], 'C_initial': 0.0557, 'C_limits': [-0.0943, 0.2057], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1308, 'B_limits': [-0.3308, 0.0692], 'C_initial': 0.0010, 'C_limits': [-0.1490, 0.1510], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1004, 'B_limits': [-0.3004, 0.0996], 'C_initial': -0.0113, 'C_limits': [-0.1613, 0.1387], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0932, 'B_limits': [-0.2932, 0.1068], 'C_initial': -0.0125, 'C_limits': [-0.1625, 0.1375], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3674, 'B_limits': [-0.5674, -0.1674], 'C_initial': 0.1057, 'C_limits': [-0.0443, 0.2557], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '4')] = {'B_initial': -0.2315, 'B_limits': [-0.4315, -0.0315], 'C_initial': 0.0236, 'C_limits': [-0.1264, 0.1736], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17')] = {'B_initial': -0.0714, 'B_limits': [-0.2714, 0.1286], 'C_initial': -0.0218, 'C_limits': [-0.1718, 0.1282], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2659, 'B_limits': [-0.4659, -0.0659], 'C_initial': 0.0735, 'C_limits': [-0.0765, 0.2235], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0328, 'B_limits': [-0.2328, 0.1672], 'C_initial': 0.0383, 'C_limits': [-0.1117, 0.1883], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
