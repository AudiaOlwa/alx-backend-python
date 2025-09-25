import logging
from datetime import datetime

# Configure un logger pour écrire dans requests.log
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")  # le fichier sera à la racine du projet
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Récupérer l’utilisateur (ou "Anonymous" s’il n’est pas connecté)
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Créer un log
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Continuer le traitement normal
        response = self.get_response(request)
        return response
