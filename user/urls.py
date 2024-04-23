from django.urls import path

from .views import *

urlpatterns = [
    # Profile
    path('profile', own_profile),
    path('<str:username>/profile', user_profile),
    path('profiles', get_profiles),

    # Buddy
    path('<str:user_id>/follow', follow_user),
    path('<str:user_id>/unfollow', unfollow_user),
    path('<str:user_id>/followers', followers_list),
    path('<str:user_id>/following', following_list),

    # Auth
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login', user_login),
    path('register', user_register),
    path('password/reset', password_reset),
    path('password/reset/confirm', password_reset_confirm),
]
