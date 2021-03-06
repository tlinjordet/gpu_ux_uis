#!/usr/bin/env python
# coding=utf-8

# BSD 3-Clause License
#
# Copyright (c) 2017,
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Original source: https://github.com/pytorch/examples/blob/master/mnist/main.py

## Modified by Trond Linjordet 03.06.2022 to illustrate resuming training.
## Added lines for this purpose are marked with the comment `## resume`.

from __future__ import print_function
import argparse
import datetime  ## resume
import os  ## resume
import subprocess  ##resume
import sys
import time  ## resume
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4 * 4 * 50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                )
            )


def test(args, model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(
                output, target, reduction="sum"
            ).item()  # sum up batch loss
            pred = output.argmax(
                dim=1, keepdim=True
            )  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print(
        "\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
            test_loss,
            correct,
            len(test_loader.dataset),
            100.0 * correct / len(test_loader.dataset),
        )
    )
    return test_loss  ## resume


def main():
    # Training settings
    parser = argparse.ArgumentParser(description="PyTorch MNIST Example")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=128,
        metavar="N",
        help="input batch size for training (default: 128)",
    )
    parser.add_argument(
        "--test-batch-size",
        type=int,
        default=1000,
        metavar="N",
        help="input batch size for testing (default: 1000)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=5,
        metavar="N",
        help="number of epochs to train (default: 5)",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=0.01,
        metavar="LR",
        help="learning rate (default: 0.01)",
    )
    parser.add_argument(
        "--momentum",
        type=float,
        default=0.5,
        metavar="M",
        help="SGD momentum (default: 0.5)",
    )
    parser.add_argument(
        "--no-cuda", action="store_true", default=False, help="disables CUDA training"
    )
    parser.add_argument(
        "--seed", type=int, default=1, metavar="S", help="random seed (default: 1)"
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=10,
        metavar="N",
        help="how many batches to wait before logging training status",
    )
    parser.add_argument(
        "--save-model",
        action="store_true",
        default=False,
        help="For Saving the current Model",
    )
    ## resume: {
    # parser.add_argument(
    #    "--slurm_job_id",
    #    type=int,
    #    default=1,
    #    help="For defining dependency",
    # )
    ## } resume.

    args = parser.parse_args()

    ## resume: { Check if the desired number of epochs was reached. If so, exit.
    completed_epoch = 0
    checkpoint_path = ""
    if os.path.exists(f"mnist_cnn_epoch{args.epochs}.pt"):
        # Finish training, no need to relaunch training script again.
        print("The checkpoint for the target final epoch already exists. Exit.")
        return
    # If not, load saved model, and keep training.
    else:
        for epoch in range(1, args.epochs + 1):
            if os.path.exists(f"mnist_cnn_epoch{epoch}.pt"):
                completed_epoch = epoch
                checkpoint_path = f"mnist_cnn_epoch{epoch}.pt"
    print(f"Resuming from epoch {completed_epoch}.")
    ## } resume.

    use_cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)
    ## resume: TODO Check if re-initializing fixed random seed in subtasks
    ## resume: .. affects batches/results during machine learning.
    ## resume: If there is an issue, set a different random seed
    ## resume: for each subtask

    device = torch.device("cuda" if use_cuda else "cpu")

    kwargs = {"num_workers": 1, "pin_memory": True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            "./data",
            train=True,
            download=True,
            transform=transforms.Compose(
                [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
            ),
        ),
        batch_size=args.batch_size,
        shuffle=True,
        **kwargs,
    )
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            "./data",
            train=False,
            transform=transforms.Compose(
                [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
            ),
        ),
        batch_size=args.test_batch_size,
        shuffle=True,
        **kwargs,
    )

    model = Net().to(device)
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)

    ## resume: { Resume if previously saved model checkpoint was found
    ## resume: Use code from https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html
    if completed_epoch > 0:
        print(f"Loading checkpoint {checkpoint_path}.")
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        current_epoch = checkpoint["epoch"]
        assert completed_epoch == current_epoch  ## resume: just a sanity check.
        loaded_loss = checkpoint["loss"]  ## resume: shown in tutorial, not used.
        print("Resume: loaded a checkpoint from a previous Slurm job.")
    ## } resume.
    else:
        current_epoch = 0

    for epoch in range(current_epoch + 1, args.epochs + 1):
        t0 = time.perf_counter()  ## resume
        train(args, model, device, train_loader, optimizer, epoch)
        test_loss = test(args, model, device, test_loader)
        ## resume: {
        if args.save_model:
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": test_loss,
                },
                f"mnist_cnn_epoch{epoch}.pt",
            )
            ## resume: Add code to delete older model files if necessary,
            older_file = f"mnist_cnn_epoch{epoch-5}.pt"
            if os.path.exists(older_file):
                os.remove(older_file)
                print("Resume: cleaned up older checkpoint")
            ## resume: ...TODO to save/propagate the best model so far, etc.
        t1 = time.perf_counter()
        total = t1 - t0
        # totaldelta = str(datetime.timedelta(total))
        print(f"It took {total} seconds to train, test, and save epoch {epoch}.")
        ## } resume.

    ## resume: # if args.save_model:
    ## resume: #    torch.save(model.state_dict(), "mnist_cnn.pt")


if __name__ == "__main__":
    print(torch.cuda.is_available())
    main()
