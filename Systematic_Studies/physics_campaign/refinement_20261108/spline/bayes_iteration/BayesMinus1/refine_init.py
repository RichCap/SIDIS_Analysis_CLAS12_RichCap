# Run-local guide for spline BayesMinus1. The shared Phi_h files are not edited.
# start=auto chose the manual baseline. The 3D spline B windows selected by these
# histograms have median width 0.0153 and 428 of 452 are narrower than 0.05.
# The C windows are narrower (median 0.0070, 445 of 452). --use_spline_init is not used.
# Pass 1 uses that baseline. Later passes edit only the keys this histogram misses.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 2. These starts are this histogram's unconstrained cosine.
# Limits are opened by 0.2 so that cosine is not a boundary.
# The second-pass half-width is off when it is narrower than the error.
special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18329646, "B_limits": [-0.38329646, 0.01670354], "C_initial": -0.00780770, "C_limits": [-0.20780770, 0.19219230], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "4")] = {"B_initial": -0.26391280, "B_limits": [-0.46391280, -0.06391280], "C_initial": -0.02740670, "C_limits": [-0.22740670, 0.17259330], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26831289, "B_limits": [-0.46831289, -0.06831289], "C_initial": 0.01205210, "C_limits": [-0.18794790, 0.21205210], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "19")] = {"B_initial": -0.24701466, "B_limits": [-0.44701466, -0.04701466], "C_initial": 0.05158469, "C_limits": [-0.14841531, 0.25158469], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5")] = {"B_initial": -0.29925379, "B_limits": [-0.49925379, -0.09925379], "C_initial": -0.02356073, "C_limits": [-0.22356073, 0.17643927], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29")] = {"B_initial": -0.27269572, "B_limits": [-0.47269572, -0.07269572], "C_initial": 0.08855136, "C_limits": [-0.11144864, 0.28855136], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34")] = {"B_initial": -0.15868993, "B_limits": [-0.35868993, 0.04131007], "C_initial": -0.00005640, "C_limits": [-0.20005640, 0.19994360], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24")] = {"B_initial": -0.23153358, "B_limits": [-0.43153358, -0.03153358], "C_initial": 0.05214348, "C_limits": [-0.14785652, 0.25214348], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15")] = {"B_initial": -0.30279927, "B_limits": [-0.50279927, -0.10279927], "C_initial": 0.05641956, "C_limits": [-0.14358044, 0.25641956], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10465808, "B_limits": [-0.30465808, 0.09534192], "C_initial": -0.00759917, "C_limits": [-0.20759917, 0.19240083], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42512837, "B_limits": [-0.62512837, -0.22512837], "C_initial": 0.10985403, "C_limits": [-0.09014597, 0.30985403], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30421008, "B_limits": [-0.50421008, -0.10421008], "C_initial": 0.10138803, "C_limits": [-0.09861197, 0.30138803], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12782037, "B_limits": [-0.32782037, 0.07217963], "C_initial": 0.00108644, "C_limits": [-0.19891356, 0.20108644], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "10")] = {"B_initial": -0.16921266, "B_limits": [-0.36921266, 0.03078734], "C_initial": 0.01620063, "C_limits": [-0.18379937, 0.21620063], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "33")] = {"B_initial": -0.11073946, "B_limits": [-0.31073946, 0.08926054], "C_initial": -0.09014433, "C_limits": [-0.29014433, 0.10985567], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "1")] = {"B_initial": -0.05804439, "B_limits": [-0.25804439, 0.14195561], "C_initial": 0.01095878, "C_limits": [-0.18904122, 0.21095878], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20")] = {"B_initial": -0.26834537, "B_limits": [-0.46834537, -0.06834537], "C_initial": 0.08767722, "C_limits": [-0.11232278, 0.28767722], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36238198, "B_limits": [-0.56238198, -0.16238198], "C_initial": 0.10694118, "C_limits": [-0.09305882, 0.30694118], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "29")] = {"B_initial": -0.23955372, "B_limits": [-0.43955372, -0.03955372], "C_initial": 0.07556187, "C_limits": [-0.12443813, 0.27556187], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13371329, "B_limits": [-0.33371329, 0.06628671], "C_initial": 0.00902849, "C_limits": [-0.19097151, 0.20902849], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09640733, "B_limits": [-0.29640733, 0.10359267], "C_initial": -0.01344537, "C_limits": [-0.21344537, 0.18655463], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22")] = {"B_initial": -0.01410440, "B_limits": [-0.21410440, 0.18589560], "C_initial": 0.03712000, "C_limits": [-0.16288000, 0.23712000], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "31")] = {"B_initial": 0.00560983, "B_limits": [-0.19439017, 0.20560983], "C_initial": 0.04125399, "C_limits": [-0.15874601, 0.24125399], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "11")] = {"B_initial": -0.26048729, "B_limits": [-0.46048729, -0.06048729], "C_initial": 0.02552227, "C_limits": [-0.17447773, 0.22552227], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "7")] = {"B_initial": -0.02999359, "B_limits": [-0.22999359, 0.17000641], "C_initial": 0.02798914, "C_limits": [-0.17201086, 0.22798914], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08818562, "B_limits": [-0.28818562, 0.11181438], "C_initial": -0.02003184, "C_limits": [-0.22003184, 0.17996816], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "4")] = {"B_initial": -0.23247840, "B_limits": [-0.43247840, -0.03247840], "C_initial": 0.02449139, "C_limits": [-0.17550861, 0.22449139], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2")] = {"B_initial": -0.13313667, "B_limits": [-0.33313667, 0.06686333], "C_initial": 0.03030880, "C_limits": [-0.16969120, 0.23030880], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "24")] = {"B_initial": -0.21194214, "B_limits": [-0.41194214, -0.01194214], "C_initial": 0.05117175, "C_limits": [-0.14882825, 0.25117175], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "8")] = {"B_initial": -0.12065990, "B_limits": [-0.32065990, 0.07934010], "C_initial": -0.04094343, "C_limits": [-0.24094343, 0.15905657], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "16")] = {"B_initial": -0.17805814, "B_limits": [-0.37805814, 0.02194186], "C_initial": -0.01087079, "C_limits": [-0.21087079, 0.18912921], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35")] = {"B_initial": -0.26068075, "B_limits": [-0.46068075, -0.06068075], "C_initial": 0.08097565, "C_limits": [-0.11902435, 0.28097565], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "3")] = {"B_initial": -0.19858658, "B_limits": [-0.39858658, 0.00141342], "C_initial": 0.01921514, "C_limits": [-0.18078486, 0.21921514], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("12", "7")] = {"B_initial": -0.07081919, "B_limits": [-0.27081919, 0.12918081], "C_initial": -0.01632308, "C_limits": [-0.21632308, 0.18367692], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "16")] = {"B_initial": -0.19046272, "B_limits": [-0.39046272, 0.00953728], "C_initial": -0.01630870, "C_limits": [-0.21630870, 0.18369130], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "9")] = {"B_initial": -0.20105021, "B_limits": [-0.40105021, -0.00105021], "C_initial": -0.00002394, "C_limits": [-0.20002394, 0.19997606], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "14")] = {"B_initial": -0.02900716, "B_limits": [-0.22900716, 0.17099284], "C_initial": 0.03454105, "C_limits": [-0.16545895, 0.23454105], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "3")] = {"B_initial": -0.17207616, "B_limits": [-0.37207616, 0.02792384], "C_initial": 0.01272148, "C_limits": [-0.18727852, 0.21272148], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "7")] = {"B_initial": -0.04731915, "B_limits": [-0.24731915, 0.15268085], "C_initial": 0.01855037, "C_limits": [-0.18144963, 0.21855037], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "12")] = {"B_initial": -0.25197789, "B_limits": [-0.45197789, -0.05197789], "C_initial": 0.04542607, "C_limits": [-0.15457393, 0.24542607], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "29")] = {"B_initial": -0.23367757, "B_limits": [-0.43367757, -0.03367757], "C_initial": 0.02208573, "C_limits": [-0.17791427, 0.22208573], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "7")] = {"B_initial": -0.04139224, "B_limits": [-0.24139224, 0.15860776], "C_initial": 0.01865892, "C_limits": [-0.18134108, 0.21865892], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("8", "19")] = {"B_initial": -0.15175530, "B_limits": [-0.35175530, 0.04824470], "C_initial": -0.02392847, "C_limits": [-0.22392847, 0.17607153], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "9")] = {"B_initial": -0.23176737, "B_limits": [-0.43176737, -0.03176737], "C_initial": -0.02737942, "C_limits": [-0.22737942, 0.17262058], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9")] = {"B_initial": -0.03456370, "B_limits": [-0.23456370, 0.16543630], "C_initial": -0.01374895, "C_limits": [-0.21374895, 0.18625105], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "21")] = {"B_initial": -0.14004135, "B_limits": [-0.34004135, 0.05995865], "C_initial": 0.00612468, "C_limits": [-0.19387532, 0.20612468], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "4")] = {"B_initial": -0.21715409, "B_limits": [-0.41715409, -0.01715409], "C_initial": -0.00469946, "C_limits": [-0.20469946, 0.19530054], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
