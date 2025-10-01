from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Message

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


def conversation_view(request, user_id):
    other_user = User.objects.get(pk=user_id)
    conversation = (
        Message.objects.filter(
            (Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)),
            parent_message__isnull=True
        )
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver")
    )
    return render(request, "messaging/conversation.html", {"conversation": conversation})
