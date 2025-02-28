from django.shortcuts import render
from .models import Data

# Create your views here.

def indexpage(request):
    data = Data.objects.using('data').all()
    if request.method == "POST":
        data_post = request.POST
        #user = data.get("user") request.POST.get('selected_id') 
        id = data_post.get("select")
        number = data_post.get("number")
        name = data_post.get("name")
        post_data = [id, number, name]
        upd_profile = Data.objects.using('data').get(id=id)
        upd_profile.name, upd_profile.number = name, number
        upd_profile.save(using='data')
        return render(request, 'index.html', {'data': data, 'post_data': post_data})
    return render(request, 'index.html', {'data': data})

def room(request, room_name):
    return render(request, 'chat/test.html', {
        'room_name': room_name
    })