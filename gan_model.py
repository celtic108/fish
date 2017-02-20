#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#    General adversarial network
#    to create average images to 
#    subtract from the training
#    images
#_________________________________

import tensorflow as tf
import numpy as np
import imagedataloadertiny as idl  #contains get_dataset function
import time
from PIL import Image

#k = 1950000
scale=3
width = 20*scale
height = 13*scale
k = width*height*3
l = 15
size = (width, height)


X = tf.placeholder(tf.float32, shape=[None, k])
W1 = tf.Variable(tf.truncated_normal([k,l], mean=0.0, stddev=0.001))
b1 = tf.Variable(tf.zeros([l])/10)
W2 = tf.Variable(tf.truncated_normal([l,k], mean=0.0, stddev=0.1))
b2 = tf.Variable(tf.zeros([k])/10)

Y1 = tf.nn.sigmoid(tf.matmul(X/255.0, W1) + b1)
Yout = tf.nn.sigmoid(tf.matmul(Y1, W2) + b2)

bitwise_input = tf.placeholder(tf.float32, shape=[None,l])

genYout = tf.nn.relu(tf.matmul(bitwise_input, W2) + b2)

loss = tf.reduce_sum(tf.squared_difference(Yout, X/255.0))
trainer = tf.train.GradientDescentOptimizer(0.0003).minimize(loss)

saver = tf.train.Saver([W1, b1, W2, b2])

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

#if you want to restore the weights and biases from the previous run
save_question = input("Restore previous model? 1 for yes: ")
if save_question ==1:
	saver.restore(sess, "./model")

entry = input("Perform training? 1 for yes: ")

if entry ==1:

	start_time = time.time()
	count = 0
	sample_size = 45
	prev_error = 999999999999
	error_change = 100.0
	for i in range(1):
		images, labels = idl.get_dataset(sample_size, size)
		length = images.shape[0]
		print images.shape
		print length
		print k
		images = np.asarray(images).reshape(length,k)
		while error_change > 0:
			#print type(images)
			#print np.asarray(images).shape
			error, _ = sess.run([loss,trainer], feed_dict={X:images})
			error_change = prev_error-error
			prev_error = error
			if count % 1000 == 0:
				print ("Error %.3f   Time: %.2f" % (error, time.time()-start_time))
			count +=1
	#predict = sess.run(modelout, feed_dict={modelX:oldboards[200].reshape(1,18)})
	#print predict
	
	entry2 = input("Do you want to save the results? 1 for yes: ")
	if entry2 ==1:
		saver.save(sess,"./model")

#input_sequence = np.asarray([0, 1, 1, 1]).reshape((1,4))
pix = Image.new('RGB', (width, height))
gen_image = pix.load()
#gen_pixels = sess.run(genYout, feed_dict={bitwise_input:input_sequence})

dummy, _ = idl.get_dataset(1, size)
gen_pixels = sess.run(Yout, feed_dict={X:np.asarray(dummy).reshape(1,k)})

#gen_pixels = np.asarray(gen_pixels*255).reshape(500, 325, 3).astype(int)

#gen_pixels = dummy
#for i in range(3):
#	print np.asarray(dummy).reshape(1,k)[0][i]
#print (gen_pixels[0,0],gen_pixels[0,1],gen_pixels[0,2])

for i in range(width):
	for j in range(height):
		gen_image[i,j]=(int(255*gen_pixels[0,3*(i+j*width)]),
		 int(255*gen_pixels[0,3*(i+j*width)+1]), 
		 int(255*gen_pixels[0,3*(i+j*width)+2]))
#print gen_image[1,1]
size = 500, 325
pix = pix.resize(size, Image.ANTIALIAS)
pix.show()
