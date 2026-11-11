# Run-local BC_RC guide for spline sub_y_7. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17 and 5 of 452 are narrower than 0.05, so the windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_y_7", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.18966469, "B_limits": [-0.38966469, 0.01033531], "C_initial": 0.01130724, "C_limits": [-0.18869276, 0.21130724], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.18208857, "B_limits": [-0.38208857, 0.01791143], "C_initial": -0.01714162, "C_limits": [-0.21714162, 0.18285838], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.11912547, "B_limits": [-0.31912547, 0.08087453], "C_initial": -0.05218445, "C_limits": [-0.25218445, 0.14781555], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.00887286, "B_limits": [-0.19112714, 0.20887286], "C_initial": -0.01563280, "C_limits": [-0.21563280, 0.18436720], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.01106705, "B_limits": [-0.18893295, 0.21106705], "C_initial": -0.00630695, "C_limits": [-0.20630695, 0.19369305], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03423447, "B_limits": [-0.23423447, 0.16576553], "C_initial": -0.02559289, "C_limits": [-0.22559289, 0.17440711], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.00355025, "B_limits": [-0.19644975, 0.20355025], "C_initial": 0.03798528, "C_limits": [-0.16201472, 0.23798528], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.14291751, "B_limits": [-0.34291751, 0.05708249], "C_initial": 0.05646088, "C_limits": [-0.14353912, 0.25646088], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11783509, "B_limits": [-0.31783509, 0.08216491], "C_initial": -0.01723372, "C_limits": [-0.21723372, 0.18276628], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14456908, "B_limits": [-0.34456908, 0.05543092], "C_initial": 0.04088842, "C_limits": [-0.15911158, 0.24088842], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20657576, "B_limits": [-0.40657576, -0.00657576], "C_initial": 0.08431884, "C_limits": [-0.11568116, 0.28431884], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06863874, "B_limits": [-0.26863874, 0.13136126], "C_initial": -0.09296142, "C_limits": [-0.29296142, 0.10703858], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10498906, "B_limits": [-0.30498906, 0.09501094], "C_initial": -0.00820956, "C_limits": [-0.20820956, 0.19179044], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "4", "3D", "BC")] = {"B_initial": -0.17549514, "B_limits": [-0.37549514, 0.02450486], "C_initial": 0.00725966, "C_limits": [-0.19274034, 0.20725966], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "9", "3D", "BC")] = {"B_initial": -0.06054656, "B_limits": [-0.26054656, 0.13945344], "C_initial": 0.01459228, "C_limits": [-0.18540772, 0.21459228], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "15", "3D", "BC")] = {"B_initial": -0.06384442, "B_limits": [-0.26384442, 0.13615558], "C_initial": 0.01262355, "C_limits": [-0.18737645, 0.21262355], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02257802, "B_limits": [-0.17742198, 0.22257802], "C_initial": 0.03766615, "C_limits": [-0.16233385, 0.23766615], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "1", "3D", "BC")] = {"B_initial": -0.04367327, "B_limits": [-0.24367327, 0.15632673], "C_initial": 0.01537209, "C_limits": [-0.18462791, 0.21537209], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.10009084, "B_limits": [-0.30009084, 0.09990916], "C_initial": 0.03590999, "C_limits": [-0.16409001, 0.23590999], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.20526263, "B_limits": [-0.40526263, -0.00526263], "C_initial": 0.07870433, "C_limits": [-0.12129567, 0.27870433], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "5", "3D", "BC")] = {"B_initial": -0.22724311, "B_limits": [-0.42724311, -0.02724311], "C_initial": -0.03158376, "C_limits": [-0.23158376, 0.16841624], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07490691, "B_limits": [-0.27490691, 0.12509309], "C_initial": -0.00814857, "C_limits": [-0.20814857, 0.19185143], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19600122, "B_limits": [-0.39600122, 0.00399878], "C_initial": -0.00105887, "C_limits": [-0.20105887, 0.19894113], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20703705, "B_limits": [-0.40703705, -0.00703705], "C_initial": 0.08075129, "C_limits": [-0.11924871, 0.28075129], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.21917500, "B_limits": [-0.41917500, -0.01917500], "C_initial": -0.04105412, "C_limits": [-0.24105412, 0.15894588], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24377696, "B_limits": [-0.44377696, -0.04377696], "C_initial": -0.03575885, "C_limits": [-0.23575885, 0.16424115], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.24051710, "B_limits": [-0.44051710, -0.04051710], "C_initial": 0.04177807, "C_limits": [-0.15822193, 0.24177807], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "12", "3D", "BC")] = {"B_initial": -0.28274516, "B_limits": [-0.48274516, -0.08274516], "C_initial": 0.08081138, "C_limits": [-0.11918862, 0.28081138], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
