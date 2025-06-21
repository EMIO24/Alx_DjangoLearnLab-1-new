# Create Operation

## Command
```python
from bookshelf.models import Book

# Create a new Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year='1949-06-08')

# Output the created book's details
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")
