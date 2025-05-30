
from django.contrib import admin
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agent_profile/', views.Agent_profile,name="agent"),
    path("agent_update/<int:id>/",views.Agent_update,name="agent_update"),  # Include the app's URLs
    path("properties/", views.property_list, name="property_list"),
    path("login/", views.agent_login, name="agent_login"),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
