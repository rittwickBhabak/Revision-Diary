from django.db import models
from django.urls import reverse 

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    created_at = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("myapp:home")
    
    def __str__(self):
        return self.title 


class ToDo(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()

    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.task.title} is to be done at {self.date} and Completed:{self.is_completed}"