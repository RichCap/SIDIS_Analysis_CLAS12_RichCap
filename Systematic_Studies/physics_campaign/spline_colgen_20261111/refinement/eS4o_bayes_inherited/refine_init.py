# Run-local guide for eS4o Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('1', '13')] = {'B_initial': -0.3225, 'B_limits': [-0.5225, -0.1225], 'C_initial': 0.1154, 'C_limits': [-0.0346, 0.2654], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2735, 'B_limits': [-0.4735, -0.0735], 'C_initial': 0.0725, 'C_limits': [-0.0775, 0.2225], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '16')] = {'B_initial': -0.1718, 'B_limits': [-0.3718, 0.0282], 'C_initial': 0.0404, 'C_limits': [-0.1096, 0.1904], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '28')] = {'B_initial': -0.1902, 'B_limits': [-0.3902, 0.0098], 'C_initial': -0.0498, 'C_limits': [-0.1998, 0.1002], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.3388, 'B_limits': [0.1388, 0.5388], 'C_initial': 0.1959, 'C_limits': [0.0459, 0.3459], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '27')] = {'B_initial': -0.1458, 'B_limits': [-0.3458, 0.0542], 'C_initial': -0.0469, 'C_limits': [-0.1969, 0.1031], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '24')] = {'B_initial': -0.1507, 'B_limits': [-0.3507, 0.0493], 'C_initial': -0.0012, 'C_limits': [-0.1512, 0.1488], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.3307, 'B_limits': [-0.5307, -0.1307], 'C_initial': -0.0124, 'C_limits': [-0.1624, 0.1376], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '14')] = {'B_initial': -0.1274, 'B_limits': [-0.3274, 0.0726], 'C_initial': -0.0210, 'C_limits': [-0.1710, 0.1290], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '17')] = {'B_initial': -0.2149, 'B_limits': [-0.4149, -0.0149], 'C_initial': 0.0411, 'C_limits': [-0.1089, 0.1911], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '24')] = {'B_initial': -0.1416, 'B_limits': [-0.3416, 0.0584], 'C_initial': -0.3860, 'C_limits': [-0.5360, -0.2360], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '11')] = {'B_initial': -0.2487, 'B_limits': [-0.4487, -0.0487], 'C_initial': 0.0515, 'C_limits': [-0.0985, 0.2015], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
