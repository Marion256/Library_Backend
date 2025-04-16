from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False, db_index=True)
    is_staff = models.BooleanField(default=False, db_index=True)

class Books(models.Model):
    title = models.CharField(max_length=255)
    published_at = models.PositiveIntegerField()
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    copies = models.PositiveIntegerField(default=0)
    pages = models.PositiveIntegerField(default=0)
    summary = models.CharField(max_length=1000)

class Reservations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserve', db_index=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='reserved_book', db_index=True)
    copies = models.PositiveBigIntegerField(default=0)
    contact = models.PositiveIntegerField(default=0)
    reservation_date = models.DateField()
    status = models.CharField(default='Pending')
