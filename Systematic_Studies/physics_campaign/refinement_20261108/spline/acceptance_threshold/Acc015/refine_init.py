# Run-local Acc015 guide. The shared Phi_h files are not edited.
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
special_fit_parameters_set[("1", "4")] = {"B_initial": -0.23321931, "B_limits": [-0.43321931, -0.03321931], "C_initial": 0.02482559, "C_limits": [-0.17517441, 0.22482559], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8")] = {"B_initial": -0.12470639, "B_limits": [-0.32470639, 0.07529361], "C_initial": -0.04435558, "C_limits": [-0.24435558, 0.15564442], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9")] = {"B_initial": -0.02913523, "B_limits": [-0.22913523, 0.17086477], "C_initial": -0.01614174, "C_limits": [-0.21614174, 0.18385826], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08461767, "B_limits": [-0.28461767, 0.11538233], "C_initial": -0.02176119, "C_limits": [-0.22176119, 0.17823881], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "19")] = {"B_initial": -0.25011757, "B_limits": [-0.45011757, -0.05011757], "C_initial": 0.04857059, "C_limits": [-0.15142941, 0.24857059], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "22")] = {"B_initial": -0.02287591, "B_limits": [-0.22287591, 0.17712409], "C_initial": 0.03267255, "C_limits": [-0.16732745, 0.23267255], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "3")] = {"B_initial": -0.16874847, "B_limits": [-0.36874847, 0.03125153], "C_initial": 0.01750517, "C_limits": [-0.18249483, 0.21750517], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "7")] = {"B_initial": -0.04776858, "B_limits": [-0.24776858, 0.15223142], "C_initial": 0.01792993, "C_limits": [-0.18207007, 0.21792993], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "14")] = {"B_initial": -0.02735, "B_limits": [-0.22735, 0.17265], "C_initial": 0.03509639, "C_limits": [-0.16490361, 0.23509639], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "16")] = {"B_initial": -0.18338588, "B_limits": [-0.38338588, 0.01661412], "C_initial": 0.01074236, "C_limits": [-0.18925764, 0.21074236], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "21")] = {"B_initial": -0.13957119, "B_limits": [-0.33957119, 0.06042881], "C_initial": 0.00648769, "C_limits": [-0.19351231, 0.20648769], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29")] = {"B_initial": -0.24265066, "B_limits": [-0.44265066, -0.04265066], "C_initial": 0.07471007, "C_limits": [-0.12528993, 0.27471007], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "15")] = {"B_initial": -0.11209768, "B_limits": [-0.31209768, 0.08790232], "C_initial": -0.00116962, "C_limits": [-0.20116962, 0.19883038], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29")] = {"B_initial": -0.27988036, "B_limits": [-0.47988036, -0.07988036], "C_initial": 0.09167454, "C_limits": [-0.10832546, 0.29167454], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "19")] = {"B_initial": -0.03536342, "B_limits": [-0.23536342, 0.16463658], "C_initial": -0.00749717, "C_limits": [-0.20749717, 0.19250283], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "29")] = {"B_initial": -0.27611928, "B_limits": [-0.47611928, -0.07611928], "C_initial": 0.05254278, "C_limits": [-0.14745722, 0.25254278], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34")] = {"B_initial": -0.15065946, "B_limits": [-0.35065946, 0.04934054], "C_initial": -0.00119441, "C_limits": [-0.20119441, 0.19880559], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "3")] = {"B_initial": -0.19882609, "B_limits": [-0.39882609, 0.00117391], "C_initial": 0.01945544, "C_limits": [-0.18054456, 0.21945544], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "7")] = {"B_initial": -0.04270234, "B_limits": [-0.24270234, 0.15729766], "C_initial": 0.01659693, "C_limits": [-0.18340307, 0.21659693], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31")] = {"B_initial": 0.00546483, "B_limits": [-0.19453517, 0.20546483], "C_initial": 0.0412536, "C_limits": [-0.1587464, 0.2412536], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "2")] = {"B_initial": -0.1332223, "B_limits": [-0.3332223, 0.0667777], "C_initial": 0.03043389, "C_limits": [-0.16956611, 0.23043389], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "6")] = {"B_initial": -0.36637008, "B_limits": [-0.56637008, -0.16637008], "C_initial": 0.06970497, "C_limits": [-0.13029503, 0.26970497], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "10")] = {"B_initial": -0.16761873, "B_limits": [-0.36761873, 0.03238127], "C_initial": 0.01657708, "C_limits": [-0.18342292, 0.21657708], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "11")] = {"B_initial": -0.26788648, "B_limits": [-0.46788648, -0.06788648], "C_initial": 0.01814383, "C_limits": [-0.18185617, 0.21814383], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09725953, "B_limits": [-0.29725953, 0.10274047], "C_initial": -0.01257044, "C_limits": [-0.21257044, 0.18742956], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35")] = {"B_initial": -0.27856893, "B_limits": [-0.47856893, -0.07856893], "C_initial": 0.09258563, "C_limits": [-0.10741437, 0.29258563], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("8", "30")] = {"B_initial": -0.18825663, "B_limits": [-0.38825663, 0.01174337], "C_initial": 0.01791568, "C_limits": [-0.18208432, 0.21791568], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "3")] = {"B_initial": -0.15532525, "B_limits": [-0.35532525, 0.04467475], "C_initial": -0.00501834, "C_limits": [-0.20501834, 0.19498166], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "4")] = {"B_initial": -0.21788412, "B_limits": [-0.41788412, -0.01788412], "C_initial": -0.00413838, "C_limits": [-0.20413838, 0.19586162], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42561572, "B_limits": [-0.62561572, -0.22561572], "C_initial": 0.1107981, "C_limits": [-0.0892019, 0.3107981], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("9", "8")] = {"B_initial": -0.07194708, "B_limits": [-0.27194708, 0.12805292], "C_initial": -0.04364379, "C_limits": [-0.24364379, 0.15635621], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "2")] = {"B_initial": -0.11287567, "B_limits": [-0.31287567, 0.08712433], "C_initial": 0.03863917, "C_limits": [-0.16136083, 0.23863917], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10457837, "B_limits": [-0.30457837, 0.09542163], "C_initial": -0.00819101, "C_limits": [-0.20819101, 0.19180899], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "9")] = {"B_initial": -0.15085019, "B_limits": [-0.35085019, 0.04914981], "C_initial": -0.01500695, "C_limits": [-0.21500695, 0.18499305], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11")] = {"B_initial": -0.2679941, "B_limits": [-0.4679941, -0.0679941], "C_initial": 0.00957715, "C_limits": [-0.19042285, 0.20957715], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "16")] = {"B_initial": -0.16605649, "B_limits": [-0.36605649, 0.03394351], "C_initial": 0.01001557, "C_limits": [-0.18998443, 0.21001557], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12736819, "B_limits": [-0.32736819, 0.07263181], "C_initial": 0.00112723, "C_limits": [-0.19887277, 0.20112723], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20")] = {"B_initial": -0.27326993, "B_limits": [-0.47326993, -0.07326993], "C_initial": 0.08972657, "C_limits": [-0.11027343, 0.28972657], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13180495, "B_limits": [-0.33180495, 0.06819505], "C_initial": 0.00702851, "C_limits": [-0.19297149, 0.20702851], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "4")] = {"B_initial": -0.26946017, "B_limits": [-0.46946017, -0.06946017], "C_initial": -0.03135797, "C_limits": [-0.23135797, 0.16864203], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "9")] = {"B_initial": -0.19985281, "B_limits": [-0.39985281, 0.00014719], "C_initial": -0.00082084, "C_limits": [-0.20082084, 0.19917916], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30448265, "B_limits": [-0.50448265, -0.10448265], "C_initial": 0.10200714, "C_limits": [-0.09799286, 0.30200714], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5")] = {"B_initial": -0.29996334, "B_limits": [-0.49996334, -0.09996334], "C_initial": -0.02435871, "C_limits": [-0.22435871, 0.17564129], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "15")] = {"B_initial": -0.10574476, "B_limits": [-0.30574476, 0.09425524], "C_initial": -0.00011432, "C_limits": [-0.20011432, 0.19988568], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "9")] = {"B_initial": -0.23214611, "B_limits": [-0.43214611, -0.03214611], "C_initial": -0.02758933, "C_limits": [-0.22758933, 0.17241067], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15")] = {"B_initial": -0.30628102, "B_limits": [-0.50628102, -0.10628102], "C_initial": 0.05926742, "C_limits": [-0.14073258, 0.25926742], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "24")] = {"B_initial": -0.21409346, "B_limits": [-0.41409346, -0.01409346], "C_initial": 0.05246264, "C_limits": [-0.14753736, 0.25246264], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36437642, "B_limits": [-0.56437642, -0.16437642], "C_initial": 0.10572935, "C_limits": [-0.09427065, 0.30572935], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("16", "16")] = {"B_initial": -0.17812134, "B_limits": [-0.37812134, 0.02187866], "C_initial": -0.01106397, "C_limits": [-0.21106397, 0.18893603], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
