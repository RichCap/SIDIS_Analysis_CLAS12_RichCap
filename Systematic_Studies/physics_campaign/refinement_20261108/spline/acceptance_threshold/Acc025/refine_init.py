# Run-local Acc025 guide. The shared Phi_h files are not edited.
# start=auto chose the manual baseline. The 3D spline B windows for these
# 452 histograms have median width 0.0153 and 428 are narrower than 0.05.
# The C windows have median width 0.0070 and 445 are narrower than 0.05.
# Those windows can pin a fit. --use_spline_init is not used.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 2: manual limits left these histograms off the cosine the points support,
# or the manual baseline raised chi-squared. Starts are that cosine. Limits are
# wide enough that it is not on the boundary. The second-pass half-width is off
# when it is narrower than that parameter's error.
special_fit_parameters_set[("1", "4")] = {"B_initial": -0.23316577, "B_limits": [-0.43316577, -0.03316577], "C_initial": 0.02489426, "C_limits": [-0.17510574, 0.22489426], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8")] = {"B_initial": -0.12523402, "B_limits": [-0.32523402, 0.07476598], "C_initial": -0.04401149, "C_limits": [-0.24401149, 0.15598851], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9")] = {"B_initial": -0.0292026, "B_limits": [-0.2292026, 0.1707974], "C_initial": -0.01620135, "C_limits": [-0.21620135, 0.18379865], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08472426, "B_limits": [-0.28472426, 0.11527574], "C_initial": -0.02188871, "C_limits": [-0.22188871, 0.17811129], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "19")] = {"B_initial": -0.25016199, "B_limits": [-0.45016199, -0.05016199], "C_initial": 0.04853842, "C_limits": [-0.15146158, 0.24853842], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "22")] = {"B_initial": -0.0227518, "B_limits": [-0.2227518, 0.1772482], "C_initial": 0.03282625, "C_limits": [-0.16717375, 0.23282625], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "7")] = {"B_initial": -0.04820963, "B_limits": [-0.24820963, 0.15179037], "C_initial": 0.01775384, "C_limits": [-0.18224616, 0.21775384], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "14")] = {"B_initial": -0.02785431, "B_limits": [-0.22785431, 0.17214569], "C_initial": 0.03492444, "C_limits": [-0.16507556, 0.23492444], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "29")] = {"B_initial": -0.24265178, "B_limits": [-0.44265178, -0.04265178], "C_initial": 0.07472306, "C_limits": [-0.12527694, 0.27472306], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "15")] = {"B_initial": -0.1122343, "B_limits": [-0.3122343, 0.0877657], "C_initial": -0.00122765, "C_limits": [-0.20122765, 0.19877235], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18366098, "B_limits": [-0.38366098, 0.01633902], "C_initial": -0.00797197, "C_limits": [-0.20797197, 0.19202803], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24")] = {"B_initial": -0.23827692, "B_limits": [-0.43827692, -0.03827692], "C_initial": 0.05027265, "C_limits": [-0.14972735, 0.25027265], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "29")] = {"B_initial": -0.28140895, "B_limits": [-0.48140895, -0.08140895], "C_initial": 0.0906512, "C_limits": [-0.1093488, 0.2906512], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "29")] = {"B_initial": -0.23723756, "B_limits": [-0.43723756, -0.03723756], "C_initial": 0.02412515, "C_limits": [-0.17587485, 0.22412515], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "33")] = {"B_initial": -0.11031998, "B_limits": [-0.31031998, 0.08968002], "C_initial": -0.09059237, "C_limits": [-0.29059237, 0.10940763], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "3")] = {"B_initial": -0.19891579, "B_limits": [-0.39891579, 0.00108421], "C_initial": 0.01950437, "C_limits": [-0.18049563, 0.21950437], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "7")] = {"B_initial": -0.03791028, "B_limits": [-0.23791028, 0.16208972], "C_initial": 0.01980844, "C_limits": [-0.18019156, 0.21980844], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31")] = {"B_initial": 0.0054587, "B_limits": [-0.1945413, 0.2054587], "C_initial": 0.04124149, "C_limits": [-0.15875851, 0.24124149], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "2")] = {"B_initial": -0.13248171, "B_limits": [-0.33248171, 0.06751829], "C_initial": 0.03059607, "C_limits": [-0.16940393, 0.23059607], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "3")] = {"B_initial": -0.1637771, "B_limits": [-0.3637771, 0.0362229], "C_initial": 0.02297498, "C_limits": [-0.17702502, 0.22297498], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "10")] = {"B_initial": -0.1677513, "B_limits": [-0.3677513, 0.0322487], "C_initial": 0.01650752, "C_limits": [-0.18349248, 0.21650752], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "11")] = {"B_initial": -0.2587701, "B_limits": [-0.4587701, -0.0587701], "C_initial": 0.02536411, "C_limits": [-0.17463589, 0.22536411], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "16")] = {"B_initial": -0.19140922, "B_limits": [-0.39140922, 0.00859078], "C_initial": -0.01668702, "C_limits": [-0.21668702, 0.18331298], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09731891, "B_limits": [-0.29731891, 0.10268109], "C_initial": -0.01264292, "C_limits": [-0.21264292, 0.18735708], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35")] = {"B_initial": -0.26422692, "B_limits": [-0.46422692, -0.06422692], "C_initial": 0.08247201, "C_limits": [-0.11752799, 0.28247201], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("8", "30")] = {"B_initial": -0.1882301, "B_limits": [-0.3882301, 0.0117699], "C_initial": 0.01779943, "C_limits": [-0.18220057, 0.21779943], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "4")] = {"B_initial": -0.21802786, "B_limits": [-0.41802786, -0.01802786], "C_initial": -0.0042115, "C_limits": [-0.2042115, 0.1957885], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42824513, "B_limits": [-0.62824513, -0.22824513], "C_initial": 0.1083875, "C_limits": [-0.0916125, 0.3083875], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("9", "10")] = {"B_initial": -0.08336845, "B_limits": [-0.28336845, 0.11663155], "C_initial": 0.00378062, "C_limits": [-0.19621938, 0.20378062], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "2")] = {"B_initial": -0.11657702, "B_limits": [-0.31657702, 0.08342298], "C_initial": 0.03554489, "C_limits": [-0.16445511, 0.23554489], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26687985, "B_limits": [-0.46687985, -0.06687985], "C_initial": 0.01081844, "C_limits": [-0.18918156, 0.21081844], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12656326, "B_limits": [-0.32656326, 0.07343674], "C_initial": 0.00176623, "C_limits": [-0.19823377, 0.20176623], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "9")] = {"B_initial": -0.18617896, "B_limits": [-0.38617896, 0.01382104], "C_initial": -0.00454668, "C_limits": [-0.20454668, 0.19545332], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20")] = {"B_initial": -0.27201825, "B_limits": [-0.47201825, -0.07201825], "C_initial": 0.08892523, "C_limits": [-0.11107477, 0.28892523], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13321319, "B_limits": [-0.33321319, 0.06678681], "C_initial": 0.00842473, "C_limits": [-0.19157527, 0.20842473], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "4")] = {"B_initial": -0.26543866, "B_limits": [-0.46543866, -0.06543866], "C_initial": -0.02874311, "C_limits": [-0.22874311, 0.17125689], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "9")] = {"B_initial": -0.19991845, "B_limits": [-0.39991845, 8.155e-05], "C_initial": -0.0008543, "C_limits": [-0.2008543, 0.1991457], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30455999, "B_limits": [-0.50455999, -0.10455999], "C_initial": 0.10192976, "C_limits": [-0.09807024, 0.30192976], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5")] = {"B_initial": -0.29993333, "B_limits": [-0.49993333, -0.09993333], "C_initial": -0.02434269, "C_limits": [-0.22434269, 0.17565731], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "16")] = {"B_initial": -0.18749591, "B_limits": [-0.38749591, 0.01250409], "C_initial": -0.00032885, "C_limits": [-0.20032885, 0.19967115], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "9")] = {"B_initial": -0.23606843, "B_limits": [-0.43606843, -0.03606843], "C_initial": -0.03071601, "C_limits": [-0.23071601, 0.16928399], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15")] = {"B_initial": -0.30628528, "B_limits": [-0.50628528, -0.10628528], "C_initial": 0.05928534, "C_limits": [-0.14071466, 0.25928534], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "24")] = {"B_initial": -0.21121295, "B_limits": [-0.41121295, -0.01121295], "C_initial": 0.04994868, "C_limits": [-0.15005132, 0.24994868], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36437632, "B_limits": [-0.56437632, -0.16437632], "C_initial": 0.10570705, "C_limits": [-0.09429295, 0.30570705], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
