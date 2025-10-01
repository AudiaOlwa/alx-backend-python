from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Supprimer le compte utilisateur connecté.
    Cela déclenche automatiquement le signal post_delete
    qui nettoie les données liées.
    """
    user = request.user
    username = user.username
    user.delete()
    return Response({"message": f"L'utilisateur {username} a été supprimé avec ses données associées."})
