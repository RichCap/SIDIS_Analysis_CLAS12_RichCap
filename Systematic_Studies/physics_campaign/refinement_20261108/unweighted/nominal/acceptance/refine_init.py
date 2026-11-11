# Run-local unweighted nominal acceptance guide.
# start=auto chose the manual baseline: the 3D spline keys these histograms select have median B width 0.0153, and 428 of 452 are narrower than 0.05. C windows are narrower. Those windows can pin a fit on the limits.
# The shared Phi_h files are not edited. --use_spline_init is not passed.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 2. Pass 1 used the manual baseline and made these histograms worse than the cosine they support.
# Starts are that cosine. Limits are wide enough that the cosine is not on the boundary.
# (1,8), (5,7), and (8,30) are not opened: the free cosine stays inside the stored errors.
special_fit_parameters_set[("1", "4")] = {"B_initial": -0.22004090, "B_limits": [-0.34004090, -0.10004090], "C_initial": 0.02256412, "C_limits": [-0.05743588, 0.10256412], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "19")] = {"B_initial": -0.26164303, "B_limits": [-0.38164303, -0.14164303], "C_initial": 0.04898305, "C_limits": [-0.03101695, 0.12898305], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "22")] = {"B_initial": 0.00627897, "B_limits": [-0.11372103, 0.12627897], "C_initial": 0.02230841, "C_limits": [-0.05769159, 0.10230841], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "16")] = {"B_initial": -0.17985259, "B_limits": [-0.29985259, -0.05985259], "C_initial": 0.00053418, "C_limits": [-0.07946582, 0.08053418], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "29")] = {"B_initial": -0.28177945, "B_limits": [-0.40177945, -0.16177945], "C_initial": 0.08418979, "C_limits": [0.00418979, 0.16418979], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "34")] = {"B_initial": -0.20446920, "B_limits": [-0.32446920, -0.08446920], "C_initial": 0.01547153, "C_limits": [-0.06452847, 0.09547153], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "2")] = {"B_initial": -0.15115589, "B_limits": [-0.27115589, -0.03115589], "C_initial": 0.01197937, "C_limits": [-0.06802063, 0.09197937], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18437104, "B_limits": [-0.30437104, -0.06437104], "C_initial": -0.01254948, "C_limits": [-0.09254948, 0.06745052], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "24")] = {"B_initial": -0.30808417, "B_limits": [-0.42808417, -0.18808417], "C_initial": 0.07554590, "C_limits": [-0.00445410, 0.15554590], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "29")] = {"B_initial": -0.27059146, "B_limits": [-0.39059146, -0.15059146], "C_initial": 0.07153700, "C_limits": [-0.00846300, 0.15153700], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "31")] = {"B_initial": 0.01822031, "B_limits": [-0.10177969, 0.13822031], "C_initial": 0.03775394, "C_limits": [-0.04224606, 0.11775394], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "10")] = {"B_initial": -0.17939770, "B_limits": [-0.29939770, -0.05939770], "C_initial": 0.00370648, "C_limits": [-0.07629352, 0.08370648], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "11")] = {"B_initial": -0.26672566, "B_limits": [-0.38672566, -0.14672566], "C_initial": 0.02089351, "C_limits": [-0.05910649, 0.10089351], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "21")] = {"B_initial": -0.08972865, "B_limits": [-0.20972865, 0.03027135], "C_initial": -0.01502952, "C_limits": [-0.09502952, 0.06497048], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("9", "7")] = {"B_initial": -0.47708271, "B_limits": [-0.59708271, -0.35708271], "C_initial": 0.09302507, "C_limits": [0.01302507, 0.17302507], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10076688, "B_limits": [-0.22076688, 0.01923312], "C_initial": -0.02547120, "C_limits": [-0.10547120, 0.05452880], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26915263, "B_limits": [-0.38915263, -0.14915263], "C_initial": 0.00750208, "C_limits": [-0.07249792, 0.08750208], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "17")] = {"B_initial": -0.26612178, "B_limits": [-0.38612178, -0.14612178], "C_initial": 0.00736019, "C_limits": [-0.07263981, 0.08736019], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12826487, "B_limits": [-0.24826487, -0.00826487], "C_initial": -0.00895825, "C_limits": [-0.08895825, 0.07104175], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "20")] = {"B_initial": -0.29138722, "B_limits": [-0.41138722, -0.17138722], "C_initial": 0.09626673, "C_limits": [0.01626673, 0.17626673], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13972450, "B_limits": [-0.25972450, -0.01972450], "C_initial": 0.00852211, "C_limits": [-0.07147789, 0.08852211], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "10")] = {"B_initial": -0.35770780, "B_limits": [-0.47770780, -0.23770780], "C_initial": 0.07859628, "C_limits": [-0.00140372, 0.15859628], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5")] = {"B_initial": -0.30805664, "B_limits": [-0.42805664, -0.18805664], "C_initial": -0.03065942, "C_limits": [-0.11065942, 0.04934058], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "15")] = {"B_initial": -0.11383617, "B_limits": [-0.23383617, 0.00616383], "C_initial": -0.01057616, "C_limits": [-0.09057616, 0.06942384], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15")] = {"B_initial": -0.33023025, "B_limits": [-0.45023025, -0.21023025], "C_initial": 0.06859452, "C_limits": [-0.01140548, 0.14859452], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "24")] = {"B_initial": -0.23923015, "B_limits": [-0.35923015, -0.11923015], "C_initial": 0.06223193, "C_limits": [-0.01776807, 0.14223193], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("16", "12")] = {"B_initial": -0.38178500, "B_limits": [-0.50178500, -0.26178500], "C_initial": 0.10302794, "C_limits": [0.02302794, 0.18302794], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
# These five histograms still sit off the unconstrained cosine after the manual pass. Starts are that cosine.
special_fit_parameters_set[("10", "9")] = {"B_initial": -0.15768987, "B_limits": [-0.27768987, -0.03768987], "C_initial": -0.02472932, "C_limits": [-0.10472932, 0.05527068], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "14")] = {"B_initial": -0.03546514, "B_limits": [-0.15546514, 0.08453486], "C_initial": 0.02520174, "C_limits": [-0.05479826, 0.10520174], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "29")] = {"B_initial": -0.26792462, "B_limits": [-0.38792462, -0.14792462], "C_initial": 0.03400972, "C_limits": [-0.04599028, 0.11400972], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "35")] = {"B_initial": -0.27647004, "B_limits": [-0.39647004, -0.15647004], "C_initial": 0.07453438, "C_limits": [-0.00546562, 0.15453438], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("17", "2")] = {"B_initial": -0.06597417, "B_limits": [-0.18597417, 0.05402583], "C_initial": -0.00350063, "C_limits": [-0.08350063, 0.07649937], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
