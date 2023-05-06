from django.urls import path
from .views import LoginView, RegisterView, LogoutView, SearchView

app_name = 'users'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('search', SearchView.as_view(), name='user_search'),
]
