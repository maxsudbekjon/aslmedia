from rest_framework.fields import ImageField, CharField, IntegerField, SerializerMethodField, BooleanField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, ChoiceField, ListField, Serializer

from film.models import Film, Actor, Author, Genre, Country, FilmImage, FilmQualityVideo, Comment, Wishlist, Bookmark, \
    WatchHistory


class ActorModelSerializer(ModelSerializer):
    class Meta:
        model=Actor
        fields='__all__'
class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'
class GenreModelSerializer(ModelSerializer):
    class Meta:
        model=Genre
        fields='__all__'
class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
class FilmModelSerializer(ModelSerializer):
    genre = ListField(child=IntegerField() )
    actor = ListField(child=IntegerField())
    author = ListField(child=IntegerField())
    country = ListField(child=IntegerField())
    class Meta:
        model = Film
        fields = (
            'category', 'name', 'description', 'genre',
            'actor', 'author', 'country', 'year',
             'translate_year', 'time')
class FilmImageUpdateModelSerializer(ModelSerializer):
    class Meta:
        model=Film
        fields=('image',)
class FilmImageModelSerializer(ModelSerializer):
    class Meta:
        model=FilmImage
        fields='__all__'
class FilmVideoModelSerializer(ModelSerializer):
    class Meta:
        model=FilmQualityVideo
        fields='__all__'

class CommentModelSerializer(ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"
class WishListModelSerializer(ModelSerializer):
    class Meta:
        model=Wishlist
        fields='__all__'

class BookmarkModelSerializer(ModelSerializer):
    class Meta:
        model=Bookmark
        fields='__all__'

class WatchHistoryModelSerializer(ModelSerializer):
    class Meta:
        model=WatchHistory
        fields='__all__'

class WatchFilmSerializer(ModelSerializer):
    star = SerializerMethodField()
    class Meta:
        model=Film
        fields='name','image','year','like_count','dislike_count','star'
    def get_star(self, obj):
        return obj.like_count - obj.dislike_count
class UpdatePasswordSerializer(Serializer):
    old_password=CharField(max_length=255)
    new_password=CharField(max_length=255)
class FilmListModelSerializer(ModelSerializer):
    like=BooleanField(default=False)
    dis_like=BooleanField(default=False)
    class Meta:
        model=Film
        fields='__all__'
class FilmCalendarModelSerializer(ModelSerializer):
    class Meta:
        model=Film
        fields='name','image','year','like_count','dislike_count','translate_year'