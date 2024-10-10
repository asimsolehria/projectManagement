from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.

    This serializer handles the serialization and deserialization
    of Project instances, including fields for the project ID, name,
    description, associated users, and deletion status.
    """

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'users', 'is_deleted', 'deleted_at']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    This serializer handles the serialization and deserialization
    of Task instances, including fields for the task ID, associated
    project, title, description, status, due date, and deletion status.
    """

    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'status', 'due_date', 'is_deleted', 'deleted_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the creation of a new user, including
    validating input data and hashing the user's password.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """
        Create a new user with the validated data.

        This method overrides the default create method to ensure the
        password is hashed before saving the user instance.

        Args:
            validated_data (dict): A dictionary containing the validated
            user registration data.

        Returns:
            User: The created User instance.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
