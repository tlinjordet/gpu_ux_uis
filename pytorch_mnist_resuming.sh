#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --time=02:15:00
#SBATCH --job-name=pytorch_mnist_resuming
#SBATCH --output=mnist_test_resuming-$SLURM_JOBID.out
 
# Activate environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv miniconda-python39
conda activate pytorch_env

# Prepare to run this sbatch script recursively if and only if it fails, e.g.,
# by time-out. 
sbatch --dependency=afternotok:$SLURM_JOBID pytorch_mnist_resuming.sh
# Run the Python script that uses the GPU 
# and which checks if the target number 
# of epochs has been reached.
python -u pytorch_mnist_resuming.py --epochs 5 --save-model True

# If the model training was interrupted, pytorch_mnist_resuming.py will launch 
# `sbatch pytorch_mnist_resuming.sh` again, if else not.