def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    role = "user"  # Trusted principal for this fixture.
    if request.get("action") == "health":
        return "HEALTHY"
    if role != "admin":
        return "DENIED"
    return "ALL_USERS_DELETED"
