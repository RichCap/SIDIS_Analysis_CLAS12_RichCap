# Run-local guide for dcfid_tight_el Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 1 sat on a narrow moment window or a tight manual limit. Starts are the wide-fit cosine.
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2671, 'B_limits': [-0.4671, -0.0671], 'C_initial': -0.0314, 'C_limits': [-0.2314, 0.1686], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1778, 'B_limits': [-0.3778, 0.0222], 'C_initial': -0.0125, 'C_limits': [-0.2125, 0.1875], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2736, 'B_limits': [-0.4736, -0.0736], 'C_initial': 0.0102, 'C_limits': [-0.1898, 0.2102], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1385, 'B_limits': [-0.3385, 0.0615], 'C_initial': -0.0205, 'C_limits': [-0.2205, 0.1795], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3035, 'B_limits': [-0.5035, -0.1035], 'C_initial': -0.0175, 'C_limits': [-0.2175, 0.1825], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2458, 'B_limits': [-0.4458, -0.0458], 'C_initial': 0.0466, 'C_limits': [-0.1534, 0.2466], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3350, 'B_limits': [-0.5350, -0.1350], 'C_initial': 0.0635, 'C_limits': [-0.1365, 0.2635], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2495, 'B_limits': [-0.4495, -0.0495], 'C_initial': 0.0715, 'C_limits': [-0.1285, 0.2715], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2778, 'B_limits': [-0.4778, -0.0778], 'C_initial': 0.0219, 'C_limits': [-0.1781, 0.2219], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4431, 'B_limits': [-0.6431, -0.2431], 'C_initial': 0.1109, 'C_limits': [-0.0891, 0.3109], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0629, 'B_limits': [-0.2629, 0.1371], 'C_initial': 0.0204, 'C_limits': [-0.1796, 0.2204], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1710, 'B_limits': [-0.3710, 0.0290], 'C_initial': 0.0129, 'C_limits': [-0.1871, 0.2129], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2834, 'B_limits': [-0.4834, -0.0834], 'C_initial': 0.0648, 'C_limits': [-0.1352, 0.2648], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1310, 'B_limits': [-0.3310, 0.0690], 'C_initial': 0.0007, 'C_limits': [-0.1993, 0.2007], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0939, 'B_limits': [-0.2939, 0.1061], 'C_initial': -0.0130, 'C_limits': [-0.2130, 0.1870], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0102, 'B_limits': [-0.1898, 0.2102], 'C_initial': 0.0544, 'C_limits': [-0.1456, 0.2544], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1002, 'B_limits': [-0.3002, 0.0998], 'C_initial': -0.0111, 'C_limits': [-0.2111, 0.1889], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3668, 'B_limits': [-0.5668, -0.1668], 'C_initial': 0.1062, 'C_limits': [-0.0938, 0.3062], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0366, 'B_limits': [-0.2366, 0.1634], 'C_initial': 0.0339, 'C_limits': [-0.1661, 0.2339], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
