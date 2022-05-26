from django.urls import path, re_path
from .consumers import *

websocket_urlpatterns = [
    path('ws/sif-socket-server/<str:fromusername>/<str:tousername>/',
         ChatConsumer.as_asgi()),

]
