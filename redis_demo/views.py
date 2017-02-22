from django.shortcuts import render, redirect, reverse
from django_redis import get_redis_connection

r = get_redis_connection('default')


def index(request):
    if request.method == 'GET':
        name = r.get('name').decode('utf-8')
        data = {
            'name': name,
        }
        return render(request, 'redis_demo/index.html', data)
    else:
        name = request.POST['name']
        r.set('name', name)
        return redirect(reverse('redis-demo_index'))