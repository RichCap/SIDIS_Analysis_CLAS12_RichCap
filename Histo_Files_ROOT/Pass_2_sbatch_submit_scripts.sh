#!/bin/bash

DIR_WITH_SCRIPTS="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT"
skip_rdf=false
skip_mdf=false
skip_gdf=false
use_cat=false
use_git=false
use_lt=false
script_type="SIDIS"  # Default script type

# Function to display help message
function display_help {
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  --skip-rdf       Skip submitting jobs for rdf files."
    echo "  --skip-mdf       Skip submitting jobs for mdf files."
    echo "  --skip-gdf       Skip submitting jobs for gdf files."
    echo "  --only-rdf       Only submitting jobs for rdf files."
    echo "  --only-mdf       Only submitting jobs for mdf files."
    echo "  --only-gdf       Only submitting jobs for gdf files."
    echo "  --cat            Display the contents of the scripts instead of submitting them with sbatch."
    echo "  --git            Display the 'git' status of the scripts instead of submitting them with sbatch. (Same as using 'git diff' on the file)"
    echo "  --lt             Shows the file location as if using the 'lt' command (basically my version of 'ls -lhtr')"
    echo "  --type <type>    Specify the script type: 'sidis', 'proton', or 'mom'. Default is 'sidis'."
    echo "  --help, -h       Display this help message and exit."
    echo
    echo "If no options are provided, the script will submit jobs for rdf, mdf, and gdf files using sbatch."
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --skip-rdf) skip_rdf=true ;;
        --skip-mdf) skip_mdf=true ;;
        --skip-gdf) skip_gdf=true ;;
        --only-rdf) skip_mdf=true ; skip_gdf=true ;;
        --only-mdf) skip_rdf=true ; skip_gdf=true ;;
        --only-gdf) skip_rdf=true ; skip_mdf=true ;;
        --cat) use_cat=true ;;
        --git) use_git=true ;;
        --lt) use_lt=true ;;
        --type)
            if [[ -n $2 ]]; then
                case $2 in
                    sidis) script_type="SIDIS" ;;
                    proton) script_type="Tagged_Proton_SIDIS" ;;
                    mom) script_type="Mom" ;;
                    *) echo "Unknown script type: $2"; exit 1 ;;
                esac
                shift
            else
                echo "No script type specified"; exit 1
            fi
            ;;
        --help) display_help; exit 0 ;;
        -h)     display_help; exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

if [ "$use_cat" = false ] && [ "$use_git" = false ] && [ "$use_lt" = false ]; then
    echo "Submitting jobs for running makeROOT_epip_${script_type}_histos_new.py"
    echo ""
    echo "Currently Running Jobs:"
    squeue -u richcap
    echo "Total:"
    squeue -u richcap | wc -l
    echo ""
else
    echo ""
    echo ""
    echo ""
    echo ""
fi

# Submit or cat for mdf files
if [ "$skip_mdf" = false ]; then
    if [ "$use_lt" = false ]; then
        cd "${DIR_WITH_SCRIPTS}/Matching_REC_MC/"
    else
        echo ""
    fi
    script_path="${DIR_WITH_SCRIPTS}/Matching_REC_MC/sbatch_${script_type}_python_matching_MC_Pass2.sh"
    if [ "$use_cat" = true ]; then
        echo "Checking for mdf file in:"
        pwd
        cat "$script_path"
        echo ""
        echo ""
    else
        if [ "$use_git" = true ]; then
            echo "Checking for mdf file in:"
            pwd
            git diff "$script_path"
            echo ""
            echo ""
        else
            if [ "$use_lt" = true ]; then
                ls -lhtr "$script_path"
            else
                echo "Submitting for mdf file in:"
                pwd
                # echo "Would sbatch $script_path"
                sbatch "$script_path"
            fi
        fi
    fi
else
    echo ""
    echo "Skipping mdf files..."
    echo ""
fi

# Submit or cat for gdf files
if [ "$skip_gdf" = false ]; then
    if [ "$use_lt" = false ]; then
        cd "${DIR_WITH_SCRIPTS}/GEN_MC/"
    else
        echo ""
    fi
    script_path="${DIR_WITH_SCRIPTS}/GEN_MC/sbatch_${script_type}_python_gen_MC_Pass2.sh"
    if [ "$use_cat" = true ]; then
        echo "Checking for gdf file in:"
        pwd
        cat "$script_path"
        echo ""
        echo ""
    else
        if [ "$use_git" = true ]; then
            echo "Checking for gdf file in:"
            pwd
            git diff "$script_path"
            echo ""
            echo ""
        else
            if [ "$use_lt" = true ];then
                ls -lhtr "$script_path"
            else
                echo "Submitting for gdf file in:"
                pwd
                # echo "Would sbatch $script_path"
                sbatch "$script_path"
            fi
        fi
    fi
else
    echo ""
    echo "Skipping gdf files..."
    echo ""
fi

# Submit or cat for rdf files
if [ "$skip_rdf" = false ]; then
    if [ "$use_lt" = false ]; then
        cd "${DIR_WITH_SCRIPTS}/REAL_Data/"
    else
        echo ""
    fi
    script_path="${DIR_WITH_SCRIPTS}/REAL_Data/sbatch_${script_type}_python_real_data_Pass2.sh"
    if [ "$use_cat" = true ]; then
        echo "Checking for rdf file in:"
        pwd
        cat "$script_path"
        echo ""
        echo ""
    else
        if [ "$use_git" = true ]; then
            echo "Checking for rdf file in:"
            pwd
            git diff "$script_path"
            echo ""
            echo ""
        else
            if [ "$use_lt" = true ]; then
                ls -lhtr "$script_path"
            else
                echo "Submitting for rdf file in:"
                pwd
                # echo "Would sbatch $script_path"
                sbatch "$script_path"
            fi
        fi
    fi
else
    echo ""
    echo "Skipping rdf files..."
    echo ""
fi

echo ""
if [ "$use_cat" = false ] && [ "$use_git" = false ] && [ "$use_lt" = false ]; then
    echo "Done submitting all jobs"
    echo "Currently Running Jobs:"
    squeue -u richcap
    echo "Total:"
    squeue -u richcap | wc -l
fi

echo ""
echo ""
echo ""
echo "Done"
echo ""
