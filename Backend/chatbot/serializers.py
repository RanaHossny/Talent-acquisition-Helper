from rest_framework import serializers
from .models import Message, Conversation

class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(), 
        source='conversation',  
        write_only=True  
    )

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'conversation', 'conversation_id']
        read_only_fields = ['timestamp', 'conversation']  
    def create(self, validated_data):
        conversation = validated_data.pop('conversation')
        message = Message.objects.create(conversation=conversation, **validated_data)
        return message
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'created_at', 'messages', 'token_valid']
