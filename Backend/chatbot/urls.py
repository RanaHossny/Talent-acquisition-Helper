from .views import MessageListView, ConversationListView
from django.urls import path

urlpatterns = [
     path('messages/', MessageListView.as_view(), name='message-list'),  # Message list: GET, POST, DELETE
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),  # Conversation list: GET, POST, DELETE

]
