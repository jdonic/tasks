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