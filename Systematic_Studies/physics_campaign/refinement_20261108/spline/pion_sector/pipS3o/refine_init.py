# Run-local pion-sector guide. The shared Phi_h files are not edited.
# Pass 2 opens only the bins whose own cosine was missed. Shared Phi_h files were not edited.
import importlib.util
manual_path = '/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py'
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Overrides are this histogram's unconstrained cosine. Limits are wide enough that the cosine is not on the first-pass boundary.
special_fit_parameters_set[("1", "1")] = {'B_initial': -0.49182381, 'B_limits': [-0.95, 0.71709752], 'C_initial': -0.24941601, 'C_limits': [-0.87149936, 0.37266733], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("1", "4")] = {'B_initial': 0.14340901, 'B_limits': [-0.26414692, 0.55096494], 'C_initial': 0.20870802, 'C_limits': [0.02393655, 0.3934795], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("1", "5")] = {'B_initial': -0.12777825, 'B_limits': [-0.29936276, 0.04380626], 'C_initial': 0.01686379, 'C_limits': [-0.13313621, 0.16686379], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("1", "8")] = {'B_initial': -0.35652006, 'B_limits': [-0.95, 0.43536223], 'C_initial': -0.23163349, 'C_limits': [-0.68521579, 0.22194881], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("1", "15")] = {'B_initial': 0.15572695, 'B_limits': [-0.24826527, 0.55971917], 'C_initial': 0.10118226, 'C_limits': [-0.14585485, 0.34821937], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("1", "16")] = {'B_initial': 0.07532708, 'B_limits': [-0.07467292, 0.22532708], 'C_initial': 0.01050406, 'C_limits': [-0.13949594, 0.16050406], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("1", "22")] = {'B_initial': -0.30790631, 'B_limits': [-0.95, 0.41480533], 'C_initial': -0.10636607, 'C_limits': [-0.49309818, 0.28036605], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("1", "24")] = {'B_initial': -0.11538721, 'B_limits': [-0.26538721, 0.03461279], 'C_initial': -0.03791352, 'C_limits': [-0.18791352, 0.11208648], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("2", "6")] = {'B_initial': -0.36422755, 'B_limits': [-0.59839676, -0.13005833], 'C_initial': 0.02302217, 'C_limits': [-0.16446094, 0.21050529], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("2", "7")] = {'B_initial': -0.07048096, 'B_limits': [-0.26384088, 0.12287896], 'C_initial': -0.01178986, 'C_limits': [-0.16299017, 0.13941045], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("2", "14")] = {'B_initial': -0.17832552, 'B_limits': [-0.51240749, 0.15575646], 'C_initial': -0.01497095, 'C_limits': [-0.21113766, 0.18119576], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("2", "29")] = {'B_initial': -0.1982829, 'B_limits': [-0.3482829, -0.0482829], 'C_initial': 0.05846496, 'C_limits': [-0.09153504, 0.20846496], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("5", "3")] = {'B_initial': -0.36593273, 'B_limits': [-0.90983223, 0.17796676], 'C_initial': -0.02802028, 'C_limits': [-0.32813638, 0.27209582], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("5", "5")] = {'B_initial': -0.01535285, 'B_limits': [-0.66032581, 0.62962012], 'C_initial': 0.08630253, 'C_limits': [-0.21618108, 0.38878613], 'Allow_Multiple_Fits': False, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("5", "7")] = {'B_initial': 0.08315077, 'B_limits': [-0.31311248, 0.47941402], 'C_initial': 0.0957958, 'C_limits': [-0.15198844, 0.34358004], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("5", "13")] = {'B_initial': 0.08354534, 'B_limits': [-0.17142079, 0.33851147], 'C_initial': 0.09935853, 'C_limits': [-0.0708004, 0.26951746], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("5", "15")] = {'B_initial': -0.00446619, 'B_limits': [-0.17924135, 0.17030897], 'C_initial': 0.09662049, 'C_limits': [-0.05337951, 0.24662049], 'Allow_Multiple_Fits': False, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("5", "31")] = {'B_initial': 0.09008243, 'B_limits': [-0.47382302, 0.65398787], 'C_initial': 0.07117847, 'C_limits': [-0.23559904, 0.37795598], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("6", "22")] = {'B_initial': -0.17639627, 'B_limits': [-0.32639627, -0.02639627], 'C_initial': -0.08964217, 'C_limits': [-0.23964217, 0.06035783], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("6", "27")] = {'B_initial': -0.06656084, 'B_limits': [-0.21656084, 0.08343916], 'C_initial': -0.08146551, 'C_limits': [-0.23146551, 0.06853449], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("7", "3")] = {'B_initial': 0.57696774, 'B_limits': [-0.62149821, 0.95], 'C_initial': 0.35170566, 'C_limits': [-0.0667482, 0.77015952], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("7", "15")] = {'B_initial': -0.09630515, 'B_limits': [-0.24630515, 0.05369485], 'C_initial': -0.00294981, 'C_limits': [-0.15294981, 0.14705019], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("7", "22")] = {'B_initial': -0.11903027, 'B_limits': [-0.26903027, 0.03096973], 'C_initial': -0.01870651, 'C_limits': [-0.16870651, 0.13129349], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("8", "28")] = {'B_initial': -0.26514458, 'B_limits': [-0.89723976, 0.36695059], 'C_initial': -0.14782599, 'C_limits': [-0.60786338, 0.31221139], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("9", "3")] = {'B_initial': -0.2932872, 'B_limits': [-0.68890485, 0.10233046], 'C_initial': -0.06363014, 'C_limits': [-0.29521079, 0.1679505], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("9", "6")] = {'B_initial': -0.18162587, 'B_limits': [-0.34869741, -0.01455433], 'C_initial': 0.05284473, 'C_limits': [-0.09715527, 0.20284473], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("9", "7")] = {'B_initial': -0.3680759, 'B_limits': [-0.5180759, -0.2180759], 'C_initial': 0.09800924, 'C_limits': [-0.05199076, 0.24800924], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("9", "11")] = {'B_initial': -0.01130163, 'B_limits': [-0.16264653, 0.14004328], 'C_initial': 0.08593328, 'C_limits': [-0.06406672, 0.23593328], 'Allow_Multiple_Fits': False, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("10", "14")] = {'B_initial': -0.07123659, 'B_limits': [-0.22123659, 0.07876341], 'C_initial': 0.03265237, 'C_limits': [-0.11734763, 0.18265237], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("10", "31")] = {'B_initial': 0.00113185, 'B_limits': [-0.14886815, 0.15113185], 'C_initial': 0.07646414, 'C_limits': [-0.07495584, 0.22788412], 'Allow_Multiple_Fits': False, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("11", "20")] = {'B_initial': -0.08516834, 'B_limits': [-0.39081358, 0.22047691], 'C_initial': -0.05323926, 'C_limits': [-0.25961779, 0.15313927], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("13", "4")] = {'B_initial': -0.22374626, 'B_limits': [-0.43558739, -0.01190513], 'C_initial': -0.01559756, 'C_limits': [-0.16559756, 0.13440244], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("13", "14")] = {'B_initial': -0.13329283, 'B_limits': [-0.28329283, 0.01670717], 'C_initial': 0.02693579, 'C_limits': [-0.12306421, 0.17693579], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("14", "9")] = {'B_initial': -0.20196956, 'B_limits': [-0.35196956, -0.05196956], 'C_initial': 0.00526186, 'C_limits': [-0.14473814, 0.15526186], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
special_fit_parameters_set[("15", "9")] = {'B_initial': -0.25897708, 'B_limits': [-0.4541046, -0.06384956], 'C_initial': -0.04222233, 'C_limits': [-0.20211963, 0.11767497], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("15", "13")] = {'B_initial': -0.13329809, 'B_limits': [-0.28329809, 0.01670191], 'C_initial': -0.065377, 'C_limits': [-0.215377, 0.084623], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("15", "24")] = {'B_initial': 0.34816353, 'B_limits': [-0.42783625, 0.95], 'C_initial': -0.6324186, 'C_limits': [-0.95, 0.51889617], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[("16", "13")] = {'B_initial': -0.04191543, 'B_limits': [-0.19191543, 0.10808457], 'C_initial': 0.01993024, 'C_limits': [-0.13006976, 0.16993024], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': False}
