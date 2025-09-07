from django.shortcuts import render
from django.views.generic import TemplateView

# Placeholder views for data analysis
class AnalysisView(TemplateView):
    template_name = 'data_analysis/analysis.html'
