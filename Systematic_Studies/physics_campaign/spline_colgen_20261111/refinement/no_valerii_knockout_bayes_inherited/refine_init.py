# Run-local guide for no_valerii_knockout Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1778, 'B_limits': [-0.3778, 0.0222], 'C_initial': -0.0125, 'C_limits': [-0.1625, 0.1375], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2724, 'B_limits': [-0.4724, -0.0724], 'C_initial': -0.0360, 'C_limits': [-0.1860, 0.1140], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2756, 'B_limits': [-0.4756, -0.0756], 'C_initial': 0.0090, 'C_limits': [-0.1410, 0.1590], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1385, 'B_limits': [-0.3385, 0.0615], 'C_initial': -0.0205, 'C_limits': [-0.1705, 0.1295], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2457, 'B_limits': [-0.4457, -0.0457], 'C_initial': 0.0468, 'C_limits': [-0.1032, 0.1968], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3345, 'B_limits': [-0.5345, -0.1345], 'C_initial': 0.0618, 'C_limits': [-0.0882, 0.2118], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3054, 'B_limits': [-0.5054, -0.1054], 'C_initial': -0.0197, 'C_limits': [-0.1697, 0.1303], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1354, 'B_limits': [-0.3354, 0.0646], 'C_initial': 0.0040, 'C_limits': [-0.1460, 0.1540], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0622, 'B_limits': [-0.2622, 0.1378], 'C_initial': 0.0216, 'C_limits': [-0.1284, 0.1716], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2775, 'B_limits': [-0.4775, -0.0775], 'C_initial': 0.0220, 'C_limits': [-0.1280, 0.1720], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0116, 'B_limits': [-0.1884, 0.2116], 'C_initial': 0.0553, 'C_limits': [-0.0947, 0.2053], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0936, 'B_limits': [-0.2936, 0.1064], 'C_initial': -0.0128, 'C_limits': [-0.1628, 0.1372], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1707, 'B_limits': [-0.3707, 0.0293], 'C_initial': 0.0132, 'C_limits': [-0.1368, 0.1632], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4413, 'B_limits': [-0.6413, -0.2413], 'C_initial': 0.1109, 'C_limits': [-0.0391, 0.2609], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2495, 'B_limits': [-0.4495, -0.0495], 'C_initial': 0.0715, 'C_limits': [-0.0785, 0.2215], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2834, 'B_limits': [-0.4834, -0.0834], 'C_initial': 0.0648, 'C_limits': [-0.0852, 0.2148], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3651, 'B_limits': [-0.5651, -0.1651], 'C_initial': 0.1060, 'C_limits': [-0.0440, 0.2560], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0347, 'B_limits': [-0.2347, 0.1653], 'C_initial': 0.0352, 'C_limits': [-0.1148, 0.1852], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1008, 'B_limits': [-0.3008, 0.0992], 'C_initial': -0.0101, 'C_limits': [-0.1601, 0.1399], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7')] = {'B_initial': -0.0314, 'B_limits': [-0.2314, 0.1686], 'C_initial': 0.0434, 'C_limits': [-0.1066, 0.1934], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2670, 'B_limits': [-0.4670, -0.0670], 'C_initial': 0.0743, 'C_limits': [-0.0757, 0.2243], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
