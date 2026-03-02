#!/bin/tcsh -f

# run_simple_unfold_parallel.tcsh
# Launches 515 parallel instances of Make_RC_Factor_Plots.py
# with per-job output and timing/memory stats

# Help option
if ( $#argv >= 1 ) then
    if ( $#argv > 0 && ( "$argv[1]" == "-h" || "$argv[1]" == "--help" ) ) then
        echo "Usage: ./run_rc_factor_plots_parallel.tcsh [-h|--help]"
        echo ""
        echo "Purpose:"
        echo "  This script launches multiple parallel jobs of the Make_RC_Factor_Plots.py script,"
        echo "  each processing a different Q2-y-z-pT bins (using the 4D bin converter which goes from 1 to 515 by default)."
        echo "  It handles safe parallel execution with file locking, captures per-job logs, and measures runtime"
        echo "  and peak memory usage using /usr/bin/time."
        echo ""
        echo "What it does:"
        echo "  - Launches jobs in background for parallelism."
        echo "  - Redirects stdout/stderr to per-bin log files."
        echo "  - Records timing/memory stats in separate .time files."
        echo "  - Optionally limits concurrent jobs to avoid overload."
        echo "  - Waits for all jobs to complete and prints a summary of runtimes/peak memory."
        echo ""
        echo "How to use:"
        echo "  1. Edit variables at the top: script path, njobs, args (flags for Python script),"
        echo "     log_dir, max_concurrent (0 = no limit)."
        echo "  2. Run: ./run_simple_unfold_parallel.tcsh"
        echo "  3. Outputs go to log_dir: RC_Log_of_Q2_y_z_pT_Bin_#.out and RC_Time_of_Q2_y_z_pT_Bin_#.time"
        echo "  4. For help: ./run_rc_factor_plots_parallel.tcsh -h"
        echo ""
        echo "Customization:"
        echo "  - Change 'args' for different Python flags."
        echo "  - Set max_concurrent > 0 to queue jobs (e.g., 20 for 20 at a time is the default)."
        exit 0
    endif
endif

set script     = "./Make_RC_Factor_Plots.py"
set njobs      = 515
set log_dir    = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RC_Correction_Code/Logs_for_RC_Plots"
set log_prefix = "Prokudin_RC_Log_of_Q2_y_z_pT_Bin_"
set time_prefix = "Prokudin_RC_Time_of_Q2_y_z_pT_Bin_"

# Arguments for the Python script (easily changeable here)
set args  = '-si -f -uj -n Prokudin'
set emsg  = 'Ran using the default EvGen Cross Sections. Was running as background parallel jobs in tmuxTTree.'
set title = 'Used the default EvGen Cross Sections'

# Optional: limit concurrent jobs if machine is overloaded (set to 0 = unlimited)
set max_concurrent = 20  # e.g. 20 = limit to 20 running at a time or 0 for all runs at once

# Ensure log directory exists
mkdir -p $log_dir

echo "===================================================================="
echo " Starting parallel RC Plot run"
echo "   Jobs       : 1 to $njobs"
echo "   Command    : $script $args <bin>"
echo "   Start time : `date`"
echo "===================================================================="


set joblist = ""
set running = 0

foreach i (`seq 1 $njobs`)
    set outfile = $log_dir/${log_prefix}${i}.out
    set timefile = $log_dir/${time_prefix}${i}.time

    echo "Launching job $i → $outfile + $timefile"

    # Prepend the full command to the log file
    echo "Full command: $script $args -em '$emsg' -t '$title' -4d $i" >! $outfile

    /usr/bin/time -v -o $timefile $script $args -em "$emsg" -t "$title" -4d $i >>& $outfile &
    # set cmd = "/usr/bin/time -v -o $timefile $script $args -em \"$emsg\" -t \"$title\" -4d $i >>& $outfile &"
    # eval $cmd

    set pid = $!
    set joblist = "$joblist $pid"

    @ running++
    if ( $max_concurrent > 0 && $running >= $max_concurrent ) then
        wait     # wait for any job to finish before launching more
        @ running = 0
    endif
end

echo ""
echo "All $njobs jobs launched. Waiting for completion..."
echo ""
echo "Start time  : `date`"
echo ""

wait

echo ""
echo "===================================================================="
echo " All jobs finished"
echo " End time   : `date`"
echo ""
echo " Log files:   $log_dir/${log_prefix}*.out"
echo " Time stats:  $log_dir/${time_prefix}*.time  (includes runtime + peak RSS memory)"
echo ""
echo " Quick summary of runtimes and peak memory:"
echo "------------------------------------------"
grep -H "Elapsed\|Maximum resident" $log_dir/${time_prefix}*.time | grep -v Average | sort -t: -k2
echo "===================================================================="

echo "$emsg See the log files in $log_dir/${log_prefix}* for details." | mail -s "Finished running all parallel Make_RC_Factor_Plots.py tasks" "richard.capobianco@uconn.edu"

exit 0
