#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --array=1-20%1
#SBATCH --time=00:01:00
#SBATCH --job-name=pytorch_mnist_resuming
#SBATCH --output=mnist_test_resuming.out

TARGET_EPOCHS=50

# Activate environment
uenv verbose cuda-11.4 cudnn-11.4-8.2.4
uenv miniconda-python39
conda activate pytorch_env

# Run the Python script that uses the GPU 
# and which checks if the target number 
# of epochs has been reached.
echo $SLURM_JOBID
echo $SLURM_ARRAY_JOB_ID

echo $SLURM_ARRAY_JOB_ID > mnist_test_resuming-subtask_${SLURM_ARRAY_TASK_ID}.txt
echo $SLURM_ARRAY_TASK_ID >>  mnist_test_resuming-subtask_${SLURM_ARRAY_TASK_ID}.txt
python -u pytorch_mnist_resuming.py --epochs $TARGET_EPOCHS --save-model > mnist_test_resuming-subtask_${SLURM_ARRAY_TASK_ID}.txt

# Stop job array after the first subtask where the final checkpoint exists.
echo "Checking for mnist_cnn_epoch${TARGET_EPOCHS}.pt"
if [ -f  "mnist_cnn_epoch${TARGET_EPOCHS}.pt" ]; then
  echo "Final checkpoint exists. Cancelling array job."
  scancel --state=PENDING $SLURM_ARRAY_JOB_ID
  sleep 40
fi
