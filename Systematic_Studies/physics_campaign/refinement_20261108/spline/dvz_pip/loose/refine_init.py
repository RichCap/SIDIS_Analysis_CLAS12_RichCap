# Run-local pion |dvz| loose guide. The shared Phi_h files are not edited.
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

special_fit_parameters_set[("1", "3")] = {"B_initial": -0.16958092, "B_limits": [-0.36958092, 0.03041908], "C_initial": 0.01778044, "C_limits": [-0.18221956, 0.21778044], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "4")] = {"B_initial": -0.23135249, "B_limits": [-0.43135249, -0.03135249], "C_initial": 0.02548187, "C_limits": [-0.17451813, 0.22548187], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "8")] = {"B_initial": -0.12278043, "B_limits": [-0.32278043, 0.07721957], "C_initial": -0.04339750, "C_limits": [-0.24339750, 0.15660250], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "9")] = {"B_initial": -0.02681831, "B_limits": [-0.22681831, 0.17318169], "C_initial": -0.01453818, "C_limits": [-0.21453818, 0.18546182], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08499270, "B_limits": [-0.28499270, 0.11500730], "C_initial": -0.02244902, "C_limits": [-0.22244902, 0.17755098], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "19")] = {"B_initial": -0.25022873, "B_limits": [-0.45022873, -0.05022873], "C_initial": 0.04912355, "C_limits": [-0.15087645, 0.24912355], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("1", "22")] = {"B_initial": -0.01453303, "B_limits": [-0.21453303, 0.18546697], "C_initial": 0.03670673, "C_limits": [-0.16329327, 0.23670673], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "7")] = {"B_initial": -0.04805677, "B_limits": [-0.24805677, 0.15194323], "C_initial": 0.01706869, "C_limits": [-0.18293131, 0.21706869], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "14")] = {"B_initial": -0.02593725, "B_limits": [-0.22593725, 0.17406275], "C_initial": 0.03586679, "C_limits": [-0.16413321, 0.23586679], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "16")] = {"B_initial": -0.18333462, "B_limits": [-0.38333462, 0.01666538], "C_initial": 0.01027289, "C_limits": [-0.18972711, 0.21027289], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "21")] = {"B_initial": -0.13823457, "B_limits": [-0.33823457, 0.06176543], "C_initial": 0.00668936, "C_limits": [-0.19331064, 0.20668936], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("2", "29")] = {"B_initial": -0.24238297, "B_limits": [-0.44238297, -0.04238297], "C_initial": 0.07520721, "C_limits": [-0.12479279, 0.27520721], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("3", "3")] = {"B_initial": -0.17157308, "B_limits": [-0.37157308, 0.02842692], "C_initial": 0.01281049, "C_limits": [-0.18718951, 0.21281049], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18261052, "B_limits": [-0.38261052, 0.01738948], "C_initial": -0.00757697, "C_limits": [-0.20757697, 0.19242303], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("3", "24")] = {"B_initial": -0.24768308, "B_limits": [-0.44768308, -0.04768308], "C_initial": 0.05719274, "C_limits": [-0.14280726, 0.25719274], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("3", "29")] = {"B_initial": -0.27983557, "B_limits": [-0.47983557, -0.07983557], "C_initial": 0.09165361, "C_limits": [-0.10834639, 0.29165361], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("4", "19")] = {"B_initial": -0.03565823, "B_limits": [-0.23565823, 0.16434177], "C_initial": -0.00797272, "C_limits": [-0.20797272, 0.19202728], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("4", "29")] = {"B_initial": -0.23738143, "B_limits": [-0.43738143, -0.03738143], "C_initial": 0.02539570, "C_limits": [-0.17460430, 0.22539570], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("4", "33")] = {"B_initial": -0.10909669, "B_limits": [-0.30909669, 0.09090331], "C_initial": -0.09083250, "C_limits": [-0.29083250, 0.10916750], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("4", "34")] = {"B_initial": -0.15898130, "B_limits": [-0.35898130, 0.04101870], "C_initial": 0.00219084, "C_limits": [-0.19780916, 0.20219084], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("5", "3")] = {"B_initial": -0.19838293, "B_limits": [-0.39838293, 0.00161707], "C_initial": 0.01893908, "C_limits": [-0.18106092, 0.21893908], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("5", "7")] = {"B_initial": -0.04043392, "B_limits": [-0.24043392, 0.15956608], "C_initial": 0.01838725, "C_limits": [-0.18161275, 0.21838725], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("5", "31")] = {"B_initial": 0.01049497, "B_limits": [-0.18950503, 0.21049497], "C_initial": 0.04216051, "C_limits": [-0.15783949, 0.24216051], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("6", "1")] = {"B_initial": -0.05813621, "B_limits": [-0.25813621, 0.14186379], "C_initial": 0.01046606, "C_limits": [-0.18953394, 0.21046606], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("6", "2")] = {"B_initial": -0.13145262, "B_limits": [-0.33145262, 0.06854738], "C_initial": 0.03136313, "C_limits": [-0.16863687, 0.23136313], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "10")] = {"B_initial": -0.16741328, "B_limits": [-0.36741328, 0.03258672], "C_initial": 0.01665630, "C_limits": [-0.18334370, 0.21665630], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "11")] = {"B_initial": -0.25801201, "B_limits": [-0.45801201, -0.05801201], "C_initial": 0.02505735, "C_limits": [-0.17494265, 0.22505735], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "16")] = {"B_initial": -0.19047132, "B_limits": [-0.39047132, 0.00952868], "C_initial": -0.01622809, "C_limits": [-0.21622809, 0.18377191], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09606701, "B_limits": [-0.29606701, 0.10393299], "C_initial": -0.01120273, "C_limits": [-0.21120273, 0.18879727], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("7", "35")] = {"B_initial": -0.26372470, "B_limits": [-0.46372470, -0.06372470], "C_initial": 0.08270508, "C_limits": [-0.11729492, 0.28270508], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("8", "19")] = {"B_initial": -0.15119773, "B_limits": [-0.35119773, 0.04880227], "C_initial": -0.02178051, "C_limits": [-0.22178051, 0.17821949], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("9", "4")] = {"B_initial": -0.21873385, "B_limits": [-0.41873385, -0.01873385], "C_initial": -0.00444543, "C_limits": [-0.20444543, 0.19555457], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42773078, "B_limits": [-0.62773078, -0.22773078], "C_initial": 0.10832614, "C_limits": [-0.09167386, 0.30832614], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10415054, "B_limits": [-0.30415054, 0.09584946], "C_initial": -0.00699975, "C_limits": [-0.20699975, 0.19300025], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26670046, "B_limits": [-0.46670046, -0.06670046], "C_initial": 0.01059791, "C_limits": [-0.18940209, 0.21059791], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12739399, "B_limits": [-0.32739399, 0.07260601], "C_initial": 0.00064073, "C_limits": [-0.19935927, 0.20064073], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("11", "20")] = {"B_initial": -0.27651187, "B_limits": [-0.47651187, -0.07651187], "C_initial": 0.09273590, "C_limits": [-0.10726410, 0.29273590], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13340218, "B_limits": [-0.33340218, 0.06659782], "C_initial": 0.01022870, "C_limits": [-0.18977130, 0.21022870], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("13", "4")] = {"B_initial": -0.26431444, "B_limits": [-0.46431444, -0.06431444], "C_initial": -0.02867673, "C_limits": [-0.22867673, 0.17132327], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("13", "9")] = {"B_initial": -0.19971945, "B_limits": [-0.39971945, 0.00028055], "C_initial": -0.00112333, "C_limits": [-0.20112333, 0.19887667], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30418795, "B_limits": [-0.50418795, -0.10418795], "C_initial": 0.10192479, "C_limits": [-0.09807521, 0.30192479], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("14", "5")] = {"B_initial": -0.29747122, "B_limits": [-0.49747122, -0.09747122], "C_initial": -0.02322359, "C_limits": [-0.22322359, 0.17677641], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("15", "9")] = {"B_initial": -0.23151898, "B_limits": [-0.43151898, -0.03151898], "C_initial": -0.02703157, "C_limits": [-0.22703157, 0.17296843], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}

special_fit_parameters_set[("15", "15")] = {"B_initial": -0.30570194, "B_limits": [-0.50570194, -0.10570194], "C_initial": 0.06018247, "C_limits": [-0.13981753, 0.26018247], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("15", "24")] = {"B_initial": -0.21387746, "B_limits": [-0.41387746, -0.01387746], "C_initial": 0.05320873, "C_limits": [-0.14679127, 0.25320873], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36299248, "B_limits": [-0.56299248, -0.16299248], "C_initial": 0.10624023, "C_limits": [-0.09375977, 0.30624023], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("16", "16")] = {"B_initial": -0.17754859, "B_limits": [-0.37754859, 0.02245141], "C_initial": -0.01080064, "C_limits": [-0.21080064, 0.18919936], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
