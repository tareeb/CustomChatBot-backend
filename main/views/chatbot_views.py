from rest_framework import status
from rest_framework.decorators import ( api_view, permission_classes)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from main.serializers import ChatbotSerializer , AllChatbotSerializer

from pipelines.SimpleRag import RagPipeline
from pipelines.Neo4jPipeline import Neo4jPipeline

from main.models import Chatbots

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_chatbot(request):
    
    try:
        username = request.user
        
        print(request.data)
        chatbot_name = request.data.get("chatbotname")
        title = request.data.get("title" , None)  
        prompt = request.data.get("prompt", None)  
        isPublic = request.data.get("isPublic", False)
        modeltype = request.data.get("modeltype")

        user = User.objects.get(username=username)
        chatbot = Chatbots.objects.create(name=chatbot_name, user=user, model_type=modeltype, 
                                        title=title, prompt=prompt , isPublic=isPublic)
        serializer = ChatbotSerializer(chatbot)

        if chatbot:
            return Response(
                {
                    "success": True,
                    "message": "Chatbot created successfully.",
                    "data": serializer.data,
                },
                status=201,
            )
        else:
            return Response(
                {"success": False, "message": "Failed to create chatbot."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Exception as e:
        print(e)
        return Response(
                {"success": False, "message": "Failed to create chatbot."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_chatbot(request):
    
    try:
        chatbotname = request.data.get("chatbotname")
        
        try:
            chatbot = Chatbots.objects.get(name=chatbotname)
        except Chatbots.DoesNotExist:
            return Response(
                {"message": "Chatbot not found"}, status=status.HTTP_404_NOT_FOUND
        )
            
        if chatbot.user != request.user:
            return Response(
                {"message": "Not authorized for this chatbot"},
                status=status.HTTP_404_NOT_FOUND,
        )
            
        chatbot.title      = request.data.get('title', chatbot.title)  
        chatbot.prompt     = request.data.get('prompt', chatbot.prompt)  
        chatbot.isPublic   = request.data.get('isPublic', chatbot.isPublic) 

        chatbot.save()
        serializer = ChatbotSerializer(chatbot)

        if chatbot:
            return Response(
                {
                    "success": True,
                    "message": "Chatbot Updated successfully.",
                    "data": serializer.data,
                },
                status=201,
            )
        else:
            return Response(
                {"success": False, "message": "Failed to Update chatbot."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Exception as e:
        print(e)
        return Response(
                {"success": False, "message": "Failed to Update chatbot."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def getchatbotdata(request, chatbotname):
    try:
        chatbot = Chatbots.objects.get(name=chatbotname)
        serializer = ChatbotSerializer(chatbot)
        return Response({"success": True, "data": serializer.data})

    except Chatbots.DoesNotExist:
        return Response(
            {"success": False, "message": "Chatbot does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {"success": False, "message": f"Could not fetch data: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        

@api_view(["GET"])
def all_chatbots(request):
    try:
        chatbots = Chatbots.objects.filter(isPublic=True)
        serializer = AllChatbotSerializer(chatbots, many=True)
        return Response({"success": True, "data": serializer.data})
    except Exception as e:
        print(e)
        return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def chatbots_by_user(request):
    try:
        username = request.user
        user = User.objects.get(username=username)
        chatbots = Chatbots.objects.filter(user=user)
        serializer = ChatbotSerializer(chatbots, many=True)
        return Response({"success": True, "data": serializer.data})
    except User.DoesNotExist:
        return Response(
            {"success": False, "message": "User does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deletechatbot(request, chatbotname):

    try:
        chatbot = Chatbots.objects.get(name=chatbotname)
    except Chatbots.DoesNotExist:
        return Response(
            {"message": "Chatbot not found"}, status=status.HTTP_404_NOT_FOUND
        )

    botname = request.data.get("chatbotname")
    if botname != chatbotname:
        return Response(
            {"message": "Chatbot name mismatch"}, status=status.HTTP_400_BAD_REQUEST
        )

    if chatbot.user != request.user:
        return Response(
            {"message": "Not authorized for this chatbot"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        if chatbot.model_type == Chatbots.ModelType.SIMPLE:
            pipeline = RagPipeline()
            pipeline.delete_collection(chatbotname)
            chatbot.delete()
        elif chatbot.model_type == Chatbots.ModelType.ADVANCED:
            pipeline = Neo4jPipeline()
            pipeline.deleteAdvanceChatbot(chatbotname)
            chatbot.delete()
    except Exception as e:
        print(f"Error in Deleting Chatbot : {e}")
        return Response(
            {"message": "Error in deleting chatbot"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {"message": "Chatbot deleted successfully"}, status=status.HTTP_200_OK
    )
