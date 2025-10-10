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
    sender = serializers.SlugRelatedField(
        slug_field="user_id",  # On utilise le user_id comme identifiant
        queryset=User.objects.all()
    )
    conversation = serializers.SlugRelatedField(
        slug_field="conversation_id",  # On utilise le conversation_id comme identifiant
        queryset=Conversation.objects.all()
    )
    preview = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "conversation", "sender", "message_body", "sent_at", "preview"]

    def get_preview(self, obj):
        return obj.message_body[:30]


# -------------------------
# Conversation Serializer
# -------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participants_ids = serializers.SlugRelatedField(
        many=True,
        slug_field="user_id",          # 👈 ici on dit d’utiliser user_id au lieu de id
        queryset=User.objects.all(),   # 👈 DRF sait où chercher
        write_only=True,
        source="participants"          # 👈 relie ça au champ ManyToMany participants
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "participants_ids",
            "created_at",
            "messages",
        ]

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation

    # Exemple d’utilisation de ValidationError
    def validate_participants_ids(self, value):
    #"""Vérifie qu’il y a au moins deux participants"""
        if len(value) < 2:
            raise serializers.ValidationError(
            "Une conversation doit avoir au moins deux participants."
            )
        return value