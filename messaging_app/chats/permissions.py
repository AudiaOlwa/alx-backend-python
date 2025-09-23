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
    Permission qui :
    - Autorise uniquement les utilisateurs authentifiés
    - Vérifie que l'utilisateur fait partie de la conversation
    """

    def has_permission(self, request, view):
        # Autoriser seulement les utilisateurs connectés
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l’utilisateur est participant de la conversation.
        On suppose que Conversation a un champ participants = ManyToMany(User).
        Et que Message est lié à Conversation par un FK.
        """
        if hasattr(obj, "participants"):  # Cas Conversation
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):  # Cas Message
            return request.user in obj.conversation.participants.all()

        return False