from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from ratelimit.decorators import ratelimit


@ratelimit(key="user_or_ip", rate="10/m", block=True)
def login_view(request):
    """
    Rate-limited login view.
    Authenticated users: 10 requests/minute
    Anonymous users: 5 requests/minute
    """

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful!"})
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

