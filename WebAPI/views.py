from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import Books_Serializer, User_serializer, Books_log_serializer, Roles_serializer
from .models import Books, Books_log, Roles
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q


def teacherauth(username):
    user = User.objects.get(username=username)
    try:
        rr = Roles.objects.get(user_id=user, user_role='teacher')
    except:
        rr = None
    if rr:
        return True
    else:
        return False


def libauth(username):
    user = User.objects.get(username=username)
    try:
        rr = Roles.objects.get(user_id=user, user_role='librarian')
    except:
        rr = None
    if rr:
        return True
    else:
        return False


def adminauth(username):
    user = User.objects.get(username=username)
    try:
        rr = Roles.objects.get(user_id=user, user_role='admin')
    except:
        rr = None
    if rr:
        return True
    else:
        return False


def studentauth(username):
    user = User.objects.get(username=username)
    try:
        rr = Roles.objects.get(user_id=user, user_role='student')
    except:
        rr = None
    if rr:
        return True
    else:
        return False


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    username = request.user.username
    if teacherauth(username):
        return Response(f'Welcome to WebAPI {username}')
    else:
        return Response(f'Your are not a teacher {username}')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def books_viewall(request):
    books = Books.objects.all()
    serialzer = Books_Serializer(books, many=True)
    return Response(serialzer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def books_viewone(request, id):
    books = Books.objects.get(book_id=id)
    serialzer = Books_Serializer(books, many=False)
    return Response(serialzer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def books_add(request):
    username = request.user.username
    if libauth(username):
        serialzer = Books_Serializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
        return Response(serialzer.data)
    else:
        return Response("Only librarian can add books")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def books_update(request, id):
    username = request.user.username
    if libauth(username):
        books = Books.objects.get(book_id=id)
        serialzer = Books_Serializer(instance=books, data=request.data)
        if serialzer.is_valid():
            serialzer.save()
        return Response(serialzer.data)
    else:
        return Response("Only librarian can add books")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def books_delete(request, id):
    username = request.user.username
    if libauth(username):
        books = Books.objects.get(book_id=id)
        books.delete()
        return Response("Sucessfully Deleted ")
    else:
        return Response("Only librarian can add books")


# User function from here-----------------------------------------------------------------------------------------------


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_viewall(request):

    username = request.user.username
    if adminauth(username):
        users = User.objects.all()
        serialzer = User_serializer(users, many=True)
        return Response(serialzer.data)
    elif teacherauth(username):
        roles = Roles.objects.filter(Q(user_role="teacher") | Q(user_role="student"))
        role_serializer = Roles_serializer(roles, many=True)
        user_id = []
        users = []
        for i in list(role_serializer.data):
            user_id.append(i['user_id'])
        for i in user_id:
            u = User.objects.get(id=i)
            serialzer = User_serializer(u, many=False)
            users.append(serialzer.data)
        return Response(users)
    elif studentauth(username):
        roles = Roles.objects.filter(user_role="student")
        role_serializer = Roles_serializer(roles, many=True)
        user_id = []
        users = []
        for i in list(role_serializer.data):
            user_id.append(i['user_id'])
        for i in user_id:
            u = User.objects.get(id=i)
            serialzer = User_serializer(u, many=False)
            users.append(serialzer.data)
        return Response(users)
    else:
        return Response("Error")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_viewone(request, username):
    users = User.objects.get(username=username)
    serialzer = User_serializer(users, many=False)
    return Response(serialzer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def users_add(request):
    serialzer = User_serializer(data=request.data)
    if serialzer.is_valid():
        serialzer.save()
    return Response(serialzer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def users_update(request, id):
    users = User.objects.get(id=id)
    serialzer = User_serializer(instance=users, data=request.data)
    if serialzer.is_valid():
        serialzer.save()
    return Response(serialzer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def users_delete(request, id):
    users = User.objects.get(id=id)
    users.delete()
    return Response("Sucessfully Deleted ")

# Book-log function from here-------------------------------------------------------------------------------------------


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_log_viewall(request):
    username = request.user.username
    if libauth(username):
        book_logs = Books_log.objects.all()
        serialzer = Books_log_serializer(book_logs, many=True)
        return Response(serialzer.data)
    else:
        return Response("Your are not a librarian")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_log_viewone(request, id):
    username = request.user.username
    if libauth(username):
        users = User.objects.get(id=id)
        book_logs = Books_log.objects.filter(user=users)
        serialzer = Books_log_serializer(book_logs, many=True)
        return Response(serialzer.data)
    else:
        return Response("Your are not a librarian")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_log_add(request):
    username = request.user.username
    if libauth(username):
        data = request.data
        users = User.objects.get(id=int(data["user_id"]))
        books = Books.objects.get(book_id=str(data["book_id"]))
        bl = Books_log(user=users, book=books)
        bl.save()
        serialzer = Books_log_serializer(data=bl)
        if serialzer.is_valid():
            serialzer.save()
        return Response(serialzer.data)
    else:
        return Response("Your are not a librarian")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_log_update(request, id):
    username = request.user.username
    if libauth(username):
        books_log = Books_log.objects.get(id=id)
        serialzer = Books_log_serializer(instance=books_log, data=request.data)
        if serialzer.is_valid():
            serialzer.save()
        return Response(serialzer.data)
    else:
        return Response("Your are not a librarian")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def book_log_delete(request, id):
    bl = Books_log.objects.get(id=id)
    bl.delete()
    return Response("Sucessfully Deleted ")

# roles function from here-----------------------------------------------------------------------------------------------


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def roles_viewall(request):
    username = request.user.username
    if adminauth(username):
        roles = Roles.objects.all()
        serialzer = Roles_serializer(roles, many=True)
        return Response(serialzer.data)
    else:
        return Response(f"Your are not admin {username}")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def roles_viewone(request, id):
    username = request.user.username
    if adminauth(username):
        roles = Roles.objects.get(user_id=id)
        serialzer = Roles_serializer(roles, many=False)
        return Response(serialzer.data)
    else:
        return Response("Your are not admin")


@api_view(['POST'])

def roles_add(request):
    username = request.user.username
    if adminauth(username):
        data = request.data
        user = User.objects.get(id=int(data['user_id']))
        print(user)
        user_role = data['user_role']

        rr = Roles(user_id=user, user_role=str(user_role))
        rr.save()
        serialzer = Roles_serializer(data=rr)
        if serialzer.is_valid():
            serialzer.save()
        return Response(serialzer.data)
    else:
        return Response("Your are not admin")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def roles_update(request, id):
    username = request.user.username
    if adminauth(username):
        roles = Roles.objects.get(id=int(id))
        serialzer = Roles_serializer(instance=roles, data=request.data)
        if serialzer.is_valid():
            serialzer.save()
        return Response(serialzer.data)
    else:
        return Response("Your are not admin")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def roles_delete(request, id):
    username = request.user.username
    if adminauth(username):
        rr = Roles.objects.get(id=int(id))
        rr.delete()
        return Response("Sucessfully Deleted ")
    else:
        return Response("Your are not admin")
