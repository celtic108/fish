import Image
import os

rootdir = '/home/greg/Desktop/fish/sorted'


new_size = (1589, 908)

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if not file.startswith('.'):
			old_image = Image.open(os.path.join(subdir, file), 'r')
			new_image = old_image.resize(new_size, Image.ANTIALIAS)
			new_image.save(os.path.join(subdir,file))


#old_im = Image.open('someimage.jpg')
#old_size = old_im.size

#new_size = (800, 800)
#new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
#new_im.paste(old_im, ((new_size[0]-old_size[0])/2,
#                      (new_size[1]-old_size[1])/2))

#new_im.show()
# new_im.save('someimage.jpg')
