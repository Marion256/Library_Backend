from django.urls import path
from .views import *

urlpatterns = [
    path('login', LoginUser.as_view()),
    path('register', RegisterUser.as_view()),

    #========paths for the books===========
    path('add_books', AddBooks.as_view()),
    path('list_books', ListBooks.as_view()),
    path('book_detail/<int:book_id>', BookDetails),
    path('edit_book/<int:pk>', EditBooks.as_view()),
    path('delete_book/<int:pk>', DeleteBook.as_view()),

    #=======================paths for user==================
    path('list_users', ListUsers.as_view()),
    path('delete_user/<int:pk>', DeleteUser.as_view()),
    path('deactivate_user/<int:pk>', DeactivateUser.as_view()),
    path('update_user/<int:pk>',UpdateUser.as_view()),
    path('single_user/<int:pk>', SingleUser.as_view()),

    #======================paths for reservations====================
    path('user_reservations/<int:user_id>', UserReservations),
    path('post_reservations', PostReservations.as_view()),
    path('delete_reservation/<int:pk>', DeleteReservation.as_view()),
    path('list_reservations', ListReservations.as_view()),
    path('change_status/<int:pk>', ChangeStatus.as_view()),
    path('borrowed_books', BorrowedBooks.as_view())
] 