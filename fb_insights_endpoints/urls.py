from django.urls import path
from .views import facebook_insights_view, facebook_posts_view, facebook_post_metrics_view

urlpatterns = [
    path('insights/<str:page_id>/', facebook_insights_view, name='facebook_insights'),
    path('posts/<str:page_id>/', facebook_posts_view, name='facebook_posts'),
    path('post_metrics/<str:post_id>/', facebook_post_metrics_view, name='facebook_post_metrics'),
]
