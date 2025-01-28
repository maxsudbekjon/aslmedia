from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from user.serializer import UserModelSerializer, UserContinueModelSerializer, UserDeleteModelSerializer, \
    UserLoginSerializer

from user.models import User


# Create your views here.
@extend_schema(tags=['register'])
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
# @extend_schema(
#     tags=['register'],
#     request=UserContinueModelSerializer,
#     responses={200: {"message": "success"}}
# )
# class UserCreateContinueUpdateAPIView(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserContinueModelSerializer
#     lookup_field='id'


@extend_schema(
    tags=['register'],
    request=UserContinueModelSerializer,

    responses={200: {"message": "success"}},


)
@api_view(['PATCH'])
def user_register_continue(request, id):

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    serializer = UserContinueModelSerializer(data=request.data, instance=user, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "success"}, status=200)
    return Response(serializer.errors, status=400)

@extend_schema(tags=['register'])
class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteModelSerializer
    lookup_field = 'id'
@extend_schema(tags=['login'],request=UserLoginSerializer,responses={200: {"message": "success"}})
@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)
    else:
        return JsonResponse({"error": "Invalid data"}, status=400)


