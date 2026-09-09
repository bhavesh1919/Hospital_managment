from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatMessage(models.Model):
    sender =models.ForeignKey(
        User,on_delete = models.CASCADE,
        related_name="sent_messages"
    )

    receiver =models.ForeignKey(
        User,on_delete = models.CASCADE,
        related_name="received_messages"
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read =   models.BooleanField(default=False)


    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"


    ##PHASE 1
# ✓ WebSocket connection
# ✓ Patient ↔ Doctor
# ✓ Send message
# ✓ Receive message
# ✓ Save message

# PHASE 2
# □ Load old messages
# □ Chat history
# □ Unread messages
# □ Read/unread status
# □ Online/offline status
# □ Typing indicator

# PHASE 3
# □ Doctor dashboard → Chat button
# □ Patient dashboard → Chat button
# □ Only authorized patient/doctor can chat
# □ Better UI
# □ Notifications

# PHASE 4
# □ Redis
# □ Production WebSocket configuration
# □ Secure wss://