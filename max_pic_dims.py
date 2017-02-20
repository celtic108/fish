from PIL import Image
import numpy as np
import os




def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
    width, height = image.size
    #image = image.crop((width//2-500, height//2-325, width//2+500, height//2+325))
    #image = image.resize(size, Image.ANTIALIAS)
    #pixel_values = list(image.getdata())
    #if image.mode == 'RGB':
    #    channels = 3
    #elif image.mode == 'L':
    #    channels = 1
    #else:
    #    print("Unknown mode: %s" % image.mode)
    #    return None
    #pixel_values = np.array(pixel_values).flatten()
    #print pixel_values.shape
    return width, height

rootdir = '/home/greg/Desktop/fish/train'

count =0
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		count +=1
idx = np.arange(count+1)
max_width = 0
max_height = 0
min_width = float("inf")
min_height = float("inf")
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if not file.startswith('.'):
			width, height = get_image(os.path.join(subdir, file))
			if width>max_width:
				max_width = width
			if width<min_width:
				min_width = width
			if height>max_height:
				max_height = height
			if height<min_height:
				min_height = height
				
print "max_width"
print max_width
print "min_width"
print min_width
print "max_height"
print max_height
print "min_height"
print min_height

			
