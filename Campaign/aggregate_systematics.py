#!/usr/bin/env python3
# Reduce registered systematic variations. The stored triple is never overwritten.
import argparse
import json
import math
import os

SOURCE_REDUCTIONS = ["per_variation_signed", "rms", "max_excursion", "envelope", "half_difference", "not_combined"]
TOTAL_COMBINATIONS = ["quadrature", "none"]


def signed_difference(nominal, variation):
    return float(variation) - float(nominal)


def variation_record(source, variation, observables):
    # observables: name -> {nominal, variation, stat_nominal, stat_variation}
    stored = {"source": source, "variation": variation, "observables": {}}
    for name, values in observables.items():
        nominal_value   = float(values["nominal"])
        variation_value = float(values["variation"])
        stored["observables"][name] = {
            "nominal": nominal_value,
            "variation": variation_value,
            "signed_difference": signed_difference(nominal_value, variation_value),
            "stat_nominal": values.get("stat_nominal"),
            "stat_variation": values.get("stat_variation"),
        }
    return stored


def reduce_source(records, method):
    # records are one source. Each observable keeps every variation's triple.
    if(method not in SOURCE_REDUCTIONS):
        raise ValueError("unknown source_reduction %s" % method)
    names = []
    for record in records:
        for name in record["observables"]:
            if(name not in names):
                names.append(name)
    reduced = {}
    for name in names:
        shifts = []
        for record in records:
            if(name not in record["observables"]):
                continue
            shifts.append(record["observables"][name]["signed_difference"])
        if(method == "not_combined"):
            up, down = None, None
        elif(method == "per_variation_signed"):
            up   = math.sqrt(sum([shift * shift for shift in shifts if(shift > 0)])) if(any(shift > 0 for shift in shifts)) else 0.0
            down = math.sqrt(sum([shift * shift for shift in shifts if(shift < 0)])) if(any(shift < 0 for shift in shifts)) else 0.0
        elif(method == "rms"):
            rms = math.sqrt(sum([shift * shift for shift in shifts]) / float(len(shifts))) if(shifts) else 0.0
            up, down = rms, rms
        elif(method == "max_excursion"):
            up   = max([shift for shift in shifts if(shift > 0)] or [0.0])
            down = min([shift for shift in shifts if(shift < 0)] or [0.0])
            down = abs(down)
        elif(method == "envelope"):
            up   = max(shifts) if(shifts) else 0.0
            down = abs(min(shifts)) if(shifts) else 0.0
            if(up < 0.0):
                up = 0.0
            if(min(shifts) > 0.0 if(shifts) else True):
                down = 0.0
        elif(method == "half_difference"):
            if(len(shifts) < 1):
                up, down = 0.0, 0.0
            else:
                half = 0.5 * (max(shifts) - min(shifts))
                up, down = half, half
        reduced[name] = {"up": up, "down": down, "shifts": shifts}
    return reduced


def combine_sources(reduced_by_source, total_combination):
    if(total_combination not in TOTAL_COMBINATIONS):
        raise ValueError("unknown total_combination %s" % total_combination)
    names = []
    for source, reduced in reduced_by_source.items():
        for name in reduced:
            if(name not in names):
                names.append(name)
    total = {}
    for name in names:
        ups   = []
        downs = []
        for source, reduced in reduced_by_source.items():
            piece = reduced.get(name)
            if((piece is None) or (piece["up"] is None)):
                continue
            ups.append(piece["up"])
            downs.append(piece["down"])
        if(total_combination == "none"):
            total[name] = {"up": None, "down": None}
        else:
            total[name] = {
                "up": math.sqrt(sum([value * value for value in ups])) if(ups) else 0.0,
                "down": math.sqrt(sum([value * value for value in downs])) if(downs) else 0.0,
            }
    return total


def write_report(path, variations, reduced, total, config):
    folder = os.path.dirname(path)
    if(folder):
        os.makedirs(folder, exist_ok=True)
    payload = {
        "config": config,
        "variations": variations,
        "reduced": reduced,
        "total": total,
    }
    handle = open(path, "w")
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
    handle.close()
    text_path = path.replace(".json", ".txt")
    lines = ["source variation observable nominal variation signed_difference"]
    for record in variations:
        for name, values in record["observables"].items():
            lines.append("%s %s %s %s %s %s" % (
                record["source"], record["variation"], name,
                values["nominal"], values["variation"], values["signed_difference"],
            ))
    lines.append("reduced_and_total")
    lines.append(json.dumps({"reduced": reduced, "total": total}, sort_keys=True))
    handle = open(text_path, "w")
    handle.write("\n".join(lines))
    handle.write("\n")
    handle.close()


def load_config(path):
    if((path is None) or (not os.path.isfile(path))):
        return {"source_reduction": {}, "default_source_reduction": "per_variation_signed", "total_combination": "quadrature"}
    handle = open(path)
    config = json.load(handle)
    handle.close()
    return config


def aggregate(variation_files, config):
    variations = []
    for path in variation_files:
        handle = open(path)
        variations.append(json.load(handle))
        handle.close()
    by_source = {}
    for record in variations:
        by_source.setdefault(record["source"], []).append(record)
    default_method = config.get("default_source_reduction", "per_variation_signed")
    per_source = config.get("source_reduction", {})
    reduced = {}
    for source, records in by_source.items():
        method = per_source.get(source, default_method)
        reduced[source] = reduce_source(records, method)
        reduced[source]["_method"] = method
    total = combine_sources(
        {source: {name: values for name, values in pieces.items() if(name != "_method")} for source, pieces in reduced.items()},
        config.get("total_combination", "quadrature"),
    )
    return variations, reduced, total


def self_test():
    one = variation_record("particle_match", "Bank", {"B": {"nominal": 0.10, "variation": 0.13, "stat_nominal": 0.01}})
    two = variation_record("particle_match", "P12T6", {"B": {"nominal": 0.10, "variation": 0.04, "stat_nominal": 0.01}})
    if(one["observables"]["B"]["signed_difference"] != 0.03):
        raise SystemExit("signed difference")
    signed = reduce_source([one, two], "per_variation_signed")
    rms    = reduce_source([one, two], "rms")
    if(abs(signed["B"]["up"] - 0.03) > 1e-9):
        raise SystemExit("per_variation up")
    if(abs(signed["B"]["down"] - 0.06) > 1e-9):
        raise SystemExit("per_variation down")
    expect_rms = math.sqrt((0.03 ** 2 + (-0.06) ** 2) / 2.0)
    if(abs(rms["B"]["up"] - expect_rms) > 1e-9):
        raise SystemExit("rms")
    # Changing the reduction does not alter the stored triples.
    if(one["observables"]["B"]["variation"] != 0.13):
        raise SystemExit("triple overwritten")
    other = variation_record("acceptance_threshold", "0.040", {"B": {"nominal": 0.10, "variation": 0.12}})
    reduced = {
        "particle_match": reduce_source([one, two], "per_variation_signed"),
        "acceptance_threshold": reduce_source([other], "per_variation_signed"),
    }
    total = combine_sources(reduced, "quadrature")
    expect = math.sqrt(0.03 ** 2 + 0.02 ** 2)
    if(abs(total["B"]["up"] - expect) > 1e-9):
        raise SystemExit("quadrature")
    none_total = combine_sources(reduced, "none")
    if(none_total["B"]["up"] is not None):
        raise SystemExit("none combination")
    print("aggregate self_test ok")


def main():
    parser = argparse.ArgumentParser(description="Aggregate registered systematic variations.")
    parser.add_argument("-v", "--variation_file", action="append", default=[], help="One preserved variation JSON. Repeatable.")
    parser.add_argument("-g", "--config", default=None, help="aggregation_config.json")
    parser.add_argument("-o", "--output", default="systematics/total.json", help="Machine-readable total. A .txt report is written beside it.")
    parser.add_argument("-t", "--self_test", action="store_true", help="Run the reducer checks and exit.")
    args = parser.parse_args()
    if(args.self_test):
        self_test()
        return
    config = load_config(args.config)
    variations, reduced, total = aggregate(args.variation_file, config)
    write_report(args.output, variations, reduced, total, config)
    print(args.output)


if(__name__ == "__main__"):
    main()
