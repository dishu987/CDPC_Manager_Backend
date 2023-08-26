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
from .serializers.user import (UserChangePasswordSerializer,UserLoginSerializer,UserPasswordResetSerializer,UserProfileSerializer,UserRegistrationSerializer,SendPasswordResetEmailSerializer,RoleGroupSerializer,UserListSerializer)
from Company.models import Company
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
import pandas as pd
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .permissions.roles import CanAddUsers

UserModel = get_user_model()

def format_datetime(datetime_str):
    # Parse the datetime string
    dt = datetime.fromisoformat(datetime_str)
    # Convert to the current timezone
    dt = dt.astimezone(timezone.get_current_timezone())
    # Format the datetime as a string
    formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime

# Token Generate
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }



class RoleGroupListAPIView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated,IsSuperUser]
  def get(self, request, format=None):
      rolegroups = RoleGroup.objects.all()
      serializer = RoleGroupSerializer(rolegroups, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)



class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated,IsSuperUser]
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
    print(email,password)
    user = authenticate(email=email, password=password)
    if user is not None:
      payload = {
        'role' :user.role_group.role,
        'name' : user.name,
        'email' :user.email,
        'token' :get_tokens_for_user(user),
        'msg':'Login Success',
      }
      return Response(payload, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    role = UserModel.objects.get(email=request.user.email).role_group
    role_group = RoleGroup.objects.get(id=role.id).role
    return Response({"profile":serializer.data,"role":role_group}, status=status.HTTP_200_OK)



class UserListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        role_group = request.query_params.get('role_group')
        if not role_group:
            return Response({"error": "role_group is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            users = UserModel.objects.filter(role_group=role_group)
            serialized_users = UserListSerializer(users, many=True).data
            return Response(serialized_users, status=status.HTTP_200_OK)
        except UserModel.DoesNotExist:
            return Response({"error": "No users found with the given role_group"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileShowView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        userid = self.request.query_params.get('userid')
        print(userid)
        try:
            user = None
            if userid=="my":
              user = request.user
            else:
              user = get_object_or_404(UserModel, id=userid)
            print(user.role_group)
            # if str(user.role_group) == "Student Coordinator":
            company_ids = []
            try:
                companies_assigned = Company.objects.filter(assigned_coordinators=user)
                company_ids.extend(companies_assigned.values_list('id', flat=True))
            except:
                pass
            data = {
                'id':user.id,
                'name': user.name,
                'email': user.email,
                'mobile': user.mobile,
                'gender': user.gender,
                'address':user.address,
                'role_group':  user.role_group.role,
                'date_joined':format_datetime(user.date_joined.isoformat()),
                'created_at': format_datetime(user.created_at.isoformat()),
                'updated_at': format_datetime(user.updated_at.isoformat()),
                'companies_assigned': list(company_ids),
            }
            return Response(data, status=status.HTTP_200_OK)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


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


class StudentCoordinatorBulkCreateAPIView(APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated,CanAddUsers]
    def post(self, request):
        # Get the uploaded file from the request
        file = request.FILES.get('file')
        # Check if a file was provided
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        # Read the Excel file using pandas
        try:
            df = pd.read_excel(file)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        # Iterate over each row in the dataframe and create users
        created_users = []
        for index, row in df.iterrows():
            name = row['Name']
            email = row['Email']
            address = row['Address']
            gender = row['Gender']
            mobile = row['Mobile']
            # Create the user with default password '1234'
            role_group, created = RoleGroup.objects.get_or_create(id=10)
            user = UserModel.objects.create_user(email=email, password='1234',role_group=role_group)
            # Set additional fields
            user.name = name
            user.address = address
            user.gender = gender
            user.mobile = mobile
            # Save the user
            user.save()
            created_users.append({'name': name, 'email': email})
        return JsonResponse({'message': 'Users created successfully', 'created_users': created_users}, status=201)
