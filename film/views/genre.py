from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response

from film.models import Film, Genre
from film.serializer import GenreModelSerializer, \
    WatchFilmSerializer



@extend_schema(tags=['genre'])
class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreModelSerializer
@extend_schema(tags=['genre'])
class GenreDeleteAPIView(DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreModelSerializer
    lookup_field = 'id'
@extend_schema(tags=['genre'])
@api_view(['GET'])
def genre_films(request,id):
    genre_films=Film.objects.filter(genre__id=id)
    serializer=WatchFilmSerializer(genre_films,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

