from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from pyecharts.charts import Pie, Bar

from .forms import RegisterForm
from .models import *

from .GCN_pytorch.test import train_dominant
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
        selected_dataset = ImportIEEE.objects.filter(isFraud=1)

        return render(request, 'home.html', {'datasets': datasets, 'selected_dataset': selected_dataset})

    elif selected_dataset_id == "00002":
        try:
            import argparse

            dataset_name = 'BlogCatalog'
            hidden_dim = 64
            epoch = 100
            lr = 5e-3
            dropout = 0.3
            alpha = 0.8
            device = 'cpu'

            fake_args = argparse.Namespace(
                dataset=dataset_name,
                hidden_dim=hidden_dim,
                epoch=epoch,
                lr=lr,
                dropout=dropout,
                alpha=alpha,
                device=device
            )

            train_dominant(fake_args)

            gcn_dataset = train_dominant(fake_args)

            n = len(gcn_dataset)
            gcn_label = ['labels'] * n

            # select_dataset = dict(zip(gcn_label, gcn_dataset))
            select_dataset = gcn_dataset.tolist()

        except Dataset.DoesNotExist:
            messages.error(request, "所选数据集不存在。")

        return render(request, 'home.html', {'datasets': datasets, 'select_dataset': select_dataset})

    else:
        selected_dataset = ImportIEEE.objects.none()

    return render(request, 'home.html', {'datasets': datasets, 'selected_dataset': selected_dataset})


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

        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def charts_view(request):
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



