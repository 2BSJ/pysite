from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board


def list(request):
    page = request.GET.get('page')
    if page is None:
        page = 1
    else :
        page = int(page)
    start = (page-1) * 10
    #여러개 정렬하기 order_by('','','') -은 desc 없이 asc
    boardlist = Board.objects.all().order_by('-groupno','orderno')[start:start+10]
    listcount = Board.objects.count()
    data={
        'boardlist':boardlist,
        'page':page,
        'listcount': listcount
    }
    return render(request,'board/list.html',data)

def gowrite(request):
    return render(request,'board/write.html')


def write(request):
   # update board set order_no = order_no + 1
   # where group_no = {groupNo} and order_no !=0 and depth = {depth}+1

    board = Board()
    if request.POST['new'] == 'True':  # 그냥 리스트에서 새 글 쓸떄
        value = Board.objects.aggregate(max_groupno=Max('groupno'))
        max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]

        board.title = request.POST['title']
        board.content = request.POST['content']
        board.hit = 0
        board.groupno = max_groupno+1
        board.orderno = 0
        board.depth = 0
        board.user_id = request.session['authuser']['id']

    else: # 답글 쓸때
        value = Board.objects.filter(id=request.POST['id'])
        Board.objects.filter(orderno__gte=value[0].orderno + 1).update(orderno=F('orderno') + 1)

        board.groupno = value[0].groupno
        board.orderno = value[0].orderno + 1
        board.depth = value[0].depth + 1

        board.title = request.POST['title']
        board.content = request.POST['content']
        board.hit = 0
        board.groupno = request.POST['groupno']
        board.orderno = int(request.POST['orderno'])+1
        board.depth = int(request.POST['depth'])+1
        board.user_id = request.session['authuser']['id']


    board.save()


    return HttpResponseRedirect('/board/list')
#    board.save()

def view(request):

    board = Board.objects.get(id=request.GET['id'])
    board.hit +=1
    board.save()
    data = {
        'board':board
    }
    return render(request,'board/view.html',data)

def gomodify(request):

    board = Board.objects.get(id=request.GET['id'])
    data = {
        'board': board
    }
    return render(request,'board/modify.html',data)

def modify(request):
    board = Board.objects.get(id=request.POST['id'])
    board.title = request.POST['title']
    board.content = request.POST['content']

    board.save()

    return HttpResponseRedirect('/board/list')

def goreply(request):
    board = Board.objects.get(id=request.GET['id'])
    data = {
        'board' : board
    }
    return render(request, 'board/write.html',data)

    # reply view로 갔을때 수정!

def reply(request):

    #reply method 수정해야됨
    value = Board.objects.aggregate(max_groupno=Max('groupno'))
    max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]
    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.hit = 0
    board.groupno = max_groupno+1
    board.orderno = 1
    board.depth = 1
    board.user_id = request.session['authuser']['id']
    board.save()

    return HttpResponseRedirect('/board/list')

def delete(request):
    board = Board.objects.get(id=request.GET['id'])
    board.delete()
    return HttpResponseRedirect('/board/list')

def search(request):
    page = request.GET.get('page')
    search = request.GET.get('search')
    if page is None:
        page = 1
    else :
        page = int(page)

    start = (page-1) * 10


    if search: # 검색어 있을때
        boardlist = Board.objects.all().filter(title__icontains=search).order_by('-groupno','orderno')[start:start+10]
        listcount = Board.objects.all().filter(title__icontains=search).count()
        data = {
            'boardlist': boardlist,
            'page': page,
            'listcount': listcount,
            'search':search
        }
    else: # 검색어 없을때
        boardlist = Board.objects.all()[start:start+10]
        listcount = Board.objects.count()
        data = {
            'boardlist': boardlist,
            'page': page,
            'listcount': listcount,
            'search': search
        }

    return render(request,'board/list.html',data)


