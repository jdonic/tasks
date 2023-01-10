from django.views.generic import ListView, DetailView, CreateView

from .models import Task


class TaskListView(ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    ordering = ["due_date"]


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"


class TaskCreateView(CreateView):
    model = Task
    context_object_name = "task_new"
    template_name = "tasks/task_new.html"
    fields = ["title", "description", "due_date"]
