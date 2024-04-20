from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="/auth/login")
def index(request):
    return render(request, "chat/index.html",{"user":request.user})

@login_required(login_url="/auth/login")
def room(request, room_name):
    # print(room_name)
    return render(request, "chat/room.html", {"room_name": room_name,"user":request.user})

def signgup_view(req):
    if req.method=="POST":
        form=UserCreationForm(req.POST)
        if form.is_valid:
            form.save()
            messages.success(req, 'Account created successfully!')
            return redirect("/")      
        else:
            messages.error("try again")      
    if req.user.is_authenticated:
        return redirect("/")
    else:
       form=UserCreationForm()
       return render(req,"auth/signup.html",{"form":form})
    
def login_view(req):
    if req.method=="POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)
        if user is not None:
         login(req, user)
         redirect("/")
        # Redirect to a success page.
        else:
            return messages(req,"try again")
    
    if req.user.is_authenticated:
        return redirect("/")
    return render(req,"auth/login.html")

def logout_view(req):
    logout(req)
    return redirect("/")