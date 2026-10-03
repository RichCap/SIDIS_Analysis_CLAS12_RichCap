# Fitability of a phi_h slice. 24-bin numbers match write_fitability.classify_flags.
# 12-bin thresholds keep the same angular coverage: 60 degrees of central hole, 120 degrees lost, 120 degrees of edge.

def fitability_constants(n_bins):
    if(int(n_bins) == 24):
        return {"center_lo": 8, "center_hi": 16, "center_warn_n": 4, "dropped_warn_n": 8, "edge_allowance": 8, "min_filled": 8}
    if(int(n_bins) == 12):
        return {"center_lo": 4, "center_hi": 8, "center_warn_n": 2, "dropped_warn_n": 4, "edge_allowance": 4, "min_filled": 4}
    raise ValueError("phi fitability is defined for 24 or 12 bins, not %s" % n_bins)


def classify_flags(flags, n_bins=None):
    # flags[i] is True when phi bin i+1 is kept.
    if(n_bins is None):
        n_bins = len(flags)
    constants   = fitability_constants(n_bins)
    center_lo   = constants["center_lo"]
    center_hi   = constants["center_hi"]
    center_warn = constants["center_warn_n"]
    drop_warn   = constants["dropped_warn_n"]
    kept_n      = sum(1 for flag in flags if flag)
    dropped_n   = n_bins - kept_n
    central_n   = sum(1 for index in range(center_lo, center_hi) if(not flags[index]))
    dropped_bins = [index + 1 for index, flag in enumerate(flags) if(not flag)]
    if(kept_n == 0):
        pattern = "empty"
    elif(kept_n == n_bins):
        pattern = "full"
    elif(central_n >= center_warn):
        pattern = "center"
    else:
        prefix = 0
        while((prefix < n_bins) and (not flags[prefix])):
            prefix += 1
        suffix = 0
        while((suffix < n_bins) and (not flags[n_bins - 1 - suffix])):
            suffix += 1
        interior = False
        for index in range(prefix, n_bins - suffix):
            if(not flags[index]):
                interior = True
        if(interior):
            pattern = "scattered"
        else:
            pattern = "edges"
    if(pattern in ("empty", "center")):
        status = "unfit"
    elif((dropped_n > drop_warn) or (pattern == "scattered")):
        status = "fit_warning"
    else:
        status = "fit_ok"
    return pattern, status, kept_n, dropped_n, central_n, dropped_bins


def min_filled_bins(n_bins):
    return fitability_constants(n_bins)["min_filled"]
