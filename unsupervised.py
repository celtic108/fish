#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#    Unsupervised learning
#    to group images  
#_________________________________

import numpy as np
import os
import imagedataloadertiny as idl  #contains get_dataset function
import time
from PIL import Image

scale=6
width = 20*scale
height = 13*scale
k = width*height*3
groups = 29
size = (width, height)

start_time = time.time()
count = 0
rootdir = '/home/greg/Desktop/fish/sorted'
sample_size = 0
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		sample_size +=1
images, labels, filenames = idl.get_dataset(sample_size+1, size, rootdir)
length = images.shape[0]
images = np.asarray(images).reshape(length,k)
#centers = np.random.randint(0, 255, (groups,k))
centers = []
for i in range(groups):
	centers.append(images[i])
centers = np.asarray(centers)



for iteration in range(50):
	best_centers = []
	min_distances = []
	for image in images:
		min_distance = float("inf")
		center_count = 0
		for center in centers:
			distance = 0.0
			for i in range(k):
				delta = image[i]-center[i]
				distance += delta*delta
			if distance < min_distance:
				min_distance=distance
				best_center = center_count
			center_count+=1
		best_centers.append(best_center)
		min_distances.append(min_distance)
	for center in range(groups):
		sum_array = np.zeros(k)
		count = 0.0
		index = 0
		for best in best_centers:
			if best == center:
				sum_array = sum_array+images[index]
				count +=1
			index+=1
		centers[center]=sum_array/count

print max(min_distances)
print min(min_distances)


#for g in range(groups):
#	pix = Image.new('RGB', (width, height))
#	gen_image = pix.load()
#	gen_pixels = centers[g]
#	for i in range(width):
#		for j in range(height):
#			gen_image[i,j]=(int(gen_pixels[3*(i+j*width)]),
#			int(gen_pixels[3*(i+j*width)+1]), 
#			int(gen_pixels[3*(i+j*width)+2]))
#	pix = pix.resize((500, 325), Image.ANTIALIAS)
#	pix.show()

for i in range(groups):
	newpath = rootdir+(('/center_%s') % (i))
	if not os.path.exists(newpath): os.makedirs(newpath)
	
for mypath, center in zip(filenames, best_centers):
	last_slash = 0
	count = 0
	for character in mypath:
		if character == '/':
			last_slash = count
		count +=1
	os.rename(mypath, mypath[:last_slash]+'/center_'+str(center)+mypath[last_slash:])
	
