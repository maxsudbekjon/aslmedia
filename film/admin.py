from django.contrib import admin

from film.models import Film, Actor, Genre, Author, Country, FilmImage, WatchHistory, Bookmark, Wishlist, Comment, \
    FilmQualityVideo


# Register your models here.
admin.site.register(Actor)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Film)
admin.site.register(FilmQualityVideo)
admin.site.register(FilmImage)
admin.site.register(Comment)
admin.site.register(Wishlist)
admin.site.register(Bookmark)
admin.site.register(WatchHistory)


