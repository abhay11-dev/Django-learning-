from rest_framework.test import APITestCase

class AccountsAPITest(APITestCase):

    def test_api(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)