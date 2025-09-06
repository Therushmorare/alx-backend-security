from .models import RequestLog
from django.utils import timezone


class RequestLoggingMiddleware:
    """
    Middleware to log IP address, timestamp, and request path for every request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract IP (handles proxies via X-Forwarded-For)
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            ip = ip.split(",")[0]  # Take first IP in list
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")

        # Save request log in DB
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=timezone.now(),
            path=request.path,
        )

        # Continue with request
        response = self.get_response(request)
        return response

