from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import UnreadMessagesManager


class MessageManager(models.Manager):
    def conversation(self, user1, user2):
        return (
            self.filter(
                (models.Q(sender=user1, receiver=user2) | models.Q(sender=user2, receiver=user1)),
                parent_message__isnull=True
            )
            .select_related("sender", "receiver")
            .prefetch_related("replies__sender", "replies__receiver")
        )

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # Récupère seulement les messages non lus du user
        return (
            self.filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")  # optimisation
        )


class Message(models.Model):
    objects = MessageManager()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False) # identifie si le message est en cours de modification
    edited_by = models.ForeignKey(  
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_messages"
    )
    # Ajout pour threads
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    read = models.BooleanField(default=False)

    # ✅ Managers
    objects = models.Manager()  # Manager par défaut
    unread = UnreadMessagesManager()  # Manager custom

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {'Read' if self.read else 'Unread'}"

    

    def get_thread(self):
        """
        Récupère récursivement toutes les réponses à ce message
        """
        thread = []
        for reply in self.replies.all().select_related("sender", "receiver").prefetch_related("replies"):
            thread.append(reply)
            thread.extend(reply.get_thread())
        return thread


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} about message {self.message.id}"
# Enrégistrer les anciens messages avant les modifications
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(  # ✅ log l’éditeur
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="message_edits"
    )

    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"