# Universal initializer: 3D keys preserved (do not retune). Tight 5D spline keys removed.
# 5D keys: 3D-based B/C inits with wide limits for former high-redchi2 bins; (12,13) also has fit_range 15-345.
# Do not edit Phi_h_Fit_Parameters_Initialize.py
special_fit_parameters_set = {
    ("1", "All", "Trusted"): {
        "fit_range_lower": 60,
        "fit_range_upper": 300
    },
    ("1", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 60,
        "fit_range_upper": 300
    },
    ("2", "All", "Trusted"): {
        "fit_range_lower": 45,
        "fit_range_upper": 330
    },
    ("2", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 45,
        "fit_range_upper": 315
    },
    ("3", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 330
    },
    ("3", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("4", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("4", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("5", "All", "Trusted"): {
        "fit_range_lower": 60,
        "fit_range_upper": 300
    },
    ("5", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 60,
        "fit_range_upper": 300
    },
    ("6", "All", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("6", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("7", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("7", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("8", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("8", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("9", "All", "Trusted"): {
        "fit_range_lower": 45,
        "fit_range_upper": 330
    },
    ("9", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 45,
        "fit_range_upper": 315
    },
    ("10", "All", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("10", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("11", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("11", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("12", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("12", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("13", "All", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("13", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("14", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("14", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("15", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("15", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("16", "All", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("16", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 30,
        "fit_range_upper": 330
    },
    ("17", "All", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("17", "All", "Sectors", "Trusted"): {
        "fit_range_lower": 15,
        "fit_range_upper": 345
    },
    ("1", "All"): {
        "B_initial": -0.05588,
        "B_limits":  [0, -0.075],
        "C_initial": 0.02465,
        "C_limits":  [0, 0.05],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": False
    },
    ("1", "1"): {
        "B_initial": -0.04345,
        "B_limits":  [-0.15, 0.025],
        "C_initial": 0.04139,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "2"): {
        "B_initial": -0.13607,
        "B_limits":  [-0.225, 0],
        "C_initial": 0.03992,
        "C_limits":  [-0.075, 0.125],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "3"): {
        "B_initial": -0.04877,
        "B_limits":  [-0.2, 0.05],
        "C_initial": 0.0442,
        "C_limits":  [-0.1, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "4"): {
        "B_initial": -0.265,
        "B_limits":  [-0.3, -0.2],
        "C_initial": -0.029,
        "C_limits":  [-0.035, -0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "5"): {
        "B_initial": -0.25,
        "B_limits":  [-0.37, -0.235],
        "C_initial": 0,
        "C_limits":  [-0.05, 0.05],
        "Allow_Multiple_Fits":   False,
        "Allow_Multiple_Fits_C": False
    },
    ("1", "6"): {
        "B_initial": -0.26,
        "B_limits":  [-0.37, -0.2],
        "C_initial": 0.033,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "7"): {
        "B_initial": -0.4,
        "B_limits":  [-0.6, -0.26],
        "C_initial": 0.07,
        "C_limits":  [-0.1, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "8"): {
        "B_initial": 0.01448,
        "B_limits":  [-0.05, 0.05],
        "C_initial": 0.05767,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "9"): {
        "B_initial": -0.04971,
        "B_limits":  [-0.2, 0],
        "C_initial": 0.05967,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "10"): {
        "B_initial": -0.12198,
        "B_limits":  [-0.2, -0.05],
        "C_initial": 0.03753,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "12"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "14"): {
        "B_initial": -0.3,
        "B_limits":  [-0.4, -0.275],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "15"): {
        "B_initial": -0.03952,
        "B_limits":  [0.05, -0.15],
        "C_initial": -0.1,
        "C_limits":  [-0.025, -0.15],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "16"): {
        "B_initial": -0.08253,
        "B_limits":  [-0.15, -0.05],
        "C_initial": -0.00476,
        "C_limits":  [-0.1, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "17"): {
        "B_initial": -0.13,
        "B_limits":  [-0.15, -0.05],
        "C_initial": 0.003,
        "C_limits":  [0, 0.05],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "18"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "20"): {
        "B_initial": -0.3,
        "B_limits":  [-0.4, -0.25],
        "C_initial": 0.09,
        "C_limits":  [0.04, 0.2],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "22"): {
        "B_initial": -0.1,
        "B_limits":  [0, -0.15],
        "C_initial": -0.05,
        "C_limits":  [-0.025, -0.15],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "24"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "25"): {
        "B_initial": -0.2,
        "B_limits":  [-0.15, -0.25],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "26"): {
        "B_initial": -0.3,
        "B_limits":  [-0.2, -0.5],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "29"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "30"): {
        "B_initial": -0.1,
        "B_limits":  [0, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "31"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "32"): {
        "B_initial": -0.2,
        "B_limits":  [-0.1, -0.3],
        "C_initial": 0.02,
        "C_limits":  [0, 0.08],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "All"): {
        "B_initial": -0.08714,
        "B_limits":  [-0.105, -0.06],
        "C_initial": 0.02002,
        "C_limits":  [0, 0.05],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "1"): {
        "B_initial": -0.02,
        "B_limits":  [-0.15, 0.001],
        "C_initial": 0.05,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": 0,
        "C_limits":  [-0.05, 0.05],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "4"): {
        "B_initial": -0.2,
        "B_limits":  [-0.1, -0.3],
        "C_initial": 0,
        "C_limits":  [-0.1, 0.75],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "5"): {
        "B_initial": -0.27,
        "B_limits":  [-0.35, -0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "6"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": 0.017,
        "C_limits":  [0.005, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "7"): {
        "B_initial": -0.03,
        "B_limits":  [-0.048, -0.028],
        "C_initial": 0.1,
        "C_limits":  [0.06, 0.2],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "9"): {
        "B_initial": -0.1,
        "B_limits":  [-0.05, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "11"): {
        "B_initial": -0.2,
        "B_limits":  [-0.3, -0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "12"): {
        "B_initial": -0.35,
        "B_limits":  [-0.45, -0.25],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "14"): {
        "B_initial": -0.05,
        "B_limits":  [-0.4, 0],
        "C_initial": 0.1,
        "C_limits":  [0.06, 0.2],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "17"): {
        "B_initial": -0.25,
        "B_limits":  [-0.2, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "18"): {
        "B_initial": -0.32,
        "B_limits":  [-0.29, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "21"): {
        "B_initial": -0.15,
        "B_limits":  [-0.1, -0.2],
        "C_initial": -0.05,
        "C_limits":  [0, -0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "25"): {
        "B_initial": 0,
        "B_limits":  [-0.02, -0.06],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "29"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": 0.01,
        "C_limits":  [-0.15, 0.025],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "31"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "32"): {
        "B_initial": -0.02,
        "B_limits":  [-0.1, 0.005],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "33"): {
        "B_initial": -0.06,
        "B_limits":  [-0.1, 0.0005],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "34"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "All"): {
        "B_initial": -0.09365,
        "B_limits":  [-0.12, -0.06],
        "C_initial": -0.005016,
        "C_limits":  [-0.025, 0.025],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "4"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "5"): {
        "B_initial": -0.25,
        "B_limits":  [-0.3, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "6"): {
        "B_initial": -0.3,
        "B_limits":  [-0.2, -0.4],
        "C_initial": 0.05,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "9"): {
        "B_initial": -0.1,
        "B_limits":  [-0.15, -0.056],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "10"): {
        "B_initial": -0.12,
        "B_limits":  [-0.2, 0],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "11"): {
        "B_initial": -0.2547,
        "B_limits":  [-0.4, -0.14],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "12"): {
        "B_initial": -0.3,
        "B_limits":  [-0.2, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "18"): {
        "B_initial": -0.4,
        "B_limits":  [-0.2, -0.5],
        "C_initial": 0,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "24"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": -0.06,
        "C_limits":  [-0.15, 0.2],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "29"): {
        "B_initial": -0.2,
        "B_limits":  [-0.15, -0.3],
        "C_initial": 0,
        "C_limits":  [-0.03, 0.005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "All"): {
        "B_initial": -0.08944,
        "B_limits":  [-0.105, -0.06],
        "C_initial": -0.009253,
        "C_limits":  [-0.035, 0],
        "Allow_Multiple_Fits":   False,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "4"): {
        "B_initial": -0.2,
        "B_limits":  [-0.3, -0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "5"): {
        "B_initial": -0.3,
        "B_limits":  [-0.2, -0.4],
        "C_initial": -0.005,
        "C_limits":  [0, -0.1],
        "Allow_Multiple_Fits":   False,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "10"): {
        "B_initial": -0.2,
        "B_limits":  [-0.1, -0.3],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "11"): {
        "B_initial": -0.22,
        "B_limits":  [-0.3, -0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "12"): {
        "B_initial": -0.27,
        "B_limits":  [-0.32, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "18"): {
        "B_initial": -0.25,
        "B_limits":  [-0.3, -0.2],
        "C_initial": -0.06,
        "C_limits":  [-0.1, -0.03],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "23"): {
        "B_initial": -0.2,
        "B_limits":  [-0.22, -0.15],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "24"): {
        "B_initial": -0.22625,
        "B_limits":  [-0.25, -0.19],
        "C_initial": -0.01,
        "C_limits":  [-0.07, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "29"): {
        "B_initial": -0.18115,
        "B_limits":  [-0.25, -0.1],
        "C_initial": -0.02378,
        "C_limits":  [-0.1, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "31"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "32"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "33"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "34"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "All"): {
        "B_initial": -0.06159,
        "B_limits":  [-0.1, -0.01],
        "C_initial": 0.01978,
        "C_limits":  [-0.015, 0.05],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "1"): {
        "B_initial": -0.11,
        "B_limits":  [-0.15, 0],
        "C_initial": -0.01,
        "C_limits":  [-0.07, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "2"): {
        "B_initial": -0.1,
        "B_limits":  [-0.2, 0],
        "C_initial": -0.05,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "3"): {
        "B_initial": -0.12,
        "B_limits":  [-0.15, -0.1],
        "C_initial": 0.03,
        "C_limits":  [0.01, 0.02],
        "Allow_Multiple_Fits":   False,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "4"): {
        "B_initial": -0.28,
        "B_limits":  [-0.3, -0.03],
        "C_initial": 0.01,
        "C_limits":  [-0.05, 0.035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "5"): {
        "B_initial": -0.3,
        "B_limits":  [-0.35, -0.2],
        "C_initial": 0.01,
        "C_limits":  [-0.03, 0.08],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "6"): {
        "B_initial": -0.4,
        "B_limits":  [-0.5, -0.3],
        "C_initial": 0.03,
        "C_limits":  [0.01, 0.14],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "7"): {
        "B_initial": -0.1,
        "B_limits":  [-0.15, 0],
        "C_initial": -0.02,
        "C_limits":  [-0.07, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "8"): {
        "B_initial": -0.1,
        "B_limits":  [-0.2, 0],
        "C_initial": 0.035,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "9"): {
        "B_initial": -0.16,
        "B_limits":  [-0.22, -0.1],
        "C_initial": 0.015,
        "C_limits":  [-0.05, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "10"): {
        "B_initial": -0.24,
        "B_limits":  [-0.3, -0.03],
        "C_initial": 0.015,
        "C_limits":  [-0.05, 0.035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "11"): {
        "B_initial": -0.3,
        "B_limits":  [-0.35, -0.2],
        "C_initial": 0,
        "C_limits":  [-0.03, 0.08],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "12"): {
        "B_initial": -0.4,
        "B_limits":  [-0.5, -0.3],
        "C_initial": 0.075,
        "C_limits":  [0.01, 0.14],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "13"): {
        "B_initial": -0.027,
        "B_limits":  [-0.15, 0],
        "C_initial": 0,
        "C_limits":  [-0.07, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "14"): {
        "B_initial": -0.1,
        "B_limits":  [-0.2, 0],
        "C_initial": 0,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "15"): {
        "B_initial": -0.135,
        "B_limits":  [-0.22, -0.1],
        "C_initial": -0.005,
        "C_limits":  [-0.05, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "16"): {
        "B_initial": -0.21,
        "B_limits":  [-0.3, -0.03],
        "C_initial": -0.025,
        "C_limits":  [-0.05, 0.035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "17"): {
        "B_initial": -0.26,
        "B_limits":  [-0.35, -0.2],
        "C_initial": 0.022,
        "C_limits":  [-0.03, 0.08],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "18"): {
        "B_initial": -0.4,
        "B_limits":  [-0.5, -0.3],
        "C_initial": 0.1,
        "C_limits":  [0.01, 0.14],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "19"): {
        "B_initial": -0.1,
        "B_limits":  [-0.15, 0],
        "C_initial": -0.03,
        "C_limits":  [-0.07, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "20"): {
        "B_initial": -0.1,
        "B_limits":  [-0.2, 0],
        "C_initial": 0,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "21"): {
        "B_initial": -0.15,
        "B_limits":  [-0.22, -0.1],
        "C_initial": -0.04,
        "C_limits":  [-0.05, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "22"): {
        "B_initial": -0.2,
        "B_limits":  [-0.3, -0.03],
        "C_initial": 0,
        "C_limits":  [-0.05, 0.035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "23"): {
        "B_initial": -0.25,
        "B_limits":  [-0.35, -0.2],
        "C_initial": 0.041,
        "C_limits":  [-0.03, 0.08],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "25"): {
        "B_initial": -0.1,
        "B_limits":  [-0.15, 0],
        "C_initial": -0.03,
        "C_limits":  [-0.07, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "26"): {
        "B_initial": -0.1,
        "B_limits":  [-0.2, 0],
        "C_initial": -0.03,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "27"): {
        "B_initial": -0.155,
        "B_limits":  [-0.22, -0.1],
        "C_initial": -0.015,
        "C_limits":  [-0.05, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "28"): {
        "B_initial": -0.16,
        "B_limits":  [-0.3, -0.03],
        "C_initial": 0.01,
        "C_limits":  [-0.05, 0.035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "29"): {
        "B_initial": -0.24,
        "B_limits":  [-0.35, -0.2],
        "C_initial": 0.06,
        "C_limits":  [-0.03, 0.08],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "31"): {
        "B_initial": -0.1,
        "B_limits":  [-0.15, 0],
        "C_initial": -0.057,
        "C_limits":  [-0.07, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "32"): {
        "B_initial": -0.1,
        "B_limits":  [-0.2, 0],
        "C_initial": -0.03,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "33"): {
        "B_initial": -0.145,
        "B_limits":  [-0.22, -0.1],
        "C_initial": -0.007,
        "C_limits":  [-0.05, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "34"): {
        "B_initial": -0.18,
        "B_limits":  [-0.3, -0.03],
        "C_initial": 0.022,
        "C_limits":  [-0.05, 0.035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "All"): {
        "B_initial": -0.08526,
        "B_limits":  [-0.14, -0.03],
        "C_initial": -0.003224,
        "C_limits":  [-0.02, 0.04],
        "Allow_Multiple_Fits":   False,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "2"): {
        "B_initial": -0.11,
        "B_limits":  [0, -0.16],
        "C_initial": -0.06,
        "C_limits":  [0, -0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": False
    },
    ("6", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "4"): {
        "B_initial": -0.2,
        "B_limits":  [-0.1, -0.3],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "5"): {
        "B_initial": -0.21,
        "B_limits":  [-0.3, -0.15],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "6"): {
        "B_initial": -0.26,
        "B_limits":  [-0.3, -0.2],
        "C_initial": 0.02,
        "C_limits":  [0.005, 0.04],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "12"): {
        "B_initial": -0.4,
        "B_limits":  [-0.2, -0.45],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "15"): {
        "B_initial": -0.1,
        "B_limits":  [-0.05, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "21"): {
        "B_initial": -0.11,
        "B_limits":  [-0.17, -0.06],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "All"): {
        "B_initial": -0.08085,
        "B_limits":  [-0.1, -0.05],
        "C_initial": -0.007986,
        "C_limits":  [-0.025, 0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "3"): {
        "B_initial": -0.1,
        "B_limits":  [-0.16, -0.05],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "4"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "5"): {
        "B_initial": -0.275,
        "B_limits":  [-0.2, -0.4],
        "C_initial": -0.004896,
        "C_limits":  [0.06, -0.06],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "12"): {
        "B_initial": -0.3,
        "B_limits":  [-0.2, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "17"): {
        "B_initial": -0.2,
        "B_limits":  [-0.23, -0.15],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "18"): {
        "B_initial": -0.3,
        "B_limits":  [-0.2, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "23"): {
        "B_initial": -0.2,
        "B_limits":  [-0.23, -0.15],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "24"): {
        "B_initial": -0.4,
        "B_limits":  [-0.2, -0.45],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "29"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": 0,
        "C_limits":  [-0.1, 0.04],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "31"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "32"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "33"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "34"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "35"): {
        "B_initial": -0.15,
        "B_limits":  [-0.1, -0.2],
        "C_initial": 0,
        "C_limits":  [-0.1, 0.04],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "All"): {
        "B_initial": -0.09391,
        "B_limits":  [-0.12, -0.06],
        "C_initial": -0.03207,
        "C_limits":  [-0.05, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "2"): {
        "B_initial": -0.05,
        "B_limits":  [-0.15, 0],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "4"): {
        "B_initial": -0.2,
        "B_limits":  [-0.29, -0.1],
        "C_initial": 0,
        "C_limits":  [-0.1, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "5"): {
        "B_initial": -0.3,
        "B_limits":  [-0.2, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "6"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "9"): {
        "B_initial": -0.15,
        "B_limits":  [-0.1, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "10"): {
        "B_initial": -0.17,
        "B_limits":  [-0.27, -0.15],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "12"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "14"): {
        "B_initial": -0.13,
        "B_limits":  [-0.2, -0.02],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "18"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "21"): {
        "B_initial": 0.05,
        "B_limits":  [0, 0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "24"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "28"): {
        "B_initial": -0.01,
        "B_limits":  [-0.08, 0],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "29"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "30"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": -0.02,
        "C_limits":  [-0.1, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "31"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "32"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "33"): {
        "B_initial": -0.03629,
        "B_limits":  [-0.4, 0.1],
        "C_initial": -0.03558,
        "C_limits":  [-0.2, 0.2],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "34"): {
        "B_initial": -0.1725,
        "B_limits":  [-0.4, 0.1],
        "C_initial": 0.01992,
        "C_limits":  [-0.2, 0.2],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "All"): {
        "B_initial": -0.09686,
        "B_limits":  [-0.12, -0.065],
        "C_initial": -0.001806,
        "C_limits":  [-0.05, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "4"): {
        "B_initial": -0.15,
        "B_limits":  [-0.25, -0.1],
        "C_initial": 0.04,
        "C_limits":  [-0.06, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "5"): {
        "B_initial": -0.2,
        "B_limits":  [-0.15, -0.35],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "6"): {
        "B_initial": -0.28,
        "B_limits":  [-0.2, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "7"): {
        "B_initial": -0.3,
        "B_limits":  [-0.4, -0.19],
        "C_initial": 0.02,
        "C_limits":  [0.01, 0.04],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "11"): {
        "B_initial": -0.175,
        "B_limits":  [-0.1, -0.3],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "12"): {
        "B_initial": -0.19,
        "B_limits":  [-0.3, -0.126],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "13"): {
        "B_initial": -0.24,
        "B_limits":  [-0.4, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "14"): {
        "B_initial": -0.5,
        "B_limits":  [-0.4, -0.6],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "18"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "20"): {
        "B_initial": -0.31,
        "B_limits":  [-0.2, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "24"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "26"): {
        "B_initial": -0.21,
        "B_limits":  [-0.1, -0.3],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "29"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "30"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "31"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "32"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "All"): {
        "B_initial": -0.09074,
        "B_limits":  [-0.1, -0.05],
        "C_initial": -0.02087,
        "C_limits":  [-0.05, -0.005],
        "Allow_Multiple_Fits":   False,
        "Allow_Multiple_Fits_C": False
    },
    ("10", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "4"): {
        "B_initial": -0.2,
        "B_limits":  [-0.4, -0.1],
        "C_initial": 0,
        "C_limits":  [-0.008, 0.07],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "5"): {
        "B_initial": -0.3,
        "B_limits":  [-0.4, -0.2],
        "C_initial": 0.002,
        "C_limits":  [-0.008, 0.09],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "6"): {
        "B_initial": -0.275,
        "B_limits":  [-0.4, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "12"): {
        "B_initial": -0.275,
        "B_limits":  [-0.4, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "18"): {
        "B_initial": -0.275,
        "B_limits":  [-0.4, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "29"): {
        "B_initial": -0.2675,
        "B_limits":  [-0.4, -0.2],
        "C_initial": 0.012,
        "C_limits":  [-0.025, 0.04],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "31"): {
        "B_initial": 0,
        "B_limits":  [-0.03, 0.01],
        "C_initial": 0,
        "C_limits":  [-0.01, 0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "32"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "33"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "34"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "All"): {
        "B_initial": -0.08114,
        "B_limits":  [-0.11, -0.05],
        "C_initial": -0.02216,
        "C_limits":  [-0.05, -0.005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "4"): {
        "B_initial": -0.2,
        "B_limits":  [-0.15, -0.3],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "5"): {
        "B_initial": -0.2,
        "B_limits":  [-0.25, -0.1],
        "C_initial": -0.03,
        "C_limits":  [-0.005, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "6"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "10"): {
        "B_initial": -0.2929,
        "B_limits":  [-0.26, -0.34],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "12"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "15"): {
        "B_initial": -0.2,
        "B_limits":  [-0.1, -0.3],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "18"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": -0.03,
        "C_limits":  [-0.1, -0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "20"): {
        "B_initial": -0.26,
        "B_limits":  [-0.32, -0.23],
        "C_initial": 0.01,
        "C_limits":  [-0.01, 0.03],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "24"): {
        "B_initial": -0.13,
        "B_limits":  [-0.2, -0.1],
        "C_initial": 0,
        "C_limits":  [-0.02, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "All"): {
        "B_initial": -0.05476,
        "B_limits":  [-0.075, -0.025],
        "C_initial": -0.04945,
        "C_limits":  [-0.07, -0.03],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "4"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "6"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "12"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "15"): {
        "B_initial": -0.16,
        "B_limits":  [-0.25, -0.1],
        "C_initial": -0.14,
        "C_limits":  [-0.18, -0.05],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "18"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "20"): {
        "B_initial": -0.1,
        "B_limits":  [-0.2, -0.05],
        "C_initial": -0.17,
        "C_limits":  [-0.1, -0.24],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "24"): {
        "B_initial": 0,
        "B_limits":  [-0.05, 0.03],
        "C_initial": -0.035,
        "C_limits":  [-0.1, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "All"): {
        "B_initial": -0.09028,
        "B_limits":  [-0.13, -0.06],
        "C_initial": -0.01376,
        "C_limits":  [-0.04, -0.005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "4"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "5"): {
        "B_initial": -0.25,
        "B_limits":  [-0.18, -0.35],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "6"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "12"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "15"): {
        "B_initial": -0.21,
        "B_limits":  [-0.3, -0.1],
        "C_initial": 0.01,
        "C_limits":  [-0.001, 0.07],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "18"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "23"): {
        "B_initial": -0.1,
        "B_limits":  [-0.2, -0.04],
        "C_initial": -0.01,
        "C_limits":  [-0.02, 0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "24"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "All"): {
        "B_initial": -0.08461,
        "B_limits":  [-0.12, -0.06],
        "C_initial": -0.02939,
        "C_limits":  [-0.05, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "2"): {
        "B_initial": -0.1,
        "B_limits":  [-0.12, -0.02],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "3"): {
        "B_initial": -0.15,
        "B_limits":  [-0.25, -0.1],
        "C_initial": -0.056,
        "C_limits":  [-0.1, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "4"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "5"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "6"): {
        "B_initial": -0.4,
        "B_limits":  [-0.35, -0.5],
        "C_initial": 0.05,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "10"): {
        "B_initial": -0.15,
        "B_limits":  [-0.2, -0.05],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "11"): {
        "B_initial": -0.22,
        "B_limits":  [-0.175, -0.4],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "12"): {
        "B_initial": -0.27,
        "B_limits":  [-0.3, -0.2],
        "C_initial": 0.05,
        "C_limits":  [-0.08, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "18"): {
        "B_initial": -0.4,
        "B_limits":  [-0.2, -0.5],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "20"): {
        "B_initial": -0.02,
        "B_limits":  [-0.06, 0],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "21"): {
        "B_initial": -0.128,
        "B_limits":  [-0.165, -0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "22"): {
        "B_initial": -0.15,
        "B_limits":  [-0.3, -0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "23"): {
        "B_initial": -0.2,
        "B_limits":  [-0.3, -0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "29"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "31"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "32"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "33"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "34"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "All"): {
        "B_initial": -0.07801,
        "B_limits":  [-0.1, -0.05],
        "C_initial": -0.03144,
        "C_limits":  [-0.07, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "3"): {
        "B_initial": -0.127,
        "B_limits":  [-0.05, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "4"): {
        "B_initial": -0.1,
        "B_limits":  [-0.3, -0.05],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "6"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "9"): {
        "B_initial": -0.08,
        "B_limits":  [-0.18, -0.01],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "12"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "15"): {
        "B_initial": -0.2,
        "B_limits":  [-0.4, -0.15],
        "C_initial": -0.1,
        "C_limits":  [-0.2, -0.05],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "18"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "19"): {
        "B_initial": -0.1,
        "B_limits":  [0, -0.25],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "21"): {
        "B_initial": 0,
        "B_limits":  [-0.04, 0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "23"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "24"): {
        "B_initial": -0.19,
        "B_limits":  [-0.22, -0.14],
        "C_initial": 0,
        "C_limits":  [-0.02, 0.013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "All"): {
        "B_initial": -0.08305,
        "B_limits":  [-0.12, -0.05],
        "C_initial": -0.03288,
        "C_limits":  [-0.05, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "2"): {
        "B_initial": -0.1,
        "B_limits":  [-0.025, -0.2],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "4"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "5"): {
        "B_initial": -0.2,
        "B_limits":  [-0.4, -0.15],
        "C_initial": 0,
        "C_limits":  [-0.06, 0.04],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "6"): {
        "B_initial": -0.3684,
        "B_limits":  [-0.16, -0.38],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "12"): {
        "B_initial": -0.3,
        "B_limits":  [-0.4, -0.2],
        "C_initial": 0.02,
        "C_limits":  [-0.1, 0.04],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "17"): {
        "B_initial": -0.1,
        "B_limits":  [-0.25, -0.05],
        "C_initial": 0.01,
        "C_limits":  [-0.06, 0.04],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "25"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "27"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "All"): {
        "B_initial": -0.07127,
        "B_limits":  [-0.1, -0.05],
        "C_initial": -0.0188,
        "C_limits":  [-0.04, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "1"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "2"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "3"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "4"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "5"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "6"): {
        "B_initial": -0.24,
        "B_limits":  [-0.19, -0.3],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "7"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "8"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "9"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "10"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "11"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "12"): {
        "B_initial": -0.1335,
        "B_limits":  [-0.05, -0.25],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "13"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "14"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "15"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "16"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "17"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "18"): {
        "B_initial": -0.25,
        "B_limits":  [-0.15, -0.3],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "19"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "20"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "21"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "22"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "23"): {
        "B_initial": -0.15,
        "B_limits":  [-0.2, -0.1],
        "C_initial": -0.03,
        "C_limits":  [-0.05, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "25"): {
        "B_initial": 0,
        "B_limits":  [-0.04, 0.1],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "26"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "27"): {
        "B_initial": -0.06804,
        "B_limits":  [-0.01, -0.18],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "28"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "3", "RC"): {
        "B_initial": -0.1185,
        "B_limits":  [-0.129, -0.09],
        "C_initial": 0.03,
        "C_limits":  [0.01, 0.02],
        "Allow_Multiple_Fits":   False,
        "Allow_Multiple_Fits_C": False
    },
    ("5", "5", "RC"): {
        "B_initial": -0.3,
        "B_limits":  [-0.35, -0.2],
        "C_initial": 0.01,
        "C_limits":  [0, 0.08],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "8", "RC"): {
        "B_initial": -0.057,
        "B_limits":  [-0.2, 0],
        "C_initial": 0.035,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "14", "RC"): {
        "B_initial": -0.032,
        "B_limits":  [-0.055, 0],
        "C_initial": 0,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "20", "RC"): {
        "B_initial": -0.025,
        "B_limits":  [-0.05, 0],
        "C_initial": 0,
        "C_limits":  [-0.05, 0.005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "26", "RC"): {
        "B_initial": -0.026,
        "B_limits":  [-0.05, 0],
        "C_initial": -0.03,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "32", "RC"): {
        "B_initial": -0.03,
        "B_limits":  [-0.058, 0],
        "C_initial": -0.03,
        "C_limits":  [-0.05, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "5", "RC"): {
        "B_initial": None,
        "B_limits":  [None, None],
        "C_initial": 0.02,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "6", "RC"): {
        "B_initial": -0.3,
        "B_limits":  [-0.4, -0.15],
        "C_initial": None,
        "C_limits":  [None, None],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "8", "BC"): {
        "B_initial": 0.02,
        "B_limits":  [-0.03, 0.05],
        "C_initial": 0.05767,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "9", "BC"): {
        "B_initial": -0.038,
        "B_limits":  [-0.02, 0],
        "C_initial": 0.05967,
        "C_limits":  [0, 0.1],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "24", "BC"): {
        "B_initial": -0.05,
        "B_limits":  [-0.08, 0.02],
        "C_initial": -0.035,
        "C_limits":  [-0.1, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "24", "BC"): {
        "B_initial": -0.2,
        "B_limits":  [-0.3, -0.1],
        "C_initial": 0,
        "C_limits":  [-0.02, 0.013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "1", "3D"): {
        "B_initial": -0.07274,
        "B_limits":  [-0.0899, -0.0556],
        "C_initial": -0.01165,
        "C_limits":  [-0.0214, -0.0019],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "2", "3D"): {
        "B_initial": -0.11735,
        "B_limits":  [-0.1331, -0.1016],
        "C_initial": 0.00738,
        "C_limits":  [0.0032, 0.0116],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "3", "3D"): {
        "B_initial": -0.15587,
        "B_limits":  [-0.1695, -0.1422],
        "C_initial": 0.00568,
        "C_limits":  [0.0018, 0.0096],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "4", "3D"): {
        "B_initial": -0.19839,
        "B_limits":  [-0.209, -0.1878],
        "C_initial": 0.00083,
        "C_limits":  [-0.0042, 0.0059],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "5", "3D"): {
        "B_initial": -0.24928,
        "B_limits":  [-0.2576, -0.2409],
        "C_initial": 0.00052,
        "C_limits":  [-0.0078, 0.0088],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "6", "3D"): {
        "B_initial": -0.31656,
        "B_limits":  [-0.3272, -0.3059],
        "C_initial": 0.01416,
        "C_limits":  [0.0002, 0.0281],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "7", "3D"): {
        "B_initial": -0.4678,
        "B_limits":  [-0.5011, -0.4345],
        "C_initial": 0.08475,
        "C_limits":  [0.0567, 0.1128],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "8", "3D"): {
        "B_initial": -0.00157,
        "B_limits":  [-0.0081, 0.005],
        "C_initial": 0.00472,
        "C_limits":  [0.003, 0.0064],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "9", "3D"): {
        "B_initial": -0.05016,
        "B_limits":  [-0.056, -0.0443],
        "C_initial": -0.00028,
        "C_limits":  [-0.0026, 0.0021],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "10", "3D"): {
        "B_initial": -0.10082,
        "B_limits":  [-0.1078, -0.0939],
        "C_initial": -0.00134,
        "C_limits":  [-0.0033, 0.0007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "11", "3D"): {
        "B_initial": -0.16198,
        "B_limits":  [-0.1702, -0.1538],
        "C_initial": 0.00717,
        "C_limits":  [0.005, 0.0094],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "12", "3D"): {
        "B_initial": -0.2385,
        "B_limits":  [-0.2493, -0.2277],
        "C_initial": 0.03202,
        "C_limits":  [0.0271, 0.0369],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "13", "3D"): {
        "B_initial": -0.33919,
        "B_limits":  [-0.3538, -0.3246],
        "C_initial": 0.08173,
        "C_limits":  [0.0724, 0.0911],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "14", "3D"): {
        "B_initial": -0.54891,
        "B_limits":  [-0.5879, -0.51],
        "C_initial": 0.21295,
        "C_limits":  [0.1862, 0.2397],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "15", "3D"): {
        "B_initial": 0.00229,
        "B_limits":  [-0.0046, 0.0092],
        "C_initial": 0.00023,
        "C_limits":  [-0.0023, 0.0028],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "16", "3D"): {
        "B_initial": -0.04999,
        "B_limits":  [-0.0563, -0.0437],
        "C_initial": -0.01151,
        "C_limits":  [-0.0129, -0.0102],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "17", "3D"): {
        "B_initial": -0.10581,
        "B_limits":  [-0.1136, -0.098],
        "C_initial": -0.00918,
        "C_limits":  [-0.0109, -0.0075],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "18", "3D"): {
        "B_initial": -0.17366,
        "B_limits":  [-0.183, -0.1643],
        "C_initial": 0.00833,
        "C_limits":  [0.0048, 0.0119],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "19", "3D"): {
        "B_initial": -0.25843,
        "B_limits":  [-0.2706, -0.2462],
        "C_initial": 0.04741,
        "C_limits":  [0.0406, 0.0542],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "20", "3D"): {
        "B_initial": -0.3689,
        "B_limits":  [-0.3848, -0.353],
        "C_initial": 0.11615,
        "C_limits":  [0.105, 0.1273],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "22", "3D"): {
        "B_initial": -0.00653,
        "B_limits":  [-0.0142, 0.0012],
        "C_initial": -0.00029,
        "C_limits":  [-0.0036, 0.003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "23", "3D"): {
        "B_initial": -0.06238,
        "B_limits":  [-0.0693, -0.0555],
        "C_initial": -0.01479,
        "C_limits":  [-0.0159, -0.0137],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "24", "3D"): {
        "B_initial": -0.12185,
        "B_limits":  [-0.1302, -0.1135],
        "C_initial": -0.00957,
        "C_limits":  [-0.0117, -0.0075],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "25", "3D"): {
        "B_initial": -0.19388,
        "B_limits":  [-0.2038, -0.1839],
        "C_initial": 0.01408,
        "C_limits":  [0.0096, 0.0185],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "26", "3D"): {
        "B_initial": -0.28332,
        "B_limits":  [-0.2961, -0.2705],
        "C_initial": 0.06232,
        "C_limits":  [0.0543, 0.0703],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "29", "3D"): {
        "B_initial": -0.01812,
        "B_limits":  [-0.0265, -0.0097],
        "C_initial": 0.0011,
        "C_limits":  [-0.0027, 0.0049],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "30", "3D"): {
        "B_initial": -0.07721,
        "B_limits":  [-0.0845, -0.0699],
        "C_initial": -0.01476,
        "C_limits":  [-0.0157, -0.0138],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "31", "3D"): {
        "B_initial": -0.13957,
        "B_limits":  [-0.1483, -0.1308],
        "C_initial": -0.00714,
        "C_limits":  [-0.0096, -0.0047],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "32", "3D"): {
        "B_initial": -0.2147,
        "B_limits":  [-0.225, -0.2044],
        "C_initial": 0.02114,
        "C_limits":  [0.0161, 0.0262],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "1", "3D"): {
        "B_initial": -0.0823,
        "B_limits":  [-0.0954, -0.0692],
        "C_initial": -0.0123,
        "C_limits":  [-0.0238, -0.0008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "2", "3D"): {
        "B_initial": -0.1412,
        "B_limits":  [-0.1522, -0.1302],
        "C_initial": 0.01535,
        "C_limits":  [0.011, 0.0197],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "3", "3D"): {
        "B_initial": -0.18488,
        "B_limits":  [-0.1948, -0.1749],
        "C_initial": 0.01506,
        "C_limits":  [0.0112, 0.0189],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "4", "3D"): {
        "B_initial": -0.22796,
        "B_limits":  [-0.2361, -0.2198],
        "C_initial": 0.01151,
        "C_limits":  [0.0071, 0.0159],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "5", "3D"): {
        "B_initial": -0.28142,
        "B_limits":  [-0.2908, -0.272],
        "C_initial": 0.0126,
        "C_limits":  [0.0062, 0.019],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "6", "3D"): {
        "B_initial": -0.40134,
        "B_limits":  [-0.4263, -0.3764],
        "C_initial": 0.05592,
        "C_limits":  [0.0395, 0.0723],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "7", "3D"): {
        "B_initial": -0.02873,
        "B_limits":  [-0.0368, -0.0207],
        "C_initial": 0.00889,
        "C_limits":  [0.0066, 0.0112],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "8", "3D"): {
        "B_initial": -0.08285,
        "B_limits":  [-0.0898, -0.0759],
        "C_initial": 0.00911,
        "C_limits":  [0.0061, 0.0121],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "9", "3D"): {
        "B_initial": -0.13326,
        "B_limits":  [-0.1409, -0.1256],
        "C_initial": 0.00665,
        "C_limits":  [0.0039, 0.0094],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "10", "3D"): {
        "B_initial": -0.18876,
        "B_limits":  [-0.1964, -0.1811],
        "C_initial": 0.01021,
        "C_limits":  [0.0081, 0.0123],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "11", "3D"): {
        "B_initial": -0.26368,
        "B_limits":  [-0.2755, -0.2518],
        "C_initial": 0.02916,
        "C_limits":  [0.025, 0.0333],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "12", "3D"): {
        "B_initial": -0.43503,
        "B_limits":  [-0.4665, -0.4035],
        "C_initial": 0.11642,
        "C_limits":  [0.097, 0.1358],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "13", "3D"): {
        "B_initial": -0.01438,
        "B_limits":  [-0.021, -0.0078],
        "C_initial": 0.00136,
        "C_limits":  [-0.0009, 0.0036],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "14", "3D"): {
        "B_initial": -0.06533,
        "B_limits":  [-0.0711, -0.0596],
        "C_initial": -0.00904,
        "C_limits":  [-0.0111, -0.007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "15", "3D"): {
        "B_initial": -0.11757,
        "B_limits":  [-0.1247, -0.1104],
        "C_initial": -0.00897,
        "C_limits":  [-0.0109, -0.0071],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "16", "3D"): {
        "B_initial": -0.17716,
        "B_limits":  [-0.1847, -0.1696],
        "C_initial": 0.00229,
        "C_limits":  [-0.0003, 0.0049],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "17", "3D"): {
        "B_initial": -0.25951,
        "B_limits":  [-0.2724, -0.2467],
        "C_initial": 0.03552,
        "C_limits":  [0.029, 0.042],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "18", "3D"): {
        "B_initial": -0.44866,
        "B_limits":  [-0.4833, -0.414],
        "C_initial": 0.15415,
        "C_limits":  [0.1299, 0.1784],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "19", "3D"): {
        "B_initial": -0.01672,
        "B_limits":  [-0.0232, -0.0102],
        "C_initial": -0.00316,
        "C_limits":  [-0.0065, 0.0002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "20", "3D"): {
        "B_initial": -0.06685,
        "B_limits":  [-0.0728, -0.0609],
        "C_initial": -0.01835,
        "C_limits":  [-0.0198, -0.0169],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "21", "3D"): {
        "B_initial": -0.12046,
        "B_limits":  [-0.1279, -0.1131],
        "C_initial": -0.01524,
        "C_limits":  [-0.0172, -0.0133],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "22", "3D"): {
        "B_initial": -0.18244,
        "B_limits":  [-0.1904, -0.1745],
        "C_initial": 0.00227,
        "C_limits":  [-0.0011, 0.0057],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "23", "3D"): {
        "B_initial": -0.26871,
        "B_limits":  [-0.2823, -0.2551],
        "C_initial": 0.04606,
        "C_limits":  [0.0378, 0.0543],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "25", "3D"): {
        "B_initial": -0.02416,
        "B_limits":  [-0.0308, -0.0176],
        "C_initial": -0.00469,
        "C_limits":  [-0.0088, -0.0006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "26", "3D"): {
        "B_initial": -0.07453,
        "B_limits":  [-0.0806, -0.0685],
        "C_initial": -0.02217,
        "C_limits":  [-0.0234, -0.021],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "27", "3D"): {
        "B_initial": -0.1293,
        "B_limits":  [-0.1369, -0.1217],
        "C_initial": -0.01644,
        "C_limits":  [-0.0187, -0.0142],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "28", "3D"): {
        "B_initial": -0.19292,
        "B_limits":  [-0.2011, -0.1847],
        "C_initial": 0.00577,
        "C_limits":  [0.0017, 0.0098],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "29", "3D"): {
        "B_initial": -0.28159,
        "B_limits":  [-0.2956, -0.2676],
        "C_initial": 0.05715,
        "C_limits":  [0.0478, 0.0665],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "31", "3D"): {
        "B_initial": -0.03563,
        "B_limits":  [-0.0426, -0.0286],
        "C_initial": -0.00423,
        "C_limits":  [-0.009, 0.0005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "32", "3D"): {
        "B_initial": -0.08691,
        "B_limits":  [-0.0933, -0.0805],
        "C_initial": -0.02299,
        "C_limits":  [-0.024, -0.0219],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "33", "3D"): {
        "B_initial": -0.14296,
        "B_limits":  [-0.151, -0.1349],
        "C_initial": -0.01453,
        "C_limits":  [-0.0172, -0.0119],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "34", "3D"): {
        "B_initial": -0.20812,
        "B_limits":  [-0.2168, -0.1994],
        "C_initial": 0.01217,
        "C_limits":  [0.0075, 0.0169],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "1", "3D"): {
        "B_initial": -0.07208,
        "B_limits":  [-0.0815, -0.0627],
        "C_initial": -0.0061,
        "C_limits":  [-0.0148, 0.0026],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "2", "3D"): {
        "B_initial": -0.13145,
        "B_limits":  [-0.1405, -0.1224],
        "C_initial": 0.02475,
        "C_limits":  [0.0219, 0.0276],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "3", "3D"): {
        "B_initial": -0.18249,
        "B_limits":  [-0.1918, -0.1732],
        "C_initial": 0.03161,
        "C_limits":  [0.0295, 0.0337],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "4", "3D"): {
        "B_initial": -0.23528,
        "B_limits":  [-0.2453, -0.2253],
        "C_initial": 0.03194,
        "C_limits":  [0.0295, 0.0344],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "5", "3D"): {
        "B_initial": -0.29136,
        "B_limits":  [-0.3015, -0.2812],
        "C_initial": 0.03232,
        "C_limits":  [0.0296, 0.035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "6", "3D"): {
        "B_initial": -0.36926,
        "B_limits":  [-0.3839, -0.3546],
        "C_initial": 0.04597,
        "C_limits":  [0.0411, 0.0508],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "7", "3D"): {
        "B_initial": -0.03581,
        "B_limits":  [-0.0425, -0.0291],
        "C_initial": 0.00969,
        "C_limits":  [0.0071, 0.0123],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "8", "3D"): {
        "B_initial": -0.08066,
        "B_limits":  [-0.0887, -0.0726],
        "C_initial": 0.0132,
        "C_limits":  [0.0094, 0.017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "9", "3D"): {
        "B_initial": -0.12754,
        "B_limits":  [-0.1365, -0.1186],
        "C_initial": 0.00989,
        "C_limits":  [0.0053, 0.0145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "10", "3D"): {
        "B_initial": -0.18201,
        "B_limits":  [-0.1923, -0.1718],
        "C_initial": 0.00848,
        "C_limits":  [0.0041, 0.0129],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "11", "3D"): {
        "B_initial": -0.24556,
        "B_limits":  [-0.2563, -0.2349],
        "C_initial": 0.01454,
        "C_limits":  [0.0109, 0.0182],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "12", "3D"): {
        "B_initial": -0.34259,
        "B_limits":  [-0.3595, -0.3257],
        "C_initial": 0.04564,
        "C_limits":  [0.0387, 0.0526],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "13", "3D"): {
        "B_initial": -0.01914,
        "B_limits":  [-0.0228, -0.0155],
        "C_initial": 0.00273,
        "C_limits":  [0.0005, 0.005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "14", "3D"): {
        "B_initial": -0.05227,
        "B_limits":  [-0.0572, -0.0474],
        "C_initial": -0.01009,
        "C_limits":  [-0.0128, -0.0074],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "15", "3D"): {
        "B_initial": -0.09432,
        "B_limits":  [-0.1002, -0.0885],
        "C_initial": -0.01707,
        "C_limits":  [-0.0199, -0.0143],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "16", "3D"): {
        "B_initial": -0.14747,
        "B_limits":  [-0.1552, -0.1398],
        "C_initial": -0.01536,
        "C_limits":  [-0.0182, -0.0126],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "17", "3D"): {
        "B_initial": -0.21307,
        "B_limits":  [-0.2219, -0.2042],
        "C_initial": -0.00016,
        "C_limits":  [-0.0039, 0.0036],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "18", "3D"): {
        "B_initial": -0.3183,
        "B_limits":  [-0.3358, -0.3008],
        "C_initial": 0.05053,
        "C_limits":  [0.0401, 0.061],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "19", "3D"): {
        "B_initial": -0.02116,
        "B_limits":  [-0.0241, -0.0182],
        "C_initial": -0.00171,
        "C_limits":  [-0.0051, 0.0017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "20", "3D"): {
        "B_initial": -0.04863,
        "B_limits":  [-0.0529, -0.0443],
        "C_initial": -0.02153,
        "C_limits":  [-0.0237, -0.0193],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "21", "3D"): {
        "B_initial": -0.08815,
        "B_limits":  [-0.0936, -0.0827],
        "C_initial": -0.02864,
        "C_limits":  [-0.0306, -0.0267],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "22", "3D"): {
        "B_initial": -0.1403,
        "B_limits":  [-0.1478, -0.1328],
        "C_initial": -0.02313,
        "C_limits":  [-0.0258, -0.0204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "23", "3D"): {
        "B_initial": -0.2063,
        "B_limits":  [-0.2152, -0.1974],
        "C_initial": -0.00062,
        "C_limits":  [-0.0053, 0.004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "24", "3D"): {
        "B_initial": -0.31435,
        "B_limits":  [-0.3324, -0.2963],
        "C_initial": 0.06384,
        "C_limits":  [0.0511, 0.0766],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "25", "3D"): {
        "B_initial": -0.03267,
        "B_limits":  [-0.036, -0.0294],
        "C_initial": -0.00235,
        "C_limits":  [-0.0067, 0.002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "26", "3D"): {
        "B_initial": -0.05659,
        "B_limits":  [-0.061, -0.0522],
        "C_initial": -0.02646,
        "C_limits":  [-0.0284, -0.0245],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "27", "3D"): {
        "B_initial": -0.09456,
        "B_limits":  [-0.1002, -0.0889],
        "C_initial": -0.03244,
        "C_limits":  [-0.034, -0.0308],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "28", "3D"): {
        "B_initial": -0.1461,
        "B_limits":  [-0.1539, -0.1383],
        "C_initial": -0.02251,
        "C_limits":  [-0.0257, -0.0194],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "29", "3D"): {
        "B_initial": -0.21236,
        "B_limits":  [-0.2217, -0.203],
        "C_initial": 0.00736,
        "C_limits":  [0.0016, 0.0131],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "1", "3D"): {
        "B_initial": -0.07728,
        "B_limits":  [-0.0876, -0.067],
        "C_initial": 0.00472,
        "C_limits":  [-0.0016, 0.0111],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "2", "3D"): {
        "B_initial": -0.14656,
        "B_limits":  [-0.1556, -0.1375],
        "C_initial": 0.03026,
        "C_limits":  [0.0282, 0.0323],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "3", "3D"): {
        "B_initial": -0.20702,
        "B_limits":  [-0.2173, -0.1967],
        "C_initial": 0.03611,
        "C_limits":  [0.0333, 0.0389],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "4", "3D"): {
        "B_initial": -0.2736,
        "B_limits":  [-0.2856, -0.2616],
        "C_initial": 0.03731,
        "C_limits":  [0.0337, 0.0409],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "5", "3D"): {
        "B_initial": -0.35416,
        "B_limits":  [-0.3689, -0.3394],
        "C_initial": 0.04032,
        "C_limits":  [0.0364, 0.0443],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "7", "3D"): {
        "B_initial": -0.0544,
        "B_limits":  [-0.062, -0.0468],
        "C_initial": 0.0118,
        "C_limits":  [0.0093, 0.0143],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "8", "3D"): {
        "B_initial": -0.10827,
        "B_limits":  [-0.116, -0.1006],
        "C_initial": 0.01714,
        "C_limits":  [0.0141, 0.0202],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "9", "3D"): {
        "B_initial": -0.16144,
        "B_limits":  [-0.1706, -0.1523],
        "C_initial": 0.0137,
        "C_limits":  [0.0096, 0.0178],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "10", "3D"): {
        "B_initial": -0.22419,
        "B_limits":  [-0.2351, -0.2133],
        "C_initial": 0.01001,
        "C_limits":  [0.0054, 0.0146],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "11", "3D"): {
        "B_initial": -0.30539,
        "B_limits":  [-0.3193, -0.2915],
        "C_initial": 0.01311,
        "C_limits":  [0.0083, 0.0179],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "12", "3D"): {
        "B_initial": -0.44428,
        "B_limits":  [-0.4685, -0.4201],
        "C_initial": 0.0548,
        "C_limits":  [0.044, 0.0656],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "13", "3D"): {
        "B_initial": -0.03651,
        "B_limits":  [-0.0417, -0.0314],
        "C_initial": 0.00689,
        "C_limits":  [0.005, 0.0088],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "14", "3D"): {
        "B_initial": -0.07711,
        "B_limits":  [-0.0832, -0.0711],
        "C_initial": -0.00144,
        "C_limits":  [-0.0048, 0.0019],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "15", "3D"): {
        "B_initial": -0.12324,
        "B_limits":  [-0.1307, -0.1157],
        "C_initial": -0.01008,
        "C_limits":  [-0.0142, -0.0059],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "16", "3D"): {
        "B_initial": -0.18128,
        "B_limits":  [-0.1906, -0.172],
        "C_initial": -0.01513,
        "C_limits":  [-0.0197, -0.0106],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "17", "3D"): {
        "B_initial": -0.26054,
        "B_limits":  [-0.2732, -0.2479],
        "C_initial": -0.0088,
        "C_limits":  [-0.014, -0.0036],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "18", "3D"): {
        "B_initial": -0.4045,
        "B_limits":  [-0.4291, -0.3799],
        "C_initial": 0.04563,
        "C_limits":  [0.0323, 0.059],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "19", "3D"): {
        "B_initial": -0.02666,
        "B_limits":  [-0.03, -0.0233],
        "C_initial": 0.0011,
        "C_limits":  [-0.0018, 0.004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "20", "3D"): {
        "B_initial": -0.05722,
        "B_limits":  [-0.062, -0.0525],
        "C_initial": -0.01606,
        "C_limits":  [-0.0193, -0.0128],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "21", "3D"): {
        "B_initial": -0.09776,
        "B_limits":  [-0.104, -0.0915],
        "C_initial": -0.02732,
        "C_limits":  [-0.0311, -0.0236],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "22", "3D"): {
        "B_initial": -0.15171,
        "B_limits":  [-0.1598, -0.1436],
        "C_initial": -0.03191,
        "C_limits":  [-0.0361, -0.0277],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "23", "3D"): {
        "B_initial": -0.22856,
        "B_limits":  [-0.2403, -0.2168],
        "C_initial": -0.02127,
        "C_limits":  [-0.0268, -0.0157],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "24", "3D"): {
        "B_initial": -0.37423,
        "B_limits":  [-0.3991, -0.3493],
        "C_initial": 0.0455,
        "C_limits":  [0.0299, 0.0611],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "25", "3D"): {
        "B_initial": -0.02301,
        "B_limits":  [-0.0253, -0.0207],
        "C_initial": -0.00307,
        "C_limits":  [-0.007, 0.0009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "26", "3D"): {
        "B_initial": -0.04559,
        "B_limits":  [-0.0497, -0.0414],
        "C_initial": -0.02639,
        "C_limits":  [-0.0296, -0.0232],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "27", "3D"): {
        "B_initial": -0.08155,
        "B_limits":  [-0.0873, -0.0758],
        "C_initial": -0.03882,
        "C_limits":  [-0.0423, -0.0353],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "28", "3D"): {
        "B_initial": -0.13198,
        "B_limits":  [-0.1397, -0.1242],
        "C_initial": -0.04193,
        "C_limits":  [-0.046, -0.0379],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "29", "3D"): {
        "B_initial": -0.20641,
        "B_limits":  [-0.218, -0.1948],
        "C_initial": -0.02643,
        "C_limits":  [-0.0324, -0.0204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "31", "3D"): {
        "B_initial": -0.02629,
        "B_limits":  [-0.0286, -0.024],
        "C_initial": -0.005,
        "C_limits":  [-0.0101, 0.0001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "32", "3D"): {
        "B_initial": -0.04026,
        "B_limits":  [-0.0442, -0.0363],
        "C_initial": -0.03404,
        "C_limits":  [-0.037, -0.0311],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "33", "3D"): {
        "B_initial": -0.07113,
        "B_limits":  [-0.0769, -0.0654],
        "C_initial": -0.04658,
        "C_limits":  [-0.0496, -0.0436],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "34", "3D"): {
        "B_initial": -0.11749,
        "B_limits":  [-0.1254, -0.1096],
        "C_initial": -0.04659,
        "C_limits":  [-0.0503, -0.0428],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "35", "3D"): {
        "B_initial": -0.18884,
        "B_limits":  [-0.2007, -0.177],
        "C_initial": -0.02371,
        "C_limits":  [-0.0305, -0.0169],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "1", "3D"): {
        "B_initial": -0.08976,
        "B_limits":  [-0.1032, -0.0763],
        "C_initial": -0.02204,
        "C_limits":  [-0.0323, -0.0118],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "2", "3D"): {
        "B_initial": -0.13365,
        "B_limits":  [-0.1455, -0.1218],
        "C_initial": 0.0032,
        "C_limits":  [-0.0015, 0.0079],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "3", "3D"): {
        "B_initial": -0.16827,
        "B_limits":  [-0.1784, -0.1581],
        "C_initial": 0.00328,
        "C_limits":  [-0.001, 0.0075],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "4", "3D"): {
        "B_initial": -0.20558,
        "B_limits":  [-0.2139, -0.1972],
        "C_initial": -0.00206,
        "C_limits":  [-0.0072, 0.003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "5", "3D"): {
        "B_initial": -0.25938,
        "B_limits":  [-0.2683, -0.2504],
        "C_initial": -0.00526,
        "C_limits":  [-0.0129, 0.0024],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "6", "3D"): {
        "B_initial": -0.42,
        "B_limits":  [-0.4552, -0.3848],
        "C_initial": 0.0483,
        "C_limits":  [0.0266, 0.07],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "7", "3D"): {
        "B_initial": -0.02599,
        "B_limits":  [-0.0334, -0.0185],
        "C_initial": 0.00193,
        "C_limits":  [-0.0004, 0.0043],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "8", "3D"): {
        "B_initial": -0.07191,
        "B_limits":  [-0.0786, -0.0652],
        "C_initial": 0.00643,
        "C_limits":  [0.0045, 0.0084],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "9", "3D"): {
        "B_initial": -0.11515,
        "B_limits":  [-0.1217, -0.1086],
        "C_initial": 0.0047,
        "C_limits":  [0.0029, 0.0065],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "10", "3D"): {
        "B_initial": -0.16635,
        "B_limits":  [-0.1739, -0.1588],
        "C_initial": 0.0066,
        "C_limits":  [0.0053, 0.0079],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "11", "3D"): {
        "B_initial": -0.24418,
        "B_limits":  [-0.2564, -0.232],
        "C_initial": 0.02288,
        "C_limits":  [0.0189, 0.0269],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "12", "3D"): {
        "B_initial": -0.46608,
        "B_limits":  [-0.5106, -0.4215],
        "C_initial": 0.12983,
        "C_limits":  [0.1043, 0.1554],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "13", "3D"): {
        "B_initial": -0.0037,
        "B_limits":  [-0.0099, 0.0025],
        "C_initial": -0.00165,
        "C_limits":  [-0.003, -0.0003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "14", "3D"): {
        "B_initial": -0.05161,
        "B_limits":  [-0.0573, -0.046],
        "C_initial": -0.00654,
        "C_limits":  [-0.0082, -0.0049],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "15", "3D"): {
        "B_initial": -0.09935,
        "B_limits":  [-0.1055, -0.0932],
        "C_initial": -0.00665,
        "C_limits":  [-0.0081, -0.0052],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "16", "3D"): {
        "B_initial": -0.15718,
        "B_limits":  [-0.1653, -0.1491],
        "C_initial": 0.00258,
        "C_limits":  [0.0004, 0.0047],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "17", "3D"): {
        "B_initial": -0.24586,
        "B_limits":  [-0.2598, -0.232],
        "C_initial": 0.03446,
        "C_limits":  [0.028, 0.0409],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "18", "3D"): {
        "B_initial": -0.493,
        "B_limits":  [-0.542, -0.444],
        "C_initial": 0.18045,
        "C_limits":  [0.1486, 0.2123],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "19", "3D"): {
        "B_initial": -0.00074,
        "B_limits":  [-0.0073, 0.0059],
        "C_initial": -0.00431,
        "C_limits":  [-0.0066, -0.0021],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "20", "3D"): {
        "B_initial": -0.05186,
        "B_limits":  [-0.058, -0.0457],
        "C_initial": -0.01445,
        "C_limits":  [-0.0156, -0.0133],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "21", "3D"): {
        "B_initial": -0.10358,
        "B_limits":  [-0.1104, -0.0968],
        "C_initial": -0.01201,
        "C_limits":  [-0.0134, -0.0106],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "22", "3D"): {
        "B_initial": -0.16649,
        "B_limits":  [-0.1755, -0.1575],
        "C_initial": 0.00402,
        "C_limits":  [0.0008, 0.0073],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "23", "3D"): {
        "B_initial": -0.26263,
        "B_limits":  [-0.2778, -0.2474],
        "C_initial": 0.04915,
        "C_limits":  [0.0406, 0.0577],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "25", "3D"): {
        "B_initial": -0.00744,
        "B_limits":  [-0.0148, -0.0001],
        "C_initial": -0.00415,
        "C_limits":  [-0.0072, -0.0011],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "26", "3D"): {
        "B_initial": -0.06209,
        "B_limits":  [-0.0688, -0.0554],
        "C_initial": -0.01701,
        "C_limits":  [-0.0179, -0.0162],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "27", "3D"): {
        "B_initial": -0.11721,
        "B_limits":  [-0.1246, -0.1099],
        "C_initial": -0.01204,
        "C_limits":  [-0.0138, -0.0103],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "28", "3D"): {
        "B_initial": -0.18402,
        "B_limits":  [-0.1936, -0.1744],
        "C_initial": 0.00954,
        "C_limits":  [0.0054, 0.0137],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "29", "3D"): {
        "B_initial": -0.28541,
        "B_limits":  [-0.3014, -0.2694],
        "C_initial": 0.06489,
        "C_limits":  [0.0547, 0.075],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "31", "3D"): {
        "B_initial": -0.01927,
        "B_limits":  [-0.0275, -0.011],
        "C_initial": -0.00176,
        "C_limits":  [-0.0054, 0.0019],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "32", "3D"): {
        "B_initial": -0.0777,
        "B_limits":  [-0.0851, -0.0704],
        "C_initial": -0.01607,
        "C_limits":  [-0.0168, -0.0153],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "33", "3D"): {
        "B_initial": -0.136,
        "B_limits":  [-0.144, -0.128],
        "C_initial": -0.00859,
        "C_limits":  [-0.0108, -0.0064],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "34", "3D"): {
        "B_initial": -0.20618,
        "B_limits":  [-0.2164, -0.1959],
        "C_initial": 0.01783,
        "C_limits":  [0.0129, 0.0227],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "1", "3D"): {
        "B_initial": -0.061,
        "B_limits":  [-0.0726, -0.0494],
        "C_initial": -0.01195,
        "C_limits":  [-0.0208, -0.0031],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "2", "3D"): {
        "B_initial": -0.11298,
        "B_limits":  [-0.1244, -0.1016],
        "C_initial": 0.01021,
        "C_limits":  [0.0071, 0.0134],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "3", "3D"): {
        "B_initial": -0.15657,
        "B_limits":  [-0.1674, -0.1457],
        "C_initial": 0.01211,
        "C_limits":  [0.0092, 0.0151],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "4", "3D"): {
        "B_initial": -0.2039,
        "B_limits":  [-0.2141, -0.1937],
        "C_initial": 0.01117,
        "C_limits":  [0.0082, 0.0141],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "5", "3D"): {
        "B_initial": -0.2696,
        "B_limits":  [-0.281, -0.2582],
        "C_initial": 0.01612,
        "C_limits":  [0.0117, 0.0205],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "6", "3D"): {
        "B_initial": -0.45015,
        "B_limits":  [-0.4881, -0.4122],
        "C_initial": 0.0931,
        "C_limits":  [0.0699, 0.1163],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "7", "3D"): {
        "B_initial": -0.01674,
        "B_limits":  [-0.0224, -0.0111],
        "C_initial": 0.00133,
        "C_limits":  [-0.0003, 0.0029],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "8", "3D"): {
        "B_initial": -0.06097,
        "B_limits":  [-0.0667, -0.0552],
        "C_initial": -0.00249,
        "C_limits":  [-0.005, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "9", "3D"): {
        "B_initial": -0.1067,
        "B_limits":  [-0.113, -0.1004],
        "C_initial": -0.00496,
        "C_limits":  [-0.0074, -0.0025],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "10", "3D"): {
        "B_initial": -0.16192,
        "B_limits":  [-0.1698, -0.154],
        "C_initial": -0.00035,
        "C_limits":  [-0.0026, 0.0018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "11", "3D"): {
        "B_initial": -0.24495,
        "B_limits":  [-0.2578, -0.2321],
        "C_initial": 0.02302,
        "C_limits":  [0.018, 0.028],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "12", "3D"): {
        "B_initial": -0.47984,
        "B_limits":  [-0.5267, -0.433],
        "C_initial": 0.15579,
        "C_limits":  [0.1256, 0.186],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "13", "3D"): {
        "B_initial": -0.0114,
        "B_limits":  [-0.0164, -0.0065],
        "C_initial": -0.00378,
        "C_limits":  [-0.0062, -0.0013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "14", "3D"): {
        "B_initial": -0.053,
        "B_limits":  [-0.0583, -0.0477],
        "C_initial": -0.01615,
        "C_limits":  [-0.0178, -0.0145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "15", "3D"): {
        "B_initial": -0.09939,
        "B_limits":  [-0.1055, -0.0933],
        "C_initial": -0.01736,
        "C_limits":  [-0.019, -0.0157],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "16", "3D"): {
        "B_initial": -0.1571,
        "B_limits":  [-0.1652, -0.149],
        "C_initial": -0.00648,
        "C_limits":  [-0.0092, -0.0038],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "17", "3D"): {
        "B_initial": -0.24552,
        "B_limits":  [-0.2593, -0.2317],
        "C_initial": 0.03039,
        "C_limits":  [0.0231, 0.0377],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "19", "3D"): {
        "B_initial": -0.01861,
        "B_limits":  [-0.0238, -0.0134],
        "C_initial": -0.00519,
        "C_limits":  [-0.0087, -0.0017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "20", "3D"): {
        "B_initial": -0.05985,
        "B_limits":  [-0.0654, -0.0543],
        "C_initial": -0.02187,
        "C_limits":  [-0.023, -0.0207],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "21", "3D"): {
        "B_initial": -0.10731,
        "B_limits":  [-0.1138, -0.1009],
        "C_initial": -0.02092,
        "C_limits":  [-0.0225, -0.0194],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "22", "3D"): {
        "B_initial": -0.167,
        "B_limits":  [-0.1756, -0.1584],
        "C_initial": -0.00434,
        "C_limits":  [-0.0079, -0.0008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "23", "3D"): {
        "B_initial": -0.25892,
        "B_limits":  [-0.2734, -0.2444],
        "C_initial": 0.04354,
        "C_limits":  [0.0344, 0.0527],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "25", "3D"): {
        "B_initial": -0.03348,
        "B_limits":  [-0.0393, -0.0277],
        "C_initial": -0.00301,
        "C_limits":  [-0.0073, 0.0013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "26", "3D"): {
        "B_initial": -0.07577,
        "B_limits":  [-0.0819, -0.0697],
        "C_initial": -0.022,
        "C_limits":  [-0.0229, -0.021],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "27", "3D"): {
        "B_initial": -0.12476,
        "B_limits":  [-0.1318, -0.1177],
        "C_initial": -0.01838,
        "C_limits":  [-0.0203, -0.0165],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "28", "3D"): {
        "B_initial": -0.18645,
        "B_limits":  [-0.1957, -0.1772],
        "C_initial": 0.00374,
        "C_limits":  [-0.0008, 0.0082],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "1", "3D"): {
        "B_initial": -0.06332,
        "B_limits":  [-0.0723, -0.0543],
        "C_initial": -0.00873,
        "C_limits":  [-0.0165, -0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "2", "3D"): {
        "B_initial": -0.1226,
        "B_limits":  [-0.1302, -0.115],
        "C_initial": 0.0203,
        "C_limits":  [0.0179, 0.0227],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "3", "3D"): {
        "B_initial": -0.17386,
        "B_limits":  [-0.1823, -0.1654],
        "C_initial": 0.02724,
        "C_limits":  [0.0255, 0.029],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "4", "3D"): {
        "B_initial": -0.23056,
        "B_limits":  [-0.2402, -0.2209],
        "C_initial": 0.02856,
        "C_limits":  [0.0265, 0.0306],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "5", "3D"): {
        "B_initial": -0.29769,
        "B_limits":  [-0.3092, -0.2862],
        "C_initial": 0.03049,
        "C_limits":  [0.0282, 0.0328],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "7", "3D"): {
        "B_initial": -0.0372,
        "B_limits":  [-0.044, -0.0304],
        "C_initial": 0.00569,
        "C_limits":  [0.003, 0.0084],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "8", "3D"): {
        "B_initial": -0.08333,
        "B_limits":  [-0.0907, -0.076],
        "C_initial": 0.01216,
        "C_limits":  [0.0092, 0.0151],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "9", "3D"): {
        "B_initial": -0.1299,
        "B_limits":  [-0.1385, -0.1213],
        "C_initial": 0.01012,
        "C_limits":  [0.0063, 0.0139],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "10", "3D"): {
        "B_initial": -0.18621,
        "B_limits":  [-0.1962, -0.1762],
        "C_initial": 0.0085,
        "C_limits":  [0.0046, 0.0124],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "11", "3D"): {
        "B_initial": -0.25845,
        "B_limits":  [-0.2706, -0.2463],
        "C_initial": 0.01424,
        "C_limits":  [0.0107, 0.0178],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "12", "3D"): {
        "B_initial": -0.39053,
        "B_limits":  [-0.414, -0.3671],
        "C_initial": 0.05831,
        "C_limits":  [0.0479, 0.0687],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "13", "3D"): {
        "B_initial": -0.01966,
        "B_limits":  [-0.0238, -0.0156],
        "C_initial": 0.00148,
        "C_limits":  [-0.0003, 0.0032],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "14", "3D"): {
        "B_initial": -0.05444,
        "B_limits":  [-0.0594, -0.0495],
        "C_initial": -0.00715,
        "C_limits":  [-0.0098, -0.0045],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "15", "3D"): {
        "B_initial": -0.09596,
        "B_limits":  [-0.1022, -0.0897],
        "C_initial": -0.01345,
        "C_limits":  [-0.0164, -0.0105],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "16", "3D"): {
        "B_initial": -0.15,
        "B_limits":  [-0.1581, -0.1419],
        "C_initial": -0.01389,
        "C_limits":  [-0.0169, -0.0109],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "17", "3D"): {
        "B_initial": -0.2234,
        "B_limits":  [-0.2343, -0.2125],
        "C_initial": -0.0007,
        "C_limits":  [-0.0047, 0.0033],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "18", "3D"): {
        "B_initial": -0.36505,
        "B_limits":  [-0.3899, -0.3402],
        "C_initial": 0.06427,
        "C_limits":  [0.05, 0.0786],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "19", "3D"): {
        "B_initial": -0.01654,
        "B_limits":  [-0.0195, -0.0136],
        "C_initial": -0.00296,
        "C_limits":  [-0.0058, -0.0001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "20", "3D"): {
        "B_initial": -0.04454,
        "B_limits":  [-0.0486, -0.0405],
        "C_initial": -0.01955,
        "C_limits":  [-0.0218, -0.0174],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "21", "3D"): {
        "B_initial": -0.08282,
        "B_limits":  [-0.0883, -0.0773],
        "C_initial": -0.02682,
        "C_limits":  [-0.0291, -0.0245],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "22", "3D"): {
        "B_initial": -0.13509,
        "B_limits":  [-0.1426, -0.1276],
        "C_initial": -0.02437,
        "C_limits":  [-0.0271, -0.0216],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "23", "3D"): {
        "B_initial": -0.20843,
        "B_limits":  [-0.2191, -0.1977],
        "C_initial": -0.0037,
        "C_limits":  [-0.0087, 0.0013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "24", "3D"): {
        "B_initial": -0.35397,
        "B_limits":  [-0.3796, -0.3283],
        "C_initial": 0.07887,
        "C_limits":  [0.0614, 0.0963],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "25", "3D"): {
        "B_initial": -0.02071,
        "B_limits":  [-0.0232, -0.0182],
        "C_initial": -0.0044,
        "C_limits":  [-0.0082, -0.0006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "26", "3D"): {
        "B_initial": -0.04471,
        "B_limits":  [-0.0485, -0.0409],
        "C_initial": -0.02547,
        "C_limits":  [-0.0274, -0.0236],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "27", "3D"): {
        "B_initial": -0.08107,
        "B_limits":  [-0.0864, -0.0757],
        "C_initial": -0.03246,
        "C_limits":  [-0.0343, -0.0306],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "28", "3D"): {
        "B_initial": -0.13224,
        "B_limits":  [-0.1398, -0.1247],
        "C_initial": -0.02692,
        "C_limits":  [-0.0298, -0.0241],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "29", "3D"): {
        "B_initial": -0.20543,
        "B_limits":  [-0.2163, -0.1945],
        "C_initial": 0.0002,
        "C_limits":  [-0.0057, 0.0061],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "31", "3D"): {
        "B_initial": -0.03074,
        "B_limits":  [-0.0335, -0.028],
        "C_initial": -0.00294,
        "C_limits":  [-0.0075, 0.0016],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "32", "3D"): {
        "B_initial": -0.05208,
        "B_limits":  [-0.056, -0.0481],
        "C_initial": -0.02697,
        "C_limits":  [-0.0287, -0.0252],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "33", "3D"): {
        "B_initial": -0.0872,
        "B_limits":  [-0.0928, -0.0816],
        "C_initial": -0.03293,
        "C_limits":  [-0.0345, -0.0314],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "34", "3D"): {
        "B_initial": -0.1377,
        "B_limits":  [-0.1455, -0.1299],
        "C_initial": -0.02382,
        "C_limits":  [-0.027, -0.0207],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "35", "3D"): {
        "B_initial": -0.21083,
        "B_limits":  [-0.2221, -0.1995],
        "C_initial": 0.00995,
        "C_limits":  [0.003, 0.0169],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "1", "3D"): {
        "B_initial": -0.05931,
        "B_limits":  [-0.0693, -0.0493],
        "C_initial": 0.00328,
        "C_limits":  [-0.0016, 0.0082],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "2", "3D"): {
        "B_initial": -0.12839,
        "B_limits":  [-0.1377, -0.119],
        "C_initial": 0.0198,
        "C_limits":  [0.0171, 0.0225],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "3", "3D"): {
        "B_initial": -0.18735,
        "B_limits":  [-0.1976, -0.1771],
        "C_initial": 0.0215,
        "C_limits":  [0.0173, 0.0257],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "4", "3D"): {
        "B_initial": -0.25046,
        "B_limits":  [-0.2627, -0.2383],
        "C_initial": 0.02031,
        "C_limits":  [0.015, 0.0256],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "5", "3D"): {
        "B_initial": -0.3383,
        "B_limits":  [-0.3552, -0.3214],
        "C_initial": 0.02188,
        "C_limits":  [0.016, 0.0278],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "6", "3D"): {
        "B_initial": -0.04042,
        "B_limits":  [-0.0472, -0.0336],
        "C_initial": 0.00655,
        "C_limits":  [0.0048, 0.0083],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "7", "3D"): {
        "B_initial": -0.09221,
        "B_limits":  [-0.0992, -0.0852],
        "C_initial": 0.0037,
        "C_limits":  [0.0004, 0.007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "8", "3D"): {
        "B_initial": -0.14246,
        "B_limits":  [-0.1502, -0.1348],
        "C_initial": -0.00313,
        "C_limits":  [-0.0076, 0.0013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "9", "3D"): {
        "B_initial": -0.19986,
        "B_limits":  [-0.2093, -0.1904],
        "C_initial": -0.00884,
        "C_limits":  [-0.014, -0.0036],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "10", "3D"): {
        "B_initial": -0.28485,
        "B_limits":  [-0.2994, -0.2703],
        "C_initial": -0.00765,
        "C_limits":  [-0.0136, -0.0017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "11", "3D"): {
        "B_initial": -0.02852,
        "B_limits":  [-0.0334, -0.0236],
        "C_initial": 0.0023,
        "C_limits":  [0.0001, 0.0045],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "12", "3D"): {
        "B_initial": -0.06959,
        "B_limits":  [-0.0753, -0.0639],
        "C_initial": -0.0102,
        "C_limits":  [-0.0137, -0.0067],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "13", "3D"): {
        "B_initial": -0.11404,
        "B_limits":  [-0.1205, -0.1076],
        "C_initial": -0.02052,
        "C_limits":  [-0.0249, -0.0161],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "14", "3D"): {
        "B_initial": -0.16721,
        "B_limits":  [-0.1753, -0.1591],
        "C_initial": -0.02722,
        "C_limits":  [-0.0324, -0.0221],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "15", "3D"): {
        "B_initial": -0.24907,
        "B_limits":  [-0.2625, -0.2357],
        "C_initial": -0.02391,
        "C_limits":  [-0.0302, -0.0177],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "16", "3D"): {
        "B_initial": -0.02063,
        "B_limits":  [-0.0242, -0.0171],
        "C_initial": -0.00198,
        "C_limits":  [-0.0052, 0.0012],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "17", "3D"): {
        "B_initial": -0.05286,
        "B_limits":  [-0.0579, -0.0478],
        "C_initial": -0.02143,
        "C_limits":  [-0.025, -0.0178],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "18", "3D"): {
        "B_initial": -0.0924,
        "B_limits":  [-0.0983, -0.0865],
        "C_initial": -0.03377,
        "C_limits":  [-0.0381, -0.0294],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "19", "3D"): {
        "B_initial": -0.14183,
        "B_limits":  [-0.1494, -0.1342],
        "C_initial": -0.04034,
        "C_limits":  [-0.0454, -0.0352],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "20", "3D"): {
        "B_initial": -0.22058,
        "B_limits":  [-0.2335, -0.2077],
        "C_initial": -0.03392,
        "C_limits":  [-0.0405, -0.0274],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "21", "3D"): {
        "B_initial": -0.01638,
        "B_limits":  [-0.019, -0.0138],
        "C_initial": -0.00493,
        "C_limits":  [-0.009, -0.0009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "22", "3D"): {
        "B_initial": -0.04178,
        "B_limits":  [-0.0462, -0.0373],
        "C_initial": -0.02923,
        "C_limits":  [-0.0327, -0.0258],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "23", "3D"): {
        "B_initial": -0.07746,
        "B_limits":  [-0.0828, -0.0721],
        "C_initial": -0.04263,
        "C_limits":  [-0.0467, -0.0386],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "24", "3D"): {
        "B_initial": -0.12388,
        "B_limits":  [-0.131, -0.1168],
        "C_initial": -0.04852,
        "C_limits":  [-0.0534, -0.0436],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "25", "3D"): {
        "B_initial": -0.19998,
        "B_limits":  [-0.2124, -0.1875],
        "C_initial": -0.03886,
        "C_limits":  [-0.0456, -0.0321],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "26", "3D"): {
        "B_initial": -0.0151,
        "B_limits":  [-0.0173, -0.0129],
        "C_initial": -0.00632,
        "C_limits":  [-0.0109, -0.0017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "27", "3D"): {
        "B_initial": -0.03566,
        "B_limits":  [-0.04, -0.0313],
        "C_initial": -0.03372,
        "C_limits":  [-0.0371, -0.0303],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "28", "3D"): {
        "B_initial": -0.06856,
        "B_limits":  [-0.074, -0.0631],
        "C_initial": -0.04751,
        "C_limits":  [-0.0514, -0.0437],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "29", "3D"): {
        "B_initial": -0.11276,
        "B_limits":  [-0.1199, -0.1056],
        "C_initial": -0.05249,
        "C_limits":  [-0.0572, -0.0478],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "30", "3D"): {
        "B_initial": -0.18683,
        "B_limits":  [-0.1993, -0.1744],
        "C_initial": -0.03987,
        "C_limits":  [-0.0468, -0.0329],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "31", "3D"): {
        "B_initial": -0.0172,
        "B_limits":  [-0.0197, -0.0147],
        "C_initial": -0.00615,
        "C_limits":  [-0.0116, -0.0007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "32", "3D"): {
        "B_initial": -0.03116,
        "B_limits":  [-0.0357, -0.0267],
        "C_initial": -0.03722,
        "C_limits":  [-0.0404, -0.034],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "33", "3D"): {
        "B_initial": -0.0602,
        "B_limits":  [-0.066, -0.0544],
        "C_initial": -0.05091,
        "C_limits":  [-0.0544, -0.0475],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "34", "3D"): {
        "B_initial": -0.10129,
        "B_limits":  [-0.1089, -0.0936],
        "C_initial": -0.05383,
        "C_limits":  [-0.0582, -0.0495],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "35", "3D"): {
        "B_initial": -0.17234,
        "B_limits":  [-0.1851, -0.1596],
        "C_initial": -0.03593,
        "C_limits":  [-0.0432, -0.0286],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "1", "3D"): {
        "B_initial": -0.07113,
        "B_limits":  [-0.0849, -0.0574],
        "C_initial": -0.02257,
        "C_limits":  [-0.0311, -0.0141],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "2", "3D"): {
        "B_initial": -0.11113,
        "B_limits":  [-0.1236, -0.0986],
        "C_initial": -0.00302,
        "C_limits":  [-0.0064, 0.0003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "3", "3D"): {
        "B_initial": -0.14204,
        "B_limits":  [-0.1534, -0.1306],
        "C_initial": -0.00153,
        "C_limits":  [-0.0045, 0.0015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "4", "3D"): {
        "B_initial": -0.1761,
        "B_limits":  [-0.1858, -0.1664],
        "C_initial": -0.00268,
        "C_limits":  [-0.0059, 0.0005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "5", "3D"): {
        "B_initial": -0.22435,
        "B_limits":  [-0.2337, -0.2149],
        "C_initial": -0.00183,
        "C_limits":  [-0.0068, 0.0031],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "6", "3D"): {
        "B_initial": -0.30658,
        "B_limits":  [-0.3199, -0.2932],
        "C_initial": 0.01482,
        "C_limits":  [0.0043, 0.0253],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "7", "3D"): {
        "B_initial": -0.458,
        "B_limits":  [-0.4854, -0.4306],
        "C_initial": 0.08138,
        "C_limits":  [0.0596, 0.1032],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "8", "3D"): {
        "B_initial": -0.01234,
        "B_limits":  [-0.0186, -0.006],
        "C_initial": -0.00766,
        "C_limits":  [-0.0093, -0.006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "9", "3D"): {
        "B_initial": -0.05373,
        "B_limits":  [-0.0585, -0.049],
        "C_initial": -0.00999,
        "C_limits":  [-0.012, -0.008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "10", "3D"): {
        "B_initial": -0.09129,
        "B_limits":  [-0.0966, -0.086],
        "C_initial": -0.01023,
        "C_limits":  [-0.0121, -0.0084],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "11", "3D"): {
        "B_initial": -0.13564,
        "B_limits":  [-0.1416, -0.1297],
        "C_initial": -0.00545,
        "C_limits":  [-0.007, -0.0039],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "12", "3D"): {
        "B_initial": -0.20156,
        "B_limits":  [-0.212, -0.1911],
        "C_initial": 0.01254,
        "C_limits":  [0.0086, 0.0165],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "13", "3D"): {
        "B_initial": -0.315,
        "B_limits":  [-0.3328, -0.2972],
        "C_initial": 0.06475,
        "C_limits":  [0.0542, 0.0753],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "14", "3D"): {
        "B_initial": -0.51423,
        "B_limits":  [-0.5465, -0.482],
        "C_initial": 0.18522,
        "C_limits":  [0.1628, 0.2076],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "15", "3D"): {
        "B_initial": -0.00478,
        "B_limits":  [-0.0111, 0.0016],
        "C_initial": -0.00932,
        "C_limits":  [-0.0115, -0.0071],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "16", "3D"): {
        "B_initial": -0.04953,
        "B_limits":  [-0.0542, -0.0448],
        "C_initial": -0.01855,
        "C_limits":  [-0.0194, -0.0177],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "17", "3D"): {
        "B_initial": -0.09098,
        "B_limits":  [-0.0967, -0.0853],
        "C_initial": -0.01701,
        "C_limits":  [-0.018, -0.016],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "18", "3D"): {
        "B_initial": -0.14022,
        "B_limits":  [-0.1469, -0.1335],
        "C_initial": -0.00669,
        "C_limits":  [-0.0088, -0.0046],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "19", "3D"): {
        "B_initial": -0.21337,
        "B_limits":  [-0.2252, -0.2016],
        "C_initial": 0.0229,
        "C_limits":  [0.0171, 0.0287],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "20", "3D"): {
        "B_initial": -0.33799,
        "B_limits":  [-0.3575, -0.3185],
        "C_initial": 0.09661,
        "C_limits":  [0.0834, 0.1099],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "22", "3D"): {
        "B_initial": -0.0107,
        "B_limits":  [-0.0178, -0.0036],
        "C_initial": -0.00755,
        "C_limits":  [-0.0105, -0.0046],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "23", "3D"): {
        "B_initial": -0.05889,
        "B_limits":  [-0.0641, -0.0537],
        "C_initial": -0.01938,
        "C_limits":  [-0.0199, -0.0189],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "24", "3D"): {
        "B_initial": -0.10321,
        "B_limits":  [-0.1094, -0.097],
        "C_initial": -0.01606,
        "C_limits":  [-0.0173, -0.0148],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "25", "3D"): {
        "B_initial": -0.15563,
        "B_limits":  [-0.1628, -0.1484],
        "C_initial": -0.00188,
        "C_limits":  [-0.0046, 0.0008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "26", "3D"): {
        "B_initial": -0.23303,
        "B_limits":  [-0.2455, -0.2206],
        "C_initial": 0.03506,
        "C_limits":  [0.0281, 0.0421],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "29", "3D"): {
        "B_initial": -0.02157,
        "B_limits":  [-0.0296, -0.0136],
        "C_initial": -0.00361,
        "C_limits":  [-0.0071, -0.0001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "30", "3D"): {
        "B_initial": -0.07348,
        "B_limits":  [-0.0793, -0.0676],
        "C_initial": -0.01683,
        "C_limits":  [-0.0175, -0.0162],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "31", "3D"): {
        "B_initial": -0.12057,
        "B_limits":  [-0.1274, -0.1137],
        "C_initial": -0.01167,
        "C_limits":  [-0.0133, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "32", "3D"): {
        "B_initial": -0.17587,
        "B_limits":  [-0.1837, -0.168],
        "C_initial": 0.00598,
        "C_limits":  [0.0027, 0.0093],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "1", "3D"): {
        "B_initial": -0.05854,
        "B_limits":  [-0.068, -0.0491],
        "C_initial": -0.01848,
        "C_limits":  [-0.0269, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "2", "3D"): {
        "B_initial": -0.11009,
        "B_limits":  [-0.1191, -0.1011],
        "C_initial": 0.00591,
        "C_limits":  [0.003, 0.0089],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "3", "3D"): {
        "B_initial": -0.15507,
        "B_limits":  [-0.1638, -0.1463],
        "C_initial": 0.00976,
        "C_limits":  [0.0074, 0.0121],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "4", "3D"): {
        "B_initial": -0.20406,
        "B_limits":  [-0.213, -0.1951],
        "C_initial": 0.00978,
        "C_limits":  [0.0073, 0.0123],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "5", "3D"): {
        "B_initial": -0.27181,
        "B_limits":  [-0.2832, -0.2604],
        "C_initial": 0.01444,
        "C_limits":  [0.0109, 0.018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "6", "3D"): {
        "B_initial": -0.41113,
        "B_limits":  [-0.4371, -0.3852],
        "C_initial": 0.06137,
        "C_limits":  [0.0479, 0.0749],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "7", "3D"): {
        "B_initial": -0.02449,
        "B_limits":  [-0.0302, -0.0188],
        "C_initial": -0.00225,
        "C_limits":  [-0.0041, -0.0004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "8", "3D"): {
        "B_initial": -0.06761,
        "B_limits":  [-0.0737, -0.0615],
        "C_initial": -0.00062,
        "C_limits":  [-0.0028, 0.0016],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "9", "3D"): {
        "B_initial": -0.11253,
        "B_limits":  [-0.1191, -0.106],
        "C_initial": -0.00254,
        "C_limits":  [-0.0049, -0.0002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "10", "3D"): {
        "B_initial": -0.1663,
        "B_limits":  [-0.1743, -0.1583],
        "C_initial": -0.00018,
        "C_limits":  [-0.0023, 0.002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "11", "3D"): {
        "B_initial": -0.24638,
        "B_limits":  [-0.259, -0.2338],
        "C_initial": 0.01684,
        "C_limits":  [0.0129, 0.0207],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "12", "3D"): {
        "B_initial": -0.41841,
        "B_limits":  [-0.4492, -0.3876],
        "C_initial": 0.09707,
        "C_limits":  [0.0797, 0.1145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "13", "3D"): {
        "B_initial": -0.01232,
        "B_limits":  [-0.0167, -0.0079],
        "C_initial": -0.00571,
        "C_limits":  [-0.0074, -0.004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "14", "3D"): {
        "B_initial": -0.05131,
        "B_limits":  [-0.0565, -0.0462],
        "C_initial": -0.01403,
        "C_limits":  [-0.0158, -0.0122],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "15", "3D"): {
        "B_initial": -0.09589,
        "B_limits":  [-0.1018, -0.09],
        "C_initial": -0.01619,
        "C_limits":  [-0.018, -0.0144],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "16", "3D"): {
        "B_initial": -0.15138,
        "B_limits":  [-0.1592, -0.1436],
        "C_initial": -0.00897,
        "C_limits":  [-0.0113, -0.0067],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "17", "3D"): {
        "B_initial": -0.23622,
        "B_limits":  [-0.2494, -0.2231],
        "C_initial": 0.0199,
        "C_limits":  [0.0139, 0.0259],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "18", "3D"): {
        "B_initial": -0.42073,
        "B_limits":  [-0.4537, -0.3877],
        "C_initial": 0.12685,
        "C_limits":  [0.1049, 0.1488],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "19", "3D"): {
        "B_initial": -0.01311,
        "B_limits":  [-0.0173, -0.0089],
        "C_initial": -0.00712,
        "C_limits":  [-0.0099, -0.0044],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "20", "3D"): {
        "B_initial": -0.05054,
        "B_limits":  [-0.0556, -0.0454],
        "C_initial": -0.0212,
        "C_limits":  [-0.0224, -0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "21", "3D"): {
        "B_initial": -0.0956,
        "B_limits":  [-0.1016, -0.0896],
        "C_initial": -0.02193,
        "C_limits":  [-0.0232, -0.0206],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "22", "3D"): {
        "B_initial": -0.15273,
        "B_limits":  [-0.1609, -0.1446],
        "C_initial": -0.00929,
        "C_limits":  [-0.0123, -0.0063],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "23", "3D"): {
        "B_initial": -0.241,
        "B_limits":  [-0.2548, -0.2272],
        "C_initial": 0.03083,
        "C_limits":  [0.0229, 0.0387],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "25", "3D"): {
        "B_initial": -0.01978,
        "B_limits":  [-0.0241, -0.0154],
        "C_initial": -0.00582,
        "C_limits":  [-0.0093, -0.0023],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "26", "3D"): {
        "B_initial": -0.05727,
        "B_limits":  [-0.0625, -0.0521],
        "C_initial": -0.02257,
        "C_limits":  [-0.0235, -0.0216],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "27", "3D"): {
        "B_initial": -0.10317,
        "B_limits":  [-0.1094, -0.0969],
        "C_initial": -0.02162,
        "C_limits":  [-0.023, -0.0202],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "28", "3D"): {
        "B_initial": -0.16166,
        "B_limits":  [-0.1701, -0.1532],
        "C_initial": -0.00476,
        "C_limits":  [-0.0083, -0.0012],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "29", "3D"): {
        "B_initial": -0.25219,
        "B_limits":  [-0.2665, -0.2379],
        "C_initial": 0.04343,
        "C_limits":  [0.0344, 0.0525],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "31", "3D"): {
        "B_initial": -0.02971,
        "B_limits":  [-0.0345, -0.0249],
        "C_initial": -0.00256,
        "C_limits":  [-0.0066, 0.0015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "32", "3D"): {
        "B_initial": -0.06809,
        "B_limits":  [-0.0737, -0.0625],
        "C_initial": -0.02066,
        "C_limits":  [-0.0216, -0.0197],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "33", "3D"): {
        "B_initial": -0.11507,
        "B_limits":  [-0.1217, -0.1084],
        "C_initial": -0.01791,
        "C_limits":  [-0.0196, -0.0162],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "34", "3D"): {
        "B_initial": -0.17492,
        "B_limits":  [-0.1838, -0.166],
        "C_initial": 0.0027,
        "C_limits":  [-0.0015, 0.0069],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "1", "3D"): {
        "B_initial": -0.04508,
        "B_limits":  [-0.0536, -0.0365],
        "C_initial": -0.00652,
        "C_limits":  [-0.0123, -0.0007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "2", "3D"): {
        "B_initial": -0.10505,
        "B_limits":  [-0.1139, -0.0962],
        "C_initial": 0.01186,
        "C_limits":  [0.0096, 0.0142],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "3", "3D"): {
        "B_initial": -0.16422,
        "B_limits":  [-0.1745, -0.154],
        "C_initial": 0.01449,
        "C_limits":  [0.0112, 0.0178],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "4", "3D"): {
        "B_initial": -0.23911,
        "B_limits":  [-0.2524, -0.2258],
        "C_initial": 0.01508,
        "C_limits":  [0.0112, 0.0189],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "5", "3D"): {
        "B_initial": -0.34031,
        "B_limits":  [-0.3569, -0.3237],
        "C_initial": 0.02632,
        "C_limits":  [0.022, 0.0307],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "6", "3D"): {
        "B_initial": -0.02306,
        "B_limits":  [-0.0283, -0.0179],
        "C_initial": -0.00038,
        "C_limits":  [-0.0023, 0.0015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "7", "3D"): {
        "B_initial": -0.06478,
        "B_limits":  [-0.0717, -0.0579],
        "C_initial": -0.00611,
        "C_limits":  [-0.0096, -0.0026],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "8", "3D"): {
        "B_initial": -0.11532,
        "B_limits":  [-0.124, -0.1067],
        "C_initial": -0.01215,
        "C_limits":  [-0.0163, -0.0079],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "9", "3D"): {
        "B_initial": -0.18677,
        "B_limits":  [-0.1989, -0.1746],
        "C_initial": -0.01119,
        "C_limits":  [-0.0155, -0.0069],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "10", "3D"): {
        "B_initial": -0.29249,
        "B_limits":  [-0.309, -0.276],
        "C_initial": 0.01216,
        "C_limits":  [0.0057, 0.0187],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "11", "3D"): {
        "B_initial": -0.01419,
        "B_limits":  [-0.017, -0.0113],
        "C_initial": -0.00473,
        "C_limits":  [-0.0077, -0.0018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "12", "3D"): {
        "B_initial": -0.04464,
        "B_limits":  [-0.0494, -0.0399],
        "C_initial": -0.02228,
        "C_limits":  [-0.0247, -0.0199],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "13", "3D"): {
        "B_initial": -0.0892,
        "B_limits":  [-0.0958, -0.0826],
        "C_initial": -0.03009,
        "C_limits":  [-0.0328, -0.0274],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "14", "3D"): {
        "B_initial": -0.1571,
        "B_limits":  [-0.1677, -0.1465],
        "C_initial": -0.02393,
        "C_limits":  [-0.0279, -0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "15", "3D"): {
        "B_initial": -0.26284,
        "B_limits":  [-0.2786, -0.247],
        "C_initial": 0.01374,
        "C_limits":  [0.005, 0.0224],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "16", "3D"): {
        "B_initial": -0.01712,
        "B_limits":  [-0.0194, -0.0148],
        "C_initial": -0.00484,
        "C_limits":  [-0.0088, -0.0009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "17", "3D"): {
        "B_initial": -0.04225,
        "B_limits":  [-0.0467, -0.0379],
        "C_initial": -0.02732,
        "C_limits":  [-0.0294, -0.0253],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "18", "3D"): {
        "B_initial": -0.08394,
        "B_limits":  [-0.0903, -0.0775],
        "C_initial": -0.0343,
        "C_limits":  [-0.0364, -0.0322],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "19", "3D"): {
        "B_initial": -0.15002,
        "B_limits":  [-0.1606, -0.1395],
        "C_initial": -0.02286,
        "C_limits":  [-0.0272, -0.0185],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "20", "3D"): {
        "B_initial": -0.25532,
        "B_limits":  [-0.2714, -0.2393],
        "C_initial": 0.02599,
        "C_limits":  [0.0157, 0.0363],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "21", "3D"): {
        "B_initial": -0.02637,
        "B_limits":  [-0.0289, -0.0239],
        "C_initial": -0.00126,
        "C_limits":  [-0.006, 0.0035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "22", "3D"): {
        "B_initial": -0.04838,
        "B_limits":  [-0.0529, -0.0438],
        "C_initial": -0.02642,
        "C_limits":  [-0.0283, -0.0245],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "23", "3D"): {
        "B_initial": -0.08842,
        "B_limits":  [-0.0951, -0.0817],
        "C_initial": -0.03161,
        "C_limits":  [-0.0335, -0.0297],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "24", "3D"): {
        "B_initial": -0.15345,
        "B_limits":  [-0.1643, -0.1426],
        "C_initial": -0.01454,
        "C_limits":  [-0.0196, -0.0095],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "1", "3D"): {
        "B_initial": -0.04141,
        "B_limits":  [-0.0511, -0.0318],
        "C_initial": -0.00032,
        "C_limits":  [-0.004, 0.0034],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "2", "3D"): {
        "B_initial": -0.10497,
        "B_limits":  [-0.1145, -0.0955],
        "C_initial": 0.00349,
        "C_limits":  [-0.001, 0.008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "3", "3D"): {
        "B_initial": -0.16096,
        "B_limits":  [-0.1728, -0.1492],
        "C_initial": -0.00075,
        "C_limits":  [-0.0075, 0.006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "4", "3D"): {
        "B_initial": -0.22638,
        "B_limits":  [-0.2408, -0.2119],
        "C_initial": -0.00634,
        "C_limits":  [-0.0148, 0.0022],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "6", "3D"): {
        "B_initial": -0.02302,
        "B_limits":  [-0.0281, -0.0179],
        "C_initial": -0.00171,
        "C_limits":  [-0.005, 0.0016],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "7", "3D"): {
        "B_initial": -0.06224,
        "B_limits":  [-0.0681, -0.0564],
        "C_initial": -0.01961,
        "C_limits":  [-0.0241, -0.0151],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "8", "3D"): {
        "B_initial": -0.10482,
        "B_limits":  [-0.1122, -0.0974],
        "C_initial": -0.03298,
        "C_limits":  [-0.0389, -0.027],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "9", "3D"): {
        "B_initial": -0.15912,
        "B_limits":  [-0.1685, -0.1498],
        "C_initial": -0.04362,
        "C_limits":  [-0.0509, -0.0363],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "10", "3D"): {
        "B_initial": -0.24755,
        "B_limits":  [-0.2632, -0.2319],
        "C_initial": -0.0454,
        "C_limits":  [-0.0545, -0.0363],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "11", "3D"): {
        "B_initial": -0.01297,
        "B_limits":  [-0.016, -0.0099],
        "C_initial": -0.00609,
        "C_limits":  [-0.0107, -0.0015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "12", "3D"): {
        "B_initial": -0.03953,
        "B_limits":  [-0.0441, -0.0349],
        "C_initial": -0.03249,
        "C_limits":  [-0.0367, -0.0283],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "13", "3D"): {
        "B_initial": -0.07478,
        "B_limits":  [-0.0808, -0.0687],
        "C_initial": -0.0483,
        "C_limits":  [-0.0537, -0.0429],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "14", "3D"): {
        "B_initial": -0.12267,
        "B_limits":  [-0.1306, -0.1148],
        "C_initial": -0.0589,
        "C_limits":  [-0.0657, -0.0521],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "15", "3D"): {
        "B_initial": -0.20469,
        "B_limits":  [-0.2189, -0.1905],
        "C_initial": -0.05661,
        "C_limits":  [-0.0656, -0.0476],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "16", "3D"): {
        "B_initial": -0.00879,
        "B_limits":  [-0.0111, -0.0065],
        "C_initial": -0.00742,
        "C_limits":  [-0.0129, -0.002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "17", "3D"): {
        "B_initial": -0.02695,
        "B_limits":  [-0.0311, -0.0228],
        "C_initial": -0.03857,
        "C_limits":  [-0.0425, -0.0346],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "18", "3D"): {
        "B_initial": -0.05726,
        "B_limits":  [-0.0629, -0.0517],
        "C_initial": -0.05513,
        "C_limits":  [-0.0601, -0.0502],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "19", "3D"): {
        "B_initial": -0.10073,
        "B_limits":  [-0.1081, -0.0933],
        "C_initial": -0.06462,
        "C_limits":  [-0.0709, -0.0583],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "20", "3D"): {
        "B_initial": -0.17812,
        "B_limits":  [-0.1917, -0.1646],
        "C_initial": -0.05793,
        "C_limits":  [-0.0669, -0.049],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "21", "3D"): {
        "B_initial": -0.00929,
        "B_limits":  [-0.012, -0.0065],
        "C_initial": -0.00524,
        "C_limits":  [-0.0114, 0.0009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "22", "3D"): {
        "B_initial": -0.02006,
        "B_limits":  [-0.0246, -0.0155],
        "C_initial": -0.03973,
        "C_limits":  [-0.0433, -0.0361],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "23", "3D"): {
        "B_initial": -0.04595,
        "B_limits":  [-0.0521, -0.0398],
        "C_initial": -0.05602,
        "C_limits":  [-0.0604, -0.0517],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "24", "3D"): {
        "B_initial": -0.08539,
        "B_limits":  [-0.0934, -0.0774],
        "C_initial": -0.06335,
        "C_limits":  [-0.0691, -0.0576],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "25", "3D"): {
        "B_initial": -0.15837,
        "B_limits":  [-0.1722, -0.1445],
        "C_initial": -0.05088,
        "C_limits":  [-0.0599, -0.0419],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "1", "3D"): {
        "B_initial": -0.07169,
        "B_limits":  [-0.0828, -0.0606],
        "C_initial": -0.03415,
        "C_limits":  [-0.0431, -0.0252],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "2", "3D"): {
        "B_initial": -0.11716,
        "B_limits":  [-0.1276, -0.1067],
        "C_initial": -0.01227,
        "C_limits":  [-0.0161, -0.0085],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "3", "3D"): {
        "B_initial": -0.16037,
        "B_limits":  [-0.1693, -0.1514],
        "C_initial": -0.00983,
        "C_limits":  [-0.0132, -0.0065],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "4", "3D"): {
        "B_initial": -0.21638,
        "B_limits":  [-0.2263, -0.2065],
        "C_initial": -0.00782,
        "C_limits":  [-0.0125, -0.0032],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "5", "3D"): {
        "B_initial": -0.37091,
        "B_limits":  [-0.4027, -0.3391],
        "C_initial": 0.03957,
        "C_limits":  [0.0226, 0.0565],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "6", "3D"): {
        "B_initial": -0.02432,
        "B_limits":  [-0.0303, -0.0183],
        "C_initial": -0.0147,
        "C_limits":  [-0.0166, -0.0128],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "7", "3D"): {
        "B_initial": -0.0699,
        "B_limits":  [-0.0767, -0.0631],
        "C_initial": -0.01367,
        "C_limits":  [-0.0154, -0.0119],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "8", "3D"): {
        "B_initial": -0.12059,
        "B_limits":  [-0.1275, -0.1137],
        "C_initial": -0.01151,
        "C_limits":  [-0.0131, -0.0099],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "9", "3D"): {
        "B_initial": -0.19143,
        "B_limits":  [-0.2027, -0.1802],
        "C_initial": 0.00357,
        "C_limits":  [0, 0.0071],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "10", "3D"): {
        "B_initial": -0.38789,
        "B_limits":  [-0.4268, -0.349],
        "C_initial": 0.09691,
        "C_limits":  [0.075, 0.1189],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "11", "3D"): {
        "B_initial": -0.00925,
        "B_limits":  [-0.0145, -0.004],
        "C_initial": -0.01476,
        "C_limits":  [-0.0165, -0.013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "12", "3D"): {
        "B_initial": -0.05748,
        "B_limits":  [-0.064, -0.051],
        "C_initial": -0.02021,
        "C_limits":  [-0.021, -0.0194],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "13", "3D"): {
        "B_initial": -0.11263,
        "B_limits":  [-0.1197, -0.1056],
        "C_initial": -0.01486,
        "C_limits":  [-0.0164, -0.0133],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "14", "3D"): {
        "B_initial": -0.19021,
        "B_limits":  [-0.2025, -0.1779],
        "C_initial": 0.01048,
        "C_limits":  [0.0052, 0.0157],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "15", "3D"): {
        "B_initial": -0.40188,
        "B_limits":  [-0.4434, -0.3603],
        "C_initial": 0.13328,
        "C_limits":  [0.1065, 0.1601],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "16", "3D"): {
        "B_initial": -0.00745,
        "B_limits":  [-0.0132, -0.0017],
        "C_initial": -0.01253,
        "C_limits":  [-0.0149, -0.0101],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "17", "3D"): {
        "B_initial": -0.05935,
        "B_limits":  [-0.0664, -0.0523],
        "C_initial": -0.02064,
        "C_limits":  [-0.0213, -0.02],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "18", "3D"): {
        "B_initial": -0.1184,
        "B_limits":  [-0.126, -0.1108],
        "C_initial": -0.01196,
        "C_limits":  [-0.0141, -0.0098],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "19", "3D"): {
        "B_initial": -0.20089,
        "B_limits":  [-0.214, -0.1877],
        "C_initial": 0.02137,
        "C_limits":  [0.0147, 0.028],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "21", "3D"): {
        "B_initial": -0.01163,
        "B_limits":  [-0.0182, -0.0051],
        "C_initial": -0.00813,
        "C_limits":  [-0.0112, -0.0051],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "22", "3D"): {
        "B_initial": -0.06782,
        "B_limits":  [-0.0755, -0.0602],
        "C_initial": -0.01748,
        "C_limits":  [-0.0186, -0.0164],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "23", "3D"): {
        "B_initial": -0.13076,
        "B_limits":  [-0.139, -0.1225],
        "C_initial": -0.0054,
        "C_limits":  [-0.0083, -0.0025],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "24", "3D"): {
        "B_initial": -0.21772,
        "B_limits":  [-0.2316, -0.2038],
        "C_initial": 0.03514,
        "C_limits":  [0.0273, 0.043],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "26", "3D"): {
        "B_initial": -0.02044,
        "B_limits":  [-0.0279, -0.013],
        "C_initial": -0.00151,
        "C_limits":  [-0.0052, 0.0021],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "27", "3D"): {
        "B_initial": -0.08156,
        "B_limits":  [-0.09, -0.0732],
        "C_initial": -0.01119,
        "C_limits":  [-0.013, -0.0094],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "28", "3D"): {
        "B_initial": -0.1486,
        "B_limits":  [-0.1575, -0.1397],
        "C_initial": 0.00444,
        "C_limits":  [0.0007, 0.0081],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "1", "3D"): {
        "B_initial": -0.04607,
        "B_limits":  [-0.0543, -0.0378],
        "C_initial": -0.02022,
        "C_limits":  [-0.0271, -0.0134],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "2", "3D"): {
        "B_initial": -0.09732,
        "B_limits":  [-0.1051, -0.0895],
        "C_initial": -0.00137,
        "C_limits":  [-0.0038, 0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "3", "3D"): {
        "B_initial": -0.14447,
        "B_limits":  [-0.1525, -0.1364],
        "C_initial": 0.00135,
        "C_limits":  [-0.001, 0.0037],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "4", "3D"): {
        "B_initial": -0.19736,
        "B_limits":  [-0.2064, -0.1883],
        "C_initial": 0.00204,
        "C_limits":  [-0.0005, 0.0046],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "5", "3D"): {
        "B_initial": -0.27204,
        "B_limits":  [-0.2847, -0.2594],
        "C_initial": 0.00907,
        "C_limits":  [0.006, 0.0122],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "6", "3D"): {
        "B_initial": -0.42555,
        "B_limits":  [-0.4536, -0.3975],
        "C_initial": 0.05965,
        "C_limits":  [0.0469, 0.0724],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "7", "3D"): {
        "B_initial": -0.0239,
        "B_limits":  [-0.029, -0.0188],
        "C_initial": -0.00747,
        "C_limits":  [-0.0091, -0.0058],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "8", "3D"): {
        "B_initial": -0.06399,
        "B_limits":  [-0.0699, -0.0581],
        "C_initial": -0.00976,
        "C_limits":  [-0.0119, -0.0076],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "9", "3D"): {
        "B_initial": -0.10804,
        "B_limits":  [-0.1146, -0.1014],
        "C_initial": -0.01246,
        "C_limits":  [-0.015, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "10", "3D"): {
        "B_initial": -0.16182,
        "B_limits":  [-0.1701, -0.1536],
        "C_initial": -0.00984,
        "C_limits":  [-0.0125, -0.0072],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "11", "3D"): {
        "B_initial": -0.24283,
        "B_limits":  [-0.2558, -0.2299],
        "C_initial": 0.00798,
        "C_limits":  [0.0033, 0.0127],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "12", "3D"): {
        "B_initial": -0.41716,
        "B_limits":  [-0.4484, -0.386],
        "C_initial": 0.08697,
        "C_limits":  [0.0696, 0.1043],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "13", "3D"): {
        "B_initial": -0.01344,
        "B_limits":  [-0.0172, -0.0097],
        "C_initial": -0.00838,
        "C_limits":  [-0.0105, -0.0062],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "14", "3D"): {
        "B_initial": -0.04885,
        "B_limits":  [-0.0537, -0.044],
        "C_initial": -0.01933,
        "C_limits":  [-0.0206, -0.018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "15", "3D"): {
        "B_initial": -0.09167,
        "B_limits":  [-0.0975, -0.0859],
        "C_initial": -0.02194,
        "C_limits":  [-0.0235, -0.0204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "16", "3D"): {
        "B_initial": -0.14586,
        "B_limits":  [-0.1536, -0.1381],
        "C_initial": -0.01466,
        "C_limits":  [-0.0173, -0.012],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "17", "3D"): {
        "B_initial": -0.22943,
        "B_limits":  [-0.2425, -0.2163],
        "C_initial": 0.01403,
        "C_limits":  [0.0076, 0.0204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "18", "3D"): {
        "B_initial": -0.41146,
        "B_limits":  [-0.4441, -0.3788],
        "C_initial": 0.11662,
        "C_limits":  [0.0954, 0.1378],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "19", "3D"): {
        "B_initial": -0.01299,
        "B_limits":  [-0.0166, -0.0094],
        "C_initial": -0.00671,
        "C_limits":  [-0.0098, -0.0036],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "20", "3D"): {
        "B_initial": -0.04704,
        "B_limits":  [-0.0519, -0.0422],
        "C_initial": -0.02163,
        "C_limits":  [-0.0227, -0.0206],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "21", "3D"): {
        "B_initial": -0.08995,
        "B_limits":  [-0.0959, -0.084],
        "C_initial": -0.02274,
        "C_limits":  [-0.024, -0.0215],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "22", "3D"): {
        "B_initial": -0.145,
        "B_limits":  [-0.153, -0.137],
        "C_initial": -0.01089,
        "C_limits":  [-0.014, -0.0078],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "23", "3D"): {
        "B_initial": -0.23047,
        "B_limits":  [-0.2441, -0.2169],
        "C_initial": 0.02684,
        "C_limits":  [0.0191, 0.0345],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "25", "3D"): {
        "B_initial": -0.0177,
        "B_limits":  [-0.0214, -0.014],
        "C_initial": -0.00268,
        "C_limits":  [-0.0065, 0.0012],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "26", "3D"): {
        "B_initial": -0.05194,
        "B_limits":  [-0.057, -0.0469],
        "C_initial": -0.01949,
        "C_limits":  [-0.0208, -0.0182],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "27", "3D"): {
        "B_initial": -0.09561,
        "B_limits":  [-0.1018, -0.0894],
        "C_initial": -0.01869,
        "C_limits":  [-0.0203, -0.0171],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "28", "3D"): {
        "B_initial": -0.15178,
        "B_limits":  [-0.1602, -0.1433],
        "C_initial": -0.00267,
        "C_limits":  [-0.0063, 0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "29", "3D"): {
        "B_initial": -0.23896,
        "B_limits":  [-0.2531, -0.2249],
        "C_initial": 0.0427,
        "C_limits":  [0.0339, 0.0515],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "31", "3D"): {
        "B_initial": -0.02631,
        "B_limits":  [-0.0305, -0.0221],
        "C_initial": 0.00371,
        "C_limits":  [-0.0008, 0.0082],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "32", "3D"): {
        "B_initial": -0.06176,
        "B_limits":  [-0.0672, -0.0563],
        "C_initial": -0.01396,
        "C_limits":  [-0.0158, -0.0121],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "33", "3D"): {
        "B_initial": -0.10668,
        "B_limits":  [-0.1134, -0.1],
        "C_initial": -0.01089,
        "C_limits":  [-0.0132, -0.0086],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "34", "3D"): {
        "B_initial": -0.16429,
        "B_limits":  [-0.1733, -0.1553],
        "C_initial": 0.00938,
        "C_limits":  [0.005, 0.0138],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "1", "3D"): {
        "B_initial": -0.03599,
        "B_limits":  [-0.0446, -0.0274],
        "C_initial": -0.00466,
        "C_limits":  [-0.008, -0.0013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "2", "3D"): {
        "B_initial": -0.09892,
        "B_limits":  [-0.1076, -0.0902],
        "C_initial": -0.00272,
        "C_limits":  [-0.0066, 0.0011],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "3", "3D"): {
        "B_initial": -0.16092,
        "B_limits":  [-0.1716, -0.1502],
        "C_initial": -0.00799,
        "C_limits":  [-0.0136, -0.0024],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "4", "3D"): {
        "B_initial": -0.24209,
        "B_limits":  [-0.2567, -0.2275],
        "C_initial": -0.01092,
        "C_limits":  [-0.0178, -0.0041],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "6", "3D"): {
        "B_initial": -0.02311,
        "B_limits":  [-0.0282, -0.018],
        "C_initial": -0.00429,
        "C_limits":  [-0.0072, -0.0014],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "7", "3D"): {
        "B_initial": -0.06678,
        "B_limits":  [-0.0731, -0.0605],
        "C_initial": -0.02054,
        "C_limits":  [-0.0242, -0.0169],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "8", "3D"): {
        "B_initial": -0.11871,
        "B_limits":  [-0.1268, -0.1106],
        "C_initial": -0.03078,
        "C_limits":  [-0.0357, -0.0259],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "9", "3D"): {
        "B_initial": -0.19264,
        "B_limits":  [-0.2046, -0.1806],
        "C_initial": -0.03205,
        "C_limits":  [-0.0385, -0.0256],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "10", "3D"): {
        "B_initial": -0.34277,
        "B_limits":  [-0.3695, -0.3161],
        "C_initial": 0.00702,
        "C_limits":  [-0.0067, 0.0207],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "11", "3D"): {
        "B_initial": -0.016,
        "B_limits":  [-0.0192, -0.0128],
        "C_initial": -0.00543,
        "C_limits":  [-0.0098, -0.0011],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "12", "3D"): {
        "B_initial": -0.04874,
        "B_limits":  [-0.0539, -0.0436],
        "C_initial": -0.02954,
        "C_limits":  [-0.0325, -0.0265],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "13", "3D"): {
        "B_initial": -0.09468,
        "B_limits":  [-0.1017, -0.0877],
        "C_initial": -0.03948,
        "C_limits":  [-0.0435, -0.0355],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "14", "3D"): {
        "B_initial": -0.16386,
        "B_limits":  [-0.1749, -0.1528],
        "C_initial": -0.03534,
        "C_limits":  [-0.0415, -0.0291],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "15", "3D"): {
        "B_initial": -0.31084,
        "B_limits":  [-0.3372, -0.2845],
        "C_initial": 0.01998,
        "C_limits":  [0.0038, 0.0362],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "16", "3D"): {
        "B_initial": -0.01616,
        "B_limits":  [-0.0185, -0.0138],
        "C_initial": -0.00219,
        "C_limits":  [-0.0076, 0.0032],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "17", "3D"): {
        "B_initial": -0.04242,
        "B_limits":  [-0.0472, -0.0377],
        "C_initial": -0.02996,
        "C_limits":  [-0.0325, -0.0274],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "18", "3D"): {
        "B_initial": -0.08478,
        "B_limits":  [-0.0916, -0.078],
        "C_initial": -0.03785,
        "C_limits":  [-0.0412, -0.0345],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "19", "3D"): {
        "B_initial": -0.15102,
        "B_limits":  [-0.1619, -0.1401],
        "C_initial": -0.02751,
        "C_limits":  [-0.0336, -0.0214],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "21", "3D"): {
        "B_initial": -0.02216,
        "B_limits":  [-0.0247, -0.0196],
        "C_initial": 0.0051,
        "C_limits":  [-0.001, 0.0112],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "22", "3D"): {
        "B_initial": -0.04515,
        "B_limits":  [-0.0502, -0.0401],
        "C_initial": -0.02376,
        "C_limits":  [-0.0263, -0.0212],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "23", "3D"): {
        "B_initial": -0.08573,
        "B_limits":  [-0.093, -0.0785],
        "C_initial": -0.02881,
        "C_limits":  [-0.032, -0.0257],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "24", "3D"): {
        "B_initial": -0.15047,
        "B_limits":  [-0.1619, -0.1391],
        "C_initial": -0.01235,
        "C_limits":  [-0.0187, -0.006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "1", "3D"): {
        "B_initial": -0.04683,
        "B_limits":  [-0.0552, -0.0385],
        "C_initial": -0.02803,
        "C_limits":  [-0.0337, -0.0224],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "2", "3D"): {
        "B_initial": -0.08217,
        "B_limits":  [-0.0907, -0.0736],
        "C_initial": -0.01737,
        "C_limits":  [-0.0194, -0.0153],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "3", "3D"): {
        "B_initial": -0.12005,
        "B_limits":  [-0.1289, -0.1112],
        "C_initial": -0.01662,
        "C_limits":  [-0.0186, -0.0147],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "4", "3D"): {
        "B_initial": -0.1662,
        "B_limits":  [-0.1754, -0.157],
        "C_initial": -0.0146,
        "C_limits":  [-0.0169, -0.0123],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "5", "3D"): {
        "B_initial": -0.23471,
        "B_limits":  [-0.2473, -0.2221],
        "C_initial": -0.00271,
        "C_limits":  [-0.0074, 0.002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "6", "3D"): {
        "B_initial": -0.38455,
        "B_limits":  [-0.4123, -0.3568],
        "C_initial": 0.0517,
        "C_limits":  [0.0372, 0.0662],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "7", "3D"): {
        "B_initial": -0.01341,
        "B_limits":  [-0.0181, -0.0087],
        "C_initial": -0.01442,
        "C_limits":  [-0.017, -0.0118],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "8", "3D"): {
        "B_initial": -0.04704,
        "B_limits":  [-0.0525, -0.0416],
        "C_initial": -0.01985,
        "C_limits":  [-0.021, -0.0187],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "9", "3D"): {
        "B_initial": -0.08789,
        "B_limits":  [-0.0948, -0.081],
        "C_initial": -0.01898,
        "C_limits":  [-0.0201, -0.0179],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "10", "3D"): {
        "B_initial": -0.13974,
        "B_limits":  [-0.1482, -0.1313],
        "C_initial": -0.00897,
        "C_limits":  [-0.0117, -0.0063],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "11", "3D"): {
        "B_initial": -0.21796,
        "B_limits":  [-0.2316, -0.2043],
        "C_initial": 0.0204,
        "C_limits":  [0.0135, 0.0272],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "12", "3D"): {
        "B_initial": -0.3864,
        "B_limits":  [-0.4174, -0.3554],
        "C_initial": 0.1085,
        "C_limits":  [0.0896, 0.1274],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "13", "3D"): {
        "B_initial": -0.00189,
        "B_limits":  [-0.0068, 0.003],
        "C_initial": -0.00644,
        "C_limits":  [-0.0102, -0.0026],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "14", "3D"): {
        "B_initial": -0.04009,
        "B_limits":  [-0.0458, -0.0344],
        "C_initial": -0.0157,
        "C_limits":  [-0.0179, -0.0135],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "15", "3D"): {
        "B_initial": -0.0856,
        "B_limits":  [-0.0931, -0.0781],
        "C_initial": -0.01105,
        "C_limits":  [-0.0135, -0.0086],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "16", "3D"): {
        "B_initial": -0.14263,
        "B_limits":  [-0.152, -0.1333],
        "C_initial": 0.00694,
        "C_limits":  [0.0029, 0.011],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "17", "3D"): {
        "B_initial": -0.22713,
        "B_limits":  [-0.2421, -0.2121],
        "C_initial": 0.04985,
        "C_limits":  [0.0411, 0.0586],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "19", "3D"): {
        "B_initial": -0.00165,
        "B_limits":  [-0.0077, 0.0044],
        "C_initial": 0.00334,
        "C_limits":  [-0.0012, 0.0079],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "20", "3D"): {
        "B_initial": -0.04514,
        "B_limits":  [-0.0517, -0.0386],
        "C_initial": -0.00661,
        "C_limits":  [-0.0097, -0.0035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "21", "3D"): {
        "B_initial": -0.09501,
        "B_limits":  [-0.1033, -0.0867],
        "C_initial": 0.00158,
        "C_limits":  [-0.0018, 0.0049],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "22", "3D"): {
        "B_initial": -0.15637,
        "B_limits":  [-0.1666, -0.1462],
        "C_initial": 0.02561,
        "C_limits":  [0.0209, 0.0304],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "25", "3D"): {
        "B_initial": -0.00626,
        "B_limits":  [-0.0134, 0.0009],
        "C_initial": 0.01407,
        "C_limits":  [0.0088, 0.0193],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "26", "3D"): {
        "B_initial": -0.05506,
        "B_limits":  [-0.0624, -0.0477],
        "C_initial": 0.00454,
        "C_limits":  [0.0005, 0.0086],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "27", "3D"): {
        "B_initial": -0.10898,
        "B_limits":  [-0.1181, -0.0998],
        "C_initial": 0.01594,
        "C_limits":  [0.0115, 0.0204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "1", "3D"): {
        "B_initial": -0.02713,
        "B_limits":  [-0.0324, -0.0219],
        "C_initial": -0.01247,
        "C_limits":  [-0.0164, -0.0085],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "2", "3D"): {
        "B_initial": -0.0631,
        "B_limits":  [-0.0692, -0.057],
        "C_initial": -0.01131,
        "C_limits":  [-0.0133, -0.0094],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "3", "3D"): {
        "B_initial": -0.10355,
        "B_limits":  [-0.1114, -0.0957],
        "C_initial": -0.0158,
        "C_limits":  [-0.0192, -0.0124],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "4", "3D"): {
        "B_initial": -0.14886,
        "B_limits":  [-0.1577, -0.14],
        "C_initial": -0.02001,
        "C_limits":  [-0.0246, -0.0154],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "5", "3D"): {
        "B_initial": -0.20386,
        "B_limits":  [-0.2151, -0.1926],
        "C_initial": -0.02072,
        "C_limits":  [-0.0264, -0.0151],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "6", "3D"): {
        "B_initial": -0.30413,
        "B_limits":  [-0.3235, -0.2848],
        "C_initial": -0.00613,
        "C_limits":  [-0.0148, 0.0025],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "7", "3D"): {
        "B_initial": -0.01599,
        "B_limits":  [-0.0188, -0.0131],
        "C_initial": -0.00201,
        "C_limits":  [-0.0052, 0.0012],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "8", "3D"): {
        "B_initial": -0.03945,
        "B_limits":  [-0.0435, -0.0354],
        "C_initial": -0.01612,
        "C_limits":  [-0.0178, -0.0144],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "9", "3D"): {
        "B_initial": -0.07274,
        "B_limits":  [-0.0783, -0.0672],
        "C_initial": -0.025,
        "C_limits":  [-0.0272, -0.0227],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "10", "3D"): {
        "B_initial": -0.11317,
        "B_limits":  [-0.1195, -0.1069],
        "C_initial": -0.02838,
        "C_limits":  [-0.0319, -0.0249],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "11", "3D"): {
        "B_initial": -0.16497,
        "B_limits":  [-0.1737, -0.1562],
        "C_initial": -0.02357,
        "C_limits":  [-0.029, -0.0181],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "12", "3D"): {
        "B_initial": -0.26376,
        "B_limits":  [-0.2816, -0.2459],
        "C_initial": 0.00564,
        "C_limits":  [-0.0054, 0.0166],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "13", "3D"): {
        "B_initial": -0.00985,
        "B_limits":  [-0.0122, -0.0075],
        "C_initial": 0.00496,
        "C_limits":  [0.0006, 0.0093],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "14", "3D"): {
        "B_initial": -0.03047,
        "B_limits":  [-0.034, -0.0269],
        "C_initial": -0.01335,
        "C_limits":  [-0.0156, -0.0111],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "15", "3D"): {
        "B_initial": -0.06243,
        "B_limits":  [-0.0675, -0.0573],
        "C_initial": -0.02133,
        "C_limits":  [-0.0233, -0.0194],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "16", "3D"): {
        "B_initial": -0.10214,
        "B_limits":  [-0.1081, -0.0962],
        "C_initial": -0.02121,
        "C_limits":  [-0.0242, -0.0182],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "17", "3D"): {
        "B_initial": -0.15364,
        "B_limits":  [-0.1623, -0.145],
        "C_initial": -0.01029,
        "C_limits":  [-0.0155, -0.0051],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "18", "3D"): {
        "B_initial": -0.25248,
        "B_limits":  [-0.2706, -0.2343],
        "C_initial": 0.03126,
        "C_limits":  [0.0192, 0.0433],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "19", "3D"): {
        "B_initial": -0.01009,
        "B_limits":  [-0.0128, -0.0074],
        "C_initial": 0.0146,
        "C_limits":  [0.0094, 0.0198],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "20", "3D"): {
        "B_initial": -0.03084,
        "B_limits":  [-0.0347, -0.027],
        "C_initial": -0.00497,
        "C_limits":  [-0.0081, -0.0018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "21", "3D"): {
        "B_initial": -0.06329,
        "B_limits":  [-0.0688, -0.0578],
        "C_initial": -0.01103,
        "C_limits":  [-0.0136, -0.0084],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "22", "3D"): {
        "B_initial": -0.10364,
        "B_limits":  [-0.1102, -0.0971],
        "C_initial": -0.00728,
        "C_limits":  [-0.0105, -0.0041],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "23", "3D"): {
        "B_initial": -0.15587,
        "B_limits":  [-0.1652, -0.1465],
        "C_initial": 0.00908,
        "C_limits":  [0.0037, 0.0145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "25", "3D"): {
        "B_initial": -0.01416,
        "B_limits":  [-0.0174, -0.0109],
        "C_initial": 0.02637,
        "C_limits":  [0.0204, 0.0323],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "26", "3D"): {
        "B_initial": -0.03639,
        "B_limits":  [-0.0408, -0.032],
        "C_initial": 0.00677,
        "C_limits":  [0.0028, 0.0108],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "27", "3D"): {
        "B_initial": -0.07019,
        "B_limits":  [-0.0764, -0.064],
        "C_initial": 0.00304,
        "C_limits":  [-0.0003, 0.0064],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "28", "3D"): {
        "B_initial": -0.11181,
        "B_limits":  [-0.1191, -0.1045],
        "C_initial": 0.01044,
        "C_limits":  [0.0068, 0.0141],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "1", "3D", "RC"): {
        "B_initial": -0.05789,
        "B_limits":  [-0.075, -0.0408],
        "C_initial": -0.01465,
        "C_limits":  [-0.0254, -0.0039],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "2", "3D", "RC"): {
        "B_initial": -0.09547,
        "B_limits":  [-0.1122, -0.0787],
        "C_initial": 0.0049,
        "C_limits":  [0.0004, 0.0094],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "3", "3D", "RC"): {
        "B_initial": -0.12305,
        "B_limits":  [-0.1383, -0.1078],
        "C_initial": 0.00218,
        "C_limits":  [-0.0016, 0.006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "4", "3D", "RC"): {
        "B_initial": -0.15349,
        "B_limits":  [-0.1662, -0.1408],
        "C_initial": -0.00478,
        "C_limits":  [-0.0089, -0.0007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "5", "3D", "RC"): {
        "B_initial": -0.19192,
        "B_limits":  [-0.2019, -0.1819],
        "C_initial": -0.00844,
        "C_limits":  [-0.0146, -0.0023],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "6", "3D", "RC"): {
        "B_initial": -0.24557,
        "B_limits":  [-0.2544, -0.2368],
        "C_initial": 0.00035,
        "C_limits":  [-0.0102, 0.0109],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "7", "3D", "RC"): {
        "B_initial": -0.36735,
        "B_limits":  [-0.3909, -0.3438],
        "C_initial": 0.06145,
        "C_limits":  [0.0386, 0.0843],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "8", "3D", "RC"): {
        "B_initial": 0.01228,
        "B_limits":  [0.0071, 0.0174],
        "C_initial": 0.00492,
        "C_limits":  [0.003, 0.0068],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "9", "3D", "RC"): {
        "B_initial": -0.02296,
        "B_limits":  [-0.0274, -0.0185],
        "C_initial": -0.00303,
        "C_limits":  [-0.0057, -0.0004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "10", "3D", "RC"): {
        "B_initial": -0.05894,
        "B_limits":  [-0.0642, -0.0536],
        "C_initial": -0.00783,
        "C_limits":  [-0.01, -0.0056],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "11", "3D", "RC"): {
        "B_initial": -0.10394,
        "B_limits":  [-0.1103, -0.0976],
        "C_initial": -0.00427,
        "C_limits":  [-0.006, -0.0025],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "12", "3D", "RC"): {
        "B_initial": -0.16225,
        "B_limits":  [-0.1708, -0.1537],
        "C_initial": 0.01409,
        "C_limits":  [0.0101, 0.0181],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "13", "3D", "RC"): {
        "B_initial": -0.24008,
        "B_limits":  [-0.2514, -0.2287],
        "C_initial": 0.05528,
        "C_limits":  [0.047, 0.0635],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "14", "3D", "RC"): {
        "B_initial": -0.3962,
        "B_limits":  [-0.4246, -0.3678],
        "C_initial": 0.17041,
        "C_limits":  [0.1463, 0.1945],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "15", "3D", "RC"): {
        "B_initial": 0.01619,
        "B_limits":  [0.0111, 0.0212],
        "C_initial": -2e-05,
        "C_limits":  [-0.003, 0.0029],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "16", "3D", "RC"): {
        "B_initial": -0.02007,
        "B_limits":  [-0.0245, -0.0157],
        "C_initial": -0.01524,
        "C_limits":  [-0.017, -0.0135],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "17", "3D", "RC"): {
        "B_initial": -0.06022,
        "B_limits":  [-0.066, -0.0544],
        "C_initial": -0.01673,
        "C_limits":  [-0.0182, -0.0153],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "18", "3D", "RC"): {
        "B_initial": -0.11125,
        "B_limits":  [-0.1186, -0.1039],
        "C_initial": -0.00403,
        "C_limits":  [-0.0069, -0.0011],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "19", "3D", "RC"): {
        "B_initial": -0.17702,
        "B_limits":  [-0.1868, -0.1673],
        "C_initial": 0.02887,
        "C_limits":  [0.0229, 0.0348],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "20", "3D", "RC"): {
        "B_initial": -0.26313,
        "B_limits":  [-0.2757, -0.2505],
        "C_initial": 0.08953,
        "C_limits":  [0.0794, 0.0996],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "22", "3D", "RC"): {
        "B_initial": 0.0083,
        "B_limits":  [0.0027, 0.0139],
        "C_initial": -0.00114,
        "C_limits":  [-0.0049, 0.0027],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "23", "3D", "RC"): {
        "B_initial": -0.02981,
        "B_limits":  [-0.0347, -0.0249],
        "C_initial": -0.01922,
        "C_limits":  [-0.0206, -0.0178],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "24", "3D", "RC"): {
        "B_initial": -0.07303,
        "B_limits":  [-0.0793, -0.0667],
        "C_initial": -0.01763,
        "C_limits":  [-0.0193, -0.0159],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "25", "3D", "RC"): {
        "B_initial": -0.12797,
        "B_limits":  [-0.1358, -0.1201],
        "C_initial": 0.00158,
        "C_limits":  [-0.0022, 0.0054],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "26", "3D", "RC"): {
        "B_initial": -0.19822,
        "B_limits":  [-0.2085, -0.1879],
        "C_initial": 0.0442,
        "C_limits":  [0.037, 0.0514],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "29", "3D", "RC"): {
        "B_initial": -0.00214,
        "B_limits":  [-0.0083, 0.004],
        "C_initial": -0.00028,
        "C_limits":  [-0.0046, 0.0041],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "30", "3D", "RC"): {
        "B_initial": -0.04217,
        "B_limits":  [-0.0474, -0.0369],
        "C_initial": -0.01972,
        "C_limits":  [-0.021, -0.0185],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "31", "3D", "RC"): {
        "B_initial": -0.08787,
        "B_limits":  [-0.0945, -0.0812],
        "C_initial": -0.0155,
        "C_limits":  [-0.0175, -0.0135],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "32", "3D", "RC"): {
        "B_initial": -0.14576,
        "B_limits":  [-0.154, -0.1376],
        "C_initial": 0.00874,
        "C_limits":  [0.0042, 0.0132],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "1", "3D", "RC"): {
        "B_initial": -0.06701,
        "B_limits":  [-0.08, -0.054],
        "C_initial": -0.01465,
        "C_limits":  [-0.0269, -0.0024],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "2", "3D", "RC"): {
        "B_initial": -0.11364,
        "B_limits":  [-0.1259, -0.1014],
        "C_initial": 0.01377,
        "C_limits":  [0.0095, 0.018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "3", "3D", "RC"): {
        "B_initial": -0.14574,
        "B_limits":  [-0.1574, -0.1341],
        "C_initial": 0.01214,
        "C_limits":  [0.0086, 0.0157],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "4", "3D", "RC"): {
        "B_initial": -0.17888,
        "B_limits":  [-0.1892, -0.1685],
        "C_initial": 0.00615,
        "C_limits":  [0.0025, 0.0098],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "5", "3D", "RC"): {
        "B_initial": -0.22358,
        "B_limits":  [-0.2339, -0.2133],
        "C_initial": 0.00296,
        "C_limits":  [-0.0016, 0.0075],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "6", "3D", "RC"): {
        "B_initial": -0.33007,
        "B_limits":  [-0.3507, -0.3094],
        "C_initial": 0.03574,
        "C_limits":  [0.0229, 0.0485],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "7", "3D", "RC"): {
        "B_initial": -0.01051,
        "B_limits":  [-0.0166, -0.0045],
        "C_initial": 0.00843,
        "C_limits":  [0.0061, 0.0108],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "8", "3D", "RC"): {
        "B_initial": -0.0472,
        "B_limits":  [-0.0529, -0.0415],
        "C_initial": 0.00589,
        "C_limits":  [0.0026, 0.0091],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "9", "3D", "RC"): {
        "B_initial": -0.08265,
        "B_limits":  [-0.089, -0.0763],
        "C_initial": -3e-05,
        "C_limits":  [-0.003, 0.003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "10", "3D", "RC"): {
        "B_initial": -0.12408,
        "B_limits":  [-0.1305, -0.1176],
        "C_initial": -0.00077,
        "C_limits":  [-0.0028, 0.0012],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "11", "3D", "RC"): {
        "B_initial": -0.1831,
        "B_limits":  [-0.1929, -0.1733],
        "C_initial": 0.01188,
        "C_limits":  [0.0087, 0.0151],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "12", "3D", "RC"): {
        "B_initial": -0.3186,
        "B_limits":  [-0.3432, -0.294],
        "C_initial": 0.08497,
        "C_limits":  [0.0679, 0.102],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "13", "3D", "RC"): {
        "B_initial": 0.00371,
        "B_limits":  [-0.0002, 0.0077],
        "C_initial": 0.00052,
        "C_limits":  [-0.0021, 0.0032],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "14", "3D", "RC"): {
        "B_initial": -0.02787,
        "B_limits":  [-0.0318, -0.024],
        "C_initial": -0.0132,
        "C_limits":  [-0.0154, -0.011],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "15", "3D", "RC"): {
        "B_initial": -0.06453,
        "B_limits":  [-0.0698, -0.0593],
        "C_initial": -0.01644,
        "C_limits":  [-0.0182, -0.0147],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "16", "3D", "RC"): {
        "B_initial": -0.10936,
        "B_limits":  [-0.1152, -0.1035],
        "C_initial": -0.00903,
        "C_limits":  [-0.011, -0.0071],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "17", "3D", "RC"): {
        "B_initial": -0.17422,
        "B_limits":  [-0.1845, -0.164],
        "C_initial": 0.01872,
        "C_limits":  [0.0131, 0.0243],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "18", "3D", "RC"): {
        "B_initial": -0.32066,
        "B_limits":  [-0.3469, -0.2945],
        "C_initial": 0.12486,
        "C_limits":  [0.1028, 0.1469],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "19", "3D", "RC"): {
        "B_initial": 0.00175,
        "B_limits":  [-0.002, 0.0055],
        "C_initial": -0.00459,
        "C_limits":  [-0.0084, -0.0008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "20", "3D", "RC"): {
        "B_initial": -0.02781,
        "B_limits":  [-0.0318, -0.0239],
        "C_initial": -0.02303,
        "C_limits":  [-0.0246, -0.0215],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "21", "3D", "RC"): {
        "B_initial": -0.06567,
        "B_limits":  [-0.0712, -0.0602],
        "C_initial": -0.02272,
        "C_limits":  [-0.0242, -0.0212],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "22", "3D", "RC"): {
        "B_initial": -0.1128,
        "B_limits":  [-0.1191, -0.1065],
        "C_initial": -0.00832,
        "C_limits":  [-0.0112, -0.0055],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "23", "3D", "RC"): {
        "B_initial": -0.18119,
        "B_limits":  [-0.1921, -0.1703],
        "C_initial": 0.03112,
        "C_limits":  [0.0236, 0.0386],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "25", "3D", "RC"): {
        "B_initial": -0.00506,
        "B_limits":  [-0.0088, -0.0013],
        "C_initial": -0.00662,
        "C_limits":  [-0.0112, -0.002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "26", "3D", "RC"): {
        "B_initial": -0.03401,
        "B_limits":  [-0.0381, -0.0299],
        "C_initial": -0.02714,
        "C_limits":  [-0.0283, -0.026],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "27", "3D", "RC"): {
        "B_initial": -0.07297,
        "B_limits":  [-0.0787, -0.0672],
        "C_initial": -0.02372,
        "C_limits":  [-0.0255, -0.0219],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "28", "3D", "RC"): {
        "B_initial": -0.12179,
        "B_limits":  [-0.1283, -0.1153],
        "C_initial": -0.00395,
        "C_limits":  [-0.0075, -0.0004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "29", "3D", "RC"): {
        "B_initial": -0.19254,
        "B_limits":  [-0.2038, -0.1813],
        "C_initial": 0.04407,
        "C_limits":  [0.0353, 0.0528],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "31", "3D", "RC"): {
        "B_initial": -0.01559,
        "B_limits":  [-0.0197, -0.0114],
        "C_initial": -0.00665,
        "C_limits":  [-0.0118, -0.0015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "32", "3D", "RC"): {
        "B_initial": -0.04466,
        "B_limits":  [-0.0491, -0.0402],
        "C_initial": -0.02818,
        "C_limits":  [-0.0291, -0.0272],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "33", "3D", "RC"): {
        "B_initial": -0.08486,
        "B_limits":  [-0.091, -0.0787],
        "C_initial": -0.02148,
        "C_limits":  [-0.0237, -0.0192],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "34", "3D", "RC"): {
        "B_initial": -0.13533,
        "B_limits":  [-0.1423, -0.1283],
        "C_initial": 0.00349,
        "C_limits":  [-0.0009, 0.0078],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "1", "3D", "RC"): {
        "B_initial": -0.05982,
        "B_limits":  [-0.0687, -0.0509],
        "C_initial": -0.0076,
        "C_limits":  [-0.0168, 0.0016],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "2", "3D", "RC"): {
        "B_initial": -0.10771,
        "B_limits":  [-0.1169, -0.0985],
        "C_initial": 0.0239,
        "C_limits":  [0.021, 0.0268],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "3", "3D", "RC"): {
        "B_initial": -0.14768,
        "B_limits":  [-0.1576, -0.1378],
        "C_initial": 0.02943,
        "C_limits":  [0.0273, 0.0316],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "4", "3D", "RC"): {
        "B_initial": -0.19083,
        "B_limits":  [-0.2017, -0.1799],
        "C_initial": 0.02693,
        "C_limits":  [0.0243, 0.0296],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "5", "3D", "RC"): {
        "B_initial": -0.23994,
        "B_limits":  [-0.2516, -0.2283],
        "C_initial": 0.02289,
        "C_limits":  [0.0202, 0.0256],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "6", "3D", "RC"): {
        "B_initial": -0.31421,
        "B_limits":  [-0.3302, -0.2983],
        "C_initial": 0.02836,
        "C_limits":  [0.025, 0.0318],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "7", "3D", "RC"): {
        "B_initial": -0.01941,
        "B_limits":  [-0.025, -0.0138],
        "C_initial": 0.00946,
        "C_limits":  [0.0068, 0.0121],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "8", "3D", "RC"): {
        "B_initial": -0.05003,
        "B_limits":  [-0.0574, -0.0427],
        "C_initial": 0.01144,
        "C_limits":  [0.0075, 0.0154],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "9", "3D", "RC"): {
        "B_initial": -0.08403,
        "B_limits":  [-0.0925, -0.0755],
        "C_initial": 0.00572,
        "C_limits":  [0.001, 0.0105],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "10", "3D", "RC"): {
        "B_initial": -0.12655,
        "B_limits":  [-0.1364, -0.1168],
        "C_initial": 0.00094,
        "C_limits":  [-0.0035, 0.0054],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "11", "3D", "RC"): {
        "B_initial": -0.17943,
        "B_limits":  [-0.1901, -0.1688],
        "C_initial": 0.00248,
        "C_limits":  [-0.0008, 0.0058],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "12", "3D", "RC"): {
        "B_initial": -0.26396,
        "B_limits":  [-0.2801, -0.2479],
        "C_initial": 0.02591,
        "C_limits":  [0.0202, 0.0317],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "13", "3D", "RC"): {
        "B_initial": -0.00198,
        "B_limits":  [-0.004, 0],
        "C_initial": 0.00228,
        "C_limits":  [-0.0002, 0.0048],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "14", "3D", "RC"): {
        "B_initial": -0.01964,
        "B_limits":  [-0.023, -0.0163],
        "C_initial": -0.01252,
        "C_limits":  [-0.0154, -0.0097],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "15", "3D", "RC"): {
        "B_initial": -0.04856,
        "B_limits":  [-0.0531, -0.044],
        "C_initial": -0.02146,
        "C_limits":  [-0.0242, -0.0187],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "16", "3D", "RC"): {
        "B_initial": -0.08951,
        "B_limits":  [-0.0959, -0.0831],
        "C_initial": -0.02207,
        "C_limits":  [-0.0244, -0.0197],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "17", "3D", "RC"): {
        "B_initial": -0.14359,
        "B_limits":  [-0.1513, -0.1359],
        "C_initial": -0.00971,
        "C_limits":  [-0.0128, -0.0067],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "18", "3D", "RC"): {
        "B_initial": -0.23294,
        "B_limits":  [-0.248, -0.2179],
        "C_initial": 0.03629,
        "C_limits":  [0.0266, 0.0459],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "19", "3D", "RC"): {
        "B_initial": -0.00351,
        "B_limits":  [-0.0053, -0.0018],
        "C_initial": -0.00262,
        "C_limits":  [-0.0063, 0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "20", "3D", "RC"): {
        "B_initial": -0.0149,
        "B_limits":  [-0.0175, -0.0123],
        "C_initial": -0.0242,
        "C_limits":  [-0.0264, -0.022],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "21", "3D", "RC"): {
        "B_initial": -0.04144,
        "B_limits":  [-0.0454, -0.0375],
        "C_initial": -0.03253,
        "C_limits":  [-0.0342, -0.0309],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "22", "3D", "RC"): {
        "B_initial": -0.08169,
        "B_limits":  [-0.0877, -0.0757],
        "C_initial": -0.02815,
        "C_limits":  [-0.0303, -0.026],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "23", "3D", "RC"): {
        "B_initial": -0.13634,
        "B_limits":  [-0.1438, -0.1289],
        "C_initial": -0.00683,
        "C_limits":  [-0.011, -0.0027],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "24", "3D", "RC"): {
        "B_initial": -0.22775,
        "B_limits":  [-0.2429, -0.2126],
        "C_initial": 0.05565,
        "C_limits":  [0.0434, 0.0679],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "25", "3D", "RC"): {
        "B_initial": -0.01413,
        "B_limits":  [-0.0169, -0.0114],
        "C_initial": -0.00376,
        "C_limits":  [-0.0084, 0.0008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "26", "3D", "RC"): {
        "B_initial": -0.02142,
        "B_limits":  [-0.0242, -0.0186],
        "C_initial": -0.0292,
        "C_limits":  [-0.0311, -0.0273],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "27", "3D", "RC"): {
        "B_initial": -0.04658,
        "B_limits":  [-0.0507, -0.0424],
        "C_initial": -0.03552,
        "C_limits":  [-0.0367, -0.0344],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "28", "3D", "RC"): {
        "B_initial": -0.08666,
        "B_limits":  [-0.0929, -0.0804],
        "C_initial": -0.02541,
        "C_limits":  [-0.0283, -0.0225],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "29", "3D", "RC"): {
        "B_initial": -0.14199,
        "B_limits":  [-0.1498, -0.1342],
        "C_initial": 0.00503,
        "C_limits":  [-0.0006, 0.0107],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "1", "3D", "RC"): {
        "B_initial": -0.06839,
        "B_limits":  [-0.0777, -0.0591],
        "C_initial": 0.00255,
        "C_limits":  [-0.0041, 0.0092],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "2", "3D", "RC"): {
        "B_initial": -0.12611,
        "B_limits":  [-0.1351, -0.1172],
        "C_initial": 0.02831,
        "C_limits":  [0.0263, 0.0304],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "3", "3D", "RC"): {
        "B_initial": -0.17699,
        "B_limits":  [-0.1876, -0.1664],
        "C_initial": 0.03229,
        "C_limits":  [0.0293, 0.0353],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "4", "3D", "RC"): {
        "B_initial": -0.23583,
        "B_limits":  [-0.2487, -0.223],
        "C_initial": 0.02986,
        "C_limits":  [0.0259, 0.0338],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "5", "3D", "RC"): {
        "B_initial": -0.31234,
        "B_limits":  [-0.3287, -0.296],
        "C_initial": 0.02646,
        "C_limits":  [0.0223, 0.0307],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "7", "3D", "RC"): {
        "B_initial": -0.04073,
        "B_limits":  [-0.0471, -0.0344],
        "C_initial": 0.01046,
        "C_limits":  [0.0079, 0.013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "8", "3D", "RC"): {
        "B_initial": -0.08209,
        "B_limits":  [-0.0893, -0.0749],
        "C_initial": 0.01472,
        "C_limits":  [0.0115, 0.0179],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "9", "3D", "RC"): {
        "B_initial": -0.12517,
        "B_limits":  [-0.134, -0.1163],
        "C_initial": 0.00902,
        "C_limits":  [0.0047, 0.0133],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "10", "3D", "RC"): {
        "B_initial": -0.17933,
        "B_limits":  [-0.1903, -0.1683],
        "C_initial": 0.00183,
        "C_limits":  [-0.0029, 0.0066],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "11", "3D", "RC"): {
        "B_initial": -0.25433,
        "B_limits":  [-0.2689, -0.2397],
        "C_initial": -0.00067,
        "C_limits":  [-0.0053, 0.004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "12", "3D", "RC"): {
        "B_initial": -0.38868,
        "B_limits":  [-0.4136, -0.3638],
        "C_initial": 0.0297,
        "C_limits":  [0.0208, 0.0386],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "13", "3D", "RC"): {
        "B_initial": -0.02091,
        "B_limits":  [-0.0247, -0.0171],
        "C_initial": 0.00587,
        "C_limits":  [0.0039, 0.0079],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "14", "3D", "RC"): {
        "B_initial": -0.04877,
        "B_limits":  [-0.054, -0.0436],
        "C_initial": -0.00391,
        "C_limits":  [-0.0074, -0.0004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "15", "3D", "RC"): {
        "B_initial": -0.08502,
        "B_limits":  [-0.0919, -0.0782],
        "C_initial": -0.01447,
        "C_limits":  [-0.0187, -0.0103],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "16", "3D", "RC"): {
        "B_initial": -0.1346,
        "B_limits":  [-0.1436, -0.1256],
        "C_initial": -0.02214,
        "C_limits":  [-0.0266, -0.0177],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "17", "3D", "RC"): {
        "B_initial": -0.20714,
        "B_limits":  [-0.2199, -0.1944],
        "C_initial": -0.01966,
        "C_limits":  [-0.0243, -0.015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "18", "3D", "RC"): {
        "B_initial": -0.34226,
        "B_limits":  [-0.3661, -0.3184],
        "C_initial": 0.02728,
        "C_limits":  [0.0153, 0.0392],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "19", "3D", "RC"): {
        "B_initial": -0.01012,
        "B_limits":  [-0.0121, -0.0082],
        "C_initial": 0.00021,
        "C_limits":  [-0.0028, 0.0032],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "20", "3D", "RC"): {
        "B_initial": -0.02796,
        "B_limits":  [-0.0316, -0.0243],
        "C_initial": -0.01833,
        "C_limits":  [-0.0216, -0.015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "21", "3D", "RC"): {
        "B_initial": -0.05902,
        "B_limits":  [-0.0643, -0.0538],
        "C_initial": -0.0309,
        "C_limits":  [-0.0346, -0.0272],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "22", "3D", "RC"): {
        "B_initial": -0.10498,
        "B_limits":  [-0.1124, -0.0976],
        "C_initial": -0.037,
        "C_limits":  [-0.0409, -0.0331],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "23", "3D", "RC"): {
        "B_initial": -0.17527,
        "B_limits":  [-0.1866, -0.1639],
        "C_initial": -0.02832,
        "C_limits":  [-0.0333, -0.0234],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "24", "3D", "RC"): {
        "B_initial": -0.31003,
        "B_limits":  [-0.3331, -0.287],
        "C_initial": 0.03489,
        "C_limits":  [0.0202, 0.0496],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "25", "3D", "RC"): {
        "B_initial": -0.00581,
        "B_limits":  [-0.0073, -0.0043],
        "C_initial": -0.0039,
        "C_limits":  [-0.008, 0.0002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "26", "3D", "RC"): {
        "B_initial": -0.01574,
        "B_limits":  [-0.0186, -0.0128],
        "C_initial": -0.0283,
        "C_limits":  [-0.0315, -0.0251],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "27", "3D", "RC"): {
        "B_initial": -0.04268,
        "B_limits":  [-0.0473, -0.0381],
        "C_initial": -0.0413,
        "C_limits":  [-0.0446, -0.038],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "28", "3D", "RC"): {
        "B_initial": -0.0857,
        "B_limits":  [-0.0924, -0.079],
        "C_initial": -0.04473,
        "C_limits":  [-0.0483, -0.0411],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "29", "3D", "RC"): {
        "B_initial": -0.15405,
        "B_limits":  [-0.1648, -0.1433],
        "C_initial": -0.02919,
        "C_limits":  [-0.0346, -0.0238],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "31", "3D", "RC"): {
        "B_initial": -0.00817,
        "B_limits":  [-0.0108, -0.0055],
        "C_initial": -0.00574,
        "C_limits":  [-0.0109, -0.0005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "32", "3D", "RC"): {
        "B_initial": -0.00958,
        "B_limits":  [-0.0122, -0.007],
        "C_initial": -0.03524,
        "C_limits":  [-0.038, -0.0324],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "33", "3D", "RC"): {
        "B_initial": -0.03207,
        "B_limits":  [-0.0363, -0.0278],
        "C_initial": -0.04722,
        "C_limits":  [-0.0498, -0.0447],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "34", "3D", "RC"): {
        "B_initial": -0.0719,
        "B_limits":  [-0.0783, -0.0655],
        "C_initial": -0.04577,
        "C_limits":  [-0.049, -0.0425],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "35", "3D", "RC"): {
        "B_initial": -0.13806,
        "B_limits":  [-0.1485, -0.1276],
        "C_initial": -0.02008,
        "C_limits":  [-0.0268, -0.0134],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "1", "3D", "RC"): {
        "B_initial": -0.07384,
        "B_limits":  [-0.0876, -0.0601],
        "C_initial": -0.02648,
        "C_limits":  [-0.0377, -0.0152],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "2", "3D", "RC"): {
        "B_initial": -0.11318,
        "B_limits":  [-0.126, -0.1003],
        "C_initial": -7e-05,
        "C_limits":  [-0.0051, 0.005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "3", "3D", "RC"): {
        "B_initial": -0.13893,
        "B_limits":  [-0.1505, -0.1273],
        "C_initial": -0.00051,
        "C_limits":  [-0.0046, 0.0036],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "4", "3D", "RC"): {
        "B_initial": -0.16625,
        "B_limits":  [-0.1762, -0.1563],
        "C_initial": -0.00733,
        "C_limits":  [-0.0117, -0.0029],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "5", "3D", "RC"): {
        "B_initial": -0.20801,
        "B_limits":  [-0.217, -0.199],
        "C_initial": -0.01349,
        "C_limits":  [-0.0193, -0.0077],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "6", "3D", "RC"): {
        "B_initial": -0.34142,
        "B_limits":  [-0.3694, -0.3134],
        "C_initial": 0.0323,
        "C_limits":  [0.0144, 0.0502],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "7", "3D", "RC"): {
        "B_initial": -0.00973,
        "B_limits":  [-0.0165, -0.003],
        "C_initial": 0.0015,
        "C_limits":  [-0.0008, 0.0038],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "8", "3D", "RC"): {
        "B_initial": -0.04634,
        "B_limits":  [-0.0523, -0.0403],
        "C_initial": 0.00381,
        "C_limits":  [0.0017, 0.0059],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "9", "3D", "RC"): {
        "B_initial": -0.0779,
        "B_limits":  [-0.0838, -0.072],
        "C_initial": -0.0011,
        "C_limits":  [-0.0032, 0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "10", "3D", "RC"): {
        "B_initial": -0.11592,
        "B_limits":  [-0.1223, -0.1095],
        "C_initial": -0.00354,
        "C_limits":  [-0.0049, -0.0022],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "11", "3D", "RC"): {
        "B_initial": -0.17598,
        "B_limits":  [-0.1858, -0.1662],
        "C_initial": 0.00587,
        "C_limits":  [0.0029, 0.0088],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "12", "3D", "RC"): {
        "B_initial": -0.34799,
        "B_limits":  [-0.3821, -0.3139],
        "C_initial": 0.09636,
        "C_limits":  [0.0739, 0.1189],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "13", "3D", "RC"): {
        "B_initial": 0.01145,
        "B_limits":  [0.0065, 0.0164],
        "C_initial": -0.00164,
        "C_limits":  [-0.0033, 0],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "14", "3D", "RC"): {
        "B_initial": -0.02445,
        "B_limits":  [-0.0288, -0.0202],
        "C_initial": -0.00973,
        "C_limits":  [-0.0117, -0.0078],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "15", "3D", "RC"): {
        "B_initial": -0.05945,
        "B_limits":  [-0.0643, -0.0546],
        "C_initial": -0.01358,
        "C_limits":  [-0.0152, -0.012],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "16", "3D", "RC"): {
        "B_initial": -0.10325,
        "B_limits":  [-0.1097, -0.0968],
        "C_initial": -0.00913,
        "C_limits":  [-0.0108, -0.0075],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "17", "3D", "RC"): {
        "B_initial": -0.17265,
        "B_limits":  [-0.1838, -0.1615],
        "C_initial": 0.01544,
        "C_limits":  [0.0101, 0.0208],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "18", "3D", "RC"): {
        "B_initial": -0.36217,
        "B_limits":  [-0.399, -0.3253],
        "C_initial": 0.14391,
        "C_limits":  [0.1152, 0.1727],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "19", "3D", "RC"): {
        "B_initial": 0.01423,
        "B_limits":  [0.0092, 0.0192],
        "C_initial": -0.00459,
        "C_limits":  [-0.0073, -0.0019],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "20", "3D", "RC"): {
        "B_initial": -0.02267,
        "B_limits":  [-0.0271, -0.0182],
        "C_initial": -0.01834,
        "C_limits":  [-0.0198, -0.0169],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "21", "3D", "RC"): {
        "B_initial": -0.06092,
        "B_limits":  [-0.0661, -0.0557],
        "C_initial": -0.01966,
        "C_limits":  [-0.0209, -0.0184],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "22", "3D", "RC"): {
        "B_initial": -0.10938,
        "B_limits":  [-0.1166, -0.1022],
        "C_initial": -0.00824,
        "C_limits":  [-0.0109, -0.0056],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "23", "3D", "RC"): {
        "B_initial": -0.18569,
        "B_limits":  [-0.198, -0.1734],
        "C_initial": 0.02996,
        "C_limits":  [0.0224, 0.0375],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "25", "3D", "RC"): {
        "B_initial": 0.00804,
        "B_limits":  [0.0025, 0.0136],
        "C_initial": -0.00492,
        "C_limits":  [-0.0084, -0.0014],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "26", "3D", "RC"): {
        "B_initial": -0.03065,
        "B_limits":  [-0.0355, -0.0258],
        "C_initial": -0.02151,
        "C_limits":  [-0.0227, -0.0204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "27", "3D", "RC"): {
        "B_initial": -0.07175,
        "B_limits":  [-0.0774, -0.0661],
        "C_initial": -0.02012,
        "C_limits":  [-0.0215, -0.0187],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "28", "3D", "RC"): {
        "B_initial": -0.12387,
        "B_limits":  [-0.1316, -0.1161],
        "C_initial": -0.00281,
        "C_limits":  [-0.0063, 0.0007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "29", "3D", "RC"): {
        "B_initial": -0.20526,
        "B_limits":  [-0.2183, -0.1922],
        "C_initial": 0.04625,
        "C_limits":  [0.0371, 0.0554],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "31", "3D", "RC"): {
        "B_initial": -0.00283,
        "B_limits":  [-0.009, 0.0033],
        "C_initial": -0.00306,
        "C_limits":  [-0.0072, 0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "32", "3D", "RC"): {
        "B_initial": -0.04377,
        "B_limits":  [-0.0492, -0.0383],
        "C_initial": -0.0211,
        "C_limits":  [-0.0221, -0.0201],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "33", "3D", "RC"): {
        "B_initial": -0.08757,
        "B_limits":  [-0.0938, -0.0813],
        "C_initial": -0.01696,
        "C_limits":  [-0.0188, -0.0152],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "34", "3D", "RC"): {
        "B_initial": -0.1429,
        "B_limits":  [-0.1512, -0.1346],
        "C_initial": 0.00562,
        "C_limits":  [0.0012, 0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "1", "3D", "RC"): {
        "B_initial": -0.04568,
        "B_limits":  [-0.0573, -0.034],
        "C_initial": -0.01394,
        "C_limits":  [-0.0235, -0.0044],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "2", "3D", "RC"): {
        "B_initial": -0.0873,
        "B_limits":  [-0.0996, -0.075],
        "C_initial": 0.00822,
        "C_limits":  [0.0049, 0.0115],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "3", "3D", "RC"): {
        "B_initial": -0.11967,
        "B_limits":  [-0.1317, -0.1076],
        "C_initial": 0.00841,
        "C_limits":  [0.0052, 0.0116],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "4", "3D", "RC"): {
        "B_initial": -0.1559,
        "B_limits":  [-0.1674, -0.1444],
        "C_initial": 0.00456,
        "C_limits":  [0.0015, 0.0076],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "5", "3D", "RC"): {
        "B_initial": -0.20966,
        "B_limits":  [-0.2215, -0.1978],
        "C_initial": 0.00441,
        "C_limits":  [0.0012, 0.0076],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "6", "3D", "RC"): {
        "B_initial": -0.36377,
        "B_limits":  [-0.3951, -0.3325],
        "C_initial": 0.0681,
        "C_limits":  [0.0483, 0.0879],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "7", "3D", "RC"): {
        "B_initial": 0.00048,
        "B_limits":  [-0.0036, 0.0046],
        "C_initial": 0.00109,
        "C_limits":  [-0.0006, 0.0028],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "8", "3D", "RC"): {
        "B_initial": -0.02951,
        "B_limits":  [-0.0339, -0.0251],
        "C_initial": -0.0055,
        "C_limits":  [-0.0082, -0.0028],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "9", "3D", "RC"): {
        "B_initial": -0.06201,
        "B_limits":  [-0.067, -0.057],
        "C_initial": -0.01124,
        "C_limits":  [-0.0138, -0.0087],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "10", "3D", "RC"): {
        "B_initial": -0.10376,
        "B_limits":  [-0.1101, -0.0974],
        "C_initial": -0.01078,
        "C_limits":  [-0.0127, -0.0089],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "11", "3D", "RC"): {
        "B_initial": -0.16997,
        "B_limits":  [-0.1805, -0.1594],
        "C_initial": 0.00629,
        "C_limits":  [0.0022, 0.0103],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "12", "3D", "RC"): {
        "B_initial": -0.35422,
        "B_limits":  [-0.39, -0.3185],
        "C_initial": 0.12362,
        "C_limits":  [0.0961, 0.1511],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "13", "3D", "RC"): {
        "B_initial": 0.0055,
        "B_limits":  [0.0025, 0.0085],
        "C_initial": -0.00447,
        "C_limits":  [-0.0073, -0.0017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "14", "3D", "RC"): {
        "B_initial": -0.02026,
        "B_limits":  [-0.0238, -0.0167],
        "C_initial": -0.0199,
        "C_limits":  [-0.0218, -0.018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "15", "3D", "RC"): {
        "B_initial": -0.05311,
        "B_limits":  [-0.0576, -0.0486],
        "C_initial": -0.02408,
        "C_limits":  [-0.0255, -0.0226],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "16", "3D", "RC"): {
        "B_initial": -0.09724,
        "B_limits":  [-0.1037, -0.0908],
        "C_initial": -0.01668,
        "C_limits":  [-0.0188, -0.0145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "17", "3D", "RC"): {
        "B_initial": -0.16833,
        "B_limits":  [-0.1796, -0.1571],
        "C_initial": 0.01515,
        "C_limits":  [0.0086, 0.0217],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "19", "3D", "RC"): {
        "B_initial": -0.00146,
        "B_limits":  [-0.0047, 0.0017],
        "C_initial": -0.0065,
        "C_limits":  [-0.0104, -0.0026],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "20", "3D", "RC"): {
        "B_initial": -0.0256,
        "B_limits":  [-0.0294, -0.0218],
        "C_initial": -0.02613,
        "C_limits":  [-0.0274, -0.0248],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "21", "3D", "RC"): {
        "B_initial": -0.05937,
        "B_limits":  [-0.0643, -0.0545],
        "C_initial": -0.02762,
        "C_limits":  [-0.0288, -0.0265],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "22", "3D", "RC"): {
        "B_initial": -0.1056,
        "B_limits":  [-0.1125, -0.0987],
        "C_initial": -0.01367,
        "C_limits":  [-0.0168, -0.0106],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "23", "3D", "RC"): {
        "B_initial": -0.18025,
        "B_limits":  [-0.1922, -0.1683],
        "C_initial": 0.03062,
        "C_limits":  [0.0221, 0.0392],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "25", "3D", "RC"): {
        "B_initial": -0.01556,
        "B_limits":  [-0.0194, -0.0117],
        "C_initial": -0.00498,
        "C_limits":  [-0.0097, -0.0003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "26", "3D", "RC"): {
        "B_initial": -0.03957,
        "B_limits":  [-0.0439, -0.0352],
        "C_initial": -0.02664,
        "C_limits":  [-0.0276, -0.0256],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "27", "3D", "RC"): {
        "B_initial": -0.07471,
        "B_limits":  [-0.0802, -0.0692],
        "C_initial": -0.02483,
        "C_limits":  [-0.0264, -0.0232],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "28", "3D", "RC"): {
        "B_initial": -0.12309,
        "B_limits":  [-0.1307, -0.1155],
        "C_initial": -0.00441,
        "C_limits":  [-0.0086, -0.0002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "1", "3D", "RC"): {
        "B_initial": -0.05117,
        "B_limits":  [-0.0594, -0.0429],
        "C_initial": -0.0101,
        "C_limits":  [-0.0183, -0.0019],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "2", "3D", "RC"): {
        "B_initial": -0.10015,
        "B_limits":  [-0.1076, -0.0927],
        "C_initial": 0.0196,
        "C_limits":  [0.0172, 0.022],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "3", "3D", "RC"): {
        "B_initial": -0.14088,
        "B_limits":  [-0.1493, -0.1325],
        "C_initial": 0.02504,
        "C_limits":  [0.0232, 0.0268],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "4", "3D", "RC"): {
        "B_initial": -0.18738,
        "B_limits":  [-0.1971, -0.1776],
        "C_initial": 0.02322,
        "C_limits":  [0.0209, 0.0255],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "5", "3D", "RC"): {
        "B_initial": -0.24601,
        "B_limits":  [-0.2579, -0.2341],
        "C_initial": 0.01983,
        "C_limits":  [0.0174, 0.0222],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "7", "3D", "RC"): {
        "B_initial": -0.02065,
        "B_limits":  [-0.0264, -0.0149],
        "C_initial": 0.00559,
        "C_limits":  [0.0028, 0.0084],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "8", "3D", "RC"): {
        "B_initial": -0.05466,
        "B_limits":  [-0.0614, -0.048],
        "C_initial": 0.01075,
        "C_limits":  [0.0077, 0.0138],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "9", "3D", "RC"): {
        "B_initial": -0.08973,
        "B_limits":  [-0.0977, -0.0818],
        "C_initial": 0.00618,
        "C_limits":  [0.0022, 0.0101],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "10", "3D", "RC"): {
        "B_initial": -0.13451,
        "B_limits":  [-0.144, -0.1251],
        "C_initial": 0.00075,
        "C_limits":  [-0.0033, 0.0048],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "11", "3D", "RC"): {
        "B_initial": -0.19558,
        "B_limits":  [-0.2072, -0.1839],
        "C_initial": 0.0009,
        "C_limits":  [-0.0024, 0.0042],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "12", "3D", "RC"): {
        "B_initial": -0.31211,
        "B_limits":  [-0.3338, -0.2904],
        "C_initial": 0.03427,
        "C_limits":  [0.0256, 0.0429],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "13", "3D", "RC"): {
        "B_initial": -0.00222,
        "B_limits":  [-0.0048, 0.0004],
        "C_initial": 0.00147,
        "C_limits":  [-0.0004, 0.0033],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "14", "3D", "RC"): {
        "B_initial": -0.02395,
        "B_limits":  [-0.0277, -0.0202],
        "C_initial": -0.00916,
        "C_limits":  [-0.0119, -0.0064],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "15", "3D", "RC"): {
        "B_initial": -0.05392,
        "B_limits":  [-0.059, -0.0488],
        "C_initial": -0.01788,
        "C_limits":  [-0.0209, -0.0149],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "16", "3D", "RC"): {
        "B_initial": -0.09644,
        "B_limits":  [-0.1033, -0.0896],
        "C_initial": -0.02149,
        "C_limits":  [-0.0242, -0.0187],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "17", "3D", "RC"): {
        "B_initial": -0.15808,
        "B_limits":  [-0.1678, -0.1484],
        "C_initial": -0.01254,
        "C_limits":  [-0.0158, -0.0093],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "18", "3D", "RC"): {
        "B_initial": -0.27975,
        "B_limits":  [-0.3012, -0.2583],
        "C_initial": 0.04482,
        "C_limits":  [0.0318, 0.0579],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "19", "3D", "RC"): {
        "B_initial": 0.00099,
        "B_limits":  [-0.0005, 0.0024],
        "C_initial": -0.00327,
        "C_limits":  [-0.0064, -0.0002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "20", "3D", "RC"): {
        "B_initial": -0.0134,
        "B_limits":  [-0.016, -0.0108],
        "C_initial": -0.02186,
        "C_limits":  [-0.0241, -0.0196],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "21", "3D", "RC"): {
        "B_initial": -0.04033,
        "B_limits":  [-0.0445, -0.0362],
        "C_initial": -0.03099,
        "C_limits":  [-0.0331, -0.0289],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "22", "3D", "RC"): {
        "B_initial": -0.08149,
        "B_limits":  [-0.0876, -0.0753],
        "C_initial": -0.03066,
        "C_limits":  [-0.0329, -0.0284],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "23", "3D", "RC"): {
        "B_initial": -0.14336,
        "B_limits":  [-0.1526, -0.1341],
        "C_initial": -0.01252,
        "C_limits":  [-0.0169, -0.0081],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "24", "3D", "RC"): {
        "B_initial": -0.26751,
        "B_limits":  [-0.2891, -0.246],
        "C_initial": 0.06595,
        "C_limits":  [0.0492, 0.0827],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "25", "3D", "RC"): {
        "B_initial": -0.00302,
        "B_limits":  [-0.0045, -0.0015],
        "C_initial": -0.00504,
        "C_limits":  [-0.0091, -0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "26", "3D", "RC"): {
        "B_initial": -0.01296,
        "B_limits":  [-0.0153, -0.0106],
        "C_initial": -0.02789,
        "C_limits":  [-0.0298, -0.0259],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "27", "3D", "RC"): {
        "B_initial": -0.03816,
        "B_limits":  [-0.0422, -0.0342],
        "C_initial": -0.03614,
        "C_limits":  [-0.0376, -0.0346],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "28", "3D", "RC"): {
        "B_initial": -0.07865,
        "B_limits":  [-0.0848, -0.0726],
        "C_initial": -0.03172,
        "C_limits":  [-0.034, -0.0294],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "29", "3D", "RC"): {
        "B_initial": -0.14082,
        "B_limits":  [-0.1501, -0.1316],
        "C_initial": -0.00555,
        "C_limits":  [-0.011, -0.0001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "31", "3D", "RC"): {
        "B_initial": -0.01266,
        "B_limits":  [-0.015, -0.0103],
        "C_initial": -0.00394,
        "C_limits":  [-0.0087, 0.0008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "32", "3D", "RC"): {
        "B_initial": -0.01947,
        "B_limits":  [-0.0221, -0.0169],
        "C_initial": -0.02941,
        "C_limits":  [-0.0311, -0.0277],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "33", "3D", "RC"): {
        "B_initial": -0.0436,
        "B_limits":  [-0.0478, -0.0394],
        "C_initial": -0.03593,
        "C_limits":  [-0.0371, -0.0348],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "34", "3D", "RC"): {
        "B_initial": -0.08384,
        "B_limits":  [-0.0902, -0.0775],
        "C_initial": -0.02683,
        "C_limits":  [-0.0297, -0.024],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "35", "3D", "RC"): {
        "B_initial": -0.14651,
        "B_limits":  [-0.1561, -0.137],
        "C_initial": 0.00765,
        "C_limits":  [0.0008, 0.0145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "1", "3D", "RC"): {
        "B_initial": -0.05029,
        "B_limits":  [-0.0594, -0.0412],
        "C_initial": 0.00153,
        "C_limits":  [-0.0036, 0.0067],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "2", "3D", "RC"): {
        "B_initial": -0.10795,
        "B_limits":  [-0.1172, -0.0987],
        "C_initial": 0.01813,
        "C_limits":  [0.0153, 0.021],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "3", "3D", "RC"): {
        "B_initial": -0.15737,
        "B_limits":  [-0.1681, -0.1467],
        "C_initial": 0.01777,
        "C_limits":  [0.0133, 0.0222],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "4", "3D", "RC"): {
        "B_initial": -0.21229,
        "B_limits":  [-0.2251, -0.1994],
        "C_initial": 0.01305,
        "C_limits":  [0.0074, 0.0187],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "5", "3D", "RC"): {
        "B_initial": -0.29331,
        "B_limits":  [-0.311, -0.2756],
        "C_initial": 0.00795,
        "C_limits":  [0.0017, 0.0142],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "6", "3D", "RC"): {
        "B_initial": -0.02653,
        "B_limits":  [-0.032, -0.021],
        "C_initial": 0.00553,
        "C_limits":  [0.0037, 0.0073],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "7", "3D", "RC"): {
        "B_initial": -0.06662,
        "B_limits":  [-0.0728, -0.0604],
        "C_initial": 0.00151,
        "C_limits":  [-0.002, 0.005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "8", "3D", "RC"): {
        "B_initial": -0.1075,
        "B_limits":  [-0.1148, -0.1002],
        "C_initial": -0.00767,
        "C_limits":  [-0.0123, -0.0031],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "9", "3D", "RC"): {
        "B_initial": -0.15681,
        "B_limits":  [-0.166, -0.1476],
        "C_initial": -0.01669,
        "C_limits":  [-0.022, -0.0114],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "10", "3D", "RC"): {
        "B_initial": -0.23424,
        "B_limits":  [-0.2487, -0.2198],
        "C_initial": -0.02114,
        "C_limits":  [-0.027, -0.0153],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "11", "3D", "RC"): {
        "B_initial": -0.01327,
        "B_limits":  [-0.0168, -0.0098],
        "C_initial": 0.00151,
        "C_limits":  [-0.0008, 0.0038],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "12", "3D", "RC"): {
        "B_initial": -0.04273,
        "B_limits":  [-0.0474, -0.038],
        "C_initial": -0.01241,
        "C_limits":  [-0.016, -0.0088],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "13", "3D", "RC"): {
        "B_initial": -0.07826,
        "B_limits":  [-0.084, -0.0726],
        "C_initial": -0.02481,
        "C_limits":  [-0.0293, -0.0203],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "14", "3D", "RC"): {
        "B_initial": -0.12382,
        "B_limits":  [-0.1314, -0.1162],
        "C_initial": -0.0342,
        "C_limits":  [-0.0393, -0.0291],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "15", "3D", "RC"): {
        "B_initial": -0.19841,
        "B_limits":  [-0.2114, -0.1854],
        "C_initial": -0.03514,
        "C_limits":  [-0.041, -0.0292],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "16", "3D", "RC"): {
        "B_initial": -0.00472,
        "B_limits":  [-0.0069, -0.0026],
        "C_initial": -0.00263,
        "C_limits":  [-0.006, 0.0007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "17", "3D", "RC"): {
        "B_initial": -0.02551,
        "B_limits":  [-0.0294, -0.0216],
        "C_initial": -0.02347,
        "C_limits":  [-0.0272, -0.0198],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "18", "3D", "RC"): {
        "B_initial": -0.05662,
        "B_limits":  [-0.0616, -0.0516],
        "C_initial": -0.03745,
        "C_limits":  [-0.0418, -0.0331],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "19", "3D", "RC"): {
        "B_initial": -0.09901,
        "B_limits":  [-0.1059, -0.0922],
        "C_initial": -0.04591,
        "C_limits":  [-0.0508, -0.041],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "20", "3D", "RC"): {
        "B_initial": -0.17105,
        "B_limits":  [-0.1833, -0.1588],
        "C_initial": -0.04218,
        "C_limits":  [-0.0482, -0.0362],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "21", "3D", "RC"): {
        "B_initial": -0.00013,
        "B_limits":  [-0.0015, 0.0012],
        "C_initial": -0.00547,
        "C_limits":  [-0.0096, -0.0013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "22", "3D", "RC"): {
        "B_initial": -0.01424,
        "B_limits":  [-0.0174, -0.0111],
        "C_initial": -0.03102,
        "C_limits":  [-0.0345, -0.0275],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "23", "3D", "RC"): {
        "B_initial": -0.04191,
        "B_limits":  [-0.0461, -0.0377],
        "C_initial": -0.04557,
        "C_limits":  [-0.0495, -0.0416],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "24", "3D", "RC"): {
        "B_initial": -0.08184,
        "B_limits":  [-0.0879, -0.0758],
        "C_initial": -0.05258,
        "C_limits":  [-0.0571, -0.048],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "25", "3D", "RC"): {
        "B_initial": -0.15185,
        "B_limits":  [-0.1634, -0.1403],
        "C_initial": -0.04412,
        "C_limits":  [-0.0503, -0.038],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "26", "3D", "RC"): {
        "B_initial": 0.00135,
        "B_limits":  [-0.0002, 0.0029],
        "C_initial": -0.00678,
        "C_limits":  [-0.0115, -0.002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "27", "3D", "RC"): {
        "B_initial": -0.00802,
        "B_limits":  [-0.011, -0.0051],
        "C_initial": -0.03522,
        "C_limits":  [-0.0386, -0.0318],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "28", "3D", "RC"): {
        "B_initial": -0.03327,
        "B_limits":  [-0.0373, -0.0292],
        "C_initial": -0.04972,
        "C_limits":  [-0.0534, -0.0461],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "29", "3D", "RC"): {
        "B_initial": -0.07143,
        "B_limits":  [-0.0773, -0.0656],
        "C_initial": -0.05514,
        "C_limits":  [-0.0594, -0.0509],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "30", "3D", "RC"): {
        "B_initial": -0.13996,
        "B_limits":  [-0.1513, -0.1286],
        "C_initial": -0.04246,
        "C_limits":  [-0.0488, -0.0362],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "31", "3D", "RC"): {
        "B_initial": -0.00047,
        "B_limits":  [-0.003, 0.0021],
        "C_initial": -0.00647,
        "C_limits":  [-0.012, -0.001],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "32", "3D", "RC"): {
        "B_initial": -0.00335,
        "B_limits":  [-0.0064, -0.0003],
        "C_initial": -0.03814,
        "C_limits":  [-0.0412, -0.0351],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "33", "3D", "RC"): {
        "B_initial": -0.02528,
        "B_limits":  [-0.0296, -0.021],
        "C_initial": -0.05173,
        "C_limits":  [-0.0548, -0.0487],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "34", "3D", "RC"): {
        "B_initial": -0.06105,
        "B_limits":  [-0.0671, -0.055],
        "C_initial": -0.05393,
        "C_limits":  [-0.0577, -0.0501],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "35", "3D", "RC"): {
        "B_initial": -0.12753,
        "B_limits":  [-0.1388, -0.1162],
        "C_initial": -0.03386,
        "C_limits":  [-0.0408, -0.0269],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "1", "3D", "RC"): {
        "B_initial": -0.05432,
        "B_limits":  [-0.0684, -0.0402],
        "C_initial": -0.02649,
        "C_limits":  [-0.036, -0.017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "2", "3D", "RC"): {
        "B_initial": -0.0908,
        "B_limits":  [-0.1044, -0.0772],
        "C_initial": -0.00673,
        "C_limits":  [-0.0105, -0.003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "3", "3D", "RC"): {
        "B_initial": -0.11464,
        "B_limits":  [-0.1274, -0.1019],
        "C_initial": -0.0064,
        "C_limits":  [-0.0095, -0.0033],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "4", "3D", "RC"): {
        "B_initial": -0.14039,
        "B_limits":  [-0.1517, -0.1291],
        "C_initial": -0.00941,
        "C_limits":  [-0.0124, -0.0064],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "5", "3D", "RC"): {
        "B_initial": -0.17793,
        "B_limits":  [-0.1881, -0.1678],
        "C_initial": -0.01165,
        "C_limits":  [-0.0154, -0.0079],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "6", "3D", "RC"): {
        "B_initial": -0.24514,
        "B_limits":  [-0.2567, -0.2336],
        "C_initial": 0,
        "C_limits":  [-0.008, 0.008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "7", "3D", "RC"): {
        "B_initial": -0.37055,
        "B_limits":  [-0.3914, -0.3497],
        "C_initial": 0.06028,
        "C_limits":  [0.042, 0.0786],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "8", "3D", "RC"): {
        "B_initial": 0.0046,
        "B_limits":  [-0.0008, 0.0101],
        "C_initial": -0.00793,
        "C_limits":  [-0.0097, -0.0062],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "9", "3D", "RC"): {
        "B_initial": -0.02839,
        "B_limits":  [-0.0325, -0.0243],
        "C_initial": -0.01303,
        "C_limits":  [-0.0152, -0.0109],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "10", "3D", "RC"): {
        "B_initial": -0.05692,
        "B_limits":  [-0.0615, -0.0524],
        "C_initial": -0.01635,
        "C_limits":  [-0.0183, -0.0144],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "11", "3D", "RC"): {
        "B_initial": -0.09121,
        "B_limits":  [-0.0962, -0.0862],
        "C_initial": -0.01535,
        "C_limits":  [-0.0168, -0.0139],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "12", "3D", "RC"): {
        "B_initial": -0.1437,
        "B_limits":  [-0.1523, -0.1351],
        "C_initial": -0.00287,
        "C_limits":  [-0.006, 0.0003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "13", "3D", "RC"): {
        "B_initial": -0.23556,
        "B_limits":  [-0.2501, -0.2211],
        "C_initial": 0.04084,
        "C_limits":  [0.0314, 0.0503],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "14", "3D", "RC"): {
        "B_initial": -0.3918,
        "B_limits":  [-0.4164, -0.3672],
        "C_initial": 0.14993,
        "C_limits":  [0.1289, 0.1709],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "15", "3D", "RC"): {
        "B_initial": 0.01141,
        "B_limits":  [0.0064, 0.0164],
        "C_initial": -0.00966,
        "C_limits":  [-0.0123, -0.0071],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "16", "3D", "RC"): {
        "B_initial": -0.02226,
        "B_limits":  [-0.0258, -0.0187],
        "C_initial": -0.02221,
        "C_limits":  [-0.0233, -0.0211],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "17", "3D", "RC"): {
        "B_initial": -0.05389,
        "B_limits":  [-0.0584, -0.0494],
        "C_initial": -0.02383,
        "C_limits":  [-0.0247, -0.023],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "18", "3D", "RC"): {
        "B_initial": -0.09265,
        "B_limits":  [-0.0981, -0.0872],
        "C_initial": -0.0172,
        "C_limits":  [-0.0188, -0.0156],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "19", "3D", "RC"): {
        "B_initial": -0.15207,
        "B_limits":  [-0.1618, -0.1423],
        "C_initial": 0.0072,
        "C_limits":  [0.0021, 0.0123],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "20", "3D", "RC"): {
        "B_initial": -0.25416,
        "B_limits":  [-0.2702, -0.2381],
        "C_initial": 0.07309,
        "C_limits":  [0.0609, 0.0853],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "22", "3D", "RC"): {
        "B_initial": 0.00562,
        "B_limits":  [0.0001, 0.0111],
        "C_initial": -0.00827,
        "C_limits":  [-0.0116, -0.0049],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "23", "3D", "RC"): {
        "B_initial": -0.02974,
        "B_limits":  [-0.0337, -0.0258],
        "C_initial": -0.02354,
        "C_limits":  [-0.0243, -0.0228],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "24", "3D", "RC"): {
        "B_initial": -0.06372,
        "B_limits":  [-0.0686, -0.0588],
        "C_initial": -0.02323,
        "C_limits":  [-0.0242, -0.0223],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "25", "3D", "RC"): {
        "B_initial": -0.10545,
        "B_limits":  [-0.1114, -0.0995],
        "C_initial": -0.01245,
        "C_limits":  [-0.0147, -0.0102],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "26", "3D", "RC"): {
        "B_initial": -0.16904,
        "B_limits":  [-0.1795, -0.1586],
        "C_initial": 0.01983,
        "C_limits":  [0.0135, 0.0261],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "29", "3D", "RC"): {
        "B_initial": -0.00471,
        "B_limits":  [-0.0109, 0.0015],
        "C_initial": -0.0048,
        "C_limits":  [-0.0087, -0.0009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "30", "3D", "RC"): {
        "B_initial": -0.04223,
        "B_limits":  [-0.0468, -0.0377],
        "C_initial": -0.02144,
        "C_limits":  [-0.0222, -0.0207],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "31", "3D", "RC"): {
        "B_initial": -0.0785,
        "B_limits":  [-0.0839, -0.0731],
        "C_initial": -0.01909,
        "C_limits":  [-0.0204, -0.0177],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "32", "3D", "RC"): {
        "B_initial": -0.12289,
        "B_limits":  [-0.1294, -0.1164],
        "C_initial": -0.0045,
        "C_limits":  [-0.0074, -0.0016],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "1", "3D", "RC"): {
        "B_initial": -0.04394,
        "B_limits":  [-0.0535, -0.0344],
        "C_initial": -0.02082,
        "C_limits":  [-0.0299, -0.0117],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "2", "3D", "RC"): {
        "B_initial": -0.08736,
        "B_limits":  [-0.0969, -0.0779],
        "C_initial": 0.00389,
        "C_limits":  [0.0008, 0.007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "3", "3D", "RC"): {
        "B_initial": -0.12189,
        "B_limits":  [-0.1313, -0.1125],
        "C_initial": 0.00597,
        "C_limits":  [0.0034, 0.0085],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "4", "3D", "RC"): {
        "B_initial": -0.16006,
        "B_limits":  [-0.1695, -0.1506],
        "C_initial": 0.00293,
        "C_limits":  [0.0003, 0.0055],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "5", "3D", "RC"): {
        "B_initial": -0.21595,
        "B_limits":  [-0.227, -0.2049],
        "C_initial": 0.00243,
        "C_limits":  [-0.0002, 0.005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "6", "3D", "RC"): {
        "B_initial": -0.33726,
        "B_limits":  [-0.3598, -0.3147],
        "C_initial": 0.03987,
        "C_limits":  [0.0287, 0.051],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "7", "3D", "RC"): {
        "B_initial": -0.00678,
        "B_limits":  [-0.0115, -0.0021],
        "C_initial": -0.00238,
        "C_limits":  [-0.0042, -0.0005],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "8", "3D", "RC"): {
        "B_initial": -0.03908,
        "B_limits":  [-0.0441, -0.0341],
        "C_initial": -0.00307,
        "C_limits":  [-0.0054, -0.0007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "9", "3D", "RC"): {
        "B_initial": -0.07236,
        "B_limits":  [-0.0778, -0.0669],
        "C_initial": -0.00839,
        "C_limits":  [-0.0109, -0.0059],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "10", "3D", "RC"): {
        "B_initial": -0.11396,
        "B_limits":  [-0.1207, -0.1073],
        "C_initial": -0.01048,
        "C_limits":  [-0.0125, -0.0084],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "11", "3D", "RC"): {
        "B_initial": -0.17904,
        "B_limits":  [-0.1896, -0.1684],
        "C_initial": -3e-05,
        "C_limits":  [-0.003, 0.003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "12", "3D", "RC"): {
        "B_initial": -0.32026,
        "B_limits":  [-0.3453, -0.2952],
        "C_initial": 0.06879,
        "C_limits":  [0.0531, 0.0845],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "13", "3D", "RC"): {
        "B_initial": 0.0048,
        "B_limits":  [0.0018, 0.0078],
        "C_initial": -0.00585,
        "C_limits":  [-0.0078, -0.0039],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "14", "3D", "RC"): {
        "B_initial": -0.0219,
        "B_limits":  [-0.0257, -0.0181],
        "C_initial": -0.01708,
        "C_limits":  [-0.0191, -0.0151],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "15", "3D", "RC"): {
        "B_initial": -0.05462,
        "B_limits":  [-0.0592, -0.05],
        "C_initial": -0.02261,
        "C_limits":  [-0.0243, -0.0209],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "16", "3D", "RC"): {
        "B_initial": -0.09799,
        "B_limits":  [-0.1043, -0.0917],
        "C_initial": -0.01946,
        "C_limits":  [-0.0212, -0.0177],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "17", "3D", "RC"): {
        "B_initial": -0.16753,
        "B_limits":  [-0.1785, -0.1566],
        "C_initial": 0.00377,
        "C_limits":  [-0.0014, 0.0089],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "18", "3D", "RC"): {
        "B_initial": -0.31746,
        "B_limits":  [-0.3437, -0.2912],
        "C_initial": 0.10138,
        "C_limits":  [0.0808, 0.122],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "19", "3D", "RC"): {
        "B_initial": 0.00349,
        "B_limits":  [0.0008, 0.0062],
        "C_initial": -0.00768,
        "C_limits":  [-0.0108, -0.0046],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "20", "3D", "RC"): {
        "B_initial": -0.02031,
        "B_limits":  [-0.0239, -0.0167],
        "C_initial": -0.02475,
        "C_limits":  [-0.0261, -0.0234],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "21", "3D", "RC"): {
        "B_initial": -0.05338,
        "B_limits":  [-0.0581, -0.0487],
        "C_initial": -0.02843,
        "C_limits":  [-0.0294, -0.0275],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "22", "3D", "RC"): {
        "B_initial": -0.0986,
        "B_limits":  [-0.1053, -0.0919],
        "C_initial": -0.01906,
        "C_limits":  [-0.0215, -0.0166],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "23", "3D", "RC"): {
        "B_initial": -0.17181,
        "B_limits":  [-0.1834, -0.1602],
        "C_initial": 0.01686,
        "C_limits":  [0.0096, 0.0242],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "25", "3D", "RC"): {
        "B_initial": -0.00332,
        "B_limits":  [-0.0061, -0.0006],
        "C_initial": -0.00681,
        "C_limits":  [-0.0107, -0.003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "26", "3D", "RC"): {
        "B_initial": -0.02619,
        "B_limits":  [-0.0299, -0.0225],
        "C_initial": -0.02644,
        "C_limits":  [-0.0276, -0.0253],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "27", "3D", "RC"): {
        "B_initial": -0.05997,
        "B_limits":  [-0.0648, -0.0551],
        "C_initial": -0.028,
        "C_limits":  [-0.029, -0.027],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "28", "3D", "RC"): {
        "B_initial": -0.10675,
        "B_limits":  [-0.1137, -0.0998],
        "C_initial": -0.01368,
        "C_limits":  [-0.0168, -0.0106],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "29", "3D", "RC"): {
        "B_initial": -0.18251,
        "B_limits":  [-0.1946, -0.1705],
        "C_initial": 0.03153,
        "C_limits":  [0.023, 0.0401],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "31", "3D", "RC"): {
        "B_initial": -0.01313,
        "B_limits":  [-0.0163, -0.0099],
        "C_initial": -0.00396,
        "C_limits":  [-0.0083, 0.0004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "32", "3D", "RC"): {
        "B_initial": -0.03598,
        "B_limits":  [-0.04, -0.032],
        "C_initial": -0.02475,
        "C_limits":  [-0.0259, -0.0236],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "33", "3D", "RC"): {
        "B_initial": -0.07073,
        "B_limits":  [-0.076, -0.0655],
        "C_initial": -0.02406,
        "C_limits":  [-0.0255, -0.0226],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "34", "3D", "RC"): {
        "B_initial": -0.11899,
        "B_limits":  [-0.1264, -0.1116],
        "C_initial": -0.00532,
        "C_limits":  [-0.0093, -0.0014],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "1", "3D", "RC"): {
        "B_initial": -0.03262,
        "B_limits":  [-0.0406, -0.0247],
        "C_initial": -0.00731,
        "C_limits":  [-0.0135, -0.0011],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "2", "3D", "RC"): {
        "B_initial": -0.08188,
        "B_limits":  [-0.0905, -0.0733],
        "C_initial": 0.01108,
        "C_limits":  [0.0087, 0.0134],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "3", "3D", "RC"): {
        "B_initial": -0.12902,
        "B_limits":  [-0.1391, -0.1189],
        "C_initial": 0.0111,
        "C_limits":  [0.0075, 0.0147],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "4", "3D", "RC"): {
        "B_initial": -0.19102,
        "B_limits":  [-0.2039, -0.1781],
        "C_initial": 0.00652,
        "C_limits":  [0.0022, 0.0108],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "5", "3D", "RC"): {
        "B_initial": -0.28009,
        "B_limits":  [-0.2965, -0.2636],
        "C_initial": 0.00926,
        "C_limits":  [0.0052, 0.0133],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "6", "3D", "RC"): {
        "B_initial": -0.00626,
        "B_limits":  [-0.0104, -0.0021],
        "C_initial": -0.00018,
        "C_limits":  [-0.0022, 0.0018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "7", "3D", "RC"): {
        "B_initial": -0.03623,
        "B_limits":  [-0.0421, -0.0303],
        "C_initial": -0.00778,
        "C_limits":  [-0.0114, -0.0042],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "8", "3D", "RC"): {
        "B_initial": -0.07488,
        "B_limits":  [-0.0825, -0.0673],
        "C_initial": -0.01705,
        "C_limits":  [-0.0213, -0.0128],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "9", "3D", "RC"): {
        "B_initial": -0.13349,
        "B_limits":  [-0.1443, -0.1227],
        "C_initial": -0.02104,
        "C_limits":  [-0.0251, -0.017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "10", "3D", "RC"): {
        "B_initial": -0.22497,
        "B_limits":  [-0.24, -0.21],
        "C_initial": -0.00468,
        "C_limits":  [-0.0103, 0.0009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "11", "3D", "RC"): {
        "B_initial": 0.00272,
        "B_limits":  [0.0012, 0.0042],
        "C_initial": -0.00465,
        "C_limits":  [-0.0078, -0.0015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "12", "3D", "RC"): {
        "B_initial": -0.01542,
        "B_limits":  [-0.0188, -0.0121],
        "C_initial": -0.02432,
        "C_limits":  [-0.0268, -0.0218],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "13", "3D", "RC"): {
        "B_initial": -0.04873,
        "B_limits":  [-0.0539, -0.0435],
        "C_initial": -0.03468,
        "C_limits":  [-0.0372, -0.0322],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "14", "3D", "RC"): {
        "B_initial": -0.10485,
        "B_limits":  [-0.1138, -0.0959],
        "C_initial": -0.03178,
        "C_limits":  [-0.0351, -0.0285],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "15", "3D", "RC"): {
        "B_initial": -0.19684,
        "B_limits":  [-0.2107, -0.183],
        "C_initial": 0.00211,
        "C_limits":  [-0.0059, 0.0101],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "16", "3D", "RC"): {
        "B_initial": -0.00052,
        "B_limits":  [-0.0019, 0.0009],
        "C_initial": -0.00504,
        "C_limits":  [-0.0092, -0.0009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "17", "3D", "RC"): {
        "B_initial": -0.0129,
        "B_limits":  [-0.0159, -0.0099],
        "C_initial": -0.02939,
        "C_limits":  [-0.0315, -0.0273],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "18", "3D", "RC"): {
        "B_initial": -0.04376,
        "B_limits":  [-0.0487, -0.0388],
        "C_initial": -0.0381,
        "C_limits":  [-0.0399, -0.0363],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "19", "3D", "RC"): {
        "B_initial": -0.09892,
        "B_limits":  [-0.1078, -0.09],
        "C_initial": -0.02831,
        "C_limits":  [-0.0321, -0.0245],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "20", "3D", "RC"): {
        "B_initial": -0.19137,
        "B_limits":  [-0.2053, -0.1774],
        "C_initial": 0.01954,
        "C_limits":  [0.0096, 0.0295],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "21", "3D", "RC"): {
        "B_initial": -0.00997,
        "B_limits":  [-0.0121, -0.0078],
        "C_initial": -0.00174,
        "C_limits":  [-0.0067, 0.0032],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "22", "3D", "RC"): {
        "B_initial": -0.01869,
        "B_limits":  [-0.0219, -0.0155],
        "C_initial": -0.02839,
        "C_limits":  [-0.0303, -0.0265],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "23", "3D", "RC"): {
        "B_initial": -0.04822,
        "B_limits":  [-0.0534, -0.043],
        "C_initial": -0.03439,
        "C_limits":  [-0.036, -0.0328],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "24", "3D", "RC"): {
        "B_initial": -0.10312,
        "B_limits":  [-0.1123, -0.0939],
        "C_initial": -0.01734,
        "C_limits":  [-0.0222, -0.0125],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "1", "3D", "RC"): {
        "B_initial": -0.03443,
        "B_limits":  [-0.0434, -0.0255],
        "C_initial": -0.00202,
        "C_limits":  [-0.006, 0.002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "2", "3D", "RC"): {
        "B_initial": -0.08752,
        "B_limits":  [-0.0974, -0.0776],
        "C_initial": 0.00224,
        "C_limits":  [-0.0025, 0.007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "3", "3D", "RC"): {
        "B_initial": -0.13406,
        "B_limits":  [-0.1464, -0.1218],
        "C_initial": -0.00399,
        "C_limits":  [-0.0111, 0.0031],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "4", "3D", "RC"): {
        "B_initial": -0.18994,
        "B_limits":  [-0.2048, -0.1751],
        "C_initial": -0.01321,
        "C_limits":  [-0.0221, -0.0044],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "6", "3D", "RC"): {
        "B_initial": -0.01001,
        "B_limits":  [-0.014, -0.006],
        "C_initial": -0.00273,
        "C_limits":  [-0.006, 0.0006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "7", "3D", "RC"): {
        "B_initial": -0.03935,
        "B_limits":  [-0.0445, -0.0342],
        "C_initial": -0.02147,
        "C_limits":  [-0.0262, -0.0168],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "8", "3D", "RC"): {
        "B_initial": -0.07373,
        "B_limits":  [-0.0805, -0.067],
        "C_initial": -0.03689,
        "C_limits":  [-0.043, -0.0308],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "9", "3D", "RC"): {
        "B_initial": -0.12003,
        "B_limits":  [-0.1287, -0.1113],
        "C_initial": -0.0505,
        "C_limits":  [-0.0578, -0.0432],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "10", "3D", "RC"): {
        "B_initial": -0.19962,
        "B_limits":  [-0.2144, -0.1848],
        "C_initial": -0.05715,
        "C_limits":  [-0.066, -0.0483],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "11", "3D", "RC"): {
        "B_initial": 0.00088,
        "B_limits":  [-0.001, 0.0027],
        "C_initial": -0.00685,
        "C_limits":  [-0.0115, -0.0022],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "12", "3D", "RC"): {
        "B_initial": -0.01622,
        "B_limits":  [-0.0198, -0.0127],
        "C_initial": -0.03414,
        "C_limits":  [-0.0385, -0.0298],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "13", "3D", "RC"): {
        "B_initial": -0.04419,
        "B_limits":  [-0.0492, -0.0392],
        "C_initial": -0.05144,
        "C_limits":  [-0.0569, -0.046],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "14", "3D", "RC"): {
        "B_initial": -0.08529,
        "B_limits":  [-0.0922, -0.0784],
        "C_initial": -0.06393,
        "C_limits":  [-0.0705, -0.0573],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "15", "3D", "RC"): {
        "B_initial": -0.16005,
        "B_limits":  [-0.1731, -0.147],
        "C_initial": -0.06416,
        "C_limits":  [-0.0727, -0.0556],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "16", "3D", "RC"): {
        "B_initial": 0.00513,
        "B_limits":  [0.0037, 0.0066],
        "C_initial": -0.00799,
        "C_limits":  [-0.0135, -0.0025],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "17", "3D", "RC"): {
        "B_initial": -0.00382,
        "B_limits":  [-0.0066, -0.001],
        "C_initial": -0.03983,
        "C_limits":  [-0.0438, -0.0359],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "18", "3D", "RC"): {
        "B_initial": -0.02752,
        "B_limits":  [-0.0317, -0.0233],
        "C_initial": -0.05727,
        "C_limits":  [-0.0621, -0.0524],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "19", "3D", "RC"): {
        "B_initial": -0.06514,
        "B_limits":  [-0.0712, -0.0591],
        "C_initial": -0.06763,
        "C_limits":  [-0.0736, -0.0617],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "20", "3D", "RC"): {
        "B_initial": -0.13662,
        "B_limits":  [-0.1489, -0.1244],
        "C_initial": -0.06138,
        "C_limits":  [-0.0697, -0.053],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "21", "3D", "RC"): {
        "B_initial": 0.00442,
        "B_limits":  [0.0018, 0.007],
        "C_initial": -0.00556,
        "C_limits":  [-0.0118, 0.0006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "22", "3D", "RC"): {
        "B_initial": 0.00271,
        "B_limits":  [-0.0004, 0.0058],
        "C_initial": -0.04035,
        "C_limits":  [-0.0439, -0.0368],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "23", "3D", "RC"): {
        "B_initial": -0.01722,
        "B_limits":  [-0.0216, -0.0128],
        "C_initial": -0.05673,
        "C_limits":  [-0.0608, -0.0526],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "24", "3D", "RC"): {
        "B_initial": -0.05177,
        "B_limits":  [-0.058, -0.0456],
        "C_initial": -0.06369,
        "C_limits":  [-0.069, -0.0584],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "25", "3D", "RC"): {
        "B_initial": -0.12031,
        "B_limits":  [-0.1325, -0.1081],
        "C_initial": -0.04923,
        "C_limits":  [-0.0578, -0.0407],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "1", "3D", "RC"): {
        "B_initial": -0.05569,
        "B_limits":  [-0.0676, -0.0438],
        "C_initial": -0.03938,
        "C_limits":  [-0.0495, -0.0293],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "2", "3D", "RC"): {
        "B_initial": -0.09855,
        "B_limits":  [-0.1099, -0.0872],
        "C_initial": -0.01711,
        "C_limits":  [-0.0214, -0.0129],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "3", "3D", "RC"): {
        "B_initial": -0.13274,
        "B_limits":  [-0.1428, -0.1227],
        "C_initial": -0.01661,
        "C_limits":  [-0.02, -0.0132],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "4", "3D", "RC"): {
        "B_initial": -0.17699,
        "B_limits":  [-0.1867, -0.1673],
        "C_initial": -0.01787,
        "C_limits":  [-0.0216, -0.0141],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "5", "3D", "RC"): {
        "B_initial": -0.30593,
        "B_limits":  [-0.3322, -0.2796],
        "C_initial": 0.02488,
        "C_limits":  [0.01, 0.0398],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "6", "3D", "RC"): {
        "B_initial": -0.00523,
        "B_limits":  [-0.011, 0.0005],
        "C_initial": -0.0154,
        "C_limits":  [-0.0174, -0.0135],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "7", "3D", "RC"): {
        "B_initial": -0.04439,
        "B_limits":  [-0.0503, -0.0385],
        "C_initial": -0.01738,
        "C_limits":  [-0.0192, -0.0155],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "8", "3D", "RC"): {
        "B_initial": -0.08489,
        "B_limits":  [-0.0908, -0.079],
        "C_initial": -0.01978,
        "C_limits":  [-0.0213, -0.0183],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "9", "3D", "RC"): {
        "B_initial": -0.14274,
        "B_limits":  [-0.1521, -0.1333],
        "C_initial": -0.01082,
        "C_limits":  [-0.0135, -0.0081],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "10", "3D", "RC"): {
        "B_initial": -0.30378,
        "B_limits":  [-0.3352, -0.2723],
        "C_initial": 0.07228,
        "C_limits":  [0.0518, 0.0928],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "11", "3D", "RC"): {
        "B_initial": 0.00874,
        "B_limits":  [0.0041, 0.0134],
        "C_initial": -0.0149,
        "C_limits":  [-0.0168, -0.013],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "12", "3D", "RC"): {
        "B_initial": -0.03068,
        "B_limits":  [-0.0359, -0.0255],
        "C_initial": -0.02405,
        "C_limits":  [-0.025, -0.0231],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "13", "3D", "RC"): {
        "B_initial": -0.07515,
        "B_limits":  [-0.0809, -0.0693],
        "C_initial": -0.02343,
        "C_limits":  [-0.0244, -0.0224],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "14", "3D", "RC"): {
        "B_initial": -0.13978,
        "B_limits":  [-0.1501, -0.1294],
        "C_initial": -0.00406,
        "C_limits":  [-0.0085, 0.0004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "15", "3D", "RC"): {
        "B_initial": -0.31435,
        "B_limits":  [-0.348, -0.2807],
        "C_initial": 0.10919,
        "C_limits":  [0.0837, 0.1347],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "16", "3D", "RC"): {
        "B_initial": 0.00976,
        "B_limits":  [0.0049, 0.0146],
        "C_initial": -0.01272,
        "C_limits":  [-0.0154, -0.01],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "17", "3D", "RC"): {
        "B_initial": -0.0314,
        "B_limits":  [-0.037, -0.0258],
        "C_initial": -0.0247,
        "C_limits":  [-0.0254, -0.024],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "18", "3D", "RC"): {
        "B_initial": -0.0793,
        "B_limits":  [-0.0856, -0.073],
        "C_initial": -0.02053,
        "C_limits":  [-0.0222, -0.0188],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "19", "3D", "RC"): {
        "B_initial": -0.14891,
        "B_limits":  [-0.1601, -0.1377],
        "C_initial": 0.00738,
        "C_limits":  [0.0014, 0.0133],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "21", "3D", "RC"): {
        "B_initial": 0.00512,
        "B_limits":  [-0.0003, 0.0105],
        "C_initial": -0.00856,
        "C_limits":  [-0.0119, -0.0052],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "22", "3D", "RC"): {
        "B_initial": -0.0385,
        "B_limits":  [-0.0446, -0.0324],
        "C_initial": -0.02178,
        "C_limits":  [-0.0229, -0.0207],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "23", "3D", "RC"): {
        "B_initial": -0.08982,
        "B_limits":  [-0.0966, -0.083],
        "C_initial": -0.01386,
        "C_limits":  [-0.0164, -0.0114],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "24", "3D", "RC"): {
        "B_initial": -0.16392,
        "B_limits":  [-0.1759, -0.152],
        "C_initial": 0.02193,
        "C_limits":  [0.0146, 0.0292],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "26", "3D", "RC"): {
        "B_initial": -0.00388,
        "B_limits":  [-0.01, 0.0022],
        "C_initial": -0.00228,
        "C_limits":  [-0.0062, 0.0017],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "27", "3D", "RC"): {
        "B_initial": -0.0506,
        "B_limits":  [-0.0573, -0.0439],
        "C_initial": -0.01573,
        "C_limits":  [-0.0175, -0.0139],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "28", "3D", "RC"): {
        "B_initial": -0.10547,
        "B_limits":  [-0.1129, -0.098],
        "C_initial": -0.00384,
        "C_limits":  [-0.0073, -0.0004],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "1", "3D", "RC"): {
        "B_initial": -0.03375,
        "B_limits":  [-0.042, -0.0255],
        "C_initial": -0.02253,
        "C_limits":  [-0.0301, -0.015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "2", "3D", "RC"): {
        "B_initial": -0.07809,
        "B_limits":  [-0.086, -0.0701],
        "C_initial": -0.00326,
        "C_limits":  [-0.0058, -0.0007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "3", "3D", "RC"): {
        "B_initial": -0.11485,
        "B_limits":  [-0.123, -0.1067],
        "C_initial": -0.0028,
        "C_limits":  [-0.0054, -0.0002],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "4", "3D", "RC"): {
        "B_initial": -0.15628,
        "B_limits":  [-0.165, -0.1475],
        "C_initial": -0.00578,
        "C_limits":  [-0.0086, -0.0029],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "5", "3D", "RC"): {
        "B_initial": -0.21726,
        "B_limits":  [-0.2286, -0.2059],
        "C_initial": -0.00433,
        "C_limits":  [-0.007, -0.0016],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "6", "3D", "RC"): {
        "B_initial": -0.3476,
        "B_limits":  [-0.3716, -0.3236],
        "C_initial": 0.03852,
        "C_limits":  [0.0272, 0.0499],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "7", "3D", "RC"): {
        "B_initial": -0.00678,
        "B_limits":  [-0.0112, -0.0023],
        "C_initial": -0.00761,
        "C_limits":  [-0.0094, -0.0059],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "8", "3D", "RC"): {
        "B_initial": -0.03835,
        "B_limits":  [-0.0433, -0.0334],
        "C_initial": -0.01192,
        "C_limits":  [-0.0142, -0.0097],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "9", "3D", "RC"): {
        "B_initial": -0.07217,
        "B_limits":  [-0.0777, -0.0666],
        "C_initial": -0.01822,
        "C_limits":  [-0.0208, -0.0157],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "10", "3D", "RC"): {
        "B_initial": -0.11491,
        "B_limits":  [-0.1218, -0.108],
        "C_initial": -0.0202,
        "C_limits":  [-0.0226, -0.0178],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "11", "3D", "RC"): {
        "B_initial": -0.18189,
        "B_limits":  [-0.1928, -0.171],
        "C_initial": -0.00861,
        "C_limits":  [-0.0125, -0.0047],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "12", "3D", "RC"): {
        "B_initial": -0.3259,
        "B_limits":  [-0.3513, -0.3005],
        "C_initial": 0.06243,
        "C_limits":  [0.046, 0.0788],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "13", "3D", "RC"): {
        "B_initial": 0.00313,
        "B_limits":  [0.0003, 0.0059],
        "C_initial": -0.00838,
        "C_limits":  [-0.0107, -0.006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "14", "3D", "RC"): {
        "B_initial": -0.02253,
        "B_limits":  [-0.0262, -0.0189],
        "C_initial": -0.02187,
        "C_limits":  [-0.0234, -0.0204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "15", "3D", "RC"): {
        "B_initial": -0.05532,
        "B_limits":  [-0.0599, -0.0507],
        "C_initial": -0.02793,
        "C_limits":  [-0.0293, -0.0266],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "16", "3D", "RC"): {
        "B_initial": -0.09916,
        "B_limits":  [-0.1055, -0.0928],
        "C_initial": -0.02469,
        "C_limits":  [-0.0267, -0.0226],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "17", "3D", "RC"): {
        "B_initial": -0.16948,
        "B_limits":  [-0.1805, -0.1584],
        "C_initial": -0.00097,
        "C_limits":  [-0.0066, 0.0047],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "18", "3D", "RC"): {
        "B_initial": -0.31982,
        "B_limits":  [-0.346, -0.2936],
        "C_initial": 0.09649,
        "C_limits":  [0.0759, 0.1171],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "19", "3D", "RC"): {
        "B_initial": 0.00263,
        "B_limits":  [0.0002, 0.0051],
        "C_initial": -0.00694,
        "C_limits":  [-0.0103, -0.0036],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "20", "3D", "RC"): {
        "B_initial": -0.02052,
        "B_limits":  [-0.0241, -0.017],
        "C_initial": -0.02444,
        "C_limits":  [-0.0258, -0.0231],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "21", "3D", "RC"): {
        "B_initial": -0.05346,
        "B_limits":  [-0.0581, -0.0488],
        "C_initial": -0.02856,
        "C_limits":  [-0.0295, -0.0276],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "22", "3D", "RC"): {
        "B_initial": -0.09864,
        "B_limits":  [-0.1053, -0.092],
        "C_initial": -0.01995,
        "C_limits":  [-0.0225, -0.0174],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "23", "3D", "RC"): {
        "B_initial": -0.17161,
        "B_limits":  [-0.1832, -0.16],
        "C_initial": 0.01424,
        "C_limits":  [0.0071, 0.0214],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "25", "3D", "RC"): {
        "B_initial": -0.00286,
        "B_limits":  [-0.0054, -0.0003],
        "C_initial": -0.0032,
        "C_limits":  [-0.0073, 0.0009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "26", "3D", "RC"): {
        "B_initial": -0.02516,
        "B_limits":  [-0.0288, -0.0215],
        "C_initial": -0.02247,
        "C_limits":  [-0.024, -0.0209],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "27", "3D", "RC"): {
        "B_initial": -0.05879,
        "B_limits":  [-0.0637, -0.0539],
        "C_initial": -0.02419,
        "C_limits":  [-0.0256, -0.0227],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "28", "3D", "RC"): {
        "B_initial": -0.10542,
        "B_limits":  [-0.1125, -0.0984],
        "C_initial": -0.01061,
        "C_limits":  [-0.0139, -0.0073],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "29", "3D", "RC"): {
        "B_initial": -0.18071,
        "B_limits":  [-0.1928, -0.1686],
        "C_initial": 0.03257,
        "C_limits":  [0.0241, 0.0411],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "31", "3D", "RC"): {
        "B_initial": -0.01213,
        "B_limits":  [-0.0151, -0.0092],
        "C_initial": 0.00286,
        "C_limits":  [-0.0019, 0.0076],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "32", "3D", "RC"): {
        "B_initial": -0.03452,
        "B_limits":  [-0.0385, -0.0305],
        "C_initial": -0.01706,
        "C_limits":  [-0.0192, -0.015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "33", "3D", "RC"): {
        "B_initial": -0.06927,
        "B_limits":  [-0.0746, -0.0639],
        "C_initial": -0.01597,
        "C_limits":  [-0.0183, -0.0136],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "34", "3D", "RC"): {
        "B_initial": -0.11756,
        "B_limits":  [-0.1251, -0.11],
        "C_initial": 0.00269,
        "C_limits":  [-0.0016, 0.007],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "1", "3D", "RC"): {
        "B_initial": -0.02591,
        "B_limits":  [-0.0336, -0.0182],
        "C_initial": -0.00548,
        "C_limits":  [-0.0091, -0.0019],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "2", "3D", "RC"): {
        "B_initial": -0.07731,
        "B_limits":  [-0.0855, -0.0691],
        "C_initial": -0.00371,
        "C_limits":  [-0.0077, 0.0003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "3", "3D", "RC"): {
        "B_initial": -0.12635,
        "B_limits":  [-0.1364, -0.1163],
        "C_initial": -0.01249,
        "C_limits":  [-0.0184, -0.0066],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "4", "3D", "RC"): {
        "B_initial": -0.1925,
        "B_limits":  [-0.2059, -0.1791],
        "C_initial": -0.02152,
        "C_limits":  [-0.0286, -0.0145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "6", "3D", "RC"): {
        "B_initial": -0.00855,
        "B_limits":  [-0.0126, -0.0045],
        "C_initial": -0.00464,
        "C_limits":  [-0.0075, -0.0018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "7", "3D", "RC"): {
        "B_initial": -0.04102,
        "B_limits":  [-0.0463, -0.0358],
        "C_initial": -0.02244,
        "C_limits":  [-0.0262, -0.0186],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "8", "3D", "RC"): {
        "B_initial": -0.08163,
        "B_limits":  [-0.0885, -0.0747],
        "C_initial": -0.03622,
        "C_limits":  [-0.0411, -0.0313],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "9", "3D", "RC"): {
        "B_initial": -0.1427,
        "B_limits":  [-0.1531, -0.1323],
        "C_initial": -0.04266,
        "C_limits":  [-0.0488, -0.0365],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "10", "3D", "RC"): {
        "B_initial": -0.27074,
        "B_limits":  [-0.2936, -0.2478],
        "C_initial": -0.01089,
        "C_limits":  [-0.0235, 0.0018],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "11", "3D", "RC"): {
        "B_initial": -0.00152,
        "B_limits":  [-0.0037, 0.0007],
        "C_initial": -0.00586,
        "C_limits":  [-0.0102, -0.0015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "12", "3D", "RC"): {
        "B_initial": -0.02302,
        "B_limits":  [-0.0269, -0.0191],
        "C_initial": -0.03157,
        "C_limits":  [-0.0347, -0.0284],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "13", "3D", "RC"): {
        "B_initial": -0.05884,
        "B_limits":  [-0.0645, -0.0532],
        "C_initial": -0.04418,
        "C_limits":  [-0.048, -0.0403],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "14", "3D", "RC"): {
        "B_initial": -0.11706,
        "B_limits":  [-0.1264, -0.1077],
        "C_initial": -0.04334,
        "C_limits":  [-0.049, -0.0377],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "15", "3D", "RC"): {
        "B_initial": -0.24393,
        "B_limits":  [-0.2664, -0.2215],
        "C_initial": 0.00934,
        "C_limits":  [-0.0063, 0.025],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "16", "3D", "RC"): {
        "B_initial": -0.00261,
        "B_limits":  [-0.0042, -0.001],
        "C_initial": -0.00274,
        "C_limits":  [-0.0081, 0.0026],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "17", "3D", "RC"): {
        "B_initial": -0.01731,
        "B_limits":  [-0.0206, -0.014],
        "C_initial": -0.03178,
        "C_limits":  [-0.0344, -0.0292],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "18", "3D", "RC"): {
        "B_initial": -0.05038,
        "B_limits":  [-0.0557, -0.0451],
        "C_initial": -0.04131,
        "C_limits":  [-0.0443, -0.0383],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "19", "3D", "RC"): {
        "B_initial": -0.10715,
        "B_limits":  [-0.1164, -0.0979],
        "C_initial": -0.03231,
        "C_limits":  [-0.0378, -0.0268],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "21", "3D", "RC"): {
        "B_initial": -0.00966,
        "B_limits":  [-0.0117, -0.0076],
        "C_initial": 0.00444,
        "C_limits":  [-0.0017, 0.0106],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "22", "3D", "RC"): {
        "B_initial": -0.02058,
        "B_limits":  [-0.0241, -0.0171],
        "C_initial": -0.02521,
        "C_limits":  [-0.0278, -0.0226],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "23", "3D", "RC"): {
        "B_initial": -0.05239,
        "B_limits":  [-0.058, -0.0468],
        "C_initial": -0.03086,
        "C_limits":  [-0.0337, -0.028],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "24", "3D", "RC"): {
        "B_initial": -0.10877,
        "B_limits":  [-0.1184, -0.0992],
        "C_initial": -0.01393,
        "C_limits":  [-0.02, -0.0078],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "1", "3D", "RC"): {
        "B_initial": -0.03195,
        "B_limits":  [-0.0411, -0.0228],
        "C_initial": -0.03218,
        "C_limits":  [-0.0388, -0.0256],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "2", "3D", "RC"): {
        "B_initial": -0.0661,
        "B_limits":  [-0.0754, -0.0568],
        "C_initial": -0.02087,
        "C_limits":  [-0.0233, -0.0185],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "3", "3D", "RC"): {
        "B_initial": -0.09592,
        "B_limits":  [-0.1052, -0.0866],
        "C_initial": -0.02246,
        "C_limits":  [-0.0245, -0.0204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "4", "3D", "RC"): {
        "B_initial": -0.13157,
        "B_limits":  [-0.1407, -0.1225],
        "C_initial": -0.02372,
        "C_limits":  [-0.0257, -0.0217],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "5", "3D", "RC"): {
        "B_initial": -0.18592,
        "B_limits":  [-0.197, -0.1749],
        "C_initial": -0.01538,
        "C_limits":  [-0.0192, -0.0115],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "6", "3D", "RC"): {
        "B_initial": -0.30712,
        "B_limits":  [-0.3298, -0.2844],
        "C_initial": 0.03903,
        "C_limits":  [0.025, 0.0531],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "7", "3D", "RC"): {
        "B_initial": 0.00596,
        "B_limits":  [0.0013, 0.0106],
        "C_initial": -0.01499,
        "C_limits":  [-0.0176, -0.0124],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "8", "3D", "RC"): {
        "B_initial": -0.02346,
        "B_limits":  [-0.0283, -0.0186],
        "C_initial": -0.02187,
        "C_limits":  [-0.0232, -0.0205],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "9", "3D", "RC"): {
        "B_initial": -0.05673,
        "B_limits":  [-0.0628, -0.0507],
        "C_initial": -0.02446,
        "C_limits":  [-0.0255, -0.0235],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "10", "3D", "RC"): {
        "B_initial": -0.09973,
        "B_limits":  [-0.1071, -0.0923],
        "C_initial": -0.0185,
        "C_limits":  [-0.0208, -0.0162],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "11", "3D", "RC"): {
        "B_initial": -0.1659,
        "B_limits":  [-0.1778, -0.154],
        "C_initial": 0.00684,
        "C_limits":  [0.0004, 0.0132],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "12", "3D", "RC"): {
        "B_initial": -0.30479,
        "B_limits":  [-0.3303, -0.2793],
        "C_initial": 0.09465,
        "C_limits":  [0.0756, 0.1137],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "13", "3D", "RC"): {
        "B_initial": 0.0158,
        "B_limits":  [0.0112, 0.0204],
        "C_initial": -0.00659,
        "C_limits":  [-0.0103, -0.0029],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "14", "3D", "RC"): {
        "B_initial": -0.01524,
        "B_limits":  [-0.0202, -0.0103],
        "C_initial": -0.01759,
        "C_limits":  [-0.02, -0.0151],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "15", "3D", "RC"): {
        "B_initial": -0.05273,
        "B_limits":  [-0.0593, -0.0462],
        "C_initial": -0.01603,
        "C_limits":  [-0.0186, -0.0134],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "16", "3D", "RC"): {
        "B_initial": -0.10141,
        "B_limits":  [-0.1098, -0.093],
        "C_initial": -0.00132,
        "C_limits":  [-0.0054, 0.0027],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "17", "3D", "RC"): {
        "B_initial": -0.17506,
        "B_limits":  [-0.1884, -0.1617],
        "C_initial": 0.03894,
        "C_limits":  [0.0304, 0.0475],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "19", "3D", "RC"): {
        "B_initial": 0.01443,
        "B_limits":  [0.009, 0.0199],
        "C_initial": 0.00311,
        "C_limits":  [-0.0014, 0.0076],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "20", "3D", "RC"): {
        "B_initial": -0.01952,
        "B_limits":  [-0.0251, -0.0139],
        "C_initial": -0.00853,
        "C_limits":  [-0.0119, -0.0052],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "21", "3D", "RC"): {
        "B_initial": -0.06077,
        "B_limits":  [-0.0681, -0.0535],
        "C_initial": -0.00296,
        "C_limits":  [-0.0066, 0.0006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "22", "3D", "RC"): {
        "B_initial": -0.11386,
        "B_limits":  [-0.123, -0.1047],
        "C_initial": 0.01857,
        "C_limits":  [0.0137, 0.0235],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "25", "3D", "RC"): {
        "B_initial": 0.00852,
        "B_limits":  [0.0022, 0.0148],
        "C_initial": 0.01365,
        "C_limits":  [0.0085, 0.0188],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "26", "3D", "RC"): {
        "B_initial": -0.0287,
        "B_limits":  [-0.0351, -0.0223],
        "C_initial": 0.00256,
        "C_limits":  [-0.0017, 0.0068],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "27", "3D", "RC"): {
        "B_initial": -0.07337,
        "B_limits":  [-0.0814, -0.0653],
        "C_initial": 0.0118,
        "C_limits":  [0.007, 0.0166],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "1", "3D", "RC"): {
        "B_initial": -0.02041,
        "B_limits":  [-0.0259, -0.015],
        "C_initial": -0.01516,
        "C_limits":  [-0.0195, -0.0108],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "2", "3D", "RC"): {
        "B_initial": -0.0514,
        "B_limits":  [-0.0578, -0.045],
        "C_initial": -0.01226,
        "C_limits":  [-0.0143, -0.0102],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "3", "3D", "RC"): {
        "B_initial": -0.08182,
        "B_limits":  [-0.0896, -0.074],
        "C_initial": -0.01847,
        "C_limits":  [-0.022, -0.015],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "4", "3D", "RC"): {
        "B_initial": -0.11535,
        "B_limits":  [-0.1239, -0.1068],
        "C_initial": -0.02579,
        "C_limits":  [-0.0303, -0.0212],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "5", "3D", "RC"): {
        "B_initial": -0.15669,
        "B_limits":  [-0.1668, -0.1466],
        "C_initial": -0.03056,
        "C_limits":  [-0.036, -0.0251],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "6", "3D", "RC"): {
        "B_initial": -0.23438,
        "B_limits":  [-0.2504, -0.2184],
        "C_initial": -0.0213,
        "C_limits":  [-0.0293, -0.0133],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "7", "3D", "RC"): {
        "B_initial": -0.0033,
        "B_limits":  [-0.0064, -0.0002],
        "C_initial": -0.00345,
        "C_limits":  [-0.0061, -0.0008],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "8", "3D", "RC"): {
        "B_initial": -0.02067,
        "B_limits":  [-0.0242, -0.0172],
        "C_initial": -0.01731,
        "C_limits":  [-0.0192, -0.0155],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "9", "3D", "RC"): {
        "B_initial": -0.04521,
        "B_limits":  [-0.0497, -0.0407],
        "C_initial": -0.02834,
        "C_limits":  [-0.0307, -0.026],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "10", "3D", "RC"): {
        "B_initial": -0.07613,
        "B_limits":  [-0.0813, -0.0709],
        "C_initial": -0.03468,
        "C_limits":  [-0.0379, -0.0314],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "11", "3D", "RC"): {
        "B_initial": -0.11726,
        "B_limits":  [-0.1246, -0.1099],
        "C_initial": -0.03313,
        "C_limits":  [-0.0381, -0.0282],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "12", "3D", "RC"): {
        "B_initial": -0.19742,
        "B_limits":  [-0.2124, -0.1824],
        "C_initial": -0.00689,
        "C_limits":  [-0.0171, 0.0034],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "13", "3D", "RC"): {
        "B_initial": 0.00173,
        "B_limits":  [-0.0009, 0.0044],
        "C_initial": 0.00345,
        "C_limits":  [-0.0004, 0.0073],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "14", "3D", "RC"): {
        "B_initial": -0.01136,
        "B_limits":  [-0.014, -0.0087],
        "C_initial": -0.0148,
        "C_limits":  [-0.0172, -0.0124],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "15", "3D", "RC"): {
        "B_initial": -0.03474,
        "B_limits":  [-0.0387, -0.0308],
        "C_initial": -0.02451,
        "C_limits":  [-0.0266, -0.0224],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "16", "3D", "RC"): {
        "B_initial": -0.06581,
        "B_limits":  [-0.0708, -0.0609],
        "C_initial": -0.02651,
        "C_limits":  [-0.0294, -0.0237],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "17", "3D", "RC"): {
        "B_initial": -0.1081,
        "B_limits":  [-0.1156, -0.1005],
        "C_initial": -0.01752,
        "C_limits":  [-0.0223, -0.0127],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "18", "3D", "RC"): {
        "B_initial": -0.19071,
        "B_limits":  [-0.2064, -0.175],
        "C_initial": 0.02384,
        "C_limits":  [0.0123, 0.0353],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "19", "3D", "RC"): {
        "B_initial": -0.00034,
        "B_limits":  [-0.0031, 0.0025],
        "C_initial": 0.01287,
        "C_limits":  [0.0081, 0.0176],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "20", "3D", "RC"): {
        "B_initial": -0.01215,
        "B_limits":  [-0.015, -0.0093],
        "C_initial": -0.00659,
        "C_limits":  [-0.0098, -0.0034],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "21", "3D", "RC"): {
        "B_initial": -0.03585,
        "B_limits":  [-0.0402, -0.0315],
        "C_initial": -0.01385,
        "C_limits":  [-0.0166, -0.0111],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "22", "3D", "RC"): {
        "B_initial": -0.06794,
        "B_limits":  [-0.0735, -0.0624],
        "C_initial": -0.01139,
        "C_limits":  [-0.0146, -0.0081],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "23", "3D", "RC"): {
        "B_initial": -0.1118,
        "B_limits":  [-0.1201, -0.1035],
        "C_initial": 0.00426,
        "C_limits":  [-0.0009, 0.0094],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "25", "3D", "RC"): {
        "B_initial": -0.00636,
        "B_limits":  [-0.0095, -0.0032],
        "C_initial": 0.0244,
        "C_limits":  [0.019, 0.0299],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "26", "3D", "RC"): {
        "B_initial": -0.01821,
        "B_limits":  [-0.0215, -0.0149],
        "C_initial": 0.00506,
        "C_limits":  [0.0011, 0.009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "27", "3D", "RC"): {
        "B_initial": -0.04293,
        "B_limits":  [-0.0478, -0.038],
        "C_initial": 0.00066,
        "C_limits":  [-0.0029, 0.0043],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "28", "3D", "RC"): {
        "B_initial": -0.07648,
        "B_limits":  [-0.0827, -0.0702],
        "C_initial": 0.00758,
        "C_limits":  [0.0037, 0.0114],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "5", "3D", "BC"): {
        "B_initial": -0.275,
        "B_limits":  [-0.4, -0.15],
        "C_initial": 0,
        "C_limits":  [-0.12, 0.12],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "9", "3D", "BC"): {
        "B_initial": -0.15,
        "B_limits":  [-0.25, -0.05],
        "C_initial": 0,
        "C_limits":  [-0.12, 0.12],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "3", "3D", "BC"): {
        "B_initial": -0.127,
        "B_limits":  [-0.25, -0.04],
        "C_initial": 0,
        "C_limits":  [-0.12, 0.12],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "2", "5D"): {
        "B_initial": -0.13289,
        "B_limits":  [-0.48289, 0.21711],
        "C_initial": 0.0174,
        "C_limits":  [-0.2026, 0.2374],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "3", "5D"): {
        "B_initial": -0.17038,
        "B_limits":  [-0.52038, 0.17962],
        "C_initial": 0.0144,
        "C_limits":  [-0.2056, 0.2344],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "4", "5D"): {
        "B_initial": -0.23883,
        "B_limits":  [-0.58883, 0.11117],
        "C_initial": 0.00885,
        "C_limits":  [-0.21115, 0.22885],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "7", "5D"): {
        "B_initial": -0.46214,
        "B_limits":  [-0.81214, -0.11214],
        "C_initial": 0.092881,
        "C_limits":  [-0.12712, 0.31288],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "19", "5D"): {
        "B_initial": -0.26151,
        "B_limits":  [-0.61151, 0.088495],
        "C_initial": 0.045063,
        "C_limits":  [-0.17494, 0.26506],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "26", "5D"): {
        "B_initial": -0.26618,
        "B_limits":  [-0.61618, 0.083818],
        "C_initial": 0.068199,
        "C_limits":  [-0.1518, 0.2882],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "32", "5D"): {
        "B_initial": -0.21141,
        "B_limits":  [-0.56141, 0.13859],
        "C_initial": 0.021657,
        "C_limits":  [-0.19834, 0.24166],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "2", "5D"): {
        "B_initial": -0.19994,
        "B_limits":  [-0.54994, 0.15006],
        "C_initial": 0.02955,
        "C_limits":  [-0.19045, 0.24955],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "5", "5D"): {
        "B_initial": -0.29966,
        "B_limits":  [-0.64966, 0.050344],
        "C_initial": 0.0031,
        "C_limits":  [-0.2169, 0.2231],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "6", "5D"): {
        "B_initial": -0.42264,
        "B_limits":  [-0.77264, -0.07264],
        "C_initial": 0.032575,
        "C_limits":  [-0.18743, 0.25257],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "9", "5D"): {
        "B_initial": -0.10588,
        "B_limits":  [-0.45588, 0.24412],
        "C_initial": 0.013313,
        "C_limits":  [-0.20669, 0.23331],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "10", "5D"): {
        "B_initial": -0.1892,
        "B_limits":  [-0.5392, 0.1608],
        "C_initial": 0.01845,
        "C_limits":  [-0.20155, 0.23845],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "6", "5D"): {
        "B_initial": -0.1,
        "B_limits":  [-0.45, 0.25],
        "C_initial": -0.0007398,
        "C_limits":  [-0.22074, 0.21926],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "8", "5D"): {
        "B_initial": -0.075836,
        "B_limits":  [-0.42584, 0.27416],
        "C_initial": 0.019428,
        "C_limits":  [-0.20057, 0.23943],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "12", "5D"): {
        "B_initial": -0.37631,
        "B_limits":  [-0.72631, -0.026314],
        "C_initial": 0.061446,
        "C_limits":  [-0.15855, 0.28145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "17", "5D"): {
        "B_initial": -0.22141,
        "B_limits":  [-0.57141, 0.12859],
        "C_initial": -0.0045645,
        "C_limits":  [-0.22456, 0.21544],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "23", "5D"): {
        "B_initial": -0.24753,
        "B_limits":  [-0.59753, 0.10247],
        "C_initial": 0.006,
        "C_limits":  [-0.214, 0.226],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "28", "5D"): {
        "B_initial": -0.14184,
        "B_limits":  [-0.49184, 0.20816],
        "C_initial": -0.03233,
        "C_limits":  [-0.25233, 0.18767],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "16", "5D"): {
        "B_initial": -0.16764,
        "B_limits":  [-0.51764, 0.18236],
        "C_initial": -0.022034,
        "C_limits":  [-0.24203, 0.19797],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "28", "5D"): {
        "B_initial": -0.12411,
        "B_limits":  [-0.47411, 0.22589],
        "C_initial": -0.040674,
        "C_limits":  [-0.26067, 0.17933],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "12", "5D"): {
        "B_initial": -0.42189,
        "B_limits":  [-0.77189, -0.071885],
        "C_initial": 0.098347,
        "C_limits":  [-0.12165, 0.31835],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "17", "5D"): {
        "B_initial": -0.22815,
        "B_limits":  [-0.57815, 0.12185],
        "C_initial": 0.036993,
        "C_limits":  [-0.18301, 0.25699],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "18", "5D"): {
        "B_initial": -0.47193,
        "B_limits":  [-0.82193, -0.12193],
        "C_initial": 0.16641,
        "C_limits":  [-0.053587, 0.38641],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "29", "5D"): {
        "B_initial": -0.29351,
        "B_limits":  [-0.64351, 0.056494],
        "C_initial": 0.075806,
        "C_limits":  [-0.14419, 0.29581],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "3", "5D"): {
        "B_initial": -0.16856,
        "B_limits":  [-0.51856, 0.18144],
        "C_initial": 0.02265,
        "C_limits":  [-0.19735, 0.24265],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "5", "5D"): {
        "B_initial": -0.25815,
        "B_limits":  [-0.60815, 0.091849],
        "C_initial": 0.013341,
        "C_limits":  [-0.20666, 0.23334],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "11", "5D"): {
        "B_initial": -0.24827,
        "B_limits":  [-0.59827, 0.10173],
        "C_initial": 0.024102,
        "C_limits":  [-0.1959, 0.2441],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "12", "5D"): {
        "B_initial": -0.44654,
        "B_limits":  [-0.79654, -0.096536],
        "C_initial": 0.1303,
        "C_limits":  [-0.0897, 0.3503],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "20", "5D"): {
        "B_initial": -0.070081,
        "B_limits":  [-0.42008, 0.27992],
        "C_initial": -0.016513,
        "C_limits":  [-0.23651, 0.20349],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "22", "5D"): {
        "B_initial": -0.16884,
        "B_limits":  [-0.51884, 0.18116],
        "C_initial": -0.01185,
        "C_limits":  [-0.23185, 0.20815],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "5", "5D"): {
        "B_initial": -0.2476,
        "B_limits":  [-0.5976, 0.1024],
        "C_initial": 0.04106,
        "C_limits":  [-0.17894, 0.26106],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "10", "5D"): {
        "B_initial": -0.17596,
        "B_limits":  [-0.52596, 0.17404],
        "C_initial": 0.010468,
        "C_limits":  [-0.20953, 0.23047],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "11", "5D"): {
        "B_initial": -0.25579,
        "B_limits":  [-0.60579, 0.094206],
        "C_initial": 0.0267,
        "C_limits":  [-0.1933, 0.2467],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "12", "5D"): {
        "B_initial": -0.40797,
        "B_limits":  [-0.75797, -0.057969],
        "C_initial": 0.059714,
        "C_limits":  [-0.16029, 0.27971],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "18", "5D"): {
        "B_initial": -0.3351,
        "B_limits":  [-0.6851, 0.014904],
        "C_initial": 0.039191,
        "C_limits":  [-0.18081, 0.25919],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "24", "5D"): {
        "B_initial": -0.33523,
        "B_limits":  [-0.68523, 0.014774],
        "C_initial": 0.075806,
        "C_limits":  [-0.14419, 0.29581],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "34", "5D"): {
        "B_initial": -0.11934,
        "B_limits":  [-0.46934, 0.23066],
        "C_initial": -0.023247,
        "C_limits":  [-0.24325, 0.19675],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "8", "5D"): {
        "B_initial": -0.1582,
        "B_limits":  [-0.5082, 0.1918],
        "C_initial": -0.0114,
        "C_limits":  [-0.2314, 0.2086],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "7", "5D"): {
        "B_initial": -0.49857,
        "B_limits":  [-0.84857, -0.14857],
        "C_initial": 0.11065,
        "C_limits":  [-0.10935, 0.33065],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "13", "5D"): {
        "B_initial": -0.32337,
        "B_limits":  [-0.67337, 0.026633],
        "C_initial": 0.064449,
        "C_limits":  [-0.15555, 0.28445],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "14", "5D"): {
        "B_initial": -0.54972,
        "B_limits":  [-0.89972, -0.19972],
        "C_initial": 0.1991,
        "C_limits":  [-0.020901, 0.4191],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "19", "5D"): {
        "B_initial": -0.2079,
        "B_limits":  [-0.5579, 0.1421],
        "C_initial": 0.017775,
        "C_limits":  [-0.20222, 0.23778],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "20", "5D"): {
        "B_initial": -0.37298,
        "B_limits":  [-0.72298, -0.022977],
        "C_initial": 0.10003,
        "C_limits":  [-0.11997, 0.32003],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "25", "5D"): {
        "B_initial": -0.17286,
        "B_limits":  [-0.52286, 0.17714],
        "C_initial": -0.0069,
        "C_limits":  [-0.2269, 0.2131],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "29", "5D"): {
        "B_initial": -0.0068,
        "B_limits":  [-0.3568, 0.3432],
        "C_initial": -5.0005e-05,
        "C_limits":  [-0.22005, 0.21995],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "4", "5D"): {
        "B_initial": -0.20833,
        "B_limits":  [-0.55833, 0.14167],
        "C_initial": 0.015666,
        "C_limits":  [-0.20433, 0.23567],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "5", "5D"): {
        "B_initial": -0.27846,
        "B_limits":  [-0.62846, 0.071542],
        "C_initial": 0.00545,
        "C_limits":  [-0.21455, 0.22545],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "8", "5D"): {
        "B_initial": -0.053289,
        "B_limits":  [-0.40329, 0.29671],
        "C_initial": -0.0042,
        "C_limits":  [-0.2242, 0.2158],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "9", "5D"): {
        "B_initial": -0.13356,
        "B_limits":  [-0.48356, 0.21644],
        "C_initial": -0.00735,
        "C_limits":  [-0.22735, 0.21265],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "11", "5D"): {
        "B_initial": -0.26403,
        "B_limits":  [-0.61403, 0.085965],
        "C_initial": 0.018274,
        "C_limits":  [-0.20173, 0.23827],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "12", "5D"): {
        "B_initial": -0.44656,
        "B_limits":  [-0.79656, -0.096556],
        "C_initial": 0.11048,
        "C_limits":  [-0.10952, 0.33048],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "17", "5D"): {
        "B_initial": -0.26329,
        "B_limits":  [-0.61329, 0.086712],
        "C_initial": 0.016814,
        "C_limits":  [-0.20319, 0.23681],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "18", "5D"): {
        "B_initial": -0.43691,
        "B_limits":  [-0.78691, -0.086909],
        "C_initial": 0.13328,
        "C_limits":  [-0.086722, 0.35328],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "29", "5D"): {
        "B_initial": -0.25853,
        "B_limits":  [-0.60853, 0.091469],
        "C_initial": 0.060212,
        "C_limits":  [-0.15979, 0.28021],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "4", "5D"): {
        "B_initial": -0.24671,
        "B_limits":  [-0.59671, 0.10329],
        "C_initial": 0.018589,
        "C_limits":  [-0.20141, 0.23859],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "8", "5D"): {
        "B_initial": -0.10838,
        "B_limits":  [-0.45838, 0.24162],
        "C_initial": -0.00395,
        "C_limits":  [-0.22395, 0.21605],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "10", "5D"): {
        "B_initial": -0.30278,
        "B_limits":  [-0.65278, 0.047225],
        "C_initial": 0.017453,
        "C_limits":  [-0.20255, 0.23745],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "12", "5D"): {
        "B_initial": -0.05425,
        "B_limits":  [-0.40425, 0.29575],
        "C_initial": -0.014726,
        "C_limits":  [-0.23473, 0.20527],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "13", "5D"): {
        "B_initial": -0.093701,
        "B_limits":  [-0.4437, 0.2563],
        "C_initial": -0.02539,
        "C_limits":  [-0.24539, 0.19461],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "18", "5D"): {
        "B_initial": -0.068118,
        "B_limits":  [-0.41812, 0.28188],
        "C_initial": -0.040049,
        "C_limits":  [-0.26005, 0.17995],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "20", "5D"): {
        "B_initial": -0.25266,
        "B_limits":  [-0.60266, 0.097344],
        "C_initial": 0.05445,
        "C_limits":  [-0.16555, 0.27445],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "13", "5D"): {
        "B_initial": -0.079779,
        "B_limits":  [-0.33, 0.17],
        "C_initial": -0.036795,
        "C_limits":  [-0.22, 0.14],
        "fit_range_lower": 15,
        "fit_range_upper": 345,
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "18", "5D"): {
        "B_initial": -0.038277,
        "B_limits":  [-0.38828, 0.31172],
        "C_initial": -0.071065,
        "C_limits":  [-0.29106, 0.14894],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "22", "5D"): {
        "B_initial": -0.00775,
        "B_limits":  [-0.35775, 0.34225],
        "C_initial": -0.036727,
        "C_limits":  [-0.25673, 0.18327],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "1", "5D"): {
        "B_initial": -0.067401,
        "B_limits":  [-0.4174, 0.2826],
        "C_initial": -0.0126,
        "C_limits":  [-0.2326, 0.2074],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "3", "5D"): {
        "B_initial": -0.18122,
        "B_limits":  [-0.53122, 0.16878],
        "C_initial": -0.019314,
        "C_limits":  [-0.23931, 0.20069],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "8", "5D"): {
        "B_initial": -0.14386,
        "B_limits":  [-0.49386, 0.20614],
        "C_initial": -0.01965,
        "C_limits":  [-0.23965, 0.20035],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "13", "5D"): {
        "B_initial": -0.10192,
        "B_limits":  [-0.45192, 0.24808],
        "C_initial": -0.013194,
        "C_limits":  [-0.23319, 0.20681],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "9", "5D"): {
        "B_initial": -0.14254,
        "B_limits":  [-0.49254, 0.20746],
        "C_initial": -0.013675,
        "C_limits":  [-0.23367, 0.20633],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "14", "5D"): {
        "B_initial": -0.039685,
        "B_limits":  [-0.38968, 0.31032],
        "C_initial": -0.0309,
        "C_limits":  [-0.2509, 0.1891],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "15", "5D"): {
        "B_initial": -0.086037,
        "B_limits":  [-0.43604, 0.26396],
        "C_initial": -0.024525,
        "C_limits":  [-0.24453, 0.19547],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "20", "5D"): {
        "B_initial": -0.029128,
        "B_limits":  [-0.37913, 0.32087],
        "C_initial": -0.0103,
        "C_limits":  [-0.2303, 0.2097],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "27", "5D"): {
        "B_initial": -0.085586,
        "B_limits":  [-0.43559, 0.26441],
        "C_initial": -0.017689,
        "C_limits":  [-0.23769, 0.20231],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "34", "5D"): {
        "B_initial": -0.17331,
        "B_limits":  [-0.52331, 0.17669],
        "C_initial": 0.0207,
        "C_limits":  [-0.1993, 0.2407],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "16", "5D"): {
        "B_initial": -0.010278,
        "B_limits":  [-0.36028, 0.33972],
        "C_initial": -0.0013288,
        "C_limits":  [-0.22133, 0.21867],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "21", "5D"): {
        "B_initial": -0.034463,
        "B_limits":  [-0.38446, 0.31554],
        "C_initial": -0.0015,
        "C_limits":  [-0.2215, 0.2185],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "23", "5D"): {
        "B_initial": -0.093951,
        "B_limits":  [-0.44395, 0.25605],
        "C_initial": -0.037233,
        "C_limits":  [-0.25723, 0.18277],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "9", "5D"): {
        "B_initial": -0.10061,
        "B_limits":  [-0.45061, 0.24939],
        "C_initial": -0.03015,
        "C_limits":  [-0.25015, 0.18985],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "14", "5D"): {
        "B_initial": -0.024547,
        "B_limits":  [-0.37455, 0.32545],
        "C_initial": -0.013681,
        "C_limits":  [-0.23368, 0.20632],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "19", "5D"): {
        "B_initial": -0.006498,
        "B_limits":  [-0.3565, 0.3435],
        "C_initial": 0.016308,
        "C_limits":  [-0.20369, 0.23631],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "2", "5D", "RC"): {
        "B_initial": -0.10684,
        "B_limits":  [-0.45684, 0.24316],
        "C_initial": 0.0141,
        "C_limits":  [-0.2059, 0.2341],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "3", "5D", "RC"): {
        "B_initial": -0.1333,
        "B_limits":  [-0.4833, 0.2167],
        "C_initial": 0.009,
        "C_limits":  [-0.211, 0.229],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "4", "5D", "RC"): {
        "B_initial": -0.19062,
        "B_limits":  [-0.54062, 0.15938],
        "C_initial": -0.00035002,
        "C_limits":  [-0.22035, 0.21965],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "7", "5D", "RC"): {
        "B_initial": -0.34809,
        "B_limits":  [-0.69809, 0.0019129],
        "C_initial": 0.064599,
        "C_limits":  [-0.1554, 0.2846],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "26", "5D", "RC"): {
        "B_initial": -0.17491,
        "B_limits":  [-0.52491, 0.17509],
        "C_initial": 0.047094,
        "C_limits":  [-0.17291, 0.26709],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "32", "5D", "RC"): {
        "B_initial": -0.13896,
        "B_limits":  [-0.48896, 0.21104],
        "C_initial": 0.005772,
        "C_limits":  [-0.21423, 0.22577],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "2", "5D", "RC"): {
        "B_initial": -0.1685,
        "B_limits":  [-0.5185, 0.1815],
        "C_initial": 0.027,
        "C_limits":  [-0.193, 0.247],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "5", "5D", "RC"): {
        "B_initial": -0.22771,
        "B_limits":  [-0.57771, 0.12229],
        "C_initial": -0.0024,
        "C_limits":  [-0.2224, 0.2176],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "6", "5D", "RC"): {
        "B_initial": -0.32239,
        "B_limits":  [-0.67239, 0.027614],
        "C_initial": 0.013055,
        "C_limits":  [-0.20695, 0.23305],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "9", "5D", "RC"): {
        "B_initial": -0.057764,
        "B_limits":  [-0.40776, 0.29224],
        "C_initial": 0.0039208,
        "C_limits":  [-0.21608, 0.22392],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "8", "5D", "RC"): {
        "B_initial": -0.044333,
        "B_limits":  [-0.39433, 0.30567],
        "C_initial": 0.018133,
        "C_limits":  [-0.20187, 0.23813],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "12", "5D", "RC"): {
        "B_initial": -0.28078,
        "B_limits":  [-0.63078, 0.069221],
        "C_initial": 0.039795,
        "C_limits":  [-0.18021, 0.25979],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "17", "5D", "RC"): {
        "B_initial": -0.14329,
        "B_limits":  [-0.49329, 0.20671],
        "C_initial": -0.018067,
        "C_limits":  [-0.23807, 0.20193],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "18", "5D", "RC"): {
        "B_initial": -0.23885,
        "B_limits":  [-0.58885, 0.11115],
        "C_initial": 0.018454,
        "C_limits":  [-0.20155, 0.23845],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "28", "5D", "RC"): {
        "B_initial": -0.078881,
        "B_limits":  [-0.42888, 0.27112],
        "C_initial": -0.041441,
        "C_limits":  [-0.26144, 0.17856],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "11", "5D", "RC"): {
        "B_initial": -0.28383,
        "B_limits":  [-0.63383, 0.066173],
        "C_initial": -0.0019316,
        "C_limits":  [-0.22193, 0.21807],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "23", "5D", "RC"): {
        "B_initial": -0.16905,
        "B_limits":  [-0.51905, 0.18095],
        "C_initial": -0.035418,
        "C_limits":  [-0.25542, 0.18458],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "28", "5D", "RC"): {
        "B_initial": -0.068718,
        "B_limits":  [-0.41872, 0.28128],
        "C_initial": -0.045956,
        "C_limits":  [-0.26596, 0.17404],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "29", "5D", "RC"): {
        "B_initial": -0.14905,
        "B_limits":  [-0.49905, 0.20095],
        "C_initial": -0.0119,
        "C_limits":  [-0.2319, 0.2081],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "6", "5D", "RC"): {
        "B_initial": -0.32455,
        "B_limits":  [-0.67455, 0.025449],
        "C_initial": 0.029898,
        "C_limits":  [-0.1901, 0.2499],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "12", "5D", "RC"): {
        "B_initial": -0.31073,
        "B_limits":  [-0.66073, 0.039266],
        "C_initial": 0.067133,
        "C_limits":  [-0.15287, 0.28713],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "17", "5D", "RC"): {
        "B_initial": -0.14907,
        "B_limits":  [-0.49907, 0.20093],
        "C_initial": 0.020086,
        "C_limits":  [-0.19991, 0.24009],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "18", "5D", "RC"): {
        "B_initial": -0.34864,
        "B_limits":  [-0.69864, 0.0013637],
        "C_initial": 0.12901,
        "C_limits":  [-0.090993, 0.34901],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "23", "5D", "RC"): {
        "B_initial": -0.20471,
        "B_limits":  [-0.55471, 0.14529],
        "C_initial": 0.03085,
        "C_limits":  [-0.18915, 0.25085],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "29", "5D", "RC"): {
        "B_initial": -0.20568,
        "B_limits":  [-0.55568, 0.14432],
        "C_initial": 0.054034,
        "C_limits":  [-0.16597, 0.27403],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "3", "5D", "RC"): {
        "B_initial": -0.13078,
        "B_limits":  [-0.48078, 0.21922],
        "C_initial": 0.0174,
        "C_limits":  [-0.2026, 0.2374],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "5", "5D", "RC"): {
        "B_initial": -0.19146,
        "B_limits":  [-0.54146, 0.15854],
        "C_initial": 0.0014493,
        "C_limits":  [-0.21855, 0.22145],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "6", "5D", "RC"): {
        "B_initial": -0.34001,
        "B_limits":  [-0.69001, 0.0099865],
        "C_initial": 0.040614,
        "C_limits":  [-0.17939, 0.26061],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "11", "5D", "RC"): {
        "B_initial": -0.16965,
        "B_limits":  [-0.51965, 0.18035],
        "C_initial": 0.008832,
        "C_limits":  [-0.21117, 0.22883],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "12", "5D", "RC"): {
        "B_initial": -0.32379,
        "B_limits":  [-0.67379, 0.026213],
        "C_initial": 0.094917,
        "C_limits":  [-0.12508, 0.31492],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "20", "5D", "RC"): {
        "B_initial": -0.034239,
        "B_limits":  [-0.38424, 0.31576],
        "C_initial": -0.01919,
        "C_limits":  [-0.23919, 0.20081],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "22", "5D", "RC"): {
        "B_initial": -0.10506,
        "B_limits":  [-0.45506, 0.24494],
        "C_initial": -0.0252,
        "C_limits":  [-0.2452, 0.1948],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "5", "5D", "RC"): {
        "B_initial": -0.18926,
        "B_limits":  [-0.53926, 0.16074],
        "C_initial": 0.0261,
        "C_limits":  [-0.1939, 0.2461],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "10", "5D", "RC"): {
        "B_initial": -0.12376,
        "B_limits":  [-0.47376, 0.22624],
        "C_initial": 0.0060645,
        "C_limits":  [-0.21394, 0.22606],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "11", "5D", "RC"): {
        "B_initial": -0.19354,
        "B_limits":  [-0.54354, 0.15646],
        "C_initial": 0.0063,
        "C_limits":  [-0.2137, 0.2263],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "12", "5D", "RC"): {
        "B_initial": -0.31801,
        "B_limits":  [-0.66801, 0.031988],
        "C_initial": 0.036978,
        "C_limits":  [-0.18302, 0.25698],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "18", "5D", "RC"): {
        "B_initial": -0.23725,
        "B_limits":  [-0.58725, 0.11275],
        "C_initial": 0.0159,
        "C_limits":  [-0.2041, 0.2359],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "24", "5D", "RC"): {
        "B_initial": -0.2372,
        "B_limits":  [-0.5872, 0.1128],
        "C_initial": 0.05512,
        "C_limits":  [-0.16488, 0.27512],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "34", "5D", "RC"): {
        "B_initial": -0.063149,
        "B_limits":  [-0.41315, 0.28685],
        "C_initial": -0.02973,
        "C_limits":  [-0.24973, 0.19027],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "35", "5D", "RC"): {
        "B_initial": -0.18107,
        "B_limits":  [-0.53107, 0.16893],
        "C_initial": 0.02175,
        "C_limits":  [-0.19825, 0.24175],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "7", "5D", "RC"): {
        "B_initial": -0.39867,
        "B_limits":  [-0.74867, -0.048671],
        "C_initial": 0.075741,
        "C_limits":  [-0.14426, 0.29574],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "14", "5D", "RC"): {
        "B_initial": -0.4252,
        "B_limits":  [-0.7752, -0.075204],
        "C_initial": 0.15725,
        "C_limits":  [-0.062754, 0.37725],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "19", "5D", "RC"): {
        "B_initial": -0.1402,
        "B_limits":  [-0.4902, 0.2098],
        "C_initial": 0.003627,
        "C_limits":  [-0.21637, 0.22363],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "20", "5D", "RC"): {
        "B_initial": -0.28034,
        "B_limits":  [-0.63034, 0.069665],
        "C_initial": 0.07343,
        "C_limits":  [-0.14657, 0.29343],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "26", "5D", "RC"): {
        "B_initial": -0.1919,
        "B_limits":  [-0.5419, 0.1581],
        "C_initial": 0.0090326,
        "C_limits":  [-0.21097, 0.22903],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "4", "5D", "RC"): {
        "B_initial": -0.16146,
        "B_limits":  [-0.51146, 0.18854],
        "C_initial": 0.0082493,
        "C_limits":  [-0.21175, 0.22825],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "5", "5D", "RC"): {
        "B_initial": -0.21254,
        "B_limits":  [-0.56254, 0.13746],
        "C_initial": -0.0003,
        "C_limits":  [-0.2203, 0.2197],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "6", "5D", "RC"): {
        "B_initial": -0.35245,
        "B_limits":  [-0.70245, -0.0024518],
        "C_initial": 0.03994,
        "C_limits":  [-0.18006, 0.25994],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "9", "5D", "RC"): {
        "B_initial": -0.094146,
        "B_limits":  [-0.44415, 0.25585],
        "C_initial": -0.01635,
        "C_limits":  [-0.23635, 0.20365],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "11", "5D", "RC"): {
        "B_initial": -0.19373,
        "B_limits":  [-0.54373, 0.15627],
        "C_initial": 0.0033875,
        "C_limits":  [-0.21661, 0.22339],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "12", "5D", "RC"): {
        "B_initial": -0.34491,
        "B_limits":  [-0.69491, 0.005092],
        "C_initial": 0.078281,
        "C_limits":  [-0.14172, 0.29828],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "18", "5D", "RC"): {
        "B_initial": -0.32813,
        "B_limits":  [-0.67813, 0.021872],
        "C_initial": 0.10114,
        "C_limits":  [-0.11886, 0.32114],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "29", "5D", "RC"): {
        "B_initial": -0.18328,
        "B_limits":  [-0.53328, 0.16672],
        "C_initial": 0.043812,
        "C_limits":  [-0.17619, 0.26381],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "4", "5D", "RC"): {
        "B_initial": -0.19856,
        "B_limits":  [-0.54856, 0.15144],
        "C_initial": 0.0097631,
        "C_limits":  [-0.21024, 0.22976],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "10", "5D", "RC"): {
        "B_initial": -0.22915,
        "B_limits":  [-0.57915, 0.12085],
        "C_initial": -0.00069762,
        "C_limits":  [-0.2207, 0.2193],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "12", "5D", "RC"): {
        "B_initial": -0.02641,
        "B_limits":  [-0.37641, 0.32359],
        "C_initial": -0.016277,
        "C_limits":  [-0.23628, 0.20372],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "13", "5D", "RC"): {
        "B_initial": -0.052866,
        "B_limits":  [-0.40287, 0.29713],
        "C_initial": -0.029483,
        "C_limits":  [-0.24948, 0.19052],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "15", "5D", "RC"): {
        "B_initial": -0.17456,
        "B_limits":  [-0.52456, 0.17544],
        "C_initial": 0.0073601,
        "C_limits":  [-0.21264, 0.22736],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "18", "5D", "RC"): {
        "B_initial": -0.02743,
        "B_limits":  [-0.37743, 0.32257],
        "C_initial": -0.04359,
        "C_limits":  [-0.26359, 0.17641],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "20", "5D", "RC"): {
        "B_initial": -0.18325,
        "B_limits":  [-0.53325, 0.16675],
        "C_initial": 0.04425,
        "C_limits":  [-0.17575, 0.26425],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "13", "5D", "RC"): {
        "B_initial": -0.04573,
        "B_limits":  [-0.30, 0.20],
        "C_initial": -0.039373,
        "C_limits":  [-0.22, 0.14],
        "fit_range_lower": 15,
        "fit_range_upper": 345,
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "15", "5D", "RC"): {
        "B_initial": -0.25965,
        "B_limits":  [-0.60965, 0.09035],
        "C_initial": -0.10905,
        "C_limits":  [-0.32905, 0.11095],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "18", "5D", "RC"): {
        "B_initial": -0.01165,
        "B_limits":  [-0.36165, 0.33835],
        "C_initial": -0.073822,
        "C_limits":  [-0.29382, 0.14618],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "20", "5D", "RC"): {
        "B_initial": -0.12161,
        "B_limits":  [-0.47161, 0.22839],
        "C_initial": -0.0265,
        "C_limits":  [-0.2465, 0.1935],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "22", "5D", "RC"): {
        "B_initial": 0.0087,
        "B_limits":  [-0.3413, 0.3587],
        "C_initial": -0.037079,
        "C_limits":  [-0.25708, 0.18292],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "1", "5D", "RC"): {
        "B_initial": -0.054763,
        "B_limits":  [-0.40476, 0.29524],
        "C_initial": -0.01465,
        "C_limits":  [-0.23465, 0.20535],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "3", "5D", "RC"): {
        "B_initial": -0.14404,
        "B_limits":  [-0.49404, 0.20596],
        "C_initial": -0.023989,
        "C_limits":  [-0.24399, 0.19601],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "8", "5D", "RC"): {
        "B_initial": -0.10652,
        "B_limits":  [-0.45652, 0.24348],
        "C_initial": -0.031127,
        "C_limits":  [-0.25113, 0.18887],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("13", "15", "5D", "RC"): {
        "B_initial": -0.26967,
        "B_limits":  [-0.61967, 0.080328],
        "C_initial": 0.087879,
        "C_limits":  [-0.13212, 0.30788],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "9", "5D", "RC"): {
        "B_initial": -0.10492,
        "B_limits":  [-0.45492, 0.24508],
        "C_initial": -0.018494,
        "C_limits":  [-0.23849, 0.20151],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "10", "5D", "RC"): {
        "B_initial": -0.096966,
        "B_limits":  [-0.44697, 0.25303],
        "C_initial": -0.0089,
        "C_limits":  [-0.2289, 0.2111],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "11", "5D", "RC"): {
        "B_initial": -0.19565,
        "B_limits":  [-0.54565, 0.15435],
        "C_initial": -0.00235,
        "C_limits":  [-0.22235, 0.21765],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "12", "5D", "RC"): {
        "B_initial": -0.33335,
        "B_limits":  [-0.68335, 0.016648],
        "C_initial": 0.077603,
        "C_limits":  [-0.1424, 0.2976],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "15", "5D", "RC"): {
        "B_initial": -0.046748,
        "B_limits":  [-0.39675, 0.30325],
        "C_initial": -0.028176,
        "C_limits":  [-0.24818, 0.19182],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "18", "5D", "RC"): {
        "B_initial": -0.31354,
        "B_limits":  [-0.66354, 0.036459],
        "C_initial": 0.084898,
        "C_limits":  [-0.1351, 0.3049],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "20", "5D", "RC"): {
        "B_initial": -0.0085,
        "B_limits":  [-0.3585, 0.3415],
        "C_initial": -0.01155,
        "C_limits":  [-0.23155, 0.20845],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "21", "5D", "RC"): {
        "B_initial": -0.054183,
        "B_limits":  [-0.40418, 0.29582],
        "C_initial": -0.036341,
        "C_limits":  [-0.25634, 0.18366],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "27", "5D", "RC"): {
        "B_initial": -0.048245,
        "B_limits":  [-0.39825, 0.30175],
        "C_initial": -0.022205,
        "C_limits":  [-0.2422, 0.1978],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "16", "5D", "RC"): {
        "B_initial": -0.0005,
        "B_limits":  [-0.3505, 0.3495],
        "C_initial": -0.0017982,
        "C_limits":  [-0.2218, 0.2182],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "21", "5D", "RC"): {
        "B_initial": -0.01755,
        "B_limits":  [-0.36755, 0.33245],
        "C_initial": -0.00255,
        "C_limits":  [-0.22255, 0.21745],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "9", "5D", "RC"): {
        "B_initial": -0.065897,
        "B_limits":  [-0.4159, 0.2841],
        "C_initial": -0.034677,
        "C_limits":  [-0.25468, 0.18532],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "12", "5D", "RC"): {
        "B_initial": -0.30366,
        "B_limits":  [-0.65366, 0.04634],
        "C_initial": 0.076883,
        "C_limits":  [-0.14312, 0.29688],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "14", "5D", "RC"): {
        "B_initial": -0.0049987,
        "B_limits":  [-0.355, 0.345],
        "C_initial": -0.015043,
        "C_limits":  [-0.23504, 0.20496],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "19", "5D", "RC"): {
        "B_initial": 0.0037499,
        "B_limits":  [-0.34625, 0.35375],
        "C_initial": 0.016707,
        "C_limits":  [-0.20329, 0.23671],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("1", "32", "5D", "BC"): {
        "B_initial": -0.12141,
        "B_limits":  [-0.47141, 0.22859],
        "C_initial": 0.010453,
        "C_limits":  [-0.20955, 0.23045],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("2", "6", "5D", "BC"): {
        "B_initial": -0.29002,
        "B_limits":  [-0.64002, 0.059983],
        "C_initial": 0.0025,
        "C_limits":  [-0.2175, 0.2225],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "12", "5D", "BC"): {
        "B_initial": -0.31338,
        "B_limits":  [-0.66338, 0.036619],
        "C_initial": 0.033213,
        "C_limits":  [-0.18679, 0.25321],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "17", "5D", "BC"): {
        "B_initial": -0.15116,
        "B_limits":  [-0.50116, 0.19884],
        "C_initial": -0.026924,
        "C_limits":  [-0.24692, 0.19308],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "18", "5D", "BC"): {
        "B_initial": -0.24917,
        "B_limits":  [-0.59917, 0.10083],
        "C_initial": 0.01843,
        "C_limits":  [-0.20157, 0.23843],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("3", "28", "5D", "BC"): {
        "B_initial": -0.079656,
        "B_limits":  [-0.42966, 0.27034],
        "C_initial": -0.046731,
        "C_limits":  [-0.26673, 0.17327],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("4", "29", "5D", "BC"): {
        "B_initial": -0.16249,
        "B_limits":  [-0.51249, 0.18751],
        "C_initial": -0.0044812,
        "C_limits":  [-0.22448, 0.21552],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "6", "5D", "BC"): {
        "B_initial": -0.39284,
        "B_limits":  [-0.74284, -0.04284],
        "C_initial": 0.01188,
        "C_limits":  [-0.20812, 0.23188],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "12", "5D", "BC"): {
        "B_initial": -0.35195,
        "B_limits":  [-0.70195, -0.0019499],
        "C_initial": 0.06154,
        "C_limits":  [-0.15846, 0.28154],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "18", "5D", "BC"): {
        "B_initial": -0.38102,
        "B_limits":  [-0.73102, -0.03102],
        "C_initial": 0.12497,
        "C_limits":  [-0.095029, 0.34497],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "23", "5D", "BC"): {
        "B_initial": -0.21528,
        "B_limits":  [-0.56528, 0.13472],
        "C_initial": 0.026061,
        "C_limits":  [-0.19394, 0.24606],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("5", "29", "5D", "BC"): {
        "B_initial": -0.21003,
        "B_limits":  [-0.56003, 0.13997],
        "C_initial": 0.052711,
        "C_limits":  [-0.16729, 0.27271],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "3", "5D", "BC"): {
        "B_initial": -0.12869,
        "B_limits":  [-0.47869, 0.22131],
        "C_initial": 0.028415,
        "C_limits":  [-0.19158, 0.24842],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "11", "5D", "BC"): {
        "B_initial": -0.17624,
        "B_limits":  [-0.52624, 0.17376],
        "C_initial": 0.015666,
        "C_limits":  [-0.20433, 0.23567],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("6", "12", "5D", "BC"): {
        "B_initial": -0.3715,
        "B_limits":  [-0.7215, -0.021498],
        "C_initial": 0.087159,
        "C_limits":  [-0.13284, 0.30716],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "5", "5D", "BC"): {
        "B_initial": -0.275,
        "B_limits":  [-0.4, -0.15],
        "C_initial": 0,
        "C_limits":  [-0.12, 0.12],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "11", "5D", "BC"): {
        "B_initial": -0.18766,
        "B_limits":  [-0.53766, 0.16234],
        "C_initial": 0.030158,
        "C_limits":  [-0.18984, 0.25016],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "12", "5D", "BC"): {
        "B_initial": -0.36653,
        "B_limits":  [-0.71653, -0.016527],
        "C_initial": 0.035636,
        "C_limits":  [-0.18436, 0.25564],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "18", "5D", "BC"): {
        "B_initial": -0.27977,
        "B_limits":  [-0.62977, 0.070229],
        "C_initial": 0.002877,
        "C_limits":  [-0.21712, 0.22288],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "24", "5D", "BC"): {
        "B_initial": -0.25964,
        "B_limits":  [-0.60964, 0.090362],
        "C_initial": 0.042042,
        "C_limits":  [-0.17796, 0.26204],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("7", "34", "5D", "BC"): {
        "B_initial": -0.061653,
        "B_limits":  [-0.41165, 0.28835],
        "C_initial": -0.026836,
        "C_limits":  [-0.24684, 0.19316],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("8", "9", "5D", "BC"): {
        "B_initial": -0.15,
        "B_limits":  [-0.25, -0.05],
        "C_initial": 0,
        "C_limits":  [-0.12, 0.12],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "7", "5D", "BC"): {
        "B_initial": -0.42463,
        "B_limits":  [-0.77463, -0.074633],
        "C_initial": 0.052451,
        "C_limits":  [-0.16755, 0.27245],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "14", "5D", "BC"): {
        "B_initial": -0.44579,
        "B_limits":  [-0.79579, -0.095795],
        "C_initial": 0.14486,
        "C_limits":  [-0.075136, 0.36486],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "19", "5D", "BC"): {
        "B_initial": -0.14174,
        "B_limits":  [-0.49174, 0.20826],
        "C_initial": 0.0025342,
        "C_limits":  [-0.21747, 0.22253],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "20", "5D", "BC"): {
        "B_initial": -0.28515,
        "B_limits":  [-0.63515, 0.06485],
        "C_initial": 0.080434,
        "C_limits":  [-0.13957, 0.30043],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("9", "25", "5D", "BC"): {
        "B_initial": -0.12582,
        "B_limits":  [-0.47582, 0.22418],
        "C_initial": -0.028648,
        "C_limits":  [-0.24865, 0.19135],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "11", "5D", "BC"): {
        "B_initial": -0.19393,
        "B_limits":  [-0.54393, 0.15607],
        "C_initial": 0.016102,
        "C_limits":  [-0.2039, 0.2361],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "12", "5D", "BC"): {
        "B_initial": -0.36507,
        "B_limits":  [-0.71507, -0.015069],
        "C_initial": 0.070063,
        "C_limits":  [-0.14994, 0.29006],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "18", "5D", "BC"): {
        "B_initial": -0.34585,
        "B_limits":  [-0.69585, 0.0041513],
        "C_initial": 0.099196,
        "C_limits":  [-0.1208, 0.3192],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("10", "29", "5D", "BC"): {
        "B_initial": -0.18853,
        "B_limits":  [-0.53853, 0.16147],
        "C_initial": 0.047184,
        "C_limits":  [-0.17282, 0.26718],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "10", "5D", "BC"): {
        "B_initial": -0.25398,
        "B_limits":  [-0.60398, 0.096018],
        "C_initial": 0.0042025,
        "C_limits":  [-0.2158, 0.2242],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "13", "5D", "BC"): {
        "B_initial": -0.059894,
        "B_limits":  [-0.40989, 0.29011],
        "C_initial": -0.037434,
        "C_limits":  [-0.25743, 0.18257],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("11", "20", "5D", "BC"): {
        "B_initial": -0.19724,
        "B_limits":  [-0.54724, 0.15276],
        "C_initial": 0.045,
        "C_limits":  [-0.175, 0.265],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("12", "13", "5D", "BC"): {
        "B_initial": -0.057025,
        "B_limits":  [-0.31, 0.19],
        "C_initial": -0.040158,
        "C_limits":  [-0.22, 0.14],
        "fit_range_lower": 15,
        "fit_range_upper": 345,
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "9", "5D", "BC"): {
        "B_initial": -0.10861,
        "B_limits":  [-0.45861, 0.24139],
        "C_initial": -0.018068,
        "C_limits":  [-0.23807, 0.20193],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "11", "5D", "BC"): {
        "B_initial": -0.1926,
        "B_limits":  [-0.5426, 0.1574],
        "C_initial": 0.014647,
        "C_limits":  [-0.20535, 0.23465],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "15", "5D", "BC"): {
        "B_initial": -0.055386,
        "B_limits":  [-0.40539, 0.29461],
        "C_initial": -0.030457,
        "C_limits":  [-0.25046, 0.18954],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("14", "20", "5D", "BC"): {
        "B_initial": -2.1234e-08,
        "B_limits":  [-0.35, 0.35],
        "C_initial": -0.0070626,
        "C_limits":  [-0.22706, 0.21294],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "3", "5D", "BC"): {
        "B_initial": -0.127,
        "B_limits":  [-0.25, -0.04],
        "C_initial": 0,
        "C_limits":  [-0.12, 0.12],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "16", "5D", "BC"): {
        "B_initial": 0.016352,
        "B_limits":  [-0.33365, 0.36635],
        "C_initial": 0.0007165,
        "C_limits":  [-0.21928, 0.22072],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("15", "21", "5D", "BC"): {
        "B_initial": -0.015298,
        "B_limits":  [-0.3653, 0.3347],
        "C_initial": -0.015973,
        "C_limits":  [-0.23597, 0.20403],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("16", "9", "5D", "BC"): {
        "B_initial": -0.06369,
        "B_limits":  [-0.41369, 0.28631],
        "C_initial": -0.036665,
        "C_limits":  [-0.25666, 0.18334],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    },
    ("17", "14", "5D", "BC"): {
        "B_initial": -0.007326,
        "B_limits":  [-0.35733, 0.34267],
        "C_initial": -0.017429,
        "C_limits":  [-0.23743, 0.20257],
        "Allow_Multiple_Fits":   True,
        "Allow_Multiple_Fits_C": True
    }
}
