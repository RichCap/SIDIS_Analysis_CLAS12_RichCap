# Spline MC is divided by its unweighted counterpart with ROOT's TH1::Divide.
# AccSpline and the other weight tags are left unchanged.

SPLINE_SUFFIX = "_(Spline)"
CORRECTION_ON = "spline_amplitude_correction=divided_by_unweighted"
CORRECTION_OFF = "spline_amplitude_correction=off"


def divide_spline_active(weight_tag, mode):
    choice = "auto" if(mode in [None, ""]) else str(mode)
    if(choice not in ["auto", "on", "off"]):
        raise ValueError("invalid spline_amplitude_correction: %s" % choice)
    tag = "" if(weight_tag in [None, ""]) else str(weight_tag)
    if(choice == "on"):
        if(tag != "Spline"):
            raise ValueError("spline amplitude correction on requires weight_tag Spline")
        return True
    if(choice == "off"):
        return False
    return tag == "Spline"


def unweighted_spline_counterpart(name):
    # Trailing _(Spline) only. _(AccSpline) does not end with that token.
    text = str(name)
    if(text.endswith(SPLINE_SUFFIX)):
        return text[:-len(SPLINE_SUFFIX)]
    return ""


def correction_metadata(active):
    if(active):
        return CORRECTION_ON
    return CORRECTION_OFF


def output_root_with_weight(path, weight_tag, active):
    tag = "" if(weight_tag in [None, ""]) else str(weight_tag)
    text = str(path)
    if(tag == ""):
        return text
    divide = bool(active) and (tag == "Spline")
    suffix = "_W%s_DivUnw.root" % tag if(divide) else "_W%s.root" % tag
    if(text.endswith(suffix)):
        return text
    if(divide and text.endswith("_W%s.root" % tag)):
        return text[:-5] + "_DivUnw.root"
    if(text.endswith(".root")):
        return text[:-5] + suffix
    return text


def axis_edges_match(left, right):
    if(left.GetNbins() != right.GetNbins()):
        return False
    left_edges = left.GetXbins()
    right_edges = right.GetXbins()
    left_n = 0 if(left_edges is None) else int(left_edges.GetSize())
    right_n = 0 if(right_edges is None) else int(right_edges.GetSize())
    if((left_n > 0) or (right_n > 0)):
        if(left_n != right_n):
            return False
        for index in range(left_n):
            if(abs(float(left_edges[index]) - float(right_edges[index])) > 1e-6):
                return False
        return True
    if(abs(float(left.GetXmin()) - float(right.GetXmin())) > 1e-6):
        return False
    if(abs(float(left.GetXmax()) - float(right.GetXmax())) > 1e-6):
        return False
    return True


def histograms_match_for_divide(weighted, unweighted):
    if((weighted is None) or (unweighted is None)):
        return False
    if(str(weighted.ClassName()) != str(unweighted.ClassName())):
        return False
    if(not axis_edges_match(weighted.GetXaxis(), unweighted.GetXaxis())):
        return False
    if(int(weighted.GetDimension()) >= 2):
        if(not axis_edges_match(weighted.GetYaxis(), unweighted.GetYaxis())):
            return False
    if(int(weighted.GetDimension()) >= 3):
        if(not axis_edges_match(weighted.GetZaxis(), unweighted.GetZaxis())):
            return False
    return True


def divide_spline_histogram(weighted, unweighted):
    # Returns a detached clone, or None when the counterpart cannot be divided.
    # A false return does not replace the input histogram.
    if(not histograms_match_for_divide(weighted, unweighted)):
        return None
    clone = weighted.Clone("%s_DivUnw" % weighted.GetName())
    clone.SetDirectory(0)
    if(not clone.Divide(unweighted)):
        return None
    return clone


def prepare_spline_histogram(weighted, unweighted, active):
    if(not active):
        return weighted
    return divide_spline_histogram(weighted, unweighted)
