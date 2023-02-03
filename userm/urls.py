from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('register/', views.register, name="register"),
    path('login/', auth_view.LoginView.as_view(template_name='userm/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='userm/logout.html'), name="logout"),
    path('homepage/', views.homepage, name="homepage"),

    path('project1/', views.project1, name="project1"),
    path("project1/result/", views.result),

    path('project2/', views.project2, name="project2"),
    path("project2/resulta/", views.resulta),

    path('project3/', views.project3, name="project3"),
    
    path('project4/', views.project4, name="project4"),

    path('project5/', views.project5, name="project5"),

]
