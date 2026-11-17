# Run-local guide for noSmear Bayesian inherited. The shared manual file is not edited.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py')
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Bins whose first pass sat on a bad local start or a limit that excluded the histogram cosine.
special_fit_parameters_set[('10', '11')] = {'B_initial': -0.2751, 'B_limits': [-0.4751, -0.0751], 'C_initial': 0.0092, 'C_limits': [-0.1908, 0.2092], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('13', '4')] = {'B_initial': -0.2663, 'B_limits': [-0.4663, -0.0663], 'C_initial': -0.0317, 'C_limits': [-0.2317, 0.1683], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '16')] = {'B_initial': -0.1767, 'B_limits': [-0.3767, 0.0233], 'C_initial': -0.0112, 'C_limits': [-0.2112, 0.1888], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '3')] = {'B_initial': -0.1307, 'B_limits': [-0.3307, 0.0693], 'C_initial': 0.0033, 'C_limits': [-0.1967, 0.2033], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('15', '15')] = {'B_initial': -0.3137, 'B_limits': [-0.5137, -0.1137], 'C_initial': 0.0629, 'C_limits': [-0.1371, 0.2629], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('14', '5')] = {'B_initial': -0.2985, 'B_limits': [-0.4985, -0.0985], 'C_initial': -0.0166, 'C_limits': [-0.2166, 0.1834], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '33')] = {'B_initial': -0.1068, 'B_limits': [-0.3068, 0.0932], 'C_initial': -0.0837, 'C_limits': [-0.2837, 0.1163], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '19')] = {'B_initial': -0.2414, 'B_limits': [-0.4414, -0.0414], 'C_initial': 0.0463, 'C_limits': [-0.1537, 0.2463], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '2')] = {'B_initial': -0.1502, 'B_limits': [-0.3502, 0.0498], 'C_initial': 0.0223, 'C_limits': [-0.1777, 0.2223], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('6', '1')] = {'B_initial': -0.0623, 'B_limits': [-0.2623, 0.1377], 'C_initial': 0.0201, 'C_limits': [-0.1799, 0.2201], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('4', '34')] = {'B_initial': -0.1340, 'B_limits': [-0.3340, 0.0660], 'C_initial': -0.0195, 'C_limits': [-0.2195, 0.1805], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '10')] = {'B_initial': -0.1723, 'B_limits': [-0.3723, 0.0277], 'C_initial': 0.0164, 'C_limits': [-0.1836, 0.2164], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '29')] = {'B_initial': -0.2493, 'B_limits': [-0.4493, -0.0493], 'C_initial': 0.0778, 'C_limits': [-0.1222, 0.2778], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('5', '31')] = {'B_initial': 0.0072, 'B_limits': [-0.1928, 0.2072], 'C_initial': 0.0529, 'C_limits': [-0.1471, 0.2529], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('9', '7')] = {'B_initial': -0.4386, 'B_limits': [-0.6386, -0.2386], 'C_initial': 0.1106, 'C_limits': [-0.0894, 0.3106], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '11')] = {'B_initial': -0.2716, 'B_limits': [-0.4716, -0.0716], 'C_initial': 0.0217, 'C_limits': [-0.1783, 0.2217], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('3', '24')] = {'B_initial': -0.2900, 'B_limits': [-0.4900, -0.0900], 'C_initial': 0.0746, 'C_limits': [-0.1254, 0.2746], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('7', '21')] = {'B_initial': -0.0926, 'B_limits': [-0.2926, 0.1074], 'C_initial': -0.0090, 'C_limits': [-0.2090, 0.1910], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '8')] = {'B_initial': -0.1025, 'B_limits': [-0.3025, 0.0975], 'C_initial': -0.0119, 'C_limits': [-0.2119, 0.1881], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('16', '12')] = {'B_initial': -0.3601, 'B_limits': [-0.5601, -0.1601], 'C_initial': 0.1070, 'C_limits': [-0.0930, 0.3070], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('10', '2')] = {'B_initial': -0.1117, 'B_limits': [-0.3117, 0.0883], 'C_initial': 0.0387, 'C_limits': [-0.1613, 0.2387], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '22')] = {'B_initial': -0.0396, 'B_limits': [-0.2396, 0.1604], 'C_initial': 0.0345, 'C_limits': [-0.1655, 0.2345], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17')] = {'B_initial': -0.0720, 'B_limits': [-0.2720, 0.1280], 'C_initial': -0.0235, 'C_limits': [-0.2235, 0.1765], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('11', '20')] = {'B_initial': -0.2554, 'B_limits': [-0.4554, -0.0554], 'C_initial': 0.0812, 'C_limits': [-0.1188, 0.2812], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
