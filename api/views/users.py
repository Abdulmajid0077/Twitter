from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.users import User

from api.utils import send_code_to_email
from api.serializers import EmailSerializer


class SendEmailRegistrationView(APIView):
    serializer_class = EmailSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        user = User.objects.create(email=email)
        send_code_to_email(email, user.create_verify_code())

        data = {
            "status": True,
            "message": "Verification code sent to your email.",
            "tokens": user.token()
        }

        return Response(data)