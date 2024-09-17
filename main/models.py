from django.db import models
from django.contrib.auth.models import User

class Chatbots(models.Model):
    class ModelType(models.TextChoices):
        SIMPLE = 'simple', 'Simple'
        ADVANCED = 'advanced', 'Advanced'

    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(null=True, blank=True, default=None) 
    isPublic = models.BooleanField(default=False)
    prompt = models.TextField(null=True, blank=True, default=None) 
    model_type = models.CharField(
        max_length=10, 
        choices=ModelType.choices, 
        default=ModelType.SIMPLE 
    )

    def __str__(self):
        return self.name

class Documents(models.Model):
    documentname = models.TextField()
    chatbot = models.ForeignKey(Chatbots, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('documentname', 'chatbot')
        
    def __str__(self):
        return self.documentname