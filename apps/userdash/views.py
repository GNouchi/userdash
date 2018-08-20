from django.shortcuts import render , redirect
from django.contrib import messages
from .models import *

def logout(request):
    request.session.clear()
    return redirect('/')

def index(request):
    if 'user_id' in request.session: return redirect('/dashboard')
    return render(request, 'index.html')

def register(request):
    if 'user_id' in request.session: return redirect('/dashboard')
    return render(request, 'register.html')

def selfregister(request):
    if 'user_id' in request.session: return redirect('/dashboard')
    if request.method != 'POST': return redirect('/')
    result = User.objects.regValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/register')
    request.session['user_id'] = result['user_id']
    return redirect('/dashboard')

def login(request):
    if 'user_id' in request.session: return redirect('/dashboard')
    return render(request, 'login.html')

def userlogin(request):
    if request.method != 'POST':
        return redirect('/')
    result = User.objects.loginValidator(request.POST)
    try:
        request.session['user_id'] = result['user_id']
        return redirect('/dashboard')
    except:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/login')

def dashboard(request):
    if 'user_id'not in request.session: return redirect('/logout')
    all_users= User.objects.all()
    current_user = User.objects.get(id = request.session['user_id'])
    context = {
        'all_users' : all_users,
        'current_user' : current_user,
    }
    return render(request, 'dashboard.html', context) 

def profile(request):
    if 'user_id'not in request.session: return redirect('/logout')
    current_user = User.objects.get(id = request.session['user_id'])
    context = {
        'current_user' : current_user,
    }
    return render(request, 'profile.html', context)

def updateprofile(request):
    if 'user_id'not in request.session: return redirect('/logout')
    if request.method != 'POST': return redirect('/logout')
    result = User.objects.updateValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/profile')
    return redirect('/profile') 

def wall(request, id):
    if 'user_id'not in request.session: return redirect('/logout')
    wall_owner = User.objects.get(id = id)
    all_messages = Message.objects.all().filter(owner = wall_owner.id)
    all_comments = Comment.objects.all()
    context = {
        'wall_owner' : wall_owner,
        'all_messages' : all_messages,
        'all_comments': all_comments,
    }
    return render(request ,'wall.html', context)

def message(request):
    if request.method != 'POST': return redirect('/logout')
    wall_owner = User.objects.get(id = request.POST['owner_id'])
    author_user = User.objects.get(id = request.POST['author_id'])
    result = Message.objects.create(
        content = request.POST['content'], 
        owner = wall_owner, 
        author = author_user)
    return redirect('/wall/'+str(wall_owner.id))

def comment(request):
    if request.method != 'POST': return redirect('/logout')
    this_message = Message.objects.get(id = request.POST['message_id'])
    author = User.objects.get(id = request.POST['author_id'])
    result = Comment.objects.create(
        content = request.POST['content'], 
        message = this_message,
        author = author)
    print("created     ", result)
    return redirect('/wall/'+str(this_message.owner.id))



# *************************************************************************#
# *************************** admin privies *******************************# 
# *************************************************************************#
def edit(request, id):
    if 'user_id'not in request.session: 
        return redirect('/logout')
    current_user = User.objects.get(id = request.session['user_id'])
    if current_user.user_level != 9:
        return redirect('/dashboard')
        
    edit_user = User.objects.get(id = id)
    context = {
        'edit_user':edit_user
    }
    return render(request, 'edit.html', context) 

def newuser(request):
    if 'user_id'not in request.session: 
        return redirect('/logout')
    current_user = User.objects.get(id = request.session['user_id'])
    if current_user.user_level != 9:
        return redirect('/dashboard')
    return render (request, "newuser.html")

def adminusercreate(request):
    current_user = User.objects.get(id = request.session['user_id'])
    if current_user.user_level != 9:
        return redirect('/dashboard')
    if request.method != 'POST': 
        return redirect('/logout')
    result = User.objects.regValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/newuser')
    messages.error(request, ("Admin created userid" + str(result['user_id'])))
    return redirect('/newuser')

def updateinfo(request):
    if 'user_id'not in request.session: return redirect('/logout')
    current_user = User.objects.get(id = request.session['user_id'])
    if current_user.user_level != 9: return redirect('/dashboard')
    if request.method != 'POST': return redirect('/logout')
    result = User.objects.updateValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/edit/'+request.POST['edit_id'])
    return redirect('/edit/'+request.POST['edit_id']) 

def destroy(request,id):
    current_user = User.objects.get(id = request.session['user_id'])
    if current_user.user_level != 9:
        return redirect('/dashboard')
    rm_user = User.objects.get(id =id )
    messages.error(request, ("Admin destroyed userid" + str(rm_user.id)))
    rm_user.delete()
    return redirect('/dashboard')
