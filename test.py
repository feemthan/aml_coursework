import os

data_dir = './video_outputs'
for i, j, k in os.walk(data_dir):
    print(i, j, k)