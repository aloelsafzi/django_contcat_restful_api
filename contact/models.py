from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    phone = models.CharField(max_length=13, null=False, blank=False)
    first_address = models.TextField(null=True, blank=True)
    seconds_address = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='user_contact' ,on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'contacts'
        ordering = ['-id']

    def __str__(self):
        return self.phone
