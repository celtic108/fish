#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Read in all images and write the RGB pixel
#   values to a single labeled csv file
#______________________________________________

from PIL import Image
import numpy as np
import os
import csv
import time


def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
    width, height = image.size
    image = image.crop((width//2-500, height//2-325, width//2+500, height//2+325))
    size = 500, 325
    image = image.resize(size, Image.ANTIALIAS)
    pixel_values = list(image.getdata())
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = np.array(pixel_values).flatten()
    #print pixel_values.shape
    return pixel_values#, width, height
    

def get_dataset(num_samples):
	#start_time = time.time()
	rootdir = '/home/greg/Desktop/fish/train/Curated'
	#ALB = 0
	#BET = 0
	#DOL = 0
	#LAG = 0
	#NoF = 0
	#OTHER = 0
	#SHARK = 0
	#YFT = 0
	
	idx = np.random.choice(45,size = num_samples, replace = False)
	#print idx
	count = 0
	images = []
	labels = []
	#width = 1280
	#height = 720
	#minwidth = 1000000
	#minheight = 10000000
	#maxwidth = 0
	#maxheight = 0
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			count +=1
			if count in idx:
				print os.path.join(subdir, file)
				if "SHARK" in os.path.join(subdir, file):
					pixel_values = get_image(os.path.join(subdir, file))
					labels.append([0,0,0,0,0,0,7,0])
					#SHARK +=1
				elif "ALB" in os.path.join(subdir, file):
					pixel_values = get_image(os.path.join(subdir, file))
					labels.append([1,0,0,0,0,0,0,0])
					#ALB +=1
				elif "BET" in os.path.join(subdir, file):
					pixel_values = get_image(os.path.join(subdir, file))
					labels.append([0,1,0,0,0,0,0,0])
					#BET +=1
				elif "LAG" in os.path.join(subdir, file):
					#LAG +=1
					labels.append([0,0,0,1,0,0,0,0])
					pixel_values = get_image(os.path.join(subdir, file))
					#with open('raw_training.csv', 'a') as csvfile:
						#writer = csv.writer(csvfile)
						#writer.writerow([[0, 0, 0, 1, 0, 0, 0, 0],pixel_values,file])
						#foo = np.concatenate(([0, 0, 0, 1, 0, 0, 0, 0],pixel_values))
						#np.savetxt(csvfile, foo,delimiter = ",")
				elif "NoF" in os.path.join(subdir, file):
					pixel_values = get_image(os.path.join(subdir, file))
					labels.append([0,0,0,0,1,0,0,0])
					#NoF +=1
				elif "DOL" in os.path.join(subdir, file):
					pixel_values = get_image(os.path.join(subdir, file))
					labels.append([0,0,1,0,0,0,0,0])
					#DOL +=1
				elif "YFT" in os.path.join(subdir, file):
					pixel_values = get_image(os.path.join(subdir, file))
					labels.append([0,0,0,0,0,0,0,1])
					#YFT +=1
				else:
					pixel_values = get_image(os.path.join(subdir, file))
					labels.append([0,0,0,0,0,1,0,0])
					#OTHER +=1
				#if width > maxwidth:
				#	maxwidth = width
				#if width < minwidth:
				#	minwidth = width
				#if height > maxheight:
				#	maxheight = height
				#if height < minheight:
				#	minheight = height
				
				try:
					images.append(pixel_values)
				except UnboundLocalError:
					print "No pixel values"
					#labels.append([0,0,0,1,0,0,0,0])
	#print ALB
	#print BET
	#print DOL
	#print LAG
	#print NoF
	#print OTHER
	#print SHARK
	#print YFT
	#print minwidth
	#print minheight
	#rint maxwidth
	#print maxheight
	#print time.time()-start_time
	return ((np.asarray(images), np.asarray(labels)))
	

