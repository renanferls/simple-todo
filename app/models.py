from django.db import models

TASK_STATE = (
    ("TODO", "To Do"),
    ("INPROGRESS", "In Progress"),
    ("DONE", "Done"),
    ("ARCHIVED", "Archived"),
)


class Label(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    current_state = models.CharField(max_length=20, choices=TASK_STATE, default="TODO")
    due_date = models.DateTimeField(auto_now_add=True, null = True)
    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class LabelTask(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
