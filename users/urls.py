from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.BBLoginView.as_view(), name='login'),
    path('logout/', views.BBLogoutView.as_view(), name='logout'),

]