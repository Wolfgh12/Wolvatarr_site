from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('active-intercept/', views.active_intercept, name='active_intercept'),
    path('api/telemetry/', views.telemetry_api, name='telemetry_api'),
    path('api/intercept-beacon/', views.active_intercept_beacon, name='intercept_beacon'),
    path('api/pilot/', views.arcade_pilot_api, name='arcade_pilot_api'),
    path('api/audit/', views.real_site_audit_api, name='real_site_audit_api'),
    path('api/domain-lookup/', views.domain_lookup_api, name='domain_lookup_api'),
    path('api/scam-audit/', views.scam_threat_audit_api, name='scam_threat_audit_api'),
    path('api/audit-pdf/', views.download_audit_pdf, name='download_audit_pdf'),
]