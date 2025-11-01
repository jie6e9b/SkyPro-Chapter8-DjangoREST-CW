from django.urls import path
from .views import LinkChatIdView, UnlinkChatIdView

urlpatterns = [
    path("link/", LinkChatIdView.as_view(), name="link_chat_id"),
    path("unlink/", UnlinkChatIdView.as_view(), name="unlink_chat_id"),
]
