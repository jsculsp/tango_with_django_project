from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('''
        <div>Rango says hey there partner!</div>
        <div><a href='/rango/about/'>About</div>
        ''')

def about(request):
    return HttpResponse('Rango says here is the about page.')
