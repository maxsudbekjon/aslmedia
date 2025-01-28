from rest_framework.fields import ImageField, CharField
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

    class Meta:
        model = Film
        fields = (
            'category', 'name', 'description', 'genre',
            'actor', 'author', 'country', 'year',
            'image', 'translate_year', 'time')

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
    class Meta:
        model=Film
        fields='name','image','year','like_count','dislike_count'
class UpdatePasswordSerializer(Serializer):
    old_password=CharField(max_length=255)
    new_password=CharField(max_length=255)
class FilmListModelSerializer(ModelSerializer):
    class Meta:
        model=Film
        fields='__all__'