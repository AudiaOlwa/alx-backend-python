from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


# On ajoute le signal pre_save pour stocker l’ancien contenu avant modification.
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Signal pour logger les éditions de messages"""
    if instance.pk:  # si le message existe déjà
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_message.content != instance.content:
            # Sauvegarder l'ancien contenu
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content,
                edited_by=instance.edited_by
            )
            instance.edited = True  # marquer comme édité

# Supprimer les données liées à l’utilisateur supprimé
@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    
    # Supprimer tous les messages envoyés ou reçus
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Supprimer toutes ses notifications
    Notification.objects.filter(user=instance).delete()

    # Supprimer ses historiques d’édition
    MessageHistory.objects.filter(edited_by=instance).delete()