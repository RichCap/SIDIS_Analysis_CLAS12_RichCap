#!/usr/bin/env python3
# Recovery, fixed-point cache, comparison, and thesis-plan helpers.
# This module does not unfold, refit, or start the RC or BC grids.

import fcntl
import json
import os
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if(THIS_DIR not in sys.path):
    sys.path.insert(0, THIS_DIR)
import sidis_physics_lib as phys

THESIS_ROOT = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis"
WORLD_TABLE_DIR = "/Users/richardcapobianco/Desktop/World_Data_Tables"
WORLD_REPORT = "/Users/richardcapobianco/Desktop/World_Data_Comparison_Report.md"


def read_json(path):
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    return payload


def overlay_count(directory):
    count = 0
    if(not os.path.isdir(directory)):
        return 0
    for root, dirs, files in os.walk(directory):
        for name in files:
            if(name.lower().endswith((".pdf", ".png"))):
                count += 1
    return count


def audit_one_directory(directory):
    note_path = os.path.join(directory, "refinement_note.json")
    fit_path = os.path.join(directory, "fit.json")
    init_path = os.path.join(directory, "refine_init.py")
    note = read_json(note_path) if(os.path.isfile(note_path)) else None
    fit_payload = read_json(fit_path) if(os.path.isfile(fit_path)) else None
    init_text = open(init_path).read() if(os.path.isfile(init_path)) else ""
    overlays = overlay_count(directory)
    result = phys.classify_refinement_dir(note, fit_payload, init_text, overlays)
    result["directory"] = directory
    result["note"] = note_path
    result["fit"] = fit_path
    result["refine_init"] = init_path if(os.path.isfile(init_path)) else ""
    result["overlay_count"] = overlays
    return result


def audit_refinements(output_dir):
    rows = []
    for folder in ["fits", "corrected"]:
        root = os.path.join(output_dir, folder)
        if(not os.path.isdir(root)):
            continue
        for current, dirs, files in os.walk(root):
            if("refinement_note.json" in files):
                rows.append(audit_one_directory(current))
    rows.sort(key=lambda row: row["directory"])
    counts = {"verified": 0, "incomplete": 0, "unverifiable": 0}
    for row in rows:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    return {"count": len(rows), "counts": counts, "rows": rows}


def audit_markdown(report, output_dir):
    lines = []
    lines.append("# Refinement consistency audit")
    lines.append("")
    lines.append("This audit only reads fit JSON, refinement notes, guide files, and overlay files. It does not refit.")
    lines.append("")
    lines.append("`verified` means each stated after-quality matches the saved fit and the stated cell count matches. It is not a new visual review of every histogram.")
    lines.append("")
    lines.append("`unverifiable` means the note cannot be checked against a stored before/after number. Those fits stay in place and are not fully validated.")
    lines.append("")
    lines.append("`incomplete` is the only class scheduled for a later targeted refinement.")
    lines.append("")
    lines.append("Records: `%s`. Verified: `%s`. Incomplete: `%s`. Unverifiable: `%s`." % (
        report["count"], report["counts"].get("verified", 0), report["counts"].get("incomplete", 0), report["counts"].get("unverifiable", 0),
    ))
    lines.append("")
    for label in ["incomplete", "unverifiable", "verified"]:
        lines.append("## %s" % label)
        lines.append("")
        found = [row for row in report["rows"] if(row["classification"] == label)]
        if(len(found) == 0):
            lines.append("None.")
            lines.append("")
            continue
        for row in found:
            lines.append("- `%s`" % os.path.relpath(row["directory"], output_dir))
            lines.append("  - Reason: %s" % row["reason"])
            if(str(row.get("minimum_check", "")).strip() != ""):
                lines.append("  - Minimum check: %s" % row["minimum_check"])
            for item in row.get("evidence", [])[:4]:
                lines.append("  - Evidence: %s" % item)
        lines.append("")
    return "\n".join(lines)


def write_audit(output_dir, manifest_path):
    report = audit_refinements(output_dir)
    json_path = os.path.join(output_dir, "reports", "refinement_consistency_audit.json")
    md_path = os.path.join(output_dir, "reports", "SIDIS_Refinement_Consistency_Audit.md")
    phys.write_json(json_path, report)
    handle = open(md_path, "w")
    handle.write(audit_markdown(report, output_dir))
    handle.write("\n")
    handle.close()
    if(os.path.isfile(manifest_path)):
        manifest = read_json(manifest_path)
        compact = []
        for row in report["rows"]:
            compact.append({
                "directory": row["directory"],
                "classification": row["classification"],
                "reason": row["reason"],
                "minimum_check": row.get("minimum_check", ""),
                "validated": row["classification"] == "verified",
            })
        manifest["refinement_audit"] = {
            "count": report["count"],
            "counts": report["counts"],
            "report": md_path,
            "evidence": json_path,
            "rows": compact,
        }
        phys.write_json(manifest_path, manifest)
    return {"markdown": md_path, "json": json_path, "counts": report["counts"], "count": report["count"]}


def normalized_bc_status(output_dir):
    missing = []
    present = []
    for campaign in ["unweighted", "spline"]:
        path = phys.normalized_bc_path(output_dir, campaign)
        if(os.path.isfile(path)):
            present.append(path)
        else:
            missing.append(path)
    return {"present": present, "missing": missing, "ready": len(missing) == 0}


def world_comparison_report(output_dir):
    status = normalized_bc_status(output_dir)
    tables = []
    if(os.path.isdir(WORLD_TABLE_DIR)):
        for name in sorted(os.listdir(WORLD_TABLE_DIR)):
            tables.append(name)
    blocker = ""
    if(not status["ready"]):
        blocker = "normalized_bc.json is absent, so current CLAS12 moments are not available for comparison"
    lines = []
    lines.append("# World-data comparison status")
    lines.append("")
    lines.append("The Desktop research report is context. Its CLAS12 values and agreement statistics are not used.")
    lines.append("")
    lines.append("Hall C `hallc_2510.03562_cos_moments_refit_all.csv` is a refit from published multiplicities. It is not the collaboration's published moment table.")
    lines.append("")
    lines.append("HERMES cosine moments are not in the table directory and are not invented.")
    lines.append("")
    lines.append("Osipenko comparisons, when the CLAS12 file exists, use the depolarization conversion re-derived from the CSVs. Repeated matches to one CLAS12 bin are correlated and are not a naive chi-squared.")
    lines.append("")
    lines.append("No-rho0 overlays use the actual NoRho0 fits. They are not an assumed rescaling of the nominal result.")
    lines.append("")
    if(blocker != ""):
        lines.append("Status: blocked.")
        lines.append("")
        lines.append(blocker + ".")
    else:
        lines.append("Status: ready to plot from the normalized BC files.")
    lines.append("")
    lines.append("Table files present: `%s`." % len(tables))
    for name in tables:
        lines.append("- `%s`" % name)
    lines.append("")
    if(os.path.isfile(WORLD_REPORT)):
        lines.append("Supporting report: `%s`." % WORLD_REPORT)
    lines.append("")
    return {"status": "blocked" if(blocker != "") else "ready", "blocker": blocker, "markdown": "\n".join(lines), "tables": tables}


def theory_comparison_report(output_dir):
    status = normalized_bc_status(output_dir)
    blocker = ""
    if(not status["ready"]):
        blocker = "normalized_bc.json is absent, so theory curves are not evaluated on the current moments"
    lines = []
    lines.append("# Theory comparison status")
    lines.append("")
    lines.append("No numerical curve is written in this status file. A curve is computed only from a checked formula and its published parameters.")
    lines.append("")
    lines.append("- Cahn Gaussian: diagnostic, once the normalized moments exist. Not a published prediction by itself.")
    lines.append("- Barone et al. 2015: use the published Cahn and Boer-Mulders calculation. An incomplete Boer-Mulders term is not labeled as that paper's full model.")
    lines.append("- Bastami et al. 2019 and Balitsky and Prokudin 2026: interpretation-only until the paper formula used here is checked against the publication. They are not fabricated curves.")
    lines.append("- A0 comparisons prefer shape and P_T width unless absolute normalization has been shown to match.")
    lines.append("")
    if(blocker != ""):
        lines.append("Status: blocked.")
        lines.append("")
        lines.append(blocker + ".")
    else:
        lines.append("Status: the moments exist. Quantitative curves still require the checked formulas before they are plotted.")
    lines.append("")
    state = "blocked" if(blocker != "") else "interpretation_only"
    return {"status": state, "blocker": blocker, "markdown": "\n".join(lines)}


def mosaic_is_older_than_normalized_bc(output_dir):
    newest = 0.0
    found = False
    folder = os.path.join(output_dir, "mosaics")
    if(os.path.isdir(folder)):
        for name in os.listdir(folder):
            if(name.lower().endswith(".pdf")):
                found = True
                stamp = os.path.getmtime(os.path.join(folder, name))
                if(stamp > newest):
                    newest = stamp
    if(not found):
        return True
    for campaign in ["unweighted", "spline"]:
        norm_path = phys.normalized_bc_path(output_dir, campaign)
        if(not os.path.isfile(norm_path)):
            return True
        if(os.path.getmtime(norm_path) > newest):
            return True
    return False


def comparison_figure_count(output_dir):
    count = 0
    root = os.path.join(output_dir, "reports")
    if(not os.path.isdir(root)):
        return 0
    for current, dirs, files in os.walk(root):
        for name in files:
            lower = name.lower()
            plotted = lower.endswith(".pdf") or lower.endswith(".png")
            named = ("world" in lower) or ("theory" in lower) or ("hall" in lower)
            if(plotted and named):
                count += 1
    return count


def thesis_rows(output_dir):
    world = world_comparison_report(output_dir)
    theory = theory_comparison_report(output_dir)
    norm = normalized_bc_status(output_dir)
    figures = comparison_figure_count(output_dir)
    mosaics_stale = mosaic_is_older_than_normalized_bc(output_dir)
    if(not norm["ready"]):
        moment_status = "blocked"
        moment_dependency = "write and check normalized_bc.json"
    elif(mosaics_stale):
        moment_status = "blocked"
        moment_dependency = "redraw z, P_T, and P_T^2 mosaics from normalized_bc.json, without a second A0 scale, before any figure is inserted"
    else:
        moment_status = "provisional"
        moment_dependency = "choose the quoted campaign; the acceptance-level band is not the final systematic"
    if(figures == 0):
        world_status = "blocked"
        theory_status = "blocked"
        world_dependency = "no world-data overlay, residual plot, or agreement table has been written"
        theory_dependency = "no checked theory curve has been written"
    else:
        world_status = "provisional"
        theory_status = "provisional"
        world_dependency = "review the comparison figures before they replace the placeholder"
        theory_dependency = "a plotted curve still has to be checked against the publication"
    if(world["status"] == "blocked"):
        world_status = "blocked"
        world_dependency = world["blocker"]
    if(theory["status"] == "blocked"):
        theory_status = "blocked"
        theory_dependency = theory["blocker"]
    conclusion_status = "blocked"
    if((world_status == "blocked") or (theory_status == "blocked") or (moment_status == "blocked")):
        conclusion_dependency = "validated moment figures and validated world and theory comparisons"
    else:
        conclusion_dependency = "a quoted campaign and reviewed comparison text"
    rows = [
        {
            "chapter": "5",
            "section": "Radiative Corrections",
            "source": "Analysis_Procedures/Analysis_Procedures_SubSections/Radiative_Corrections.tex",
            "location": "equation RadiativeCorrection and RC_Factor_Application",
            "action": "retain",
            "artifact": "",
            "caption": "",
            "citation": "BYER2023108702",
            "text": "Keep the nominal factor as the radiated-to-Born event ratio and the application as division of the acceptance-corrected yield. Do not restore the commented bin-center fit as the nominal correction.",
            "justification": "The live equations match apply_nominal_corrections.py, which writes RC_Bayesian by dividing by the event-ratio factors. The fixed-point cross section is a separate alternative.",
            "status": "verified",
            "dependency": "",
        },
        {
            "chapter": "5",
            "section": "Radiative Corrections",
            "source": "Analysis_Procedures/Analysis_Procedures_SubSections/Radiative_Corrections.tex",
            "location": "after RC_Factor_Application; the commented eq:RCPhiFit stays commented",
            "action": "revise",
            "artifact": os.path.join(output_dir, "fixed_point", "rc_grid_status.json"),
            "caption": "",
            "citation": "BYER2023108702",
            "text": "Add that a fixed-point sigma_tot/sigma_B evaluation is an alternative used only for model dependence. It is not the nominal factor. Its cubature uncertainty is not an experimental systematic. SF 0 is Prokudin. SF 2 is the electroproduction A_ep spline, and that spline omits the virtual-photon flux. The RC cache finished with 10848 succeeded cells for each of SF 0 and SF 2. No moment-shift table was formed from that cache, so neither alternative enters the quadrature and no shift is quoted.",
            "justification": "rc_grid_status.json records complete grids. budgets.json still excludes radiative SF 0, SF 2, and their difference, and stores no radiative number. The number is not zero.",
            "status": "provisional",
            "dependency": "reviewed radiative shift tables; do not quote the cache as a systematic",
        },
        {
            "chapter": "5",
            "section": "Bin-Centering Corrections",
            "source": "Analysis_Procedures/Analysis_Procedures.tex",
            "location": "equation eq:BC_Factor_Definition and eq:BC_Factor_Application",
            "action": "retain",
            "artifact": phys.BC_EVENT_JSON,
            "caption": "",
            "citation": "",
            "text": "Keep BC as the unweighted sub-bin mean divided by the center sub-bin, zeros included, on the 3x3x3x3x5 grid. The nominal application divides the RC-corrected yield by that factor.",
            "justification": "The live equations match the nominal JSON field BC_Factor and the nominal Stage C application.",
            "status": "verified",
            "dependency": "",
        },
        {
            "chapter": "5",
            "section": "Bin-Centering Corrections",
            "source": "Analysis_Procedures/Analysis_Procedures.tex",
            "location": "equation eq:BCIterationWeight and the paragraph that says the fully corrected results include this BC factor",
            "action": "revise",
            "artifact": phys.INJECTION_SPLINE_TXT,
            "caption": "",
            "citation": "",
            "text": "State that the campaign nominal factor is the event-style unweighted JSON, not the one-update weight in eq:BCIterationWeight and not a spline. The histogram-weight spline is the raw-amplitude file. It is not the electroproduction A_ep spline. A_ep divides Fit_Par_A by the bin area and luminosity and does not divide by Gamma. Histogram normalization may still divide by Gamma. B and C stay dimensionless in both conventions. The spline BC alternative and the iteration stay out of the quoted systematic.",
            "justification": "bin_centering.json keeps the iteration and the spline-transfer method not combined, with a null systematic. The injection path is the raw-amplitude file named by the workflow.",
            "status": "verified",
            "dependency": "",
        },
        {
            "chapter": "5",
            "section": "Procedure Overview",
            "source": "Analysis_Procedures/Analysis_Procedures_SubSections/Procedural_Overview.tex",
            "location": "equation eq:NormalizedA, after eq:DeltaPT2",
            "action": "revise",
            "artifact": phys.normalized_bc_path(output_dir, "unweighted"),
            "caption": "",
            "citation": "klimenko2024",
            "text": "Keep the luminosity, beam-blocker, and tracking factors, and keep Gamma in the reported histogram amplitude. State that normalized_bc.json divides the stored Fit_Par_A by bin area times luminosity times Gamma after the fit, with Delta(p_T^2) in that area, and does not rescale B or C. eq:BinVolume itself uses Delta(p_T). A later figure must say which width it used. Do not interchange that file with the A_ep spline, which omits Gamma.",
            "justification": "write_normalized_results.py sets pT2 true and builds A0 from area, luminosity, and flux. The electroproduction note keeps Gamma out of A_ep. The two files are not the same amplitude.",
            "status": "provisional",
            "dependency": "the quoted figure must name Delta(p_T) or Delta(p_T^2) before the normalized file is inserted",
        },
        {
            "chapter": "5",
            "section": "Acceptance Corrections",
            "source": "Analysis_Procedures/Analysis_Procedures_SubSections/Acceptance_Corrections.tex",
            "location": "tab:UnfoldingSummary and the paragraph on the 5D matrix",
            "action": "retain",
            "artifact": "",
            "caption": "",
            "citation": "DAgostini:1994fjx",
            "text": "Keep the 3D Bayesian result as the result shown in the thesis. Keep the 5D matrix as a systematic test, not as the source of the quoted moments. Do not change the stated acceptance threshold 0.020 or the iteration choice k=6 in Q2-y bins 1 and 5 and k=5 otherwise.",
            "justification": "Those choices are the live thesis text and the nominal campaign definition. The Spline 5D file is absent and contributes no number.",
            "status": "verified",
            "dependency": "",
        },
        {
            "chapter": "6",
            "section": "Cosine Moment Extractions",
            "source": "Results/Results_SubSections/Cosine_Moment_Extractions.tex",
            "location": "the averaged percent-difference paragraph and the commented 455-bin note",
            "action": "revise",
            "artifact": phys.normalized_bc_path(output_dir, "unweighted"),
            "caption": "",
            "citation": "",
            "text": "Do not keep or recompute those percentages for this plan. They describe an older acc025 chain, and the comment quotes 455 bins. Each normalized_bc.json has 452 Fit_Pars_from_3D_BC_RC_Bayesian cells. Leave the paragraph unchanged until a new average is calculated from the campaign fits. Do not invent a replacement percentage.",
            "justification": "The live images are named 3D_rho0_acc025 and 3D_WITHOUT_rho0_acc025. The campaign files are the 0.020 nominal chain. The counts and the filenames are not the same result.",
            "status": "blocked",
            "dependency": "a new stage-to-stage average from the campaign fits, calculated separately for Unweighted and Spline",
        },
        {
            "chapter": "6",
            "section": "Cosine Moment Extractions",
            "source": "Results/Results_SubSections/Cosine_Moment_Extractions.tex",
            "location": "fig:Moments_Bayesian_noRho_z through fig:Moments_BCRC_pT",
            "action": "revise",
            "artifact": os.path.join(output_dir, "mosaics"),
            "caption": "Acceptance, radiative, and bin-centering corrected A0, B, and C. The band is the provisional acceptance-level budget, not the final systematic. Unweighted and Spline are separate.",
            "citation": "",
            "text": "Do not replace the four existing correction-stage figures until the mosaics are redrawn from normalized_bc.json. The redraw does not pass the A0 scale a second time and keeps the two campaigns apart. The existing acc025 figures stay until that redraw exists. Do not call the band final, and do not choose a quoted campaign in the caption." + (" The current mosaic PDFs are older than normalized_bc.json." if(mosaics_stale) else ""),
            "justification": "normalized_bc.json is labeled provisional_acceptance_level. Neither campaign is the quoted result." + (" The mosaic directory is older than both normalized files." if(mosaics_stale) else " The mosaic files are not older than the normalized files."),
            "status": moment_status,
            "dependency": moment_dependency,
        },
        {
            "chapter": "6",
            "section": "Cosine Moment Extractions",
            "source": "Results/Results_SubSections/Cosine_Moment_Extractions.tex",
            "location": "end of the section, after the P_T moment figures and before Closure Tests",
            "action": "add",
            "artifact": os.path.join(output_dir, "kt2", "unweighted", "run_20261102_152727", "kt2_results.tsv"),
            "caption": "Gaussian P_T^2 slope of normalized A0. The error is the provisional acceptance-level uncertainty. This is not a measured intrinsic width.",
            "citation": "",
            "text": "Add the kT2 figure only from run_20261102_152727, not from the older top-level kt2_results.tsv. Unweighted has 91 rows: all 91 have a large log uncertainty, 78 are also consistent with zero slope, and 13 are not. Spline has 91 rows: all 91 have a large log uncertainty, 80 are also consistent with zero slope, and 11 are not. Do not quote one width, and do not interpret the slope as a model conclusion. Keep the two campaigns separate. The spline companion table is the same run directory under kt2/spline.",
            "justification": "That run used the normalized BC file and the systematic error field. The top-level TSV is an older, different file. A slope consistent with zero is not a kT2 measurement.",
            "status": "provisional",
            "dependency": "the same quoted-campaign choice as the moment figures; do not promote the top-level TSV",
        },
        {
            "chapter": "6",
            "section": "Closure Tests",
            "source": "Results/Results_SubSections/Closure_Tests.tex",
            "location": "sec:Unfold_MC and sec:phi_h_edge_cuts",
            "action": "retain",
            "artifact": "",
            "caption": "",
            "citation": "",
            "text": "Leave the three placeholder paragraphs as they are. Do not add a closure number, a passed or failed statement, or an edge-cut tolerance.",
            "justification": "The section states the tests and does not report a result. No closure artifact was produced for this plan.",
            "status": "blocked",
            "dependency": "a stored closure result; none is available",
        },
        {
            "chapter": "6",
            "section": "Systematic Uncertainties",
            "source": "Results/Results_SubSections/Systematic_Uncertainties.tex",
            "location": "tab:SystematicUncertainties; keep the following input order unchanged",
            "action": "revise",
            "artifact": os.path.join(output_dir, "budgets.json"),
            "caption": "Source list in the present order. Blank cells are not zero. The total band is provisional and acceptance-level.",
            "citation": "",
            "text": "Keep every subsection in its current order, from the sampling fraction through acceptance reweighting. Do not fill the three moment columns from the raw budget RMS. Those A shifts are not in the normalized A0 units. The normalized total is Fit_Par_A_SYS, Fit_Par_B_SYS, and Fit_Par_C_SYS, and it is provisional. Per-source cells stay blank until a scaled per-source table exists. Sectors, radiative alternatives, the spline BC alternative, the BC iteration, and the fifteen-subdivision RMS stay out of the sum. A missing source is named and is not entered as zero.",
            "justification": "budgets.json is provisional for both campaigns. electron_sector and pion_sector are not combined. The radiative and bin-centering alternatives are listed under excluded and have no number. Subdivision shifts were not fitted, so they are not in the sum. The fifteen-file RMS, once it exists, is one Unweighted term, not five terms, and it is not copied into Spline.",
            "status": "blocked",
            "dependency": "a per-source table scaled like normalized_bc.json, plus the missing radiative and bin-centering shifts",
        },
        {
            "chapter": "6",
            "section": "Sector dependence",
            "source": "Results/Results_SubSections/Uncertainties_SubSections/Sys_Sector_Dependence.tex",
            "location": "after the last paragraph of sys-sector",
            "action": "add",
            "artifact": os.path.join(output_dir, "phi_figures"),
            "caption": "Partial sector phi_h canvases. Empty pads are N/A and are not zero. Sectors are not in the final quadrature.",
            "citation": "",
            "text": "The twelve electron-sector and twelve pion-sector canvases may be shown as diagnostics. Keep both sector families out of the final quadrature until that inclusion is authorized. Do not replace an empty pad by zero.",
            "justification": "Twenty-four sector PDFs are present under phi_figures. budgets.json marks both sector sources not combined. Empty bins stay out of the RMS.",
            "status": "provisional",
            "dependency": "authorization to show sector diagnostics; they still do not enter the sum",
        },
        {
            "chapter": "6",
            "section": "Radiative-Correction Model Dependence",
            "source": "Results/Results_SubSections/Uncertainties_SubSections/Sys_Radiative_Model.tex",
            "location": "sys-rc-model, after the description of the alternative",
            "action": "revise",
            "artifact": os.path.join(output_dir, "fixed_point", "rc_grid_status.json"),
            "caption": "",
            "citation": "BYER2023108702",
            "text": "Keep the nominal description. Add that the fixed-point SF 0 and SF 2 caches finished and that their moment shifts were not extracted or reviewed. Do not write a systematic value. The cubature uncertainty on sigma_tot/sigma_B is not that value.",
            "justification": "The subsection defines the comparison. The cache does not by itself supply the shift of A0, B, or C. The budget excludes it.",
            "status": "provisional",
            "dependency": "reviewed radiative shift tables",
        },
        {
            "chapter": "6",
            "section": "BC Corrections",
            "source": "Results/Results_SubSections/Uncertainties_SubSections/Sys_Iterative_Bin_Centering.tex",
            "location": "sys-bc-iter and sys-bc-kin",
            "action": "revise",
            "artifact": os.path.join(output_dir, "reports", "bin_centering.json"),
            "caption": "",
            "citation": "",
            "text": "Keep the definitions. State that the one-update azimuthal weight and the spline alternative are not combined. The fifteen subdivision files are on disk, but the fitted A, B, and C shifts from a full refinement are not. Those shifts become one pooled RMS for Unweighted only, not five quadrature terms, and they are not copied into Spline. Until those shifts exist, the cells stay blank.",
            "justification": "bin_centering.json records the subdivision files and awaiting_observable_shifts. The iteration and method systematics are null.",
            "status": "provisional",
            "dependency": "fifteen refined subdivision shifts before any BC sampling number is entered",
        },
        {
            "chapter": "7",
            "section": "Comparisons to World Data",
            "source": "Conclusions/Conclusions_SubSections/Comparisons_to_World_Data.tex",
            "location": "section body; it is one placeholder sentence",
            "action": "replace",
            "artifact": os.path.join(output_dir, "reports", "world_comparisons.md"),
            "caption": "B and C at matched kinematics. Hall C moments, if shown, are a refit from published multiplicities.",
            "citation": "HallCSIDIS:2025plr",
            "text": "Do not replace the placeholder with the readiness note. Fill the section only from comparison figures that do not yet exist. Use the current normalized moments, not the October 30 CLAS12 values and not their chi-squared. hallc_2510.03562_cos_moments_refit_all.csv is a refit, not the Hall C published moment table; HallCSIDIS:2025plr is the multiplicity paper. HarrisonThesis and Osipenko:2008rv are the other CLAS samples already in the bibliography. HERMES cosine moments are absent from the table directory and are not invented. A no-rho0 curve uses the NoRho0 fits, not a rescaling. Do not claim a first multidimensional or first same-energy measurement.",
            "justification": "The tex file is one sentence. world_comparisons.md lists external tables and does not contain an overlay, a residual plot, or an agreement table.",
            "status": world_status,
            "dependency": world_dependency,
        },
        {
            "chapter": "7",
            "section": "Comparisons to Theory Models",
            "source": "Conclusions/Conclusions_SubSections/Comparisons_to_Theory_Models.tex",
            "location": "section body; it is one placeholder sentence",
            "action": "add",
            "artifact": os.path.join(output_dir, "reports", "theory_comparisons.md"),
            "caption": "",
            "citation": "Cahn:1978se",
            "text": "Do not add a numerical curve. Cahn:1978se may be named as the kinematic effect already used in the thesis, not as a new plotted prediction. Barone et al. 2015, Bastami et al. 2019, and Balitsky and Prokudin 2026 stay interpretation-only: no checked formula is stored, and those papers were not given citation keys in this plan. Do not present a partial Boer-Mulders term as the Barone et al. 2015 model. An A0 comparison, once a checked curve exists, prefers shape and P_T width unless the absolute normalization has been shown to match.",
            "justification": "theory_comparisons.md states that no numerical curve is written. The bibliography was searched for those three model papers and no matching key was used here.",
            "status": theory_status,
            "dependency": theory_dependency,
        },
        {
            "chapter": "7",
            "section": "Final Conclusions",
            "source": "Conclusions/Conclusions_SubSections/Final_Conclusions.tex",
            "location": "the placeholder sentence",
            "action": "revise",
            "artifact": "",
            "caption": "",
            "citation": "",
            "text": "Leave the placeholder in place. A later closing paragraph may state only the measured moments and the kinematic coverage that were actually shown. It must separate those statements from an interpretation of the P_T width or of a model comparison. It must not claim a first multidimensional or first same-energy measurement.",
            "justification": "The section is one sentence. The world and theory sections have no validated comparison, and no campaign has been chosen as the quoted result.",
            "status": conclusion_status,
            "dependency": conclusion_dependency,
        },
        {
            "chapter": "A",
            "section": "Additional Figures",
            "source": "Appendix_Sections/Additional_Phi_h_Figures.tex",
            "location": "A:Phi_h_Unfolded_AC, A:Phi_h_Unfolded_RC, and A:Phi_h_Unfolded_BC",
            "action": "retain",
            "artifact": os.path.join(output_dir, "phi_figures"),
            "caption": "",
            "citation": "",
            "text": "Keep the families already drawn. The main text already collects all 17 Q2-y bins for the replaced acceptance and bin-centering canvases, and the appendix still has the radiative bins 2-17 plus the without-rho0 sets. Do not add a second copy of a family that the main text already shows. A sector canvas or a missing correction stage may be added only when that family is absent from the main text. The three nominal stages must use their own acceptance, RC, and BC files. One stage is not a substitute for another. No file is copied in this plan.",
            "justification": "The appendix states that the consolidated main-text figures collect every Q2-y bin for the families that were replaced. Campaign nominal canvases exist for all three stages, and the without-rho0 directory has only the acceptance canvas.",
            "status": "provisional",
            "dependency": "a later editing pass may insert a missing family; this plan does not copy figures",
        },
        {
            "chapter": "A",
            "section": "Additional Tables",
            "source": "Appendix_Sections/Appendix.tex",
            "location": "chapter Additional Tables, after the fiducial-cut table",
            "action": "add",
            "artifact": phys.normalized_bc_path(output_dir, "spline"),
            "caption": "Normalized A0, B, and C after acceptance, radiative, and bin-centering corrections. One campaign per table.",
            "citation": "",
            "text": "Do not add the numerical table yet. When it is added, use normalized_bc.json, one table for each campaign, with the provisional acceptance-level uncertainty labeled as provisional. Do not merge the campaigns and do not use the older normalized.json.",
            "justification": "The additional-tables chapter currently contains the DC fiducial vertices and no moment table. Both normalized files exist, but neither campaign is the quoted result.",
            "status": "blocked",
            "dependency": "a quoted campaign and the bin-width statement required for eq:NormalizedA",
        },
    ]
    return rows


def thesis_plan_markdown(output_dir, thesis_root):
    rows = thesis_rows(output_dir)
    lines = []
    lines.append("# SIDIS thesis integration plan")
    lines.append("")
    lines.append("This file is a specification for a later editing pass. It does not modify the thesis.")
    lines.append("")
    lines.append("The thesis source was read on 2026-11-02. No thesis file was edited, no figure was copied into the thesis, and the thesis was not compiled.")
    lines.append("")
    lines.append("Thesis root: `%s`." % thesis_root)
    lines.append("")
    lines.append("Chapter order in `main.tex` is Introduction, The Experiment, Data Processing and Event Selection, Monte Carlo, Analysis Procedure, Results and Systematic Uncertainties, and Conclusions and Outlook. Appendix A is Additional Figures. `Timeline.tex` is commented out of `main.tex`.")
    lines.append("")
    lines.append("Chapter 6 keeps its current section order: Cosine Moment Extractions, Closure Tests, then Systematic Uncertainties. Unweighted and Spline stay separate. Neither is the quoted result. Unavailable numbers stay blocked or provisional. A blocked row is not a measurement and is not entered as zero.")
    lines.append("")
    for row in rows:
        lines.append("## Chapter %s — %s" % (row["chapter"], row["section"]))
        lines.append("")
        lines.append("- Source: `%s`" % row["source"])
        lines.append("- Location: %s" % row["location"])
        lines.append("- Action: %s" % row["action"])
        lines.append("- Status: %s" % row["status"])
        lines.append("- Artifact: `%s`" % row["artifact"])
        if(row["caption"] != ""):
            lines.append("- Suggested caption or title: %s" % row["caption"])
        if(row["citation"] != ""):
            lines.append("- Citation key: `%s`" % row["citation"])
        lines.append("- Draft text: %s" % row["text"])
        lines.append("- Justification: %s" % row["justification"])
        if(str(row["dependency"]).strip() != ""):
            lines.append("- Dependency: %s" % row["dependency"])
        lines.append("")
    return "\n".join(lines)


def correct_py_command(job):
    command = [
        phys.LOCAL_PYTHON,
        phys.SKILL_CORRECT,
        "-m", str(job["mode"]),
        "-q", str(int(job["q2y"])),
        "-z", str(int(job["zpt"])),
        "-p", str(int(job["phi"])),
    ]
    if(str(job["mode"]) == "RC"):
        command.extend(["-s", str(int(job["sf"]))])
    return command


def save_fixed_point_record(path, payload):
    folder = os.path.dirname(path)
    if(folder):
        os.makedirs(folder, exist_ok=True)
    temporary = "%s.partial.%s" % (path, threading.get_ident())
    handle = open(temporary, "w")
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
    handle.close()
    os.replace(temporary, path)


def parse_fixed_point_stdout(text, returncode):
    inner = None
    stripped = str(text).strip()
    if(stripped.startswith("{")):
        try:
            inner = json.loads(stripped)
        except ValueError:
            inner = None
    if(not isinstance(inner, dict)):
        inner = {"ok": False, "error": "cross_section output was not a JSON object", "stdout_tail": stripped[-400:]}
    if(int(returncode) != 0):
        inner["ok"] = False
        inner["returncode"] = int(returncode)
    return inner


def terminate_process_group(pid, wait_s=2.0):
    # correct.py is the session leader. Its cross_section child is in the same group.
    try:
        os.killpg(int(pid), signal.SIGTERM)
    except OSError:
        return
    deadline = time.time() + float(wait_s)
    while(time.time() < deadline):
        try:
            os.killpg(int(pid), 0)
        except OSError:
            return
        time.sleep(0.05)
    try:
        os.killpg(int(pid), signal.SIGKILL)
    except OSError:
        return


def job_identity(job):
    sf_index = None if(job.get("sf") is None) else int(job["sf"])
    return {
        "mode": job["mode"],
        "q2y_bin": int(job["q2y"]),
        "zpt_bin": int(job["zpt"]),
        "phi_bin": int(job["phi"]),
        "sf_index": sf_index,
    }


def run_fixed_point_pool(jobs, cache_dir, log_dir, workers, fingerprint, command_for_job, retry_failed=False, timeout_s=120):
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    pending = []
    skipped_ok = []
    left_failed = []
    for job in jobs:
        path = os.path.join(cache_dir, phys.fixed_point_cache_name(job["mode"], job["q2y"], job["zpt"], job["phi"], job.get("sf")))
        state = phys.fixed_point_cache_state(path, fingerprint)
        if(state == "ok"):
            skipped_ok.append(path)
            continue
        if((state == "failed") and (not retry_failed)):
            left_failed.append(path)
            continue
        pending.append(job)
    live = []
    live_lock = threading.Lock()
    stop_new = threading.Event()

    def live_pids():
        with live_lock:
            return [proc.pid for proc in live if(proc.poll() is None)]

    def kill_live():
        for pid in live_pids():
            terminate_process_group(pid)

    def handle_term(signum, frame):
        stop_new.set()
        kill_live()
        raise SystemExit("rc grid interrupted")

    def execute_job(job):
        identity = job_identity(job)
        if(stop_new.is_set()):
            identity["ok"] = False
            identity["stopped"] = True
            return identity
        started = time.time()
        command = command_for_job(job)
        log_name = "q%s_z%s_p%s_s%s.log" % (identity["q2y_bin"], identity["zpt_bin"], identity["phi_bin"], identity["sf_index"])
        log_path = os.path.join(log_dir, log_name)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
        with live_lock:
            live.append(proc)
        returncode = 1
        stdout = ""
        stderr = ""
        try:
            stdout, stderr = proc.communicate(timeout=timeout_s)
            returncode = int(proc.returncode)
        except subprocess.TimeoutExpired:
            terminate_process_group(proc.pid)
            stdout, stderr = proc.communicate()
            returncode = -1
            stop_new.set()
            stderr = (stderr or "") + "\ntimeout\n"
        finally:
            with live_lock:
                if(proc in live):
                    live.remove(proc)
        inner = parse_fixed_point_stdout(stdout, returncode)
        saved = {
            "ok": inner.get("ok") is True,
            "skill_fingerprint": fingerprint,
            "seconds": time.time() - started,
            "command": command,
            "result": inner,
        }
        saved.update(identity)
        dest = os.path.join(cache_dir, phys.fixed_point_cache_name(job["mode"], job["q2y"], job["zpt"], job["phi"], job.get("sf")))
        if(os.path.isfile(dest)):
            previous = phys.fixed_point_cache_state(dest, fingerprint)
            if(previous == "ok"):
                saved["ok"] = True
                saved["preserved_ok"] = True
                return saved
        save_fixed_point_record(dest, saved)
        handle = open(log_path, "w")
        handle.write("returncode %s\n" % returncode)
        handle.write(stderr or "")
        handle.close()
        if(saved["ok"] is not True):
            stop_new.set()
        return saved

    results = []
    previous_handler = signal.getsignal(signal.SIGTERM)
    signal.signal(signal.SIGTERM, handle_term)
    pool = None
    try:
        if(len(pending) > 0):
            pool = ThreadPoolExecutor(max_workers=int(workers))
            results = list(pool.map(execute_job, pending))
    finally:
        stop_new.set()
        kill_live()
        if(pool is not None):
            pool.shutdown(wait=True, cancel_futures=True)
        signal.signal(signal.SIGTERM, previous_handler)
    failed = [row for row in results if((row.get("ok") is not True) and (not row.get("stopped")))]
    stopped = [row for row in results if(row.get("stopped"))]
    succeeded = [row for row in results if(row.get("ok") is True)]
    return {
        "workers": int(workers),
        "ran": len(results) - len(stopped),
        "succeeded": len(succeeded),
        "failed": len(failed),
        "stopped": len(stopped),
        "skipped_ok": len(skipped_ok),
        "left_failed": len(left_failed),
        "failed_paths": [phys.fixed_point_cache_name(row["mode"], row["q2y_bin"], row["zpt_bin"], row["phi_bin"], row["sf_index"]) for row in failed],
        "seconds_each": [row["seconds"] for row in results if("seconds" in row)],
    }


def grid_summary_complete(summary):
    if(summary is None):
        return False
    if(summary.get("failed", 0) > 0):
        return False
    if(summary.get("left_failed", 0) > 0):
        return False
    if(summary.get("stopped", 0) > 0):
        return False
    return True


class RcGridLock:
    def __init__(self, path, wait):
        self.path = path
        self.wait = wait
        self.handle = None

    def __enter__(self):
        folder = os.path.dirname(self.path)
        if(folder):
            os.makedirs(folder, exist_ok=True)
        self.handle = open(self.path, "a+")
        flag = fcntl.LOCK_EX
        if(not self.wait):
            flag = flag | fcntl.LOCK_NB
        try:
            fcntl.flock(self.handle.fileno(), flag)
        except BlockingIOError:
            self.handle.close()
            self.handle = None
            raise RuntimeError("rc grid lock is busy")
        return self

    def __exit__(self, exc_type, exc, tb):
        if(self.handle is not None):
            try:
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            finally:
                self.handle.close()
                self.handle = None
        return False


def run_radiative_grids(jobs_sf0, jobs_sf2, cache_dir, log_dir, sf2_workers, fingerprint, command_for_job, lock_path, wait_for_lock=True, retry_failed=False, timeout_s=120, status_path=None):
    # SF 0 finishes before SF 2 starts. The lock covers both.
    if(status_path is None):
        status_path = os.path.join(os.path.dirname(lock_path), "rc_grid_status.json")
    status = {"complete": False, "reason": "interrupted", "sf0": None, "sf2": None, "sf0_workers": 1, "sf2_workers": None}
    sf2_limit = phys.resolve_worker_count("RC", 2, sf2_workers)
    status["sf2_workers"] = sf2_limit["workers"]
    with RcGridLock(lock_path, wait_for_lock):
        try:
            summary0 = run_fixed_point_pool(jobs_sf0, cache_dir, log_dir, 1, fingerprint, command_for_job, retry_failed, timeout_s)
            status["sf0"] = summary0
            if(not grid_summary_complete(summary0)):
                status["reason"] = "sf0_incomplete"
                return status
            summary2 = run_fixed_point_pool(jobs_sf2, cache_dir, log_dir, sf2_limit["workers"], fingerprint, command_for_job, retry_failed, timeout_s)
            status["sf2"] = summary2
            if(not grid_summary_complete(summary2)):
                status["reason"] = "sf2_incomplete"
                return status
            status["complete"] = True
            status["reason"] = "complete"
            return status
        finally:
            phys.write_json(status_path, status)


def benchmark_bin_list():
    by_q = {}
    for q2y_bin, zpt_bin in phys.nominal_analysis_bins():
        by_q.setdefault(q2y_bin, []).append(zpt_bin)
    plan = [(1, 0, 1), (1, -1, 12), (5, 0, 6), (8, 0, 10), (9, 0, 15), (11, 0, 18), (14, -1, 3), (17, 0, 24)]
    picks = []
    for q2y_bin, z_index, phi_bin in plan:
        z_list = by_q[q2y_bin]
        zpt_bin = z_list[z_index]
        picks.append({"mode": "RC", "sf": 2, "q2y": q2y_bin, "zpt": zpt_bin, "phi": phi_bin})
    return picks


def vm_stat_map():
    text = subprocess.check_output(["vm_stat"], text=True)
    stats = {}
    for line in text.splitlines():
        if(":" not in line):
            continue
        key, rest = line.split(":", 1)
        token = rest.strip().strip(".").split()
        if((len(token) > 0) and token[0].isdigit()):
            stats[key.strip()] = int(token[0])
    return stats


def memory_free_percent():
    text = subprocess.check_output(["memory_pressure"], text=True)
    for line in text.splitlines():
        if("System-wide memory free percentage:" in line):
            token = line.split(":")[1].strip().rstrip("%")
            return float(token)
    return None


def cross_section_sample():
    text = subprocess.check_output(["ps", "-axo", "pid=,rss=,%cpu=,command="], text=True)
    rows = []
    rss = 0
    cpu = 0.0
    threads = 0
    for line in text.splitlines():
        if("example/cross_section" not in line):
            continue
        parts = line.split(None, 3)
        if(len(parts) < 3):
            continue
        pid = int(parts[0])
        rss += int(parts[1])
        cpu += float(parts[2])
        thread_text = subprocess.check_output(["ps", "-M", "-p", str(pid)], text=True)
        thread_count = max(len(thread_text.splitlines()) - 1, 0)
        threads = max(threads, thread_count)
        rows.append(pid)
    return {"processes": len(rows), "rss_kb": rss, "cpu_percent": cpu, "max_threads": threads}


def sample_resources():
    vm = vm_stat_map()
    processes = cross_section_sample()
    return {
        "time": time.time(),
        "swapouts": vm.get("Swapouts", 0),
        "compressor_pages": vm.get("Pages occupied by compressor", 0),
        "free_percent": memory_free_percent(),
        "processes": processes["processes"],
        "rss_kb": processes["rss_kb"],
        "cpu_percent": processes["cpu_percent"],
        "max_threads": processes["max_threads"],
    }


def recommend_sf2_workers(rows):
    ordered = sorted(rows, key=lambda row: row["workers"])
    chosen = None
    for row in ordered:
        if(row["failures"] > 0):
            break
        if(row["swapouts_delta"] > 0):
            break
        if(row["compressor_delta"] > 100000):
            break
        if(chosen is None):
            chosen = row
            continue
        if(row["per_second"] >= (chosen["per_second"] * 1.15)):
            chosen = row
            continue
        break
    if(chosen is None):
        return 1
    return int(chosen["workers"])


def run_sf2_concurrency_benchmark(cache_root, worker_counts):
    jobs = benchmark_bin_list()
    fingerprint = phys.skill_input_fingerprint()
    rows = []
    for count in worker_counts:
        folder = os.path.join(cache_root, "workers_%s" % int(count))
        samples = []
        stop = threading.Event()

        def loop(box=samples, flag=stop):
            while(not flag.is_set()):
                try:
                    box.append(sample_resources())
                except (OSError, subprocess.CalledProcessError, ValueError):
                    box.append({"time": time.time(), "sample_error": True})
                flag.wait(0.4)

        thread = threading.Thread(target=loop)
        thread.start()
        started = time.time()
        summary = run_fixed_point_pool(
            jobs,
            os.path.join(folder, "cache"),
            os.path.join(folder, "logs"),
            count,
            fingerprint,
            correct_py_command,
            retry_failed=False,
            timeout_s=120,
        )
        elapsed = time.time() - started
        stop.set()
        thread.join()
        good_samples = [row for row in samples if(row.get("sample_error") is not True)]
        swap_start = good_samples[0]["swapouts"] if(len(good_samples) > 0) else 0
        swap_end = good_samples[-1]["swapouts"] if(len(good_samples) > 0) else 0
        compressor_start = good_samples[0]["compressor_pages"] if(len(good_samples) > 0) else 0
        compressor_peak = compressor_start
        rss_peak = 0
        cpu_peak = 0.0
        threads_peak = 0
        free_min = None
        gap_peak = 0.0
        previous = None
        for row in good_samples:
            compressor_peak = max(compressor_peak, row.get("compressor_pages", 0))
            rss_peak = max(rss_peak, row.get("rss_kb", 0))
            cpu_peak = max(cpu_peak, row.get("cpu_percent", 0.0))
            threads_peak = max(threads_peak, row.get("max_threads", 0))
            free_value = row.get("free_percent")
            if(free_value is not None):
                free_min = free_value if(free_min is None) else min(free_min, free_value)
            if(previous is not None):
                gap_peak = max(gap_peak, row["time"] - previous)
            previous = row["time"]
        per_second = 0.0 if(elapsed <= 0) else (float(summary["succeeded"]) / elapsed)
        mean_seconds = None
        if(len(summary["seconds_each"]) > 0):
            mean_seconds = sum(summary["seconds_each"]) / float(len(summary["seconds_each"]))
        rows.append({
            "workers": int(count),
            "bins": len(jobs),
            "elapsed_s": elapsed,
            "per_second": per_second,
            "mean_job_s": mean_seconds,
            "succeeded": summary["succeeded"],
            "failures": summary["failed"],
            "swapouts_delta": int(swap_end) - int(swap_start),
            "compressor_delta": int(compressor_peak) - int(compressor_start),
            "rss_peak_kb": rss_peak,
            "cpu_peak_percent": cpu_peak,
            "max_threads": threads_peak,
            "free_percent_min": free_min,
            "sample_gap_s": gap_peak,
            "jobs": [{"q2y": job["q2y"], "zpt": job["zpt"], "phi": job["phi"]} for job in jobs],
        })
    return {"rows": rows, "recommended_workers": recommend_sf2_workers(rows), "jobs": jobs}


def write_stage_report(path, text):
    folder = os.path.dirname(path)
    if(folder):
        os.makedirs(folder, exist_ok=True)
    handle = open(path, "w")
    handle.write(text)
    if(not text.endswith("\n")):
        handle.write("\n")
    handle.close()
    return path
