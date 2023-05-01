from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification_chef_service

def notification_count_recouvrement(request):
    notifications = Notification_chef_service.objects.filter(read=False).order_by('-created_at')
    count = notifications.count()
    
    return dict(notification_count_recouvrement=count)
