from django.urls import path
from .views import user_login, user_create_account, user_logout, choose_plan

urlpatterns = [
    path('login/', user_login, name='login'),
    path('create-account', user_create_account, name='create_account'),
    path('logout', user_logout, name='logout'),
    path('choose-plan', choose_plan, name='choose_plan'),
    
]