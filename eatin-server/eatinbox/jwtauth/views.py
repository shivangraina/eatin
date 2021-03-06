import datetime
from django.utils import timezone
from .permissions import IsValidUser, IsOwnerOrReadOnly


from rest_framework import permissions, status

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings

from rest_framework_jwt.views import refresh_jwt_token

from rest_framework.exceptions import ValidationError

# Here ListCreate is used just for development purpose to view users.
# Each time u GET the register url new tokens will be generated
# Same is the case with retrieve
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .utils import jwt_response_payload_handler
from .serializers import RegisterSerializer, RegisterDetailSerializer

User = get_user_model()
exp_delta = api_settings.JWT_EXPIRATION_DELTA   # This delta is for maximum time before which u can refresh the token through previous token.


jwt_create_payload = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Login view, which checks that token is valid or not(i.e expired or not)

class AuthView(APIView):

    permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def post(self, request, *args, **kwargs):
        print(request.user)
        # if request.user.is_authenticated:
        #     print('f')
        #     return Response({'token': 'nibba'})
        data = request.data
        email = data.get('email')
        password = data.get('password')
        is_user = data.get('is_user')
        user = authenticate(email=email, password=password)
        if user is not None:

            try:
                flag = getattr(user, is_user)
            except AttributeError:
                return Response("is_user field not valid")

            if flag is True:
                print(user)
                payload = jwt_create_payload(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        else:
            return Response("Invalid Credentials")


# Register View for any user. Here token will be generated for first time.

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def post(self, request, *args, **kwargs):
        # Overrided this method for understanding purposes only.
        print(request.data)
        instance = RegisterSerializer(data=request.data, context=self.get_serializer_context())
        try:
            instance.is_valid()
        except ValidationError:
            return Response(data=instance.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance.save()
        except:
            return Response(data=instance.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=instance.data, status=status.HTTP_201_CREATED)

# The following view will give us the detailed view.
# Here token will be generated again.


class RetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterDetailSerializer
    permission_classes = [IsValidUser]
    # permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'
    # def get_serializer_context(self):
    #     return {'request': self.request}


def refresh_token(request):
    token = refresh_jwt_token(request)
    print(token)
    exp = timezone.now() + exp_delta - datetime.timedelta(seconds=300)
    response = {
        'token': token,
        'exp': exp,
    }
    return Response(response, status=200)
