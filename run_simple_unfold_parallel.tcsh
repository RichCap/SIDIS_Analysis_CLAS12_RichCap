#!/bin/tcsh -f

# run_simple_unfold_parallel.tcsh
# Launches 17 parallel instances of Simple_RooUnfold_SelfContained.py
# with per-job output and timing/memory stats

# Help option
if ( $#argv >= 1 ) then
    if ( $#argv > 0 && ( "$argv[1]" == "-h" || "$argv[1]" == "--help" ) ) then
        echo "Usage: ./run_simple_unfold_parallel.tcsh [-h|--help]"
        echo ""
        echo "Purpose:"
        echo "  This script launches multiple parallel jobs of the Simple_RooUnfold_SelfContained.py script,"
        echo "  each processing a different Q2-y bin (1 to 17 by default). It handles safe parallel execution"
        echo "  with file locking (assumed in the Python script), captures per-job logs, and measures runtime"
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
        echo "  3. Outputs go to log_dir: Unfold_Log_of_Q2_y_Bin_#.out and Unfold_Time_of_Q2_y_Bin_#.time"
        echo "  4. For help: ./run_simple_unfold_parallel.tcsh -h"
        echo ""
        echo "Customization:"
        echo "  - Change 'args' for different Python flags."
        echo "  - Set max_concurrent > 0 to queue jobs (e.g., 8 for 8 at a time)."
        exit 0
    endif
endif

set script     = "./Simple_RooUnfold_SelfContained.py"
set njobs      = 17
set log_dir    = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Logs_for_Simple_Unfolding"
# set log_prefix = "Unfold_Log_of_Q2_y_Bin_"
# set time_prefix = "Unfold_Time_of_Q2_y_Bin_"
set log_prefix = "ZerothOrderAcc_Unfold_Log_of_Q2_y_Bin_"
set time_prefix = "ZerothOrderAcc_Unfold_Time_of_Q2_y_Bin_"

# Arguments for the Python script (easily changeable here)
# set args       = "-bi 1 -nt 1 -smear -u3D -e -em \"Test of parallel running\""
# set args       = '-r "FULL_Unfolded_Histos_From_Simple_RooUnfold_SelfContained.root" -smear -u3D -e -em "Running default Unfolding as background parallel jobs. Ran in tmuxUnfold (in case there were any local issues)"'
set args  = '-r ZerothOrderAcc_Unfolded_Histos_From_Simple_RooUnfold_SelfContained.root -smear -u3D -e -sfin /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_ZerothOrderAcc_All_Batches.root -mod -wa'
set emsg  = 'Running Unfolding with 0th Order Acceptance Weights as background parallel jobs. Ran in tmuxTTree.'
set title = 'Applied the 0th Order Acceptance Weights'

# Optional: limit concurrent jobs if machine is overloaded (set to 0 = unlimited)
set max_concurrent = 0   # 0 = run all 17 at once; e.g. 8 = limit to 8 running at a time

# Ensure log directory exists
mkdir -p $log_dir

echo "===================================================================="
echo " Starting parallel RooUnfold test run"
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
    echo "Full command: $script $args -em '$emsg' -ti '$title' $i" >! $outfile

    /usr/bin/time -v -o $timefile $script $args -em "$emsg" -ti "$title" $i >>& $outfile &
    # set cmd = "/usr/bin/time -v -o $timefile $script $args -em \"$emsg\" -ti \"$title\" $i >>& $outfile &"
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

exit 0
