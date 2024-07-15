import requests

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .helper import FacebookClient

@api_view(['GET'])
def login_api(request):
    return redirect(reverse('social:begin', args=['facebook']))

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def facebook_insights_view(request):
    
    user = request.user
    page_info = FacebookClient.get_facebook_page_info(user)

    if not page_info:
        return JsonResponse({'error': 'Failed to retrieve page access token or page ID'}, status=400)

    page_access_token, page_id = page_info
    metrics_param = request.GET.get('metrics')

    if metrics_param:
        requested_metrics = metrics_param.split(',')
        valid, invalid_metrics = FacebookClient.validate_page_metrics(requested_metrics)
        if not valid:
            return JsonResponse(
                {'error': f'Invalid metrics requested: {", ".join(invalid_metrics)}'}, status=400
            )
        metrics = requested_metrics
    else:
        metrics = FacebookClient.page_insights_metrices

    url = f"https://graph.facebook.com/{page_id}/insights"
    params = {
        'metric': ','.join(metrics),
        'access_token': page_access_token
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return JsonResponse(
            {'error': 'Failed to fetch insights from Facebook'}, status=response.status_code
        )

    return JsonResponse(response.json(), status=200)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def facebook_post_metrics_view(request):

    user = request.user

    page_info = FacebookClient.get_facebook_page_info(user)
    post_info = FacebookClient.get_facebook_posts(user)

    post_id = post_info['data'][0]['id']
    page_access_token = page_info[0]

    metrics_param = request.GET.get('metrics')

    if metrics_param:
        requested_metrics = metrics_param.split(',')
        valid, invalid_metrics = FacebookClient.validate_post_metrics(requested_metrics)
        if not valid:
            return JsonResponse(
                {'error': f'Invalid metrics requested: {", ".join(invalid_metrics)}'}, status=400
            )
        metrics = requested_metrics
    else:
        metrics = FacebookClient.post_insights_metrices

    url = f"https://graph.facebook.com/{post_id}/insights"
    params = {
        'metric': ','.join(metrics),
        'access_token': page_access_token
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return JsonResponse(
            {'error': 'Failed to fetch insights from Facebook'}, status=response.status_code
        )

    return JsonResponse(response.json(), status=200)






