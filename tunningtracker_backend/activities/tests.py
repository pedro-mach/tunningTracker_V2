from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from vehicles.models import Vehicle
from .models import Activity

class ActivityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        
        self.client.force_authenticate(user=self.user)
        self.vehicle = Vehicle.objects.create(
            user=self.user, placa='KBC1234', marca='VW', modelo='Golf', ano=2020
        )
        self.vehicle_other = Vehicle.objects.create(
            user=self.other_user, placa='XYZ9876', marca='Fiat', modelo='Uno', ano=2010
        )
        self.activity_user = Activity.objects.create(
            vehicle=self.vehicle, tipo='Manutenção', descricao='Troca de óleo', valor=150.00, data_atividade='2023-01-01'
        )

    def test_create_activity_for_owned_vehicle(self):
        url = '/api/v1/activities/'
        data = {
            'vehicle': self.vehicle.id,
            'tipo': 'Modificação',
            'descricao': 'Rodas de liga',
            'valor': 2500.00,
            'data_atividade': '2023-02-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 2)

    def test_create_activity_on_other_users_vehicle_fails(self):
        url = '/api/v1/activities/'
        data = {
            'vehicle': self.vehicle_other.id,
            'tipo': 'Manutenção',
            'descricao': 'Roubo',
            'valor': 20.00,
            'data_atividade': '2023-03-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_activities(self):
        url = '/api/v1/activities/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['descricao'], 'Troca de óleo')
