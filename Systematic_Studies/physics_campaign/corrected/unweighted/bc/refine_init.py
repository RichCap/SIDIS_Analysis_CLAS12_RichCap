# BC_RC_Bayesian guide for unweighted. The shared spline initializer is not edited.
# Only bins whose stored curve missed the histogram cosine are overridden.
import importlib.util
spec = importlib.util.spec_from_file_location('spline_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py')
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)
special_fit_parameters_set[('10', '17', '3D', 'BC')] = {'B_initial': -0.19795138, 'B_limits': [-0.31795138, -0.07795138], 'C_initial': -0.00280364, 'C_limits': [-0.08280364, 0.07719636], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '15', '3D', 'BC')] = {'B_initial': -0.08531907, 'B_limits': [-0.20531907, 0.03468093], 'C_initial': -0.01668605, 'C_limits': [-0.09668605, 0.06331395], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.19747465, 'B_limits': [-0.31747465, -0.07747465], 'C_initial': 0.06524518, 'C_limits': [-0.01475482, 0.14524518], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.26521303, 'B_limits': [-0.38521303, -0.14521303], 'C_initial': 0.05286726, 'C_limits': [-0.02713274, 0.13286726], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '2', '3D', 'BC')] = {'B_initial': -0.11146100, 'B_limits': [-0.23146100, 0.00853900], 'C_initial': 0.01675081, 'C_limits': [-0.06324919, 0.09675081], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.20891734, 'B_limits': [-0.32891734, -0.08891734], 'C_initial': -0.00695073, 'C_limits': [-0.08695073, 0.07304927], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3', '3D', 'BC')] = {'B_initial': -0.09869136, 'B_limits': [-0.21869136, 0.02130864], 'C_initial': -0.01532207, 'C_limits': [-0.09532207, 0.06467793], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.21711298, 'B_limits': [-0.33711298, -0.09711298], 'C_initial': 0.05333633, 'C_limits': [-0.02666367, 0.13333633], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.12036306, 'B_limits': [-0.24036306, -0.00036306], 'C_initial': -0.01934848, 'C_limits': [-0.09934848, 0.06065152], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20', '3D', 'BC')] = {'B_initial': -0.23089252, 'B_limits': [-0.35089252, -0.11089252], 'C_initial': 0.09028401, 'C_limits': [0.01028401, 0.17028401], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.00316769, 'B_limits': [-0.11683231, 0.12316769], 'C_initial': -0.03066703, 'C_limits': [-0.11066703, 0.04933297], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '29', '3D', 'BC')] = {'B_initial': -0.19894826, 'B_limits': [-0.31894826, -0.07894826], 'C_initial': 0.07803000, 'C_limits': [-0.00197000, 0.15803000], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
