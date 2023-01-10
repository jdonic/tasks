from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect
from django.forms import Form

import datetime

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
    template_name = "tasks/task_new.html"
    fields = ["title", "description", "due_date"]

    def form_valid(self, form: Form) -> None:
        # Check if the title and description fields are not empty
        if form.cleaned_data["title"] and form.cleaned_data["description"]:
            # The title and description fields are not empty
            # Check if the due date is in the future
            current_date = datetime.date.today()
            due_date = form.cleaned_data["due_date"]
            if due_date > current_date:
                # The due date is in the future, so save the form data
                form.save()
                return redirect("task_list")
            else:
                # The due date is not in the future, so display an error message
                form.add_error("due_date", "The due date must be in the future")
                return render(self.request, self.template_name, {"form": form})
        else:
            # The title or description field is empty, so display an error message
            return render(self.request, self.template_name, {"form": form})
