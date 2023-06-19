from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction

class PostViewTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.post_list_url = reverse('posts')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }


        # Step 1: Create a user by hitting the registration endpoint
        response = self.client.post(self.register_url, self.user_data, format='json')
        # print(response.data)
        # self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.token = response.data['data']['token']
     
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def create_single_post(self):
        post_data = {'title': 'title', 'body': 'body'}

        response = self.client.post(self.post_list_url, post_data, format='json')
        return response

    def create_post(self):
        for i in range(5):
            post_data = {'title': f'title {i+1}', 'body': f'body {i+1}'}

            response = self.client.post(self.post_list_url, post_data, format='json')

    def test_create_posts(self):
        for i in range(5):
            post_data = {'title': f'title {i+1}', 'body': f'body {i+1}'}

            response = self.client.post(self.post_list_url, post_data, format='json')
        
        response = self.client.get(self.post_list_url)
        # self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 5)


    def test_get_all_posts(self):
        self.create_post()#
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 5)

    def test_get_single_post(self):
        self.create_post()
        response = self.client.get("/api/posts/1")
        self.assertEqual(response.data['status'], status.HTTP_200_OK)

    def test_update_post(self):
        self.create_post()
        response = self.client.put("/api/posts/1",{'title':'updated title','body':'updated body'},format='json')
        self.assertEqual(response.data['status'], status.HTTP_200_OK)

    def test_delete_post(self):
        self.create_post()
        response = self.client.delete("/api/posts/1")
        self.assertEqual(response.data['status'], status.HTTP_204_NO_CONTENT)
        
