from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.views import APIView

class MessageListView(APIView):
    """
    View to list, create, and delete messages for a user in a conversation.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get the list of messages for the authenticated user's conversations.
        """
        messages = Message.objects.filter(conversation__user=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new message in a conversation for the authenticated user.
        """
        conversation_id = request.data.get('conversation_id')
        if not conversation_id:
            return Response({"detail": "Conversation ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(conversation=conversation)

            conversation_serializer = ConversationSerializer(conversation)
            return Response(conversation_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, *args, **kwargs):
        """
        Delete a message from the authenticated user's conversation.
        """
        try:
            message = Message.objects.get(id=request.data['id'], conversation__user=request.user)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response({'detail': "Message not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)






class ConversationListView(APIView):
    """
    View to list, create, update, and delete conversations for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get the list of conversations for the authenticated user.
        """
        conversations = Conversation.objects.filter(user=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new conversation for the authenticated user.
        """
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save(user=request.user)
            return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete a conversation for the authenticated user.
        """
        try:
            conversation = Conversation.objects.get(id=request.data['id'], user=request.user)
            conversation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found or you don\'t have permission.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        """
        Update conversations (set token_valid=False) for the authenticated user.
        """
        updated_count = Conversation.objects.filter(user=request.user).update(token_valid=False)
        return Response({'detail': f'{updated_count} conversations updated.'}, status=status.HTTP_200_OK)
