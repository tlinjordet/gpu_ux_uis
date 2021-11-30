# Slurm Quickstart

[Slurm](https://slurm.schedmd.com/) is a resource manager and job scheduler system, which we will use to begin moving away from manually reserving blocks of time in a calendar. 
 
While Slurm has its own documentation that is worth looking at, the following will demonstrate a minimal way to run a deep learning script on one of gorina7's A100 GPUs.
 
Jobs are launched from gorina11, so ssh to gorina11 first. Enter the following commands:
```
ssh $username@gorina11.ux.uis.no
cd /bhome/$username/
```
To run on GPUs via Slurm, your data and script should always be placed somewhere under `/bhome/$username/`.

To run through this quickstart, continue with the following commands:
```
git clone https://github.com/tlinjordet/gpu_ux_uis.git
cd gpu_ux_uis
sbatch pytorch_mnist_setup.sh 
tail -f mnist_setup.out
```
Wait until the environment is done being created. You can read ahead while this is happening to understand what the quickstart does and demonstrates, and then come back here to run the final commands. 

Finally, run the following commands to actually run the script that trains and tests a deep neural network on the MNIST dataset:
```
sbatch pytorch_mnist.sh
tail -f mnist_test_01.out
```

Now, after a while, the neural network should be training! 
You've been quickstarted on Slurm. 

Below are details about the scripts used in the above commands, and some additional Slurm commands to try out. 

## Files used in this quickstart

To better understand what is happening in the quickstart scripts and have an idea how to apply this example to your own work, we describe each of the three scripts in turn. 

### Environment setup script 

First, we have the environment setup shell script that gets via `sbatch` passed to Slurm, `pytorch_mnist_setup.sh`:
```
#!/bin/bash
#SBATCH --gres=gpu:0
#SBATCH --partition=gpuA100 
#SBATCH --time=02:15:00
#SBATCH --job-name=pytorch_mnist_setup
#SBATCH --output=mnist_setup.out
 
# Set up environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv miniconda-python39
conda create -n pytorch_env -c pytorch pytorch torchvision numpy -y
```
We should always run a separate job that creates a specific virtual environment without occupying GPUs. This is ensured by the second line of the script, 
```
#SBATCH --gres=gpu:0
```
which specifies that this job should have zero GPUs allocated. The `#SBATCH` options and `uenv` commands are discussed in further detail in the next section. 

Note that the environment-creating command 
```
conda create -n pytorch_env -c pytorch pytorch torchvision numpy -y
```
will create an environment that can later be activated by the command `conda activate pytorch_env` assuming the correct base Anaconda or Miniconda environment is activated, here done by `uenv miniconda-python39`. 

### GPU-job script

Second, we have the GPU-job shell script that gets passed to Slurm by the `sbatch` command, namely `pytorch_mnist.sh`:
 
```
#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --time=02:15:00
#SBATCH --job-name=pytorch_mnist
#SBATCH --output=mnist_test_01.out
 
# Activate environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv miniconda-python39
conda activate pytorch_env
# Run the Python script that uses the GPU
python -u pytorch_mnist.py
```

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

Various drivers and environmental variables are made available via `uenv` commands. For more details, run (e.g., in an `sbatch` script) the command `uenv` with no arguments. 
 
The `uenv` command 
```
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
```
helps to provision the desired CUDA and cudnn driver versions. 
The next `uenv` command 
```
uenv miniconda-python39
```
also provides the shared Miniconda installation to base the environment on. *Note: This base Python may change later, but this works now.*
 
Finally, the environment is activated, 
```
conda activate pytorch_env
```
and the deep learning example script is run:
```
python -u pytorch_mnist.py
```

### Python script

Third, we have an example Python script to train a deep neural network using the PyTorch framework, `pytorch_mnist.py` in this repo. 

Note that this is the Python script called by the final line of `pytorch_mnist.sh`. 
The environment provisioned by Slurm, including an available GPU, means that the user does not have to worry about direct conflicts with other users' processes when sending jobs to a GPU. If the requested resources are not available right now, the job will be queued. 

The details of this script are beyond the scope of this documentation, but it represents a "Hello world" or toy example script for deep learning. See docstrings inside `pytorch_mnist.py` for more information. 

# Troubleshooting

Here, quick solutions to problems encountered by users will be added in an *ad hoc* manner. 

 - If you have no `/bhome/$username` directory, then send theo an email and ask him to make one for you.
 - If you cannot use the `uenv` command, it is probably because you have deleted or modified some of your user configuration files (.bashrc, .profile and/or .login). Send theo an email and ask him to reinstate the standard version of these files for your user. 

# Some additional Slurm commands to try

When you have submitted your job by `sbatch`, you should get a Slurm Job ID, and you can later check on whether your job is running (`R`) or pending (`PD`) by the command `squeue`. 

You can also cancel a job by the command `scancel $JOBID`.

When you have created your own script, you can test it before submitting it to slurm by the command `sbatch --test-only <name of script>.sh`. 

# Conclusion

Please see the official documentation for more [Slurm](https://slurm.schedmd.com/) information. 

However, this is a living document and detailed, technical and constructive questions and comments are welcome, and will be used to update our own specific documentation.
