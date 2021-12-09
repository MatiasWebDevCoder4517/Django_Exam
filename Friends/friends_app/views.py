from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from .models import *
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, "index.html")

def register(request):
    # print(request.POST)
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")

        else:
            request.POST['name']
            request.POST['alias']
            request.POST['email']
            request.POST['date_birth']
            hashed = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt())
            decoded_hash = hashed.decode('utf-8')

            user = User.objects.create(
                name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], date_birth=request.POST['date_birth'], password=decoded_hash)
            request.session['u_id'] = user.id
            messages.success(request, "User successfully added")
            return render(request, "login.html")


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    user_list = User.objects.filter(email=request.POST['email'])
    if not user_list:
        messages.error(request, "Invalid credentials!")
        return render(request, 'login.html')
    user = user_list[0]

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['login'] = True
        request.session['u_id'] = user.id
        request.session['u_email'] = user.email
        request.session['u_name'] = user.name
        request.session['u_alias'] = user.alias

        add_users = User.objects.get(id=request.session['u_id'])
        friend = Friendship.objects.create(friendship=add_users)
        friend.friends_users.add(add_users)

        return render(request, 'success.html')
    else:
        messages.error(request, "Invalid credentials!")
        return render(request, 'login.html')


def logout(request):
    request.session.clear()
    messages.info(request, "Logged out successfully!")
    return redirect('/')

#################################################################################################
def friends_list(request):
    if request.method == 'GET':
        if request.session['login'] == True:
            user = User.objects.get(id=request.session['u_id'])
            data = {
                "all_friends": Friendship.objects.all(),
                "all_users": User.objects.all(),
                "user": user,
            }
            return render(request, "friends_list.html", data)
        else:
            messages.error(request, "Something went wrong, try again later")
            return redirect('/')


def refresh(request):
    if request.method == 'GET':
        if request.session['login'] == True:
            user = User.objects.get(id=request.session['u_id'])
            data = {
                "all_friends": Friendship.objects.all(),
                "all_users": User.objects.all(),
                "user": user,
            }
            return render(request, "friends_list.html", data)
        else:
            messages.error(request, "Something went wrong, try again later")
            return redirect('/')


def profile(request, user_id):
    if request.method == 'GET':
        thisUser = User.objects.get(id=user_id)
        data = {
            "thisUser": thisUser
        }
        return render(request, "view_profile.html", data)

#########################################################################
def add_as_friend(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=request.session['u_id'])
        friendship = Friendship.objects.get(id=user_id)
        friendship.friends_users.add(user)
        friendship.save()
        return redirect('/friends_list')

def remove_friend(request, id):
    if request.method == 'GET':
        user = User.objects.get(id=request.session['u_id'])
        friendship = Friendship.objects.get(id=id)
        friendship.friends_users.remove(user)
        friendship.save()
        return redirect('/friends_list')

#######################################################################################
## TESTING ##
def add_friend(request):
    if request.method == 'GET':
        return render(request, "add_friend.html")
    else:
        errors = Friendship.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/friends/create')

        else:
            if request.method == 'POST':
                request.POST['name']
                user = User.objects.get(id=request.session['u_id'])

                Friendship.objects.create(
                    name=request.POST['name'], friendship=user)

                messages.success(request, "Friend successfully added")
                return redirect('/friends/create')


def delete_friend(request, id):
    obj = get_object_or_404(Friendship, id=id)
    obj.delete()
    messages.success(request, "Friend successfully eliminated")
    return redirect("/friends_list")
## TESTING ##
#######################################################################################
