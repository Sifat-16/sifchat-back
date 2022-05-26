from django.urls import path
from .views import *
from knox.views import LogoutView

urlpatterns = [
    path('register/', RegisterUserApi.as_view()),
    path('login/', LoginUserApi.as_view()),
    path('logout/', LogoutView.as_view()),
    path('update/<int:pk>', UpdateProfileApi.as_view()),
    path('user/<int:pk>', GetUserWithProfile.as_view()),
    path('user/all', GetAllUserWithProfile.as_view()),
    path('mythreads', GetAllMyThreads.as_view()),
    
]
