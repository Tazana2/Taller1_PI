from django.core.management.base import BaseCommand
from movie.models import Movie
import os, json

class Command(BaseCommand):
    help = "Load movies from movies.json into the Movie model"
    
    def handle(self, *args, **kwargs):
        json_file_path = "movie/management/commands/movies.json"
        
        # Load data from the JSON file
        with open(json_file_path, "r") as file:
            movies = json.load(file)
        
        
        # Create a Movie object for each movie in the JSON file
        for i in range(100):
            movie = movies[i]
            exist = Movie.objects.filter(title=movie['title']).first() # Check if the movie already exists in the database
            
            if not exist:
                Movie.objects.create(
                    title = movie['title'],
                    image = "movie/images/default.jpg",
                    genre = movie['genre'],
                    year = movie['year'],
                )