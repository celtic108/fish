import Image
import os

rootdir = '/home/greg/Desktop/fish/safetest/sharks'


new_size = (227, 227)
count = 0
last_slash = 0
for character in rootdir:
	if character == '/':
		last_slash = count
	count +=1
newpath = rootdir[:last_slash]+'/chopped'
if not os.path.exists(newpath): os.makedirs(newpath)
	
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if not file.startswith('.'):
			old_image = Image.open(os.path.join(subdir, file), 'r')
			width, height = old_image.size
			for i in range(13):
				for j in range(7):
					image = old_image.crop((int(i*227/2), int(j*227/2), int(i*227/2)+227, int(j*227/2)+227))
					find_dot = 0
					last_slash = 0
					count = 0
					mypath = str(os.path.join(subdir, file))
					for character in mypath:
						if character == '/':
							next_to_last_slash = last_slash
							last_slash = count
						if character == '.':
							find_dot = count
						count +=1
					image.save(mypath[:next_to_last_slash]+'/chopped'+mypath[last_slash:find_dot]+str(i)+str(j)+mypath[find_dot:])
					
