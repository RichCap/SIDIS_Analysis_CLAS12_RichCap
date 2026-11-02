# BC_RC_Bayesian guide for spline. The shared spline initializer is not edited.
# Only bins whose stored curve missed the histogram cosine are overridden.
import importlib.util
spec = importlib.util.spec_from_file_location('spline_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py')
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.12013919, 'B_limits': [-0.24013919, -0.00013919], 'C_initial': -0.01497745, 'C_limits': [-0.09497745, 0.06502255], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.15588058, 'B_limits': [-0.27588058, -0.03588058], 'C_initial': 0.03577787, 'C_limits': [-0.04422213, 0.11577787], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.20844812, 'B_limits': [-0.32844812, -0.08844812], 'C_initial': 0.08769285, 'C_limits': [0.00769285, 0.16769285], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33', '3D', 'BC')] = {'B_initial': -0.06393204, 'B_limits': [-0.18393204, 0.05606796], 'C_initial': -0.09028222, 'C_limits': [-0.17153621, -0.00902822], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '2', '3D', 'BC')] = {'B_initial': -0.10100389, 'B_limits': [-0.22100389, 0.01899611], 'C_initial': 0.04324262, 'C_limits': [-0.03675738, 0.12324262], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.20668183, 'B_limits': [-0.32668183, -0.08668183], 'C_initial': -0.00375347, 'C_limits': [-0.08375347, 0.07624653], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20', '3D', 'BC')] = {'B_initial': -0.21701231, 'B_limits': [-0.33701231, -0.09701231], 'C_initial': 0.08713291, 'C_limits': [0.00713291, 0.16713291], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4', '3D', 'BC')] = {'B_initial': -0.22473984, 'B_limits': [-0.34834676, -0.10113293], 'C_initial': -0.04000668, 'C_limits': [-0.12000668, 0.03999332], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.23909396, 'B_limits': [-0.37059564, -0.10759228], 'C_initial': 0.04473732, 'C_limits': [-0.03526268, 0.12473732], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
