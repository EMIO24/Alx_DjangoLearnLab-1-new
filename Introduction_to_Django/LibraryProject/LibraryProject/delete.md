
---

### **`update.md`**
This file documents the **Update** operation.

```markdown
# Update Operation

## Command
```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Output the updated book's details
print(f"Updated book: {book.title} by {book.author}, published in {book.publication_year}")
