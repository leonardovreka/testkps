from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated

class TodoViewSet(viewsets.ModelViewSet):

    # queryset = Todo.objects.all() είχα αυτό αλλά το αλλάζω με τα def
    authentication_classes = (JWTAuthentication,)
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    #φέρνει τοδος μονο για τον συγκεκριμένω user
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

    #κάνει το συνδεδεμένο υσερ ως τον owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#filtra sto url
    filterset_fields = ["is_completed", "due_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "title"]
    ordering = ["-created_at"]

