# Run-local guide for nominal_only_20261030 Acc015 Bayesian. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose pass-1 window missed the histogram cosine. Starts are the wide fit on the filled phi range.
# (1, 17) and (1, 22) were left: the stored and wide curves overlap and the stored fit already follows the points.
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2747, 'B_limits': [-0.4747, -0.0747], 'C_initial': 0.0089, 'C_limits': [-0.1411, 0.1589], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '11', '3D')] = special_fit_parameters_set[('10', '11')]
special_fit_parameters_set[('14', '15')] = {'B_initial': -0.1070, 'B_limits': [-0.3070, 0.0930], 'C_initial': 0.0011, 'C_limits': [-0.1489, 0.1511], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '15', '3D')] = special_fit_parameters_set[('14', '15')]
special_fit_parameters_set[('10', '16')] = {'B_initial': -0.1649, 'B_limits': [-0.3649, 0.0351], 'C_initial': 0.0103, 'C_limits': [-0.1397, 0.1603], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '16', '3D')] = special_fit_parameters_set[('10', '16')]
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.3035, 'B_limits': [-0.5035, -0.1035], 'C_initial': -0.0175, 'C_limits': [-0.1675, 0.1325], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5', '3D')] = special_fit_parameters_set[('14', '5')]
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2458, 'B_limits': [-0.4458, -0.0458], 'C_initial': 0.0466, 'C_limits': [-0.1034, 0.1966], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19', '3D')] = special_fit_parameters_set[('1', '19')]
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1312, 'B_limits': [-0.3312, 0.0688], 'C_initial': -0.0209, 'C_limits': [-0.1709, 0.1291], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34', '3D')] = special_fit_parameters_set[('4', '34')]
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3350, 'B_limits': [-0.5350, -0.1350], 'C_initial': 0.0635, 'C_limits': [-0.0865, 0.2135], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15', '3D')] = special_fit_parameters_set[('15', '15')]
special_fit_parameters_set[('9', '3')] = {'B_initial': -0.1573, 'B_limits': [-0.3573, 0.0427], 'C_initial': -0.0082, 'C_limits': [-0.1582, 0.1418], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '3', '3D')] = special_fit_parameters_set[('9', '3')]
special_fit_parameters_set[('2', '3')] = {'B_initial': -0.1708, 'B_limits': [-0.3708, 0.0292], 'C_initial': 0.0183, 'C_limits': [-0.1317, 0.1683], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('2', '3', '3D')] = special_fit_parameters_set[('2', '3')]
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1307, 'B_limits': [-0.3307, 0.0693], 'C_initial': 0.0009, 'C_limits': [-0.1491, 0.1509], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3', '3D')] = special_fit_parameters_set[('11', '3')]
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2856, 'B_limits': [-0.4856, -0.0856], 'C_initial': 0.0157, 'C_limits': [-0.1343, 0.1657], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11', '3D')] = special_fit_parameters_set[('7', '11')]
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0939, 'B_limits': [-0.2939, 0.1061], 'C_initial': -0.0130, 'C_limits': [-0.1630, 0.1370], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21', '3D')] = special_fit_parameters_set[('7', '21')]
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0102, 'B_limits': [-0.1898, 0.2102], 'C_initial': 0.0544, 'C_limits': [-0.0956, 0.2044], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31', '3D')] = special_fit_parameters_set[('5', '31')]
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4394, 'B_limits': [-0.6394, -0.2394], 'C_initial': 0.1141, 'C_limits': [-0.0359, 0.2641], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7', '3D')] = special_fit_parameters_set[('9', '7')]
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1710, 'B_limits': [-0.3710, 0.0290], 'C_initial': 0.0130, 'C_limits': [-0.1370, 0.1630], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10', '3D')] = special_fit_parameters_set[('7', '10')]
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2495, 'B_limits': [-0.4495, -0.0495], 'C_initial': 0.0714, 'C_limits': [-0.0786, 0.2214], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29', '3D')] = special_fit_parameters_set[('3', '29')]
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1001, 'B_limits': [-0.3001, 0.0999], 'C_initial': -0.0110, 'C_limits': [-0.1610, 0.1390], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8', '3D')] = special_fit_parameters_set[('10', '8')]
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3668, 'B_limits': [-0.5668, -0.1668], 'C_initial': 0.1062, 'C_limits': [-0.0438, 0.2562], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12', '3D')] = special_fit_parameters_set[('16', '12')]
special_fit_parameters_set[('13', '10')] = {'B_initial': -0.3089, 'B_limits': [-0.5089, -0.1089], 'C_initial': 0.1056, 'C_limits': [-0.0444, 0.2556], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '10', '3D')] = special_fit_parameters_set[('13', '10')]
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2718, 'B_limits': [-0.4718, -0.0718], 'C_initial': -0.0344, 'C_limits': [-0.1844, 0.1156], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4', '3D')] = special_fit_parameters_set[('13', '4')]
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2676, 'B_limits': [-0.4676, -0.0676], 'C_initial': 0.0744, 'C_limits': [-0.0756, 0.2244], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20', '3D')] = special_fit_parameters_set[('11', '20')]
