# RC_Bayesian guide for spline. The shared manual initializer is not edited.
# Only bins whose stored curve missed the histogram cosine are overridden.
import importlib.util
spec = importlib.util.spec_from_file_location('manual_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py')
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)
special_fit_parameters_set[('13', '4', '3D', 'RC')] = {'B_initial': -0.21633628, 'B_limits': [-0.49891267, 0.06624011], 'C_initial': -0.03902588, 'C_limits': [-0.18806144, 0.11000967], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'RC')] = {'B_initial': -0.12194357, 'B_limits': [-0.27249318, 0.02860604], 'C_initial': -0.01554574, 'C_limits': [-0.07817447, 0.04708298], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'RC')] = {'B_initial': -0.20166031, 'B_limits': [-0.32334565, -0.07997498], 'C_initial': 0.08003116, 'C_limits': [-0.03250000, 0.19256231], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33', '3D', 'RC')] = {'B_initial': -0.06745848, 'B_limits': [-0.21023109, 0.07531413], 'C_initial': -0.09406553, 'C_limits': [-0.15499073, -0.03314034], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'RC')] = {'B_initial': -0.24044746, 'B_limits': [-0.33091710, -0.14997781], 'C_initial': 0.04190400, 'C_limits': [-0.06500000, 0.14880800], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D', 'RC')] = {'B_initial': -0.24473610, 'B_limits': [-0.40055963, -0.08891257], 'C_initial': -0.03674242, 'C_limits': [-0.12553353, 0.05204869], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'RC')] = {'B_initial': -0.19688214, 'B_limits': [-0.32783124, -0.06593304], 'C_initial': -0.00421244, 'C_limits': [-0.06755465, 0.05912977], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
