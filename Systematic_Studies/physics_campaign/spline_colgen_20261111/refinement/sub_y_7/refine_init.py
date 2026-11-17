# Run-local guide for sub_y_7 BC_RC_Bayesian. Shared manual and spline files are not edited.
# BC_RC selects ('q','z','3D','BC'), then ('q','z','BC'), then untagged ('q','z').
# Selected spline limits are mostly [None, None], and the numeric windows are tight enough to pin B and C, so this pass starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Diagnosed misses. Windows sit on the wide-fit cosine. (6,2) was left because the stored and wide curves overlap. Shared files stay untouched.
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.2207, 'B_limits': [-0.3407, -0.1007], 'C_initial': -0.0437, 'C_limits': [-0.1437, 0.0563], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'BC')] = {'B_initial': -0.2474, 'B_limits': [-0.3674, -0.1274], 'C_initial': -0.0289, 'C_limits': [-0.1289, 0.0711], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.2697, 'B_limits': [-0.3897, -0.1497], 'C_initial': 0.0456, 'C_limits': [-0.0544, 0.1456], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.2028, 'B_limits': [-0.3228, -0.0828], 'C_initial': -0.0020, 'C_limits': [-0.1020, 0.0980], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.1750, 'B_limits': [-0.2950, -0.0550], 'C_initial': 0.0644, 'C_limits': [-0.0356, 0.1644], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.1119, 'B_limits': [-0.2319, 0.0081], 'C_initial': -0.0215, 'C_limits': [-0.1215, 0.0785], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D', 'BC')] = {'B_initial': -0.0841, 'B_limits': [-0.2041, 0.0359], 'C_initial': -0.0294, 'C_limits': [-0.1294, 0.0706], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'BC')] = {'B_initial': 0.0283, 'B_limits': [-0.0917, 0.1483], 'C_initial': 0.0108, 'C_limits': [-0.0892, 0.1108], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.0266, 'B_limits': [-0.0934, 0.1466], 'C_initial': 0.0508, 'C_limits': [-0.0492, 0.1508], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '5', '3D', 'BC')] = {'B_initial': -0.1832, 'B_limits': [-0.3032, -0.0632], 'C_initial': -0.0183, 'C_limits': [-0.1183, 0.0817], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.1831, 'B_limits': [-0.3031, -0.0631], 'C_initial': 0.0480, 'C_limits': [-0.0520, 0.1480], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22', '3D', 'BC')] = {'B_initial': -0.0096, 'B_limits': [-0.1296, 0.1104], 'C_initial': 0.0398, 'C_limits': [-0.0602, 0.1398], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8', '3D', 'BC')] = {'B_initial': -0.0708, 'B_limits': [-0.1908, 0.0492], 'C_initial': -0.0113, 'C_limits': [-0.1113, 0.0887], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0551, 'B_limits': [-0.0649, 0.1751], 'C_initial': 0.0102, 'C_limits': [-0.0898, 0.1102], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.0212, 'B_limits': [-0.1412, 0.0988], 'C_initial': -0.0249, 'C_limits': [-0.1249, 0.0751], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7', '3D', 'BC')] = {'B_initial': -0.0163, 'B_limits': [-0.1363, 0.1037], 'C_initial': 0.0345, 'C_limits': [-0.0655, 0.1345], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
