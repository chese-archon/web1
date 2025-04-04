from django.shortcuts import render, redirect
from .models import Data
from django.http import JsonResponse
import json

# Create your views here.


def notification_closed(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Окно закрылось:", data)
        print("Окно закрылось: views info")
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid request"}, status=400)

def indexpage(request):
    data = Data.objects.using('data').all()
    if request.method == "POST":
        if "update" in request.POST:
            for i in data:
                i.refresh_from_db() # получает обновление от стороннего изменения бд
            #return redirect('indexpage')
        elif "returnOldValue" in request.POST:
            val = request.POST.get("returnOldValue")
            arr = val.split(" ")
            print(arr)
            print('returnOldValue', val)
            # old_value + ' '+ new_value + ' '+ table + ' ' + column + ' ' + str_id
            if arr[2] == "table1":
                old_value = arr[0]
                new_value = arr[1]
                table = arr[2]
                column = arr[3]
                str_id = arr[4]
                upd_profile = Data.objects.using('data').get(id=str_id)
                #upd_profile.column = 
                setattr(upd_profile, column, old_value)
                upd_profile.save()

        else:
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

#def room(request, room_name):
#    return render(request, 'chat/test.html', {
#        'room_name': room_name
#    })