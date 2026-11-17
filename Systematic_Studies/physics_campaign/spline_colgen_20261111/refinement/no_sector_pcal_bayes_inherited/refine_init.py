# Run-local guide for no_sector_pcal Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1778, 'B_limits': [-0.3778, 0.0222], 'C_initial': -0.0125, 'C_limits': [-0.1625, 0.1375], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2760, 'B_limits': [-0.4760, -0.0760], 'C_initial': 0.0093, 'C_limits': [-0.1407, 0.1593], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1385, 'B_limits': [-0.3385, 0.0615], 'C_initial': -0.0205, 'C_limits': [-0.1705, 0.1295], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.2990, 'B_limits': [-0.4990, -0.0990], 'C_initial': -0.0120, 'C_limits': [-0.1620, 0.1380], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2459, 'B_limits': [-0.4459, -0.0459], 'C_initial': 0.0467, 'C_limits': [-0.1033, 0.1967], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3095, 'B_limits': [-0.5095, -0.1095], 'C_initial': 0.1059, 'C_limits': [-0.0441, 0.2559], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3346, 'B_limits': [-0.5346, -0.1346], 'C_initial': 0.0629, 'C_limits': [-0.0871, 0.2129], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2495, 'B_limits': [-0.4495, -0.0495], 'C_initial': 0.0715, 'C_limits': [-0.0785, 0.2215], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2785, 'B_limits': [-0.4785, -0.0785], 'C_initial': 0.0214, 'C_limits': [-0.1286, 0.1714], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4449, 'B_limits': [-0.6449, -0.2449], 'C_initial': 0.1099, 'C_limits': [-0.0401, 0.2599], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1716, 'B_limits': [-0.3716, 0.0284], 'C_initial': 0.0123, 'C_limits': [-0.1377, 0.1623], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2834, 'B_limits': [-0.4834, -0.0834], 'C_initial': 0.0648, 'C_limits': [-0.0852, 0.2148], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0620, 'B_limits': [-0.2620, 0.1380], 'C_initial': 0.0178, 'C_limits': [-0.1322, 0.1678], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0949, 'B_limits': [-0.2949, 0.1051], 'C_initial': -0.0135, 'C_limits': [-0.1635, 0.1365], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1274, 'B_limits': [-0.3274, 0.0726], 'C_initial': -0.0029, 'C_limits': [-0.1529, 0.1471], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1031, 'B_limits': [-0.3031, 0.0969], 'C_initial': -0.0115, 'C_limits': [-0.1615, 0.1385], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0101, 'B_limits': [-0.1899, 0.2101], 'C_initial': 0.0537, 'C_limits': [-0.0963, 0.2037], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3669, 'B_limits': [-0.5669, -0.1669], 'C_initial': 0.1079, 'C_limits': [-0.0421, 0.2579], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0393, 'B_limits': [-0.2393, 0.1607], 'C_initial': 0.0314, 'C_limits': [-0.1186, 0.1814], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
