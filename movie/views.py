from django.shortcuts import render
from .models import Movie

# Create your views here.
def home(request):
    # return render(request, 'home.html', {"name": "Daniel Santana Meza"})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {"movies": movies, "searchTerm": searchTerm})

def about(request):
    return render(request, 'about.html')