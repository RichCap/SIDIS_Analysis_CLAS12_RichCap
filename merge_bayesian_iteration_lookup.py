#!/usr/bin/env python3
# 9/30/2026: persistent Bayesian-iteration lookup for 3D and 5D unfolding.
# k_selected is the data-stability choice. Closure fields never replace it.
# A merge rewrites only the configuration named by the call.

import argparse
import datetime
import json
import os
import shutil
import sys
import tempfile

_BOOT = os.path.abspath(os.path.dirname(__file__))
SCHEMA_VERSION = 1
Q2Y_MIN = 1
Q2Y_MAX = 17
STUDY_REL = "Unfold_Iteration_Study_3D/DataFirst_4Way_NoRhoSub_3pct_4pct_5pct"
DEFAULT_LOOKUP = os.path.join(_BOOT, "Unfold_Iteration_Config", "bayesian_iteration_lookup.json")
DEFAULT_STUDY = os.path.join(_BOOT, STUDY_REL)
INITIAL_CUTS = ("0.0005", "0.010", "0.020", "0.030", "0.040", "0.050")
DATA_STATUS = ("ok", "gapped", "unresolved")
CLOSURE_SCOPE = ("", "nominal_only", "four_way")

FIELD_ORDER_3D = [
    "dimension", "acceptance_cut", "acceptance_label", "acceptance_tag", "q2y_bin",
    "k_selected", "k_lo", "k_hi", "window", "k_supported", "data_status",
    "n_supported", "C_E", "mean_error",
    "closure_scope", "nominal_status", "nominal_k",
    "fourway_status", "fourway_k", "closure_validated_k",
    "source_study", "source_table", "updated_utc",
]
FIELD_ORDER_5D = [name for name in FIELD_ORDER_3D if(name != "q2y_bin")]


def parse_args():
    parser = argparse.ArgumentParser(description="merge_bayesian_iteration_lookup.py:\n\tMerge Bayesian iteration selections into one 3D/5D lookup.")
    parser.add_argument("-p", "--lookup_path", default=DEFAULT_LOOKUP, help="Lookup JSON path.\n")
    parser.add_argument("-i", "--input_tsv", default="", help="TSV of records to merge.\n")
    parser.add_argument("-u", "--update", default="", help="Which fields to rewrite: data, closure, or full.\n")
    parser.add_argument("-r", "--replace_scope", default="", help="keys rewrites named records. cut replaces that dimension and acceptance cut.\n")
    parser.add_argument("-d", "--dimension", default="3D", help="Dimension used when an input row does not name one.\n")
    parser.add_argument("-c", "--cuts", action="append", default=[], help="Keep only this acceptance cut from the TSV. Repeat to keep several.\n")
    parser.add_argument("-s", "--source_study", default="", help="Study path stored on records this call rewrites.\n")
    parser.add_argument("-a", "--source_table", default="", help="Table path stored on records this call rewrites.\n")
    parser.add_argument("-e", "--study_dir", default=DEFAULT_STUDY, help="Corrected 3D study used by --initialize.\n")
    parser.add_argument("-n", "--initialize", action="store_true", help="Load the saved 3D tables into the lookup.\n")
    parser.add_argument("-t", "--self_test", action="store_true", help="Check merge behavior on a temporary file and exit.\n")
    return parser.parse_args()


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_cut(value):
    text = str(value).strip()
    if(text.endswith("%")):
        raise ValueError("pass the fractional acceptance cut, not a percent label")
    number = float(text)
    # 0.0005 must stay 0.0005. "%.3f" would round it to 0.001.
    if(abs(number - 0.0005) <= 1.0e-12):
        return "0.0005"
    return "%.3f" % number


def acceptance_tag(cut_text):
    if(cut_text == "0.0005"):
        return "0005"
    return "%03d" % int(round(float(cut_text) * 1000.0))


def acceptance_label(cut_text):
    if(cut_text == "0.0005"):
        return "0.05%"
    percent = float(cut_text) * 100.0
    nearest = round(percent)
    if(abs(percent - nearest) <= 1.0e-9):
        return "%d%%" % int(nearest)
    return "%.4g%%" % percent


def as_int_or_none(value):
    if(value in ("", None)):
        return None
    if(isinstance(value, bool)):
        raise ValueError("bool is not an iteration")
    if(isinstance(value, float)):
        if(value != int(value)):
            raise ValueError("iteration is not an integer")
        return int(value)
    return int(value)


def as_float_or_none(value):
    if(value in ("", None)):
        return None
    return float(value)


def parse_supported(value):
    if(value in ("", None)):
        return []
    if(isinstance(value, (list, tuple))):
        return [int(item) for item in value]
    return [int(part) for part in str(value).split(",") if(part != "")]


def window_text(k_lo, k_hi):
    if((k_lo is None) or (k_hi is None)):
        return ""
    return "%d-%d" % (k_lo, k_hi)


def first_present(row, *names):
    for name in names:
        if(name not in row):
            continue
        if(row[name] in ("", None)):
            continue
        return row[name]
    return None


def read_tsv(path):
    rows = []
    with open(path) as handle:
        header = handle.readline().rstrip("\n").split("\t")
        for line in handle:
            if((line.strip() == "") or line.startswith("#")):
                continue
            parts = line.rstrip("\n").split("\t")
            if(len(parts) != len(header)):
                raise ValueError("column count changed in %s" % path)
            rows.append(dict(zip(header, parts)))
    return rows


def identity_from_row(row, dimension):
    dim = row.get("dimension") or dimension
    if("acceptance_cut" in row):
        raw_cut = row["acceptance_cut"]
    else:
        raw_cut = row["cut"]
    cut = canonical_cut(raw_cut)
    q_present = False
    q_val = None
    if(("q2y_bin" in row) and (row["q2y_bin"] not in ("", None))):
        q_present = True
        q_val = int(row["q2y_bin"])
    elif(("q2y" in row) and (row["q2y"] not in ("", None))):
        q_present = True
        q_val = int(row["q2y"])
    if(dim == "5D"):
        if(q_present):
            raise ValueError("5D record must not include q2y_bin")
        return dim, cut, None
    if(dim != "3D"):
        raise ValueError("dimension must be 3D or 5D")
    if(not q_present):
        raise ValueError("3D record requires q2y_bin")
    if((q_val < Q2Y_MIN) or (q_val > Q2Y_MAX)):
        raise ValueError("q2y_bin must be 1 through 17")
    return dim, cut, q_val


def record_key(record):
    dimension = record["dimension"]
    cut = canonical_cut(record["acceptance_cut"])
    if(dimension == "3D"):
        if("q2y_bin" not in record):
            raise ValueError("3D record requires q2y_bin")
        q2y = int(record["q2y_bin"])
        if((q2y < Q2Y_MIN) or (q2y > Q2Y_MAX)):
            raise ValueError("q2y_bin must be 1 through 17")
        return (dimension, cut, q2y)
    if(dimension == "5D"):
        if("q2y_bin" in record):
            raise ValueError("5D record must not include q2y_bin")
        return (dimension, cut, None)
    raise ValueError("dimension must be 3D or 5D")


def ordered_record(record):
    names = FIELD_ORDER_3D if(record["dimension"] == "3D") else FIELD_ORDER_5D
    return {name: record[name] for name in names}


def sort_key(record):
    q2y = record["q2y_bin"] if("q2y_bin" in record) else -1
    return (record["dimension"], record["acceptance_cut"], q2y)


def index_records(records):
    found = {}
    for record in records:
        key = record_key(record)
        if(key in found):
            raise ValueError("duplicate lookup key %s" % (key,))
        found[key] = record
    return found


def load_lookup(path):
    if(not os.path.isfile(path)):
        return {"schema_version": SCHEMA_VERSION, "records": []}
    with open(path) as handle:
        payload = json.load(handle)
    if(not isinstance(payload, dict)):
        raise ValueError("lookup must be a JSON object")
    if(payload.get("schema_version") != SCHEMA_VERSION):
        raise ValueError("schema_version %s is not %s" % (payload.get("schema_version"), SCHEMA_VERSION))
    if(not isinstance(payload.get("records"), list)):
        raise ValueError("records must be a list")
    index_records(payload["records"])
    return payload


def write_lookup(path, payload):
    folder = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(folder, exist_ok=True)
    payload["schema_version"] = SCHEMA_VERSION
    payload["records"] = [ordered_record(record) for record in payload["records"]]
    payload["records"] = sorted(payload["records"], key=sort_key)
    tmp_path = os.path.join(folder, os.path.basename(path) + ".tmp")
    handle = open(tmp_path, "w")
    try:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    except Exception:
        handle.close()
        if(os.path.isfile(tmp_path)):
            os.remove(tmp_path)
        raise
    handle.close()
    os.replace(tmp_path, os.path.abspath(path))


def new_record(dimension, cut, q2y):
    record = {
        "dimension": dimension,
        "acceptance_cut": cut,
        "acceptance_label": acceptance_label(cut),
        "acceptance_tag": acceptance_tag(cut),
        "k_selected": None,
        "k_lo": None,
        "k_hi": None,
        "window": "",
        "k_supported": [],
        "data_status": "",
        "n_supported": None,
        "C_E": None,
        "mean_error": None,
        "closure_scope": "",
        "nominal_status": "",
        "nominal_k": None,
        "fourway_status": "",
        "fourway_k": None,
        "closure_validated_k": None,
        "source_study": "",
        "source_table": "",
        "updated_utc": "",
    }
    if(dimension == "3D"):
        record["q2y_bin"] = q2y
    return record


def copy_record(record):
    copied = dict(record)
    copied["k_supported"] = list(record.get("k_supported", []))
    return copied


def normalize_scope(text):
    # The comparison table marks copied 3/4/5 percent rows as reused_four_way.
    if(text == "reused_four_way"):
        return "four_way"
    return text or ""


def apply_data(record, row):
    status = row.get("data_status", row.get("status", ""))
    if(status not in DATA_STATUS):
        raise ValueError("data_status must be ok, gapped, or unresolved")
    k_sel = as_int_or_none(row.get("k_selected"))
    k_lo  = as_int_or_none(row.get("k_lo"))
    k_hi  = as_int_or_none(row.get("k_hi"))
    if(status == "unresolved"):
        if(k_sel is not None):
            raise ValueError("unresolved record cannot carry k_selected")
        record["data_status"]  = status
        record["k_selected"]   = None
        record["k_lo"]         = None
        record["k_hi"]         = None
        record["window"]       = ""
        record["k_supported"]  = []
        record["n_supported"]  = 0
        record["C_E"]          = None
        record["mean_error"]   = None
        return record
    supported = parse_supported(row.get("k_supported"))
    if(len(supported) == 0):
        raise ValueError("supported window is empty")
    if(k_lo is None):
        k_lo = supported[0]
    if(k_hi is None):
        k_hi = supported[-1]
    if(k_lo != supported[0]):
        raise ValueError("k_lo is not the first supported iteration")
    if(k_hi != supported[-1]):
        raise ValueError("k_hi is not the last supported iteration")
    if(k_sel != supported[0]):
        raise ValueError("k_selected must be the first supported iteration")
    window = window_text(k_lo, k_hi)
    supplied = str(row.get("window", "") or "")
    if((supplied != "") and (supplied != window)):
        raise ValueError("window %s does not match %s" % (supplied, window))
    n_supported = as_int_or_none(row.get("n_supported"))
    if(n_supported is None):
        n_supported = len(supported)
    if(n_supported != len(supported)):
        raise ValueError("n_supported does not match k_supported")
    contiguous = (supported[-1] - supported[0] + 1) == len(supported)
    if((status == "ok") and (not contiguous)):
        raise ValueError("status ok requires a contiguous window")
    if((status == "gapped") and contiguous):
        raise ValueError("status gapped requires a gap")
    record["data_status"] = status
    record["k_selected"]  = k_sel
    record["k_lo"]        = k_lo
    record["k_hi"]        = k_hi
    record["window"]      = window
    record["k_supported"] = supported
    record["n_supported"] = n_supported
    record["C_E"]         = as_float_or_none(row.get("C_E"))
    record["mean_error"]  = as_float_or_none(row.get("mean_error"))
    return record


def apply_closure(record, row):
    scope = normalize_scope(row.get("closure_scope", ""))
    if(scope not in CLOSURE_SCOPE):
        raise ValueError("closure_scope %s is not nominal_only or four_way" % scope)
    nominal_status = row.get("nominal_status", "") or ""
    fourway_status = row.get("fourway_status", "") or ""
    nominal_k = as_int_or_none(first_present(row, "nominal_k", "nominal_final_k"))
    fourway_k = as_int_or_none(first_present(row, "fourway_k", "fourway_final_k"))
    if(nominal_status == "pass"):
        if(nominal_k is None):
            raise ValueError("nominal pass requires nominal_k")
    elif(nominal_k is not None):
        raise ValueError("nominal_k is stored only when nominal_status is pass")
    if(fourway_status == "pass"):
        if(fourway_k is None):
            raise ValueError("four-way pass requires fourway_k")
        validated = fourway_k
    elif(fourway_k is not None):
        raise ValueError("fourway_k is stored only when fourway_status is pass")
    else:
        validated = None
    record["closure_scope"]        = scope
    record["nominal_status"]       = nominal_status
    record["nominal_k"]            = nominal_k
    record["fourway_status"]       = fourway_status
    record["fourway_k"]            = fourway_k
    record["closure_validated_k"]  = validated
    return record


def apply_provenance(record, source_study, source_table, clock):
    record["acceptance_cut"]   = canonical_cut(record["acceptance_cut"])
    record["acceptance_label"] = acceptance_label(record["acceptance_cut"])
    record["acceptance_tag"]   = acceptance_tag(record["acceptance_cut"])
    if(source_study):
        record["source_study"] = source_study
    if(source_table):
        record["source_table"] = source_table
    record["updated_utc"] = clock()
    return record


def merge_rows(path, rows, dimension="3D", update="full", replace_scope="keys", source_study="", source_table="", clock=None):
    if(clock is None):
        clock = utc_now
    if(update not in ("data", "closure", "full")):
        raise ValueError("update must be data, closure, or full")
    if(replace_scope not in ("keys", "cut")):
        raise ValueError("replace_scope must be keys or cut")
    payload = load_lookup(path)
    existing = index_records(payload["records"])
    prepared = []
    seen = {}
    for row in rows:
        dim, cut, q2y = identity_from_row(row, dimension)
        key = (dim, cut, q2y)
        if(key in seen):
            raise ValueError("duplicate input key %s" % (key,))
        seen[key] = row
        prepared.append((key, dim, cut, q2y, row))
    if(update == "closure"):
        for key, _dim, _cut, _q2y, _row in prepared:
            if(key not in existing):
                raise ValueError("closure update requires an existing record for %s" % (key,))
    touched_cuts = set((item[1], item[2]) for item in prepared)
    kept = {}
    for key, record in existing.items():
        dim = key[0]
        cut = key[1]
        drop_cut = (replace_scope == "cut") and ((dim, cut) in touched_cuts)
        drop_key = (replace_scope == "keys") and (key in seen)
        if(drop_cut or drop_key):
            continue
        kept[key] = record
    for key, dim, cut, q2y, row in prepared:
        old = existing.get(key)
        if(old is None):
            record = new_record(dim, cut, q2y)
        else:
            record = copy_record(old)
            record["acceptance_cut"] = cut
        if(update in ("data", "full")):
            apply_data(record, row)
        if(update in ("closure", "full")):
            apply_closure(record, row)
        apply_provenance(record, source_study, source_table, clock)
        kept[key] = record
    write_lookup(path, {"schema_version": SCHEMA_VERSION, "records": list(kept.values())})
    return load_lookup(path)


def lookup_record(path, dimension, acceptance_cut, q2y_bin=None):
    cut = canonical_cut(acceptance_cut)
    if(dimension == "3D"):
        if(q2y_bin is None):
            raise ValueError("3D lookup requires q2y_bin")
        key = ("3D", cut, int(q2y_bin))
    elif(dimension == "5D"):
        if(q2y_bin is not None):
            raise ValueError("5D lookup does not take q2y_bin")
        key = ("5D", cut, None)
    else:
        raise ValueError("dimension must be 3D or 5D")
    payload = load_lookup(path)
    for record in payload["records"]:
        if(record_key(record) == key):
            return ordered_record(record)
    return None


def supported_text(k_lo, k_hi):
    return ",".join(str(k_val) for k_val in range(int(k_lo), int(k_hi) + 1))


def data_row(cut, q2y, k_lo, k_hi, status="ok"):
    supported = supported_text(k_lo, k_hi)
    return {
        "cut": cut,
        "q2y": q2y,
        "status": status,
        "k_selected": k_lo if(status != "unresolved") else "",
        "k_lo": k_lo if(status != "unresolved") else "",
        "k_hi": k_hi if(status != "unresolved") else "",
        "k_supported": supported if(status != "unresolved") else "",
        "n_supported": (int(k_hi) - int(k_lo) + 1) if(status != "unresolved") else 0,
        "C_E": 0.5 if(status != "unresolved") else "",
        "mean_error": 10.0 if(status != "unresolved") else "",
    }


def initialize_lookup(lookup_path, study_dir):
    rec_path = os.path.join(study_dir, "expanded", "tables", "recommendations_all.tsv")
    cmp_path = os.path.join(study_dir, "expanded", "tables", "iteration_comparison.tsv")
    if(not os.path.isfile(rec_path)):
        raise SystemExit("missing %s" % rec_path)
    if(not os.path.isfile(cmp_path)):
        raise SystemExit("missing %s" % cmp_path)
    recs = read_tsv(rec_path)
    cmps = read_tsv(cmp_path)
    if((len(recs) != 102) or (len(cmps) != 102)):
        raise SystemExit("expected 102 recommendation rows and 102 comparison rows")
    rec_map = {}
    for row in recs:
        cut = canonical_cut(row["cut"])
        if(cut == "0.025"):
            raise SystemExit("refusing to insert the current code default 0.025")
        key = (cut, int(row["q2y"]))
        if(key in rec_map):
            raise SystemExit("duplicate recommendation %s Q2-y %s" % key)
        rec_map[key] = row
    expected = [(cut, q2y) for cut in INITIAL_CUTS for q2y in range(Q2Y_MIN, Q2Y_MAX + 1)]
    if(sorted(rec_map) != sorted(expected)):
        raise SystemExit("recommendation keys are not the six completed cuts")
    cmp_map = {}
    for row in cmps:
        cut = canonical_cut(row["cut"])
        if(cut == "0.025"):
            raise SystemExit("refusing to insert the current code default 0.025")
        key = (cut, int(row["q2y"]))
        if(key in cmp_map):
            raise SystemExit("duplicate comparison %s Q2-y %s" % key)
        cmp_map[key] = row
    if(set(cmp_map) != set(rec_map)):
        raise SystemExit("comparison keys do not match the recommendations")
    for key in expected:
        rec = rec_map[key]
        cmp = cmp_map[key]
        if(str(rec["k_selected"]) != str(cmp["k_selected"])):
            raise SystemExit("k_selected mismatch at %s Q2-y %s" % key)
        if(str(rec["status"]) != str(cmp["data_status"])):
            raise SystemExit("data_status mismatch at %s Q2-y %s" % key)
        window = ""
        if(rec["k_lo"] not in ("", None)):
            window = "%s-%s" % (rec["k_lo"], rec["k_hi"])
        if(window != cmp["window"]):
            raise SystemExit("window mismatch at %s Q2-y %s" % key)
        if(str(rec["k_supported"]) != str(cmp["k_supported"])):
            raise SystemExit("k_supported mismatch at %s Q2-y %s" % key)
    for cut, tag in (("0.030", "030"), ("0.040", "040"), ("0.050", "050")):
        iter_path = os.path.join(study_dir, "tables", "iteration_cut_%s.tsv" % tag)
        old_rows = read_tsv(iter_path)
        if(len(old_rows) != 17):
            raise SystemExit("expected 17 rows in %s" % iter_path)
        for row in old_rows:
            q2y = int(row["q2y"])
            got = rec_map[(cut, q2y)]["k_selected"]
            if(str(got) != str(row["data_k"])):
                raise SystemExit("reused data_k mismatch %s Q2-y %s" % (cut, q2y))
    full_rows = []
    for key in expected:
        rec = rec_map[key]
        cmp = dict(cmp_map[key])
        cmp["cut"]          = key[0]
        cmp["q2y"]          = key[1]
        cmp["status"]       = rec["status"]
        cmp["k_selected"]   = rec["k_selected"]
        cmp["k_lo"]         = rec["k_lo"]
        cmp["k_hi"]         = rec["k_hi"]
        cmp["k_supported"]  = rec["k_supported"]
        cmp["n_supported"]  = rec["n_supported"]
        cmp["C_E"]          = rec["C_E"]
        cmp["mean_error"]   = rec["mean_error"]
        full_rows.append(cmp)
    merge_rows(
        lookup_path,
        full_rows,
        dimension="3D",
        update="full",
        replace_scope="cut",
        source_study=STUDY_REL,
        source_table="expanded/tables/iteration_comparison.tsv",
    )
    print("Wrote %s" % lookup_path)
    return 0


def production_bytes():
    if(not os.path.isfile(DEFAULT_LOOKUP)):
        return None
    with open(DEFAULT_LOOKUP, "rb") as handle:
        return handle.read()


def self_test():
    if(canonical_cut("0.0005") != "0.0005"):
        raise SystemExit("self_test 0.0005 canonical cut")
    if(canonical_cut("0.02") != "0.020"):
        raise SystemExit("self_test 0.020 canonical cut")
    if(acceptance_tag("0.0005") != "0005"):
        raise SystemExit("self_test 0.0005 tag")
    if(acceptance_tag("0.010") != "010"):
        raise SystemExit("self_test 1 percent tag")
    if(acceptance_label("0.0005") != "0.05%"):
        raise SystemExit("self_test 0.05 percent label")
    if(acceptance_label("0.030") != "3%"):
        raise SystemExit("self_test 3 percent label")
    before = production_bytes()
    folder = tempfile.mkdtemp(prefix="iteration_lookup_")
    path = os.path.join(folder, "bayesian_iteration_lookup.json")
    stamps = {"n": 0}

    def clock():
        stamps["n"] += 1
        return "2026-09-30T00:00:%02dZ" % stamps["n"]

    try:
        if(load_lookup(path)["records"] != []):
            raise SystemExit("self_test missing file is not empty")
        cut_a = []
        for q2y, k_lo in ((1, 6), (2, 5)):
            row = data_row("0.030", q2y, k_lo, 25)
            row["closure_scope"]   = "reused_four_way"
            row["nominal_status"]  = "pass"
            row["nominal_final_k"] = k_lo
            row["fourway_status"]  = "unresolved"
            row["fourway_final_k"] = ""
            cut_a.append(row)
        cut_b = [data_row("0.050", 1, 5, 25)]
        cut_b[0]["closure_scope"]   = "four_way"
        cut_b[0]["nominal_status"]  = "fail"
        cut_b[0]["nominal_final_k"] = ""
        cut_b[0]["fourway_status"]  = "unresolved"
        cut_b[0]["fourway_final_k"] = ""
        five = [data_row("0.030", 1, 9, 12)]
        five[0]["dimension"] = "5D"
        del five[0]["q2y"]
        merge_rows(path, cut_a + cut_b, dimension="3D", update="full", replace_scope="cut", source_study="test", source_table="test.tsv", clock=clock)
        merge_rows(path, five, dimension="5D", update="full", replace_scope="keys", source_study="test-5d", source_table="test-5d.tsv", clock=clock)
        payload = load_lookup(path)
        if(len(payload["records"]) != 4):
            raise SystemExit("self_test expected 4 records")
        kept = lookup_record(path, "3D", "0.030", q2y_bin=1)
        if((kept["k_selected"] != 6) or (kept["closure_scope"] != "four_way") or (kept["nominal_k"] != 6)):
            raise SystemExit("self_test initial 3 percent record")
        if(kept["closure_validated_k"] is not None):
            raise SystemExit("self_test unresolved closure stored a validated k")
        other = lookup_record(path, "3D", "0.050", q2y_bin=1)
        five_rec = lookup_record(path, "5D", "0.030")
        if((five_rec is None) or ("q2y_bin" in five_rec) or (five_rec["k_selected"] != 9)):
            raise SystemExit("self_test 5D record")
        other_utc = other["updated_utc"]
        five_utc = five_rec["updated_utc"]
        moved = data_row("0.030", 1, 8, 25)
        moved["k_selected"] = 99
        moved["fourway_status"] = "pass"
        moved["fourway_final_k"] = 15
        try:
            merge_rows(path, [moved], dimension="3D", update="data", replace_scope="keys", clock=clock)
            raise SystemExit("self_test data row with a bad k_selected was accepted")
        except ValueError:
            pass
        moved = data_row("0.030", 1, 8, 25)
        merge_rows(path, [moved], dimension="3D", update="data", replace_scope="keys", source_table="data-update.tsv", clock=clock)
        updated = lookup_record(path, "3D", "0.030", q2y_bin=1)
        sibling = lookup_record(path, "3D", "0.030", q2y_bin=2)
        if(updated["k_selected"] != 8):
            raise SystemExit("self_test data update did not change k")
        if((updated["nominal_k"] != 6) or (updated["closure_scope"] != "four_way") or (updated["fourway_status"] != "unresolved")):
            raise SystemExit("self_test data update cleared closure")
        if(updated["closure_validated_k"] is not None):
            raise SystemExit("self_test data update invented closure_validated_k")
        if((sibling["k_selected"] != 5) or (lookup_record(path, "3D", "0.050", q2y_bin=1)["updated_utc"] != other_utc)):
            raise SystemExit("self_test one-bin update changed another record")
        if(lookup_record(path, "5D", "0.030")["updated_utc"] != five_utc):
            raise SystemExit("self_test 3D update changed 5D")
        closure_row = {
            "cut": "0.030",
            "q2y": 1,
            "k_selected": 3,
            "closure_scope": "four_way",
            "nominal_status": "fail",
            "nominal_final_k": "",
            "fourway_status": "unresolved",
            "fourway_final_k": "",
        }
        merge_rows(path, [closure_row], dimension="3D", update="closure", replace_scope="keys", clock=clock)
        after_closure = lookup_record(path, "3D", "0.030", q2y_bin=1)
        if((after_closure["k_selected"] != 8) or (after_closure["nominal_status"] != "fail") or (after_closure["nominal_k"] is not None)):
            raise SystemExit("self_test closure update changed the data-selected k")
        # Put closure back, then drop the stale Q2-y bin with a cut-scoped data rewrite.
        restore = data_row("0.030", 1, 8, 25)
        restore["closure_scope"]   = "four_way"
        restore["nominal_status"]  = "pass"
        restore["nominal_final_k"] = 8
        restore["fourway_status"]  = "unresolved"
        restore["fourway_final_k"] = ""
        merge_rows(path, [restore], dimension="3D", update="closure", replace_scope="keys", clock=clock)
        # closure update cannot create nominal_k when the row is closure-only and nominal pass needs the k.
        # The restore above is an update=closure row, so nominal_final_k is applied and k_selected stays 8.
        if(lookup_record(path, "3D", "0.030", q2y_bin=1)["k_selected"] != 8):
            raise SystemExit("self_test restore changed k_selected")
        replacement = data_row("0.030", 1, 7, 25)
        merge_rows(path, [replacement], dimension="3D", update="data", replace_scope="cut", clock=clock)
        if(lookup_record(path, "3D", "0.030", q2y_bin=2) is not None):
            raise SystemExit("self_test cut replace kept a stale bin")
        replaced = lookup_record(path, "3D", "0.030", q2y_bin=1)
        if((replaced["k_selected"] != 7) or (replaced["nominal_status"] != "pass") or (replaced["nominal_k"] != 8)):
            raise SystemExit("self_test cut replace did not keep closure on the remaining bin")
        if(lookup_record(path, "3D", "0.050", q2y_bin=1)["k_selected"] != 5):
            raise SystemExit("self_test cut replace changed the other cut")
        if(lookup_record(path, "5D", "0.030")["k_selected"] != 9):
            raise SystemExit("self_test cut replace changed 5D")
        snapshot = open(path, "rb").read()
        bad_five = {"dimension": "5D", "cut": "0.050", "q2y_bin": 1, "status": "ok", "k_selected": 4, "k_lo": 4, "k_hi": 6, "k_supported": "4,5,6", "n_supported": 3}
        try:
            merge_rows(path, [bad_five], dimension="5D", update="full", replace_scope="keys", clock=clock)
            raise SystemExit("self_test accepted a 5D q2y_bin")
        except ValueError:
            pass
        bad_three = {"dimension": "3D", "cut": "0.050", "status": "ok", "k_selected": 4, "k_lo": 4, "k_hi": 6, "k_supported": "4,5,6", "n_supported": 3}
        try:
            merge_rows(path, [bad_three], dimension="3D", update="full", replace_scope="keys", clock=clock)
            raise SystemExit("self_test accepted a 3D row without q2y_bin")
        except ValueError:
            pass
        if(open(path, "rb").read() != snapshot):
            raise SystemExit("self_test rejection wrote the lookup")
        try:
            lookup_record(path, "3D", "0.030")
            raise SystemExit("self_test 3D lookup without q2y_bin")
        except ValueError:
            pass
        try:
            lookup_record(path, "5D", "0.030", q2y_bin=1)
            raise SystemExit("self_test 5D lookup accepted q2y_bin")
        except ValueError:
            pass
        try:
            merge_rows(path, [{"cut": "0.010", "q2y": 1, "closure_scope": "nominal_only", "nominal_status": "fail", "fourway_status": "intentionally_not_run"}], dimension="3D", update="closure", replace_scope="keys", clock=clock)
            raise SystemExit("self_test closure update created a missing record")
        except ValueError:
            pass
        wrong = os.path.join(folder, "wrong.json")
        with open(wrong, "w") as handle:
            handle.write('{"schema_version": 2, "records": []}\n')
        try:
            load_lookup(wrong)
            raise SystemExit("self_test accepted a different schema_version")
        except ValueError:
            pass
    finally:
        shutil.rmtree(folder)
    after = production_bytes()
    if(before != after):
        raise SystemExit("self_test touched the production lookup")
    print("self_test ok")
    return 0


def main():
    args = parse_args()
    if(args.self_test):
        return self_test()
    if(args.initialize):
        return initialize_lookup(args.lookup_path, args.study_dir)
    if(args.input_tsv == ""):
        raise SystemExit("merge requires --input_tsv")
    if(args.update == ""):
        raise SystemExit("merge requires --update")
    if(args.replace_scope == ""):
        raise SystemExit("merge requires --replace_scope")
    rows = read_tsv(args.input_tsv)
    if(len(args.cuts) > 0):
        allowed = set(canonical_cut(cut) for cut in args.cuts)
        kept = []
        for row in rows:
            raw = row["acceptance_cut"] if("acceptance_cut" in row) else row["cut"]
            if(canonical_cut(raw) in allowed):
                kept.append(row)
        rows = kept
    merge_rows(
        args.lookup_path,
        rows,
        dimension=args.dimension,
        update=args.update,
        replace_scope=args.replace_scope,
        source_study=args.source_study,
        source_table=args.source_table,
    )
    print("Updated %s" % args.lookup_path)
    return 0


if(__name__ == "__main__"):
    sys.exit(main() or 0)
