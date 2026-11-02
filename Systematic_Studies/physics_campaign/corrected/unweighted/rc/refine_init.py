# RC_Bayesian guide for unweighted. The shared manual initializer is not edited.
# Only bins whose stored curve missed the histogram cosine are overridden.
import importlib.util
spec = importlib.util.spec_from_file_location('manual_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py')
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)
special_fit_parameters_set[('3', '16', '3D', 'RC')] = {'B_initial': -0.12278993, 'B_limits': [-0.28194690, 0.03636705], 'C_initial': -0.02025422, 'C_limits': [-0.08608128, 0.04557284], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'RC')] = {'B_initial': -0.26469560, 'B_limits': [-0.35716653, -0.17222467], 'C_initial': 0.05097448, 'C_limits': [-0.06500000, 0.16694896], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'RC')] = {'B_initial': -0.19168818, 'B_limits': [-0.29997703, -0.08339933], 'C_initial': 0.05859441, 'C_limits': [-0.03250000, 0.14968882], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20', '3D', 'RC')] = {'B_initial': -0.22061414, 'B_limits': [-0.32781758, -0.11341070], 'C_initial': 0.08474180, 'C_limits': [0.00500000, 0.16448360], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
