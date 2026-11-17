# Run-local guide for nominal_only_20261030 NoRho0 Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
# (1, 17), (1, 16), (1, 22), (3, 7), (7, 10), and (11, 20) were left: the stored and wide curves overlap.
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2490, 'B_limits': [-0.4490, -0.0490], 'C_initial': -0.0188, 'C_limits': [-0.1688, 0.1312], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2591, 'B_limits': [-0.4591, -0.0591], 'C_initial': 0.0097, 'C_limits': [-0.1403, 0.1597], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1655, 'B_limits': [-0.3655, 0.0345], 'C_initial': -0.0166, 'C_limits': [-0.1666, 0.1334], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1238, 'B_limits': [-0.3238, 0.0762], 'C_initial': -0.0190, 'C_limits': [-0.1690, 0.1310], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3244, 'B_limits': [-0.5244, -0.1244], 'C_initial': 0.0588, 'C_limits': [-0.0912, 0.2088], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2434, 'B_limits': [-0.4434, -0.0434], 'C_initial': 0.0463, 'C_limits': [-0.1037, 0.1963], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.2946, 'B_limits': [-0.4946, -0.0946], 'C_initial': -0.0071, 'C_limits': [-0.1571, 0.1429], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0630, 'B_limits': [-0.2630, 0.1370], 'C_initial': 0.0248, 'C_limits': [-0.1252, 0.1748], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.0823, 'B_limits': [-0.2823, 0.1177], 'C_initial': -0.0074, 'C_limits': [-0.1574, 0.1426], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2651, 'B_limits': [-0.4651, -0.0651], 'C_initial': 0.0243, 'C_limits': [-0.1257, 0.1743], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4431, 'B_limits': [-0.6431, -0.2431], 'C_initial': 0.1143, 'C_limits': [-0.0357, 0.2643], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2791, 'B_limits': [-0.4791, -0.0791], 'C_initial': 0.0653, 'C_limits': [-0.0847, 0.2153], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2426, 'B_limits': [-0.4426, -0.0426], 'C_initial': 0.0725, 'C_limits': [-0.0775, 0.2225], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0135, 'B_limits': [-0.1865, 0.2135], 'C_initial': 0.0533, 'C_limits': [-0.0967, 0.2033], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3634, 'B_limits': [-0.5634, -0.1634], 'C_initial': 0.1039, 'C_limits': [-0.0461, 0.2539], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.2999, 'B_limits': [-0.4999, -0.0999], 'C_initial': 0.1022, 'C_limits': [-0.0478, 0.2522], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
