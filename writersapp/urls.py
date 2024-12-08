from django.urls import path
from .views import UserListView, LoginView, UpdateUserRoleView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-role/<int:user_id>/', UpdateUserRoleView.as_view(), name='update-user-role')
]
