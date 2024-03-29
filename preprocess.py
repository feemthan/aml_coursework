import os
import subprocess
import pdb

root_dir = 'HMDB_simp'
for classes in os.listdir(root_dir):
    for folders in os.listdir(os.path.join(root_dir, classes)):
        subprocess.call(['ffmpeg', '-y', '-r', '30', '-pattern_type', 'sequence','-i', f'HMDB_simp/{classes}/{folders}/%04d.jpg', f'video_outputs/{classes}_{folders}.mp4'])

root_dir = 'video_outputs'

for file_name in os.listdir(root_dir):
    class_name = file_name.split('_')[0]
    if not os.path.exists(f'{root_dir}/{class_name}'):
        os.makedirs(f'{root_dir}/{class_name}')

    subprocess.call(['mv', f'{root_dir}/{file_name}', f'{root_dir}/{class_name}/{file_name.split("_")[-1].split(".")[0]}.mp4'])

import pandas as pd
class_path = []

for dir_path, _, files in os.walk(root_dir):
    for file in files:
        # print(dir_path, _, file)
        # pdb.set_trace()
        paths = os.path.join(dir_path, file)
        class_name = dir_path.split('/')[-1]
        class_path.append([paths, class_name])

pd.DataFrame(class_path).to_csv('class_path.csv', index=False, header=False)
