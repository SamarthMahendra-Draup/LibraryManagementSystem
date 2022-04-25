#from django.shortcuts import render
#from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import Books_Serializer, User_serializer, Books_log_serializer, Roles_serializer
from .models import Books, Books_log, Roles
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.views import APIView
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse


@api_view(['POST'])
def login_view(request):
    username = request.data['username']
    password = request.data['password']
    print(username)
    print(password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response("Login sucessfull")
    else:
        return Response("error logging you in ")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    usern = request.user.username
    logout(request)
    return Response(f"Sucessfully logged you out {usern}")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return HttpResponse(request.user.username)


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


class Index(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        username = request.user.username
        return Response(f'Your are not a teacher {username}')


class Booksviewall(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Books.objects.all()
        serialzer = Books_Serializer(books, many=True)
        return Response(serialzer.data)


class Booksviewone(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        books = Books.objects.get(book_id=id)
        serialzer = Books_Serializer(books, many=False)
        return Response(serialzer.data)


class Booksadd(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        username = request.username
        if libauth(username):
            serializer = Books_Serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            Response("Only librarian can add books")


class Booksupdate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        username = request.user.username
        if libauth(username):
            books = Books.objects.get(book_id=id)
            serialzer = Books_Serializer(instance=books, data=request.data)
            if serialzer.is_valid():
                serialzer.save()
            return Response(serialzer.data)
        else:
            return Response("Only librarian can add books")


class Booksdelete(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
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
def users_viewone(request, un):
    username = request.user.username
    if adminauth(username):
        users = User.objects.get(username=un)
        serialzer = User_serializer(users, many=False)
        return Response(serialzer.data)
    else:
        return Response("Only admin can access this")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def users_add(request):
    username = request.user.username
    if adminauth(username):
        un = request.data['username']
        ps = request.data['password']
        em = request.data['email']
        fs = request.data['first_name']
        ls = request.data['last_name']
        role = request.data['role']
        uu = User.objects.create_user(username=un, password=ps, email=em, first_name=fs, last_name=ls)
        uu.save()
        uuu = User.objects.get(username=un)
        rr = Roles(user_id=uuu, user_role=str(role))
        rr.save()
        serialzer = User_serializer(uuu, many=False)
        return Response(serialzer.data)
    elif teacherauth(username):
        un = request.data['username']
        ps = request.data['password']
        em = request.data['email']
        fs = request.data['first_name']
        ls = request.data['last_name']
        role = request.data['role']
        if role == 'teacher' or role == 'student':
            uu = User.objects.create_user(username=un, password=ps, email=em, first_name=fs, last_name=ls)
            uu.save()
            uuu = User.objects.get(username=un)
            rr = Roles(user_id=uuu, user_role=str(role))
            rr.save()
            serialzer = User_serializer(uuu, many=False)
            return Response(serialzer.data)
        else:
            return Response("you have permission to add only a teacher or a user")
    else:
        return Response("Only admin can add data")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def users_update(request, id):
    username = request.user.username
    if adminauth(username):
        users = User.objects.get(id=id)
        users.username = request.data['username']
        users.first_name = request.data['first_name']
        users.last_name = request.data['last_name']
        users.email = request.data['email']
        users.password = request.data['password']
        users.save()
        return Response("SUCESSFULLY UPDATED")
    else:
        return Response("Only admin can update data")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def users_delete(request, id):
    username = request.user.username
    if adminauth(username):
        users = User.objects.get(id=id)
        users.delete()
        return Response("Sucessfully Deleted ")
    else:
        return Response("Only admin can delete data")

# Book-log function from here-------------------------------------------------------------------------------------------


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calculatefee(request, id):
    username = request.user.username
    dd = 0
    if libauth(username):
        book_logs = Books_log.objects.get(id=id)
        if book_logs.date_returned is not None:
            dd = (book_logs.date_exp-book_logs.date_issued)
            cc = dd.days*10
            if book_logs.date_returned > book_logs.date_exp:
                dd2 = book_logs.date_returned-book_logs.date_exp
                cc += dd2.days*20
        return Response(f"fee :{cc}")
    else:
        return Response("Error")


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
        date_issued = request.data["date_issued"]
        date_exp = request.data["date_exp"]
        if "date_returned" in request.data:
            bl = Books_log(user=users, book=books, date_issued=date_issued, date_exp=date_exp, date_returned=request.data["date_returned"])
        else:
            bl = Books_log(user=users, book=books, date_issued=date_issued, date_exp=date_exp)
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
        books_log.date_returned = request.data["date_returned"]
        books_log.save()
        return Response("Updated")
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
@permission_classes([IsAuthenticated])
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
