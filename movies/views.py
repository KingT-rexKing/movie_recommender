from django.shortcuts import render
from .models import Movie
from .models import Collection
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse


from django.contrib.auth import login, authenticate




def home(request):
    movies = Movie.objects.all()[:10]  # 仅获取10部最新的电影
    return render(request, 'home.html', {'movies': movies})


def search_movies(request): #搜索电影
    query = request.GET.get('query', '')
    movies = Movie.objects.filter(title__icontains=query)
    return render(request, 'search.html', {'movies': movies})


@login_required
def create_collection(request): #创建收藏夹
    if request.method == 'POST':
        name = request.POST.get('name', '')
        collection = Collection.objects.create(name=name, user=request.user)
        return redirect('collection_detail', collection_id=collection.id)

    return render(request, 'create_collection.html')

@login_required
def collection_detail(request, collection_id): #收藏夹详情
    collection = get_object_or_404(Collection, id=collection_id)
    if collection.user != request.user:
        return HttpResponseForbidden()
    return render(request, 'collection_detail.html', {'collection': collection})

@login_required
def add_movie_to_collection(request, collection_id, movie_id): #添加电影到收藏夹
    collection = get_object_or_404(Collection, id=collection_id)
    movie = get_object_or_404(Movie, id=movie_id)
    if collection.user != request.user:
        return HttpResponseForbidden()
    collection.movies.add(movie)
    return redirect('collection_detail', collection_id=collection.id)

@login_required
def remove_movie_from_collection(request, collection_id, movie_id): #删除收藏夹中的电影
    collection = get_object_or_404(Collection, id=collection_id)
    movie = get_object_or_404(Movie, id=movie_id)
    if collection.user != request.user:
        return HttpResponseForbidden()
    collection.movies.remove(movie)
    return redirect('collection_detail', collection_id=collection.id)

@login_required
def user_collections(request): #个人收藏夹
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'user_collections.html', {'collections': collections})

@login_required #个人主页
def user_home(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'user_home.html', {'collections': collections})

def movie_detail(request, movie_id): #电影详情页
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

def register_request(request): #注册
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("movies:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request): #登录
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('movies:home')  
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request = request,
                  template_name = "login.html",
                  context={"form":form})

               
from .views import user_home


