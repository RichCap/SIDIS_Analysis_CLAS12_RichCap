# Run-local guide for dcfidref_loose_el Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1821, 'B_limits': [-0.3821, 0.0179], 'C_initial': -0.0150, 'C_limits': [-0.1650, 0.1350], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2719, 'B_limits': [-0.4719, -0.0719], 'C_initial': 0.0124, 'C_limits': [-0.1376, 0.1624], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3049, 'B_limits': [-0.5049, -0.1049], 'C_initial': -0.0186, 'C_limits': [-0.1686, 0.1314], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2454, 'B_limits': [-0.4454, -0.0454], 'C_initial': 0.0469, 'C_limits': [-0.1031, 0.1969], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3084, 'B_limits': [-0.5084, -0.1084], 'C_initial': 0.1058, 'C_limits': [-0.0442, 0.2558], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3333, 'B_limits': [-0.5333, -0.1333], 'C_initial': 0.0628, 'C_limits': [-0.0872, 0.2128], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2779, 'B_limits': [-0.4779, -0.0779], 'C_initial': 0.0216, 'C_limits': [-0.1284, 0.1716], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2504, 'B_limits': [-0.4504, -0.0504], 'C_initial': 0.0696, 'C_limits': [-0.0804, 0.2196], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2911, 'B_limits': [-0.4911, -0.0911], 'C_initial': 0.0663, 'C_limits': [-0.0837, 0.2163], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4435, 'B_limits': [-0.6435, -0.2435], 'C_initial': 0.1096, 'C_limits': [-0.0404, 0.2596], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1001, 'B_limits': [-0.3001, 0.0999], 'C_initial': -0.0117, 'C_limits': [-0.1617, 0.1383], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0090, 'B_limits': [-0.1910, 0.2090], 'C_initial': 0.0539, 'C_limits': [-0.0961, 0.2039], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1737, 'B_limits': [-0.3737, 0.0263], 'C_initial': 0.0134, 'C_limits': [-0.1366, 0.1634], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1304, 'B_limits': [-0.3304, 0.0696], 'C_initial': 0.0010, 'C_limits': [-0.1490, 0.1510], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3670, 'B_limits': [-0.5670, -0.1670], 'C_initial': 0.1065, 'C_limits': [-0.0435, 0.2565], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0395, 'B_limits': [-0.2395, 0.1605], 'C_initial': 0.0302, 'C_limits': [-0.1198, 0.1802], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2646, 'B_limits': [-0.4646, -0.0646], 'C_initial': 0.0737, 'C_limits': [-0.0763, 0.2237], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0291, 'B_limits': [-0.2291, 0.1709], 'C_initial': 0.0412, 'C_limits': [-0.1088, 0.1912], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '24')] = {'B_initial': -0.2028, 'B_limits': [-0.4028, -0.0028], 'C_initial': 0.0480, 'C_limits': [-0.1020, 0.1980], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
