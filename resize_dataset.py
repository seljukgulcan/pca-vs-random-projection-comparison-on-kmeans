import sys
import os
from pathlib import Path

import skimage
import numpy as np

# Resizes images to lower dimensions

# Usage: resize_dataset.py <dataset_folder> <dimension>
# Example: resize_dataset.py train2017 64

dataset = sys.argv[1]
dimension = int(sys.argv[2])

resized_img_folder = f'{dataset}_{dimension}'

if not os.path.isdir(resized_img_folder):
    os.mkdir(resized_img_folder)

for filename in os.listdir(dataset):
    input_filepath = Path(dataset) / filename
    im = skimage.io.imread(input_filepath)

    if im.ndim != 3:
        continue # We exclude the grayscale images

    im = skimage.transform.resize(im, output_shape=(dimension, dimension))
    im = (im * 255).astype(np.uint8)
    output_filepath = Path(resized_img_folder) / filename
    skimage.io.imsave(output_filepath, im)