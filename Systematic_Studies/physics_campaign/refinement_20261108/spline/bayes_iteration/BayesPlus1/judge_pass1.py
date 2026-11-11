# Compare the manual-baseline remake with the stored fit and the histogram cosine.
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "fit_before.json"), "r") as handle:
    before = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
with open(os.path.join(here, "fit.json"), "r") as handle:
    after = json.load(handle)["Fit_Pars_from_3D_Bayesian"]
with open(os.path.join(here, "diagnosis_before.json"), "r") as handle:
    diagnosis = json.load(handle)

print("before", len(before), "after", len(after), "missing", sorted(set(before) - set(after)), "extra", sorted(set(after) - set(before)))
better = 0
worse = 0
same = 0
targets = []
worse_rows = []
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

by_bin = {}
for row in diagnosis["rows"]:
    by_bin[row["bin"]] = row

for bin_name, cell in before.items():
    new = after[bin_name]
    row = by_bin[bin_name]
    free = row["free"]
    if(free is None):
        continue
    d_stored = float(new["Chi2"]) - float(cell["Chi2"])
    d_free = float(new["Chi2"]) - float(free["Chi2"])
    needs = False
    reason = []
    if(d_stored > 0.05):
        needs = True
        reason.append("worse_than_stored")
    if(d_free > 0.5):
        needs = True
        reason.append("short_of_cosine")
    if(not needs):
        continue
    b_err = free["B_ERR"] if(free["B_ERR"] is not None) else 0.05
    c_err = free["C_ERR"] if(free["C_ERR"] is not None) else 0.05
    allow_b = not (0.5 * abs(float(free["B"])) < float(b_err))
    allow_c = not (0.5 * abs(float(free["C"])) < float(c_err))
    targets.append({
        "bin": bin_name,
        "q2y": row["q2y"],
        "zpt": row["zpt"],
        "reason": reason,
        "stored_Chi2": cell["Chi2"],
        "pass1_Chi2": new["Chi2"],
        "free_Chi2": free["Chi2"],
        "NDF": new["NDF"],
        "pass1_B": new["Fit_Par_B"],
        "pass1_C": new["Fit_Par_C"],
        "pass1_B_ERR": new["Fit_Par_B_ERR"],
        "pass1_C_ERR": new["Fit_Par_C_ERR"],
        "free_B": free["B"],
        "free_C": free["C"],
        "free_B_ERR": free["B_ERR"],
        "free_C_ERR": free["C_ERR"],
        "Allow_Multiple_Fits": allow_b,
        "Allow_Multiple_Fits_C": allow_c,
        "dB_nominal": row.get("dB_nominal"),
        "dC_nominal": row.get("dC_nominal"),
    })

targets.sort(key=lambda item: float(item["pass1_Chi2"]) - float(item["free_Chi2"]), reverse=True)
worse_rows.sort(reverse=True)
q2y = sorted(set(int(item["q2y"]) for item in targets))
print("better", better, "worse", worse, "same", same, "targets", len(targets), "q2y", q2y)
print("worst stored deltas")
for item in worse_rows[:12]:
    print("  worse", round(item[0], 3), item[1], "stored", round(item[2]["Chi2"], 3), "pass1", round(item[3]["Chi2"], 3), "B", item[3]["Fit_Par_B"], "C", item[3]["Fit_Par_C"])
print("targets")
for item in targets:
    print("  %s gap_free %.3f d_stored %.3f B %.5f -> %.5f C %.5f -> %.5f allow %s %s" % (
        item["bin"],
        float(item["pass1_Chi2"]) - float(item["free_Chi2"]),
        float(item["pass1_Chi2"]) - float(item["stored_Chi2"]),
        float(item["pass1_B"]),
        float(item["free_B"]),
        float(item["pass1_C"]),
        float(item["free_C"]),
        item["Allow_Multiple_Fits"],
        item["Allow_Multiple_Fits_C"],
    ))
one = after["(Q2_y_Bin_1)-(z_pT_Bin_8)"]
print("bin18 pass1", one["Fit_Par_B"], one["Fit_Par_B_ERR"], one["Fit_Par_C"], one["Fit_Par_C_ERR"], one["Chi2"], one["NDF"])
with open(os.path.join(here, "pass2_targets.json"), "w") as handle:
    json.dump({"q2y": q2y, "targets": targets, "better": better, "worse": worse, "same": same}, handle, indent=2)
