from django.urls import path
from .views import UserSubscription
from .import views


urlpatterns = [
    path('', views.homepage, name="homepage"),
   path('signup', views.signup, name="signup"),
   path('signin', views.signin, name="signin"),
   path('signout', views.signout, name="signout"),
   path('choose-subscription/', UserSubscription, name='usersubscription' )
    
]