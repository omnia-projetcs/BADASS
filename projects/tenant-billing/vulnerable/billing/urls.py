from django.urls import path
from billing import views

urlpatterns = [
    path("health/", views.health),
    path("api/session/", views.session),
    path("api/tenants/<int:tenant_id>/invoices/<str:number>/", views.invoice),
    path("api/tenants/<int:tenant_id>/exports/", views.export_create),
    path("api/exports/<uuid:job_id>/", views.export_read),
    path("api/tenants/<int:tenant_id>/members/<str:username>/revoke/", views.member_revoke),
    path("api/tenants/<int:tenant_id>/invitations/", views.invite_create),
    path("api/tenants/<int:tenant_id>/invitations/<uuid:invite_id>/revoke/", views.invite_revoke),
    path("api/invitations/accept/", views.invite_accept),
    path("api/tenants/<int:tenant_id>/invoices/<str:number>/download/", views.download_create),
    path("api/download/", views.download_read),
    path("api/webhooks/payment/", views.webhook),
]
