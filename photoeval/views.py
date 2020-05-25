from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from flask import Flask,request,render_template,url_for,flash,redirect,jsonify
from InstagramAPI import InstagramAPI
import os
#import tensorflow as tf
from PIL import Image
import cv2
import base64
import io
#from funcs import *
import pickle

import urllib.request,json
import random


instaApi = InstagramAPI('photoeval', 'tryhardboi')
instaApi.login()






def read_json(path):
	print(path+'.json')
	with open(path+'.json', encoding="utf8",errors='ignore') as f:
		data = json.load(f)
	return data
def like_process(likes):
    global boi
    boi = 0
    new_likes = []
    for like in likes:
        boi += like
        model = boi/len(likes)
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

    for i in json:
        likes.append(i['edge_media_preview_like']['count'])

    new_likes = like_process(likes)

    new_likes.reverse()
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



def get_data(username,me,pwd,DATADIR):
	os.system(f'instagram-scraper {username}  -m 24  -t image --media-metadata -u {me} -p {pwd}')
	training(username,DATADIR)
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
	return redirect('train')
def train(request):
	return render(request,'photoeval/train.html')
