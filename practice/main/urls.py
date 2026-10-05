from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('tours/', views.tours, name='tours'),
    path('tours/<str:tour_slug>', views.tour_detail, name='tour_detail'),
    path('booking/<str:tour_slug>/<int:schedule_id>/', views.booking, name='booking'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:home'), name='logout'),

]