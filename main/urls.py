from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("<str:chatbotname>/adddocument/", adddocument),
    path("<str:chatbotname>/getdocuments/", getdocumentsname),
    path("<str:chatbotname>/deletedocument/", deletedocument),
    path("<str:chatbotname>/deletechatbot/", deletechatbot),
    
    path("<str:chatbotname>/chat/",  chat),
    path("<str:chatbotname>/publicchat/",  public_chat, name="publicChat"),
    
    path("logout/",  logout_view, name="logout"),
    path("login/",  login_api, name="login"),
    path("signup/",  signup_api, name="signup"),
    
    path("createchatbot/",  create_chatbot, name="createChatbot"),
    path("updatechatbot/",  update_chatbot, name="updateChatbot"),
    path("getallchatbots/",  all_chatbots, name="getallChatbots"),
    path("<str:chatbotname>/getchatbotdata/",  getchatbotdata),
    path("chatbotbyuser/",  chatbots_by_user, name="chatbotByUser"),
]
