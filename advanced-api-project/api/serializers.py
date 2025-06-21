from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """Serializes Book model fields and validates publication year."""
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """Ensures publication year is not in the future."""
        if value > datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author model fields and nested BookSerializer."""
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books'] #added id
        