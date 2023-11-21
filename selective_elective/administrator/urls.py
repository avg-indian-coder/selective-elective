from django.urls import path
from . import views
from website import models

app_name = "administrator"

urlpatterns = [
    path('', views.a_login, name="login"),
    path("logout/", views.a_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("allocate/", views.allocate, name="allocate"),
    path("naughty/", views.naughty, name="naughty"),
]