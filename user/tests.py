import json

from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from .serializers import UserRequestSerializer

class UserTests(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path('api/v1/user/', include('user.urls'))
    ]

    def test_create_user(self):
        print('test_create_user: Memastikan berhasil create user')

        new_user = { 
            'username': 'test', 
            'email': 'test@email.com', 
            'password': 'test123', 
            'first_name': 'test', 
            'last_name': 'test',
        }

        data_json = json.dumps(new_user)

        url = reverse('create-user')
        response = self.client.post(url, data_json, content_type='application/json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        print('test_update_user: Memastika berhasil update user')
        
        new_user = { 
            'username': 'test', 
            'email': 'test@email.com', 
            'password': 'test123', 
            'first_name': 'test', 
            'last_name': 'test',
        }

        user_serializer = UserRequestSerializer(data=new_user)
        user_serializer.is_valid()
        user_serializer.save()

        id_user = user_serializer.data['id']

        update_user = { 
            'id': id_user,
            'username': 'test_2', 
            'email': 'test2@email.com', 
            'password': 'test1234', 
            'first_name': 'test2', 
            'last_name': 'test2',
        }

        url_update = reverse('update-user')
        response = self.client.put(url_update, json.dumps(update_user), content_type='application/json')
        response_dict = json.loads(response.content)
        print(response_dict)

        # hilangkan salah satu key dalam dict
        update_user.pop('password')
        update_user.pop('id')

        self.assertDictEqual(response_dict['data'], update_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_user(self):
        print('test_delete_user: Memastikan berhasil delete user')
        
        new_user = { 
            'username': 'test', 
            'email': 'test@email.com', 
            'password': 'test123', 
            'first_name': 'test', 
            'last_name': 'test',
        }

        user_serializer = UserRequestSerializer(data=new_user)
        user_serializer.is_valid()
        user_serializer.save()

        id_user = user_serializer.data['id']

        url_delete = reverse('delete-user', kwargs={'id': id_user})
        response = self.client.delete(url_delete)
        
        print(json.loads(response.content))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_all_user(self):
        print('test_get_all_user: Memastikan bisa get semua user')
        
        url = reverse('get-all-user')
        response = self.client.get(url)
        
        print(json.loads(response.content))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id(self):
        print('test_get_user_by_id: Memastikan bisa get user by id')
        
        new_user = { 
            'username': 'test', 
            'email': 'test@email.com', 
            'password': 'test123', 
            'first_name': 'test', 
            'last_name': 'test',
        }

        user_serializer = UserRequestSerializer(data=new_user)
        user_serializer.is_valid()
        user_serializer.save()

        id_user = user_serializer.data['id']

        url = reverse('get-user-by-id', kwargs={'id': id_user})
        response = self.client.get(url)

        print(json.loads(response.content))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

