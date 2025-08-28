




from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views




urlpatterns = [
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path ('home_genaric/', views.home_genaric, name='home_genaric'),

    
]