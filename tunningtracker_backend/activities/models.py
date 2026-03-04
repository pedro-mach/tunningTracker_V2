import uuid
from django.db import models
from vehicles.models import Vehicle

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('Manutenção', 'Manutenção'),
        ('Modificação', 'Modificação'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='activities')
    tipo = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    descricao = models.CharField(max_length=255)
    observacoes = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_atividade = models.DateField()
    data_revisao_futura = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.tipo}: {self.descricao} no veículo {self.vehicle.placa}'
