'''
# api/test_views.py
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Book  # Assuming your Book model is here
from django.contrib.auth.models import User  # For authentication tests

class BookCreateTest(APITestCase):
    def setUp(self):
        self.create_url = reverse('book-list') # Assuming you have a URL named 'book-list'
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
def test_can_create_book(self):
        # What data are we going to send to create a book?
        book_data = {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'publication_date': '1954-07-29'}
        # Simulate making a POST request to our create book endpoint
        response = self.client.post(self.create_url, book_data, format='json') # Note the 'format' argument

        # Now we check if the response is what we expect

        # Check if the status code is 201 (Created) - this means the book was successfully created
        self.assertEqual(response.status_code, 201)

        # Check if the book was actually saved in the database
        self.assertEqual(Book.objects.count(), 1)

        # Check if the data in the response matches what we sent
        self.assertEqual(response.data['title'], 'The Lord of the Rings')
def test_create_book_with_authentication(self):
        self.client.force_authenticate(user=self.user) # Simulate being logged in as 'testuser'
        book_data = {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'publication_date': '1813-01-28'}
        response = self.client.post(self.create_url, book_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().created_by, self.user) # Assuming you have a 'created_by' field
        self.client.force_authenticate(user=None) # Remove authentication for subsequent tests if needed '''

# api/test_views.py
from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import Book, Author  # Make sure to import Author
from django.contrib.auth.models import User
from rest_framework import status

class BookAPITests(APITestCase):
    def setUp(self):
        self.list_create_url = reverse('book-list') # URL for listing and creating books
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # First create Author instances
        self.author1 = Author.objects.create(name='Author A')
        self.author2 = Author.objects.create(name='Author B')
        
        # Then create Book instances with Author objects
        self.book1 = Book.objects.create(
            title='Book 1', 
            author=self.author1,  # Use the Author instance
            publication_year='2023-01-01'
        )
        self.book2 = Book.objects.create(
            title='Book 2', 
            author=self.author2,  # Use the Author instance
            publication_year='2024-02-02'
        )
        
        # Initialize detail_url_pattern after creating books
        self.detail_url_pattern = reverse('book-detail', kwargs={'pk': self.book1.pk})

    def test_can_create_book(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # First create an author or use existing one
        new_author = Author.objects.create(name='New Author')
        
        book_data = {
            'title': 'New Book', 
            'author': new_author.id,  # Send author ID in the request
            'publication_year': '2025-03-03'
        }
        
        response = self.client.post(self.list_create_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Book')
        
        # Log out the user
        self.client.logout()

    def test_can_list_books(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Assuming no pagination

    def test_can_retrieve_book(self):
        detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book 1')

    def test_can_update_book(self):
        self.client.login(username='testuser', password='testpassword')
        detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        
        # For update, you might need to provide all required fields
        updated_data = {
            'title': 'Updated Book 1',
            'author': self.author1.id,  # Include author ID
            'publication_year': '2023-01-01'
        }
        
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book 1')
        self.client.logout()

    def test_can_delete_book(self):
        self.client.login(username='testuser', password='testpassword')
        detail_url = reverse('book-detail', kwargs={'pk': self.book2.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
        self.client.logout()