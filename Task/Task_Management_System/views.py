from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import EditTaskForm, SignupForm, StatusUpdateForm, TaskForm
from .models import Comment, Task
from .utils import send_update_mail, send_update_status

User = get_user_model()


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(
                request,
                "signup.html",
                {"form": form, "error": "Please correct the errors below."},
            )


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("my_dashboard")
        return render(request, "login.html", {"error": "Invalid email or password"})


class MyDashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = User.objects.filter(first_name=request.user).first()
        tasks = Task.objects.filter(Q(assigned_to=request.user) | Q(assigned_by=request.user))
        task_status_count = {
            "Pending": 0,
            "Completed": 0,
        }
        for task in tasks:
            if task.status == "Pending":
                task_status_count["Pending"] += 1
            elif task.status == "Completed":
                task_status_count["Completed"] += 1
        return render(
            request,
            "my_dashboard.html",
            {"tasks": tasks, "task_status_count": task_status_count, "data": data},
        )


class ShowProfileView(LoginRequiredMixin, View):
    def get(self, request):
        data = User.objects.filter(email=request.user.email).first()
        return render(request, "show_profile.html", {"data": data})


class CreateTaskView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        form = TaskForm()
        users = User.objects.all()
        return render(request, "create_task.html", {"form": form, "users": users})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            if send_update_mail(task):
                return redirect("my_dashboard")
            else:
                return render(
                    request,
                    "create_task.html",
                    {"form": form, "error": "Email sending failed. Please try again."},
                )
        else:
            return render(
                request,
                "create_task.html",
                {"form": form, "error": "Please correct the errors below."},
            )


class HomePageView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        task = Task.objects.all()
        return render(request, "my_dashboard.html", {"tasks": task})


class AddCommentView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, task_id):
        task = Task.objects.filter(id=task_id).first()
        return render(request, "add_comment.html", {"task": task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        content = request.POST.get("content")
        if not content.strip():
            return render(request, "add_comment.html", {
                "task": task,
                "error": "Comment content cannot be empty"})
        Comment.objects.create(task=task, user=request.user, comment=content)
        return redirect("my_dashboard")


class ShowDetailView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, "show_detail.html", {"task": task})


class ShowCommentView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        comments = Comment.objects.filter(task=task)
        return render(
            request, "show_comments.html", {"task": task, "comments": comments}
        )


class EditTaskView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = EditTaskForm(instance=task)
        return render(request, "edit_task.html", {"task": task, "form": form})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("my_dashboard")
        return render(request, "edit_task.html", {"form": form, "task": task})


class DeleteTaskView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            task.delete()
            return redirect("my_dashboard")
        except Task.DoesNotExist:
            raise Http404("Task does not exist")


class UpdateStatusView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = StatusUpdateForm(instance=task)
        return render(request, "update_status.html", {'task': task, "form": form})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = StatusUpdateForm(request.POST, instance=task)
        if form.is_valid():
            send_update_status(task)
            form.save()
            return redirect("my_dashboard")
        else:
            print(form.errors)
        return render(request, "update_status.html", {"form": form, "task": task})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("login")
