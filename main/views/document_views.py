from rest_framework import status
from rest_framework.decorators import ( api_view, permission_classes)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from main.serializers import  DocumentSerializer

from pipelines.SimpleRag import RagPipeline
from pipelines.Neo4jPipeline import Neo4jPipeline

from main.models import Chatbots, Documents


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def adddocument(request, chatbotname):
    try:
        try:
            chatbot = Chatbots.objects.get(name=chatbotname)
        except Chatbots.DoesNotExist:
            return Response(
                {"message": "Chatbot not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if chatbot.user != request.user:
            return Response(
                {"message": "Not Authorized for this Chatbot"},
                status=status.HTTP_404_NOT_FOUND,
            )

        docs = request.FILES.get("docs")

        if not docs:
            return Response(
                {"message": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            new_docs = Documents.objects.create(documentname=docs.name, chatbot=chatbot)
        except Exception as E:
            return Response(
                {"message": "Same Document is Already Present"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        #executor.submit(save_embeddings_advance, docs, chatbotname, docs.name)
        try:
            if chatbot.model_type == Chatbots.ModelType.SIMPLE:
                pipeline = RagPipeline()
                pipeline.save_embeddings_pipeline(docs, chatbotname)
            elif chatbot.model_type == Chatbots.ModelType.ADVANCED:
                pipeline = Neo4jPipeline()
                pipeline.save_embeddings_pipeline(docs, chatbotname,docs.name)
                
        except Exception as e:
            new_docs.delete()
            print(e.args[0])
            return Response(
                {"message": "Error in saving embeddings"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        serializer = DocumentSerializer(new_docs)

        return Response(
            {"message": "Embeddings saved successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        print(e.args[0])
        return Response(
            {"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getdocumentsname(request, chatbotname):

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

    docs = Documents.objects.filter(chatbot=chatbot)
    serializer = DocumentSerializer(docs, many=True)

    return Response(
        {"message": "Documents fetched successfully", "data": serializer.data},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deletedocument(request, chatbotname):

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

    documentname = request.data.get("documentname")

    try:
        document = Documents.objects.get(documentname=documentname, chatbot=chatbot)
    except Documents.DoesNotExist:
        return Response(
            {"message": "Document not found"}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        if chatbot.model_type == Chatbots.ModelType.SIMPLE:
            pipeline = RagPipeline()
            pipeline.delete_embeddings(chatbotname, documentname)
            document.delete()
        elif chatbot.model_type == Chatbots.ModelType.ADVANCED:
            pipeline = Neo4jPipeline()
            pipeline.deleteAdvanceDocument(chatbotname ,documentname)
            document.delete()
    except Exception as e:
        print(f"Error is deleting document : {e}")
        return Response(
            {"message": "Error in deleting Docement"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {"message": "Document deleted successfully"}, status=status.HTTP_200_OK
    )
