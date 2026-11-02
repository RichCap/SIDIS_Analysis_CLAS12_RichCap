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
