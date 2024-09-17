from rest_framework import status
from rest_framework.decorators import ( api_view, permission_classes)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated , AllowAny

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from main.serializers import TokenSerializer

@api_view(["POST"])
def login_api(request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            _token = TokenSerializer(token)           
            return Response(
                {
                    "success": True,
                    "message": "User logged in successfully.",
                    "csrf_token": _token.data["key"],
                }
            )
        else:
            return Response(
                {"success": False, "message": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = Token.objects.get(user=request.user)
        logout(request)
        token.delete()
        return Response({"message": "logout"})
    except Exception as e:
        print(e.args[0])
        return Response({"message": "logout - error {e}"})


@api_view(["POST"])
def signup_api(request):
    
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    # Check if username or email already exists
    if User.objects.filter(username=username).exists():
        return Response({"success": False, "message": "Username already exists."})
    if User.objects.filter(email=email).exists():
        return Response({"success": False, "message": "Email already exists."})

    # Create user
    user = User.objects.create_user(
        username=username, email=email, password=password
    )

    if user:
        return Response({"success": True, "message": "Sign up successful."})
    else:
        return Response({"success": False, "message": "Failed to create user."})

@api_view(["GET"])
@permission_classes([AllowAny])
def delete_session(request):
    try:
        request.session.delete()
        return Response({"message": "Session deleted"})
    except Exception as e:
        print(e.args[0])
        return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

