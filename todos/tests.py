from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Todo
from .pagination import TodoPagination


class TodoAPITestCase(APITestCase):

    def setUp(self):
        # Create a user and obtain a token for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.list_url = reverse('todo-list')

    def test_create_todo_valid_data(self):
        data = {'title': 'Test Todo', 'description': 'Test Description'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.get().title, 'Test Todo')

    def test_create_todo_missing_fields(self):
        data = {'title': ''}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_todo_invalid_data(self):
        # description should be a string
        data = {'title': 'Test Todo', 'description': True}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_todos(self):
        Todo.objects.create(title='Todo 1', description='Description 1')
        Todo.objects.create(title='Todo 2', description='Description 2')
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_todo_valid_id(self):
        todo = Todo.objects.create(title='Todo 1', description='Description 1')
        url = reverse('todo-detail', args=[todo.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Todo 1')

    def test_retrieve_todo_invalid_id(self):
        url = reverse('todo-detail', args=[999])  # Assuming 999 does not exist
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_todo_valid_data(self):
        todo = Todo.objects.create(title='Todo 1', description='Description 1')
        url = reverse('todo-detail', args=[todo.id])
        data = {'title': 'Updated Todo', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Todo')

    def test_update_todo_partial(self):
        todo = Todo.objects.create(title='Todo 1', description='Description 1')
        url = reverse('todo-detail', args=[todo.id])
        data = {'description': 'Partially Updated Description'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertEqual(todo.description, 'Partially Updated Description')

    def test_update_todo_invalid_id(self):
        data = {'title': 'Updated Todo', 'description': 'Updated Description'}
        url = reverse('todo-detail', args=[999])  # Assuming 999 does not exist
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo_valid_id(self):
        todo = Todo.objects.create(title='Todo 1', description='Description 1')
        url = reverse('todo-detail', args=[todo.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_delete_todo_invalid_id(self):
        url = reverse('todo-detail', args=[999])  # Assuming 999 does not exist
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pagination(self):
        for i in range(15):
            Todo.objects.create(
                title=f'Todo {i}', description=f'Description {i}')
        response = self.client.get(self.list_url, {'page': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']), TodoPagination.page_size)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
