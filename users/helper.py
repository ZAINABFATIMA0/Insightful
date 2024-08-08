import requests

from social_django.models import UserSocialAuth


class FacebookClient:

    page_insights_metrices = [
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

    post_insights_metrices = [
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

    def get_user_access_token_and_id(user):
        try:
            social = user.social_auth.get(provider='facebook')
            access_token = social.extra_data['access_token']
            user_id = social.extra_data.get('id', None)
            return access_token, user_id
        except UserSocialAuth.DoesNotExist:
            return None

    def get_facebook_page_info(user):
        access_token, user_id = FacebookClient.get_user_access_token_and_id(user)

        if not access_token or not user_id:
            return None

        url = f"https://graph.facebook.com/{user_id}/accounts"
        params = {'access_token': access_token}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()
        if 'data' not in data or len(data['data']) == 0:
            return None

        page_info = data['data'][0]
        return page_info.get('access_token'), page_info.get('id')

    def validate_page_metrics(requested_metrics):
        invalid_metrics = [
            metric for metric in requested_metrics if metric not in FacebookClient.page_insights_metrices
        ]
        if invalid_metrics:
            return False, invalid_metrics
        return True, None
    
    def get_facebook_posts(user):
        access_token, page_id = FacebookClient.get_facebook_page_info(user)
        if not access_token or not page_id:
            return None

        url = f"https://graph.facebook.com/{page_id}/posts"
        params = {'access_token': access_token}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return None

        return response.json()

    def validate_post_metrics(requested_metrics):
        invalid_metrics = [
            metric for metric in requested_metrics if metric not in FacebookClient.post_insights_metrices
        ]
        if invalid_metrics:
            return False, invalid_metrics
        return True, None
