from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

import datetime

from .models import Task


class TaskTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.task = Task.objects.create(
            title="Fix the car",
            description="Fix the car so I can go to Croatia.",
            due_date=datetime.date(2024, 10, 19),
        )
        cls.task_2 = Task.objects.create(
            title="Fix the washing_machine.",
            description="Fix washing machine so I have something to wear.",
            due_date=datetime.date(2023, 10, 19),
        )
        cls.task_3 = Task.objects.create(
            title="Fix myself",
            description="So I am not such a mess",
            due_date=datetime.date(2025, 10, 19),
        )

    def test_task_model(self) -> None:
        self.assertEqual(f"{self.task}", "Fix the car")
        self.assertEqual(self.task.title, "Fix the car")
        self.assertEqual(self.task.description, "Fix the car so I can go to Croatia.")
        self.assertEqual(self.task.due_date, datetime.date(2024, 10, 19))
        self.assertFalse(self.task.is_completed)
        self.assertIsNone(self.task.completed_at)

    def test_task_model_completed(self) -> None:
        self.task.mark_completed()
        self.assertTrue(self.task.is_completed)
        self.assertIsNotNone(self.task.completed_at)
        self.assertAlmostEqual(
            self.task.completed_at, timezone.now(), delta=timezone.timedelta(seconds=1)
        )

    def test_task_list_view(self) -> None:
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_list.html")
        self.assertContains(response, "Fix the car")
        self.assertContains(response, "Fix myself")
        tasks = response.context["object_list"]
        self.assertEqual(tasks[0], self.task_2)
        self.assertEqual(tasks[1], self.task)
        self.assertEqual(tasks[2], self.task_3)

    def test_task_detail_view(self) -> None:
        response = self.client.get(self.task.get_absolute_url())
        no_response = self.client.get("/tasks/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Fix the car")
        self.assertContains(response, "Fix the car so I can go to Croatia.")
        self.assertTemplateUsed(response, "tasks/task_detail.html")

    def test_task_create_view_valid_data(self) -> None:
        response = self.client.post(
            reverse("task_new"),
            {
                "title": "New task",
                "description": "New description",
                "due_date": datetime.date(2069, 6, 9),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.last().title, "New task")
        self.assertEqual(Task.objects.last().description, "New description")
        self.assertFalse(self.task.is_completed)
        self.assertIsNone(self.task.completed_at)

    def test_task_create_view_invalid_data(self) -> None:
        response = self.client.post(
            reverse("task_new"),
            {
                "title": "",
                "description": "",
                "due_date": datetime.date(2069, 6, 9),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "title", "This field is required.")
        self.assertFormError(response, "form", "description", "This field is required.")

        response = self.client.post(
            reverse("task_new"),
            {
                "title": "New task",
                "description": "New description",
                "due_date": datetime.date(2000, 1, 1),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "due_date", "The due date must be in the future"
        )
