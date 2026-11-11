# Run-local BC_RC guide for spline phi_h sampling sub_phi_7.
# The shared Phi_h files are not edited.
# start=auto chose the universal spline file.
# A BC_RC histogram selects untagged or BC keys, not the tight 3D acceptance windows.
# Selected B widths have median 0.17, and 305 of 452 bins leave B unlimited.
# --use_spline_init is not also passed. Nominal parameters are not copied onto these histograms.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2: pinned or second-pass bins. Starts are this histogram's weighted cosine, not the nominal.

special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.17803546, "B_limits": [-0.29803546, -0.05803546], "C_initial": 0.02474640, "C_limits": [-0.09525360, 0.14474640], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.18388971, "B_limits": [-0.30388971, -0.06388971], "C_initial": -0.01576277, "C_limits": [-0.13576277, 0.10423723], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.10970911, "B_limits": [-0.22970911, 0.01029089], "C_initial": -0.04660385, "C_limits": [-0.16660385, 0.07339615], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.00252120, "B_limits": [-0.11747880, 0.12252120], "C_initial": -0.01873939, "C_limits": [-0.13873939, 0.10126061], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.01155922, "B_limits": [-0.10844078, 0.13155922], "C_initial": -0.00420434, "C_limits": [-0.12420434, 0.11579566], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03706508, "B_limits": [-0.15706508, 0.08293492], "C_initial": -0.02690998, "C_limits": [-0.14690998, 0.09309002], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": -0.00058931, "B_limits": [-0.12058931, 0.11941069], "C_initial": 0.03325116, "C_limits": [-0.08674884, 0.15325116], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.12197562, "B_limits": [-0.24197562, -0.00197562], "C_initial": -0.01560394, "C_limits": [-0.13560394, 0.10439606], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14795057, "B_limits": [-0.26795057, -0.02795057], "C_initial": 0.04128404, "C_limits": [-0.07871596, 0.16128404], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20575459, "B_limits": [-0.32575459, -0.08575459], "C_initial": 0.08153955, "C_limits": [-0.03846045, 0.20153955], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06838264, "B_limits": [-0.18838264, 0.05161736], "C_initial": -0.09449783, "C_limits": [-0.21449783, 0.02550217], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10429650, "B_limits": [-0.22429650, 0.01570350], "C_initial": -0.00574347, "C_limits": [-0.12574347, 0.11425653], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "6", "3D", "BC")] = {"B_initial": -0.22403883, "B_limits": [-0.34403883, -0.10403883], "C_initial": 0.03924025, "C_limits": [-0.08075975, 0.15924025], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02512263, "B_limits": [-0.09487737, 0.14512263], "C_initial": 0.03940607, "C_limits": [-0.08059393, 0.15940607], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "1", "3D", "BC")] = {"B_initial": -0.04278895, "B_limits": [-0.16278895, 0.07721105], "C_initial": 0.00825049, "C_limits": [-0.11174951, 0.12825049], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.10328572, "B_limits": [-0.22328572, 0.01671428], "C_initial": 0.02853355, "C_limits": [-0.09146645, 0.14853355], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07519174, "B_limits": [-0.19519174, 0.04480826], "C_initial": -0.00924389, "C_limits": [-0.12924389, 0.11075611], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19821927, "B_limits": [-0.31821927, -0.07821927], "C_initial": -0.00405340, "C_limits": [-0.12405340, 0.11594660], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20962392, "B_limits": [-0.32962392, -0.08962392], "C_initial": 0.08133057, "C_limits": [-0.03866943, 0.20133057], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.22186458, "B_limits": [-0.34186458, -0.10186458], "C_initial": -0.04135064, "C_limits": [-0.16135064, 0.07864936], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24725882, "B_limits": [-0.36725882, -0.12725882], "C_initial": -0.03747414, "C_limits": [-0.15747414, 0.08252586], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.24029847, "B_limits": [-0.36029847, -0.12029847], "C_initial": 0.04159646, "C_limits": [-0.07840354, 0.16159646], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
