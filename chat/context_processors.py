from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def notification_count(request):
    channel_layer = get_channel_layer()
    notifications = Notification.objects.filter(read=False).order_by('-created_at')
    count = notifications.count()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {"type": "send_notification", "count": count},
    )
    return dict(notification_count=count)
