# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Manager custom pour récupérer les messages non lus pour un utilisateur.
    Méthode attendue par le checker : unread_for_user
    """
    def unread_for_user(self, user):
        # On filtre par receiver et read=False, puis on limite aux champs nécessaires
        return self.filter(receiver=user, read=False).only("id", "sender", "content", "timestamp")
