from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib, io, urllib, base64


def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {"name": "Daniel Santana Meza", "movies": movies, "searchTerm": searchTerm})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, "signup.html", {"email": email})

def statistics_view(request):
    matplotlib.use('Agg')

    # Obtener todas las películas
    all_movies = Movie.objects.all()
    
    # Crear diccionarios para almacenar la cantidad de películas por año y por género
    movie_counts_by_year = {}
    movie_counts_by_genre = {}

    # Filtrar las películas por año y por género
    for movie in all_movies:
        # Contar películas por año
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

        # Contar películas por género (considerando solo el primer género)
        if movie.genre:
            first_genre = movie.genre.split(',')[0]  # Suponiendo que los géneros están separados por comas
            if first_genre in movie_counts_by_genre:
                movie_counts_by_genre[first_genre] += 1
            else:
                movie_counts_by_genre[first_genre] = 1
        else:
            if 'Unknown' in movie_counts_by_genre:
                movie_counts_by_genre['Unknown'] += 1
            else:
                movie_counts_by_genre['Unknown'] = 1

    # Crear la gráfica de barras para la cantidad de películas por año
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(movie_counts_by_year)), movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(range(len(movie_counts_by_year)), movie_counts_by_year.keys(), rotation=90)
    plt.tight_layout()

    # Guardar la primera gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    # Crear la gráfica de barras para la cantidad de películas por género
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(movie_counts_by_genre)), movie_counts_by_genre.values(), width=0.5, align='center', color='orange')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(range(len(movie_counts_by_genre)), movie_counts_by_genre.keys(), rotation=90)
    plt.tight_layout()

    # Guardar la segunda gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')
    
    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})