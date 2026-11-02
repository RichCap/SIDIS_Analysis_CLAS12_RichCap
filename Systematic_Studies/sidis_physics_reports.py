#!/usr/bin/env python3
# Build the campaign Markdown report and the PowerPoint from artifacts already on disk.
# Does not fit, unfold, or start EvGen.

import csv
import json
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)
import sidis_physics_lib as phys


def read_json(path):
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    return payload


def kt2_counts(path):
    if(not os.path.isfile(path)):
        return None
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    counts = {}
    for row in rows:
        status = row.get("status", "")
        counts[status] = counts.get(status, 0) + 1
    counts["rows"] = len(rows)
    return counts


def markdown_report(output_dir, run_id):
    manifest_path = os.path.join(THIS_DIR, "sidis_physics_manifest.json")
    manifest = read_json(manifest_path) if(os.path.isfile(manifest_path)) else {}
    budgets_path = os.path.join(output_dir, "budgets.json")
    budgets = read_json(budgets_path) if(os.path.isfile(budgets_path)) else {}
    agents = phys.load_agent_reports(output_dir, run_id)
    lines = []
    lines.append("# SIDIS physics-results campaign")
    lines.append("")
    lines.append("This note describes the Unweighted and Spline campaigns that are already on disk. Both budgets are provisional. Neither campaign is selected as the quoted result.")
    lines.append("")
    lines.append("## Nominals")
    lines.append("")
    nominals = manifest.get("nominals", {})
    for campaign in ["unweighted", "spline"]:
        row = nominals.get(campaign, {})
        lines.append("- %s: weight tag `%s`, file `%s`, status `%s`." % (
            campaign, row.get("weight_tag", ""), os.path.basename(str(row.get("path", ""))), row.get("path_status", "missing"),
        ))
    lines.append("")
    lines.append("Iteration 0 is Unweighted. Iteration 1 is Spline. Acc and AccSpline are acceptance-reweighting variations.")
    lines.append("")
    lines.append("## Uncertainty budgets")
    lines.append("")
    budget_root = budgets.get("budgets", {})
    for campaign in ["unweighted", "spline"]:
        block = budget_root.get(campaign, {})
        sources = sorted(block.get("sources", {}).keys()) if(isinstance(block.get("sources"), dict)) else []
        lines.append("### %s" % campaign)
        lines.append("")
        lines.append("- Provisional: `%s`." % block.get("provisional", True))
        lines.append("- Bins in the total: `%s`." % len(block.get("totals", {})))
        lines.append("- Sources in the table: %s." % (", ".join(sources) if(len(sources) > 0) else "none"))
        excluded = [item for item in block.get("excluded", []) if(str(item).strip() != "")]
        if(len(excluded) > 0):
            lines.append("- Excluded from the sum: %s." % "; ".join(excluded))
        lines.append("")
    lines.append("That exclusion text is what the first aggregation wrote. The manifest now uses `inherited_Spline.root` as the Spline nominal, `inherited_Acc.root` as the Unweighted acceptance variation, and the corrected same-weight method branches. Those comparisons are not in the budget file yet and were not fit for this update.")
    lines.append("")
    lines.append("The subdivision systematic is one Unweighted RMS of 15 observable shifts. Those fitted shifts are not in this directory yet, so the source is not in the sum and is not entered as zero. The five variable RMS values are diagnostics. The Spline budget does not receive this source.")
    lines.append("")
    lines.append("## Fit quality and sector failures")
    lines.append("")
    lines.append("The first fits are a single remake. `refine-phi-fits` was not completed, so a return code of 0 is an initial fit, not a finished refinement.")
    lines.append("")
    failed = budgets.get("failed", [])
    lines.append("Registry failures recorded in the budget file: `%s`." % len(failed))
    lines.append("")
    lines.append("Unweighted eS1o stopped while fitting `(Q2_y_Bin_3)-(z_pT_Bin_4)`. That unfolded histogram has integral 0 and 24 empty phi bins. The same nominal bin is filled. eS1o has 422 filled and 30 empty Bayesian histograms. The nominal file has 452 filled and none empty. `TH1::Fit` on the empty histogram calls `Warning()`, and that warning segfaults inside CPyCppyy. Return code 129 is the status after the printed segmentation violation. The fitter now skips a histogram whose integral is 0 and keeps ROOT at error level during `TH1::Fit`. The 24 sector jobs were not refit. They stay `not_combined` and are not zero.")
    lines.append("")
    lines.append("## Corrections and kT2")
    lines.append("")
    for campaign in ["unweighted", "spline"]:
        report_path = os.path.join(output_dir, "corrected", campaign, "correction_report.json")
        norm_path = os.path.join(output_dir, "corrected", campaign, "normalized.json")
        if(os.path.isfile(report_path)):
            report = read_json(report_path)
            lines.append("- %s corrections wrote `%s` histograms. Problems: `%s`." % (campaign, report.get("written"), len(report.get("problems", []))))
        if(os.path.isfile(norm_path)):
            norm = read_json(norm_path)
            lines.append("- %s normalization status `%s`. Provisional systematic `%s`. Factor uncertainty unassigned: `%s`." % (
                campaign, norm.get("normalization_status"), norm.get("provisional_systematic"), norm.get("unassigned_factor_uncertainty"),
            ))
        counts = kt2_counts(os.path.join(output_dir, "kt2", campaign, "kt2_results.tsv"))
        if(counts is not None):
            lines.append("- %s kT2 rows `%s`, status counts `%s`. Source file `kt2/%s/kt2_results.tsv`." % (campaign, counts.get("rows"), counts, campaign))
    lines.append("")
    lines.append("B and C are not rescaled by the A0 factor. Their `_SYS` values stay on the unfolded scale.")
    lines.append("")
    lines.append("## Bin centering")
    lines.append("")
    lines.append("Nominal event factors are the 2026-10-26 JSON. `BC_Factor` is the unweighted sub-bin mean divided by the center sub-bin. The injection spline file is `%s`." % os.path.basename(phys.INJECTION_SPLINE_TXT))
    lines.append("")
    lines.append("The updated post-refit spline is not named by the campaign configuration, so the iteration comparison stays blocked. EvGen evaluation at the same points is deferred.")
    lines.append("")
    lines.append("## Agent records")
    lines.append("")
    if(agents["missing_tree"] is not None):
        lines.append("No agent-record directory for run `%s` (`%s`)." % (run_id, agents["missing_tree"]))
    else:
        lines.append("Run `%s` has `%s` distinct agent records." % (run_id, len(agents["records"])))
        for record in agents["records"]:
            lines.append("- `%s` / `%s` / `%s` / `%s`: `%s`." % (
                record.get("stage"), record.get("campaign"), record.get("source_or_shard"), record.get("label"), record.get("path"),
            ))
    if(len(agents["collisions"]) > 0):
        lines.append("")
        lines.append("Collisions kept the later file: `%s`." % len(agents["collisions"]))
    lines.append("")
    coverage_path = os.path.join(output_dir, "reports", "sector_coverage.json")
    lines.append("## Sector coverage")
    lines.append("")
    if(os.path.isfile(coverage_path)):
        coverage = read_json(coverage_path)
        lines.append("Sector studies stay out of quadrature. Empty histograms are N/A and are not zeroes. Fitted count is from saved JSON, which is zero while those jobs remain failed.")
        lines.append("")
        for row in coverage.get("sectors", []):
            lines.append("- `%s` `%s`: expected `%s`, fitted `%s`, N/A empty `%s`, other failures `%s`, empty fraction `%s`, filled but not saved `%s`." % (
                row.get("campaign"), row.get("name"), row.get("expected"), row.get("fitted"), row.get("empty"), row.get("other_failure"), row.get("empty_fraction"), row.get("interrupted_before_save"),
            ))
        if(coverage.get("lower_acceptance_review")):
            lines.append("")
            lines.append(coverage["lower_acceptance_review"])
    else:
        lines.append("Sector coverage file is not written yet.")
    lines.append("")
    lines.append("## Correction stages")
    lines.append("")
    lines.append("Stage A is the acceptance `Bayesian` fit. Stage B writes `RC_Bayesian` from that acceptance file and is refined on its own. Stage C writes `BC_RC_Bayesian` from the nominal RC file. A missing radiative alternative stays pending and does not block Stage B. A missing BC alternative does not block Stage C.")
    lines.append("")
    lines.append("## Figures")
    lines.append("")
    lines.append("Mosaic commands use z, P_T, and P_T2, a logarithmic A0 axis, `bin_Q2y` pad labels, series legends, and separate statistical and systematic files. Phi_h figures, when drawn, use `consolidate-thesis-phi-figures` for `unfolded_ac`, `unfolded_rc`, and `unfolded_bc` only.")
    lines.append("")
    lines.append("Artifact directory: `%s`." % os.path.abspath(output_dir))
    lines.append("")
    return "\n".join(lines)


def write_markdown(output_dir, run_id):
    text = markdown_report(output_dir, run_id)
    path = os.path.join(output_dir, "reports", "sidis_physics_campaign.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    handle = open(path, "w")
    handle.write(text)
    handle.close()
    return path


def write_pptx(output_dir, run_id):
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
    except ImportError:
        raise SystemExit("python-pptx is not installed. The PowerPoint stage stops here.")
    presentation = Presentation()
    presentation.slide_width = Inches(13.333)
    presentation.slide_height = Inches(7.5)

    def add_slide(title, bullets):
        layout = presentation.slide_layouts[1]
        slide = presentation.slides.add_slide(layout)
        slide.shapes.title.text = title
        body = slide.placeholders[1].text_frame
        body.clear()
        first = True
        for bullet in bullets:
            paragraph = body.paragraphs[0] if(first) else body.add_paragraph()
            first = False
            paragraph.text = bullet
            paragraph.font.size = Pt(18)

    text = markdown_report(output_dir, run_id)
    add_slide("SIDIS physics results", [
        "Unweighted and Spline budgets stay separate.",
        "Both budgets are provisional. Neither is the quoted result.",
        "Run %s." % run_id,
        "Source note: reports/sidis_physics_campaign.md",
    ])
    add_slide("What this deck is", [
        "Figures and short tables from artifacts already written.",
        "Fit quality uses stored Chi2, NDF, and status fields when those files are present.",
        "Pending studies are named and are not entered as zero.",
    ])
    budget_bits = []
    for line in text.splitlines():
        if(line.startswith("- ") and (("Provisional" in line) or ("Sources in the table" in line) or ("kT2" in line) or ("normalization" in line))):
            budget_bits.append(line[2:])
    if(len(budget_bits) == 0):
        budget_bits.append("Budget file was not found.")
    add_slide("Budgets and kT2", budget_bits[:8])
    add_slide("Still open", [
        "Refinement notes are not recorded for the first single-pass fits.",
        "Sector fits failed inside TH1::Fit and stay out of the sum.",
        "Subdivision RMS waits on fitted A, B, and C shifts.",
        "Spline iteration comparison and EvGen bin centering stay blocked.",
        "Radiative systematic stays pending.",
    ])
    path = os.path.join(output_dir, "reports", "sidis_physics_results.pptx")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    presentation.save(path)
    return path
