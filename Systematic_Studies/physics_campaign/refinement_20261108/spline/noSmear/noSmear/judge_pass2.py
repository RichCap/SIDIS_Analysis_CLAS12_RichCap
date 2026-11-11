# Judge pass 2 against the stored fit and the histogram cosine. Do not edit fits.
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "fit_before.json"), "r") as handle:
    before = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
with open(os.path.join(here, "fit_pass1.json"), "r") as handle:
    pass1 = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
with open(os.path.join(here, "fit.json"), "r") as handle:
    after = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
with open(os.path.join(here, "diagnosis_before.json"), "r") as handle:
    diagnosis = json.load(handle)
with open(os.path.join(here, "pass2_targets.json"), "r") as handle:
    targets = json.load(handle)["targets"]

print("counts", len(before), len(after), "missing", sorted(set(before) - set(after)))
by_bin = {}
for row in diagnosis["rows"]:
    by_bin[row["bin"]] = row
target_names = set(item["bin"] for item in targets)
better = 0
worse = 0
same = 0
worse_rows = []
still_short = []
for bin_name, cell in before.items():
    new = after[bin_name]
    dchi = float(new["Chi2"]) - float(cell["Chi2"])
    if(dchi < -0.05):
        better += 1
    elif(dchi > 0.05):
        worse += 1
        worse_rows.append((dchi, bin_name, cell, new))
    else:
        same += 1
    free = by_bin[bin_name]["free"]
    if(free is None):
        continue
    gap = float(new["Chi2"]) - float(free["Chi2"])
    if(gap > 0.5):
        still_short.append((gap, bin_name, cell, new, free))
worse_rows.sort(reverse=True)
still_short.sort(reverse=True)
print("vs stored better", better, "worse", worse, "same", same)
print("still short of cosine", len(still_short))
for item in worse_rows[:15]:
    free = by_bin[item[1]]["free"]
    print(" WORSE", round(item[0], 3), item[1], "stored", round(item[2]["Chi2"], 3), "now", round(item[3]["Chi2"], 3), "free", None if(free is None) else round(free["Chi2"], 3), "B", item[3]["Fit_Par_B"], "C", item[3]["Fit_Par_C"], "targeted", item[1] in target_names)
print("--- short ---")
for item in still_short[:20]:
    print(" SHORT", round(item[0], 3), item[1], "now", round(item[3]["Chi2"], 3), "free", round(item[4]["Chi2"], 3), "stored", round(item[2]["Chi2"], 3), "B", item[3]["Fit_Par_B"], "freeB", item[4]["B"], "C", item[3]["Fit_Par_C"], "freeC", item[4]["C"], "Berr", item[3]["Fit_Par_B_ERR"], "targeted", item[1] in target_names)
one = after["(Q2_y_Bin_1)-(z_pT_Bin_8)"]
print("bin18", one)
# non-target drift
drift = 0
for bin_name in before:
    if(bin_name in target_names):
        continue
    dchi = float(after[bin_name]["Chi2"]) - float(pass1[bin_name]["Chi2"])
    if(abs(dchi) > 0.05):
        drift += 1
        print(" nontarget drift", bin_name, dchi)
print("nontarget drift", drift)
