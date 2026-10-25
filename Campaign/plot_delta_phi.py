#!/usr/bin/env python3
# Read (Diag_DPhi) objects. This does not define the particle-matching systematic.
import argparse
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)


def object_name(kind, sample, q2y, zpt):
    return "(Diag_DPhi)_(%s)_(%s)_(Q2_y_Bin_%d)_(z_pT_Bin_%d)" % (kind, sample, int(q2y), int(zpt))


def main():
    parser = argparse.ArgumentParser(description="Plot per-bin delta phi_h diagnostics.")
    parser.add_argument("-f", "--file", required=True, help="ROOT file with Diag_DPhi histograms.")
    parser.add_argument("-o", "--output_dir", required=True, help="Directory for the multi-panel images.")
    parser.add_argument("-k", "--kind", default="smear", choices=["smear", "mom"], help="smear or momentum-correction delta phi.")
    args = parser.parse_args()
    if(not os.path.isfile(args.file)):
        raise SystemExit("missing %s" % args.file)
    print(object_name(args.kind, "mdf" if(args.kind == "smear") else "rdf", 1, 1))
    print("plot_delta_phi reads Diag_DPhi only; it is not a systematic assignment")


if(__name__ == "__main__"):
    main()
