from django.shortcuts import render
from django.views.generic import TemplateView

# Placeholder views for citizen reports
class ReportListView(TemplateView):
    template_name = 'citizen_reports/report_list.html'

class ReportSubmissionView(TemplateView):
    template_name = 'citizen_reports/submit_report.html'

class ReportDetailView(TemplateView):
    template_name = 'citizen_reports/report_detail.html'

class TransparencyLogView(TemplateView):
    template_name = 'citizen_reports/transparency_log.html'

class ReceiptVerificationView(TemplateView):
    template_name = 'citizen_reports/verify_receipt.html'

class VerifyReceiptDetailView(TemplateView):
    template_name = 'citizen_reports/verify_receipt_detail.html'
