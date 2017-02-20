from PIL import Image
import numpy as np

image1 = Image.open('train/ALB/img_00043.jpg')
#image1.show()

image2 = Image.open('train/ALB/img_00097.jpg')
#image2.show()
image3 = Image.open('train/ALB/img_00121.jpg')
image4 = Image.open('train/ALB/img_00134.jpg')
image5 = Image.open('train/ALB/img_00191.jpg')

pix1 = image1.load()
pix2 = image2.load()
pix3 = image3.load()
pix4 = image4.load()
pix5 = image5.load()
print image1.size
#for x in range(1280):
#	for y in range(720):
#		r1, g1, b1 = image1.getpixel((x,y))
#		r2, g2, b2 = image2.getpixel((x,y))
#		r3, g3, b3 = image3.getpixel((x,y))
#		r4, g4, b4 = image4.getpixel((x,y))
#		r5, g5, b5 = image5.getpixel((x,y))
#		r_ave = (r1+r2+r3+r4+r5)/5
#		g_ave = (g1+g2+g3+g4+g5)/5
#		b_ave = (b1+b2+b3+b4+b5)/5
#		pix1[x,y] = (r1-r_ave, g1-g_ave, b1-b_ave)
#		pix2[x,y] = (r2-r_ave, g2-g_ave, b2-b_ave)
#		pix3[x,y] = (r3-r_ave, g3-g_ave, b3-b_ave)
#		pix5[x,y] = (r5-r_ave, g5-g_ave, b5-b_ave)

#image1.show()
#image2.show()
#image3.show()
#mage4.show()
#image5.show()

a = np.arange(24).reshape((4,3,2))
print a
print a.flatten()
