# Run-local BC_RC guide for spline sub_y_5. The shared Phi_h files are not edited.
# start=auto chose the universal spline file. A BC_RC histogram selects 3D-BC, then BC, then the untagged key.
# Those B widths have median 0.17 and 5 of 452 are narrower than 0.05, so the windows are not tight.
# --use_spline_init is not also passed.
import importlib.util
spline_path = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py"
spec = importlib.util.spec_from_file_location("spline_phi_init_sub_y_5", spline_path)
spline_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spline_phi_init)
special_fit_parameters_set = dict(spline_phi_init.special_fit_parameters_set)

# Pass 2. The spline start left these histograms off their own cosine.
# Untagged keys with no B/C limits let the rough moment build a window around a bad start.
# Tagged keys whose limits exclude this histogram's cosine are opened around that cosine.
# (1, 8) is the second-pass edge at B=-0.045 from the legacy BC window [-0.03, 0.05] and C [0, 0.1].
# Nominal values are not copied. The half-width second pass is off when |B| or |C| is below 0.05.
special_fit_parameters_set[("1", "4", "3D", "BC")] = {"B_initial": -0.19024145, "B_limits": [-0.39024145, 0.00975855], "C_initial": 0.01016005, "C_limits": [-0.18983995, 0.21016005], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "5", "3D", "BC")] = {"B_initial": -0.18138766, "B_limits": [-0.38138766, 0.01861234], "C_initial": -0.01668257, "C_limits": [-0.21668257, 0.18331743], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "8", "3D", "BC")] = {"B_initial": -0.12099546, "B_limits": [-0.32099546, 0.07900454], "C_initial": -0.05388825, "C_limits": [-0.25388825, 0.14611175], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("1", "9", "3D", "BC")] = {"B_initial": 0.01109047, "B_limits": [-0.18890953, 0.21109047], "C_initial": -0.01348648, "C_limits": [-0.21348648, 0.18651352], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "16", "3D", "BC")] = {"B_initial": 0.00897287, "B_limits": [-0.19102713, 0.20897287], "C_initial": -0.00817371, "C_limits": [-0.20817371, 0.19182629], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "17", "3D", "BC")] = {"B_initial": -0.03374531, "B_limits": [-0.23374531, 0.16625469], "C_initial": -0.02574494, "C_limits": [-0.22574494, 0.17425506], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("1", "22", "3D", "BC")] = {"B_initial": 0.00445756, "B_limits": [-0.19554244, 0.20445756], "C_initial": 0.03886337, "C_limits": [-0.16113663, 0.23886337], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("2", "29", "3D", "BC")] = {"B_initial": -0.14352417, "B_limits": [-0.34352417, 0.05647583], "C_initial": 0.05583148, "C_limits": [-0.14416852, 0.25583148], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("3", "16", "3D", "BC")] = {"B_initial": -0.11685951, "B_limits": [-0.31685951, 0.08314049], "C_initial": -0.01687662, "C_limits": [-0.21687662, 0.18312338], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "24", "3D", "BC")] = {"B_initial": -0.14466012, "B_limits": [-0.34466012, 0.05533988], "C_initial": 0.04115050, "C_limits": [-0.15884950, 0.24115050], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("3", "29", "3D", "BC")] = {"B_initial": -0.20762048, "B_limits": [-0.40762048, -0.00762048], "C_initial": 0.08460411, "C_limits": [-0.11539589, 0.28460411], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "33", "3D", "BC")] = {"B_initial": -0.06891940, "B_limits": [-0.26891940, 0.13108060], "C_initial": -0.09269436, "C_limits": [-0.29269436, 0.10730564], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("4", "34", "3D", "BC")] = {"B_initial": -0.10529947, "B_limits": [-0.30529947, 0.09470053], "C_initial": -0.00882737, "C_limits": [-0.20882737, 0.19117263], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "4", "3D", "BC")] = {"B_initial": -0.17416448, "B_limits": [-0.37416448, 0.02583552], "C_initial": 0.00934759, "C_limits": [-0.19065241, 0.20934759], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "9", "3D", "BC")] = {"B_initial": -0.06043469, "B_limits": [-0.26043469, 0.13956531], "C_initial": 0.01496054, "C_limits": [-0.18503946, 0.21496054], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "15", "3D", "BC")] = {"B_initial": -0.06320915, "B_limits": [-0.26320915, 0.13679085], "C_initial": 0.01356189, "C_limits": [-0.18643811, 0.21356189], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("5", "31", "3D", "BC")] = {"B_initial": 0.02172719, "B_limits": [-0.17827281, 0.22172719], "C_initial": 0.03679101, "C_limits": [-0.16320899, 0.23679101], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "1", "3D", "BC")] = {"B_initial": -0.04267456, "B_limits": [-0.24267456, 0.15732544], "C_initial": 0.01665025, "C_limits": [-0.18334975, 0.21665025], "Allow_Multiple_Fits": False, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("6", "2", "3D", "BC")] = {"B_initial": -0.09959979, "B_limits": [-0.29959979, 0.10040021], "C_initial": 0.03714840, "C_limits": [-0.16285160, 0.23714840], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("7", "35", "3D", "BC")] = {"B_initial": -0.20597523, "B_limits": [-0.40597523, -0.00597523], "C_initial": 0.07894692, "C_limits": [-0.12105308, 0.27894692], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("8", "30", "3D", "BC")] = {"B_initial": -0.12921313, "B_limits": [-0.32921313, 0.07078687], "C_initial": 0.01011805, "C_limits": [-0.18988195, 0.21011805], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "5", "3D", "BC")] = {"B_initial": -0.22821235, "B_limits": [-0.42821235, -0.02821235], "C_initial": -0.03217466, "C_limits": [-0.23217466, 0.16782534], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "8", "3D", "BC")] = {"B_initial": -0.07456166, "B_limits": [-0.27456166, 0.12543834], "C_initial": -0.00776293, "C_limits": [-0.20776293, 0.19223707], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("10", "11", "3D", "BC")] = {"B_initial": -0.19620829, "B_limits": [-0.39620829, 0.00379171], "C_initial": -0.00166947, "C_limits": [-0.20166947, 0.19833053], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("11", "20", "3D", "BC")] = {"B_initial": -0.20722177, "B_limits": [-0.40722177, -0.00722177], "C_initial": 0.08035808, "C_limits": [-0.11964192, 0.28035808], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
special_fit_parameters_set[("13", "4", "3D", "BC")] = {"B_initial": -0.21950328, "B_limits": [-0.41950328, -0.01950328], "C_initial": -0.04164058, "C_limits": [-0.24164058, 0.15835942], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("14", "5", "3D", "BC")] = {"B_initial": -0.24355132, "B_limits": [-0.44355132, -0.04355132], "C_initial": -0.03511973, "C_limits": [-0.23511973, 0.16488027], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("15", "15", "3D", "BC")] = {"B_initial": -0.23987825, "B_limits": [-0.43987825, -0.03987825], "C_initial": 0.04128941, "C_limits": [-0.15871059, 0.24128941], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": False}
special_fit_parameters_set[("16", "12", "3D", "BC")] = {"B_initial": -0.28257575, "B_limits": [-0.48257575, -0.08257575], "C_initial": 0.08087654, "C_limits": [-0.11912346, 0.28087654], "Allow_Multiple_Fits": True, "Allow_Multiple_Fits_C": True}
