from rest_framework import serializers
from .models import User, Conversation, Message


# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    # Exemple explicite d’un CharField
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
            "full_name",
        ]


# -------------------------
# Message Serializer
# -------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # Exemple de champ calculé avec SerializerMethodField
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
            "preview",
        ]

    def get_preview(self, obj):
        """Retourne les 30 premiers caractères du message comme aperçu"""
        return obj.message_body[:30]


# -------------------------
# Conversation Serializer
# -------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]

    # Exemple d’utilisation de ValidationError
    def validate_participants(self, value):
        """Vérifie qu’il y a au moins 2 participants dans une conversation"""
        if len(value) < 2:
            raise serializers.ValidationError(
                "Une conversation doit avoir au moins deux participants."
            )
        return value
