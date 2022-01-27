from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from tasks.models import Task, TaskStatusChange

from tasks.serializer import TaskSerializer, TaskStatusChangeSerializer
from tasks.filters import TaskFilter, TaskStatusChangeFilter


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data.get("status") and serializer.instance.status != serializer.validated_data.get(
            "status"
        ):
            TaskStatusChange.objects.create(
                task=serializer.instance,
                original_status=serializer.instance.status,
                updated_status=serializer.validated_data.get("status"),
                user=self.request.user,
            )

        serializer.save(user=self.request.user)


class TaskStatusChangeView(ReadOnlyModelViewSet):
    queryset = TaskStatusChange.objects.all()
    serializer_class = TaskStatusChangeSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskStatusChangeFilter

    def get_queryset(self):
        return TaskStatusChange.objects.filter(task__user=self.request.user, task__deleted=False)


class TaskStatusChangeViewNested(ReadOnlyModelViewSet):
    queryset = TaskStatusChange.objects.all()
    serializer_class = TaskStatusChangeSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskStatusChangeFilter

    def get_queryset(self):
        return TaskStatusChange.objects.filter(
            task=self.kwargs["task_pk"], task__user=self.request.user, task__deleted=False
        )
