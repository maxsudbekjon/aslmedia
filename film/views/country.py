from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView

from film.models import Country
from film.serializer import CountryModelSerializer


@extend_schema(tags=['country'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
@extend_schema(tags=['country'])
class CountryDeleteAPIView(DestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
    lookup_field = 'id'