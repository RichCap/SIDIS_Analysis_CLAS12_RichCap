# Run-local guide for sub_z_3 BC_RC_Bayesian. Shared manual and spline files are not edited.
# BC_RC selects ('q','z','3D','BC'), then ('q','z','BC'), then untagged ('q','z').
# The spline file has 5 ('q','z','3D','BC') keys and 4 ('q','z','BC') keys. Those numeric windows have median widths about 0.018 in B and 0.009 in C, including the one-sided ('1','9','BC') window [-0.02, 0].
# Untagged keys are the fallback for the other bins: 320 B limits are [None, None] and 178 of 183 numeric B windows have width at most 0.3. Those windows are tight enough to pin fits, so this guide starts from the manual initializer.
import importlib.util
spec = importlib.util.spec_from_file_location("manual_phi_init", "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Phi_h_Fit_Parameters_Initialize.py")
manual_phi_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manual_phi_init)
special_fit_parameters_set = dict(manual_phi_init.special_fit_parameters_set)

# Histogram misses versus a wide cosine. C capped at 0, a negative-only second-pass shrink, or the one-sided ('1','9','BC') corner.
special_fit_parameters_set[('5', '31', '3D', 'BC')] = {'B_initial': 0.0274, 'B_limits': [-0.0726, 0.1274], 'C_initial': 0.0514, 'C_limits': [-0.0486, 0.1514], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '17', '3D', 'BC')] = {'B_initial': -0.0215, 'B_limits': [-0.1215, 0.0785], 'C_initial': -0.0243, 'C_limits': [-0.1243, 0.0757], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
special_fit_parameters_set[('1', '9', '3D', 'BC')] = {'B_initial': 0.0589, 'B_limits': [-0.0411, 0.1589], 'C_initial': 0.0128, 'C_limits': [-0.0872, 0.1128], 'Allow_Multiple_Fits': True, 'Allow_Multiple_Fits_C': True}
