import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .routing import SERVICES


class GatewayView(APIView):

    def post(self, request, service, path):

        service_url = SERVICES.get(service)

        if not service_url:
            return Response({"error": "Service not found"}, status=404)

        url = f"{service_url}/{path}"

        try:
            response = requests.post(
                url,
                json=request.data,
                headers=request.headers,
                timeout=5
            )

            return Response(
                response.json(),
                status=response.status_code
            )

        except requests.exceptions.RequestException:

            return Response(
                {"error": "Service unavailable"},
                status=503
            )