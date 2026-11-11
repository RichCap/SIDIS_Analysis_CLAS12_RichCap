# Run-local BC_RC guide for spline sub_pt_7. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17 and 5 of 452 are narrower than 0.05, so the windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_pt_7", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.17857201, "B_limits": [-0.37857201, 0.02142799], "C_initial": 0.02268179, "C_limits": [-0.17731821, 0.22268179], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.17800278, "B_limits": [-0.37800278, 0.02199722], "C_initial": -0.01046055, "C_limits": [-0.21046055, 0.18953945], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.13109664, "B_limits": [-0.33109664, 0.06890336], "C_initial": -0.06654059, "C_limits": [-0.26654059, 0.13345941], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.00844271, "B_limits": [-0.19155729, 0.20844271], "C_initial": -0.01576169, "C_limits": [-0.21576169, 0.18423831], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.01391371, "B_limits": [-0.18608629, 0.21391371], "C_initial": -0.00501767, "C_limits": [-0.20501767, 0.19498233], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03628846, "B_limits": [-0.23628846, 0.16371154], "C_initial": -0.02591633, "C_limits": [-0.22591633, 0.17408367], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("12", "24", "3D", "BC")] = {"B_initial": -0.10736501, "B_limits": [-0.30736501, 0.09263499], "C_initial": 0.02182334, "C_limits": [-0.17817666, 0.22182334], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "14", "3D", "BC")] = {"B_initial": 0.01266277, "B_limits": [-0.18733723, 0.21266277], "C_initial": 0.02926655, "C_limits": [-0.17073345, 0.22926655], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.14821675, "B_limits": [-0.34821675, 0.05178325], "C_initial": 0.05938823, "C_limits": [-0.14061177, 0.25938823], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "15", "3D", "BC")] = {"B_initial": -0.06327619, "B_limits": [-0.26327619, 0.13672381], "C_initial": 0.01635132, "C_limits": [-0.18364868, 0.21635132], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.09874104, "B_limits": [-0.29874104, 0.10125896], "C_initial": 0.03479785, "C_limits": [-0.16520215, 0.23479785], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.21634917, "B_limits": [-0.41634917, -0.01634917], "C_initial": 0.09026081, "C_limits": [-0.10973919, 0.29026081], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07471480, "B_limits": [-0.27471480, 0.12528520], "C_initial": -0.00817233, "C_limits": [-0.20817233, 0.19182767], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19915550, "B_limits": [-0.39915550, 0.00084450], "C_initial": 0.00130571, "C_limits": [-0.19869429, 0.20130571], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.21731722, "B_limits": [-0.41731722, -0.01731722], "C_initial": 0.08670832, "C_limits": [-0.11329168, 0.28670832], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.22858908, "B_limits": [-0.42858908, -0.02858908], "C_initial": -0.04178272, "C_limits": [-0.24178272, 0.15821728], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24723777, "B_limits": [-0.44723777, -0.04723777], "C_initial": -0.03293282, "C_limits": [-0.23293282, 0.16706718], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.24159898, "B_limits": [-0.44159898, -0.04159898], "C_initial": 0.04697916, "C_limits": [-0.15302084, 0.24697916], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11818345, "B_limits": [-0.31818345, 0.08181655], "C_initial": -0.01336440, "C_limits": [-0.21336440, 0.18663560], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.15675954, "B_limits": [-0.35675954, 0.04324046], "C_initial": 0.03849598, "C_limits": [-0.16150402, 0.23849598], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.21034203, "B_limits": [-0.41034203, -0.01034203], "C_initial": 0.09283101, "C_limits": [-0.10716899, 0.29283101], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06719231, "B_limits": [-0.26719231, 0.13280769], "C_initial": -0.09447026, "C_limits": [-0.29447026, 0.10552974], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10504261, "B_limits": [-0.30504261, 0.09495739], "C_initial": -0.00514883, "C_limits": [-0.20514883, 0.19485117], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
