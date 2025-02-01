
import os
import re

from django.db.models import ExpressionWrapper, F, IntegerField
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from film.models import Film, FilmQualityVideo
from film.serializer import FilmModelSerializer, FilmListModelSerializer, WatchFilmSerializer


@extend_schema(tags=['film'])
class FilmDetailAPIView(APIView):
    def get(self, request, id):
        film = get_object_or_404(Film, id=id)  # Filmni olib kelamiz yoki 404 qaytaramiz
        film.visit_count += 1  # visit_count ni oshiramiz
        film.save(update_fields=['visit_count'])  # Faqat visit_count maydonini yangilaymiz

        serializer = FilmListModelSerializer(film)  # `many=True` kerak emas, chunki bitta obyekt

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        film = get_object_or_404(Film, id=id)
        action = request.data.get("action")  # "like" yoki "dislike" keladi

        if action == "like":
            if film.like:  # Agar avval like bosilgan bo‘lsa, olib tashlaymiz
                film.like = False
                film.like_count -= 1
            else:
                film.like = True
                film.like_count += 1
                film.dis_like = False  # Dislike bo‘lsa, uni olib tashlaymiz
                film.dislike_count = max(0, film.dislike_count - 1)

        elif action == "dislike":
            if film.dis_like:  # Agar avval dislike bosilgan bo‘lsa, olib tashlaymiz
                film.dis_like = False
                film.dislike_count -= 1
            else:
                film.dis_like = True
                film.dislike_count += 1
                film.like = False  # Like bo‘lsa, uni olib tashlaymiz
                film.like_count = max(0, film.like_count - 1)

        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        film.save(update_fields=["like", "dis_like", "like_count", "dislike_count"])
        serializer = FilmListModelSerializer(film)
        return Response(serializer.data, status=status.HTTP_200_OK)
@extend_schema(tags=['film'])
class Top100FilmsAPIView(APIView):
    def get(self, request):
        films = (
            Film.objects.filter(is_active=True)
            .annotate(
                rating=ExpressionWrapper(F("like_count") - F("dislike_count"), output_field=IntegerField())
            )
            .order_by("-rating")[:100]
        )
        serializer = WatchFilmSerializer(films, many=True)
        return Response(serializer.data)

@extend_schema(tags=['film'])
class VideoStreamAPIView(APIView):
    def get(self, request, pk, quality):
        try:
            video = FilmQualityVideo.objects.get(film_id=pk, quality=quality)
        except FilmQualityVideo.DoesNotExist:
            raise NotFound("Video topilmadi.")

        range_header = request.headers.get('Range', None)
        video_path = video.video_file.path

        if range_header:

            range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)
            if range_match:
                start = int(range_match.group(1))
                end = range_match.group(2)
                end = int(end) if end else os.path.getsize(video_path) - 1

                with open(video_path, 'rb') as f:
                    f.seek(start)
                    data = f.read(end - start + 1)

                response = FileResponse(data, status=206, content_type='video/mp4')
                response['Content-Range'] = f"bytes {start}-{end}/{os.path.getsize(video_path)}"
                return response

        return FileResponse(open(video_path, 'rb'), content_type='video/mp4')


class HelloWorld(APIView):
    def get(self , request):
        return Response({"message" : "Hello world"})