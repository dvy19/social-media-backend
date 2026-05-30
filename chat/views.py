from email.message import Message

from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
# Create your views here.
# chat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import MessageSerializer

from .models import Conversation


class CreateConversationAPIView(APIView):

    def post(self, request):

        current_user = request.user

        other_user_id = request.data.get("id")

        try:
            other_user = settings.AUTH_USER_MODEL.objects.get(
                id=other_user_id
            )

        except settings.AUTH_USER_MODEL.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        conversation = Conversation.objects.filter(
            participants=current_user
        ).filter(
            participants=other_user
        ).first()

        if conversation:
            return Response({
                "conversation_id": conversation.id
            })

        conversation = Conversation.objects.create()

        conversation.participants.add(
            current_user,
            other_user
        )

        return Response({
            "conversation_id": conversation.id
        })
    
class SendMessageAPIView(APIView):

    def post(self, request):

        conversation_id = request.data.get(
            "conversation_id"
        )

        text = request.data.get(
            "text"
        )

        try:
            conversation = Conversation.objects.get(
                id=conversation_id
            )

        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=404
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            text=text
        )

        serializer =    MessageSerializer(
            message
        )

        return Response(
            serializer.data
        )
    
class GetMessagesAPIView(APIView):

    def get(
        self,
        request,
        conversation_id
    ):

        messages = Message.objects.filter(
            conversation_id=conversation_id
        ).order_by("created_at")

        serializer = MessageSerializer(
            messages,
            many=True
        )

        return Response(
            serializer.data
        )