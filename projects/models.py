from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    """
    Model representing a project.

    Attributes:
        name (str): The name of the project.
        description (str): A detailed description of the project.
        created_by (User): The user who created the project.
        users (ManyToManyField): Users associated with the project.
        is_deleted (bool): Flag indicating whether the project is deleted.
        deleted_at (datetime): Timestamp of when the project was deleted.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    users = models.ManyToManyField(User, related_name='projects')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        """
        Soft delete the project by marking it as deleted.

        This method sets the `is_deleted` flag to True and records
        the timestamp of deletion in `deleted_at`.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restore the project by marking it as not deleted.

        This method resets the `is_deleted` flag and clears the
        `deleted_at` timestamp.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class Task(models.Model):
    """
    Model representing a task associated with a project.

    Attributes:
        project (Project): The project to which the task belongs.
        title (str): The title of the task.
        description (str): A detailed description of the task.
        status (str): The current status of the task (e.g., pending or completed).
        due_date (date): The deadline for completing the task.
        created_by (User): The user who created the task.
        is_deleted (bool): Flag indicating whether the task is deleted.
        deleted_at (datetime): Timestamp of when the task was deleted.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        """
        Soft delete the task by marking it as deleted.

        This method sets the `is_deleted` flag to True and records
        the timestamp of deletion in `deleted_at`.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restore the task by marking it as not deleted.

        This method resets the `is_deleted` flag and clears the
        `deleted_at` timestamp.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()
