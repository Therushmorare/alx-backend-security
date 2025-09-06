from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.cache import cache
from ipgeolocation import IpGeoLocation

from .models import RequestLog, BlockedIP


class RequestLoggingMiddleware:
    """
    Middleware that logs requests, blocks blacklisted IPs,
    and adds geolocation data (country, city).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.geo = IpGeoLocation()  # Initialize geolocation lookup

    def __call__(self, request):
        # Extract IP
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            ip = ip.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")

        # Block if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Check cache first
        geo_data = cache.get(f"geo:{ip}")
        if not geo_data:
            try:
                geo_info = self.geo.lookup(ip)
                geo_data = {
                    "country": geo_info.get("country_name", ""),
                    "city": geo_info.get("city", ""),
                }
            except Exception:
                geo_data = {"country": "", "city": ""}
            # Cache for 24h
            cache.set(f"geo:{ip}", geo_data, 60 * 60 * 24)

        # Log request with geolocation
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=timezone.now(),
            path=request.path,
            country=geo_data.get("country", ""),
            city=geo_data.get("city", ""),
        )

        return self.get_response(request)

