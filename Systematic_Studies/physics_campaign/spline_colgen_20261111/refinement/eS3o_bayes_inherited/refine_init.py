# Run-local guide for eS3o Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 1 keys existed with no start, so the second fit pass collapsed near zero, or a manual limit pinned B or C. Starts are the wide-fit cosine.
special_fit_parameters_set[('1', '11')] = {'B_initial': -0.1680, 'B_limits': [-0.3680, 0.0320], 'C_initial': -0.0108, 'C_limits': [-0.1608, 0.1392], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2276, 'B_limits': [-0.4276, -0.0276], 'C_initial': 0.0319, 'C_limits': [-0.1181, 0.1819], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '10')] = {'B_initial': -0.2407, 'B_limits': [-0.4407, -0.0407], 'C_initial': -0.0608, 'C_limits': [-0.2108, 0.0892], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '25')] = {'B_initial': -0.1333, 'B_limits': [-0.3333, 0.0667], 'C_initial': 0.0204, 'C_limits': [-0.1296, 0.1704], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '23')] = {'B_initial': -0.2003, 'B_limits': [-0.4003, -0.0003], 'C_initial': 0.0182, 'C_limits': [-0.1318, 0.1682], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '27')] = {'B_initial': -0.0929, 'B_limits': [-0.2929, 0.1071], 'C_initial': -0.0226, 'C_limits': [-0.1726, 0.1274], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('8', '21')] = {'B_initial': -0.0986, 'B_limits': [-0.2986, 0.1014], 'C_initial': -0.0339, 'C_limits': [-0.1839, 0.1161], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '32')] = {'B_initial': -0.1449, 'B_limits': [-0.3449, 0.0551], 'C_initial': 0.0195, 'C_limits': [-0.1305, 0.1695], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '9')] = {'B_initial': -0.1487, 'B_limits': [-0.3487, 0.0513], 'C_initial': -0.0494, 'C_limits': [-0.1994, 0.1006], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '18')] = {'B_initial': -0.1300, 'B_limits': [-0.3300, 0.0700], 'C_initial': -0.0432, 'C_limits': [-0.1932, 0.1068], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '24')] = {'B_initial': -0.1763, 'B_limits': [-0.3763, 0.0237], 'C_initial': 0.0181, 'C_limits': [-0.1319, 0.1681], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '17')] = {'B_initial': -0.2646, 'B_limits': [-0.4646, -0.0646], 'C_initial': 0.0051, 'C_limits': [-0.1449, 0.1551], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '29')] = {'B_initial': -0.2453, 'B_limits': [-0.4453, -0.0453], 'C_initial': 0.0398, 'C_limits': [-0.1102, 0.1898], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '23')] = {'B_initial': -0.1397, 'B_limits': [-0.3397, 0.0603], 'C_initial': -0.0497, 'C_limits': [-0.1997, 0.1003], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3511, 'B_limits': [-0.5511, -0.1511], 'C_initial': 0.1608, 'C_limits': [0.0108, 0.3108], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
