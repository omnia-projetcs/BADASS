"""Small reporting service using the real Django ORM and JSONField transforms."""
import json
import os
from django.conf import settings

settings.configure(SECRET_KEY=os.environ["LAB_SESSION_KEY"], DEBUG=False, ALLOWED_HOSTS=["web", "localhost"],
                   ROOT_URLCONF=__name__, DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "/tmp/report.sqlite"}},
                   INSTALLED_APPS=[])
import django
django.setup()
from django.db import connection, models
from django.http import JsonResponse
from django.urls import path
from django.core.wsgi import get_wsgi_application


class Record(models.Model):
    data = models.JSONField()

    class Meta:
        app_label = "reports"


class Secret(models.Model):
    value = models.TextField()

    class Meta:
        app_label = "reports"


def report(request):
    field = request.GET.get("field", "customer")
    if len(field) > 300:
        return JsonResponse({"error": "Field too long"}, status=400)
    try:
        rows = list(Record.objects.values_list("data__" + field, flat=True))
    except ValueError:
        return JsonResponse({"error": "Invalid field alias"}, status=400)
    return JsonResponse({"values": rows})


urlpatterns = [path("health/", lambda request: JsonResponse({"status": "ok"})), path("report/", report)]
application = get_wsgi_application()

if __name__ == "__main__":
    with connection.schema_editor() as editor:
        editor.create_model(Record)
        editor.create_model(Secret)
    Record.objects.create(data={"customer": "PUBLIC_CUSTOMER", "amount": 100})
    Secret.objects.create(value="LAB_PRIVATE_ACCOUNTING_KEY")
