from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from film.models import Comment
from film.serializer import CommentModelSerializer


@extend_schema(tags=['comment'])
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer

@extend_schema(tags=['comment'])
class FilmCommentListAPIView(APIView):
    def get(self, request, id):
        try:
            comments = Comment.objects.filter(film_id=id)
            if not comments.exists():
                return Response({"detail": "No comments found for this film."}, status=status.HTTP_404_NOT_FOUND)
            serializer = CommentModelSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


