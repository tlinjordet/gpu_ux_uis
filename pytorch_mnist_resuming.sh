#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --time=01:00:00
#SBATCH --job-name=pytorch_mnist_resuming
#SBATCH --output=mnist_test_resuming.out


# Activate environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv miniconda-python39
conda activate pytorch_env

# Run the Python script that uses the GPU 
# and which checks if the target number 
# of epochs has been reached.
python -u pytorch_mnist_resuming.py --epochs 500 --save-model --slurm_job_id=$SLURM_JOBID

# If the model training was interrupted, pytorch_mnist_resuming.py will launch 
# `sbatch pytorch_mnist_resuming.sh` again, if else not.
