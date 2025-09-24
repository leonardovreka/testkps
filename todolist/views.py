from rest_framework import viewsets, permissions
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

#filtra sto url
    filterset_fields = ["is_completed", "due_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "title"]
    ordering = ["-created_at"]

