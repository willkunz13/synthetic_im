# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/Dino.ipynb (unless otherwise specified).

__all__ = ['DinoDataset', 'predict_images']

# Cell
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from skimage import io, transform
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import ipdb
import os
import sys
import copy
from pathlib import Path
from synthetic_im import vision_transformer
from ..lib import get_project_root

# Cell

class DinoDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, path, transform=None):
        self.path = path
        self.files = list(Path(self.path).rglob('*.jpg'))
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = self.files[idx]
        image = io.imread(img_name)
        if self.transform:
            image = self.transform(image)

        return image

# Cell
def predict_images(model, dataloader, patch_size = 8, threshold = .6, output_dir = Path('data/output')):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    was_training = model.training
    for p in model.parameters():
      p.requires_grad = False
    model.eval()
    model.to(device)

    with torch.no_grad():
        for i, inputs in enumerate(dataloader):
            w, h = inputs.shape[2] - inputs.shape[2] % patch_size, inputs.shape[3] - inputs.shape[3] % patch_size
            inputs = inputs[:, :, :w, :h]


            w_featmap = inputs.shape[-2] // patch_size
            h_featmap = inputs.shape[-1] // patch_size

            attentions = model.forward_selfattention(inputs.to(device))
            bs = attentions.shape[0] # batch size
            nh = attentions.shape[1] # number of head

            # we keep only the output patch attention
            attentions = attentions[:, :, 0, 1:].reshape(bs,nh, -1)

            # we keep only a certain percentage of the mass
            val, idx = torch.sort(attentions)
            val /= torch.sum(val, dim=2, keepdim=True)
            cumval = torch.cumsum(val, dim=2)
            th_attn = cumval > (1 - threshold)
            idx2 = torch.argsort(idx)
            for batch in range(bs):
                for head in range(nh):
                    th_attn[batch,head] = th_attn[batch,head][idx2[batch,head]]
            th_attn = th_attn.reshape(bs,nh, w_featmap, h_featmap).float()
            # interpolate
            th_attn = nn.functional.interpolate(th_attn, scale_factor=patch_size, mode="nearest").cpu().numpy()

            attentions = attentions.reshape(bs, nh, w_featmap, h_featmap)
            attentions = nn.functional.interpolate(attentions, scale_factor=patch_size, mode="nearest").cpu().numpy()

            os.makedirs(output_dir, exist_ok=True)

            for batch in range(attentions.shape[0]):
                out_img = attentions[batch].sum(0)
                fname = str(output_dir) + '/attn-' + dataloader.dataset.files[i * bs + batch].name
                plt.imsave(
                    fname=fname,
                    arr=out_img,
                    cmap="inferno",
                    format="jpg"
                )
                print(f"{fname} saved.")
