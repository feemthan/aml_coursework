# Import necessary packages
import os
import subprocess
import pdb
from PIL import Image

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import json
from tqdm import tqdm

directory = 'HMDB_simp'
new_size = (224, 224)

file_paths = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.jpg'):
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

for image_path in tqdm(file_paths, desc="Resizing images", unit="image"):
    image = Image.open(image_path)
    resized_image = image.resize(new_size)
    resized_image.save(image_path)

root_dir = 'video_outputs'
if not os.path.exists(root_dir):
    os.makedirs(root_dir)
else:
    pass

# call ffmpeg to generate videos via subprocess
root_dir = 'HMDB_simp'
for classes in os.listdir(root_dir):
    for folders in os.listdir(os.path.join(root_dir, classes)):
        output_dir = 'video_outputs/' + classes
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            pass
        subprocess.call(['ffmpeg', '-y', '-r', '30', '-pattern_type', 'sequence','-i', 'HMDB_simp/'+classes+'/'+folders+'/%04d.jpg', output_dir +'/'+folders+'.mp4'])

# Train, test and val dataset preparation
current_dir = os.getcwd()
class_path = []
for dir_path, _, files in os.walk(root_dir):
    for file in files:
        if not file.endswith('.csv'):
            paths = os.path.join(current_dir, dir_path, file)
            class_name = dir_path.split('/')[-1]
            class_path.append([f"{paths} {class_name}"])

# convert to dataframe to be run by train_test_split
dataset = pd.DataFrame(class_path)
dataset.to_csv('class_path.csv', index=False, header=False)

file_path = dataset.iloc[:, 0].str.split(' ', expand=True)[0]
class_name = dataset.iloc[:, 0].str.split(' ', expand=True)[1]

label_encoder = LabelEncoder()
class_name = label_encoder.fit_transform(class_name)

# map the labels to numbers
label_to_num_map = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
label_to_num_map = {k: int(v) for k, v in label_to_num_map.items()}

# build json file to remap in the future
with open('label_mapping.json', 'w') as file:
    json.dump(label_to_num_map, file)

# split multiple times for 70 15 15, put your student ID here
STUDENT_ID = 2538
X_train, X_temp, y_train, y_temp = train_test_split(file_path, class_name, test_size=0.3, random_state=STUDENT_ID)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=STUDENT_ID)

# convert to dataframe
train_df = pd.DataFrame({'filepath': X_train, 'class': y_train})
val_df = pd.DataFrame({'filepath': X_val, 'class': y_val})
test_df = pd.DataFrame({'filepath': X_test, 'class': y_test})

# save to csv without index or header
train_df.to_csv('video_outputs/train.csv', index=False, header=False, sep=' ')
val_df.to_csv('video_outputs/val.csv', index=False, header=False, sep=' ')
test_df.to_csv('video_outputs/test.csv', index=False, header=False, sep=' ')
