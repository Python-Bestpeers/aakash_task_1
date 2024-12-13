from django.urls import path

from .views import (
    Add_Comment,
    Create_Task,
    Delete_Task,
    Edit_Task,
    Home_Page,
    Login,
    Logout,
    My_Dashboard,
    Show_Comment,
    Show_Detail,
    Show_Profile,
    Signup,
)

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('', Signup.as_view(), name='signup'),
    path('create_task/', Create_Task.as_view(), name='create_task'),
    path('home_page/', Home_Page.as_view(), name='home_page'),
    path('logout/', Logout.as_view(), name='logout'),
    path('add_comment/<int:task_id>/', Add_Comment.as_view(), name='add_comment'),
    path('show_comments/<int:task_id>/', Show_Comment.as_view(), name='show_comments'),
    path('edit_task/<int:task_id>/', Edit_Task.as_view(), name='edit_task'),
    path('delete_task/<int:task_id>/', Delete_Task.as_view(), name='delete_task'),
    path('show_detail/<int:task_id>/', Show_Detail.as_view(), name='show_detail'),
    path('show_profile/', Show_Profile.as_view(), name='show_profile'),
    path('my_dashboard/', My_Dashboard.as_view(), name='my_dashboard'),

]
