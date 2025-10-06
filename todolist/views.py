from rest_framework import viewsets, generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Todo
from .serializers import TodoSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

#registration imports μαζι με (generics, status, AllowAny, RegistrationSerializer)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class TodoViewSet(viewsets.ModelViewSet):

    authentication_classes = (JWTAuthentication,)
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    # Return only todos for the logged-in user
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Todo.objects.all()
        return Todo.objects.filter(owner=user)

    # Set the owner to the logged-in user when creating
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# filtra sto url
    filterset_fields = ["is_completed", "due_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "title"]
    ordering = ["-created_at"]

# Registration
class RegistrationViewSet(generics.CreateAPIView):          #CreateAPIView create new objects via POST
    serializer_class = RegistrationSerializer               #του λεω ποιο serializer να χρησιμοπ
    permission_classes = (AllowAny,)                        #για να κάνουν register και μη authenticated users, γτ δεν θα έχουν τοκενς οταν κανουν ρεγιστερ

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) #request τα data σε json
        serializer.is_valid(raise_exception=True)           #κάνει τσεκ τα validation rules για password match etc
        user = serializer.save()                            #αν ολα καλά κάνει create τον user

        refresh = RefreshToken.for_user(user)               #new tokens tied to specific user
        access = refresh.access_token

        return Response(                                    #γυρνάει σε json
            {
                "id": user.id,
                "username": user.username,
                "access": str(access),  # <- correct key name
                "refresh": str(refresh),  # <- correct key name
            },
            status=status.HTTP_201_CREATED,
        )

#Registration create user + issue tokens directly (RefreshToken.for_user)
#Login use TokenObtainPairView (or serializer) since credentials need to be checked