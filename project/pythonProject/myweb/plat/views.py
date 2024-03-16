from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm

from pyecharts.charts import Bar
# Create your views here.

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
		# Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, "OUT")
    print("out")
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect('home')
        
    else:
        form = RegisterForm()
        
        return render(request, 'register.html', {'form':form})
        
    return render(request, 'register.html', {'form':form})

def charts_view(request):
    bar = Bar()
    bar.add_xaxis(["1", "2", "3"])
    bar.add_yaxis("a", [1, 2, 3])
    bar.render('/home/z/PycharmProjects/django_platform/project/pythonProject/myweb/plat/templates/plat/charts.html')
    return render(request, 'charts.html')