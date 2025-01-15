from django.db import models
import random
import string

class UserCollection(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def generate_unique_name(self):
        """Generate a valid random unique collection name."""
        length = 10  # Total length of the collection name
        while True:
            # Ensure the first character is a letter or underscore
            first_char = random.choice(string.ascii_letters + '_')
            # Generate the remaining characters from letters and digits
            remaining_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 1))
            name = first_char + remaining_chars

            # Check if the name is unique
            if not UserCollection.objects.filter(name=name).exists():
                return name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.generate_unique_name()
        super().save(*args, **kwargs)