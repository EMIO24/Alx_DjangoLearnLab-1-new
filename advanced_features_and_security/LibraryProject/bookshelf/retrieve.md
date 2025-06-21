
---

### **`retrieve.md`**
This file documents the **Retrieve** operation.

```markdown
# Retrieve Operation

## Command
```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Output the book's details
print(f"Book details: {book.title} by {book.author}, published in {book.publication_year}")
