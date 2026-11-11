# Run-local unweighted 5D Bayesian guide.
# start=auto chose the universal spline file. These histogram names select ("q", "z", "5D") when that key exists, otherwise ("q", "z").
# Selected B windows: median width 0.2225 on 192 limited bins, 4 of 452 narrower than 0.05, and 260 with no B limits. C windows are wider. They are not tight enough to pin the fits.
# The unweighted nominal acceptance refinement is a comparison source. Its central values are not copied onto these histograms.
# The shared Phi_h files are not edited. --use_spline_init is not passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. Pass 1 used the spline file. These histograms missed their own cosine.
# The 5D key is more specific than the untagged spline key, so only these bins change.
# Starts are the wide-limit cosine of this histogram, not the nominal 3D value.
# Restored: the spline start or its limits sent the second fit pass off the stored cosine.
special_fit_parameters_set[("1", "8", "5D")] = {"B_initial": -0.02849924, "B_limits": [-0.17849924, 0.12150076], "C_initial": 0.01576316, "C_limits": [-0.08423684, 0.11576316], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("2", "16", "5D")] = {"B_initial": -0.18436157, "B_limits": [-0.33436157, -0.03436157], "C_initial": 0.00710783, "C_limits": [-0.09289217, 0.10710783], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("2", "29", "5D")] = {"B_initial": -0.27085890, "B_limits": [-0.42085890, -0.12085890], "C_initial": 0.07805696, "C_limits": [-0.02194304, 0.17805696], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("3", "16", "5D")] = {"B_initial": -0.18172055, "B_limits": [-0.33172055, -0.03172055], "C_initial": -0.00567238, "C_limits": [-0.10567238, 0.09432762], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("3", "29", "5D")] = {"B_initial": -0.27892346, "B_limits": [-0.42892346, -0.12892346], "C_initial": 0.07761130, "C_limits": [-0.02238870, 0.17761130], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("5", "3", "5D")] = {"B_initial": -0.18908615, "B_limits": [-0.33908615, -0.03908615], "C_initial": 0.02034082, "C_limits": [-0.07965918, 0.12034082], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("5", "31", "5D")] = {"B_initial": 0.00597903, "B_limits": [-0.14402097, 0.15597903], "C_initial": 0.03927117, "C_limits": [-0.06072883, 0.13927117], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("6", "6", "5D")] = {"B_initial": -0.40454707, "B_limits": [-0.55454707, -0.25454707], "C_initial": 0.04527461, "C_limits": [-0.05472539, 0.14527461], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("9", "4", "5D")] = {"B_initial": -0.20726812, "B_limits": [-0.35726812, -0.05726812], "C_initial": -0.00151016, "C_limits": [-0.10151016, 0.09848984], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("12", "24", "5D")] = {"B_initial": -0.12194526, "B_limits": [-0.27194526, 0.02805474], "C_initial": 0.00520836, "C_limits": [-0.09479164, 0.10520836], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("13", "10", "5D")] = {"B_initial": -0.34490256, "B_limits": [-0.49490256, -0.19490256], "C_initial": 0.07615015, "C_limits": [-0.02384985, 0.17615015], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("14", "5", "5D")] = {"B_initial": -0.30925883, "B_limits": [-0.45925883, -0.15925883], "C_initial": -0.03178142, "C_limits": [-0.13178142, 0.06821858], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
special_fit_parameters_set[("15", "15", "5D")] = {"B_initial": -0.31735822, "B_limits": [-0.46735822, -0.16735822], "C_initial": 0.06211285, "C_limits": [-0.03788715, 0.16211285], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # restore
# Opened: the stored fit is off this histogram's wide-limit cosine, so the limit or the moment window was too tight.
special_fit_parameters_set[("1", "18", "5D")] = {"B_initial": -0.18337939, "B_limits": [-0.33337939, -0.03337939], "C_initial": 0.01778684, "C_limits": [-0.08221316, 0.11778684], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("1", "22", "5D")] = {"B_initial": -0.02382204, "B_limits": [-0.17382204, 0.12617796], "C_initial": 0.02347925, "C_limits": [-0.07652075, 0.12347925], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("2", "34", "5D")] = {"B_initial": -0.19736506, "B_limits": [-0.34736506, -0.04736506], "C_initial": 0.01305543, "C_limits": [-0.08694457, 0.11305543], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("3", "2", "5D")] = {"B_initial": -0.15017531, "B_limits": [-0.30017531, -0.00017531], "C_initial": 0.01187902, "C_limits": [-0.08812098, 0.11187902], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("3", "3", "5D")] = {"B_initial": -0.18178215, "B_limits": [-0.33178215, -0.03178215], "C_initial": -0.00078463, "C_limits": [-0.10078463, 0.09921537], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("3", "24", "5D")] = {"B_initial": -0.32596192, "B_limits": [-0.47596192, -0.17596192], "C_initial": 0.08550463, "C_limits": [-0.01449537, 0.18550463], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("4", "19", "5D")] = {"B_initial": -0.03085280, "B_limits": [-0.18085280, 0.11914720], "C_initial": -0.00529802, "C_limits": [-0.10529802, 0.09470198], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("4", "29", "5D")] = {"B_initial": -0.27115400, "B_limits": [-0.42115400, -0.12115400], "C_initial": 0.03679568, "C_limits": [-0.06320432, 0.13679568], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("5", "7", "5D")] = {"B_initial": -0.02458880, "B_limits": [-0.17458880, 0.12541120], "C_initial": 0.03118957, "C_limits": [-0.06881043, 0.13118957], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("7", "16", "5D")] = {"B_initial": -0.18858683, "B_limits": [-0.33858683, -0.03858683], "C_initial": -0.01437224, "C_limits": [-0.11437224, 0.08562776], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("7", "21", "5D")] = {"B_initial": -0.09510679, "B_limits": [-0.24510679, 0.05489321], "C_initial": -0.01119190, "C_limits": [-0.11119190, 0.08880810], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("7", "35", "5D")] = {"B_initial": -0.26793913, "B_limits": [-0.41793913, -0.11793913], "C_initial": 0.07137814, "C_limits": [-0.02862186, 0.17137814], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("8", "28", "5D")] = {"B_initial": -0.13876181, "B_limits": [-0.28876181, 0.01123819], "C_initial": -0.03783447, "C_limits": [-0.13783447, 0.06216553], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("8", "30", "5D")] = {"B_initial": -0.23892894, "B_limits": [-0.38892894, -0.08892894], "C_initial": 0.03917333, "C_limits": [-0.06082667, 0.13917333], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("11", "3", "5D")] = {"B_initial": -0.12583956, "B_limits": [-0.27583956, 0.02416044], "C_initial": -0.00852468, "C_limits": [-0.10852468, 0.09147532], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("12", "7", "5D")] = {"B_initial": -0.06319104, "B_limits": [-0.21319104, 0.08680896], "C_initial": -0.01623066, "C_limits": [-0.11623066, 0.08376934], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("13", "9", "5D")] = {"B_initial": -0.19343117, "B_limits": [-0.34343117, -0.04343117], "C_initial": -0.00285636, "C_limits": [-0.10285636, 0.09714364], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("14", "29", "5D")] = {"B_initial": -0.26843123, "B_limits": [-0.41843123, -0.11843123], "C_initial": 0.05565505, "C_limits": [-0.04434495, 0.15565505], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("15", "9", "5D")] = {"B_initial": -0.24646121, "B_limits": [-0.39646121, -0.09646121], "C_initial": -0.03539853, "C_limits": [-0.13539853, 0.06460147], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("15", "24", "5D")] = {"B_initial": -0.22328301, "B_limits": [-0.37328301, -0.07328301], "C_initial": 0.05520103, "C_limits": [-0.04479897, 0.15520103], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("16", "12", "5D")] = {"B_initial": -0.37250192, "B_limits": [-0.52250192, -0.22250192], "C_initial": 0.09874936, "C_limits": [-0.00125064, 0.19874936], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("16", "16", "5D")] = {"B_initial": -0.15936962, "B_limits": [-0.30936962, -0.00936962], "C_initial": -0.00944789, "C_limits": [-0.10944789, 0.09055211], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
special_fit_parameters_set[("17", "2", "5D")] = {"B_initial": -0.06525544, "B_limits": [-0.21525544, 0.08474456], "C_initial": -0.00460221, "C_limits": [-0.10460221, 0.09539779], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}  # open
# (12, 13): the spline 5D key cut phi to 15-345 and dropped a nonempty bin at 0-15 degrees. The filled window is 0-345. No fit_range is set, so the remake uses that window.
special_fit_parameters_set[("12", "13", "5D")] = {"B_initial": -0.09797778, "B_limits": [-0.24797778, 0.05202222], "C_initial": -0.05177642, "C_limits": [-0.15177642, 0.04822358], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
