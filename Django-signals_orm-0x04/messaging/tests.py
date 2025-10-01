from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class SignalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="pass123")
        self.user2 = User.objects.create_user(username="bob", password="pass123")

    def test_message_creates_notification(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello Bob!"
        )

        # Vérifie que la notification est bien créée
        notification = Notification.objects.filter(user=self.user2, message=message).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)

# Un test qui vérifie qu’un historique est créé quand un message est modifié.

class MessageEditSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="pass123")
        self.user2 = User.objects.create_user(username="bob", password="pass123")
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello Bob!"
        )

    def test_edit_message_creates_history(self):
        # Modifier le message
        self.message.content = "Hello Bob! How are you?"
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Hello Bob!")
        self.assertTrue(self.message.edited)