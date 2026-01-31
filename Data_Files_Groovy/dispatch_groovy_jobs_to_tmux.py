#!/usr/bin/env python3

import argparse
import subprocess
import sys


def tmux_has_session(session_name):
    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return (result.returncode == 0)


def tmux_send(session_name, command_str):
    # Send the command then press Enter.
    result = subprocess.run(
        ["tmux", "send-keys", "-t", session_name, command_str, "C-m"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )
    if(result.returncode != 0):
        raise RuntimeError(f"tmux send-keys failed for session '{session_name}': {result.stderr.strip()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "-test", "-dr", "--dry-run", action="store_true", help="Print what would be sent, but do not send anything.")
    args = parser.parse_args()

    # Your alias -> real tmux session mapping:
    # tmuxSIDIS   -> hadd_sidis
    # tmuxSIDIS_1 -> hadd_sidis1
    # tmuxSIDIS_2 -> hadd_sidis2
    # tmuxSIDIS_3 -> hadd_sidis3
    # tmuxEIC     -> EIC_Environment
    # tmuxEvGen   -> EvGen
    # tmuxLUND    -> run_EvGen_lund
    # tmuxOSGL    -> Local_OSG_run
    # tmuxPython  -> Run_python
    # tmuxRADGEN  -> RADGEN
    # tmuxTTree   -> hadd_TTree

    jobs = [

# ================================================================================================================================================
# "0.1":
        { 
            "alias":   "tmuxSIDIS",
            "session": "hadd_sidis",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "data" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_REAL_Data_files_SIDIS.txt' -ub '0-24' -saj 64692480 -e -em "Ran with the Command: '-src 'data' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_REAL_Data_files_SIDIS.txt' -ub '0-24' -saj 64692480'. Ran in tmuxSIDIS." ; Done_at"""
        },

# ================================================================================================================================================
# "0.2":
        { 
            "alias":   "tmuxSIDIS_3",
            "session": "hadd_sidis3",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "data" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_REAL_Data_files_SIDIS.txt' -ub '25-48' -saj 64692480 -e -em "Ran with the Command: '-src 'data' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_REAL_Data_files_SIDIS.txt' -ub '25-48' -saj 64692480'. Ran in tmuxSIDIS_3." ; Done_at"""
        },

# ================================================================================================================================================
# "1.1":
        { 
            "alias":   "tmuxSIDIS_1",
            "session": "hadd_sidis1",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '0-48' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '0-48' -saj 64692481'. Ran in tmuxSIDIS_1." ; Done_at"""
        },

# ================================================================================================================================================
# "1.2":
        { 
            "alias":   "tmuxEIC",
            "session": "EIC_Environment",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '49-97' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '49-97' -saj 64692481'. Ran in tmuxEIC." ; Done_at"""
        },

# ================================================================================================================================================
# "1.3":
        { 
            "alias":   "tmuxEvGen",
            "session": "EvGen",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '98-146' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '98-146' -saj 64692481'. Ran in tmuxEvGen." ; Done_at"""
        },

# ================================================================================================================================================
# "1.4":
        { 
            "alias":   "tmuxLUND",
            "session": "run_EvGen_lund",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '147-195' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '147-195' -saj 64692481'. Ran in tmuxLUND." ; Done_at"""
        },

# ================================================================================================================================================
# "1.5":
        { 
            "alias":   "tmuxOSGL",
            "session": "Local_OSG_run",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '196-244' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '196-244' -saj 64692481'. Ran in tmuxOSGL." ; Done_at"""
        },

# ================================================================================================================================================
# "1.6":
        { 
            "alias":   "tmuxPython",
            "session": "Run_python",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '245-293' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '245-293' -saj 64692481'. Ran in tmuxPython." ; Done_at"""
        },

# ================================================================================================================================================
# "1.7":
        { 
            "alias":   "tmuxRADGEN",
            "session": "RADGEN",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '294-341' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '294-341' -saj 64692481'. Ran in tmuxRADGEN." ; Done_at"""
        },

# ================================================================================================================================================
# "1.8":
        { 
            "alias":   "tmuxTTree",
            "session": "hadd_TTree",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '342-389' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '342-389' -saj 64692481'. Ran in tmuxTTree." ; Done_at"""
        },

# ================================================================================================================================================
# "1.9":
        { 
            "alias":   "tmuxUnfold",
            "session": "Unfolding",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '390-437' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '390-437' -saj 64692481'. Ran in tmuxUnfold." ; Done_at"""
        },

# ================================================================================================================================================
# "1.10":
        { 
            "alias":   "tmuxMerge",
            "session": "merge_hipo",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "clasdis" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '438-485' -saj 64692481 -e -em "Ran with the Command: '-src 'clasdis' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_clasdis_files_SIDIS.txt' -ub '438-485' -saj 64692481'. Ran in tmuxMerge." ; Done_at"""
        },

# ================================================================================================================================================
# "2":
        { 
            "alias":   "tmuxSIDIS_2",
            "session": "hadd_sidis2",
            "command":  """cd_Groovy; ./run_groovy_scripts_with_emails.py -src "evgen" -mc "rec" -evt "epipX" -ptxt 'TEMP_Paths_to_MC_EvGen_files_SIDIS.txt' -saj 64692482 -e -em "Ran with the Command: '-src 'evgen' -mc 'rec' -evt 'epipX' -ptxt 'TEMP_Paths_to_MC_EvGen_files_SIDIS.txt' -saj 64692482'. Ran in tmuxSIDIS_2." ; Done_at"""
        }
    ]

    for job in jobs:
        alias   = job["alias"]
        session = job["session"]
        cmd     = job["command"].strip()

        if(not tmux_has_session(session)):
            print(f"WARNING: tmux session '{session}' not found for {alias}. Skipping.")
            continue

        if(args.dry_run):
            print(f"[DRY RUN] {alias} -> {session}\n{cmd}\n")
            continue

        # Optional: banner to make it obvious in the tmux scrollback when the dispatch happened
        tmux_send(session, f"echo '--- Dispatch for {alias} at: ' `date`")

        tmux_send(session, cmd)
        print(f"Dispatched: {alias} -> {session}")

    print("All dispatch attempts completed.")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
