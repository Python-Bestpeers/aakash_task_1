from django.urls import path

from .views import (
    AddCommentView,
    CreateTaskView,
    DeleteTaskView,
    EditTaskView,
    HomePageView,
    LoginView,
    LogoutView,
    MyDashboardView,
    ShowCommentView,
    ShowDetailView,
    ShowProfileView,
    SignupView,
    UpdateStatusView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("", SignupView.as_view(), name="signup"),
    path("create_task/", CreateTaskView.as_view(), name="create_task"),
    path("home_page/", HomePageView.as_view(), name="home_page"),
    path("ViLogoutView/", LogoutView.as_view(), name="logout"),
    path("add_comment/<int:task_id>/", AddCommentView.as_view(), name="add_comment"),
    path("show_comments/<int:task_id>/", ShowCommentView.as_view(), name="show_comments"),
    path("edit_task/<int:task_id>/", EditTaskView.as_view(), name="edit_task"),
    path("delete_task/<int:task_id>/", DeleteTaskView.as_view(), name="delete_task"),
    path("show_detail/<int:task_id>/", ShowDetailView.as_view(), name="show_detail"),
    path("show_profile/", ShowProfileView.as_view(), name="show_profile"),
    path("my_dashboard/", MyDashboardView.as_view(), name="my_dashboard"),
    path("update_status/<int:task_id>/", UpdateStatusView.as_view(), name='update_status'),
]
