from .views import message_list, conversation_list
from django.urls import path

urlpatterns = [
     path('messages/', message_list, name='message-list'),  # Message list: GET, POST, DELETE
    path('conversations/', conversation_list, name='conversation-list'),  # Conversation list: GET, POST, DELETE

]
