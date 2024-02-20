#!/bin/bash
#$ -l mem=10G,time=12:: -S /bin/bash -N epiestim -t 1-958
#$ -e /ifs/scratch/jls106_gp/nhw2114/data/20240212_run
#$ -o /ifs/scratch/jls106_gp/nhw2114/data/20240212_run
module load singularity
PASSWORD='ihme123' singularity exec --bind "$HOME"/run:/run,"$HOME"/var-lib-rstudio-server:/var/lib/rstudio-server,"$HOME"/database.conf:/etc/rstudio/database.conf,/ifs/scratch/jls106_gp/nhw2114:/ifs/scratch/jls106_gp/nhw2114 \
    "$HOME"/rstudio.simg Rscript --no-save --vanilla /ifs/scratch/jls106_gp/nhw2114/repos/rt-estimation/src/epyfilter/c2b2/epiestim_parallel.R \
    --in-dir /ifs/scratch/jls106_gp/nhw2114/repos/rt-estimation/src/epyfilter/c2b2/ \
    --data-dir /ifs/scratch/jls106_gp/nhw2114/data/20231106_synthetic_data/ \
    --out-dir /ifs/scratch/jls106_gp/nhw2114/data/20240212_run/ \
    --files-per-task 50