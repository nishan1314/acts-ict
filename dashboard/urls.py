from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', views.dashboard_view, name='home'),
    
    # Tender views
    path('tenders/', views.tender_list_view, name='tender_list'),
    path('tenders/<str:tender_id>/', views.tender_detail_view, name='tender_detail'),
    
    # Risk analysis views
    path('risk-analysis/', views.risk_analysis_view, name='risk_analysis'),
    
    # Heatmap view
    path('heatmap/', views.heatmap_view, name='heatmap'),
    
    # API endpoints
    path('api/tenders/', views.api_tender_data, name='api_tender_data'),
    path('api/risk-stats/', views.api_risk_stats, name='api_risk_stats'),
]
