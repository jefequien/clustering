import argparse
import os
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, '.')

import torch
import torchvision.transforms as transforms

import datasets

DATA_DIR = "data"
DATASETS = {
        "coco_2017_train": {
            "img_dir": "coco/train2017",
            "ann_file": "coco/annotations/instances_train2017.json"
        },
        "coco_2017_val": {
            "img_dir": "coco/val2017",
            "ann_file": "coco/annotations/instances_val2017.json"
        },
        "ade20k_train": {
            "img_dir": "ade20k/images",
            "ann_file": "ade20k/annotations/instances_train.json"
        },
        "ade20k_val": {
            "img_dir": "ade20k/images",
            "ann_file": "ade20k/annotations/instances_val.json"
        },
        "places": {
            "img_dir": "/data/vision/torralba/ade20k-places/data",
            "ann_file": ""
        },
    }


def load_dataset(dataset_name, training=False):
    img_dir = DATASETS[dataset_name]["img_dir"]
    ann_file = DATASETS[dataset_name]["ann_file"]

    if img_dir[0] != "/" and img_dir[0] != ".":
        img_dir = os.path.join(DATA_DIR, img_dir)
    if ann_file[0] != "/" and ann_file[0] != ".":
        ann_file = os.path.join(DATA_DIR, ann_file)

    train_transforms = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])
    val_transforms = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    if training:
        return datasets.coco.COCODataset(img_dir, ann_file, transform=train_transforms)
    else: 
        return datasets.coco.COCODataset(img_dir, ann_file, transform=val_transforms)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    args.workers = 1
    args.batch_size = 128
    
    train_dataset_name = "ade20k_train"
    val_dataset_name = "ade20k_val"
    train_dataset = load_dataset(train_dataset_name, training=True)
    val_dataset = load_dataset(val_dataset_name, training=False)

    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True,
        num_workers=args.workers, pin_memory=True)

    val_loader = torch.utils.data.DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False,
        num_workers=args.workers, pin_memory=True)

    data_loader = val_loader

    for i, (images, target, index) in enumerate(data_loader):
        print(images.shape, target.shape, index.shape)
        for image, targ, idx in zip(images, target, index):
            print(image.shape, targ, idx)
            print(data_loader.dataset.get_info(idx))
            image = np.array(image.numpy() * 255, dtype="uint8")
            image = np.transpose(image, (1,2,0))
            image = Image.fromarray(image)
            image.show()
            input("Press Enter to continue...")
            break



