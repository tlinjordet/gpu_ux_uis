#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --array=1-10%1
#SBATCH --time=02:15:00
#SBATCH --job-name=pytorch_mnist
#SBATCH --output=mnist_test_array.out
 
# Activate environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv miniconda-python39
conda activate pytorch_env
# Run the Python script that uses the GPU
python -u pytorch_mnist.py > subtask_0${SLURM_ARRAY_TASK_ID}.txt
