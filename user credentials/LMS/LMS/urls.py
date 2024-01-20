
from django.contrib import admin
from django.urls import path, include
from credentials.views import homepage, signin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', signin, name='signin'),
    path('', homepage, name='homepage'),
    path('accounts/', include('credentials.urls'))
]
