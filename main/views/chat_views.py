from rest_framework import status
from rest_framework.decorators import ( api_view, permission_classes)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from pipelines.SimpleRag import RagPipeline
from pipelines.Neo4jPipeline import Neo4jPipeline

from main.models import Chatbots
from utils.LLM_Guard import LLMGuard

@api_view(["POST"])
@permission_classes([AllowAny])
def chat(request, chatbotname):
    try:
        if request.session.session_key is None:
            request.session.create()

        query = request.data.get("query")

        try:
            chatbot = Chatbots.objects.get(name=chatbotname)
        except Chatbots.DoesNotExist:
            return Response(
                {"message": "Chatbot not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
        flag = LLMGuard(query)
        
        if flag:
            return Response(
                {"message": "Inappropriate Query Detected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        prompt = chatbot.prompt
        
        if chatbot.model_type == Chatbots.ModelType.SIMPLE:
            pipeline = RagPipeline()
            response = pipeline.generate_history_chat_response(query, chatbotname, request, prompt )
            return Response({"response": response}, status=status.HTTP_200_OK)
        elif chatbot.model_type == Chatbots.ModelType.ADVANCED:
            pipline = Neo4jPipeline()
            response = pipline.generate_history_chat_response(query, request, chatbotname , prompt)
            return Response({"response": response}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
                {"message": f"{e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["POST"])
@permission_classes([AllowAny])
def public_chat(request, chatbotname):
    try:
        
        if request.session.session_key is None:
            request.session.create()

        query = request.data.get("query")

        try:
            chatbot = Chatbots.objects.get(name=chatbotname)
        except Chatbots.DoesNotExist:
            return Response(
                {"message": "Chatbot not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
        if chatbot.isPublic == False:
            return Response(
                {"message": "Chatbot not Public"}, status=status.HTTP_404_NOT_FOUND
            )
        
        flag = LLMGuard(query)
        
        if flag:
            return Response(
                {"message": "Inappropriate Query Detected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        prompt = chatbot.prompt
        
        if chatbot.model_type == Chatbots.ModelType.SIMPLE:
            pipeline = RagPipeline()
            response = pipeline.generate_history_chat_response(query, chatbotname, request, prompt )
            return Response({"response": response}, status=status.HTTP_200_OK)
        elif chatbot.model_type == Chatbots.ModelType.ADVANCED:
            pipline = Neo4jPipeline()
            response = pipline.generate_history_chat_response(query, request, chatbotname , prompt)
            return Response({"response": response}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(
                {"message": f"{e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

