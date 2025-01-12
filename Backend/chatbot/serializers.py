from rest_framework import serializers
from .models import Message, Conversation

class MessageSerializer(serializers.ModelSerializer):
    # Use `conversation_id` to link the conversation in the request data
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(), 
        source='conversation',  # This refers to the related `conversation` field
        write_only=True  # This field won't be included in the response
    )

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'conversation', 'conversation_id']
        read_only_fields = ['timestamp', 'conversation']  # Make `timestamp` and `conversation` read-only

    def create(self, validated_data):
        # `conversation` is retrieved from `conversation_id` field
        conversation = validated_data.pop('conversation')
        # Create a new message associated with the conversation
        message = Message.objects.create(conversation=conversation, **validated_data)
        return message
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'created_at', 'messages']
