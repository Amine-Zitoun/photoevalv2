from django.shortcuts import render
from django.http import HttpResponse
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
    data = request.POST.copy()
    username = data.get('actname')
    img_count = data.get('imgcount')
    
    return render(request,'photoeval/start.html')
