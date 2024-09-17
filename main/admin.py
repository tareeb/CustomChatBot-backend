from django.contrib import admin
from .models import Chatbots, Documents

class ChatbotsAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date_created' , "title" , "prompt" , "isPublic" , "model_type")
    
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('documentname', 'chatbot', 'date_created') 

admin.site.register(Chatbots , ChatbotsAdmin)
admin.site.register(Documents , DocumentsAdmin)
