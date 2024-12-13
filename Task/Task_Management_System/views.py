import re

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import TaskForm
from .models import Comment, Task

User = get_user_model()


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            errors = {}

            if not username.isalpha():
                errors["username"] = "Username must contain only characters."

            if User.objects.filter(email=email).exists():
                errors["email"] = "Email is already registered."

            if "@" not in email or "." not in email:
                errors["email"] = "Enter a valid email address."

            if len(password) < 5:
                errors["password"] = "Password must be at least 5 characters."

            if not re.search(r"[!@#$%^&*|<>,(){}]", password):
                errors["password"] = "Password must contain at least one special character."

            if errors:
                return render(request, "signup.html", {"errors": errors})

            user = User(first_name=username, email=email)
            user.set_password(password)
            user.save()

            return redirect("login")
        except IntegrityError as e:
            return render(request, 'signup.html', {'error': 'Email or Username already exists.', 'details': str(e)})
        except Exception as e:
            return render(request, 'signup.html', {'error': 'An error occurred', 'details': str(e)})


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('home_page')
        return render(request, 'login.html', {'error': 'Invalid email or password'})


class My_Dashboard(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = get_object_or_404(User, first_name=request.user)
        tasks = Task.objects.filter(assigned_to=request.user)
        print('Username:', data)
        print("TASKS:", tasks)
        task_status_count = {
            'Pending': 0,
            'Completed': 0,
        }
        for task in tasks:
            if task.status == 'Pending':
                task_status_count['Pending'] += 1
            elif task.status == 'Completed':
                task_status_count['Completed'] += 1
        return render(request, 'my_dashboard.html', {'tasks': tasks, 'task_status_count': task_status_count, 'data': data})


class Show_Profile(LoginRequiredMixin, View):
    def get(self, request):
        data = get_object_or_404(User, email=request.user.email)
        return render(request, 'show_profile.html', {'data': data})


class Create_Task(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = TaskForm()
        users = User.objects.all()
        return render(request, 'create_task.html', {'form': form, 'users': users})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            assigned_to = form.cleaned_data['assigned_to']
            assigned_by = request.user
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            priority = form.cleaned_data['priority']
            status = form.cleaned_data['status']

            Task.objects.create(
                title=title,
                description=description,
                assigned_to=assigned_to,
                assigned_by=assigned_by,
                start_date=start_date,
                end_date=end_date,
                priority=priority,
                status=status,
            )
            subject = 'Task Assigned'
            message = f'''Task : {title},
                        Description: {description},
                        Assigned By: {assigned_by},
                        Priority: {priority}
                        Start Date: {start_date},
                        End Date: {end_date}
            '''
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [assigned_to.email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('home_page')
        else:
            return render(request, 'create_task.html', {"form": form, "error": 'Please correct the errors below.'})


class Home_Page(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        task = Task.objects.all()
        return render(request, 'home_page.html', {'tasks': task})


class Add_Comment(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, task_id):
        task = Task.objects.filter(id=task_id).first()
        print('Task:', task.id, task.title)
        return render(request, 'add_comment.html', {'task': task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        content = request.POST.get('content')
        print('Task and Content:', task, content)
        Comment.objects.create(task=task, user=request.user, comment=content)
        return redirect('home_page')


class Show_Detail(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        print('Task:', task)
        return render(request, 'show_detail.html', {'task': task})



class Show_Comment(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        comments = Comment.objects.filter(task=task)
        print('TASK and Comments:', task, comments)
        return render(request, 'show_comments.html', {'task': task, 'comments': comments})


class Edit_Task(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'edit_task.html', {'task': task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.title = request.POST.get('title')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.end_date = request.POST.get('end_date')
        task.description = request.POST.get('description')
        task.save()
        return redirect("home_page")


class Delete_Task(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            task.delete()
            return redirect("home_page")
        except Task.DoesNotExist:
            return render(request, "home_page.html", {"error": "Task does not exist"})

# class TaskSearch(LoginRequiredMixin,View):
#     def get(self,request):
#         query = request.GET.get('q','')
#         print(query)
#         if query:

#           tasks = Task.objects.filter(
#                 Q(title__icontains=query) |
#                 Q(end_date=query) |
#                 Q(status=query)
#           )
#           print(tasks)
#         else:
#             tasks = Task.objects.all()
#         return render(request, 'task_search.html', {'tasks': tasks, 'query': query})



class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')
