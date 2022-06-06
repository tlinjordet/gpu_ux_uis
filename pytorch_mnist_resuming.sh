#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --array=1-170%1
#SBATCH --time=00:01:00
#SBATCH --job-name=pytorch_mnist_resuming
#SBATCH --output=mnist_test_resuming.out


# Activate environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv miniconda-python39
conda activate pytorch_env

# Run the Python script that uses the GPU 
# and which checks if the target number 
# of epochs has been reached.
python -u pytorch_mnist_resuming.py --epochs 500 --save-model > mnist_test_resuming-subtask_${SLURM_ARRAY_TASK_ID}.txt

