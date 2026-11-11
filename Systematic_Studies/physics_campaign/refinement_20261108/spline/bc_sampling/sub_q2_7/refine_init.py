# Run-local BC_RC guide for spline sub_q2_7. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17, 5 of 452 are narrower than 0.05, and 305 leave B unlimited.
# C median width is 0.10, with 10 narrower than 0.05 and 364 unlimited. The windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_q2_7", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.17533101, "B_limits": [-0.37533101, 0.02466899], "C_initial": -0.01197962, "C_limits": [-0.21197962, 0.18802038], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.12427164, "B_limits": [-0.32427164, 0.07572836], "C_initial": -0.05400209, "C_limits": [-0.25400209, 0.14599791], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.00562475, "B_limits": [-0.19437525, 0.20562475], "C_initial": -0.01086420, "C_limits": [-0.21086420, 0.18913580], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03325109, "B_limits": [-0.23325109, 0.16674891], "C_initial": -0.02513511, "C_limits": [-0.22513511, 0.17486489], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.00898491, "B_limits": [-0.19101509, 0.20898491], "C_initial": 0.04026048, "C_limits": [-0.15973952, 0.24026048], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11441782, "B_limits": [-0.31441782, 0.08558218], "C_initial": -0.01578996, "C_limits": [-0.21578996, 0.18421004], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14332913, "B_limits": [-0.34332913, 0.05667087], "C_initial": 0.04272865, "C_limits": [-0.15727135, 0.24272865], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20692112, "B_limits": [-0.40692112, -0.00692112], "C_initial": 0.08610064, "C_limits": [-0.11389936, 0.28610064], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.07046714, "B_limits": [-0.27046714, 0.12953286], "C_initial": -0.09264357, "C_limits": [-0.29264357, 0.10735643], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10404939, "B_limits": [-0.30404939, 0.09595061], "C_initial": -0.00927127, "C_limits": [-0.20927127, 0.19072873], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "4", "3D", "BC")] = {"B_initial": -0.17772490, "B_limits": [-0.37772490, 0.02227510], "C_initial": 0.00935388, "C_limits": [-0.19064612, 0.20935388], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02375813, "B_limits": [-0.17624187, 0.22375813], "C_initial": 0.04026977, "C_limits": [-0.15973023, 0.24026977], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "1", "3D", "BC")] = {"B_initial": -0.03938008, "B_limits": [-0.23938008, 0.16061992], "C_initial": 0.02034811, "C_limits": [-0.17965189, 0.22034811], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.09877262, "B_limits": [-0.29877262, 0.10122738], "C_initial": 0.03945784, "C_limits": [-0.16054216, 0.23945784], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.21125951, "B_limits": [-0.41125951, -0.01125951], "C_initial": 0.08436022, "C_limits": [-0.11563978, 0.28436022], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("9", "7", "3D", "BC")] = {"B_initial": -0.32328180, "B_limits": [-0.52328180, -0.12328180], "C_initial": 0.08633461, "C_limits": [-0.11366539, 0.28633461], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19422298, "B_limits": [-0.39422298, 0.00577702], "C_initial": 0.00047610, "C_limits": [-0.19952390, 0.20047610], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20868700, "B_limits": [-0.40868700, -0.00868700], "C_initial": 0.08458125, "C_limits": [-0.11541875, 0.28458125], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.23461994, "B_limits": [-0.43461994, -0.03461994], "C_initial": -0.04593132, "C_limits": [-0.24593132, 0.15406868], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.22771037, "B_limits": [-0.42771037, -0.02771037], "C_initial": -0.01486926, "C_limits": [-0.21486926, 0.18513074], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.22004875, "B_limits": [-0.42004875, -0.02004875], "C_initial": 0.05698218, "C_limits": [-0.14301782, 0.25698218], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
