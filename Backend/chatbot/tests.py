from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Message, Conversation
from rest_framework_simplejwt.tokens import RefreshToken

class MessageAndConversationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.conversation = Conversation.objects.create(user=self.user)
        self.message = Message.objects.create(
            conversation=self.conversation,
            content="Hello, this is a test message."
        )

    def test_list_messages(self):
        """
        Test that an authenticated user can list messages.
        """
        response = self.client.get('/chatbot/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

    def test_create_message(self):
        """
        Test that an authenticated user can create a message in a conversation.
        """
        data = {
            'conversation_id': self.conversation.id,
            "sender": "chatbot",
            "content": "yes ,i can."
                  }
        response = self.client.post('/chatbot/messages/',data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_message_without_conversation_id(self):
        """
        Test that creating a message without a conversation ID returns an error.
        """
        data = {'content': "Missing conversation ID."}
        response = self.client.post('/chatbot/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Conversation ID is required.')

    def test_delete_message(self):
        """
        Test that an authenticated user can delete their own message.
        """
        data = {'id': self.message.id}
        response = self.client.delete('/chatbot/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_list_conversations(self):
        """
        Test that an authenticated user can list their conversations.
        """
        response = self.client.get('/chatbot/conversations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  


    def test_delete_conversation(self):
        """
        Test that an authenticated user can delete their own conversation.
        """
        data = {'id': self.conversation.id}
        response = self.client.delete('/chatbot/conversations/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_update_conversations(self):
        """
        Test that an authenticated user can update conversations (set token_valid=False).
        """
        response = self.client.put('/chatbot/conversations/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], '1 conversations updated.') 

