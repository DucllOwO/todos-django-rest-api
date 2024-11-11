from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Todo


class TodoAPITests(TestCase):
    def setUp(self):
        # Set up API client and user with token-based authentication
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Sample todo item data
        self.todo_data = {
            'title': 'Test Todo',
            'description': 'This is a test todo item.',
            'completed': False
        }
        self.todo = Todo.objects.create(**self.todo_data)

        # Define URLs for list and detail endpoints
        self.list_url = reverse('todo-list')
        self.detail_url = reverse('todo-detail', kwargs={'pk': self.todo.pk})

    def test_default_pagination(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_custom_page_size(self):
        response = self.client.get(self.list_url, {'page_size': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_invalid_page_request(self):
        response = self.client.get(self.list_url, {'page': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_todo(self):
        # Test creating a new todo item
        new_todo_data = {
            'title': 'New Todo',
            'description': 'This is a new todo item.',
            'completed': False
        }
        response = self.client.post(
            self.list_url, new_todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.latest(
            'id').title, new_todo_data['title'])

    def test_retrieve_todo(self):
        # Test retrieving a single todo item by ID
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.todo_data['title'])

    def test_update_todo(self):
        # Test updating an existing todo item
        updated_data = {
            'title': 'Updated Todo',
            'description': 'This is an updated todo item.',
            'completed': True
        }
        response = self.client.put(
            self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, updated_data['title'])
        self.assertEqual(self.todo.completed, updated_data['completed'])

    def test_delete_todo(self):
        # Test deleting a todo item by ID
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_create_todo_unauthenticated(self):
        # Test that unauthenticated create request fails
        self.client.credentials()  # Remove token for unauthenticated test
        response = self.client.post(
            self.list_url, self.todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_todo_unauthenticated(self):
        # Test that unauthenticated delete request fails
        self.client.credentials()  # Remove token for unauthenticated test
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
