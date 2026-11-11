#!/usr/bin/env python3
# Replace only the three systematic columns in a copy of the bin-border table.

import argparse
import json
import os
import re

KEY = "Fit_Pars_from_3D_BC_RC_Bayesian"
ROW = re.compile(r"^(\d+) -- (\d+) & ")
SYS_FIELDS = (7, 10, 13)


def format_sys(value):
    number = float(value)
    if(number == 0.0):
        return "0"
    text = "%.3g" % number
    return text


def parse_args():
    parser = argparse.ArgumentParser(description="Update bin-border systematic columns from one normalized JSON.")
    parser.add_argument("-j", "--json_file", required=True)
    parser.add_argument("-i", "--input_tex", required=True)
    parser.add_argument("-o", "--output_tex", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    payload = json.load(open(args.json_file))
    cells = payload[KEY]
    lines = open(args.input_tex).read().splitlines()
    updated = 0
    output = []
    for line in lines:
        match = ROW.match(line)
        if(match is None):
            output.append(line)
            continue
        if("Skipped" in line):
            output.append(line)
            continue
        q2y = int(match.group(1))
        zpt = int(match.group(2))
        key = "(Q2_y_Bin_%d)-(z_pT_Bin_%d)" % (q2y, zpt)
        if(key not in cells):
            raise SystemExit("missing %s" % key)
        cell = cells[key]
        fields = line.split("&")
        if(len(fields) < 14):
            raise SystemExit("short row %s" % key)
        values = [
            cell["Fit_Par_A_SYS"],
            cell["Fit_Par_B_SYS"],
            cell["Fit_Par_C_SYS"],
        ]
        for index, value in zip(SYS_FIELDS, values):
            updated_field, count = re.subn(r"\$[^$]*\$", "$%s$" % format_sys(value), fields[index], count=1)
            if(count != 1):
                raise SystemExit("systematic field missing in %s" % key)
            fields[index] = updated_field
        rebuilt = "&".join(fields)
        if(not rebuilt.rstrip().endswith("\\\\")):
            raise SystemExit("row ending changed for %s" % key)
        output.append(rebuilt)
        updated += 1
    if(updated != 452):
        raise SystemExit("updated %d rows, expected 452" % updated)
    os.makedirs(os.path.dirname(os.path.abspath(args.output_tex)), exist_ok=True)
    handle = open(args.output_tex, "w")
    handle.write("\n".join(output) + "\n")
    handle.close()
    print("wrote %s (%d rows)" % (args.output_tex, updated))


if(__name__ == "__main__"):
    main()
