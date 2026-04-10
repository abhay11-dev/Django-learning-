import jwt
from django.http import JsonResponse

SECRET = "supersecret"

class JWTAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        token = request.headers.get("Authorization")

        if not token:
            return JsonResponse({"error": "Token missing"}, status=401)

        try:
            jwt.decode(token, SECRET, algorithms=["HS256"])
        except:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return self.get_response(request)