from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from relationship_app.models import Cources

from .serializer import CourcesSerializer


@api_view(["GET"])
def view_cources(request):
    cources = Cources.objects.all()
    serializer = CourcesSerializer(cources, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_course(request):
    data = request.data
    serializer = CourcesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
