# Run-local BC_RC guide for spline phi_h sampling sub_phi_9.
# The shared Phi_h files are not edited.
# start=auto chose the universal spline file.
# A BC_RC histogram selects untagged or BC keys, not the tight 3D acceptance windows.
# Selected B widths have median 0.17, and 305 of 452 bins leave B unlimited.
# --use_spline_init is not also passed. Nominal parameters are not copied onto these histograms.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2: pinned or second-pass bins. Starts are this histogram's weighted cosine, not the nominal.

special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.17932570, "B_limits": [-0.29932570, -0.05932570], "C_initial": 0.02315326, "C_limits": [-0.09684674, 0.14315326], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.18531589, "B_limits": [-0.30531589, -0.06531589], "C_initial": -0.01690027, "C_limits": [-0.13690027, 0.10309973], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.10836321, "B_limits": [-0.22836321, 0.01163679], "C_initial": -0.04584888, "C_limits": [-0.16584888, 0.07415112], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.00187836, "B_limits": [-0.11812164, 0.12187836], "C_initial": -0.02005159, "C_limits": [-0.14005159, 0.09994841], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.01269821, "B_limits": [-0.10730179, 0.13269821], "C_initial": -0.00338917, "C_limits": [-0.12338917, 0.11661083], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03693972, "B_limits": [-0.15693972, 0.08306028], "C_initial": -0.02704719, "C_limits": [-0.14704719, 0.09295281], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": -0.00051889, "B_limits": [-0.12051889, 0.11948111], "C_initial": 0.03289885, "C_limits": [-0.08710115, 0.15289885], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.12212395, "B_limits": [-0.24212395, -0.00212395], "C_initial": -0.01567468, "C_limits": [-0.13567468, 0.10432532], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14840887, "B_limits": [-0.26840887, -0.02840887], "C_initial": 0.04090295, "C_limits": [-0.07909705, 0.16090295], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20519662, "B_limits": [-0.32519662, -0.08519662], "C_initial": 0.08063643, "C_limits": [-0.03936357, 0.20063643], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06853178, "B_limits": [-0.18853178, 0.05146822], "C_initial": -0.09464440, "C_limits": [-0.21464440, 0.02535560], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10411713, "B_limits": [-0.22411713, 0.01588287], "C_initial": -0.00556424, "C_limits": [-0.12556424, 0.11443576], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "6", "3D", "BC")] = {"B_initial": -0.22597842, "B_limits": [-0.34597842, -0.10597842], "C_initial": 0.03999291, "C_limits": [-0.08000709, 0.15999291], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02417604, "B_limits": [-0.09582396, 0.14417604], "C_initial": 0.03867904, "C_limits": [-0.08132096, 0.15867904], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.10358597, "B_limits": [-0.22358597, 0.01641403], "C_initial": 0.02863859, "C_limits": [-0.09136141, 0.14863859], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07540867, "B_limits": [-0.19540867, 0.04459133], "C_initial": -0.00884362, "C_limits": [-0.12884362, 0.11115638], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19880109, "B_limits": [-0.31880109, -0.07880109], "C_initial": -0.00451714, "C_limits": [-0.12451714, 0.11548286], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20908152, "B_limits": [-0.32908152, -0.08908152], "C_initial": 0.08119860, "C_limits": [-0.03880140, 0.20119860], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.22171642, "B_limits": [-0.34171642, -0.10171642], "C_initial": -0.04102129, "C_limits": [-0.16102129, 0.07897871], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24681256, "B_limits": [-0.36681256, -0.12681256], "C_initial": -0.03819996, "C_limits": [-0.15819996, 0.08180004], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.24049736, "B_limits": [-0.36049736, -0.12049736], "C_initial": 0.04157923, "C_limits": [-0.07842077, 0.16157923], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
