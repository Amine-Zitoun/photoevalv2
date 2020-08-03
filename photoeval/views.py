from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from flask import Flask,request,render_template,url_for,flash,redirect,jsonify
from InstagramAPI import InstagramAPI
import os
import tensorflow as tf
from PIL import Image
from tensorflow.keras.callbacks import TensorBoard
import cv2
import tensorflow as tf
from PIL import Image
import cv2
import base64
import io
#from funcs import *
import pickle
import numpy as np
import urllib.request,json
import random
import operator

instaApi = InstagramAPI('photoeval', 'tryhardboi')
instaApi.login()



IMG_SIZE=80


def read_json(path):
	print(path+'.json')
	with open(path+'.json', encoding="utf8",errors='ignore') as f:
		data = json.load(f)
	return data
def like_process(likes):
    global boi
    s = 0
    new_likes = []
    for like in likes:
        s += like
    model = s/len(likes)

    for like in likes:
        if like >= model:
            like = 1
            new_likes.append(like)
        else:
            like = 0
            new_likes.append(like)
    return new_likes


def get_userID(username):
	instaApi.searchUsername(username)
	print(username)
	print(instaApi.LastJson["user"])
	try:
		return instaApi.LastJson["user"]["pk"]
	except Exception:
		print("username doesn't exist")
		return False



def follow_id(id):
    instaApi.follow(id)

def training(username,DATADIR):
    json_path = f'{username}'
    json_file = os.path.join(DATADIR,json_path)
    json = read_json(json_file) # 5
    likes =[]
    for i in json['GraphImages']:
        likes.append(i['edge_media_preview_like']['count'])

    new_likes = like_process(likes)


    new_likes.reverse()
    training_data = []
    print(new_likes)
    k = 0
    while (k <= len(os.listdir(DATADIR))-1):
        try:
            print(k)
            class_img = new_likes[k]



            img_array = cv2.imread(os.path.join(DATADIR,os.listdir(DATADIR)[k]),cv2.IMREAD_GRAYSCALE)
            print(img_array)
            new_arr = cv2.resize(img_array, (IMG_SIZE,IMG_SIZE))
            training_data.append([new_arr,class_img])

        except Exception as e:
            pass
        k += 1
    return training_data

def stock(training_data):
	x= []
	y= []
	import pickle

	for features,labels in training_data:
		x.append(features)
		y.append(labels)
	X = np.array(x).reshape(-1,IMG_SIZE,IMG_SIZE,1)


	pickle_boi = open('x.pickle','wb')
	pickle.dump(X,pickle_boi)
	pickle_boi = open('y.pickle','wb')
	pickle.dump(y,pickle_boi)
	pickle_boi.close()
	print('KAMALNA STOCKENA SI ZEBY')



def get_data(username,me,pwd,DATADIR):
    os.system(f'instagram-scraper {username}  -m 24  -t image --media-metadata -u {me} -p {pwd}')
    training_data= training(username,DATADIR)
    print(training_data)
    stock(training_data)






# Create your views here.
def index(request):
    return render(request,'photoeval/index.html')

def test(request):
    return render(request,'photoeval/test.html')


def login(request):
    return render(request,'photoeval/login.html')


def signup(request):
    return render(request,'photoeval/signup.html')



def start(request):
    return render(request,'photoeval/start.html')
def Model():

    X = pickle.load(open('x.pickle', 'rb'))
    y = pickle.load(open('y.pickle', 'rb'))


    X =X/255.0

    conv_layers = [1,2,3]
    dense_layers = [1,2,3]
    layer_sizes = [64,32,128]
    dict_acc = {}
    print("=====================")
    print("started optimizing...")
    print("======================")
    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                model = tf.keras.models.Sequential()
                NAME="{}-conv-{}-nodes-{}-dense".format(conv_layer,layer_size,dense_layer)
                tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))
                model.add(tf.keras.layers.Conv2D(layer_size, (3,3), input_shape= X.shape[1:]))
                model.add(tf.keras.layers.Activation('relu'))
                model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
                for l in range(conv_layer-1):
                    model.add(tf.keras.layers.Conv2D(layer_size, (3,3), input_shape= X.shape[1:]))
                    model.add(tf.keras.layers.Activation('relu'))
                    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))

                model.add(tf.keras.layers.Flatten())
                for _ in range(dense_layer):
                    model.add(tf.keras.layers.Dense(layer_size))
                    model.add(tf.keras.layers.Activation('relu'))
                    model.add(tf.keras.layers.Dropout(0.2))
                model.add(tf.keras.layers.Dense(1))
                model.add(tf.keras.layers.Activation('sigmoid'))
                model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
                model.fit(X,y,batch_size=32,epochs=10,validation_split=0.3,callbacks=[tensorboard])
                dict_acc[NAME] = model.evaluate(X,y)
    print("=====================")
    print("done optimizing...")
    print("======================")
    best_model = max(dict_acc.items(), key=operator.itemgetter(1))[0]
    print("=====================")
    print("best is {}...".format(best_model))
    print("======================")
    conv_layers = [int(best_model.split('-')[0])]
    layer_sizes = [int(best_model.split('-')[2])]
    dense_layers = [int(best_model.split('-')[0])]
    print("=====================")
    print("started training...")
    print("======================")
    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                model = tf.keras.models.Sequential()
                NAME="{}-conv-{}-nodes-{}-dense".format(conv_layer,layer_size,dense_layer)
                tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))
                model.add(tf.keras.layers.Conv2D(layer_size, (3,3), input_shape= X.shape[1:]))
                model.add(tf.keras.layers.Activation('relu'))
                model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
                for l in range(conv_layer-1):
                    model.add(tf.keras.layers.Conv2D(layer_size, (3,3), input_shape= X.shape[1:]))
                    model.add(tf.keras.layers.Activation('relu'))
                    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))

                model.add(tf.keras.layers.Flatten())
                for _ in range(dense_layer):
                    model.add(tf.keras.layers.Dense(layer_size))
                    model.add(tf.keras.layers.Activation('relu'))
                    model.add(tf.keras.layers.Dropout(0.2))
                model.add(tf.keras.layers.Dense(1))
                model.add(tf.keras.layers.Activation('sigmoid'))
                model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
                model.fit(X,y,batch_size=32,epochs=10,validation_split=0.3,callbacks=[tensorboard])
    print("=====================")
    print("done training...")
    print("======================")
    model.save('PP.model')






def process(image):
    image = image.resize((80,80))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image.reshape(-1,80,80,1)

def begintraining(request):
    Model()
    return render(request,'photoeval/testmodel.html')

def follow(request):
    data = request.POST.copy()
    #print(data)
    username = data.get('actname')
    img_count = data.get('imgcount')
    print(username)
    id = get_userID(username)
    follow_id(id)
    messages.success(request,f'{username}')
    return render(request,'photoeval/data.html')

def data(request):
	data = request.POST.copy()
	username = data.get('username')
	#print(data)
	DATADIR= username

	get_data(username,'photoeval', 'tryhardboi',DATADIR)
	print("3MALNA KOL CHY B S7I7 YA ZEBY")
	return render(request,'photoeval/train.html')
def train(request):
	pass
