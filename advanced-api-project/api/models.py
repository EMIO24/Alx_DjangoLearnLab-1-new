# Create your models here.
from django.db import models

# Represents an author with a name.
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Represents a book with a title, publication year, and author.
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
    