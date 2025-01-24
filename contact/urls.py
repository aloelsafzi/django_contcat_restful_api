from django.urls import path
from . import views

urlpatterns = [
    path('get-all', views.get_contacts, name='get-all-contact'),
    path('get/<int:id>', views.get_contact_by_id, name='get-contact-by-id'),
    path('create', views.add_contact, name='create-contact'),
    path('update', views.update_contact, name='update-contact'),
    path('delete/<int:id>', views.delete_contact, name='delete-contact'),
]