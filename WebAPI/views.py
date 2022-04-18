from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Books_Serializer, User_serializer ,Books_log_serializer
from .models import Books, Books_log
from django.contrib.auth.models import User


@api_view(['GET'])
def index(request):
    return Response('Welcome to WebAPI')


@api_view(['GET'])
def books_viewall(request):
    books = Books.objects.all()
    serialzer = Books_Serializer(books, many=True)
    return Response(serialzer.data)


@api_view(['GET'])
def books_viewone(request, id):
    books = Books.objects.get(book_id=id)
    serialzer = Books_Serializer(books, many=False)
    return Response(serialzer.data)


@api_view(['POST'])
def books_add(request):
    serialzer = Books_Serializer(data=request.data)
    if serialzer.is_valid():
        serialzer.save()
    return Response(serialzer.data)


@api_view(['POST'])
def books_update(request, id):
    books = Books.objects.get(book_id=id)
    serialzer = Books_Serializer(instance=books, data=request.data)
    if serialzer.is_valid():
        serialzer.save()
    return Response(serialzer.data)


@api_view(['DELETE'])
def books_delete(request, id):
    books = Books.objects.get(book_id=id)
    books.delete()
    return Response("Sucessfully Deleted ")


# User function from here-----------------------------------------------------------------------------------------------


@api_view(['GET'])
def users_viewall(request):
    users = User.objects.all()
    serialzer = User_serializer(users, many=True)
    return Response(serialzer.data)


@api_view(['GET'])
def users_viewone(request, username):
    users = User.objects.get(username=username)
    serialzer = User_serializer(users, many=False)
    return Response(serialzer.data)


@api_view(['POST'])
def users_add(request):
    serialzer = User_serializer(data=request.data)
    if serialzer.is_valid():
        serialzer.save()
    return Response(serialzer.data)


@api_view(['POST'])
def users_update(request, id):
    users = User.objects.get(id=id)
    serialzer = User_serializer(instance=users, data=request.data)
    if serialzer.is_valid():
        serialzer.save()
    return Response(serialzer.data)


@api_view(['DELETE'])
def users_delete(request, id):
    users = User.objects.get(id=id)
    users.delete()
    return Response("Sucessfully Deleted ")

# Book-log function from here-----------------------------------------------------------------------------------------------


@api_view(['GET'])
def book_log_viewall(request):
    book_logs = Books_log.objects.all()
    serialzer = Books_Serializer(book_logs, many=True)
    return Response(serialzer.data)


@api_view(['GET'])
def book_log_viewone(request, id):
    users = User.objects.get(id=id)
    book_logs = Books_log.get(user=users)
    serialzer = Books_log_serializer(book_logs, many=False)
    return Response(serialzer.data)


@api_view(['POST'])
def book_log_add(request):
    data=request.data
    users = User.objects.get(id=int(data["user_id"]))
    books = Books.objects.get(book_id=str(data["book_id"]))
    bl= Books_log(user=users,book=books)
    bl.save()
    serialzer = Books_log_serializer(data=bl)
    if serialzer.is_valid():
        serialzer.save()

    return Response(serialzer.data)

'''
@api_view(['POST'])
def users_update(request, id):
    users = User.objects.get(id=id)
    serialzer = User_serializer(instance=users, data=request.data)
    if serialzer.is_valid():
        serialzer.save()
    return Response(serialzer.data)


@api_view(['DELETE'])
def users_delete(request, id):
    users = User.objects.get(id=id)
    users.delete()
    return Response("Sucessfully Deleted ")
    '''