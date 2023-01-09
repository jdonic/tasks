from django.test import TestCase
from .models import Task
from django.utils import timezone

import datetime


class TaskTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.task = Task.objects.create(
            title="Fix the car",
            description="Fix the car so I can go to Croatia.",
            due_date=datetime.date(1997, 10, 19),
        )

    def test_task_model(self) -> None:
        self.assertEqual(f"{self.task}", "Fix the car")
        self.assertEqual(self.task.title, "Fix the car")
        self.assertEqual(self.task.description, "Fix the car so I can go to Croatia.")
        self.assertEqual(self.task.due_date, datetime.date(1997, 10, 19))
        self.assertFalse(self.task.is_completed)
        self.assertIsNone(self.task.completed_at)

    def test_task_model_completed(self) -> None:
        self.task.mark_completed()
        self.assertTrue(self.task.is_completed)
        self.assertIsNotNone(self.task.completed_at)
        self.assertAlmostEqual(
            self.task.completed_at, timezone.now(), delta=timezone.timedelta(seconds=1)
        )
