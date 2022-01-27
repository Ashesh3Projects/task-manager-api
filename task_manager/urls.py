from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers
from tasks.views import TaskStatusChangeView, TaskStatusChangeViewNested, TaskViewSet

router = routers.SimpleRouter()

router.register("tasks", TaskViewSet)

task_router = routers.NestedSimpleRouter(router, "tasks", lookup="task")
task_router.register("history", TaskStatusChangeViewNested)

router.register("history", TaskStatusChangeView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include(task_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
