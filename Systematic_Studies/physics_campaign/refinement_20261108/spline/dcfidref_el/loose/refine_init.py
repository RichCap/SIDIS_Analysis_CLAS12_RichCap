# Run-local electron DC refinement loose guide. The shared Phi_h files are not edited.
# start=auto chose the manual baseline. The 3D spline windows for these histograms are tight enough to pin B and C, so --use_spline_init is not used.
# Pass 1 is this baseline. Later overrides are added only for histograms whose own cosine is outside it.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 2. Starts are this histogram's unconstrained cosine. Limits keep that cosine off the manual boundary.
# The half-width second pass is off when the amplitude is below 0.05.
special_fit_parameters_set[("1", "10")] = {"B_initial": -0.09490073, "B_limits": [-0.18980145, 0.00000000], "C_initial": -0.00660759, "C_limits": [-0.20660759, 0.19339241], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08692273, "B_limits": [-0.17384546, 0.00000000], "C_initial": -0.02041267, "C_limits": [-0.22041267, 0.17958733], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "19")] = {"B_initial": -0.24986024, "B_limits": [-0.49972047, 0.00000000], "C_initial": 0.04862729, "C_limits": [-0.15137271, 0.24862729], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22")] = {"B_initial": -0.02585380, "B_limits": [-0.22585380, 0.17414620], "C_initial": 0.02869908, "C_limits": [-0.17130092, 0.22869908], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "3")] = {"B_initial": -0.16016023, "B_limits": [-0.32032045, 0.00000000], "C_initial": 0.02665919, "C_limits": [-0.17334081, 0.22665919], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "4")] = {"B_initial": -0.22877629, "B_limits": [-0.45755259, 0.00000000], "C_initial": 0.02744970, "C_limits": [-0.17255030, 0.22744970], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8")] = {"B_initial": -0.13354445, "B_limits": [-0.26708889, 0.00000000], "C_initial": -0.04818798, "C_limits": [-0.24818798, 0.15181202], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "9")] = {"B_initial": -0.01760564, "B_limits": [-0.21760564, 0.18239436], "C_initial": -0.00858339, "C_limits": [-0.20858339, 0.19141661], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26534426, "B_limits": [-0.53068851, 0.00000000], "C_initial": 0.01283796, "C_limits": [-0.18716204, 0.21283796], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "15")] = {"B_initial": -0.10462299, "B_limits": [-0.20924599, 0.00000000], "C_initial": 0.00248718, "C_limits": [-0.19751282, 0.20248718], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10455327, "B_limits": [-0.20910655, 0.00000000], "C_initial": -0.00884682, "C_limits": [-0.20884682, 0.19115318], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "9")] = {"B_initial": -0.15044703, "B_limits": [-0.30089406, 0.00000000], "C_initial": -0.01521913, "C_limits": [-0.21521913, 0.18478087], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20")] = {"B_initial": -0.27524331, "B_limits": [-0.55048663, 0.00000000], "C_initial": 0.09282604, "C_limits": [0.00000000, 0.18565208], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12661999, "B_limits": [-0.25323998, 0.00000000], "C_initial": 0.00139981, "C_limits": [-0.19860019, 0.20139981], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13105389, "B_limits": [-0.26210779, 0.00000000], "C_initial": 0.00506477, "C_limits": [-0.19493523, 0.20506477], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30402229, "B_limits": [-0.60804458, 0.00000000], "C_initial": 0.10224239, "C_limits": [0.00000000, 0.20448478], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4")] = {"B_initial": -0.27074298, "B_limits": [-0.54148596, 0.00000000], "C_initial": -0.03164582, "C_limits": [-0.23164582, 0.16835418], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("13", "9")] = {"B_initial": -0.19944998, "B_limits": [-0.39889996, 0.00000000], "C_initial": 0.00080744, "C_limits": [-0.19919256, 0.20080744], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5")] = {"B_initial": -0.30123019, "B_limits": [-0.60246038, 0.00000000], "C_initial": -0.02562581, "C_limits": [-0.22562581, 0.17437419], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15")] = {"B_initial": -0.30439694, "B_limits": [-0.60879389, 0.00000000], "C_initial": 0.05850933, "C_limits": [0.00000000, 0.11701866], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "24")] = {"B_initial": -0.21484070, "B_limits": [-0.42968140, 0.00000000], "C_initial": 0.05664303, "C_limits": [0.00000000, 0.11328605], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "9")] = {"B_initial": -0.23505913, "B_limits": [-0.47011826, 0.00000000], "C_initial": -0.02721989, "C_limits": [-0.22721989, 0.17278011], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36451893, "B_limits": [-0.72903786, 0.00000000], "C_initial": 0.10600077, "C_limits": [0.00000000, 0.21200155], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("16", "16")] = {"B_initial": -0.17922742, "B_limits": [-0.35845484, 0.00000000], "C_initial": -0.01149788, "C_limits": [-0.21149788, 0.18850212], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "14")] = {"B_initial": -0.02415124, "B_limits": [-0.22415124, 0.17584876], "C_initial": 0.03846155, "C_limits": [-0.16153845, 0.23846155], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "21")] = {"B_initial": -0.14086316, "B_limits": [-0.28172631, 0.00000000], "C_initial": 0.00714052, "C_limits": [-0.19285948, 0.20714052], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29")] = {"B_initial": -0.24194731, "B_limits": [-0.48389461, 0.00000000], "C_initial": 0.07458628, "C_limits": [0.00000000, 0.14917255], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18814144, "B_limits": [-0.37628288, 0.00000000], "C_initial": -0.01064755, "C_limits": [-0.21064755, 0.18935245], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24")] = {"B_initial": -0.25610768, "B_limits": [-0.51221536, 0.00000000], "C_initial": 0.05854063, "C_limits": [0.00000000, 0.11708125], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "29")] = {"B_initial": -0.28085992, "B_limits": [-0.56171984, 0.00000000], "C_initial": 0.08994971, "C_limits": [0.00000000, 0.17989943], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "3")] = {"B_initial": -0.18082876, "B_limits": [-0.36165752, 0.00000000], "C_initial": 0.01415989, "C_limits": [-0.18584011, 0.21415989], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "19")] = {"B_initial": -0.03215811, "B_limits": [-0.23215811, 0.16784189], "C_initial": 0.00315501, "C_limits": [-0.19684499, 0.20315501], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("4", "29")] = {"B_initial": -0.26192601, "B_limits": [-0.52385203, 0.00000000], "C_initial": 0.03996298, "C_limits": [-0.16003702, 0.23996298], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "3")] = {"B_initial": -0.19781897, "B_limits": [-0.39563793, 0.00000000], "C_initial": 0.02463541, "C_limits": [-0.17536459, 0.22463541], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31")] = {"B_initial": 0.00425254, "B_limits": [-0.19574746, 0.20425254], "C_initial": 0.04047686, "C_limits": [-0.15952314, 0.24047686], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "7")] = {"B_initial": -0.03895459, "B_limits": [-0.23895459, 0.16104541], "C_initial": 0.01901774, "C_limits": [-0.18098226, 0.21901774], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2")] = {"B_initial": -0.13027040, "B_limits": [-0.26054080, 0.00000000], "C_initial": 0.03138993, "C_limits": [-0.16861007, 0.23138993], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "10")] = {"B_initial": -0.17044753, "B_limits": [-0.34089507, 0.00000000], "C_initial": 0.01680095, "C_limits": [-0.18319905, 0.21680095], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "11")] = {"B_initial": -0.25911839, "B_limits": [-0.51823678, 0.00000000], "C_initial": 0.02499078, "C_limits": [-0.17500922, 0.22499078], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09851157, "B_limits": [-0.19702315, 0.00000000], "C_initial": -0.01545679, "C_limits": [-0.21545679, 0.18454321], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35")] = {"B_initial": -0.26571772, "B_limits": [-0.53143545, 0.00000000], "C_initial": 0.08205677, "C_limits": [0.00000000, 0.16411355], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "4")] = {"B_initial": -0.23074818, "B_limits": [-0.46149635, 0.00000000], "C_initial": -0.04298619, "C_limits": [-0.24298619, 0.15701381], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("8", "19")] = {"B_initial": -0.14181663, "B_limits": [-0.28363326, 0.00000000], "C_initial": -0.01788013, "C_limits": [-0.21788013, 0.18211987], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("8", "30")] = {"B_initial": -0.19015969, "B_limits": [-0.38031939, 0.00000000], "C_initial": 0.01834855, "C_limits": [-0.18165145, 0.21834855], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("8", "6")] = {"B_initial": -0.02092230, "B_limits": [-0.22092230, 0.17907770], "C_initial": 0.02673016, "C_limits": [-0.17326984, 0.22673016], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42866913, "B_limits": [-0.85733826, 0.00000000], "C_initial": 0.10691669, "C_limits": [0.00000000, 0.21383338], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
# (9, 4) pass 1 moved off a cosine that was already inside the manual window.
special_fit_parameters_set[("9", "4")] = {"B_initial": -0.21691118, "B_limits": [-0.43382235, 0.00000000], "C_initial": -0.00302824, "C_limits": [-0.20302824, 0.19697176], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
# (8, 21): manual B window [0, 0.1] pins B at 0 and collapses the error. This histogram cosine is B=-0.002901.
special_fit_parameters_set[("8", "21")] = {"B_initial": -0.00290108, "B_limits": [-0.20290108, 0.19709892], "C_initial": 0.01509631, "C_limits": [-0.18490369, 0.21509631], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
