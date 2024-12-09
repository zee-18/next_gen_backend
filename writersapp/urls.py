from django.urls import path
from .views import UserListView, LoginView, UpdateUserRoleView, SuggestionsView, SaveBookView, BookListView, UpdateBookView, WritingStats

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-role/<int:user_id>/', UpdateUserRoleView.as_view(), name='update-user-role'),
    path('suggestions/', SuggestionsView.as_view(), name='suggestions'),
    path('save-book/', SaveBookView.as_view(), name='save-book'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/update/', UpdateBookView.as_view(), name='update-book'),
    path('writing-stats/', WritingStats.as_view(), name='writing-stats'),
]
