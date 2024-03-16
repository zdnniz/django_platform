from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('charts/', views.charts_view, name='charts'),
]
