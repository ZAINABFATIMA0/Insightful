from django.contrib import admin
from django.urls import path, include

from fb_logging import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.login_api, name='api-login'),
    path('api/home/', views.home_api, name='api-home'),
    path('api/social-auth/', include('social_django.urls', namespace='social')),
    path('api/', include('get_insights.urls')),
]
