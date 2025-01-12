from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer

# Ensure the view only accepts requests from authenticated users
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])  
def message_list(request):
    if request.method == 'GET':
        # Get messages belonging to the authenticated user's conversations
        messages = Message.objects.filter(conversation__user=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        conversation_id = request.data.get('conversation_id')
        if not conversation_id:
            return Response({"detail": "Conversation ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure the conversation belongs to the authenticated user
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(conversation=conversation)

            # Return the conversation with the updated messages list
            conversation_serializer = ConversationSerializer(conversation)
            return Response(conversation_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            message = Message.objects.get(id=request.data['id'], conversation__user=request.user)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response({'detail': "Message not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def conversation_list(request):

    if request.method == 'GET':
        # Get conversations belonging to the authenticated user
        conversations = Conversation.objects.filter(user=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save(user=request.user)
            return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            conversation = Conversation.objects.get(id=request.data['id'], user=request.user)
            conversation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found or you don\'t have permission.'}, status=status.HTTP_404_NOT_FOUND)
