#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   normalizes the images based 
#   on their grouping
#_________________________________

import numpy as np
import os
import imagedataloadertiny as idl  #contains get_dataset function
import time
from PIL import Image
from scipy import stats
from scipy.stats import norm

def display_image(gen_pixels, size, name):
	gen_pixels = gen_pixels.flatten()
	width, height = size
	pix = Image.new('RGB', (width, height))
	gen_image = pix.load()
	for i in range(width):
		for j in range(height):
			gen_image[i,j]=(int(gen_pixels[3*(i+j*width)]),
			int(gen_pixels[3*(i+j*width)+1]), 
			int(gen_pixels[3*(i+j*width)+2]))
	pix = pix.resize(size, Image.ANTIALIAS)
	pix.show(title=name)

scale=20
width = 20*scale
height = 13*scale
k = width*height*3
size = (width, height)
rootdir = '/home/greg/Desktop/fish/sorted/curated/partyboatday'
count =0
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		count +=1
	
images, labels, filenames = idl.get_dataset(count, size, rootdir)

average_image = np.average(images,axis=0)
image_std = np.std(images, axis=0)
#display_image(images[0], size, 'original')
#display_image(images[0]-average_image, size, 'image minus average')
display_image(average_image, size, 'average image')

#for i in range(5):
#	pixels = []
#	for x,y in zip(images[0],average_image):
#		if abs(x-y)>i*10:
#			pixels.append(x)
#		else:
#			pixels.append(127)
#	display_image(np.asarray(pixels), size)

for image, filename in zip(images, filenames):
	if np.random.rand(1) > 0.95:
		image_diff = image-average_image
		total_diff=[]
		for i in range(width*height):
			total_diff.append(abs(image_diff[3*i])+abs(image_diff[3*i+1])+abs(image_diff[3*i+2]))
		total_diff=np.asarray(total_diff)
		total_std=[]
		for i in range(width*height):
			total_std.append(abs(image_std[3*i])+abs(image_std[3*i+1])+abs(image_std[3*i+2]))
		total_std=np.asarray(total_std)
		#max_pixel = max(image_diff)
		#min_pixel = min(image_diff)
		#display_image((image_diff-min_pixel)*255/max_pixel, size, 'image minum average minus minimum scaled to max = 255')
		new_image = []
		num_pixels = 0
		#for diff, pixel in zip(image_diff, image):
			#print pixel
			#new_image.append(pixel if diff > 20 else 127)
		for pixel in image:
			#print pixel
			if total_diff[int(num_pixels//3)]>total_std[int(num_pixels//3)]*.8:
				new_image.append(pixel)
			else:
				new_image.append(127)
			num_pixels+=1
		display_image(np.asarray(new_image), size, 'normalized')
		_ = input(filename)
