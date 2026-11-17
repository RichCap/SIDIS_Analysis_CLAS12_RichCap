# Run-local BC_RC_Bayesian guide for sub_phi_7. Shared spline and manual files are not edited.
import importlib.util
spec = importlib.util.spec_from_file_location('spline_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py')
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Diagnosed misses. Windows sit on the wide-fit cosine. Shared files stay untouched.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.2235, 'B_limits': [-0.3435, -0.1035], 'C_initial': -0.0440, 'C_limits': [-0.1440, 0.0560], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.2052, 'B_limits': [-0.3252, -0.0852], 'C_initial': -0.0051, 'C_limits': [-0.1051, 0.0949], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'BC')] = {'B_initial': -0.2507, 'B_limits': [-0.3707, -0.1307], 'C_initial': -0.0305, 'C_limits': [-0.1305, 0.0695], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.1161, 'B_limits': [-0.2361, 0.0039], 'C_initial': -0.0197, 'C_limits': [-0.1197, 0.0803], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.2696, 'B_limits': [-0.3896, -0.1496], 'C_initial': 0.0455, 'C_limits': [-0.0545, 0.1455], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D', 'BC')] = {'B_initial': -0.0832, 'B_limits': [-0.2032, 0.0368], 'C_initial': -0.0272, 'C_limits': [-0.1272, 0.0728], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.1744, 'B_limits': [-0.2944, -0.0544], 'C_initial': 0.0612, 'C_limits': [-0.0388, 0.1612], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'BC')] = {'B_initial': 0.0311, 'B_limits': [-0.0889, 0.1511], 'C_initial': 0.0158, 'C_limits': [-0.0842, 0.1158], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.0298, 'B_limits': [-0.0902, 0.1498], 'C_initial': 0.0525, 'C_limits': [-0.0475, 0.1525], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.1854, 'B_limits': [-0.3054, -0.0654], 'C_initial': 0.0489, 'C_limits': [-0.0511, 0.1489], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1', '3D', 'BC')] = {'B_initial': -0.0474, 'B_limits': [-0.1674, 0.0726], 'C_initial': 0.0177, 'C_limits': [-0.0823, 0.1177], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.0245, 'B_limits': [-0.1445, 0.0955], 'C_initial': -0.0269, 'C_limits': [-0.1269, 0.0731], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33', '3D', 'BC')] = {'B_initial': -0.0696, 'B_limits': [-0.1896, 0.0504], 'C_initial': -0.0872, 'C_limits': [-0.1872, 0.0128], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '5', '3D', 'BC')] = {'B_initial': -0.1849, 'B_limits': [-0.3049, -0.0649], 'C_initial': -0.0166, 'C_limits': [-0.1166, 0.0834], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0513, 'B_limits': [-0.0687, 0.1713], 'C_initial': 0.0098, 'C_limits': [-0.0902, 0.1098], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8', '3D', 'BC')] = {'B_initial': -0.0708, 'B_limits': [-0.1908, 0.0492], 'C_initial': -0.0120, 'C_limits': [-0.1120, 0.0880], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7', '3D', 'BC')] = {'B_initial': -0.0147, 'B_limits': [-0.1347, 0.1053], 'C_initial': 0.0384, 'C_limits': [-0.0616, 0.1384], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22', '3D', 'BC')] = {'B_initial': -0.0142, 'B_limits': [-0.1342, 0.1058], 'C_initial': 0.0344, 'C_limits': [-0.0656, 0.1344], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
