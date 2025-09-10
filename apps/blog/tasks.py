from celery import shared_task

import logging
from .models import PostAnalytics

logger = logging.getLogger(__name__)

@shared_task
def increment_post_view(post_id):
    '''implement a task to increment post view count'''
    try:
        analytics, created = PostAnalytics.objects.get_or_create(post__id=post_id)
        analytics.increment_impressions()
        analytics.save()
    except Exception as e:
        logger.error(f"Error incrementing post view for post {post_id}: {str(e)}")