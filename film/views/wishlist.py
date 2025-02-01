from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from film.models import Wishlist
from film.serializer import WishListModelSerializer


@extend_schema(tags=['wishlist'])
class WishListCreateAPIView(CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListModelSerializer
@extend_schema(tags=['wishlist'])
class WishListDeleteAPIView(DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListModelSerializer
    lookup_field = 'id'
@extend_schema(tags=['wishlist'])
class WishListAPIView(APIView):
    def get(self, request, id):
        try:
            wishlist = Wishlist.objects.filter(user_id=id)
            if not wishlist.exists():
                return Response({"detail": "No wishlist found for this user."}, status=status.HTTP_404_NOT_FOUND)
            serializer = WishListModelSerializer(wishlist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


