from numpy import *
import os
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import time
from scipy.misc import imread
from scipy.misc import imresize
import matplotlib.image as mpimg
from scipy.ndimage import filters
import urllib
from numpy import random


import tensorflow as tf

from caffe_classes import class_names
import Image
import os

#point to the folder that contains the folders of pictures
rootdir = '/home/greg/Desktop/fish/sorted/curated'

def conv(input, kernel, biases, k_h, k_w, c_o, s_h, s_w,  padding="VALID", group=1):
    '''From https://github.com/ethereon/caffe-tensorflow
    '''
    c_i = input.get_shape()[-1]
    assert c_i%group==0
    assert c_o%group==0
    convolve = lambda i, k: tf.nn.conv2d(i, k, [1, s_h, s_w, 1], padding=padding)
    
    
    if group==1:
        conv = convolve(input, kernel)
    else:
        input_groups = tf.split(3, group, input)
        kernel_groups = tf.split(3, group, kernel)
        output_groups = [convolve(i, k) for i,k in zip(input_groups, kernel_groups)]
        conv = tf.concat(3, output_groups)
    return  tf.reshape(tf.nn.bias_add(conv, biases), [-1]+conv.get_shape().as_list()[1:])



train_x = zeros((1, 227,227,3)).astype(float32)
#train_y = zeros((1, 1000))
xdim = train_x.shape[1:]
#ydim = train_y.shape[1]

net_data = load("bvlc_alexnet.npy").item()

x = tf.placeholder(tf.float32, (None,) + xdim)

#conv1
#conv(11, 11, 96, 4, 4, padding='VALID', name='conv1')
k_h = 11; k_w = 11; c_o = 96; s_h = 4; s_w = 4
conv1W = tf.Variable(net_data["conv1"][0])
conv1b = tf.Variable(net_data["conv1"][1])
conv1_in = conv(x, conv1W, conv1b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=1)
conv1 = tf.nn.relu(conv1_in)

#lrn1
#lrn(2, 2e-05, 0.75, name='norm1')
radius = 2; alpha = 2e-05; beta = 0.75; bias = 1.0
lrn1 = tf.nn.local_response_normalization(conv1,
												depth_radius=radius,
												alpha=alpha,
												beta=beta,
												bias=bias)

#maxpool1
#max_pool(3, 3, 2, 2, padding='VALID', name='pool1')
k_h = 3; k_w = 3; s_h = 2; s_w = 2; padding = 'VALID'
maxpool1 = tf.nn.max_pool(lrn1, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)


#conv2
#conv(5, 5, 256, 1, 1, group=2, name='conv2')
k_h = 5; k_w = 5; c_o = 256; s_h = 1; s_w = 1; group = 2
conv2W = tf.Variable(net_data["conv2"][0])
conv2b = tf.Variable(net_data["conv2"][1])
conv2_in = conv(maxpool1, conv2W, conv2b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
conv2 = tf.nn.relu(conv2_in)


#lrn2
#lrn(2, 2e-05, 0.75, name='norm2')
radius = 2; alpha = 2e-05; beta = 0.75; bias = 1.0
lrn2 = tf.nn.local_response_normalization(conv2,
												depth_radius=radius,
												alpha=alpha,
												beta=beta,
												bias=bias)

#maxpool2
#max_pool(3, 3, 2, 2, padding='VALID', name='pool2')                                                  
k_h = 3; k_w = 3; s_h = 2; s_w = 2; padding = 'VALID'
maxpool2 = tf.nn.max_pool(lrn2, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

#conv3
#conv(3, 3, 384, 1, 1, name='conv3')
k_h = 3; k_w = 3; c_o = 384; s_h = 1; s_w = 1; group = 1
conv3W = tf.Variable(net_data["conv3"][0])
conv3b = tf.Variable(net_data["conv3"][1])
conv3_in = conv(maxpool2, conv3W, conv3b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
conv3 = tf.nn.relu(conv3_in)

#conv4
#conv(3, 3, 384, 1, 1, group=2, name='conv4')
k_h = 3; k_w = 3; c_o = 384; s_h = 1; s_w = 1; group = 2
conv4W = tf.Variable(net_data["conv4"][0])
conv4b = tf.Variable(net_data["conv4"][1])
conv4_in = conv(conv3, conv4W, conv4b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
conv4 = tf.nn.relu(conv4_in)


#conv5
#conv(3, 3, 256, 1, 1, group=2, name='conv5')
k_h = 3; k_w = 3; c_o = 256; s_h = 1; s_w = 1; group = 2
conv5W = tf.Variable(net_data["conv5"][0])
conv5b = tf.Variable(net_data["conv5"][1])
conv5_in = conv(conv4, conv5W, conv5b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
conv5 = tf.nn.relu(conv5_in)

#maxpool5
#max_pool(3, 3, 2, 2, padding='VALID', name='pool5')
k_h = 3; k_w = 3; s_h = 2; s_w = 2; padding = 'VALID'
maxpool5 = tf.nn.max_pool(conv5, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

maxpool5_replace = tf.placeholder(tf.float32, shape=[None, 6, 6, 256])

#fc6
#fc(4096, name='fc6')
#fc6W = tf.Variable(net_data["fc6"][0])
#fc6b = tf.Variable(net_data["fc6"][1])
fc6W = tf.Variable(tf.random_uniform([9216,4096]))
fc6b = tf.Variable(tf.zeros([4096]))
fc6 = tf.nn.relu_layer(tf.reshape(maxpool5_replace, [-1, int(prod(maxpool5_replace.get_shape()[1:]))]), fc6W, fc6b)

#fc7 - modified
#fc(4096, name='fc7')
fc7W = tf.Variable(tf.random_uniform([4096, 1000]))
fc7b = tf.Variable(tf.zeros([1000]))
fc7 = tf.nn.relu_layer(fc6, fc7W, fc7b)

#fc8
#fc(1000, relu=False, name='fc8')
fc8W = tf.Variable(tf.random_uniform([1000,2]))
fc8b = tf.Variable(tf.zeros([2]))
fc8 = tf.nn.xw_plus_b(fc7, fc8W, fc8b)


#prob
#softmax(name='prob'))
prob = tf.nn.softmax(fc8)
answers = tf.placeholder(tf.float32, shape=[None,2])
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=fc8, labels=answers))
trainer = tf.train.AdagradOptimizer(0.0003).minimize(loss)

saver = tf.train.Saver([fc6W, fc6b, fc7W, fc7b, fc8W, fc8b])

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

#if you want to restore the weights and biases from the previous run
save_question = input("Restore previous model? 1 for yes: ")
if save_question ==1:
	saver.restore(sess, "./model_for_top_layers")

t = time.time()

new_size = (227, 227)
last_slash = 0
#count = 0
#for character in rootdir:
#	if character == '/':
#		last_slash = count
#	count +=1
#newpath = rootdir[:last_slash]+'/chopped'
#if not os.path.exists(newpath): os.makedirs(newpath)

fishdir = '/home/greg/Desktop/fish/sorted/chopped/fish'
notfishdir = '/home/greg/Desktop/fish/sorted/chopped/notfish'

count =0
#1193
for subdir, dirs, files in os.walk(fishdir):
	for file in files:
		count +=1
print "fish ",count
num_samples = input("how many images to use? ")
idx = np.random.choice(count+1,size = num_samples, replace = False)
#count =0
#342517
#for subdir, dirs, files in os.walk(notfishdir):
#	for file in files:
#		count +=1
print "not fish ",count
num_samples = input("how many images to use? ")
idx2 = np.random.choice(count+1,size = num_samples, replace = False)
	
count = 0
training_inputs = []
training_outputs = []
for subdir, dirs, files in os.walk(fishdir):
	for file in files:
		if not file.startswith('.'):
			count+=1
			if count in idx:
				im1 = (imread(os.path.join(subdir, file))[:,:,:3]).astype(float32)
				training_inputs.append(np.asarray(sess.run(maxpool5, feed_dict = {x:[im1]})).reshape((6,6,256)))
				#print training_inputs[0].shape
				training_outputs.append((1,0))
count = 0
for subdir, dirs, files in os.walk(notfishdir):
	for file in files:
		if not file.startswith('.'):
			count+=1
			if count in idx2:
				im1 = (imread(os.path.join(subdir, file))[:,:,:3]).astype(float32)
				training_inputs.append(np.asarray(sess.run(maxpool5, feed_dict = {x:[im1]})).reshape((6,6,256)))
				training_outputs.append((0,1))
			
print np.asarray(training_inputs).shape
print np.asarray(training_outputs).shape

entry = input("Perform training? 1 for yes: ")

if entry ==1:

	start_time = time.time()
	prev_error = 999999999999
	error_change = 100.0
	count = 0
	for i in range(1):
		while error_change > 0:
			#print type(images)
			#print np.asarray(images).shape
			error, _ = sess.run([loss,trainer], feed_dict={maxpool5_replace:training_inputs, answers:training_outputs})
			error_change = prev_error-error
			prev_error = error
			if count % 1000 == 0:
				print ("Error %.3f   Time: %.2f" % (error, time.time()-start_time))
			count +=1
	

entry2 = input("Do you want to save the results? 1 for yes: ")
if entry2 ==1:
	saver.save(sess,"./model_for_top_layers")
