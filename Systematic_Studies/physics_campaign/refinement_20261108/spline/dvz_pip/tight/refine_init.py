# Run-local pion |dvz| tight guide. The shared Phi_h files are not edited.
# start=auto chose the manual baseline. The 3D spline B windows for these 452 histograms have median width 0.0153 and 428 are narrower than 0.05. The C median width is 0.0070 and 445 are narrower than 0.05.
# Pass 1 used that baseline and pinned bins whose cosine sits outside it. Pass 2 puts those starts on each histogram's own cosine and turns off the half-width second pass when the amplitude is below 0.05.
# --use_spline_init is not used.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 2. Starts are this variation's unconstrained cosine. Limits keep that cosine off the first-pass boundary.

special_fit_parameters_set[("1", "4")] = {"B_initial": -0.23614301, "B_limits": [-0.43614301, -0.03614301], "C_initial": 0.02346132, "C_limits": [-0.17653868, 0.22346132], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "8")] = {"B_initial": -0.12884886, "B_limits": [-0.32884886, 0.07115114], "C_initial": -0.04612308, "C_limits": [-0.24612308, 0.15387692], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "9")] = {"B_initial": -0.02854722, "B_limits": [-0.22854722, 0.17145278], "C_initial": -0.01616392, "C_limits": [-0.21616392, 0.18383608], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "12")] = {"B_initial": -0.25072788, "B_limits": [-0.45072788, -0.05072788], "C_initial": 0.04667301, "C_limits": [-0.15332699, 0.24667301], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08516506, "B_limits": [-0.28516506, 0.11483494], "C_initial": -0.02173329, "C_limits": [-0.22173329, 0.17826671], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "19")] = {"B_initial": -0.25074804, "B_limits": [-0.45074804, -0.05074804], "C_initial": 0.04859682, "C_limits": [-0.15140318, 0.24859682], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "22")] = {"B_initial": -0.03290132, "B_limits": [-0.23290132, 0.16709868], "C_initial": 0.02762363, "C_limits": [-0.17237637, 0.22762363], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "7")] = {"B_initial": -0.04838022, "B_limits": [-0.24838022, 0.15161978], "C_initial": 0.01749316, "C_limits": [-0.18250684, 0.21749316], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "14")] = {"B_initial": -0.02932088, "B_limits": [-0.22932088, 0.17067912], "C_initial": 0.03388129, "C_limits": [-0.16611871, 0.23388129], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "16")] = {"B_initial": -0.18422547, "B_limits": [-0.38422547, 0.01577453], "C_initial": 0.01097804, "C_limits": [-0.18902196, 0.21097804], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "29")] = {"B_initial": -0.24319851, "B_limits": [-0.44319851, -0.04319851], "C_initial": 0.07488905, "C_limits": [-0.12511095, 0.27488905], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("3", "3")] = {"B_initial": -0.17443179, "B_limits": [-0.37443179, 0.02556821], "C_initial": 0.01031793, "C_limits": [-0.18968207, 0.21031793], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("3", "15")] = {"B_initial": -0.11351395, "B_limits": [-0.31351395, 0.08648605], "C_initial": -0.00235569, "C_limits": [-0.20235569, 0.19764431], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18462555, "B_limits": [-0.38462555, 0.01537445], "C_initial": -0.00812055, "C_limits": [-0.20812055, 0.19187945], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("3", "24")] = {"B_initial": -0.24802677, "B_limits": [-0.44802677, -0.04802677], "C_initial": 0.05700695, "C_limits": [-0.14299305, 0.25700695], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("3", "29")] = {"B_initial": -0.28065451, "B_limits": [-0.48065451, -0.08065451], "C_initial": 0.09200980, "C_limits": [-0.10799020, 0.29200980], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("4", "29")] = {"B_initial": -0.23769245, "B_limits": [-0.43769245, -0.03769245], "C_initial": 0.02307743, "C_limits": [-0.17692257, 0.22307743], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("4", "33")] = {"B_initial": -0.11146689, "B_limits": [-0.31146689, 0.08853311], "C_initial": -0.09241799, "C_limits": [-0.29241799, 0.10758201], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("4", "34")] = {"B_initial": -0.15969554, "B_limits": [-0.35969554, 0.04030446], "C_initial": 0.00036403, "C_limits": [-0.19963597, 0.20036403], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("5", "3")] = {"B_initial": -0.20004290, "B_limits": [-0.40004290, -0.00004290], "C_initial": 0.01893731, "C_limits": [-0.18106269, 0.21893731], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("5", "7")] = {"B_initial": -0.04072609, "B_limits": [-0.24072609, 0.15927391], "C_initial": 0.01731998, "C_limits": [-0.18268002, 0.21731998], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("5", "31")] = {"B_initial": -0.00326864, "B_limits": [-0.20326864, 0.19673136], "C_initial": 0.03804531, "C_limits": [-0.16195469, 0.23804531], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("6", "1")] = {"B_initial": -0.05897412, "B_limits": [-0.25897412, 0.14102588], "C_initial": 0.01109631, "C_limits": [-0.18890369, 0.21109631], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("6", "2")] = {"B_initial": -0.13262044, "B_limits": [-0.33262044, 0.06737956], "C_initial": 0.03036493, "C_limits": [-0.16963507, 0.23036493], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "10")] = {"B_initial": -0.16861403, "B_limits": [-0.36861403, 0.03138597], "C_initial": 0.01632960, "C_limits": [-0.18367040, 0.21632960], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "11")] = {"B_initial": -0.25919787, "B_limits": [-0.45919787, -0.05919787], "C_initial": 0.02533995, "C_limits": [-0.17466005, 0.22533995], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "16")] = {"B_initial": -0.19370323, "B_limits": [-0.39370323, 0.00629677], "C_initial": -0.01816729, "C_limits": [-0.21816729, 0.18183271], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09681534, "B_limits": [-0.29681534, 0.10318466], "C_initial": -0.01215680, "C_limits": [-0.21215680, 0.18784320], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "35")] = {"B_initial": -0.26468922, "B_limits": [-0.46468922, -0.06468922], "C_initial": 0.08236326, "C_limits": [-0.11763674, 0.28236326], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("8", "19")] = {"B_initial": -0.15187339, "B_limits": [-0.35187339, 0.04812661], "C_initial": -0.02236944, "C_limits": [-0.22236944, 0.17763056], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("9", "4")] = {"B_initial": -0.21879157, "B_limits": [-0.41879157, -0.01879157], "C_initial": -0.00475470, "C_limits": [-0.20475470, 0.19524530], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42878225, "B_limits": [-0.62878225, -0.22878225], "C_initial": 0.10815471, "C_limits": [-0.09184529, 0.30815471], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("9", "8")] = {"B_initial": -0.06872648, "B_limits": [-0.26872648, 0.13127352], "C_initial": -0.04110726, "C_limits": [-0.24110726, 0.15889274], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("10", "2")] = {"B_initial": -0.11318252, "B_limits": [-0.31318252, 0.08681748], "C_initial": 0.03857691, "C_limits": [-0.16142309, 0.23857691], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10512606, "B_limits": [-0.30512606, 0.09487394], "C_initial": -0.00890227, "C_limits": [-0.20890227, 0.19109773], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26662134, "B_limits": [-0.46662134, -0.06662134], "C_initial": 0.01106577, "C_limits": [-0.18893423, 0.21106577], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("10", "15")] = {"B_initial": -0.10768352, "B_limits": [-0.30768352, 0.09231648], "C_initial": 0.00085008, "C_limits": [-0.19914992, 0.20085008], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12831907, "B_limits": [-0.32831907, 0.07168093], "C_initial": 0.00073274, "C_limits": [-0.19926726, 0.20073274], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("11", "20")] = {"B_initial": -0.27679803, "B_limits": [-0.47679803, -0.07679803], "C_initial": 0.09191767, "C_limits": [-0.10808233, 0.29191767], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13367140, "B_limits": [-0.33367140, 0.06632860], "C_initial": 0.00687055, "C_limits": [-0.19312945, 0.20687055], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("13", "4")] = {"B_initial": -0.26488932, "B_limits": [-0.46488932, -0.06488932], "C_initial": -0.02870405, "C_limits": [-0.22870405, 0.17129595], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("13", "9")] = {"B_initial": -0.20044826, "B_limits": [-0.40044826, -0.00044826], "C_initial": -0.00143357, "C_limits": [-0.20143357, 0.19856643], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30548160, "B_limits": [-0.50548160, -0.10548160], "C_initial": 0.10172440, "C_limits": [-0.09827560, 0.30172440], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("14", "5")] = {"B_initial": -0.30208462, "B_limits": [-0.50208462, -0.10208462], "C_initial": -0.02455578, "C_limits": [-0.22455578, 0.17544422], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("15", "9")] = {"B_initial": -0.23232439, "B_limits": [-0.43232439, -0.03232439], "C_initial": -0.02743843, "C_limits": [-0.22743843, 0.17256157], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("15", "15")] = {"B_initial": -0.30735140, "B_limits": [-0.50735140, -0.10735140], "C_initial": 0.05879900, "C_limits": [-0.14120100, 0.25879900], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("15", "24")] = {"B_initial": -0.21444117, "B_limits": [-0.41444117, -0.01444117], "C_initial": 0.05181969, "C_limits": [-0.14818031, 0.25181969], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36519820, "B_limits": [-0.56519820, -0.16519820], "C_initial": 0.10540332, "C_limits": [-0.09459668, 0.30540332], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("16", "16")] = {"B_initial": -0.17818671, "B_limits": [-0.37818671, 0.02181329], "C_initial": -0.01064439, "C_limits": [-0.21064439, 0.18935561], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
