# Manual Train / Val / Test Split Script

from pathlib import Path
import random
import os
import sys
import shutil
import argparse

# Define and parse user input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--datapath', required=True,
                    help='Path to data folder containing images/labels')
parser.add_argument('--train_pct', type=float, default=0.7,
                    help='Train percentage (e.g., 0.7)')
parser.add_argument('--val_pct', type=float, default=0.2,
                    help='Validation percentage (e.g., 0.2)')
parser.add_argument('--test_pct', type=float, default=0.1,
                    help='Test percentage (e.g., 0.1)')
args = parser.parse_args()

# Validate sum
total = args.train_pct + args.val_pct + args.test_pct
if abs(total - 1.0) > 1e-6:
    print(f"ERROR: train_pct + val_pct + test_pct = {total}, must equal 1.0")
    sys.exit(1)

data_path = args.datapath

if not os.path.isdir(data_path):
    print("ERROR: datapath not found.")
    sys.exit(1)

# Input folders
input_image_path = os.path.join(data_path, 'images')
input_label_path = os.path.join(data_path, 'labels')

# Output paths
cwd = os.getcwd()
train_img_path = os.path.join(cwd, 'data/train/images')
train_txt_path = os.path.join(cwd, 'data/train/labels')
val_img_path   = os.path.join(cwd, 'data/validation/images')
val_txt_path   = os.path.join(cwd, 'data/validation/labels')
test_img_path  = os.path.join(cwd, 'data/test/images')
test_txt_path  = os.path.join(cwd, 'data/test/labels')

# Create folders
for p in [train_img_path, train_txt_path,
          val_img_path, val_txt_path,
          test_img_path, test_txt_path]:
    os.makedirs(p, exist_ok=True)

# Collect images
img_files = list(Path(input_image_path).rglob('*'))
random.shuffle(img_files)

file_num = len(img_files)
train_num = int(file_num * args.train_pct)
val_num   = int(file_num * args.val_pct)
test_num  = file_num - train_num - val_num

print(f"Total images: {file_num}")
print(f"Train: {train_num}, Val: {val_num}, Test: {test_num}")

# Split lists
train_files = img_files[:train_num]
val_files   = img_files[train_num:train_num + val_num]
test_files  = img_files[train_num + val_num:]

splits = [
    (train_files, train_img_path, train_txt_path),
    (val_files,   val_img_path,   val_txt_path),
    (test_files,  test_img_path,  test_txt_path)
]

# Copy files
for file_list, img_dest, txt_dest in splits:
    for img_path in file_list:
        img_fn = img_path.name
        base_fn = img_path.stem
        txt_path = os.path.join(input_label_path, base_fn + '.txt')

        shutil.copy(img_path, os.path.join(img_dest, img_fn))

        if os.path.exists(txt_path):
            shutil.copy(txt_path, os.path.join(txt_dest, base_fn + '.txt'))

print("Done! Train/Val/Test split completed.")
