from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Task

User = get_user_model()


class HomeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='password123')

    def test_home_get(self):
        self.client.login(email='testuser@gmail.com', password='password123')
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class TaskCreationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            assigned_to=self.user,
            assigned_by=self.user,
            start_date="2024-12-01",
            end_date="2024-12-31",
            priority=1,
            status="Pending",
        )

    def test_login_view(self):
        response = self.client.post(
            reverse("login"), {"email": "testuser@example.com", "password": "password123"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("my_dashboard"))

    def test_create_task_view(self):
        self.client.login(email="testuser@example.com", password="password123")
        response = self.client.post(
            reverse("create_task"),
            {
                "title": "New Task",
                "description": "Task description",
                "assigned_to": self.user.id,
                "start_date": "2024-12-01",
                "end_date": "2024-12-31",
                "priority": 1,
                "status": "Pending",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_my_dashboard_view(self):
        self.client.login(email="testuser@example.com", password="password123")
        response = self.client.get(reverse("my_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")


class TaskUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='user@gmail.com', password='user123')
        self.user2 = User.objects.create_user(email='user2@gmail.com', password='user78234')
        self.task = Task.objects.create(
            title='Initial Task',
            priority=1,
            status='pending',
            end_date='2023-12-31',
            assigned_to=self.user2,
            description='Initial Description',
            assigned_by=self.user
        )
        self.client.login(email='user@gmail.com', password='user123')
        self.url = reverse('UpdateTask', args=[self.task.id])

    def test_task_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_status.html')

    def test_task_update_view_post_success(self):
        data = {
            'title': 'Updated Task',
            'priority': 2,
            'status': 'in-progress',
            'end_date': '2023-12-31',
            'assigned_to': self.user2.id,
            'description': 'Updated Description',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.priority, 'high')
        self.assertEqual(self.task.status, 'in-progress')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertRedirects(response, reverse('home_page'))
