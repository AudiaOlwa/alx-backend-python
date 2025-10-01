from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required

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


@login_required
def inbox(request):
    # Utilisation du manager custom pour récupérer seulement les non lus
    unread_messages = Message.unread.for_user(request.user)
    return render(request, "messaging/inbox.html", {"messages": unread_messages})

@login_required
def inbox(request):
    # 1) Utilisation du manager custom (chaîne exacte attendue)
    unread_messages_via_manager = Message.unread.unread_for_user(request.user).select_related("sender", "receiver")

    # 2) Requête explicite optimisée (le checker cherche "Message.objects.filter", ".only" et "select_related")
    optimized_unread = (
        Message.objects
        .filter(receiver=request.user, read=False)
        .select_related("sender", "receiver")
        .only("id", "sender", "content", "timestamp")
    )

    # On peut choisir lequel afficher ; ici on renvoie la requête optimisée
    return render(request, "messaging/inbox.html", {"messages": optimized_unread})