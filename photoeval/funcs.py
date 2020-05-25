from django.shortcuts import render
from django.http import HttpResponse
from flask import Flask,request,render_template,url_for,flash,redirect,jsonify
from InstagramAPI import InstagramAPI
#import tensorflow as tf
from PIL import Image
import cv2
import base64
import io
import pickle

from InstagramAPI import InstagramAPI
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



def follow(id):
    instaApi.follow(id)
