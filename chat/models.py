from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message sent from {self.sender} to {self.recipient}"

    class Meta:
        ordering = ['timestamp']



class Post(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.TextField()
    profile_pic = models.ImageField(default='profile_pics/avatar.png', upload_to='profile_pics')
    def __str__(self):
       return f"{self.profile} post {self.about}"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_pic:
            try:
                img = Image.open(self.profile_pic.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_pic.path)
            except IOError as e:
                print(f"Error processing image for {self.profile}: {e}")