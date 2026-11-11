# Run-local RC guide for the event-yield RC baseline. The shared Phi_h files are not edited.
# start=auto chose the manual baseline: selected 3D RC spline B windows have median width 0.0126 and 436 of 452 are narrower than 0.05. Do not pass the universal spline file as well.
# fit_before_guide.json is the earlier guided history and is not this initializer.
import importlib.util
manual_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py"
spec = importlib.util.spec_from_file_location("manual_phi_init", manual_path)
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Pass 2: manual second pass left these RC histograms off their own unconstrained cosine.
# Starts are that cosine. Limits keep it off the boundary. Acceptance parameters are not copied here.
# (1, 8) is this RC histogram's cosine, not the acceptance result. The manual B limits [-0.05, 0.05] and C limits [0, 0.1] cannot reach it.
special_fit_parameters_set[("1", "8", "3D", "RC")] = {"B_initial": -0.10580763, "B_limits": [-0.24580763, 0.03419237], "C_initial": -0.04524792, "C_limits": [-0.16524792, 0.07475208], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}

special_fit_parameters_set[("10", "11", "3D", "RC")] = {"B_initial": -0.19686719, "B_limits": [-0.31686719, -0.07686719], "C_initial": -0.00420065, "C_limits": [-0.08420065, 0.07579935], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "20", "3D", "RC")] = {"B_initial": -0.20589851, "B_limits": [-0.32589851, -0.08589851], "C_initial": 0.08123275, "C_limits": [0.00123275, 0.16123275], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "RC")] = {"B_initial": -0.21629580, "B_limits": [-0.33629580, -0.09629580], "C_initial": -0.03899700, "C_limits": [-0.11899700, 0.04100300], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5", "3D", "RC")] = {"B_initial": -0.24472995, "B_limits": [-0.36709492, -0.12236497], "C_initial": -0.03672520, "C_limits": [-0.11672520, 0.04327480], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15", "3D", "RC")] = {"B_initial": -0.24045671, "B_limits": [-0.36068506, -0.12022835], "C_initial": 0.04191808, "C_limits": [-0.03808192, 0.12191808], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16", "3D", "RC")] = {"B_initial": -0.12195094, "B_limits": [-0.24195094, -0.00195094], "C_initial": -0.01554552, "C_limits": [-0.09554552, 0.06445448], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "29", "3D", "RC")] = {"B_initial": -0.20165174, "B_limits": [-0.32165174, -0.08165174], "C_initial": 0.08002387, "C_limits": [0.00002387, 0.16002387], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "RC")] = {"B_initial": -0.06747453, "B_limits": [-0.18747453, 0.05252547], "C_initial": -0.09409653, "C_limits": [-0.17409653, -0.01409653], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
