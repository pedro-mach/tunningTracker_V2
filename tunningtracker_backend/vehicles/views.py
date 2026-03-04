from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    """
    Lista, cria, edita ou deleta veículos do usuário autenticado.
    """
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas os veículos do próprio usuário
        return Vehicle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associa automaticamente o usuário criador da requisição ao registro do carro
        serializer.save(user=self.request.user)
