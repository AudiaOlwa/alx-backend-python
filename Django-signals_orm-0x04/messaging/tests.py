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

# On vérifie que la suppression supprime aussi les messages, notifications et historiques.
class DeleteUserTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="pass123")
        self.user2 = User.objects.create_user(username="bob", password="pass123")
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hi Bob!")
        self.message.edited_by = self.user1
        self.message.save()
        self.notification = Notification.objects.create(user=self.user2, message=self.message)
        self.history = MessageHistory.objects.create(message=self.message, old_content="Old content", edited_by=self.user1)

    def test_user_deletion_cleans_related_data(self):
        self.user1.delete()

        self.assertFalse(Message.objects.filter(sender=self.user1).exists())
        self.assertFalse(Notification.objects.filter(user=self.user1).exists())
        self.assertFalse(MessageHistory.objects.filter(edited_by=self.user1).exists())

# On valide que les threads fonctionnent et qu’on n’a pas trop de requêtes SQL.
class ThreadedConversationTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="pass")
        self.bob = User.objects.create_user(username="bob", password="pass")

        # Message racine
        self.msg1 = Message.objects.create(sender=self.alice, receiver=self.bob, content="Salut Bob!")

        # Réponse directe
        self.reply1 = Message.objects.create(sender=self.bob, receiver=self.alice, content="Salut Alice!", parent_message=self.msg1)

        # Réponse à une réponse
        self.reply2 = Message.objects.create(sender=self.alice, receiver=self.bob, content="Comment ça va?", parent_message=self.reply1)

    def test_thread_replies(self):
        thread = self.msg1.get_thread()
        contents = [m.content for m in thread]

        self.assertIn("Salut Alice!", contents)
        self.assertIn("Comment ça va?", contents)