from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_customer']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_at', 'genre']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'copies', 'contact', 'reservation_date', 'status']

admin.site.register(User, UserAdmin)
admin.site.register(Books, BookAdmin)
admin.site.register(Reservations, ReservationAdmin)