# Run-local guide for rc_sf0 RC_Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Column-generation SF0 RC histograms whose guide missed the cosine.
special_fit_parameters_set[('13', '4', '3D', 'RC')] = {'B_initial': -0.217747, 'B_limits': [-0.317747, -0.117747], 'C_initial': -0.041085, 'C_limits': [-0.141085, 0.058915], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'RC')] = {'B_initial': -0.115448, 'B_limits': [-0.215448, -0.015448], 'C_initial': -0.020780, 'C_limits': [-0.120780, 0.079220], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'RC')] = {'B_initial': -0.268635, 'B_limits': [-0.368635, -0.168635], 'C_initial': 0.045625, 'C_limits': [-0.054375, 0.145625], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'RC')] = {'B_initial': -0.169548, 'B_limits': [-0.269548, -0.069548], 'C_initial': 0.059851, 'C_limits': [-0.040149, 0.159851], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'RC')] = {'B_initial': -0.247246, 'B_limits': [-0.347246, -0.147246], 'C_initial': -0.031207, 'C_limits': [-0.131207, 0.068793], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D', 'RC')] = {'B_initial': -0.080614, 'B_limits': [-0.180614, 0.019386], 'C_initial': -0.027182, 'C_limits': [-0.127182, 0.072818], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '16', '3D', 'RC')] = {'B_initial': 0.032942, 'B_limits': [-0.067058, 0.132942], 'C_initial': 0.015747, 'C_limits': [-0.084253, 0.115747], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'RC')] = {'B_initial': -0.201569, 'B_limits': [-0.301569, -0.101569], 'C_initial': -0.006330, 'C_limits': [-0.106330, 0.093670], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'RC')] = {'B_initial': 0.027926, 'B_limits': [-0.072074, 0.127926], 'C_initial': 0.053327, 'C_limits': [-0.046673, 0.153327], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'RC')] = {'B_initial': -0.177111, 'B_limits': [-0.277111, -0.077111], 'C_initial': 0.046455, 'C_limits': [-0.053545, 0.146455], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '5', '3D', 'RC')] = {'B_initial': -0.188847, 'B_limits': [-0.288847, -0.088847], 'C_initial': -0.019497, 'C_limits': [-0.119497, 0.080503], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22', '3D', 'RC')] = {'B_initial': -0.018712, 'B_limits': [-0.118712, 0.081288], 'C_initial': 0.032506, 'C_limits': [-0.067494, 0.132506], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'RC')] = {'B_initial': 0.053819, 'B_limits': [-0.046181, 0.153819], 'C_initial': 0.011239, 'C_limits': [-0.088761, 0.111239], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '7', '3D', 'RC')] = {'B_initial': -0.015885, 'B_limits': [-0.115885, 0.084115], 'C_initial': 0.039610, 'C_limits': [-0.060390, 0.139610], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '5', '3D', 'RC')] = {'B_initial': -0.220750, 'B_limits': [-0.320750, -0.120750], 'C_initial': -0.032795, 'C_limits': [-0.132795, 0.067205], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
