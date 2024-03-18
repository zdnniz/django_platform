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

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')

    datasets = Dataset.objects.all()
    selected_dataset_id = request.GET.get('dataset')

    if selected_dataset_id == "00001":
        try:
            selected_dataset = ImportIEEE.objects.all()
            IS_Fraud = []
            for item in selected_dataset:
                if item.isFraud == 1:
                    IS_Fraud.append(item)
        except Dataset.DoesNotExist:
            messages.error(request, "所选数据集不存在。")

        return render(request, 'home.html', {'datasets': datasets, 'selected_dataset': IS_Fraud})

    if selected_dataset_id == "00002":
        try:
            selected_dataset = ImportIEEE.objects.all()
            IS_Fraud = []
            for item in selected_dataset:
                if item.isFraud == 1:
                    IS_Fraud.append(item)
        except Dataset.DoesNotExist:
            messages.error(request, "所选数据集不存在。")

        return render(request, 'home.html', {'datasets': datasets, 'selected_dataset': IS_Fraud})

    return render(request, 'home.html', {'datasets': datasets, 'selected_dataset': []})

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



