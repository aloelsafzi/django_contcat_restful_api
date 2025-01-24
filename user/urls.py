from django.urls import path
from . import views

urlpatterns = [
    path('get-all', views.get_users, name='get-all-user'),
    path('get/<int:id>', views.get_user_by_id, name='get-user-by-id'),
    path('create', views.add_user, name='create-user'),
    path('update', views.update_user, name='update-user'),
    path('delete/<int:id>', views.delete_user, name='delete-user'),
]