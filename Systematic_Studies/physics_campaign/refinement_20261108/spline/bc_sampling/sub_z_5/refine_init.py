# Run-local BC_RC guide for spline kinematic-sampling sub_z_5.
# The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17, 5 of 452 are narrower than 0.05, and 305 leave B unlimited, so the windows are not tight.
# --use_spline_init is not also passed. Nominal parameters are not copied onto these histograms.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_z_5", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.21318670, "B_limits": [-0.41318670, -0.01318670], "C_initial": 0.09479068, "C_limits": [-0.10520932, 0.29479068], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.23742479, "B_limits": [-0.43742479, -0.03742479], "C_initial": 0.04654606, "C_limits": [-0.15345394, 0.24654606], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14876569, "B_limits": [-0.34876569, 0.05123431], "C_initial": 0.04019878, "C_limits": [-0.15980122, 0.24019878], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11771331, "B_limits": [-0.31771331, 0.08228669], "C_initial": -0.01593327, "C_limits": [-0.21593327, 0.18406673], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.21266914, "B_limits": [-0.41266914, -0.01266914], "C_initial": 0.08648528, "C_limits": [-0.11351472, 0.28648528], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.24991141, "B_limits": [-0.44991141, -0.04991141], "C_initial": -0.04870076, "C_limits": [-0.24870076, 0.15129924], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.07216191, "B_limits": [-0.27216191, 0.12783809], "C_initial": -0.09172281, "C_limits": [-0.29172281, 0.10827719], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.00606002, "B_limits": [-0.19393998, 0.20606002], "C_initial": 0.03858119, "C_limits": [-0.16141881, 0.23858119], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10748117, "B_limits": [-0.30748117, 0.09251883], "C_initial": -0.00799113, "C_limits": [-0.20799113, 0.19200887], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19824516, "B_limits": [-0.39824516, 0.00175484], "C_initial": 0.00076917, "C_limits": [-0.19923083, 0.20076917], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02274413, "B_limits": [-0.17725587, 0.22274413], "C_initial": 0.03759522, "C_limits": [-0.16240478, 0.23759522], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03448774, "B_limits": [-0.23448774, 0.16551226], "C_initial": -0.02537831, "C_limits": [-0.22537831, 0.17462169], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24669403, "B_limits": [-0.44669403, -0.04669403], "C_initial": -0.02023515, "C_limits": [-0.22023515, 0.17976485], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.21578876, "B_limits": [-0.41578876, -0.01578876], "C_initial": 0.09003046, "C_limits": [-0.10996954, 0.29003046], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.13508904, "B_limits": [-0.33508904, 0.06491096], "C_initial": -0.06078138, "C_limits": [-0.26078138, 0.13921862], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
# (2, 29) C is on the second-pass edge and the cosine is outside the C window.
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.14502810, "B_limits": [-0.34502810, 0.05497190], "C_initial": 0.05742261, "C_limits": [-0.14257739, 0.25742261], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
