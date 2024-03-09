# from django.urls import path
# from . import consumers
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
#
# websocket_urlpatterns = [
#     path('ws/direct_chat/<int:user_id>/', consumers.DirectChatConsumer.as_asgi()),
#     path('ws/group_chat/<int:team_id>/', consumers.GroupChatConsumer.as_asgi()),
# ]
#
# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })