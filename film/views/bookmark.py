from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from film.models import Bookmark
from film.serializer import BookmarkModelSerializer


@extend_schema(tags=['bookmark'])
class BookmarkCreateAPIView(CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkModelSerializer
@extend_schema(tags=['bookmark'])
class BookmarkDeleteAPIView(DestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkModelSerializer
    lookup_field = 'id'
@extend_schema(tags=['bookmark'])
class BookmarkAPIView(APIView):
    def get(self, request, id):
        try:
            bookmark = Bookmark.objects.filter(user_id=id)
            if not bookmark.exists():
                return Response({"detail": "No bookmark found for this user."}, status=status.HTTP_404_NOT_FOUND)
            serializer = BookmarkModelSerializer(bookmark, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
