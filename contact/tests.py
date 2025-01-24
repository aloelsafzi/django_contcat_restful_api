import json
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from .serializers import ContactRequestSerializer

class ContactTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/v1/contact/', include('contact.urls')),
    ]

    def test_create_contact(self):
        """ 
        Memastikan bisa create contact 
        """
        print("test_create_contact: Memastikan bisa create contact")

        url = reverse('create-contact')
        data = {
            'phone': '085712123121',
            'first_address': 'Jalan Bandung',
            'seconds_address': 'Jalan Bogor',
            'user': None
        }
        data = json.dumps(data)
        response = self.client.post(url,  data, content_type='application/json')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_contact(self):
        """ 
        Memastikan berhasil update contact 
        """
        print("test_update_contact: Memastikan berhasil update contact")

        new_contact = {
            'phone': '085712123121',
            'first_address': 'Jalan Bandung',
            'seconds_address': 'Jalan Bogor',
            'user': None
        }

        new_contact_serializer = ContactRequestSerializer(data=new_contact)
        new_contact_serializer.is_valid()
        new_contact_serializer.save()

        id_contact = new_contact_serializer.data['id']

        update_contact = {
            'id': id_contact,
            'phone': '0857121231002',
            'first_address': 'Jalan Bandung 1',
            'seconds_address': 'Jalan Bogor 2',
            'user': None
        }

        url_update = reverse('update-contact')
        response = self.client.put(url_update, json.dumps(update_contact), content_type='application/json')

        print(json.loads(response.content))

        url_get_by_id = reverse('get-contact-by-id', kwargs={'id': id_contact})        

        response_contact_by_id = self.client.get(url_get_by_id)
        response_dict = json.loads(response_contact_by_id.content)
        update_contact.pop('user')

        print(response_dict['data'])
        print(update_contact)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_dict['data'], update_contact)
        

    def test_delete_contact(self):
        print("test_update_contact: Memastikan berhasil delete contact by id")

        new_contact = {
            'phone': '085712123121',
            'first_address': 'Jalan Bandung',
            'seconds_address': 'Jalan Bogor',
            'user': None
        }

        new_contact_serializer = ContactRequestSerializer(data=new_contact)
        new_contact_serializer.is_valid()
        new_contact_serializer.save()

        id_contact = new_contact_serializer.data['id']

        url = reverse('delete-contact', kwargs={'id': id_contact}) 
        response = self.client.delete(url)

        print(json.loads(response.content))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contact_by_id(self):
        print("test_update_contact: Memastikan berhasil get contact by id")

        new_contact = {
            'phone': '085712123121',
            'first_address': 'Jalan Bandung',
            'seconds_address': 'Jalan Bogor',
            'user': None
        }

        new_contact_serializer = ContactRequestSerializer(data=new_contact)
        new_contact_serializer.is_valid()
        new_contact_serializer.save()

        id_contact = new_contact_serializer.data['id']

        url = reverse('get-contact-by-id', kwargs={'id': id_contact}) 
        response = self.client.get(url)

        print(json.loads(response.content))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_contact(self):
        """ 
        Memastikan bisa get semua data contact 
        """
        print("test_get_all_contact: Memastikan bisa get semua data contact")
        url = reverse('get-all-contact')
        response = self.client.get(url)
        print(json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

