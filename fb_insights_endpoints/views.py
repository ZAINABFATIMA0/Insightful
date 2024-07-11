import requests

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def facebook_insights_view(request, page_id):

    access_token = request.GET.get('access_token')
    metrics_param = request.GET.get('metrics')

    if not page_id or not access_token:
        return JsonResponse(
            {'error': 'Missing page_id or access_token'}, status=400
            )

    url = f"https://graph.facebook.com/{page_id}/insights"

    all_metrics = [
        'page_total_actions',
        'page_cta_clicks_logged_in_total',
        'page_cta_clicks_logged_in_unique',
        'page_get_directions_clicks_logged_in_unique',
        'page_website_clicks_logged_in_unique',
        'page_post_engagements',
        'page_consumptions_unique',
        'page_consumptions_by_consumption_type',
        'page_consumptions_by_consumption_type_unique',
        'page_places_checkin_total',
        'page_places_checkin_total_unique',
        'page_negative_feedback',
        'page_negative_feedback_unique',
        'page_negative_feedback_by_type',
        'page_negative_feedback_by_type_unique',
        'page_fans_online',
        'page_fans_online_per_day',
        'page_fan_adds_by_paid_non_paid_unique',
        'page_lifetime_engaged_followers_unique',
        'page_daily_follows',
        'page_daily_follows_unique',
        'page_daily_unfollows_unique',
        'page_follows',
        'page_impressions',
        'page_impressions_unique',
        'page_impressions_paid',
        'page_impressions_paid_unique',
        'page_impressions_organic_v2',
        'page_impressions_organic_unique_v2',
        'page_impressions_viral',
        'page_impressions_viral_unique',
        'page_impressions_nonviral',
        'page_impressions_nonviral_unique',
        'page_impressions_by_story_type',
        'page_impressions_by_story_type_unique',
        'page_impressions_by_city_unique',
        'page_impressions_by_country_unique',
        'page_impressions_by_locale_unique',
        'page_impressions_by_age_gender_unique',
        'page_impressions_viral_frequency_distribution'
    ]

    if metrics_param:
        requested_metrics = metrics_param.split(',')
        invalid_metrics = [metric for metric in requested_metrics if metric not in all_metrics]
        if invalid_metrics:
            return JsonResponse(
                {'error': f'Invalid metrics requested: {", ".join(invalid_metrics)}'}, status=400
                )
        metrics = requested_metrics
    else:
        metrics = all_metrics

    params = {
        'metric': ','.join(metrics),
        'access_token': access_token
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return JsonResponse(
            {'error': 'Failed to fetch insights from Facebook'}, status=response.status_code
            )

    return JsonResponse(response.json(), status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def facebook_posts_view(request, page_id):
    access_token = request.GET.get('access_token')

    if not page_id or not access_token:
        return JsonResponse(
            {'error': 'Missing page_id or access_token'}, status=400
            )

    url = f"https://graph.facebook.com/{page_id}/posts"

    params = {
        'access_token': access_token,
        'fields': 'id,message,created_time'
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return JsonResponse(
            {'error': 'Failed to fetch posts from Facebook'}, status=response.status_code
            )

    return JsonResponse(response.json(), status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def facebook_post_metrics_view(request, post_id):

    access_token = request.GET.get('access_token')
    metrics_param = request.GET.get('metrics')

    if not post_id or not access_token:
        return JsonResponse(
            {'error': 'Missing post_id or access_token'}, status=400
            )

    all_metrics = [
        'page_posts_impressions',
        'page_posts_impressions_unique',
        'page_posts_impressions_paid',
        'page_posts_impressions_paid_unique',
        'page_posts_impressions_organic',
        'page_posts_impressions_organic_unique',
        'page_posts_served_impressions_organic_unique',
        'page_posts_impressions_viral',
        'page_posts_impressions_viral_unique',
        'page_posts_impressions_nonviral',
        'page_posts_impressions_nonviral_unique',
        'post_engaged_users',
        'post_negative_feedback',
        'post_negative_feedback_unique',
        'post_negative_feedback_by_type',
        'post_negative_feedback_by_type_unique',
        'post_engaged_fan',
        'post_clicks',
        'post_clicks_unique',
        'post_clicks_by_type',
        'post_clicks_by_type_unique',
        'post_impressions',
        'post_impressions_unique',
        'post_impressions_paid',
        'post_impressions_paid_unique',
        'post_impressions_fan',
        'post_impressions_fan_unique',
        'post_impressions_organic',
        'post_impressions_organic_unique',
        'post_impressions_viral',
        'post_impressions_viral_unique',
        'post_impressions_nonviral',
        'post_impressions_nonviral_unique',
        'post_impressions_by_story_type',
        'post_impressions_by_story_type_unique',
        'post_impressions_by_paid_non_paid',
        'post_reactions_like_total',
        'post_reactions_love_total',
        'post_reactions_wow_total',
        'post_reactions_haha_total',
        'post_reactions_sorry_total',
        'post_reactions_anger_total',
        'post_reactions_by_type_total'
    ]

    if metrics_param:
        requested_metrics = metrics_param.split(',')
        invalid_metrics = [metric for metric in requested_metrics if metric not in all_metrics]
        if invalid_metrics:
            return JsonResponse(
                {'error': f'Invalid metrics requested: {", ".join(invalid_metrics)}'}, status=400
                )
        metrics = requested_metrics
    else:
        metrics = all_metrics

    params = {
        'metric': ','.join(metrics),
        'access_token': access_token
    }

    url = f"https://graph.facebook.com/{post_id}/insights"
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return JsonResponse(
            {'error': 'Failed to fetch post metrics from Facebook'}, status=response.status_code
            )

    return JsonResponse(response.json(), status=200)
