from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    status_choices = [
        ('C', 'COMPLETED'),
        ('P', 'PENDING'),
    ]
    priority_choices = [
        ('1', '1️⃣'),
        ('2', '2️⃣'),
        ('3', '3️⃣'),
        ('4', '4️⃣'),
        ('5', '5️⃣'),
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(
        max_length=2, choices=status_choices, default="P")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=2, choices=priority_choices)

    def __str__(self):
        return self.title[:50]
