import hashlib
import hmac
import json
from functools import wraps
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from billing.models import Export, Invitation, Membership
from billing.services import downloads, exports, invitations, invoices, payments
from billing.services.access import membership


def api(fn):
    @wraps(fn)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=401)
        try:
            return fn(request, *args, **kwargs)
        except PermissionDenied:
            return JsonResponse({"error": "Forbidden"}, status=403)
        except (ValueError, KeyError, TypeError, signing.BadSignature):
            return JsonResponse({"error": "Invalid input"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
    return wrapped


def body(request):
    value = json.loads(request.body)
    if not isinstance(value, dict):
        raise ValueError("Expected object")
    return value


def health(request):
    return JsonResponse({"status": "ok"})


@require_http_methods(["GET", "POST", "DELETE"])
def session(request):
    if request.method == "POST":
        try:
            data = body(request)
            user = authenticate(request, username=data["username"], password=data["password"])
        except (ValueError, KeyError, TypeError):
            return JsonResponse({"error": "Invalid input"}, status=400)
        if user is None:
            return JsonResponse({"error": "Bad credentials"}, status=401)
        login(request, user)
    elif request.method == "DELETE":
        logout(request)
    return JsonResponse({"csrf": get_token(request), "user": request.user.get_username()})


@api
@require_http_methods(["GET"])
def invoice(request, tenant_id, number):
    membership(request.user, tenant_id)
    return JsonResponse(invoices.detail(tenant_id, number))


@api
@require_POST
def export_create(request, tenant_id):
    membership(request.user, tenant_id)
    numbers = body(request)["numbers"]
    if not isinstance(numbers, list) or not 1 <= len(numbers) <= 100 or any(
            not isinstance(n, str) or not 1 <= len(n) <= 40 for n in numbers):
        raise ValueError("Invalid invoice selection")
    job = exports.submit(request.user, tenant_id, numbers)
    return JsonResponse({"id": str(job.id)}, status=202)


@api
@require_http_methods(["GET"])
def export_read(request, job_id):
    # A job owner can inspect status after revocation. Artifact generation must
    # therefore enforce current authorization in the asynchronous worker.
    job = get_object_or_404(Export, id=job_id, requested_by=request.user)
    return JsonResponse({"status": job.status, "content": job.content})


@api
@require_POST
def member_revoke(request, tenant_id, username):
    membership(request.user, tenant_id, admin=True)
    with transaction.atomic():
        item = get_object_or_404(Membership.objects.select_for_update(), tenant_id=tenant_id, user__username=username)
        item.active = False
        item.save(update_fields=["active"])
    return JsonResponse({"revoked": True})


@api
@require_POST
def invite_create(request, tenant_id):
    membership(request.user, tenant_id, admin=True)
    email = body(request)["email"]
    if not isinstance(email, str) or not email.endswith("@example.test") or len(email) > 120:
        raise ValueError("Invalid laboratory email")
    invite, token = invitations.issue(tenant_id, email)
    return JsonResponse({"id": str(invite.id), "token": token}, status=201)


@api
@require_POST
def invite_revoke(request, tenant_id, invite_id):
    membership(request.user, tenant_id, admin=True)
    with transaction.atomic():
        invite = get_object_or_404(Invitation.objects.select_for_update(), id=invite_id, tenant_id=tenant_id)
        invite.revoked = True
        invite.save(update_fields=["revoked"])
    return JsonResponse({"revoked": True})


@api
@require_POST
def invite_accept(request):
    invitations.accept(request.user, body(request)["token"])
    return JsonResponse({"accepted": True})


@api
@require_POST
def download_create(request, tenant_id, number):
    membership(request.user, tenant_id)
    return JsonResponse({"token": downloads.issue(request.user, tenant_id, number)})


@api
@require_http_methods(["GET"])
def download_read(request):
    return HttpResponse(downloads.read(request.user, request.GET["token"]), content_type="text/csv")


@csrf_exempt
@require_POST
def webhook(request):
    signature = hmac.new(settings.WEBHOOK_KEY.encode(), request.body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, request.headers.get("X-Signature", "")):
        return JsonResponse({"error": "Invalid signature"}, status=403)
    try:
        event = body(request)
        if (not isinstance(event.get("event_id"), str) or not 1 <= len(event["event_id"]) <= 100
                or type(event.get("invoice")) is not int or type(event.get("amount")) is not int
                or not 0 < event["amount"] <= 1000000):
            raise ValueError("Invalid payment")
        payments.apply(event)
    except (ValueError, KeyError, TypeError, ObjectDoesNotExist):
        return JsonResponse({"error": "Invalid event"}, status=400)
    return JsonResponse({"accepted": True})
