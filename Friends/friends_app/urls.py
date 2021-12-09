from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('main', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('friends_list', views.friends_list),
    path('refresh', views.refresh),
    path('profile/<int:user_id>', views.profile),
    path('friend/remove/<int:user_id>', views.remove_friend),
    path('friend/add/<int:user_id>', views.add_as_friend),
    
    path('friends/create', views.add_friend),
    path('delete/<int:id>', views.delete_friend),
]



