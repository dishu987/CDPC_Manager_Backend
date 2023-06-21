from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .utils.rederers.user import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions.roles import IsHeadPlacementCoordinator,IsSuperUser,IsStudentCoordinator,IsManager
from .models import UserModel,RoleGroup
from django.forms.models import model_to_dict
import datetime
import requests
import os
from .serializers.user import (UserChangePasswordSerializer,UserLoginSerializer,UserPasswordResetSerializer,UserProfileSerializer,UserRegistrationSerializer,SendPasswordResetEmailSerializer)



# Token Generate
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsHeadPlacementCoordinator,IsSuperUser]
  def get(self,request,format=None):
    return Response({'msg':'Byye'}, status=status.HTTP_200_OK)
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)




class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated,IsHeadPlacementCoordinator]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    role = UserModel.objects.get(email=request.user.email).role_group
    role_group = RoleGroup.objects.get(id=role.id).role
    return Response({"profile":serializer.data,"role":role_group}, status=status.HTTP_200_OK)


class UserProfileShowView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    userid = self.request.query_params.get('userid')
    try:
      user = UserModel.objects.get(id=userid)
      return Response(user=user, status=status.HTTP_200_OK)
    except:
      return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
