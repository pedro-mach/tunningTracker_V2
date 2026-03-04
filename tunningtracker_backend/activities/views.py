from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Activity
from .serializers import ActivitySerializer
from vehicles.models import Vehicle

class ActivityViewSet(viewsets.ModelViewSet):
    """
    Lista, cria, edita ou deleta atividades vinculadas aos veículos do usuário.
    """
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Apenas atividades de veículos que pertencem ao request.user
        return Activity.objects.filter(vehicle__user=self.request.user).order_by('-data_atividade')

    def perform_create(self, serializer):
        # Checar se o veículo selecionado pertence de fato ao usuário da requisição
        vehicle = serializer.validated_data.get('vehicle')
        if vehicle.user != self.request.user:
            raise PermissionDenied("Você não pode adicionar atividades a um veículo de outro usuário.")
        serializer.save()
