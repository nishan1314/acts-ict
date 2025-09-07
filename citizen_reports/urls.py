from django.urls import path
from . import views

app_name = 'citizen_reports'

urlpatterns = [
    # Report submission
    path('', views.ReportListView.as_view(), name='report_list'),
    path('submit/', views.ReportSubmissionView.as_view(), name='submit_report'),
    path('<str:report_id>/', views.ReportDetailView.as_view(), name='report_detail'),
    
    # Transparency log
    path('log/', views.TransparencyLogView.as_view(), name='transparency_log'),
    
    # Receipt verification
    path('verify/', views.ReceiptVerificationView.as_view(), name='verify_receipt'),
    path('verify/<str:receipt_hash>/', views.VerifyReceiptDetailView.as_view(), name='verify_receipt_detail'),
]
