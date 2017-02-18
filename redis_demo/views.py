from django.shortcuts import render

def index(request):
    return render(request, 'redis_demo/index.html', context={})