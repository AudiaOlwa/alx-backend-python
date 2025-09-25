import logging
from datetime import datetime
import os
from django.conf import settings
import time
from django.http import JsonResponse
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
#--
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

#--
class OffensiveLanguageMiddleware:
    """
    Middleware qui limite le nombre de messages envoyés par IP.
    Max 5 messages par minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_times = {}
        self.TIME_WINDOW = 60  # secondes
        self.MAX_MESSAGES = 5  # messages par fenêtre

    def __call__(self, request):
        # Appliquer uniquement sur POST /api/messages/
        if request.path.startswith("/api/messages/") and request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()
            timestamps = self.ip_message_times.get(ip, [])
            # Supprimer les timestamps hors de la fenêtre
            timestamps = [t for t in timestamps if now - t < self.TIME_WINDOW]

            if len(timestamps) >= self.MAX_MESSAGES:
                return JsonResponse(
                    {"detail": "Message rate limit exceeded. Try again later."},
                    status=429,
                )

            timestamps.append(now)
            self.ip_message_times[ip] = timestamps

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

#---
class RolePermissionMiddleware:
    """
    Middleware qui vérifie que l'utilisateur a le rôle admin ou moderator
    avant d'autoriser certaines actions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exemple : appliquer uniquement sur certaines routes sensibles
        restricted_paths = [
            "/api/conversations/",
            "/api/messages/",
        ]

        if any(request.path.startswith(p) for p in restricted_paths):
            user = request.user
            # Vérifier que l'utilisateur est authentifié et a le rôle requis
            if not user.is_authenticated or user.role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"detail": "You do not have permission to perform this action."},
                    status=403
                )

        # Continuer le traitement normal
        response = self.get_response(request)
        return response