from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TelegramProfile
from .serializers import TelegramProfileSerializer


class LinkChatIdView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TelegramProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat_id = serializer.validated_data["chat_id"]
        profile, _ = TelegramProfile.objects.update_or_create(
            user=request.user, defaults={"chat_id": chat_id}
        )
        return Response({"chat_id": profile.chat_id}, status=status.HTTP_200_OK)


class UnlinkChatIdView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        TelegramProfile.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
