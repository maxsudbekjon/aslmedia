from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView

from film.models import Actor
from film.serializer import ActorModelSerializer

@extend_schema(tags=['actor'])
class ActorListAPIView(ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorModelSerializer
@extend_schema(tags=['actor'])
class ActorDeleteAPIView(DestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorModelSerializer
    lookup_field = 'id'