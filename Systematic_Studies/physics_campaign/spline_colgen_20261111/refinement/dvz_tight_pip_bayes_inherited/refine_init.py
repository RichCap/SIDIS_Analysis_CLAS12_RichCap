# Run-local guide for dvz_tight_pip Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# First-pass windows sat on a bad moment or a narrow limit. Starts are the wide-fit cosine on the histogram phi range.
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1787, 'B_limits': [-0.3787, 0.0213], 'C_initial': -0.0126, 'C_limits': [-0.2126, 0.1874], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2666, 'B_limits': [-0.4666, -0.0666], 'C_initial': -0.0314, 'C_limits': [-0.2314, 0.1686], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2733, 'B_limits': [-0.4733, -0.0733], 'C_initial': 0.0105, 'C_limits': [-0.1895, 0.2105], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1386, 'B_limits': [-0.3386, 0.0614], 'C_initial': -0.0219, 'C_limits': [-0.2219, 0.1781], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3360, 'B_limits': [-0.5360, -0.1360], 'C_initial': 0.0630, 'C_limits': [-0.1370, 0.2630], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3057, 'B_limits': [-0.5057, -0.1057], 'C_initial': -0.0177, 'C_limits': [-0.2177, 0.1823], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0636, 'B_limits': [-0.2636, 0.1364], 'C_initial': 0.0206, 'C_limits': [-0.1794, 0.2206], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2464, 'B_limits': [-0.4464, -0.0464], 'C_initial': 0.0467, 'C_limits': [-0.1533, 0.2467], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1319, 'B_limits': [-0.3319, 0.0681], 'C_initial': 0.0004, 'C_limits': [-0.1996, 0.2004], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2781, 'B_limits': [-0.4781, -0.0781], 'C_initial': 0.0220, 'C_limits': [-0.1780, 0.2220], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4436, 'B_limits': [-0.6436, -0.2436], 'C_initial': 0.1107, 'C_limits': [-0.0893, 0.3107], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0934, 'B_limits': [-0.2934, 0.1066], 'C_initial': -0.0125, 'C_limits': [-0.2125, 0.1875], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1719, 'B_limits': [-0.3719, 0.0281], 'C_initial': 0.0127, 'C_limits': [-0.1873, 0.2127], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '4')] = {'B_initial': -0.2349, 'B_limits': [-0.4349, -0.0349], 'C_initial': 0.0220, 'C_limits': [-0.1780, 0.2220], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2661, 'B_limits': [-0.4661, -0.0661], 'C_initial': 0.0727, 'C_limits': [-0.1273, 0.2727], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3676, 'B_limits': [-0.5676, -0.1676], 'C_initial': 0.1059, 'C_limits': [-0.0941, 0.3059], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2502, 'B_limits': [-0.4502, -0.0502], 'C_initial': 0.0717, 'C_limits': [-0.1283, 0.2717], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0018, 'B_limits': [-0.1982, 0.2018], 'C_initial': 0.0513, 'C_limits': [-0.1487, 0.2513], 'Allow_Multiple_Fits': False, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1007, 'B_limits': [-0.3007, 0.0993], 'C_initial': -0.0118, 'C_limits': [-0.2118, 0.1882], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2833, 'B_limits': [-0.4833, -0.0833], 'C_initial': 0.0643, 'C_limits': [-0.1357, 0.2643], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3099, 'B_limits': [-0.5099, -0.1099], 'C_initial': 0.1053, 'C_limits': [-0.0947, 0.3053], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0309, 'B_limits': [-0.2309, 0.1691], 'C_initial': 0.0395, 'C_limits': [-0.1605, 0.2395], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '6')] = {'B_initial': -0.3930, 'B_limits': [-0.5930, -0.1930], 'C_initial': 0.0725, 'C_limits': [-0.1275, 0.2725], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}

# Second pass collapsed the near-zero moment because its window is half the central value. Keep that moment on the first-pass error.
