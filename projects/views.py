from django.shortcuts import render

# Create your views here.
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
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Fetch the project instance
        self.perform_destroy(instance)  # Perform the soft delete
        return Response({'status': 'project soft deleted'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        # Fetch the soft-deleted project (including deleted projects in the query)
        try:
            project = Project.objects.get(pk=pk, is_deleted=True)
            project.restore()  # Call the restore method to un-delete the project
            return Response({'status': 'project restored'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'detail': 'No Project matches the given query.'}, status=status.HTTP_404_NOT_FOUND)


# Task ViewSet
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Fetch the project instance
        self.perform_destroy(instance)  # Perform the soft delete
        return Response({'status': 'task soft deleted'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        # Fetch the soft-deleted task (including deleted tasks in the query)
        try:
            task = Task.objects.get(pk=pk, is_deleted=True)
            task.restore()  # Call the restore method to un-delete the task
            return Response({'status': 'task restored'}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'detail': 'No Task matches the given query.'}, status=status.HTTP_404_NOT_FOUND)


class UserRegistrationView(APIView):

    def post(self, request):
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
