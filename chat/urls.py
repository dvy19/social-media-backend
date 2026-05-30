# chat/urls.py

from django.urls import path
from .views import CreateConversationAPIView, GetMessagesAPIView, SendMessageAPIView

urlpatterns = [

    path(
        "create-conversation/",
        CreateConversationAPIView.as_view()
    ),

    path(
    "send-message/",
    SendMessageAPIView.as_view()
    ),
    
    path(
    "messages/<int:conversation_id>/",
    GetMessagesAPIView.as_view()
)

]