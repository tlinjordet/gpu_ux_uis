# Slurm Quickstart

[Slurm](https://slurm.schedmd.com/) is a resource manager and job scheduler system, which we will use to begin moving away from manually reserving blocks of time in a calendar. 
 
While Slurm has its own documentation that is worth looking at, the following will demonstrate a minimal way to run a deep learning script on one of gorina7's A100 GPUs.
 
Jobs are launched from gorina11, so ssh to gorina11 first. 
```
ssh username@gorina11.ux.uis.no
cd /bhome/username/
```
Your data and script should be somewhere under `/bhome/$username/`.
 
First, we have an example Python script to train a deep neural network using the PyTorch framework, `pytorch_mnist.py`, see the other files in this repo. 
 
Second, we have the shell script that gets passed to Slurm, `pytorch_mnist.sh`:
 
```
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
```
This script is run from gorina11 simply by the command
```
sbatch pytorch_mnist.sh
```
and the progress can be tracked by
```
tail -f mnist_test_01.out
```
 
Now, after a while, the neural network should be training! 
You've been quickstarted on Slurm. 
 
 
## Anatomy of a Quickstart (explanatory notes): 
 
To gain a bit more understanding, we can discuss the options used here. 
The comments starting with `#SBATCH` are passed to Slurm. 
Thus, 
```
#SBATCH --gres=gpu:1
```
indicates that the computational resources provided should be of the type GPU, and that one is required. Next, 
```
#SBATCH --partition=gpuA100
```
indicates that the resources should be provided from the gpuA100 partition, currently consisting of the GPUs physically located on gorina7. Then
```
#SBATCH --time=02:15:00
```
indicates the maximum time limit for the job. The partition and cluster have time limits too, but for efficient job scheduling it is the duty of a community-oriented user to make as accurate time estimates as possible. 
 
The job name is defined by
```
#SBATCH --job-name=pytorch_mnist
```
and can be seen, along with other jobs, from gorina11 by the command `squeue`. It's helpful to consistently update the job name to reflect what is actually being done. 
 
Finally, 
```
#SBATCH --output=mnist_test_01.out
```
defines the filename to store the job output into.
 
That's it for the preamble.
 
The `uenv` command 
```
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
```
helps to provision the desired CUDA and cudnn driver versions. 
The next `uenv` command 
```
uenv miniconda-python39
```
also provides the shared miniconda-installation where commonly used/shared environments can be located.  
 
Note that the environment-creating command 
```
# conda create -n pytorch_env -c pytorch pytorch torchvision numpy -y
```
is left in the script, albeit commented out, to indicate what packages are contained therein. 

Finally, the environment is activated, 
```
conda activate pytorch_env
```
and the deep learning example script is run:
```
python -u pytorch_mnist.py
```
