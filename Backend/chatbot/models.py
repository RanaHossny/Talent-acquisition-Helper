from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} created at {self.created_at} by {self.user.username}"

class Message(models.Model):
    sender = models.CharField(max_length=10)  # e.g., 'user' or 'bot'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"

