from django.urls import path

from film.views import  ActorDeleteAPIView,  \
    AuthorDeleteAPIView, GenreDeleteAPIView,  CountryDeleteAPIView, \
    ActorListAPIView, AuthorListAPIView, GenreListAPIView, CountryListAPIView, \
     CommentCreateAPIView, FilmCommentListAPIView, WishListAPIView, \
    WishListDeleteAPIView, WishListCreateAPIView, BookmarkCreateAPIView, BookmarkDeleteAPIView, BookmarkAPIView, \
    PremiereFilmListAPIView, FilmSearchView, HarfSearchAPIView, MostViewedAPIView, LastTranslatedAPIView, \
    update_password, FilmListAPIView, foreign_movies, RussianAPIView, TrailerAPIView, genre_films, \
    SerialAPIView, CartonAPIView, VideoStreamAPIView, FilmDetailAPIView, FilmCalendarListAPIView, FilmByYearApiView,HelloWorld


urlpatterns = [
    path('film/list',FilmListAPIView.as_view()),
    path('film/detail/<int:id>',FilmDetailAPIView.as_view()),
    path('api/videos/<int:pk>/<str:quality>/', VideoStreamAPIView.as_view()),
    path('film/calendar', FilmCalendarListAPIView.as_view()),
    path('film/year/<int:year>/', FilmByYearApiView.as_view(), name='film-by-year'),

]


urlpatterns+=[
    path('actor/list',ActorListAPIView.as_view()),
    path('actor/delete/<int:id>',ActorDeleteAPIView.as_view())
]

urlpatterns+=[
    path('author/list',AuthorListAPIView.as_view()),
    path('author/delete/<int:id>',AuthorDeleteAPIView.as_view())
]

urlpatterns+=[
    path('genre/list',GenreListAPIView.as_view()),
    path('genre/delete/<int:id>',GenreDeleteAPIView.as_view())
]

urlpatterns+=[
    path('country/list',CountryListAPIView.as_view()),
    path('country/delete/<int:id>',CountryDeleteAPIView.as_view())
]


urlpatterns +=[
    path('comment/create',CommentCreateAPIView.as_view()),
    path('comment/film/<int:id>',FilmCommentListAPIView.as_view())
]

urlpatterns +=[
    path('wishlist/create',WishListCreateAPIView.as_view()),
    path('wishlist/user/<int:id>',WishListAPIView.as_view()),
    path('wishlist/delete/<int:id>',WishListDeleteAPIView.as_view())
]


urlpatterns +=[
    path('bookmark/create',BookmarkCreateAPIView.as_view()),
    path('bookmark/user/<int:id>',BookmarkAPIView.as_view()),
    path('bookmark/delete/<int:id>',BookmarkDeleteAPIView.as_view()),

]
urlpatterns +=[

    path('premiere/list',PremiereFilmListAPIView.as_view()),
    path('film/search/<str:name>',FilmSearchView.as_view()),
    path('film/letter/filter/<str:harf>',HarfSearchAPIView.as_view()),
    path('most/viewed',MostViewedAPIView.as_view()),
    path('last/translated',LastTranslatedAPIView.as_view()),
]
urlpatterns +=[

    path('update/password',update_password),

]
urlpatterns +=[

    path('foreign/movies',foreign_movies),
    path('genre/movies/<int:id>',genre_films),

]
urlpatterns +=[

    path('russian/movies',RussianAPIView.as_view()),
    path('serial',SerialAPIView.as_view()),
    # path('game/video',GameAPIView.as_view()),
    path('carton',CartonAPIView.as_view()),
    # path('program/video',ProgramAPIView.as_view()),

]
urlpatterns +=[

    path('trailer/movies',TrailerAPIView.as_view()),

]

urlpatterns +=[
    path('hello', HelloWorld.as_view()),

]