# Run-local guide for dvz_loose_pip Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 1 sat on a narrow moment window. Starts are the wide-fit cosine that followed the histogram.
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2660, 'B_limits': [-0.4660, -0.0660], 'C_initial': -0.0314, 'C_limits': [-0.2314, 0.1686], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1786, 'B_limits': [-0.3786, 0.0214], 'C_initial': -0.0137, 'C_limits': [-0.2137, 0.1863], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2734, 'B_limits': [-0.4734, -0.0734], 'C_initial': 0.0100, 'C_limits': [-0.1900, 0.2100], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3012, 'B_limits': [-0.5012, -0.1012], 'C_initial': -0.0164, 'C_limits': [-0.2164, 0.1836], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1380, 'B_limits': [-0.3380, 0.0620], 'C_initial': -0.0202, 'C_limits': [-0.2202, 0.1798], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2157, 'B_limits': [-0.4157, -0.0157], 'C_initial': 0.0683, 'C_limits': [-0.1317, 0.2683], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3396, 'B_limits': [-0.5396, -0.1396], 'C_initial': 0.0570, 'C_limits': [-0.1430, 0.2570], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2768, 'B_limits': [-0.4768, -0.0768], 'C_initial': 0.0217, 'C_limits': [-0.1783, 0.2217], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3262, 'B_limits': [-0.5262, -0.1262], 'C_initial': 0.0905, 'C_limits': [-0.1095, 0.2905], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2471, 'B_limits': [-0.4471, -0.0471], 'C_initial': 0.0726, 'C_limits': [-0.1274, 0.2726], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4379, 'B_limits': [-0.6379, -0.2379], 'C_initial': 0.1124, 'C_limits': [-0.0876, 0.3124], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0748, 'B_limits': [-0.2748, 0.1252], 'C_initial': 0.0094, 'C_limits': [-0.1906, 0.2094], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '4')] = {'B_initial': -0.1274, 'B_limits': [-0.3274, 0.0726], 'C_initial': 0.0737, 'C_limits': [-0.1263, 0.2737], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1386, 'B_limits': [-0.3386, 0.0614], 'C_initial': -0.0068, 'C_limits': [-0.2068, 0.1932], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1706, 'B_limits': [-0.3706, 0.0294], 'C_initial': 0.0132, 'C_limits': [-0.1868, 0.2132], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1094, 'B_limits': [-0.3094, 0.0906], 'C_initial': -0.0177, 'C_limits': [-0.2177, 0.1823], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2592, 'B_limits': [-0.4592, -0.0592], 'C_initial': 0.0978, 'C_limits': [-0.1022, 0.2978], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0927, 'B_limits': [-0.2927, 0.1073], 'C_initial': -0.0116, 'C_limits': [-0.2116, 0.1884], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0206, 'B_limits': [-0.1794, 0.2206], 'C_initial': 0.0581, 'C_limits': [-0.1419, 0.2581], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2903, 'B_limits': [-0.4903, -0.0903], 'C_initial': 0.0536, 'C_limits': [-0.1464, 0.2536], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3524, 'B_limits': [-0.5524, -0.1524], 'C_initial': 0.1160, 'C_limits': [-0.0840, 0.3160], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0614, 'B_limits': [-0.2614, 0.1386], 'C_initial': 0.0211, 'C_limits': [-0.1789, 0.2211], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
