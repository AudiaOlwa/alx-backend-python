from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
# Create your views here.


# -------------------------
# Conversation ViewSet
# -------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """Créer une nouvelle conversation avec participants"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="add-message")
    def add_message(self, request, pk=None):
        """Envoyer un message dans une conversation existante"""
        conversation = self.get_object()
        data = request.data.copy()
        data["conversation"] = str(conversation.conversation_id)

        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation, sender=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -------------------------
# Message ViewSet
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related("sender", "conversation").all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """Envoyer un nouveau message (endpoint générique)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(sender=request.user)
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED,
        )
