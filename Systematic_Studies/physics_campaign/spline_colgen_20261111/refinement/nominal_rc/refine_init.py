# RC_Bayesian guide for spline. The shared manual initializer is not edited.
# Only bins whose stored curve missed the histogram cosine are overridden.
import importlib.util
spec = importlib.util.spec_from_file_location('manual_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py')
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)
special_fit_parameters_set[('3', '16', '3D', 'RC')] = {'B_initial': -0.12194744, 'B_limits': [-0.28194744, 0.03805256], 'C_initial': -0.01553895, 'C_limits': [-0.09553895, 0.06446105], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'RC')] = {'B_initial': -0.20165216, 'B_limits': [-0.36165216, -0.04165216], 'C_initial': 0.08002408, 'C_limits': [0.00002408, 0.16002408], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33', '3D', 'RC')] = {'B_initial': -0.06747097, 'B_limits': [-0.22747097, 0.09252903], 'C_initial': -0.09409340, 'C_limits': [-0.17409340, -0.01409340], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'RC')] = {'B_initial': -0.19686735, 'B_limits': [-0.35686735, -0.03686735], 'C_initial': -0.00420077, 'C_limits': [-0.08420077, 0.07579923], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20', '3D', 'RC')] = {'B_initial': -0.20589937, 'B_limits': [-0.36589937, -0.04589937], 'C_initial': 0.08123344, 'C_limits': [0.00123344, 0.16123344], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4', '3D', 'RC')] = {'B_initial': -0.21629654, 'B_limits': [-0.37629654, -0.05629654], 'C_initial': -0.03899745, 'C_limits': [-0.11899745, 0.04100255], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'RC')] = {'B_initial': -0.24473052, 'B_limits': [-0.40473052, -0.08473052], 'C_initial': -0.03672562, 'C_limits': [-0.11672562, 0.04327438], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'RC')] = {'B_initial': -0.24045409, 'B_limits': [-0.40045409, -0.08045409], 'C_initial': 0.04191585, 'C_limits': [-0.03808415, 0.12191585], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}

# Column-generation RC histograms whose guide excluded the cosine.
special_fit_parameters_set[('1', '16', '3D', 'RC')] = {'B_initial': 0.0330, 'B_limits': [-0.0670, 0.1330], 'C_initial': 0.0161, 'C_limits': [-0.0839, 0.1161], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'RC')] = {'B_initial': -0.0229, 'B_limits': [-0.1229, 0.0771], 'C_initial': -0.0271, 'C_limits': [-0.1271, 0.0729], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '5', '3D', 'RC')] = {'B_initial': -0.1880, 'B_limits': [-0.2880, -0.0880], 'C_initial': -0.0204, 'C_limits': [-0.1204, 0.0796], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'RC')] = {'B_initial': 0.0534, 'B_limits': [-0.0466, 0.1534], 'C_initial': 0.0110, 'C_limits': [-0.0890, 0.1110], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '4', '3D', 'RC')] = {'B_initial': -0.1808, 'B_limits': [-0.2808, -0.0808], 'C_initial': 0.0172, 'C_limits': [-0.0828, 0.1172], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'RC')] = {'B_initial': 0.0292, 'B_limits': [-0.0708, 0.1292], 'C_initial': 0.0519, 'C_limits': [-0.0481, 0.1519], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '6', '3D', 'RC')] = {'B_initial': -0.2329, 'B_limits': [-0.3329, -0.1329], 'C_initial': 0.0420, 'C_limits': [-0.0580, 0.1420], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '5', '3D', 'RC')] = {'B_initial': -0.2223, 'B_limits': [-0.3223, -0.1223], 'C_initial': -0.0338, 'C_limits': [-0.1338, 0.0662], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7', '3D', 'RC')] = {'B_initial': -0.0161, 'B_limits': [-0.1161, 0.0839], 'C_initial': 0.0379, 'C_limits': [-0.0621, 0.1379], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '2', '3D', 'RC')] = {'B_initial': -0.1052, 'B_limits': [-0.2052, -0.0052], 'C_initial': 0.0279, 'C_limits': [-0.0721, 0.1279], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
