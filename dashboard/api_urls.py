from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'tenders', api_views.TenderViewSet)
router.register(r'organizations', api_views.OrganizationViewSet)
router.register(r'districts', api_views.DistrictViewSet)
router.register(r'categories', api_views.TenderCategoryViewSet)
router.register(r'risk-scores', api_views.RiskScoreViewSet)

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Custom analytics endpoints
    path('analytics/summary/', api_views.AnalyticsSummaryView.as_view(), name='analytics-summary'),
    path('analytics/district-risks/', api_views.DistrictRiskView.as_view(), name='district-risks'),
    path('analytics/run-analysis/', api_views.RunRiskAnalysisView.as_view(), name='run-analysis'),
    path('analytics/network-stats/', api_views.NetworkStatsView.as_view(), name='network-stats'),
    
    # Export endpoints
    path('export/tenders/', api_views.ExportTendersView.as_view(), name='export-tenders'),
    path('export/risks/', api_views.ExportRisksView.as_view(), name='export-risks'),
]
