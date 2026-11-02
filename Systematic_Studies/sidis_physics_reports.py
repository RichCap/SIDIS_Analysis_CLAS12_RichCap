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


def relative_link(from_dir, path):
    if(not os.path.isfile(path)):
        return path
    return os.path.relpath(path, from_dir)


def pdf_inventory(output_dir):
    found = []
    for root, dirs, files in os.walk(output_dir):
        for name in files:
            if(name.lower().endswith(".pdf")):
                found.append(os.path.join(root, name))
    found.sort()
    return found


def figure_use(path):
    name = os.path.basename(path)
    if("mosaic" in name):
        return "Chapter 6 moment figure. Statistical and systematic files stay separate."
    if("phi" in name.lower() or "Unfolded" in name):
        return "Phi_h canvas. An N/A pad is a missing histogram or fit, not a zero."
    if("kt2" in name.lower()):
        return "Chapter 6 transverse-momentum width, after the normalized BC file is the input."
    return "Supporting figure. Cite the path from this inventory."


def sector_rows(output_dir):
    rows = []
    for campaign in ["unweighted", "spline"]:
        for source in ["electron_sector", "pion_sector"]:
            base = os.path.join(output_dir, "fits", campaign, source)
            if(not os.path.isdir(base)):
                continue
            for name in sorted(os.listdir(base)):
                coverage_path = os.path.join(base, name, "fit_coverage.json")
                if(not os.path.isfile(coverage_path)):
                    continue
                coverage = read_json(coverage_path)
                rows.append({
                    "campaign": campaign,
                    "source": source,
                    "name": name,
                    "expected": coverage.get("expected"),
                    "fitted": coverage.get("fitted"),
                    "na": coverage.get("na"),
                    "pdf": os.path.join(output_dir, "phi_figures", campaign, source, name),
                })
    return rows


def moment_table(path, limit):
    if(not os.path.isfile(path)):
        return []
    payload = read_json(path)
    cells = payload.get("Fit_Pars_from_3D_BC_RC_Bayesian", {})
    lines = []
    names = sorted(cells.keys())
    for bin_name in names[:limit]:
        cell = cells[bin_name]
        lines.append("| `%s` | %s | %s | %s | %s | %s | %s |" % (
            bin_name,
            cell.get("Fit_Par_A"), cell.get("Fit_Par_A_ERR"), cell.get("Fit_Par_A_SYS"),
            cell.get("Fit_Par_B"), cell.get("Fit_Par_C"),
            cell.get("Fit_Par_B_SYS"),
        ))
    return lines, len(names)


def moment_lines(path):
    if(not os.path.isfile(path)):
        return [], 0
    return moment_table(path, 100000)


def shard_campaign(shard):
    names = []
    if(not isinstance(shard, list)):
        return "both"
    for job in shard:
        if(not isinstance(job, dict)):
            continue
        name = str(job.get("campaign", "")).strip()
        if(name != ""):
            names.append(name)
    unique = sorted(set(names))
    if(len(unique) == 1):
        return unique[0]
    return "both"


def expected_agent_records(output_dir):
    # One record per workflow stage that calls record_agent. Shard count comes from work_plan.json.
    plan_path = os.path.join(output_dir, "work_plan.json")
    plan = read_json(plan_path) if(os.path.isfile(plan_path)) else {}
    expected = [("resolve", "both", "manifest", "resolve")]
    for index, shard in enumerate(plan.get("nominal_shards", [])):
        expected.append(("nominal", shard_campaign(shard), "shard-%s" % index, "nominal"))
    variation_count = len(plan.get("variation_shards", []))
    for index in range(variation_count):
        expected.append(("variations", "both", "shard-%s" % index, "variation"))
    expected.extend([
        ("radiative", "both", "evgen", "radiative"),
        ("bin_centering", "both", "status", "bin_centering"),
        ("aggregate", "both", "budgets", "aggregate"),
        ("nominal_rc", "both", "nominal", "rc"),
        ("nominal_bc", "both", "nominal", "bc"),
        ("mosaic", "both", "nominal", "mosaic"),
        ("kt2", "both", "nominal", "kt2"),
        ("phi_figures", "both", "all", "phi-figures"),
    ])
    return expected


def markdown_report(output_dir, run_id):
    manifest_path = os.path.join(THIS_DIR, "sidis_physics_manifest.json")
    manifest = read_json(manifest_path) if(os.path.isfile(manifest_path)) else {}
    budgets_path = os.path.join(output_dir, "budgets.json")
    budgets = read_json(budgets_path) if(os.path.isfile(budgets_path)) else {}
    agents = phys.load_agent_reports(output_dir, run_id)
    report_dir = os.path.join(output_dir, "reports")
    lines = []
    lines.append("# SIDIS physics-results campaign")
    lines.append("")
    lines.append("Unweighted and Spline stay separate. Neither campaign is the quoted result. A missing uncertainty is named. It is not entered as zero.")
    lines.append("")
    lines.append("The acceptance-level budget is provisional. It is not the complete final systematic while radiative and bin-centering alternatives are outside the sum.")
    lines.append("")
    lines.append("## Nominal correction stages")
    lines.append("")
    lines.append("Acceptance `Bayesian`, then event-ratio `RC_Bayesian`, then event-based `BC_RC_Bayesian`. Each stage has its own fit file. B and C are not rescaled by the A0 factor.")
    lines.append("")
    nominals = manifest.get("nominals", {})
    for campaign in ["unweighted", "spline"]:
        row = nominals.get(campaign, {})
        products = phys.nominal_stage_products(output_dir, campaign)
        lines.append("### %s" % campaign)
        lines.append("")
        lines.append("- Weight tag `%s`, acceptance file `%s`, status `%s`." % (
            row.get("weight_tag", ""), os.path.basename(str(row.get("path", ""))), row.get("path_status", "missing"),
        ))
        for stage in ["acceptance", "rc", "bc"]:
            fit_path = products[stage]["fit"]
            state = "present" if(os.path.isfile(fit_path)) else "missing"
            lines.append("- %s fit `%s`: %s. [path](%s)" % (stage, products[stage]["fit_key"], state, relative_link(report_dir, fit_path)))
        fresh = phys.normalized_bc_path(output_dir, campaign)
        stale = phys.stale_normalized_path(output_dir, campaign)
        if(os.path.isfile(fresh)):
            payload = read_json(fresh)
            lines.append("- Latest normalization: `%s`, scope `%s`. [path](%s)" % (
                payload.get("normalization_status"), payload.get("systematic_scope"), relative_link(report_dir, fresh),
            ))
        else:
            lines.append("- Latest normalization: blocked. `normalized_bc.json` is not written. The older `normalized.json` is not the BC-stage result.")
            if(os.path.isfile(stale)):
                lines.append("- Older file kept: [normalized.json](%s)." % relative_link(report_dir, stale))
        lines.append("")
    lines.append("## Moments")
    lines.append("")
    lines.append("A0 is the normalized amplitude. B and C are dimensionless. `_ERR` is statistical. `_SYS` on a normalized file is the provisional acceptance-level systematic, scaled with A0 only.")
    lines.append("")
    for campaign in ["unweighted", "spline"]:
        path = phys.normalized_bc_path(output_dir, campaign)
        table, count = moment_lines(path)
        lines.append("### %s" % campaign)
        lines.append("")
        if(count == 0):
            lines.append("Blocked. The normalized BC file is not available, so this table is not filled from the older normalized file.")
            lines.append("")
            continue
        lines.append("Bins: `%s`." % count)
        lines.append("")
        lines.append("| Bin | A0 | stat | sys | B | C | B sys |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        lines.extend(table)
        lines.append("")
    lines.append("## Uncertainty budgets")
    lines.append("")
    lines.append("Iteration 0 is Unweighted. Iteration 1 is Spline. Acc and AccSpline are acceptance-reweighting variations, not nominals.")
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
    lines.append("Radiative SF 0, radiative SF 2, and the spline BC alternative stay out of the quadrature until that inclusion is reviewed. They are not zero. Electron and pion sectors stay `not_combined`.")
    lines.append("")
    lines.append("The subdivision source is one Unweighted RMS of 15 observable shifts after full refinement. The five variable RMS values are diagnostics. The source is not copied into Spline. Missing shifts are not zero.")
    lines.append("")
    audit_path = os.path.join(output_dir, "reports", "refinement_consistency_audit.json")
    lines.append("## Refinement audit")
    lines.append("")
    if(os.path.isfile(audit_path)):
        audit = read_json(audit_path)
        lines.append("Classifications: `%s`. An unverifiable note is not fully validated. [audit](%s)" % (audit.get("counts"), relative_link(report_dir, audit_path)))
    else:
        lines.append("The refinement audit file is not written yet. A nonempty note is not treated as a completed visual refinement.")
    lines.append("")
    lines.append("## Corrections and kT2")
    lines.append("")
    for campaign in ["unweighted", "spline"]:
        report_path = os.path.join(output_dir, "corrected", campaign, "correction_report.json")
        norm_path = os.path.join(output_dir, "corrected", campaign, "normalized.json")
        if(os.path.isfile(report_path)):
            report = read_json(report_path)
            lines.append("- %s corrections wrote `%s` histograms. Problems: `%s`." % (campaign, report.get("written"), len(report.get("problems", []))))
        if(os.path.isfile(norm_path) and (not os.path.isfile(phys.normalized_bc_path(output_dir, campaign)))):
            lines.append("- %s still has the older normalized.json. It is not the BC-stage result." % campaign)
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
    found = set()
    for record in agents["records"]:
        found.add((record.get("stage"), record.get("campaign"), record.get("source_or_shard"), record.get("label")))
    missing = []
    for item in expected_agent_records(output_dir):
        if(item not in found):
            missing.append(item)
    if(agents["missing_tree"] is not None):
        lines.append("No agent-record directory for run `%s` (`%s`)." % (run_id, agents["missing_tree"]))
    else:
        lines.append("Run `%s` has `%s` distinct agent records." % (run_id, len(agents["records"])))
        for record in agents["records"]:
            lines.append("- `%s` / `%s` / `%s` / `%s`: `%s`." % (
                record.get("stage"), record.get("campaign"), record.get("source_or_shard"), record.get("label"), record.get("path"),
            ))
    lines.append("")
    if(len(missing) == 0):
        lines.append("No expected agent record is absent.")
    else:
        lines.append("Missing agent records: `%s`. Each name is absent. It is not filled in as zero." % len(missing))
        for stage, campaign, source_or_shard, label in missing:
            path = phys.agent_report_path(output_dir, run_id, stage, campaign, source_or_shard, label)
            lines.append("- missing `%s` / `%s` / `%s` / `%s`: `%s`." % (
                stage, campaign, source_or_shard, label, os.path.relpath(path, report_dir),
            ))
    if(len(agents["collisions"]) > 0):
        lines.append("")
        lines.append("Collisions kept the later file: `%s`." % len(agents["collisions"]))
    lines.append("")
    lines.append("## Sector coverage")
    lines.append("")
    lines.append("Sectors stay `not_combined`. Counts below are from each `fit_coverage.json`. An empty histogram is N/A and is not zero.")
    lines.append("")
    covered = sector_rows(output_dir)
    if(len(covered) == 0):
        lines.append("No sector coverage files were found.")
    for row in covered:
        lines.append("- `%s` `%s` `%s`: expected `%s`, fitted `%s`, N/A `%s`." % (
            row["campaign"], row["source"], row["name"], row["expected"], row["fitted"], row["na"],
        ))
    lines.append("")
    lines.append("## Correction stages")
    lines.append("")
    lines.append("Stage A is the acceptance `Bayesian` fit. Stage B writes `RC_Bayesian` from that acceptance file and is refined on its own. Stage C writes `BC_RC_Bayesian` from the nominal RC file. A missing radiative alternative stays pending and does not block Stage B. A missing BC alternative does not block Stage C.")
    lines.append("")
    lines.append("## kT2")
    lines.append("")
    for campaign in ["unweighted", "spline"]:
        counts = kt2_counts(os.path.join(output_dir, "kt2", campaign, "kt2_results.tsv"))
        fresh = phys.normalized_bc_path(output_dir, campaign)
        if(counts is None):
            lines.append("- %s: missing." % campaign)
        else:
            lines.append("- %s rows `%s`, status counts `%s`." % (campaign, counts.get("rows"), counts))
        if(not os.path.isfile(fresh)):
            lines.append("- %s kT2 input is not the latest normalized BC file. Treat the stored table as stale until that file is the input." % campaign)
    lines.append("")
    lines.append("## Figures")
    lines.append("")
    pdfs = pdf_inventory(output_dir)
    lines.append("PDF count: `%s`. Every file is listed. A slide deck uses a subset." % len(pdfs))
    lines.append("")
    for path in pdfs:
        link = relative_link(report_dir, path)
        lines.append("- [%s](%s). %s" % (os.path.basename(path), link, figure_use(path)))
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
    add_slide("SIDIS A0, B, and C", [
        "Unweighted and Spline are separate. Neither is the quoted result.",
        "A0 is normalized once from corrected/<campaign>/bc/fit.json.",
        "B and C are not rescaled.",
        "The systematic band is the provisional acceptance-level budget.",
        "Numerical tables: reports/sidis_physics_campaign.md",
    ])
    pdfs = pdf_inventory(output_dir)
    mosaic_pdfs = [os.path.basename(path) for path in pdfs if("mosaic" in os.path.basename(path))]
    phi_pdfs = [os.path.basename(path) for path in pdfs if("Unfolded" in os.path.basename(path) or "phi" in os.path.basename(path).lower())]
    add_slide("Correction stages", [
        "Acceptance Bayesian, then event-ratio RC, then event BC.",
        "Fixed-point RC and spline BC are alternatives. They are not the nominal factors.",
        "delta_rc is cubature, not a systematic.",
        "Mosaic PDFs in this directory: %s." % len(mosaic_pdfs),
    ])
    add_slide("Sectors and systematics", [
        "Partial sector fits stay in the comparison tables and out of the quadrature.",
        "Empty pads are N/A. They are not zero.",
        "Phi_h PDFs listed in the Markdown inventory: %s." % len(phi_pdfs),
        "Radiative SF 0 versus SF 2 is not in the sum until it is reviewed.",
    ])
    add_slide("kT2 and comparisons", [
        "kT2 uses the latest normalized BC file. An older table is stale.",
        "World comparisons use the current CLAS12 moments, not the October 30 copy.",
        "Hall C moments used here are a refit from multiplicities.",
        "Theory curves are labeled as checked calculations or as interpretation only.",
        "Run %s. Full inventory is the Markdown report." % run_id,
    ])
    path = os.path.join(output_dir, "reports", "sidis_physics_results.pptx")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    presentation.save(path)
    return path
