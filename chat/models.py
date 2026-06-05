from django.db import models
from django.conf import settings
# Create your models here.

class Conversation(models.Model):

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )

    '''
    User.id is the authentication ID.
    Profile.id is the profile record ID.
    Profile.user_id points to the User.
    '''

    '''
    with related name we can get,

    user = User.objects.get(id=1)
    user.conversations.all()

    all conversations of the user will be returned
    '''


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    '''
    with auto_now_add, the created_at field will be automatically set to the current date and time when the conversation is created.

    with auto_now, the updated_at field will be automatically set to the current date and time whenever the conversation is saved.

    This means that the created_at field will only be set once when the conversation is created, while the updated_at field will be updated every time the conversation is modified and saved.

    sorting can be done using these fields, for example, to get the most recent conversations, we can order by updated_at in descending order.

    Conversation.objects.all().order_by("-updated_at")
    '''

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.text