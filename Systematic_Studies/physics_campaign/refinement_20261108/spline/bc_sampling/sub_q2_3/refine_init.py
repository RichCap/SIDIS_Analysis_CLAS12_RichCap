# Run-local BC_RC guide for spline sub_q2_3. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17, 5 of 452 are narrower than 0.05, and 305 leave B unlimited.
# C median width is 0.10, with 10 narrower than 0.05 and 364 unlimited. The windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_q2_3", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.17324043, "B_limits": [-0.37324043, 0.02675957], "C_initial": -0.01111175, "C_limits": [-0.21111175, 0.18888825], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.13035523, "B_limits": [-0.33035523, 0.06964477], "C_initial": -0.05825429, "C_limits": [-0.25825429, 0.14174571], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03318713, "B_limits": [-0.23318713, 0.16681287], "C_initial": -0.02486230, "C_limits": [-0.22486230, 0.17513770], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.01029887, "B_limits": [-0.18970113, 0.21029887], "C_initial": 0.04140462, "C_limits": [-0.15859538, 0.24140462], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11262018, "B_limits": [-0.31262018, 0.08737982], "C_initial": -0.01595676, "C_limits": [-0.21595676, 0.18404324], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14450157, "B_limits": [-0.34450157, 0.05549843], "C_initial": 0.04435881, "C_limits": [-0.15564119, 0.24435881], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20881230, "B_limits": [-0.40881230, -0.00881230], "C_initial": 0.08737948, "C_limits": [-0.11262052, 0.28737948], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.07017869, "B_limits": [-0.27017869, 0.12982131], "C_initial": -0.09216865, "C_limits": [-0.29216865, 0.10783135], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10450826, "B_limits": [-0.30450826, 0.09549174], "C_initial": -0.01039177, "C_limits": [-0.21039177, 0.18960823], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02384292, "B_limits": [-0.17615708, 0.22384292], "C_initial": 0.03899206, "C_limits": [-0.16100794, 0.23899206], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "1", "3D", "BC")] = {"B_initial": -0.04110267, "B_limits": [-0.24110267, 0.15889733], "C_initial": 0.02445628, "C_limits": [-0.17554372, 0.22445628], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.09949787, "B_limits": [-0.29949787, 0.10050213], "C_initial": 0.04067385, "C_limits": [-0.15932615, 0.24067385], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19362443, "B_limits": [-0.39362443, 0.00637557], "C_initial": 0.00078241, "C_limits": [-0.19921759, 0.20078241], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20905135, "B_limits": [-0.40905135, -0.00905135], "C_initial": 0.08504107, "C_limits": [-0.11495893, 0.28504107], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.23643357, "B_limits": [-0.43643357, -0.03643357], "C_initial": -0.04672315, "C_limits": [-0.24672315, 0.15327685], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.22026373, "B_limits": [-0.42026373, -0.02026373], "C_initial": 0.05695069, "C_limits": [-0.14304931, 0.25695069], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
