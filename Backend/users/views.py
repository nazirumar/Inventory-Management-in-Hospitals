# users/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserCreateSerializer
from rest_framework.permissions import AllowAny


class UserSignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Call the parent class to validate credentials and retrieve the token
        response = super().post(request, *args, **kwargs)
        
        # Retrieve the token based on the key returned by the parent class
        token_key = response.data.get('token')
        if not token_key:
            return Response({'error': 'Token not generated. Check credentials.'}, status=400)
        
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=400)
        
        # Include additional details in the response
        return Response({
            'token': token.key,
            'user_id': token.user.id,  # Use `.id` instead of `user_id` for consistency
            'username': token.user.username
        })