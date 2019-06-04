from django.urls import path
from . import views, views_player, views_city
from django.contrib.auth import views as auth_views

app_name = 'subCityList'

urlpatterns = [
    path('', views.homepage, name='homepage'),

    # Player related
    path('player/add/', views_player.player_add, name='player_add'),
    path('player/list/', views_player.player_list, name='player_list'),
    path('player/detail/<int:player_pk>/', views_player.player_detail, name='player_detail'),
    path('player/edit/<int:player_pk>/', views_player.player_edit, name='player_edit'),

    # City related
    path('city/coords/', views_city.city_coords, name='city_coords'),
    path('city/detail/<int:city_pk>/', views_city.city_detail, name='city_detail'),
    path('city/add/<int:player_pk>/', views_city.city_add, name='city_add'),
    path('city/edit/<int:city_pk>/', views_city.city_edit, name='city_edit'),
    path('city/all/', views_city.city_view_all, name='city_view_all'),

    # User related
    path('user/profile/<int:user_pk>/', views.user_profile, name='user_profile'),
    path('user/profile/', views.my_user_profile, name='my_user_profile'),
    path('user/profile/edit', views.edit_user_profile, name='edit_user_profile'),
    path('register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('user/password/', views.change_password, name='change_password'),
]
