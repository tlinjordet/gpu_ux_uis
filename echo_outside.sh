#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --time=00:01:00
#SBATCH --job-name=echo_outisde
#SBATCH --output=echo_outside_test.out
echo "Able to run sbatch script from inside sbatch script."
