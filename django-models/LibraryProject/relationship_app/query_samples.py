import django
import os

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """Query all books by a specific author."""
    author = Author.objects.get(name=author_name)  # Get the Author instance
    books = Book.objects.filter(author=author)  # Query books by this author
    return books

def query_books_in_library(library_name):
    """List all books in a specific library."""
    Library.objects.get(name=library_name).books.all()
    return books

def query_librarian_for_library(library_name):
    """Retrieve the librarian for a specific library."""
    librarian = Librarian.objects.get(library=)
    return librarian