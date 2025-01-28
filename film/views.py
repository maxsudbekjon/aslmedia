import os
from datetime import timedelta
import re
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.http import FileResponse
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from film.models import Film, Actor, Author, Genre, Country, Comment, Wishlist, Bookmark, WatchHistory
from film.serializer import FilmModelSerializer, ActorModelSerializer, AuthorModelSerializer, GenreModelSerializer, \
    CountryModelSerializer, FilmImageModelSerializer, FilmVideoModelSerializer, CommentModelSerializer, \
    WishListModelSerializer, BookmarkModelSerializer, WatchHistoryModelSerializer, \
    WatchFilmSerializer, UpdatePasswordSerializer, FilmListModelSerializer
from user.models import User
from .models import FilmQualityVideo


@extend_schema(tags=['actor'])
class ActorCreateAPIView(CreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorModelSerializer
@extend_schema(tags=['actor'])
class ActorListAPIView(ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorModelSerializer
@extend_schema(tags=['actor'])
class ActorDeleteAPIView(DestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorModelSerializer
    lookup_field = 'id'




@extend_schema(tags=['author'])
class AuthorCreateAPIView(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
@extend_schema(tags=['author'])
class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
@extend_schema(tags=['author'])
class AuthorDeleteAPIView(DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
    lookup_field = 'id'





@extend_schema(tags=['genre'])
class GenreCreateAPIView(CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreModelSerializer
@extend_schema(tags=['genre'])
class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreModelSerializer
@extend_schema(tags=['genre'])
class GenreDeleteAPIView(DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreModelSerializer
    lookup_field = 'id'





@extend_schema(tags=['country'])
class CountryCreateAPIView(CreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
@extend_schema(tags=['country'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
@extend_schema(tags=['country'])
class CountryDeleteAPIView(DestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
    lookup_field = 'id'










@extend_schema(tags=['film'])
class FilmCreateAPIView(CreateAPIView):
    queryset = Film.objects.all()
    serializer_class=FilmModelSerializer
@extend_schema(tags=['tarjima-kinolar'])
class FilmListAPIView(ListAPIView):
    queryset = Film
    serializer_class =WatchFilmSerializer
@extend_schema(tags=['film'])
class FilmImageCreateAPIView(CreateAPIView):
    queryset = Film.objects.all()
    serializer_class=FilmImageModelSerializer
@extend_schema(tags=['film'])
class FilmVideoCreateAPIView(CreateAPIView):
    queryset = Film.objects.all()
    serializer_class=FilmVideoModelSerializer

@extend_schema(tags=['horij'],responses=WatchFilmSerializer)
@api_view(['GET'])
def foreign_movies(request):
    european_countries = [
        'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium',
        'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
        'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece',
        'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia',
        'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco',
        'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal',
        'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain',
        'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City'
    ]
    european_countries_cyrillic = [
        'Албания', 'Андорра', 'Армения', 'Австрия', 'Озарбайжон', 'Беларусь', 'Бельгия',
        'Босния ва Герцеговина', 'Болгария', 'Хорватия', 'Кипр', 'Чехия',
        'Дания', 'Эстония', 'Финляндия', 'Франция', 'Грузия', 'Германия', 'Греция',
        'Венгрия', 'Исландия', 'Ирландия', 'Италия', 'Қозоғистон', 'Косово', 'Латвия',
        'Лихтенштейн', 'Литва', 'Люксембург', 'Мальта', 'Молдова', 'Монако',
        'Черногория', 'Нидерландия', 'Северная Македония', 'Норвегия', 'Польша', 'Португалия',
        'Румыния', 'Россия', 'Сан-Марино', 'Сербия', 'Словакия', 'Словения', 'Испания',
        'Швеция', 'Швейцария', 'Туркия', 'Украина', 'Буюк Британия', 'Ватикан'
    ]
    films=Film.objects.filter(Q(country__films__in=european_countries)|Q(country__films__in=european_countries_cyrillic))
    serializer = WatchFilmSerializer(films, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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



@extend_schema(tags=['watch-history'])
class WatchHistoryCreateAPIView(CreateAPIView):
    queryset = WatchHistory.objects.all()
    serializer_class = WatchHistoryModelSerializer
@extend_schema(tags=['watch-history'])
class WatchHistoryAPIView(APIView):
    def get(self, request, id):
        try:
            watch = WatchHistory.objects.filter(user_id=id)
            if not watch.exists():
                return Response({"detail": "No watch found for this user."}, status=status.HTTP_404_NOT_FOUND)
            serializer = WatchHistoryModelSerializer(watch, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['premiere'])
class PremiereFilmListAPIView(ListAPIView):
    queryset = Film.objects.all()
    serializer_class = WatchFilmSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        today = now().date()
        one_week_ago = today - timedelta(days=7)
        return queryset.filter(translate_year__range=(one_week_ago, today))


@extend_schema(tags=['search'])  # Filmni search orqli qidirish
class FilmSearchView(APIView):
    def get(self, request,name):

        if name:
            films = Film.objects.filter(Q(name__icontains=name) |
                     Q(name__iexact=name) |
                     Q(name__istartswith=name) |
                     Q(name__contains=name) )
        else:
            films = Film.objects.all()

        serializer = WatchFilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
@extend_schema(tags=['filter']) # Filmni harflar bilan filter qilish
class HarfSearchAPIView(APIView):
    def get(self,request,harf):
        if harf:
            harf=harf.lower()
            films=Film.objects.filter(name__startswith=harf)
            serializer = WatchFilmSerializer(films, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Harfda xatolik bor!!'})



@extend_schema(tags=['most-viewed']) # Ko'p marta ko'rilgan
class MostViewedAPIView(APIView):
    def get(self,request):
        films= Film.objects.order_by('-visit_count')
        serializer=WatchFilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@extend_schema(tags=['last-translated']) # So'ngi qo'shilgan
class LastTranslatedAPIView(APIView):
    def get(self,request):
        films= Film.objects.order_by('-translate_year')
        serializer=WatchFilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['update-password'], request=UpdatePasswordSerializer)
@api_view(['POST'])
def update_password(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdatePasswordSerializer(data=request.data)
    if serializer.is_valid():
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not check_password(old_password, user.password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['rus-tilida']) # Rus tilidagi kinolar
class RussianAPIView(APIView):
    def get(self,request):
        films= Film.objects.filter(category='rus')
        serializer=WatchFilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['tez-kunda']) #Tez kunda
class TrailerAPIView(APIView):
    def get(self,request):
        films= Film.objects.filter(category='trailer')
        serializer=WatchFilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['genre'])
@api_view(['GET'])
def genre_films(request,id):
    genre_films=Film.objects.filter(genre__id=id)
    serializer=WatchFilmSerializer(genre_films,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@extend_schema(tags=['year']) # Chiqarilgan yil bo'yicha
class YearAPIView(APIView):
    def get(self,request,year):
        films= Film.objects.filter(year=year)
        serializer=WatchFilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['serial']) # Seriallar
class SerialAPIView(APIView):
    def get(self,request):
        films= Film.objects.filter(category='serial')
        serializer=WatchFilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
@extend_schema(tags=['carton']) # Multfilmalr
class CartonAPIView(APIView):
    def get(self,request):
        films= Film.objects.filter(category='carton')
        serializer=WatchFilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @extend_schema(tags=['program']) # Dasturlar
# class ProgramAPIView(APIView):
#     def get(self,request):
#         films= Film.objects.filter(category='program')
#         serializer=WatchFilmSerializer(films, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
# @extend_schema(tags=['game']) # O'yinlar
# class GameAPIView(APIView):
#     def get(self,request):
#         films= Film.objects.filter(category='game')
#         serializer=WatchFilmSerializer(films, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['film'])
class FilmDetailAPIView(APIView):
    def get(self,request,id):
        film=Film.objects.filter(id=id)
        serializer=FilmListModelSerializer(film,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



@extend_schema(tags=['film'])
class VideoStreamAPIView(APIView):
    def get(self, request, pk, quality):
        # Videoni topamiz
        try:
            video = FilmQualityVideo.objects.get(film_id=pk, quality=quality)
        except FilmQualityVideo.DoesNotExist:
            raise NotFound("Video topilmadi.")

        # Segmentlarni uzatish
        range_header = request.headers.get('Range', None)
        video_path = video.video_file.path

        if range_header:
            # Bo'lib uzatish (Range Header asosida)
            range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)
            if range_match:
                start = int(range_match.group(1))
                end = range_match.group(2)
                end = int(end) if end else os.path.getsize(video_path) - 1

                # Fayldan kerakli bo'lagini o'qish
                with open(video_path, 'rb') as f:
                    f.seek(start)
                    data = f.read(end - start + 1)

                response = FileResponse(data, status=206, content_type='video/mp4')
                response['Content-Range'] = f"bytes {start}-{end}/{os.path.getsize(video_path)}"
                return response

        # To'liq video uzatish
        return FileResponse(open(video_path, 'rb'), content_type='video/mp4')




