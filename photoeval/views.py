from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from flask import Flask,request,render_template,url_for,flash,redirect,jsonify
from InstagramAPI import InstagramAPI
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

def get_userID(username):
	instaApi.searchUsername(username)
	print(instaApi.LastJson["user"])
	try:
		return instaApi.LastJson["user"]["pk"]
	except Exception:
		print("username doesn't exist")
		return False



def follow_id(id):
    instaApi.follow(id)




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
    #messages.success(request,'We sent your a follow request please accept the request before proceeding')
    return render(request,'photoeval/data.html')
