from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from .models import Comment, Task

end_date_naive = datetime(2024, 12, 31)
end_date_aware = make_aware(end_date_naive)

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
            title="Initial Task",
            description="Initial Description",
            start_date=datetime.now(),
            end_date=make_aware(datetime(2024, 12, 31)),
            assigned_to=self.user2,
            assigned_by=self.user,
            priority=1,
            status="Pending"
        )
        self.client.login(email='user@gmail.com', password='user123')
        self.url = reverse('update_status', args=[self.task.id])

    def test_task_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_status.html')

    def test_task_update_view_post_success(self):
        data = {
            'title': 'Updated Task',
            'priority': 2,
            'status': 'In Progress',
            'end_date': '2023-12-31',
            'assigned_to': self.user2,
            'description': 'Updated Description',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.priority, 2)
        self.assertEqual(self.task.status, 'In Progress')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertRedirects(response, reverse('my_dashboard'))


class DeleteTaskViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user@gmail.com', password='user123')
        self.user2 = User.objects.create_user(email='user2@gmail.com', password='user78234')
        self.task = Task.objects.create(
            title="Task to be deleted",
            description="Task to be deleted",
            start_date=datetime.now(),
            end_date=make_aware(datetime(2024, 12, 31)),
            assigned_to=self.user2,
            assigned_by=self.user,
            priority=1,
            status="Pending"
        )
        self.client.login(email='user@gmail.com', password='user123')
        self.url = reverse('delete_task', args=[self.task.id])

    def test_delete_task_success(self):
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(Task.objects.count(), 0)
        self.assertRedirects(response, reverse('my_dashboard'))

    def test_delete_task_not_found(self):
        Task.objects.all().delete()
        response = self.client.get(reverse('delete_task', args=[999]))
        self.assertEqual(response.status_code, 404)


class AddCommentViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user@gmail.com', password='user123')
        self.user2 = User.objects.create_user(email='user2@gmail.com', password='user234')
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            start_date=datetime.now(),
            end_date=make_aware(datetime(2024, 12, 31)),
            assigned_to=self.user2,
            assigned_by=self.user,
            priority=1,
            status="Pending"
        )
        self.client.login(email='user@gmail.com', password='user123')
        self.url = reverse('add_comment', args=[self.task.id])

    def test_add_comment_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_comment.html')
        self.assertContains(response, self.task.title)

    def test_add_comment_view_post_success(self):
        data = {'content': 'This is a test comment.'}
        response = self.client.post(self.url, data)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.task, self.task)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.comment, 'This is a test comment.')
        self.assertRedirects(response, reverse('my_dashboard'))

    def test_add_comment_view_post_empty_content(self):
        data = {'content': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertContains(response, "Comment content cannot be empty")

    def test_add_comment_view_post_task_not_found(self):
        url = reverse('add_comment', args=[999])
        response = self.client.post(url, {'content': 'This comment should not work.'})
        self.assertEqual(response.status_code, 404)
