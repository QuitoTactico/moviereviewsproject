from django.shortcuts import render
from django.http import HttpResponse

#gráficos
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html', {'name':'Esteban Vergara Giraldo'})

    #Trae el valor del input con name="searchMovie"
    searchTerm = request.GET.get('searchMovie')

    # SELECT * FROM Movie
    # movies = Movie.objects.all()

    # SELECT * FROM Movie WHERE title LIKE '%searchTerm%'
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {'name': 'Esteban Vergara Giraldo','searchTerm' : searchTerm,'movies':movies})


def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


# SUPER ÚTIL PARA ANÁLISIS NUMÉRICO
def statistics_view(request):
    matplotlib.use('Agg')
    # Obtiene todos los años de las películas
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')


    # Obtiene todos los géneros de las películas, pero no el primero
    #genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    
    #diccionario para almacenar el conteo de películas por año
    movie_counts_by_year = {}
    movie_counts_by_genre = {}

    # Cuenta las películas por año
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = 'None'

        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    # Tocó de esta forma

    movies = Movie.objects.all()

    for movie in movies:
        first_genre = movie.genre.split(",")[0].strip()
        
        if first_genre not in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] = 0
        movie_counts_by_genre[first_genre] += 1
    '''
    for genre in genres:
        if genre:
            movies_in_genre = Movie.objects.filter(genre=genre)
        else:
            movies_in_genre = Movie.objects.filter(genre__isnull=True)
            genre = 'None'

        count = movies_in_genre.count()
        movie_counts_by_genre[genre] = count
    '''

    bar_width = 0.5
    bar_spacing = 0.5  # de hecho nunca se usó XD
    bar_positions_year = range(len(movie_counts_by_year)) # Posiciones
    bar_positions_genre = range(len(movie_counts_by_genre))

    # Tuve que usar subplots               10, 10
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfica de películas por año
    axs[0].bar(bar_positions_year, movie_counts_by_year.values(), bar_width, align='center')
    axs[0].set_title('Movies per Year')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Number of Movies')
    axs[0].set_xticks(bar_positions_year)
    axs[0].set_xticklabels(movie_counts_by_year.keys(), rotation=90)

    # Gráfica de películas por género
    axs[1].bar(bar_positions_genre, movie_counts_by_genre.values(), bar_width, align='center')
    axs[1].set_title('Movies per Genre')
    axs[1].set_xlabel('Genre')
    axs[1].set_ylabel('Number of Movies')
    axs[1].set_xticks(bar_positions_genre)
    axs[1].set_xticklabels(movie_counts_by_genre.keys(), rotation=90)

    plt.tight_layout()

    '''
    plt.bar(bar_positions, movie_counts_by_year.values(), bar_width, align='center')
    
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # espaciado entre barras
    plt.subplots_adjust(bottom=0.3)
    '''

    # Guardar la imagen en un buffer (BytesIO)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Codificar la imagen en base64, parece que es necesario
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Y ya te deja renderizarlo
    return render(request, 'statistics.html', {'graphic': graphic})


