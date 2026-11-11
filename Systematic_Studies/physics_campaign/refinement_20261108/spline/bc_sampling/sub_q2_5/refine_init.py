# Run-local BC_RC guide for spline sub_q2_5. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17, 5 of 452 are narrower than 0.05, and 305 leave B unlimited.
# C median width is 0.10, with 10 narrower than 0.05 and 364 unlimited. The windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_q2_5", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.17495434, "B_limits": [-0.37495434, 0.02504566], "C_initial": -0.01176070, "C_limits": [-0.21176070, 0.18823930], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.12631425, "B_limits": [-0.32631425, 0.07368575], "C_initial": -0.05510889, "C_limits": [-0.25510889, 0.14489111], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.00305050, "B_limits": [-0.19694950, 0.20305050], "C_initial": -0.01217584, "C_limits": [-0.21217584, 0.18782416], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03341819, "B_limits": [-0.23341819, 0.16658181], "C_initial": -0.02484943, "C_limits": [-0.22484943, 0.17515057], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.00953484, "B_limits": [-0.19046516, 0.20953484], "C_initial": 0.04108114, "C_limits": [-0.15891886, 0.24108114], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11381083, "B_limits": [-0.31381083, 0.08618917], "C_initial": -0.01587234, "C_limits": [-0.21587234, 0.18412766], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14377150, "B_limits": [-0.34377150, 0.05622850], "C_initial": 0.04340585, "C_limits": [-0.15659415, 0.24340585], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20778371, "B_limits": [-0.40778371, -0.00778371], "C_initial": 0.08687323, "C_limits": [-0.11312677, 0.28687323], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.07035225, "B_limits": [-0.27035225, 0.12964775], "C_initial": -0.09260258, "C_limits": [-0.29260258, 0.10739742], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10414475, "B_limits": [-0.30414475, 0.09585525], "C_initial": -0.01001798, "C_limits": [-0.21001798, 0.18998202], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "4", "3D", "BC")] = {"B_initial": -0.17666910, "B_limits": [-0.37666910, 0.02333090], "C_initial": 0.01145216, "C_limits": [-0.18854784, 0.21145216], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02335302, "B_limits": [-0.17664698, 0.22335302], "C_initial": 0.03952894, "C_limits": [-0.16047106, 0.23952894], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "1", "3D", "BC")] = {"B_initial": -0.04044734, "B_limits": [-0.24044734, 0.15955266], "C_initial": 0.02248219, "C_limits": [-0.17751781, 0.22248219], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.09907052, "B_limits": [-0.29907052, 0.10092948], "C_initial": 0.04018032, "C_limits": [-0.15981968, 0.24018032], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.21313149, "B_limits": [-0.41313149, -0.01313149], "C_initial": 0.08539359, "C_limits": [-0.11460641, 0.28539359], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("9", "7", "3D", "BC")] = {"B_initial": -0.32241925, "B_limits": [-0.52241925, -0.12241925], "C_initial": 0.08680325, "C_limits": [-0.11319675, 0.28680325], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19418904, "B_limits": [-0.39418904, 0.00581096], "C_initial": 0.00100237, "C_limits": [-0.19899763, 0.20100237], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20864512, "B_limits": [-0.40864512, -0.00864512], "C_initial": 0.08461835, "C_limits": [-0.11538165, 0.28461835], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.23507663, "B_limits": [-0.43507663, -0.03507663], "C_initial": -0.04681338, "C_limits": [-0.24681338, 0.15318662], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.21982893, "B_limits": [-0.41982893, -0.01982893], "C_initial": 0.05727943, "C_limits": [-0.14272057, 0.25727943], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
