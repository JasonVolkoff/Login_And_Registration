import re
from .models import User, Message, Comment
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

################### Login Methods ###################


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validation(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        request.session['this_user'] = new_user.first_name
        messages.success(request, "You have successfully registered!")
        return redirect('/wall')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['this_user'] = user.first_name
    messages.success(request, "You have successfully logged in!")
    return redirect('/wall')


def logout(request):
    request.session.clear()
    return redirect('/')

################### Wall methods ###################


def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    messages = Message.objects.all()
    context = {
        'messages': messages,
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'wall.html', context)


def post_message(request):
    if request.method == "POST":
        this_user = User.objects.get(id=request.session['user_id'])
        Message.objects.create(
            msg_text=request.POST['message'], poster=this_user)
    return redirect('/wall')


def comment(request, id):
    if request.method == "POST":
        this_user = User.objects.get(id=request.session['user_id'])
        this_message = Message.objects.get(id=id)
        Comment.objects.create(
            comment_text=request.POST['comment'], poster=this_user, wall_message=this_message)
        return redirect('/wall')


def delete(request, id):
    delComment = Comment.objects.get(id=id)
    delComment.delete()
    return redirect('/wall')
