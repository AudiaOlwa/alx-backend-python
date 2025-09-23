import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    # Filtrer par utilisateur (expéditeur)
    sender = django_filters.NumberFilter(field_name="sender__id", lookup_expr="exact")

    # Filtrer par conversation
    conversation = django_filters.NumberFilter(field_name="conversation__id", lookup_expr="exact")

    # Filtrer par intervalle de date
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["sender", "conversation", "start_date", "end_date"]
