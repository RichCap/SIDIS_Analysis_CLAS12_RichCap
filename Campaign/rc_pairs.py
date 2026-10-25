# One-to-one Rad / No_Rad pairing for RC-factor inputs. BC-only No_Rad files are reported and left out.
import os

TOKEN_NO = "_No_Rad_"
TOKEN_RAD = "_Rad_"
PLACE = "_RADTOKEN_"


def radiation_key(path, token):
    base = os.path.basename(str(path))
    if(base.count(token) != 1):
        return None
    return base.replace(token, PLACE, 1)


def pair_rad_nrad(rad_files, nrad_files):
    rad_map = {}
    nrad_map = {}
    bad = []
    for path in rad_files:
        key = radiation_key(path, TOKEN_RAD)
        if(key is None):
            bad.append(path)
            continue
        if(key in rad_map):
            raise ValueError("duplicate Rad identity: %s" % key)
        rad_map[key] = path
    for path in nrad_files:
        key = radiation_key(path, TOKEN_NO)
        if(key is None):
            bad.append(path)
            continue
        if(key in nrad_map):
            raise ValueError("duplicate No_Rad identity: %s" % key)
        nrad_map[key] = path
    if(len(bad) > 0):
        raise ValueError("malformed radiation token: %s" % bad)
    matched = []
    unmatched_rad = []
    unmatched_nrad = []
    for key in sorted(rad_map):
        if(key in nrad_map):
            matched.append((rad_map[key], nrad_map[key]))
        else:
            unmatched_rad.append(rad_map[key])
    for key in sorted(nrad_map):
        if(key not in rad_map):
            unmatched_nrad.append(nrad_map[key])
    selected_rad = [pair[0] for pair in matched]
    selected_nrad = [pair[1] for pair in matched]
    if(len(selected_rad) != len(selected_nrad)):
        raise ValueError("selected Rad and No_Rad counts are not one-to-one")
    return {"matched": matched, "unmatched_rad": unmatched_rad, "unmatched_nrad": unmatched_nrad, "rad": selected_rad, "nrad": selected_nrad}


def report_pairs(result):
    print("rc_pairs matched %d" % len(result["matched"]))
    print("rc_pairs unmatched_rad %d" % len(result["unmatched_rad"]))
    print("rc_pairs unmatched_nrad %d" % len(result["unmatched_nrad"]))
    for rad_path, nrad_path in result["matched"]:
        print("rc_pair %s %s" % (os.path.basename(rad_path), os.path.basename(nrad_path)))
    for path in result["unmatched_rad"]:
        print("rc_unmatched_rad %s" % os.path.basename(path))
    for path in result["unmatched_nrad"]:
        print("rc_unmatched_nrad %s" % os.path.basename(path))


# Local name-only check: exact pair kept, extra No_Rad excluded, lone Rad reported, different batch or merged index not paired, duplicate or token-free names raise. No files are read and no histograms are built.
def self_test():
    prefix = "LUND_EvGen_Iterative_richcap_SBATCH_richcap_Old_MM_Cut_Groups_"
    exact_rad = prefix + "Q2_Row_5_V5_Batch_1_Rad_Merged_0.root"
    exact_nrad = prefix + "Q2_Row_5_V5_Batch_1_No_Rad_Merged_0.root"
    pair = pair_rad_nrad([exact_rad], [exact_nrad])
    if(len(pair["matched"]) != 1):
        raise SystemExit("exact pair was not accepted")
    extra = pair_rad_nrad([exact_rad], [exact_nrad, prefix + "Q2_Row_5_V7_Batch_1_No_Rad_Merged_0.root"])
    if((len(extra["nrad"]) != 1) or (len(extra["unmatched_nrad"]) != 1)):
        raise SystemExit("unmatched No_Rad entered RC")
    lone = pair_rad_nrad([prefix + "y_Col_2_V1_Batch_3_Rad_Merged_1.root"], [])
    if((len(lone["unmatched_rad"]) != 1) or (len(lone["rad"]) != 0)):
        raise SystemExit("unmatched Rad was not reported")
    different_batch = pair_rad_nrad([prefix + "Q2_Row_5_V5_Batch_2_Rad_Merged_0.root"], [exact_nrad])
    if(len(different_batch["matched"]) != 0):
        raise SystemExit("different batch was paired")
    different_merged = pair_rad_nrad([prefix + "Q2_Row_5_V5_Batch_1_Rad_Merged_1.root"], [exact_nrad])
    if(len(different_merged["matched"]) != 0):
        raise SystemExit("different merged index was paired")
    try:
        pair_rad_nrad(["/tmp/a/" + exact_rad, "/tmp/b/" + exact_rad], [])
        raise SystemExit("duplicate key did not fail")
    except ValueError:
        pass
    try:
        pair_rad_nrad(["no_token.root"], [])
        raise SystemExit("malformed name did not fail")
    except ValueError:
        pass
    print("rc_pairs self_test ok")


if(__name__ == "__main__"):
    self_test()
