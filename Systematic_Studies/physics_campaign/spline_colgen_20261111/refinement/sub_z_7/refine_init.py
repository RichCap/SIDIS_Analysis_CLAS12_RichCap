# Run-local guide for sub_z_7 BC_RC_Bayesian. Shared manual and spline files are not edited.
# BC_RC selects ('q','z','3D','BC'), then ('q','z','BC'), then untagged ('q','z').
# Untagged spline limits are mostly open, and the numeric windows are tight enough to pin B and C, so this pass starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Diagnosed misses. Windows sit on the wide-fit cosine. (1,17), (1,9), and (5,7) were left because the curves overlap. Shared files stay untouched.
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.2682, 'B_limits': [-0.3882, -0.1482], 'C_initial': 0.0507, 'C_limits': [-0.0493, 0.1507], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.1797, 'B_limits': [-0.2997, -0.0597], 'C_initial': 0.0712, 'C_limits': [-0.0288, 0.1712], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.1861, 'B_limits': [-0.3061, -0.0661], 'C_initial': 0.0505, 'C_limits': [-0.0495, 0.1505], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.0256, 'B_limits': [-0.0944, 0.1456], 'C_initial': 0.0504, 'C_limits': [-0.0496, 0.1504], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
