from django.shortcuts import render, redirect, reverse
from django.core.cache import cache

def index(request):
    if request.method == 'GET':
        name = cache.get('name')
        data = {
            'name': name,
        }
        return render(request, 'redis_demo/index.html', data)
    else:
        name = request.POST['name']
        cache.set('name', name)
        return redirect(reverse('redis-demo_index'))