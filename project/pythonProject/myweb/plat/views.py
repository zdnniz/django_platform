from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm
from .models import *
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
        datasets = Dataset.objects.all()

        fraud_data = []
        if request.method == 'POST':
            print("1")
            dataset_name = request.POST.get['DatasetName']
            if datasets.DatasetName == dataset_name:
                model = ImportIEEE.objects.filter()

            for item in model:
                if item.isFraud == 1:
                    fraud_data.append(item)

            return render(request, 'home.html', {'fraud_data': fraud_data})

        return render(request, 'home.html', {'datasets': datasets})

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
    from pyecharts.charts import Pie, Bar
    from pyecharts import options as opts

    model = ImportIEEE.objects.filter()

    fraud_number = 0
    IS_F = []

    for item in model:
        if item.isFraud == 1: fraud_number += 1
        IS_F = [fraud_number, 50 - fraud_number]

    T_ID = ['FRAUD', 'NOT_FRAUD']

    pie = Pie()
    pie.add('IS_FRAUD', [list(pi) for pi in zip(T_ID, IS_F)])

    pie.render('/home/z/PycharmProjects/django_platform/project/pythonProject/myweb/plat/templates/plat/pie.html')

    return render(request, 'pie.html')



