from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

# Define sensitive paths
SENSITIVE_PATHS = ["/admin", "/login"]

@shared_task
def detect_suspicious_ips():
    """
    Flags IPs exceeding 100 requests in the last hour or
    accessing sensitive paths as suspicious.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Count requests per IP in the last hour
    ip_counts = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(request_count=models.Count("id"))
    )

    for entry in ip_counts:
        ip = entry["ip_address"]
        count = entry["request_count"]
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={"reason": f"Exceeded 100 requests/hour ({count})"}
            )

    # Check for access to sensitive paths
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__in=SENSITIVE_PATHS)
    for log in logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            defaults={"reason": f"Accessed sensitive path: {log.path}"}
        )

