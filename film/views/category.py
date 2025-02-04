from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from film.models import Film, WatchHistory, LikeDislike
from film.serializer import WatchHistoryModelSerializer, \
    WatchFilmSerializer, UpdatePasswordSerializer, FilmCalendarModelSerializer, LikeSerializer
from user.models import User


@extend_schema(tags=['tarjima-kinolar'])
class FilmListAPIView(ListAPIView):
    queryset = Film
    serializer_class =WatchFilmSerializer


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
def update_password(request):
    try:
        user = User.objects.get(id=request.user.id)
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





@extend_schema(tags=['film-calendar'])
class FilmCalendarListAPIView(ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmCalendarModelSerializer
@extend_schema(tags=['film-year'])
class FilmByYearApiView(ListAPIView):
    serializer_class = FilmCalendarModelSerializer

    def get_queryset(self):
        year = self.kwargs.get('year')
        return Film.objects.filter(year__year=year)
@extend_schema(tags=['like'],request=LikeSerializer)
class FilmLikeDislikeAPIView(APIView):
    @extend_schema(
        request=LikeSerializer,
        responses={200: LikeSerializer},
        description="Film uchun like/dislike qo'shish yoki o'chirish"
    )
    def post(self, request, id):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            like = serializer.validated_data.get("like")
            dislike = serializer.validated_data.get("dis_like")

            try:
                film = Film.objects.get(id=id)
            except Film.DoesNotExist:
                return Response({"error": "Film topilmadi"}, status=status.HTTP_404_NOT_FOUND)

            user = request.user  # Hozirgi foydalanuvchi
            like_dislike, created = LikeDislike.objects.get_or_create(user=user, film=film)

            if like:
                if like_dislike.is_like is False:
                    film.dislike_count -= 1  # Avval dislike bosgan bo‘lsa, kamaytirish
                if like_dislike.is_like is not True:
                    film.like_count += 1  # Yangi like bosildi
                    like_dislike.is_like = True

            elif dislike:
                if like_dislike.is_like is True:
                    film.like_count -= 1  # Avval like bosgan bo‘lsa, kamaytirish
                if like_dislike.is_like is not False:
                    film.dislike_count += 1  # Yangi dislike bosildi
                    like_dislike.is_like = False

            film.save()
            like_dislike.save()

            return Response({
                "like_count": film.like_count,
                "dislike_count": film.dislike_count
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)