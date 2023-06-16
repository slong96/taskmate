from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # this will restrict user from going bypass the homepage, redirects user to login
from django.contrib.auth.forms import UserCreationForm # creating a user form
from .forms import UserRegisterForm # creating a user form
from django.contrib.auth import login # when user creates an account, this will login that user

from django.urls import reverse_lazy
from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__' # LoginView already has a form with fields
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks') # send authenticated user to task page
    
    def get_context_data(self,*args, **kwargs):
        context = super(CustomLoginView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Login'
        return context
    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    # redirect user when register form is submitted
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get_context_data(self,*args, **kwargs):
        context = super(RegisterPage, self).get_context_data(*args, **kwargs)
        context['title'] = 'Register'
        return context
    
    # overriding, if user tries to go to /register or /login in the address bar,
    # this will redirect the user to the tasks list page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView): # looks for name_list.html or have template = 'example.html'
    model = Task
    # By default, the object in the html template is called object_list. 
    # This will allow me to change it to whatever I want. 
    # For this, I changed it to task. Now when I do a for loop, I can use 'tasks'
    # instead of 'object_list'.
    context_object_name = 'tasks'

    # function to ensure user is getting their own data
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # 'tasks' is from context_object_name above
        context['tasks'] = context['tasks'].filter(user=self.request.user) # only user's task, no other users
        context['count'] = context['tasks'].filter(complete=False).count()
        context['title'] = 'Task List'

        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input # this is for the html page for value

        return context


class TaskCreate(LoginRequiredMixin, CreateView): # looks for name_form.html
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks') # urls.py name

    # form valid is built it function by django.
    # ensure the logged in user can create a task and can't create a task for a different user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    def get_context_data(self,*args, **kwargs):
        context = super(TaskCreate, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Task'
        return context


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks')

    def get_context_data(self,*args, **kwargs):
        context = super(TaskUpdate, self).get_context_data(*args, **kwargs)
        context['title'] = 'Edit Task'
        return context



def home(request):
    return render(request, 'base/home.html', {'title': 'Home'})


def about(request):
    return render(request, 'base/about.html', {'title': 'About'})


def delete_task(request, pk):
    task_query = Task.objects.get(id=pk)
    task_query.delete()
    return redirect('tasks')


def complete_task(request, pk):
    task_query = Task.objects.get(id=pk)
    task_query.complete = True
    task_query.save()
    return redirect('tasks')


def incomplete_task(request, pk):
    task_query = Task.objects.get(id=pk)
    task_query.complete = False
    task_query.save()
    return redirect('tasks')