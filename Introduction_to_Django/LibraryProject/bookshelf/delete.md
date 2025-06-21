

---

### **`delete.md`**
This file documents the **Delete** operation.

```markdown
# Delete Operation

## Command
```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Confirm deletion by retrieving all books
books = Book.objects.all()
print("Books in database:", list(books))
