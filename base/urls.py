from django.urls import path
from .views import TaskList, TaskCreate, TaskUpdate, CustomLoginView, RegisterPage
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),

    path('login/', CustomLoginView.as_view(), name='login'),
    # LogoutView comes with next_page attribute to redirect the user to another page. So I don't need a custom logout.html if I don't need it.
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='base/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'), name='password_reset_complete'),

    path('register/', RegisterPage.as_view(), name='register'),
    path('about/', views.about, name='about'),

    path('task-list/', TaskList.as_view(), name='tasks'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', views.delete_task, name='task-delete'),
    
    path('task-complete/<int:pk>/', views.complete_task, name='task-complete'),
    path('task-incomplete/<int:pk>/', views.incomplete_task, name='task-incomplete'),
]