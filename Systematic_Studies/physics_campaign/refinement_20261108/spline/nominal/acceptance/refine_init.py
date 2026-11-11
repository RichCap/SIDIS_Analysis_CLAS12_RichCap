# Run-local acceptance guide. The shared Phi_h files are not edited.
# start=auto chose the manual baseline: selected 3D spline B windows have median width 0.0153 and 428 of 452 are narrower than 0.05, and C windows are narrower. Those windows can pin B and C on the limits.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 2: the manual second pass left these histograms off the unconstrained cosine.
# Starts are that cosine. Limits are wide enough that it is not on the boundary.
special_fit_parameters_set[("1", "17")] = {"B_initial": -0.08475911, "B_limits": [-0.20475911, 0.03524089], "C_initial": -0.02190727, "C_limits": [-0.10190727, 0.05809273], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "19")] = {"B_initial": -0.25016967, "B_limits": [-0.37016967, -0.13016967], "C_initial": 0.04852024, "C_limits": [-0.03147976, 0.12852024], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "22")] = {"B_initial": -0.02286569, "B_limits": [-0.14286569, 0.09713431], "C_initial": 0.03267628, "C_limits": [-0.04732372, 0.11267628], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "4")] = {"B_initial": -0.23321868, "B_limits": [-0.35321868, -0.11321868], "C_initial": 0.02482863, "C_limits": [-0.05517137, 0.10482863], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "8")] = {"B_initial": -0.12518388, "B_limits": [-0.26390842, 0.01354066], "C_initial": -0.04454798, "C_limits": [-0.17136598, 0.08227002], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11")] = {"B_initial": -0.26690426, "B_limits": [-0.38690426, -0.14690426], "C_initial": 0.01080598, "C_limits": [-0.06919402, 0.09080598], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8")] = {"B_initial": -0.10464561, "B_limits": [-0.22464561, 0.01535439], "C_initial": -0.00821527, "C_limits": [-0.08821527, 0.07178473], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "20")] = {"B_initial": -0.27670177, "B_limits": [-0.39670177, -0.15670177], "C_initial": 0.09228792, "C_limits": [0.01228792, 0.17228792], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "3")] = {"B_initial": -0.12745048, "B_limits": [-0.24745048, -0.00745048], "C_initial": 0.00110335, "C_limits": [-0.07889665, 0.08110335], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("12", "24")] = {"B_initial": -0.13321706, "B_limits": [-0.25321706, -0.01321706], "C_initial": 0.00842359, "C_limits": [-0.07157641, 0.08842359], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "10")] = {"B_initial": -0.30455710, "B_limits": [-0.42455710, -0.18455710], "C_initial": 0.10193600, "C_limits": [0.02193600, 0.18193600], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4")] = {"B_initial": -0.26543880, "B_limits": [-0.38543880, -0.14543880], "C_initial": -0.02874313, "C_limits": [-0.10874313, 0.05125687], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5")] = {"B_initial": -0.29993425, "B_limits": [-0.41993425, -0.17993425], "C_initial": -0.02434295, "C_limits": [-0.10434295, 0.05565705], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15")] = {"B_initial": -0.30627792, "B_limits": [-0.42627792, -0.18627792], "C_initial": 0.05927655, "C_limits": [-0.02072345, 0.13927655], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "24")] = {"B_initial": -0.21409111, "B_limits": [-0.33409111, -0.09409111], "C_initial": 0.05246161, "C_limits": [-0.02753839, 0.13246161], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("16", "12")] = {"B_initial": -0.36439142, "B_limits": [-0.48439142, -0.24439142], "C_initial": 0.10571495, "C_limits": [0.02571495, 0.18571495], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "29")] = {"B_initial": -0.24265468, "B_limits": [-0.36265468, -0.12265468], "C_initial": 0.07470968, "C_limits": [-0.00529032, 0.15470968], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16")] = {"B_initial": -0.18364488, "B_limits": [-0.30364488, -0.06364488], "C_initial": -0.00800412, "C_limits": [-0.08800412, 0.07199588], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "24")] = {"B_initial": -0.24807167, "B_limits": [-0.36807167, -0.12807167], "C_initial": 0.05741853, "C_limits": [-0.02258147, 0.13741853], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "29")] = {"B_initial": -0.27990732, "B_limits": [-0.39990732, -0.15990732], "C_initial": 0.09171340, "C_limits": [0.01171340, 0.17171340], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33")] = {"B_initial": -0.11007197, "B_limits": [-0.23007197, 0.00992803], "C_initial": -0.09104107, "C_limits": [-0.17104107, -0.01104107], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34")] = {"B_initial": -0.15950529, "B_limits": [-0.27950529, -0.03950529], "C_initial": 0.00178280, "C_limits": [-0.07821720, 0.08178280], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "31")] = {"B_initial": 0.00545095, "B_limits": [-0.11454905, 0.12545095], "C_initial": 0.04124008, "C_limits": [-0.03875992, 0.12124008], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "1")] = {"B_initial": -0.05824511, "B_limits": [-0.17824511, 0.06175489], "C_initial": 0.01088906, "C_limits": [-0.06911094, 0.09088906], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "2")] = {"B_initial": -0.13311946, "B_limits": [-0.25311946, -0.01311946], "C_initial": 0.03048305, "C_limits": [-0.04951695, 0.11048305], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "10")] = {"B_initial": -0.16775511, "B_limits": [-0.28775511, -0.04775511], "C_initial": 0.01648091, "C_limits": [-0.06351909, 0.09648091], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "11")] = {"B_initial": -0.25904908, "B_limits": [-0.37904908, -0.13904908], "C_initial": 0.02519868, "C_limits": [-0.05480132, 0.10519868], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("7", "21")] = {"B_initial": -0.09733463, "B_limits": [-0.21733463, 0.02266537], "C_initial": -0.01262310, "C_limits": [-0.09262310, 0.06737690], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("9", "7")] = {"B_initial": -0.42828668, "B_limits": [-0.54828668, -0.30828668], "C_initial": 0.10839131, "C_limits": [0.02839131, 0.18839131], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "14")] = {"B_initial": -0.0274, "B_limits": [-0.18, 0.12], "C_initial": 0.0351, "C_limits": [-0.08, 0.16], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
