# Import necessary packages
import os
import subprocess
import pdb
import pandas as pd
from sklearn.model_selection import train_test_split

# call ffmpeg to generate videos via subprocess
root_dir = 'HMDB_simp'
for classes in os.listdir(root_dir):
    for folders in os.listdir(os.path.join(root_dir, classes)):

        subprocess.call(['ffmpeg', '-y', '-r', '30', '-pattern_type', 'sequence','-i', f'HMDB_simp/{classes}/{folders}/%04d.jpg', f'video_outputs/{classes}_{folders}.mp4'])

# Move to class specific location and rename
root_dir = 'video_outputs'
for file_name in os.listdir(root_dir):

    class_name = file_name.split('_')[0]
    if not os.path.exists(f'{root_dir}/{class_name}'):
        os.makedirs(f'{root_dir}/{class_name}')

    subprocess.call(['mv', f'{root_dir}/{file_name}', f'{root_dir}/{class_name}/{file_name.split("_")[-1].split(".")[0]}.mp4'])

# Train, test and val dataset preparation
class_path = []
for dir_path, _, files in os.walk(root_dir):
    for file in files:

        paths = os.path.join(dir_path, file)
        class_name = dir_path.split('/')[-1]
        class_path.append([paths, class_name])

# convert to dataframe to be run by train_test_split
dataset = pd.DataFrame(class_path)
dataset.to_csv('class_path.csv', index=False, header=False)

file_path = dataset.iloc[:,0]
class_name = dataset.iloc[:, 1]

# split multiple times for 70 15 15
X_train, X_temp, y_train, y_temp = train_test_split(file_path, class_name, test_size=0.3, random_state=2538)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=2538)

# convert to dataframe
train_df = pd.DataFrame({'filepath': X_train, 'class': y_train})
val_df = pd.DataFrame({'filepath': X_val, 'class': y_val})
test_df = pd.DataFrame({'filepath': X_test, 'class': y_test})

# save to csv without index or header
train_df.to_csv('train.csv', index=False, header=False)
val_df.to_csv('val.csv', index=False, header=False)
test_df.to_csv('test.csv', index=False, header=False)