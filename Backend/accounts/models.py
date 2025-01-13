from django.db import models
import random
import string

class UserCollection(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    
    def generate_unique_name(self):
        """Generate a random unique collection name."""
        length = 10  # Length of the random name
        while True:
            name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            if not UserCollection.objects.filter(name=name).exists():
                break
        return name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.generate_unique_name()
        super().save(*args, **kwargs)