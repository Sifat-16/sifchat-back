from cProfile import Profile
from email.mime import image
import os
from requests import request
from rest_framework import status
from django.shortcuts import render
from .serializers import *
from rest_framework import generics, permissions, parsers
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from rest_framework.response import Response
from django.contrib.auth import login
from .models import *
from knox.auth import TokenAuthentication
from django.db.models import Q
from chat.models import *

# Create your views here.


class UpdateProfileApi(generics.GenericAPIView):

    serializer_class = ProfileSerializer

    parser_classes = [parsers.MultiPartParser]

    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get(user=user)

        return Response(
            {
                'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data
            }
        )

    def put(self, request, pk, *args, **kwargs):

        user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get(user=user)

        name = request.data.get('name')
        image = request.data.get('image')
        bio = request.data.get('bio')
        gender = request.data.get('gender')

        if profile.image:
            os.remove(profile.image.path)

        profile.name = name

        # if(profile.image != None):
        #     os.remove(profile.image.path)
        profile.image = image

        profile.bio = bio

        profile.gender = gender

        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(
            serializer.data
        )


class RegisterUserApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = UserProfile.objects.get(user=user)
        return Response(
            {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'pk': user.id,
                'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data,
                'token': AuthToken.objects.create(user)[1]
            }
        )


class LoginUserApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        try:
            profile = UserProfile.objects.get(user=user)
            return Response(
                {
                    "user": UserSerializer(user, context=self.get_serializer_context()).data,
                    "profile": ProfileSerializer(profile, context=self.get_serializer_context()).data,
                    "token": AuthToken.objects.create(user)[1]
                }
            )
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "profile": "Invalid credentials"
                }
            )


class GetUserWithProfile(generics.GenericAPIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        profile = UserProfile.objects.get(user=user)

        return Response(
            {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data,

            }
        )


class GetAllUserWithProfile(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileWithUser

    def get_queryset(self):

        return UserProfile.objects.exclude(user=self.request.user)


class GetAllMyThreads(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ThreadSerializer

    def get(self, request):
        mthreads = MyThread.objects.filter(
            Q(first__user=self.request.user) | Q(second__user=self.request.user))

        return Response(ThreadSerializer(mthreads, many=True).data)


