from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from .models import Library
from .models import Book

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})
  
class LibraryDetailView(DetailView):
    """
    A class-based view to display details of a specific library and list all books in that library.
    """
    model = Library  # The model to use for the view
    template_name = 'relationship_app/library_detail.html'  # The template to render
    context_object_name = 'library'  # The name of the context variable in the template

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the template.
        """
        # Call the base implementation first to get the default context
        context = super().get_context_data(**kwargs)

        # Add the list of books in the library to the context
        context['books'] = self.object.books.all()  # Access books using the related_name 'books'
        return context
# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)  # Automatically log in the user
                return redirect("home")  # Redirect to home page
        else:
            messages.error(request, "Passwords do not match")

    return render(request,  "relationship_app/register.html")  # Show registration form
    
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Logs the user in
            return redirect("home")  # Redirect to homepage or dashboard
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    
    return render(request, "login.html")

def is_admin(user):
    if user.is_authenticated:
        try:
            return user.userprofile.role == "Admin"
        except UserProfile.DoesNotExist:
            return False
    return False

def is_librarian(user):
    if user.is_authenticated:
        try:
            return user.userprofile.role == 'Librarian'
        except UserProfile.DoesNotExist:
            return False
    return False

def is_member(user):
    if user.is_authenticated:
        try:
            return user.userprofile.role == 'Member'
        except UserProfile.DoesNotExist:
            return False
    return False

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        Book.objects.create(title=title, author=author)
        return redirect('book_list')  # Replace 'book_list'
    return render(request, 'add_book.html')  # Replace 'add_book.html'

@permission_required('relationship_app.can_change_book', raise_exception=True)
def change_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.save()
        return redirect('book_list') #replace book_list
    return render(request, 'change_book.html', {'book': book}) #replace change_book.html

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.delete()
    return redirect('book_list') #replace book_list