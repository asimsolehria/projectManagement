from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, UserRegistrationSerializer


# Project ViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Projects.

    This ViewSet handles soft deletion of projects, meaning projects
    are marked as deleted instead of being permanently removed from the database.
    """
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overrides the perform_create method to set the user who created the project.
        """
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Overrides the destroy method to perform a soft delete on a project
        instead of deleting it permanently.
        """
        instance = self.get_object()  # Fetch the project instance
        self.perform_destroy(instance)  # Perform the soft delete
        return Response({'status': 'project soft deleted'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """
        Custom perform_destroy method that soft-deletes the project.
        """
        instance.delete()

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        """
        Custom action to restore a soft-deleted project.

        If the project exists and was soft deleted, it will be restored.
        """
        try:
            project = Project.objects.get(pk=pk, is_deleted=True)
            project.restore()  # Call the restore method to un-delete the project
            return Response({'status': 'project restored'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'detail': 'No Project matches the given query.'}, status=status.HTTP_404_NOT_FOUND)


# Task ViewSet
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Tasks.

    Tasks also support soft deletion similar to Projects.
    """
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overrides the perform_create method to set the user who created the task.
        """
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Overrides the destroy method to perform a soft delete on a task.
        """
        instance = self.get_object()  # Fetch the task instance
        self.perform_destroy(instance)  # Perform the soft delete
        return Response({'status': 'task soft deleted'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """
        Custom perform_destroy method that soft-deletes the task.
        """
        instance.delete()

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        """
        Custom action to restore a soft-deleted task.

        If the task exists and was soft deleted, it will be restored.
        """
        try:
            task = Task.objects.get(pk=pk, is_deleted=True)
            task.restore()  # Call the restore method to un-delete the task
            return Response({'status': 'task restored'}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'detail': 'No Task matches the given query.'}, status=status.HTTP_404_NOT_FOUND)


# User Registration API View
class UserRegistrationView(APIView):
    """
    API View to handle user registration.

    This endpoint allows users to register and creates a new user in the system.
    """

    def post(self, request):
        """
        Handles the POST request to register a new user.

        Validates the input data using the UserRegistrationSerializer,
        and if valid, creates a new user and returns a success message.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
