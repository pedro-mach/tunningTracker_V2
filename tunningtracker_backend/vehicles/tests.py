from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Vehicle

class VehicleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        
        self.client.force_authenticate(user=self.user)
        self.vehicle1 = Vehicle.objects.create(
            user=self.user, placa='KBC1234', marca='VW', modelo='Golf', ano=2020
        )
        self.vehicle_other = Vehicle.objects.create(
            user=self.other_user, placa='XYZ9876', marca='Fiat', modelo='Uno', ano=2010
        )

    def test_create_vehicle(self):
        url = '/api/v1/vehicles/'
        data = {'placa': 'ABC4321', 'marca': 'Chevrolet', 'modelo': 'Onix', 'ano': 2018}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 3)
        # Checks if user was auto-assigned
        self.assertEqual(Vehicle.objects.get(placa='ABC4321').user, self.user)

    def test_list_vehicles_only_for_logged_user(self):
        url = '/api/v1/vehicles/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # only self.vehicle1
        self.assertEqual(response.data[0]['placa'], 'KBC1234')
