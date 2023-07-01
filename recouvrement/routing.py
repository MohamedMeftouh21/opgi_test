from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # Add more WebSocket URL patterns here
 path('ws/montant_mensuel/', consumers.MontantMensuelConsumer.as_asgi()),
    path('ws/montant_mensuel_updates/<str:unit>/', consumers.MontantMensuelConsumer_by_unite.as_asgi()),
    path('ws/montant_mensuel_updates_anne/<str:unit>/<int:anne>/', consumers.MontantMensuelConsumer_by_anne.as_asgi()),
    path('ws/chef_service/', consumers.ChefServiceConsumer.as_asgi()),
]