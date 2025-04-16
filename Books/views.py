from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from django.db import transaction
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class LoginUser(TokenObtainPairView):
    serializer_class = obtainSerializer
    permission_classes = [AllowAny]

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

#================manage users====================
#list users
class ListUsers(generics.ListAPIView):
    queryset = User.objects.filter(is_customer=True).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


#Update user 
class UpdateUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

#list single user
class SingleUser(generics.RetrieveAPIView):
      queryset = User.objects.all()
      serializer_class = UserSerializer
      permission_classes = [IsAuthenticated]

      def retrieve(self, request, *args, **kwargs):
          instance = self.get_object()
          serializer = self.get_serializer(instance)
          return Response(serializer.data, status=status.HTTP_200_OK)

#delete user account
class DeleteUser(generics.RetrieveDestroyAPIView):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     permission_classes = [IsAuthenticated]

     def delete(self, request, *args, **kwargs):
          instance = self.get_object()
          instance.delete()
          return Response({"msg": "user Deleted successfully"})

#deactivate user 
class DeactivateUser(APIView):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     
     def patch(self, request, *args, **kwargs):
          user_id = kwargs.get('pk')
          status = request.data.get('is_active')

          try:
               with transaction.atomic():
                    user = User.objects.get(pk=user_id)
                    user.is_active = status
                    user.save()

                    serializer = self.serializer_class(user)
                    return Response(serializer.data)
          except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


#===========custom pagination============
class CustomPagination(PageNumberPagination):
    page_size = 9  # Items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

#===============views to manage books==========================

#post books
class AddBooks(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

#list books
class ListBooks(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

#book detail
@api_view(['GET'])
def BookDetails(request, book_id):
    try:
        book = Books.objects.get(id=book_id)
    except Books.DoesNotExist:
        return Response({"err:book not found"})
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


#edit books
class EditBooks(generics.UpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.serializer_class(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

#remove book
class DeleteBook(generics.RetrieveDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        return Response({"err: book deleted successfully"}, status=status.HTTP_200_OK)
    
#===========================reservation views=========================
#list all reservations
class ListReservations(generics.ListAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

#list user resevations
@api_view(['GET'])
def UserReservations(request, user_id):
     try:
          user = User.objects.prefetch_related('reserve', 'reserve__book').get(id=user_id)
     except User.DoesNotExist:
          return Response({"err:user not found"})
     if request.method == 'GET':
          serializer = UserReservationSerializer(user)
          return Response(serializer.data, status=status.HTTP_200_OK)
     
#create reservations
class PostReservations(generics.CreateAPIView):
     queryset = Reservations.objects.all()
     serializer_class = ReservationSerializer
     permission_classes = [IsAuthenticated]

#Borrowed Books
class BorrowedBooks(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        # Filter reservations by the current authenticated user and status 'Taken'
        return Reservations.objects.filter(user=self.request.user, status='Taken')

#delete reservation
class DeleteReservation(generics.RetrieveDestroyAPIView):
     queryset = Reservations.objects.all()
     serializer_class = ReservationSerializer
     permission_classes = [IsAuthenticated]

     def delete(self, request, *args, **kwargs):
          instance = self.get_object()
          instance.delete()
          return Response({"msg:reservation deleted successfully"})
     
#change reservation status
class ChangeStatus(APIView):
     queryset = Reservations.objects.all()
     serializer_class = ReservationSerializer
     permission_classes = [IsAuthenticated]

     def patch(self, request, *args, **kwargs):
          reserve_id = kwargs.get('pk')
          status = request.data.get('status')

          try:
               with transaction.atomic():
                    reserve = Reservations.objects.get(pk=reserve_id)
                    reserve.status = status
                    reserve.save()

                    serializer = self.serializer_class(reserve)
                    return Response(serializer.data)
          except Reservations.DoesNotExist:
                    return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)

     
     


