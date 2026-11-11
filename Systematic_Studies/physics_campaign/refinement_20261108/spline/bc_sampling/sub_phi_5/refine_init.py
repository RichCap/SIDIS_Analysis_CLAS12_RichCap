# Run-local BC_RC guide for spline phi_h sampling sub_phi_5.
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

# Pass 2: the spline second pass or a BC limit left these histograms off their own cosine.
# Starts are this histogram's weighted cosine. Nominal parameters are not copied.
special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.17716137, "B_limits": [-0.29716137, -0.05716137], "C_initial": 0.02530779, "C_limits": [-0.09469221, 0.14530779], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.18308258, "B_limits": [-0.30308258, -0.06308258], "C_initial": -0.01521670, "C_limits": [-0.13521670, 0.10478330], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.10860800, "B_limits": [-0.22860800, 0.01139200], "C_initial": -0.04570792, "C_limits": [-0.16570792, 0.07429208], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.00211730, "B_limits": [-0.11788270, 0.12211730], "C_initial": -0.01851171, "C_limits": [-0.13851171, 0.10148829], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.01183250, "B_limits": [-0.10816750, 0.13183250], "C_initial": -0.00469976, "C_limits": [-0.12469976, 0.11530024], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03627138, "B_limits": [-0.15627138, 0.08372862], "C_initial": -0.02641146, "C_limits": [-0.14641146, 0.09358854], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": -0.00186169, "B_limits": [-0.12186169, 0.11813831], "C_initial": 0.03241090, "C_limits": [-0.08758910, 0.15241090], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.12206718, "B_limits": [-0.24206718, -0.00206718], "C_initial": -0.01533538, "C_limits": [-0.13533538, 0.10466462], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14808005, "B_limits": [-0.26808005, -0.02808005], "C_initial": 0.04171090, "C_limits": [-0.07828910, 0.16171090], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20618435, "B_limits": [-0.32618435, -0.08618435], "C_initial": 0.08234538, "C_limits": [-0.03765462, 0.20234538], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06849468, "B_limits": [-0.18849468, 0.05150532], "C_initial": -0.09452546, "C_limits": [-0.21452546, 0.02547454], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10435562, "B_limits": [-0.22435562, 0.01564438], "C_initial": -0.00566274, "C_limits": [-0.12566274, 0.11433726], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02418339, "B_limits": [-0.09581661, 0.14418339], "C_initial": 0.03892232, "C_limits": [-0.08107768, 0.15892232], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "1", "3D", "BC")] = {"B_initial": -0.04311249, "B_limits": [-0.16311249, 0.07688751], "C_initial": 0.00868073, "C_limits": [-0.11131927, 0.12868073], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.10315542, "B_limits": [-0.22315542, 0.01684458], "C_initial": 0.02876554, "C_limits": [-0.09123446, 0.14876554], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07544148, "B_limits": [-0.19544148, 0.04455852], "C_initial": -0.00991870, "C_limits": [-0.12991870, 0.11008130], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19831659, "B_limits": [-0.31831659, -0.07831659], "C_initial": -0.00451408, "C_limits": [-0.12451408, 0.11548592], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20944878, "B_limits": [-0.32944878, -0.08944878], "C_initial": 0.08092578, "C_limits": [-0.03907422, 0.20092578], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.22247023, "B_limits": [-0.34247023, -0.10247023], "C_initial": -0.04177917, "C_limits": [-0.16177917, 0.07822083], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24717283, "B_limits": [-0.36717283, -0.12717283], "C_initial": -0.03710203, "C_limits": [-0.15710203, 0.08289797], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.24022315, "B_limits": [-0.36022315, -0.12022315], "C_initial": 0.04212745, "C_limits": [-0.07787255, 0.16212745], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
