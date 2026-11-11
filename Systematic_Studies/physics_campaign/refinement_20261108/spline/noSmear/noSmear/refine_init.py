# Run-local guide for spline noSmear. The shared Phi_h files are not edited.
# start=auto chose the manual baseline. The 3D spline B windows selected by these
# histograms have median width 0.0153 and 428 of 452 are narrower than 0.05.
# The C windows are narrower (median 0.0070, 445 of 452). --use_spline_init is not used.
# Pass 1 used that baseline. Pass 2 puts only the misses on each histogram cosine
# and opens only the limits that excluded it. The second-pass half-width is turned
# off when it is narrower than that parameter's error.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

special_fit_parameters_set[("13", "4")] = {"B_initial": -0.26508932, "B_limits": [-0.46508932, -0.06508932], "C_initial": -0.02885941, "C_limits": [-0.22885941, 0.17114059], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18301700, "B_limits": [-0.38301700, 0.01698300], "C_initial": -0.00716648, "C_limits": [-0.20716648, 0.19283352], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26763296, "B_limits": [-0.46763296, -0.06763296], "C_initial": 0.00964133, "C_limits": [-0.19035867, 0.20964133], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "19")] = {"B_initial": -0.24602978, "B_limits": [-0.44602978, -0.04602978], "C_initial": 0.04768669, "C_limits": [-0.15231331, 0.24768669], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5")] = {"B_initial": -0.29926168, "B_limits": [-0.49926168, -0.09926168], "C_initial": -0.02218905, "C_limits": [-0.22218905, 0.17781095], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29")] = {"B_initial": -0.27873222, "B_limits": [-0.47873222, -0.07873222], "C_initial": 0.09362272, "C_limits": [-0.10637728, 0.29362272], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12965203, "B_limits": [-0.32965203, 0.07034797], "C_initial": 0.00392187, "C_limits": [-0.19607813, 0.20392187], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15")] = {"B_initial": -0.29634014, "B_limits": [-0.49634014, -0.09634014], "C_initial": 0.05845520, "C_limits": [-0.14154480, 0.25845520], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33")] = {"B_initial": -0.10642021, "B_limits": [-0.30642021, 0.09357979], "C_initial": -0.08988125, "C_limits": [-0.28988125, 0.11011875], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "24")] = {"B_initial": -0.26972731, "B_limits": [-0.46972731, -0.06972731], "C_initial": 0.06857901, "C_limits": [-0.13142099, 0.26857901], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "1")] = {"B_initial": -0.05791312, "B_limits": [-0.25791312, 0.14208688], "C_initial": 0.01088700, "C_limits": [-0.18911300, 0.21088700], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42567556, "B_limits": [-0.62567556, -0.22567556], "C_initial": 0.10872745, "C_limits": [-0.09127255, 0.30872745], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10647814, "B_limits": [-0.30647814, 0.09352186], "C_initial": -0.00905102, "C_limits": [-0.20905102, 0.19094898], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20")] = {"B_initial": -0.27050829, "B_limits": [-0.47050829, -0.07050829], "C_initial": 0.09552114, "C_limits": [-0.10447886, 0.29552114], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30282240, "B_limits": [-0.50282240, -0.10282240], "C_initial": 0.10076248, "C_limits": [-0.09923752, 0.30076248], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "2")] = {"B_initial": -0.11211675, "B_limits": [-0.31211675, 0.08788325], "C_initial": 0.03904823, "C_limits": [-0.16095177, 0.23904823], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34")] = {"B_initial": -0.15563644, "B_limits": [-0.35563644, 0.04436356], "C_initial": -0.00109809, "C_limits": [-0.20109809, 0.19890191], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36132517, "B_limits": [-0.56132517, -0.16132517], "C_initial": 0.10663650, "C_limits": [-0.09336350, 0.30663650], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "10")] = {"B_initial": -0.16916762, "B_limits": [-0.36916762, 0.03083238], "C_initial": 0.01916670, "C_limits": [-0.18083330, 0.21916670], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29")] = {"B_initial": -0.23654266, "B_limits": [-0.43654266, -0.03654266], "C_initial": 0.07469892, "C_limits": [-0.12530108, 0.27469892], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09493730, "B_limits": [-0.29493730, 0.10506270], "C_initial": -0.00880342, "C_limits": [-0.20880342, 0.19119658], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08535828, "B_limits": [-0.28535828, 0.11464172], "C_initial": -0.02371459, "C_limits": [-0.22371459, 0.17628541], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "2")] = {"B_initial": -0.14656004, "B_limits": [-0.34656004, 0.05343996], "C_initial": 0.02364200, "C_limits": [-0.17635800, 0.22364200], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("12", "24")] = {"B_initial": -0.12213476, "B_limits": [-0.32213476, 0.07786524], "C_initial": 0.00765556, "C_limits": [-0.19234444, 0.20765556], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31")] = {"B_initial": 0.00236029, "B_limits": [-0.19763971, 0.20236029], "C_initial": 0.04151635, "C_limits": [-0.15848365, 0.24151635], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "22")] = {"B_initial": -0.02581891, "B_limits": [-0.22581891, 0.17418109], "C_initial": 0.03438483, "C_limits": [-0.16561517, 0.23438483], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "11")] = {"B_initial": -0.25855690, "B_limits": [-0.45855690, -0.05855690], "C_initial": 0.02536601, "C_limits": [-0.17463399, 0.22536601], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "4")] = {"B_initial": -0.23064971, "B_limits": [-0.43064971, -0.03064971], "C_initial": 0.02476544, "C_limits": [-0.17523456, 0.22476544], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "24")] = {"B_initial": -0.19642729, "B_limits": [-0.39642729, 0.00357271], "C_initial": 0.05095480, "C_limits": [-0.14904520, 0.25095480], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "3")] = {"B_initial": -0.16723706, "B_limits": [-0.36723706, 0.03276294], "C_initial": 0.01468004, "C_limits": [-0.18531996, 0.21468004], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2")] = {"B_initial": -0.13388793, "B_limits": [-0.33388793, 0.06611207], "C_initial": 0.02973513, "C_limits": [-0.17026487, 0.22973513], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "8")] = {"B_initial": -0.12414939, "B_limits": [-0.32414939, 0.07585061], "C_initial": -0.04196782, "C_limits": [-0.24196782, 0.15803218], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35")] = {"B_initial": -0.26228876, "B_limits": [-0.46228876, -0.06228876], "C_initial": 0.08436610, "C_limits": [-0.11563390, 0.28436610], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "19")] = {"B_initial": -0.03259356, "B_limits": [-0.23259356, 0.16740644], "C_initial": -0.00637259, "C_limits": [-0.20637259, 0.19362741], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "16")] = {"B_initial": -0.19209310, "B_limits": [-0.39209310, 0.00790690], "C_initial": -0.01764430, "C_limits": [-0.21764430, 0.18235570], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "3")] = {"B_initial": -0.19839943, "B_limits": [-0.39839943, 0.00160057], "C_initial": 0.02035939, "C_limits": [-0.17964061, 0.22035939], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "16")] = {"B_initial": -0.17776208, "B_limits": [-0.37776208, 0.02223792], "C_initial": -0.01163789, "C_limits": [-0.21163789, 0.18836211], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("17", "2")] = {"B_initial": -0.06757817, "B_limits": [-0.26757817, 0.13242183], "C_initial": -0.00540076, "C_limits": [-0.20540076, 0.19459924], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "29")] = {"B_initial": -0.24125200, "B_limits": [-0.44125200, -0.04125200], "C_initial": 0.02795877, "C_limits": [-0.17204123, 0.22795877], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "9")] = {"B_initial": -0.20255033, "B_limits": [-0.40255033, -0.00255033], "C_initial": 0.00038060, "C_limits": [-0.19961940, 0.20038060], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("12", "7")] = {"B_initial": -0.07165935, "B_limits": [-0.27165935, 0.12834065], "C_initial": -0.01718561, "C_limits": [-0.21718561, 0.18281439], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "14")] = {"B_initial": -0.02825347, "B_limits": [-0.22825347, 0.17174653], "C_initial": 0.03629856, "C_limits": [-0.16370144, 0.23629856], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "7")] = {"B_initial": -0.04772972, "B_limits": [-0.24772972, 0.15227028], "C_initial": 0.01936823, "C_limits": [-0.18063177, 0.21936823], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "8")] = {"B_initial": -0.05639059, "B_limits": [-0.25639059, 0.14360941], "C_initial": 0.02587129, "C_limits": [-0.17412871, 0.22587129], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "15")] = {"B_initial": -0.10791992, "B_limits": [-0.30791992, 0.09208008], "C_initial": 0.00076838, "C_limits": [-0.19923162, 0.20076838], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "7")] = {"B_initial": -0.04181129, "B_limits": [-0.24181129, 0.15818871], "C_initial": 0.01775552, "C_limits": [-0.18224448, 0.21775552], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "9")] = {"B_initial": -0.23370436, "B_limits": [-0.43370436, -0.03370436], "C_initial": -0.03120044, "C_limits": [-0.23120044, 0.16879956], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("8", "30")] = {"B_initial": -0.18050649, "B_limits": [-0.38050649, 0.01949351], "C_initial": 0.01944373, "C_limits": [-0.18055627, 0.21944373], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "21")] = {"B_initial": -0.13962403, "B_limits": [-0.33962403, 0.06037597], "C_initial": 0.00626600, "C_limits": [-0.19373400, 0.20626600], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "15")] = {"B_initial": -0.11245744, "B_limits": [-0.31245744, 0.08754256], "C_initial": -0.00130859, "C_limits": [-0.20130859, 0.19869141], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "4")] = {"B_initial": -0.21992319, "B_limits": [-0.41992319, -0.01992319], "C_initial": -0.00423746, "C_limits": [-0.20423746, 0.19576254], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
