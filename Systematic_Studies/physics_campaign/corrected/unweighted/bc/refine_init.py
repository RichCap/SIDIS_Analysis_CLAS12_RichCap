# BC_RC_Bayesian guide for unweighted. The shared spline initializer is not edited.
# Only bins whose stored curve missed the histogram cosine are overridden.
import importlib.util
spec = importlib.util.spec_from_file_location('spline_phi_init', '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py')
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)
special_fit_parameters_set[('3', '16', '3D', 'BC')] = {'B_initial': -0.12035741, 'B_limits': [-0.24035741, -0.00035741], 'C_initial': -0.01934650, 'C_limits': [-0.09934650, 0.06065350], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24', '3D', 'BC')] = {'B_initial': -0.21710628, 'B_limits': [-0.33710628, -0.09710628], 'C_initial': 0.05332731, 'C_limits': [-0.02667269, 0.13332731], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D', 'BC')] = {'B_initial': -0.19748491, 'B_limits': [-0.31748491, -0.07748491], 'C_initial': 0.06524156, 'C_limits': [-0.01475844, 0.14524156], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '2', '3D', 'BC')] = {'B_initial': -0.11147860, 'B_limits': [-0.23147860, 0.00852140], 'C_initial': 0.01674560, 'C_limits': [-0.06325440, 0.09674560], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D', 'BC')] = {'B_initial': -0.20892665, 'B_limits': [-0.32892665, -0.08892665], 'C_initial': -0.00696265, 'C_limits': [-0.08696265, 0.07303735], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '17', '3D', 'BC')] = {'B_initial': -0.19795301, 'B_limits': [-0.31795301, -0.07795301], 'C_initial': -0.00281858, 'C_limits': [-0.08281858, 0.07718142], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3', '3D', 'BC')] = {'B_initial': -0.09868535, 'B_limits': [-0.21868535, 0.02131465], 'C_initial': -0.01533033, 'C_limits': [-0.09533033, 0.06466967], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20', '3D', 'BC')] = {'B_initial': -0.23089787, 'B_limits': [-0.35789171, -0.10390404], 'C_initial': 0.09028742, 'C_limits': [0.00902874, 0.17154609], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '15', '3D', 'BC')] = {'B_initial': -0.08530784, 'B_limits': [-0.20530784, 0.03469216], 'C_initial': -0.01669008, 'C_limits': [-0.09669008, 0.06330992], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D', 'BC')] = {'B_initial': -0.26522628, 'B_limits': [-0.41110074, -0.11935183], 'C_initial': 0.05286056, 'C_limits': [-0.02713944, 0.13286056], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
