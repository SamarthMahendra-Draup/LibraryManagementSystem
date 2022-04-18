from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/viewall', views.books_viewall, name='Books'),
    path('books/viewone/<str:id>', views.books_viewone, name='Books'),
    path('books/add', views.books_add, name='Books'),
    path('books/update/<str:id>', views.books_update, name='Books'),
    path('books/delete/<str:id>', views.books_delete, name='Books'),
    path('users/viewall', views.users_viewall, name='Users'),
    path('users/viewone/<str:username>', views.users_viewone, name='Users'),
    path('users/add', views.users_add, name='Users'),
    path('users/update/<str:id>', views.users_update, name='Users'),
    path('users/delete/<str:id>', views.users_delete, name='Users'),
    path('book_log/viewall', views.book_log_viewall, name='Books_log'),
    path('book_log/viewone/<str:id>', views.book_log_viewone, name='Books_log'),
    path('book_log/add', views.book_log_add, name='Books_log'),
]
