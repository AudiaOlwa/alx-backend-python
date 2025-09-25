import logging
from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponseForbidden
# Logger pour écrire dans requests.log à la racine du projet
logger = logging.getLogger(__name__)
log_path = os.path.join(settings.BASE_DIR, "requests.log")
file_handler = logging.FileHandler(log_path)
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Récupérer l'utilisateur ou "Anonymous"
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Créer un log
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Continuer le traitement normal
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware qui restreint l'accès à certaines heures.
    Interdit l'accès aux vues de chat en dehors de 18h00 - 21h00.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Heure actuelle du serveur
        now = datetime.now()
        current_hour = now.hour

        # On interdit l'accès en dehors de 18h00 - 21h00
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Chat is accessible only between 18:00 and 21:00.")

        # Continuer le traitement normal
        response = self.get_response(request)
        return response