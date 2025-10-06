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




class RegisterTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.valid = {
            "username": "nwtheia",
            "email": "nwtheia@gmail.com",
            "password": "leo123Test",
            "password2": "leo123Test",
        }

    def test_register(self):                                                          #αν μια απλή εγγραφή είναι επιτυχής.
        resp = self.client.post(self.register_url, self.valid, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)        #τσεκάρει αν και τα 2 στατους είναι ίδια αν όχι τυπώνει την απάντηση για debug
        self.assertTrue(User.objects.filter(username="nwtheia").exists())             #τσεκάρει αν το ναμε υπάρχει στην βάση
        if isinstance(resp.data, dict) and "username" in resp.data:                   #αν το ναμε υπάρχει στο api response τότε τσέκαρε αν είναι σωστό.
            self.assertEqual(resp.data['username'], self.valid['username'])           #γτ μπορεί να μην υπάρχει στο response και να κρασάρει
        print("Register: ", resp.status_code, resp.data, "\n")

    def test_duplicate_name_email(self):
        User.objects.create_user(
            username="nwtheia",
            email="nwtheia@gmail.com",
            password="leo123Test",
        )
        resp = self.client.post(self.register_url, self.valid, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.data)
        if isinstance(resp.data, dict):
            self.assertIn("username", resp.data)
            self.assertIn("email", resp.data)
        print("Register duplicate name or email: ", resp.status_code, resp.data, "\n")

    def test_register_missing_fields(self):
        invalid = {"username": "", "email": "", "password": "", "password2": ""}
        resp = self.client.post(self.register_url, invalid, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.data)
        if isinstance(resp.data, dict):
            self.assertIn("username", resp.data)
            self.assertIn("email", resp.data)
            self.assertIn("password", resp.data)
            self.assertIn("password2", resp.data)
        print("Register missing fields: ",resp.status_code, resp.data, "\n")

    def test_register_password_missmatch(self):
        mismatch = self.valid.copy()
        mismatch["password2"] = "leo123test"
        resp = self.client.post(self.register_url, mismatch, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.data)
        print("Register password missmatch: ",resp.status_code, resp.data, "\n")


class LoginTests(APITestCase):

    def setUp(self):
        self.token_url = reverse("tokens_obtain")
        self.username = "nwtheia"
        self.password = "leo123Test"
        self.user = User.objects.create_user(
            username=self.username,
            email="nwtheia@gmail.com",
            password=self.password,
        )

    def test_login_with_token_return(self):
        payload = { "username": self.username, "password": self.password}
        resp = self.client.post(self.token_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)
        self.assertTrue(isinstance(resp.data["access"], str) and resp.data["access"])
        self.assertTrue(isinstance(resp.data["refresh"], str) and resp.data["refresh"])
        print("Login with token return: ", resp.status_code, resp.data,"\n")

    def test_login_wrong_password(self):
        payload = { "username": "kapenisgamias", "password": "kapenigamia"}
        resp = self.client.post(self.token_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, resp.data)
        print("Login with wrong password or username: ", resp.status_code, resp.data,"\n")

    def test_login_missing_fields(self):
        payload = { "username": "", "password": ""}
        resp = self.client.post(self.token_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.data)
        print("Login with missing fields: ", resp.status_code, resp.data,"\n")


class TodoListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="nwtheia1", email="nwtheia1@gmail.com", password="leo123Pass"
        )
        self.user2 = User.objects.create_user(
            username="nwtheia2", email="nwtheia2@gmailcom", password="leo123Pass"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@gmail.com", password="leo123Pass"
        )
        self.admin.is_staff = True

        self.token_url = reverse("tokens_obtain")
        self.todos_list_url = reverse("todo-list")


        def authed_client(user, passw):
            resp = self.client.post(self.token_url, {"username": user, "password": passw}, format='json')
            self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
            cli = APIClient()
            cli.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
            return cli

        self.client_1 = authed_client("nwtheia1", "leo123Pass")
        self.client_2 = authed_client("nwtheia2", "leo123Pass")
        self.client_admin = authed_client("admin", "leo123Pass")

        #τοδοσ
        payload = { "title": "Paw kafe", "description": "perigrafi", "is_completed": False, "due_date": None}
        resp_1 = self.client_1.post(self.todos_list_url, payload, format='json')
        self.assertEqual(resp_1.status_code, status.HTTP_201_CREATED, resp_1.data)
        self.todo_1_id = resp_1.data['id']

        payload = {"title": "Paizw mpala", "description": "perigrafi", "is_completed": False, "due_date": None}
        resp_2 = self.client_2.post(self.todos_list_url, payload, format='json')
        self.assertEqual(resp_2.status_code, status.HTTP_201_CREATED, resp_2.data)
        self.todo_2_id = resp_2.data['id']

        self.todo_1_detail = reverse("todo-detail", args=[self.todo_1_id])
        self.todo_2_detail = reverse("todo-detail", args=[self.todo_2_id])

    def test_show_own_todos(self):
        resp_1 = self.client_1.get(self.todos_list_url)
        self.assertEqual(resp_1.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item["name"] == "nwtheia1" for item in resp_1.data))

        resp_2 = self.client_2.get(self.todos_list_url)
        self.assertEqual(resp_2.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item["name"] == "nwtheia2" for item in resp_2.data))
        print("Show own todos: ", resp_1.status_code, resp_2.status_code,"\n")

    def test_show_others_todos(self):
        resp = self.client_1.get(self.todo_2_detail)
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND), resp.data)
        print("Show others todos: ", resp.status_code,"\n")

    def test_create_todo_for_other_user(self):
        payload = {
            "title": "Kapenis the best",
            "description": "perigrafi",
            "is_completed": False,
            "due_date": None,
            "owner": "nwtheia2",           #read only γιαυτο
        }
        resp = self.client_1.post(self.todos_list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
        self.assertEqual(resp.data["name"], "nwtheia1")
        print("Create todo for others: ", resp.status_code,"\n")

    def test_admin_modifies_todo_for_other_user(self):
        patch_payload = {"title": "Kapenis the worst"}
        resp = self.client_admin.patch(self.todo_2_detail, patch_payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND), resp.data)
        if resp.status_code == status.HTTP_200_OK:
            self.assertEqual(resp.data["title"], "Kapenis the worst")
        print("Admin modifies todo for others: ", resp.status_code,"\n")




