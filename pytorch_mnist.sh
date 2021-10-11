#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --time=02:15:00
#SBATCH --job-name=pytorch_mnist
#SBATCH --output=mnist_test_01.out
 
# Set up environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv miniconda-python39
# conda create -n pytorch_env -c pytorch pytorch torchvision numpy -y
conda activate pytorch_env
python -u pytorch_mnist.py
