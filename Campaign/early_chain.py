# Commands for the first iFarm chain. One line each. No conda.
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.backends import local_command
from Campaign.dispatch import refill
from Campaign.ifarm_inputs import load_ifarm_inputs, rho_source_token
from Campaign.swif_retry import attempt_record, classify_failure, next_resources

def checkout_script(path):
    rel = os.path.relpath(path, _BOOT).replace("\\", "/")
    return "./" + rel


def repo_python():
    # Kept so older call sites still import. Generated commands use checkout_script.
    import sys
    return sys.executable


def evgen_dir():
    farm = "/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap"
    local = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/Running_EvGen_richcap"
    if(os.path.isdir(farm)):
        return farm
    return local


def write_glob_list(folder, name, glob_text):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    handle = open(path, "w")
    handle.write(str(glob_text).strip())
    handle.write("\n")
    handle.close()
    return path


def groovy_command(source, mc_type, paths_txt, data_root="work_b"):
    # Groovy has no --data_root. Analysis-tree commands below pass -droot work_b.
    # This list form is the selection summary. A real launch uses groovy_file_command, one SWIF2 job per HIPO file.
    script = checkout_script(os.path.join(_BOOT, "Data_Files_Groovy", "run_groovy_scripts_with_emails.py"))
    return local_command("%s -m slurm -src %s -mc %s -ptxt %s -na" % (script, source, mc_type, paths_txt))


def groovy_file_command(source, mc_type, hipo_path, data_root="work_b"):
    # One file, in-process, so the SWIF2 job is the process that can hit the memory or wall limit.
    import shlex
    script = checkout_script(os.path.join(_BOOT, "Data_Files_Groovy", "run_groovy_scripts_with_emails.py"))
    return local_command("%s -m sequential -src %s -mc %s -f %s -na" % (script, source, mc_type, shlex.quote(hipo_path)))


def dataframe_command(pattern, data_type, data_root="work_b"):
    # Groovy has no data-root flag. Its ROOT files stay in these historical directories. -droot selects where the DataFrame is written.
    import shlex
    script = checkout_script(os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "run_dataframe_makeROOT_helper.py"))
    if(data_type == "gdf"):
        folder = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2"
    else:
        folder = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info"
    target = os.path.join(folder, pattern)
    return local_command("%s -droot %s -i %s -dtype %s -m slurm -y" % (script, data_root, shlex.quote(target), data_type))


def batch_command(data_root="work_b"):
    script = checkout_script(os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "run_sidis_DataFrame_pipeline.py"))
    token = rho_source_token() or "rho0_new"
    return local_command("%s -droot %s -m make_batches -rst %s" % (script, data_root, token))


def rho_norm_commands(data_root="work_b"):
    submit = checkout_script(os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "Submit_Full_Histogram_Creation_Pipeline.py"))
    fit = checkout_script(os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "Get_rho_Normalization_values.py"))
    token = rho_source_token() or "rho0_new"
    histograms = local_command("%s -droot %s -m slurm -y -rho -jrho0 4 -nrrw" % (submit, data_root))
    extract = local_command("%s -droot %s -st %s" % (fit, data_root, token))
    return [histograms, extract]


def response_commands(data_root="work_b"):
    submit = checkout_script(os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "Submit_Full_Histogram_Creation_Pipeline.py"))
    five = "%s -droot %s -m slurm -y -j5D 4 -j3D 0 -j2D 0 -jBin 0 -jch4 0 -jrho0 0 -jdph 0" % (submit, data_root)
    three = "%s -droot %s -m slurm -y -j5D 0 -j3D 4 -j2D 0 -jBin 0 -jch4 0 -jrho0 0 -jdph 0" % (submit, data_root)
    two = "%s -droot %s -m slurm -y -j5D 0 -j3D 0 -j2D 4 -jBin 0 -jch4 0 -jrho0 0 -jdph 0" % (submit, data_root)
    dphi = "%s -droot %s -m slurm -y -nrrw -jdph 4 -j5D 0 -j3D 0 -j2D 0 -jBin 0 -jch4 0 -jrho0 0" % (submit, data_root)
    return {
        "response_5d": local_command(five),
        "response_3d": local_command(three),
        "response_1d": "",
        "response_2d": local_command(two),
        "diagnostic_dphi": local_command(dphi),
    }


def later_commands(rc_mode, data_root="work_b"):
    five = checkout_script(os.path.join(_BOOT, "run_Dedicated_5D_Unfold.py"))
    hybrid = os.path.join(evgen_dir(), "Run_Large_Files_For_Iterative_Corrections", "Comparison_With_Unfolding", "create_Hybrid_SIDIS_Single_File.py")
    bc = checkout_script(os.path.join(_BOOT, "BC_Corrections", "BC_Corrections_Script.py"))
    # sbatch = os.path.join(evgen_dir(), "sbatch_Gen_submission_creation_script.py")
    commands = {
        "iteration_5d": local_command("%s -droot %s --iteration_study --parm_min 1 --parm_max 10 --parm_step 1 --Min_Allowed_Acceptance_Cut 0.020 --background_source lundvpk" % (five, data_root)),
        "hybrid_attach": local_command("%s -ui UNFOLDED.root -ei RC_FACTORS.root -o HYBRID.root" % hybrid),
        "bc": local_command("%s -nb 3 -nbphi 2" % bc),
    }
    # if(rc_mode == "regenerate"):
    #     commands["rc_regenerate"] = local_command("%s --submit_both_rc_modes" % sbatch)
    # else:
    #     commands["rc_regenerate"] = ""
    return commands


def rc_histogram_commands(rc_mode):
    # Recompute RC-factor histograms from existing Rad/No_Rad ROOT files. Do not generate events.
    if(rc_mode != "regenerate"):
        return []
    compare_dir = os.path.join(evgen_dir(), "Run_Large_Files_For_Iterative_Corrections", "Comparison_With_Unfolding")
    runtime = os.path.join(compare_dir, "build_EvGen_PerFile_Hists_Runtime_ifarm_rc")
    merged = os.path.join(runtime, "merged_outputs", "Merged_EvGen_PerFile_Hists.root")
    rc_out = os.path.join(runtime, "merged_outputs", "RC_Factors_ifarm_rc.root")
    build = os.path.join(compare_dir, "Build_EvGen_PerFile_Hists.py")
    compare = os.path.join(compare_dir, "Comparison_Between_GEN_and_Unfold.py")
    return [
        local_command("%s -m slurm -y -p -rdir %s" % (build, runtime)),
        local_command("%s -r %s -ssf -sfn %s -rc -Nw -evgen" % (compare, merged, rc_out)),
    ]


def early_chain_commands(command_dir, data_root="work_b"):
    from Campaign.preflight_new_inputs import run_preflight
    config = load_ifarm_inputs()
    token = rho_source_token(config)
    if(token != "rho0_new"):
        return {"status": "blocked", "reason": "rho_source_token must be rho0_new", "commands": []}
    code = run_preflight(command_dir, data_root)
    if(code != 0):
        return {"status": "blocked", "reason": "preflight failed; no Groovy jobs were written", "commands": []}
    rho_list = os.path.join(command_dir, "new_rho0_hipo.txt")
    na_list = os.path.join(command_dir, "new_55na_hipo.txt")
    disc = config["rho_name_discriminator"]
    commands = []
    for path in open(rho_list):
        hipo = path.strip()
        if(not hipo):
            continue
        commands.append(groovy_file_command("rho0", "gdf", hipo, data_root))
        commands.append(groovy_file_command("rho0", "mdf", hipo, data_root))
    for path in open(na_list):
        hipo = path.strip()
        if(not hipo):
            continue
        commands.append(groovy_file_command("clasdis", "gdf", hipo, data_root))
        commands.append(groovy_file_command("clasdis", "mdf", hipo, data_root))
    commands.extend([
        dataframe_command("*%s*" % disc, "gdf", data_root),
        dataframe_command("*%s*" % disc, "mdf", data_root),
        dataframe_command("*inb-clasdis-55na*", "gdf", data_root),
        dataframe_command("*inb-clasdis-55na*", "mdf", data_root),
        batch_command(data_root),
    ])
    commands.extend(rho_norm_commands(data_root))
    return {"status": "checkpoint", "reason": "confirm the rho0_new factor, then resume response production", "commands": commands}


def plan_retry(status_text, command, ram_gb, hours, retry_number):
    kind = classify_failure(status_text)
    revised = next_resources(kind, ram_gb, hours, retry_number)
    return attempt_record(command, kind, ram_gb, hours, revised, retry_number)


def self_test():
    from Campaign.ifarm_inputs import classify_rho_name
    groovy_name = "MC_Gen_sidis_epip_richcap.inb.qa.rho0.new10.output-rho0_10.6gev-example.hipo.root"
    old_rho = "MC_Gen_sidis_epip_richcap.inb.qa.rho0.new10.lundrho-example.hipo.root"
    old_vpk = "MC_Matching_sidis_epip_richcap.inb.qa.rho0.new10.lundvpk-example.hipo.root"
    clasdis = "MC_Gen_sidis_epip_richcap.inb.qa.new10.inb-clasdis-55na-Q2_1.5-example.hipo.root"
    if(classify_rho_name(groovy_name) != "rho0_new"):
        raise SystemExit("new rho classified as %s" % classify_rho_name(groovy_name))
    if(classify_rho_name(old_rho) != "lundrho"):
        raise SystemExit("lundrho moved")
    if(classify_rho_name(old_vpk) != "lundvpk"):
        raise SystemExit("lundvpk moved")
    if(classify_rho_name(clasdis) != ""):
        raise SystemExit("55 nA clasdis was treated as rho")
    if("rho0_new_unconfigured" in classify_rho_name(groovy_name)):
        raise SystemExit("unconfigured suffix is not a token")
    dphi = response_commands()["diagnostic_dphi"]
    if((not dphi.startswith("./")) or ("-droot work_b" not in dphi) or ("-jdph" not in dphi) or ("-nrrw" not in dphi)):
        raise SystemExit("diagnostic command %s" % dphi)
    chosen = refill(
        [{"stage": "response_2d", "name": "b"}, {"stage": "response_5d", "name": "a"}],
        1,
    )
    if(chosen[0]["stage"] != "response_5d"):
        raise SystemExit("5D did not win the free slot")
    both = refill(
        [{"stage": "response_1d", "name": "c"}, {"stage": "response_3d", "name": "d"}, {"stage": "response_5d", "name": "e"}],
        2,
    )
    if([job["stage"] for job in both] != ["response_5d", "response_3d"]):
        raise SystemExit("refill order %s" % both)
    oom = plan_retry("CANCELLED OOM killed", "cmd", 4, 8, 0)
    if((not oom["retry"]) or (oom["revised_ram_gb"] != 5) or (oom["revised_hours"] != 8)):
        raise SystemExit("oom retry %s" % oom)
    wall = plan_retry("DUE TO TIME LIMIT", "cmd", 4, 8, 0)
    if(wall["revised_hours"] != 9):
        raise SystemExit("wall retry")
    node = plan_retry("node_fail", "cmd", 4, 8, 0)
    if((node["revised_ram_gb"] != 4) or (node["revised_hours"] != 8)):
        raise SystemExit("transient retry")
    app = plan_retry("Error: missing histogram key", "cmd", 4, 8, 0)
    if(app["retry"]):
        raise SystemExit("application failure was retried")
    capped = plan_retry("OOM", "cmd", 4, 8, 2)
    if(capped["retry"]):
        raise SystemExit("retry past the ceiling")
    print("early_chain self_test ok")


if(__name__ == "__main__"):
    self_test()
