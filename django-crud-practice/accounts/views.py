from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.


def index(request):
    return render(request, "indexx.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            print("username already exists")
            return redirect("/register/")
        user = User(
            username=username,
            password=make_password(request.POST.get("password")),
        )
        user.save()
        return redirect("accounts/login/")

        # User.objects.create(
        # name = name,
        # username = username,
        # password = password,
        # )

    else:
        return render(request, "register.html")


def login_user(request):
    # import pdb; pdb.set_trace()
    if request.method == "POST":
        usernam = request.POST["username"]
        if User.objects.filter(username=usernam).exists():
            obj = User.objects.get(username=usernam)
            old_password = obj.password
            password = request.POST.get("password")
            if check_password(password, old_password):
                login(request, obj)
                return redirect("/accounts/")
            else:
                return HttpResponse("Invalid password")
        else:
            return HttpResponse("User not Found")

    else:
        return render(request, "login.html")


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login")
    else:
        return HttpResponse("User Not Authenticated")
