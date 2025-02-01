from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView

from film.models import Author
from film.serializer import AuthorModelSerializer


@extend_schema(tags=['author'])
class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
@extend_schema(tags=['author'])
class AuthorDeleteAPIView(DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
    lookup_field = 'id'
