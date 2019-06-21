from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def joinform(request):
    return render(request, 'user/joinform.html')

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

def join(request):
    user = User()

    user.name = request.POST['name']
    user.email= request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']

    user.save()
    return HttpResponseRedirect('/user/joinsuccess')

def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):
      results = User.objects. \
                filter(email=request.POST['email']). \
                filter(password=request.POST['password'])

      # 로그인 실패
      if len(results) == 0 :
          return HttpResponseRedirect('/user/loginform?result=fail')

      # 로그인 처리
      authuser = results[0]
      request.session['authuser'] = model_to_dict(authuser)

      return HttpResponseRedirect('/')

def logout(request):
    del request.session['authuser']
    return HttpResponseRedirect('/')

def updateform(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    data = {
        'user' : user
    }
    return render(request, 'user/updateform.html',data)

def update(request):
    #id가 있냐 없냐에따라서 영속객체인지 아닌지 판단
    #그말은 update, insert가 상황에따라 달라진다는 뜻
    user = User.objects.get(id=request.session['authuser']['id'])
    user.name = request.POST['name']
    user.gender = request.POST['gender']
    if request.POST['password'] is not '': # 있냐없냐?
        user.password = request.POST['password']

    user.save()

    request.session['authuser']['name'] = user.name

    return HttpResponseRedirect('/user/updateform?result=success')

def checkemail(request):
    try:
        user = User.objects.get(email=request.GET['email'])
    except Exception as e:
        user = None
    email = request.GET['email']
    result = {
        'result' : 'success',
        'data' : "not exist" if user is None else "exist"
    }
    return JsonResponse(result)





