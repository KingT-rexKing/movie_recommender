from django.urls import path
from . import views
from django.urls import include, path
from .views import register_request, login_request, user_home



app_name = "movies"


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_movies, name='search_movies'),
    path('collections/create/', views.create_collection, name='create_collection'),
    path('collections/<int:collection_id>/', views.collection_detail, name='collection_detail'),
    path('collections/<int:collection_id>/add_movie/<int:movie_id>/', views.add_movie_to_collection, name='add_movie_to_collection'),
    path('collections/<int:collection_id>/remove_movie/<int:movie_id>/', views.remove_movie_from_collection, name='remove_movie_from_collection'),
    path('collections/', views.user_collections, name='user_collections'),
    path('home/', views.user_home, name='user_home'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('user_home/', views.user_home, name='user_home'),
]