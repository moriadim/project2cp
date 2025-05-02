from django.urls import re_path
from core import consumers

websocket_urlpatterns = [
    # Pattern for assistants to connect - each assistant connects to their own endpoint
    re_path(r'ws/assistant/(?P<assistant_id>\w+)/$',
            consumers.AssistantConsumer.as_asgi()),

    re_path(r'ws/assistance/(?P<assistance_id>\w+)/$',
            consumers.AssistanceConsumer.as_asgi())

]
