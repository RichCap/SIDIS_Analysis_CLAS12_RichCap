# Run-local guide for spline BayesPlus1. The shared Phi_h files are not edited.
# start=auto chose the manual baseline. The 3D spline B windows selected by these
# histograms have median width 0.0153 and 428 of 452 are narrower than 0.05.
# The C windows are narrower (median 0.0070, 445 of 452). --use_spline_init is not used.
# Pass 1 uses that baseline. Later passes edit only the keys this histogram misses.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 2. These starts are this histogram's unconstrained cosine.
# Limits are opened by 0.2 so that cosine is not a boundary.
# The second-pass half-width is off when it is narrower than the error.
special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18409882, "B_limits": [-0.38409882, 0.01590118], "C_initial": -0.00803113, "C_limits": [-0.20803113, 0.19196887], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "4")] = {"B_initial": -0.26627470, "B_limits": [-0.46627470, -0.06627470], "C_initial": -0.02944139, "C_limits": [-0.22944139, 0.17055861], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26605769, "B_limits": [-0.46605769, -0.06605769], "C_initial": 0.01003126, "C_limits": [-0.18996874, 0.21003126], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "19")] = {"B_initial": -0.25182672, "B_limits": [-0.45182672, -0.05182672], "C_initial": 0.04667333, "C_limits": [-0.15332667, 0.24667333], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5")] = {"B_initial": -0.30031242, "B_limits": [-0.50031242, -0.10031242], "C_initial": -0.02468420, "C_limits": [-0.22468420, 0.17531580], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29")] = {"B_initial": -0.28392119, "B_limits": [-0.48392119, -0.08392119], "C_initial": 0.09341639, "C_limits": [-0.10658361, 0.29341639], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34")] = {"B_initial": -0.16000267, "B_limits": [-0.36000267, 0.03999733], "C_initial": 0.00274006, "C_limits": [-0.19725994, 0.20274006], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15")] = {"B_initial": -0.30799717, "B_limits": [-0.50799717, -0.10799717], "C_initial": 0.06079908, "C_limits": [-0.13920092, 0.26079908], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12721087, "B_limits": [-0.32721087, 0.07278913], "C_initial": 0.00123976, "C_limits": [-0.19876024, 0.20123976], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24")] = {"B_initial": -0.26228217, "B_limits": [-0.46228217, -0.06228217], "C_initial": 0.06268175, "C_limits": [-0.13731825, 0.26268175], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09790239, "B_limits": [-0.29790239, 0.10209761], "C_initial": -0.01198766, "C_limits": [-0.21198766, 0.18801234], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42997257, "B_limits": [-0.62997257, -0.22997257], "C_initial": 0.10730340, "C_limits": [-0.09269660, 0.30730340], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30464872, "B_limits": [-0.50464872, -0.10464872], "C_initial": 0.10221800, "C_limits": [-0.09778200, 0.30221800], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "20")] = {"B_initial": -0.28128688, "B_limits": [-0.48128688, -0.08128688], "C_initial": 0.09495576, "C_limits": [-0.10504424, 0.29495576], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "1")] = {"B_initial": -0.05833214, "B_limits": [-0.25833214, 0.14166786], "C_initial": 0.01090918, "C_limits": [-0.18909082, 0.21090918], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "33")] = {"B_initial": -0.10974279, "B_limits": [-0.30974279, 0.09025721], "C_initial": -0.09155558, "C_limits": [-0.29155558, 0.10844442], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10487939, "B_limits": [-0.30487939, 0.09512061], "C_initial": -0.00850888, "C_limits": [-0.20850888, 0.19149112], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36532362, "B_limits": [-0.56532362, -0.16532362], "C_initial": 0.10513713, "C_limits": [-0.09486287, 0.30513713], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "10")] = {"B_initial": -0.16695273, "B_limits": [-0.36695273, 0.03304727], "C_initial": 0.01671045, "C_limits": [-0.18328955, 0.21671045], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13281231, "B_limits": [-0.33281231, 0.06718769], "C_initial": 0.00784753, "C_limits": [-0.19215247, 0.20784753], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29")] = {"B_initial": -0.24433078, "B_limits": [-0.44433078, -0.04433078], "C_initial": 0.07433784, "C_limits": [-0.12566216, 0.27433784], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08252807, "B_limits": [-0.28252807, 0.11747193], "C_initial": -0.02309502, "C_limits": [-0.22309502, 0.17690498], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "31")] = {"B_initial": 0.00545867, "B_limits": [-0.19454133, 0.20545867], "C_initial": 0.04134015, "C_limits": [-0.15865985, 0.24134015], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "4")] = {"B_initial": -0.23362036, "B_limits": [-0.43362036, -0.03362036], "C_initial": 0.02500651, "C_limits": [-0.17499349, 0.22500651], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "24")] = {"B_initial": -0.21506477, "B_limits": [-0.41506477, -0.01506477], "C_initial": 0.05301243, "C_limits": [-0.14698757, 0.25301243], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "22")] = {"B_initial": -0.02917367, "B_limits": [-0.22917367, 0.17082633], "C_initial": 0.02967157, "C_limits": [-0.17032843, 0.22967157], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "11")] = {"B_initial": -0.25825526, "B_limits": [-0.45825526, -0.05825526], "C_initial": 0.02485917, "C_limits": [-0.17514083, 0.22485917], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "2")] = {"B_initial": -0.13307581, "B_limits": [-0.33307581, 0.06692419], "C_initial": 0.03056741, "C_limits": [-0.16943259, 0.23056741], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "8")] = {"B_initial": -0.12649483, "B_limits": [-0.32649483, 0.07350517], "C_initial": -0.04563688, "C_limits": [-0.24563688, 0.15436312], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "16")] = {"B_initial": -0.17832865, "B_limits": [-0.37832865, 0.02167135], "C_initial": -0.01145922, "C_limits": [-0.21145922, 0.18854078], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "3")] = {"B_initial": -0.17167409, "B_limits": [-0.37167409, 0.02832591], "C_initial": 0.01271385, "C_limits": [-0.18728615, 0.21271385], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35")] = {"B_initial": -0.26594910, "B_limits": [-0.46594910, -0.06594910], "C_initial": 0.08308570, "C_limits": [-0.11691430, 0.28308570], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "3")] = {"B_initial": -0.19911028, "B_limits": [-0.39911028, 0.00088972], "C_initial": 0.01948148, "C_limits": [-0.18051852, 0.21948148], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "9")] = {"B_initial": -0.19946042, "B_limits": [-0.39946042, 0.00053958], "C_initial": -0.00136643, "C_limits": [-0.20136643, 0.19863357], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "16")] = {"B_initial": -0.19205451, "B_limits": [-0.39205451, 0.00794549], "C_initial": -0.01670609, "C_limits": [-0.21670609, 0.18329391], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "14")] = {"B_initial": -0.02646377, "B_limits": [-0.22646377, 0.17353623], "C_initial": 0.03548296, "C_limits": [-0.16451704, 0.23548296], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "7")] = {"B_initial": -0.04802422, "B_limits": [-0.24802422, 0.15197578], "C_initial": 0.01766254, "C_limits": [-0.18233746, 0.21766254], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "29")] = {"B_initial": -0.23988905, "B_limits": [-0.43988905, -0.03988905], "C_initial": 0.02493430, "C_limits": [-0.17506570, 0.22493430], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "19")] = {"B_initial": -0.03493825, "B_limits": [-0.23493825, 0.16506175], "C_initial": -0.00744960, "C_limits": [-0.20744960, 0.19255040], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "16")] = {"B_initial": -0.18263254, "B_limits": [-0.38263254, 0.01736746], "C_initial": 0.01091117, "C_limits": [-0.18908883, 0.21091117], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("17", "2")] = {"B_initial": -0.06778619, "B_limits": [-0.26778619, 0.13221381], "C_initial": -0.00602918, "C_limits": [-0.20602918, 0.19397082], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "9")] = {"B_initial": -0.02351186, "B_limits": [-0.22351186, 0.17648814], "C_initial": -0.01642591, "C_limits": [-0.21642591, 0.18357409], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "7")] = {"B_initial": -0.04006808, "B_limits": [-0.24006808, 0.15993192], "C_initial": 0.01789945, "C_limits": [-0.18210055, 0.21789945], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "9")] = {"B_initial": -0.23237958, "B_limits": [-0.43237958, -0.03237958], "C_initial": -0.02770569, "C_limits": [-0.22770569, 0.17229431], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "15")] = {"B_initial": -0.11258153, "B_limits": [-0.31258153, 0.08741847], "C_initial": -0.00156244, "C_limits": [-0.20156244, 0.19843756], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "21")] = {"B_initial": -0.13935597, "B_limits": [-0.33935597, 0.06064403], "C_initial": 0.00662834, "C_limits": [-0.19337166, 0.20662834], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "2")] = {"B_initial": -0.11294915, "B_limits": [-0.31294915, 0.08705085], "C_initial": 0.03882340, "C_limits": [-0.16117660, 0.23882340], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("8", "30")] = {"B_initial": -0.19083991, "B_limits": [-0.39083991, 0.00916009], "C_initial": 0.01943663, "C_limits": [-0.18056337, 0.21943663], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "10")] = {"B_initial": -0.09509719, "B_limits": [-0.29509719, 0.10490281], "C_initial": -0.00705449, "C_limits": [-0.20705449, 0.19294551], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "15")] = {"B_initial": -0.10568528, "B_limits": [-0.30568528, 0.09431472], "C_initial": 0.00200749, "C_limits": [-0.19799251, 0.20200749], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16")] = {"B_initial": -0.01868180, "B_limits": [-0.21868180, 0.18131820], "C_initial": -0.00015607, "C_limits": [-0.20015607, 0.19984393], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "4")] = {"B_initial": -0.21826766, "B_limits": [-0.41826766, -0.01826766], "C_initial": -0.00358830, "C_limits": [-0.20358830, 0.19641170], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
