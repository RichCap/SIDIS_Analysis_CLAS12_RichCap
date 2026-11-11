# Run-local BC_RC guide for spline kinematic-sampling sub_z_3.
# The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17, 5 of 452 are narrower than 0.05, and 305 leave B unlimited, so the windows are not tight.
# --use_spline_init is not also passed. Nominal parameters are not copied onto these histograms.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_z_3", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.13598832, "B_limits": [-0.33598832, 0.06401168], "C_initial": -0.06172923, "C_limits": [-0.26172923, 0.13827077], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03476069, "B_limits": [-0.23476069, 0.16523931], "C_initial": -0.02488774, "C_limits": [-0.22488774, 0.17511226], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.00724021, "B_limits": [-0.19275979, 0.20724021], "C_initial": 0.03984243, "C_limits": [-0.16015757, 0.23984243], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.14523032, "B_limits": [-0.34523032, 0.05476968], "C_initial": 0.05851778, "C_limits": [-0.14148222, 0.25851778], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11639151, "B_limits": [-0.31639151, 0.08360849], "C_initial": -0.01573997, "C_limits": [-0.21573997, 0.18426003], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14839059, "B_limits": [-0.34839059, 0.05160941], "C_initial": 0.04021399, "C_limits": [-0.15978601, 0.24021399], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.21372326, "B_limits": [-0.41372326, -0.01372326], "C_initial": 0.09655608, "C_limits": [-0.10344392, 0.29655608], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.07210252, "B_limits": [-0.27210252, 0.12789748], "C_initial": -0.09136908, "C_limits": [-0.29136908, 0.10863092], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10737668, "B_limits": [-0.30737668, 0.09262332], "C_initial": -0.00776633, "C_limits": [-0.20776633, 0.19223367], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02359276, "B_limits": [-0.17640724, 0.22359276], "C_initial": 0.03801620, "C_limits": [-0.16198380, 0.23801620], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.21830132, "B_limits": [-0.41830132, -0.01830132], "C_initial": 0.09307193, "C_limits": [-0.10692807, 0.29307193], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19704639, "B_limits": [-0.39704639, 0.00295361], "C_initial": 0.00223158, "C_limits": [-0.19776842, 0.20223158], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.21265724, "B_limits": [-0.41265724, -0.01265724], "C_initial": 0.08722647, "C_limits": [-0.11277353, 0.28722647], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.24920950, "B_limits": [-0.44920950, -0.04920950], "C_initial": -0.04870582, "C_limits": [-0.24870582, 0.15129418], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24526723, "B_limits": [-0.44526723, -0.04526723], "C_initial": -0.02007519, "C_limits": [-0.22007519, 0.17992481], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.23631716, "B_limits": [-0.43631716, -0.03631716], "C_initial": 0.04735187, "C_limits": [-0.15264813, 0.24735187], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
