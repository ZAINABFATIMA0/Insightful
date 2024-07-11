from django.contrib import admin
from django.urls import path, include

from fb_logging import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/', include('fb_logging.urls')),
    path('api/v1/', include('fb_insights_endpoints')),
    path('api/social-auth/', include('social_django.urls', namespace='social')),

]
