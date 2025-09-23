from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):
    """
    Permission : permet uniquement à un utilisateur de voir/éditer ses propres objets
    """

    def has_object_permission(self, request, view, obj):
        # Suppose que chaque objet a un champ "owner" (ou "user")
        return obj.user == request.user
