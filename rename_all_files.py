import os
import numpy as np

rootdir = '/home/greg/Desktop/fish/train'

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		species = subdir[30:]
		os.rename(os.path.join(subdir, file), os.path.join(subdir, str(species+file)))
		
