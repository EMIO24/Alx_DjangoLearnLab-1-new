# advanced_features_and_security/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Article
from .models import Book
from .forms import ExampleForm  # Import your form

def example_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process form data (save to database, send email, etc.)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            print(f"Received Name: {name}, Email: {email}")
            return render(request, 'success.html')  # Redirect or show success message
    else:
        form = ExampleForm()

    return render(request, 'example_template.html', {'form': form})



def book_list(request):
    books = Book.objects.all() # Retrieve all books from the database
    context = {
        'books': books, # Pass the books to the template
    }
    return render(request, 'book_list.html', context)

@login_required
def article_list(request):
    if request.user.has_perm('advanced_features_and_security.can_view'):
        articles = Article.objects.all()
        return render(request, 'article_list.html', {'articles': articles})
    else:
        return HttpResponseForbidden("You do not have permission to view articles.")

@permission_required('advanced_features_and_security.can_create', raise_exception=True)
def article_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Article.objects.create(title=title, content=content)
        return redirect('article_list')
    return render(request, 'article_create.html')

@permission_required('advanced_features_and_security.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
        return redirect('article_list')
    return render(request, 'article_edit.html', {'article': article})

@permission_required('advanced_features_and_security.can_delete', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article_list')

def book_search(request):
    query = request.GET.get('q')
    if query:
        # Use Django's ORM to prevent SQL injection
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

def book_add(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})
# Create your views here.
