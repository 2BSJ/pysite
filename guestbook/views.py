from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def add(request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.content = request.POST['content']

    guestbook.save()

    return HttpResponseRedirect('/guestbook/list')

def list(request):
    guestlist = Guestbook.objects.all().order_by('-regdate')
    data={'guestlist':guestlist}
    return render(request,'guestbook/list.html',data)

def deleteform(request, no=0):
    data ={'no':no}
    return render(request,'guestbook/deleteform.html',data)

def delete(request):
    guestbook = Guestbook.objects.filter(id=request.POST['no']).filter(password=request.POST['password'])
    guestbook.delete()

    return HttpResponseRedirect('/guestbook/list')
