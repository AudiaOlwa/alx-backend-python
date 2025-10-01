from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Message
# Create your views here.

@cache_page(60)  # cache pendant 60 secondes
def conversation_view(request, user_id):
    messages = Message.objects.filter(receiver_id=user_id).select_related("sender")
    return render(request, "chats/conversation.html", {"messages": messages})
