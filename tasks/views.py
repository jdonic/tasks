from django.views.generic import ListView, DetailView

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