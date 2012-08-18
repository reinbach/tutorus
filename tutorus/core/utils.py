from django.conf import settings
from pubnub import Pubnub

def get_pubnub_connection():
    """Setup pubnub connection"""
    return Pubnub(
        settings.PUBNUB_PUBLISH_KEY,
        settings.PUBNUB_SUBSCRIBE_KEY,
        settings.PUBNUB_SECRET_KEY,
        True
    )