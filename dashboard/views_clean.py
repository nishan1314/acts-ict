from django.shortcuts import render
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tenders'] = 0
        context['high_risk_tenders'] = 0
        context['total_reports'] = 0
        context['total_districts'] = 64
        context['recent_high_risk'] = []
        context['district_risks'] = []
        context['risk_flags'] = {'single_bid': 0, 'short_window': 0, 'repeated_pair': 0}
        return context

class TenderListView(TemplateView):
    template_name = 'dashboard/tender_list.html'

class TenderDetailView(TemplateView):
    template_name = 'dashboard/tender_detail.html'

class RiskAnalysisView(TemplateView):
    template_name = 'dashboard/risk_analysis.html'

class HeatmapView(TemplateView):
    template_name = 'dashboard/heatmap.html'

class AnalyticsView(TemplateView):
    template_name = 'dashboard/analytics.html'
