from django.urls import path, include
from . import views
app_name = 'info'

urlpatterns = [
    # авторизация
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    # пользователи
    path('users/', include([
            path('', views.UsersApiView.as_view(), name='users_view'),
            path('current/', views.UserCurrentApiView.as_view(), name='current_user_view'),
            path('<int:user_id>/', views.UserUpdateApiView.as_view(), name='user_update'),
        ])),
    path('private/', include([
            path('users/', views.PrivateUserApiView.as_view(), name='streamer_create_payout'),
            path('users/<int:user_id>/', views.PrivateUserUpdateApiView.as_view(), name='streamer_create_payout'),
        ])),
]

