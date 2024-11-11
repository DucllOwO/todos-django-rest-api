from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Todo
from .serializers import TodoSerializer
from .pagination import TodoPagination


class TodoViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for the Todo model.
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = TodoPagination  # Apply custom pagination

    def get_permissions(self):
        """
        Assign permissions based on the action being performed.
        """
        if self.action in ['create', 'destroy', 'list', 'retrieve', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        When overriding basic method like this we can add some custom logic
        """
        response = super().create(request, *args, **kwargs)
        return response
