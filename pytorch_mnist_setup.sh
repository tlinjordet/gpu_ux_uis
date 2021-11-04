#!/bin/bash
#SBATCH --gres=gpu:0
#SBATCH --partition=gpuA100 
#SBATCH --time=02:15:00
#SBATCH --job-name=pytorch_mnist_setup
#SBATCH --output=mnist_setup.out
 
# Set up environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv anaconda-3
conda create -n pytorch_env -c pytorch pytorch torchvision numpy -y
