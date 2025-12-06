from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from tasks.models import Task, Category
from tasks.serializers import TaskSerializer, CategorySerializer
from tasks.filters import TaskFilter
from tasks.permissions import IsOwnerOrReadOnly
from tasks.tasks import send_task_reminder as celery_send_task_reminder

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at"]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def remind(self, request, pk=None):
        task = self.get_object()
        if not request.user.email:
            return Response({"detail": "User has no email."}, status=status.HTTP_400_BAD_REQUEST)
        celery_send_task_reminder.delay(task.id, request.user.email)
        return Response({"status": "reminder scheduled"}, status=status.HTTP_202_ACCEPTED)
