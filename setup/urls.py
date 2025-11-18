from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('app_revendedora.urls')),  # descomente depois quando criar as rotas do app
]
