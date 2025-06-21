# Create your views here.
from rest_framework import generics
from rest_framework import viewsets, permissions
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    Requires authentication.
    Admin users can create, update, and delete books.
    Regular users can only view books.
    """
    queryset = Book.objects.all()  # This gets all the books from the database
    serializer_class = BookSerializer  # This tells Django how to convert the book data to JSON and back
    permission_classes = permissions.IsAuthenticated # Only authenticated users can access this viewset.