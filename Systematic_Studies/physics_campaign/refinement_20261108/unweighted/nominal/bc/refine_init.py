# Run-local unweighted nominal BC+RC guide.
# start=auto chose the universal spline file. A BC_RC histogram selects untagged or BC keys, not the tight 3D acceptance windows.
# Those selected B widths have median 0.17, and 305 of 452 have no B window. They are not tight enough to pin the family.
# The shared Phi_h files are not edited. --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline-file pass left these BC histograms off the cosine they support.
# Keys are (q, z, 3D, BC) so they do not apply to an acceptance histogram. Limits keep that cosine off the boundary.
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.00316822, "B_limits": [-0.11683178, 0.12316822], "C_initial": -0.03066728, "C_limits": [-0.11066728, 0.04933272], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.19894659, "B_limits": [-0.31894659, -0.07894659], "C_initial": 0.07805132, "C_limits": [-0.00194868, 0.15805132], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.12035860, "B_limits": [-0.24035860, -0.00035860], "C_initial": -0.01935402, "C_limits": [-0.09935402, 0.06064598], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.21711227, "B_limits": [-0.33711227, -0.09711227], "C_initial": 0.05333352, "C_limits": [-0.02666648, 0.13333352], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.19747615, "B_limits": [-0.31747615, -0.07747615], "C_initial": 0.06524455, "C_limits": [-0.01475545, 0.14524455], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "2", "3D", "BC")] = {"B_initial": -0.11146089, "B_limits": [-0.23146089, 0.00853911], "C_initial": 0.01675118, "C_limits": [-0.06324882, 0.09675118], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.20891642, "B_limits": [-0.32891642, -0.08891642], "C_initial": -0.00694866, "C_limits": [-0.08694866, 0.07305134], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "17", "3D", "BC")] = {"B_initial": -0.19795150, "B_limits": [-0.31795150, -0.07795150], "C_initial": -0.00280262, "C_limits": [-0.08280262, 0.07719738], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "3", "3D", "BC")] = {"B_initial": -0.09869251, "B_limits": [-0.21869251, 0.02130749], "C_initial": -0.01532205, "C_limits": [-0.09532205, 0.06467795], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.23088951, "B_limits": [-0.35088951, -0.11088951], "C_initial": 0.09028258, "C_limits": [0.01028258, 0.17028258], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "15", "3D", "BC")] = {"B_initial": -0.08531726, "B_limits": [-0.20531726, 0.03468274], "C_initial": -0.01668489, "C_limits": [-0.09668489, 0.06331511], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.26521508, "B_limits": [-0.38521508, -0.14521508], "C_initial": 0.05286674, "C_limits": [-0.02713326, 0.13286674], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
# These histograms are still off their own unconstrained cosine. The spline nominal is not the start.
special_fit_parameters_set[("2", "7", "3D", "BC")] = {"B_initial": 0.01265137, "B_limits": [-0.10734863, 0.13265137], "C_initial": 0.01712062, "C_limits": [-0.06287938, 0.09712062], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("2", "6", "3D", "BC")] = {"B_initial": -0.33004155, "B_limits": [-0.45004155, -0.21004155], "C_initial": -0.03363717, "C_limits": [-0.11363717, 0.04636283], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.17723501, "B_limits": [-0.29723501, -0.05723501], "C_initial": 0.02940447, "C_limits": [-0.05059553, 0.10940447], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.03399301, "B_limits": [-0.08600699, 0.15399301], "C_initial": 0.02205273, "C_limits": [-0.05794727, 0.10205273], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.25043482, "B_limits": [-0.37043482, -0.13043482], "C_initial": -0.03440231, "C_limits": [-0.11440231, 0.04559769], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("6", "6", "3D", "BC")] = {"B_initial": -0.38230368, "B_limits": [-0.50230368, -0.26230368], "C_initial": -0.02201966, "C_limits": [-0.10201966, 0.05798034], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.05513797, "B_limits": [-0.17513797, 0.06486203], "C_initial": -0.01732663, "C_limits": [-0.09732663, 0.06267337], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02945635, "B_limits": [-0.09054365, 0.14945635], "C_initial": 0.02605153, "C_limits": [-0.05394847, 0.10605153], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07344510, "B_limits": [-0.19344510, 0.04655490], "C_initial": -0.01818285, "C_limits": [-0.09818285, 0.06181715], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
