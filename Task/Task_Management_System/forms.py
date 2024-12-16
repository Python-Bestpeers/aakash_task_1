import re

from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Task, User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "assigned_to",
            "start_date",
            "end_date",
            "priority",
            "status",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_end_date(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")

        if not start_date or not end_date:
            raise ValidationError("Start date and end date are required.")

        if end_date < timezone.now():
            raise ValidationError("End date cannot be in the past.")

        if end_date.date() < start_date:
            raise ValidationError("End date must be after the start date.")

        return end_date

    def clean(self):
        cleaned_data = super().clean()

        assigned_to = cleaned_data.get("assigned_to")
        assigned_by = cleaned_data.get("assigned_by")

        if assigned_to and assigned_by and assigned_to == assigned_by:
            raise ValidationError(
                "Assigned to and Assigned by cannot be the same user."
            )

        return cleaned_data


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
        label="Password",
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "password"]

    def clean(self):
        cleaned_data = super().clean()
        email = self.clean_data.get("email", "")
        first_name = self.clean_data.get("first_name")
        password = self.clean_data.get("password")

        errors = {}
        if not first_name.isalpha():
            errors["first_name"] = "first_name must contain only characters."
        if User.objects.filter(email=email).exists():
            errors["email"] = "Email is already registered."
        if "@" not in email or "." not in email:
            errors["email"] = "Enter a valid email address."
        if len(password) < 5:
            errors["password"] = "Password must be at least 5 characters."
        if not re.search(r"[!@#$%^&*|<>,(){}]", password):
            errors["password"] = (
                "Password must contain at least one special character."
            )
        if errors:
            raise ValidationError(errors)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority", "status", "end_date", "description"]
        widgets = {
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority", "status", "end_date", "description"]
        widgets = {
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
