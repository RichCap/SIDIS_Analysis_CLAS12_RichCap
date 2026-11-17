# Run-local guide for eS5o Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('1', '13')] = {'B_initial': -0.3201, 'B_limits': [-0.5201, -0.1201], 'C_initial': 0.0992, 'C_limits': [-0.0508, 0.2492], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '2')] = {'B_initial': -0.3097, 'B_limits': [-0.5097, -0.1097], 'C_initial': 0.0036, 'C_limits': [-0.1464, 0.1536], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '17')] = {'B_initial': -0.1981, 'B_limits': [-0.3981, 0.0019], 'C_initial': 0.0148, 'C_limits': [-0.1352, 0.1648], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '22')] = {'B_initial': -0.1579, 'B_limits': [-0.3579, 0.0421], 'C_initial': -0.0892, 'C_limits': [-0.2392, 0.0608], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.3697, 'B_limits': [0.1697, 0.5697], 'C_initial': 0.2125, 'C_limits': [0.0625, 0.3625], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('8', '13')] = {'B_initial': -0.2135, 'B_limits': [-0.4135, -0.0135], 'C_initial': -0.0954, 'C_limits': [-0.2454, 0.0546], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '32')] = {'B_initial': -0.1967, 'B_limits': [-0.3967, 0.0033], 'C_initial': -0.0166, 'C_limits': [-0.1666, 0.1334], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '22')] = {'B_initial': -0.1791, 'B_limits': [-0.3791, 0.0209], 'C_initial': 0.0005, 'C_limits': [-0.1495, 0.1505], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '9')] = {'B_initial': -0.2429, 'B_limits': [-0.4429, -0.0429], 'C_initial': -0.0144, 'C_limits': [-0.1644, 0.1356], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '9')] = {'B_initial': -0.1696, 'B_limits': [-0.3696, 0.0304], 'C_initial': -0.0037, 'C_limits': [-0.1537, 0.1463], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '17')] = {'B_initial': -0.2893, 'B_limits': [-0.4893, -0.0893], 'C_initial': -0.0264, 'C_limits': [-0.1764, 0.1236], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3361, 'B_limits': [-0.5361, -0.1361], 'C_initial': 0.0779, 'C_limits': [-0.0721, 0.2279], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
