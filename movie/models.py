# Necesitas instalar pillow
from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    # Preguntar diferencia entre CharField y TextField
    description = models.CharField(max_length=250)
    # Dice en dónde se guardarán las imágenes montadas por la gente
    image = models.ImageField(upload_to='movies/images/')
    # Es un campo opcional
    url = models.URLField(blank=True)
    genre = models.CharField(blank=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)

    # le definimos una forma de convertir este objeto a string
    # hicimos algo parecido con Edison, que recuerdos
    def __str__(self):
        return self.title