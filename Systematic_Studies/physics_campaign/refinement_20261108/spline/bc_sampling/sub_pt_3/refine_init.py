# Run-local BC_RC guide for spline sub_pt_3. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17 and 5 of 452 are narrower than 0.05, so the windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_pt_3", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.17187427, "B_limits": [-0.37187427, 0.02812573], "C_initial": 0.02763170, "C_limits": [-0.17236830, 0.22763170], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.17332221, "B_limits": [-0.37332221, 0.02667779], "C_initial": -0.00743988, "C_limits": [-0.20743988, 0.19256012], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.13127389, "B_limits": [-0.33127389, 0.06872611], "C_initial": -0.06502497, "C_limits": [-0.26502497, 0.13497503], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.01192246, "B_limits": [-0.18807754, 0.21192246], "C_initial": -0.01375336, "C_limits": [-0.21375336, 0.18624664], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.01299471, "B_limits": [-0.18700529, 0.21299471], "C_initial": -0.00555330, "C_limits": [-0.20555330, 0.19444670], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03507219, "B_limits": [-0.23507219, 0.16492781], "C_initial": -0.02687495, "C_limits": [-0.22687495, 0.17312505], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("12", "24", "3D", "BC")] = {"B_initial": -0.11311544, "B_limits": [-0.31311544, 0.08688456], "C_initial": 0.03029873, "C_limits": [-0.16970127, 0.23029873], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "15", "3D", "BC")] = {"B_initial": -0.06168475, "B_limits": [-0.26168475, 0.13831525], "C_initial": 0.01632193, "C_limits": [-0.18367807, 0.21632193], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.09639536, "B_limits": [-0.29639536, 0.10360464], "C_initial": 0.03836175, "C_limits": [-0.16163825, 0.23836175], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.22160374, "B_limits": [-0.42160374, -0.02160374], "C_initial": 0.09497799, "C_limits": [-0.10502201, 0.29497799], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07497418, "B_limits": [-0.27497418, 0.12502582], "C_initial": -0.00614207, "C_limits": [-0.20614207, 0.19385793], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19646236, "B_limits": [-0.39646236, 0.00353764], "C_initial": 0.00313744, "C_limits": [-0.19686256, 0.20313744], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.21780846, "B_limits": [-0.41780846, -0.01780846], "C_initial": 0.08819405, "C_limits": [-0.11180595, 0.28819405], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.23372838, "B_limits": [-0.43372838, -0.03372838], "C_initial": -0.04299244, "C_limits": [-0.24299244, 0.15700756], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24602226, "B_limits": [-0.44602226, -0.04602226], "C_initial": -0.03052519, "C_limits": [-0.23052519, 0.16947481], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.23968929, "B_limits": [-0.43968929, -0.03968929], "C_initial": 0.04783900, "C_limits": [-0.15216100, 0.24783900], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11752963, "B_limits": [-0.31752963, 0.08247037], "C_initial": -0.01312513, "C_limits": [-0.21312513, 0.18687487], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.15611744, "B_limits": [-0.35611744, 0.04388256], "C_initial": 0.03902441, "C_limits": [-0.16097559, 0.23902441], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.21253579, "B_limits": [-0.41253579, -0.01253579], "C_initial": 0.09606445, "C_limits": [-0.10393555, 0.29606445], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06743313, "B_limits": [-0.26743313, 0.13256687], "C_initial": -0.09451797, "C_limits": [-0.29451797, 0.10548203], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10460829, "B_limits": [-0.30460829, 0.09539171], "C_initial": -0.00391787, "C_limits": [-0.20391787, 0.19608213], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
