from django.contrib.auth.models import User
from django.urls import reverse                                           #κοιτάει τα urls απο τα ναμε που τους εχω βάλει
from rest_framework import status                                         #δίνει τις απαντήσεις σε στατους
from rest_framework.test import APITestCase, APIClient

class CreateUserAndTodo(APITestCase):

    def setUp(self):

        #φτιάχνω τον χρήστη στην προσωρινή βάση με το testcase
        self.username = "nwtheia7"
        self.password = "12345678leo"
        self.user = User.objects.create_user(
            username=self.username,
            email="nwtheia7@example.com",
            password=self.password,
        )

        #φτιάχνω τα τοκενς
        token_url = reverse("tokens_obtain")                            #παίρνει το url που είναι το login endpoint
        resp = self.client.post(token_url, {                       #συνδέει τον χρήστη χωρίς τα τοκενς
            "username": self.username,
            "password": self.password
        }, format='json')                                               #αν δεν βάλω json τα στελνει σε ποστ το οποιο δεν δέχεται για login
        self.assertEqual(resp.status_code, status.HTTP_200_OK)          #τσεκάρει αν η σύνδεση πέτυχε αλλιώς στέλνει ερρορ
        access = resp.data['access']                                    #μεταβλητή που κρατάει το αξες τοκεν

        self.authed = APIClient()                                       #σαν ψευτικο web browser
        self.authed.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')  # καθε φορά που κάνω request βάζει το αξες μεσα για να κανει authenticate


        self.todos_url = reverse('todo-list')                           #παιρνει το url τοδο

    def test_createTodo(self):
        payload = {                                                     #φτιάχνω το τοδο με json
            "title": "Kapenis the goat",
            "description": "what a handsome guy!",
            "is_completed": False,
            "due_date": None,
        }
        create_resp = self.authed.post(self.todos_url, payload, format='json')                #στέλνει το τοδο στο url που του έδωσα πάνω σε μορφή json
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED, create_resp.data)  #τσεκάρει αν το τοδο φτιάχτηκε σωστά
        self.assertEqual(create_resp.data['title'], payload['title'])                         #διπλοτσεκάρω αν το ονομα και ο τιτλος μπηκαν στην σωστή θέση και υπάρχουν
        self.assertEqual(create_resp.data['name'], self.username)
