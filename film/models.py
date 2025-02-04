from django.db.models import IntegerField, FileField, DateField, FloatField

from django.db.models import Model, DateTimeField, BooleanField, TextChoices, CharField, ForeignKey, CASCADE, \
    TextField, ManyToManyField, PositiveIntegerField, DurationField, ImageField

from user.models import User


class Actor(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Country(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name
class Game(Model):
    name = CharField(max_length=255)
    version = FloatField()
    sistema = CharField(max_length=255)
    description = TextField()
    year = DateField()
    image = ImageField(upload_to='game-image/%y/%d')
    created_at = DateTimeField(auto_now_add=True)
    is_active = BooleanField(default=True)
    visit_count = IntegerField(default=0)
    like_count = IntegerField(default=0)
    dislike_count = IntegerField(default=0)
    like = BooleanField(default=False)
    dislike = BooleanField(default=False)
    file = FileField(upload_to='program')
class Program(Model):
    name=CharField(max_length=255)
    version=FloatField()
    sistema=CharField(max_length=255)
    description = TextField()
    year = DateField()
    image = ImageField(upload_to='program-image/%y/%d')
    created_at = DateTimeField(auto_now_add=True)
    is_active = BooleanField(default=True)
    visit_count = IntegerField(default=0)
    like_count = IntegerField(default=0)
    dislike_count = IntegerField(default=0)
    like = BooleanField(default=False)
    dislike = BooleanField(default=False)
    file=FileField(upload_to='program')
class Film(Model):
    class CategoryType(TextChoices):
        MOVIE = 'Movie', 'movie'
        SERIAL = 'Serial', 'serial'
        CARTON = 'Carton', 'carton'
        TRAILER = 'Trailer', 'trailer'
        RUS='Rus','rus'

    category = CharField(max_length=255, choices=CategoryType.choices, default=CategoryType.MOVIE)
    name = CharField(max_length=255)
    description = TextField()
    genre = ManyToManyField('film.Genre', related_name='films')
    actor = ManyToManyField('film.Actor', related_name='films')
    author = ManyToManyField('film.Author', related_name='films')
    country = ManyToManyField('film.Country', related_name='films')
    year = DateField()
    image=ImageField(upload_to='film-image/%y/%d')
    translate_year = DateField()
    time = FloatField()
    created_at = DateTimeField(auto_now_add=True)
    is_active = BooleanField(default=True)
    visit_count = IntegerField(default=0)
    like_count = IntegerField(default=0)
    dislike_count = IntegerField(default=0)
    like = BooleanField(default=False)
    dislike = BooleanField(default=False)

    def __str__(self):
        return self.name


class FilmQualityVideo(Model):
    part = PositiveIntegerField(default=1)
    film = ForeignKey('film.Film', CASCADE)
    quality = CharField(max_length=25)
    video_file = FileField(upload_to='videos/%Y/%d')

    def __str__(self):
        return self.quality


class FilmImage(Model):
    film = ForeignKey('film.Film', CASCADE)
    image = ImageField(upload_to='image/%Y/%d')


class Comment(Model):
    user = ForeignKey('user.User', on_delete=CASCADE, related_name='comments')
    film = ForeignKey('film.Film', on_delete=CASCADE, related_name='comments')
    text = TextField()
    date = DateTimeField(auto_now_add=True)
    like_count = IntegerField(default=0)
    dislike_count = IntegerField(default=0)
    like = BooleanField(default=False)
    dislike = BooleanField(default=False)
    def __str__(self):
        return self.text[:20]


class Wishlist(Model):
    user = ForeignKey('user.User', CASCADE)
    film = ForeignKey('film.Film', CASCADE)


class Bookmark(Model):
    user = ForeignKey('user.User', on_delete=CASCADE, related_name="bookmarks")
    film = ForeignKey('film.Film', on_delete=CASCADE, related_name="bookmarks")

    def __str__(self):
        return self.user.username

class WatchHistory(Model):
    user = ForeignKey('user.User', on_delete=CASCADE, related_name='watch_history')
    film = ForeignKey('film.Film', on_delete=CASCADE, related_name='watched_by_users')
    watched_at = DateTimeField(auto_now_add=True)
class LikeDislike(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    film = ForeignKey(Film, on_delete=CASCADE)
    is_like = BooleanField(null=True)

    class Meta:
        unique_together = ('user', 'film')