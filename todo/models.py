from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Todo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    exp = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="todo_images/", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")

    def __str__(self):
        return self.name

    # 모델의 save() 메서드를 오버라이딩
    def save(self, *args, **kwargs):
        if self.complete and self.completed_at is None:
            self.completed_at = timezone.now()

        if not self.complete and self.completed_at is not None:
            self.completed_at = None

        super().save(*args, **kwargs)
