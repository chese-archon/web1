from django.shortcuts import render
from .models import Data

# Create your views here.

def indexpage(request):
    data = Data.objects.using('data').all()#Data.objects.all()
    #print(data[1])
    return render(request, 'index.html', {'data': data})