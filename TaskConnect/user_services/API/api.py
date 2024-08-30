from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from user_services.API.serializer import *
from user_services.models import *
from rest_framework import generics

class RoleCreateView(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    # def create(self, request, *args, **kwargs):
    #     print(self.__dir__())
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
# class Register

# class SearchAPiView(APIView):
#     def post(self, request):
#         serializers = SearchTaskSerializer(data = request.data)
#         if serializers.is_valid():
#             return Response(serializers.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

