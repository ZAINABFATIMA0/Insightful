from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.login_api, name='login'),
    path('facebook-page-insights/', views.facebook_insights_view, name='facebook_insights'),
    path('facebook-post-insights/', views.facebook_post_metrics_view, name='facebook_posts'),
]
