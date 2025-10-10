from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):
    """
    Permission : permet uniquement à un utilisateur de voir/éditer ses propres objets
    """

    def has_object_permission(self, request, view, obj):
        # Suppose que chaque objet a un champ "owner" (ou "user")
        return obj.user == request.user
#--
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Autorise uniquement :
    - Utilisateurs authentifiés
    - Participants de la conversation à envoyer, voir, modifier et supprimer des messages
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l’utilisateur est participant avant les actions sensibles
        """
        # Identifier la conversation (cas Message ou Conversation)
        if hasattr(obj, "participants"):  # Conversation
            participants = obj.participants.all()
        elif hasattr(obj, "conversation"):  # Message
            participants = obj.conversation.participants.all()
        else:
            return False

        # Autoriser seulement si l’utilisateur est participant
        if request.user not in participants:
            return False

        # Actions protégées (lecture et écriture)
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return True

        return False