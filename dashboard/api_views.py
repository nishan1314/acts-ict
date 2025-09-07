from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg, Q
from .models import District, TenderCategory, Organization, Tender, RiskScore
from .serializers import (
    DistrictSerializer, TenderCategorySerializer, OrganizationSerializer,
    TenderListSerializer, TenderDetailSerializer, RiskScoreSerializer,
    DistrictRiskSerializer, AnalyticsSummarySerializer
)
from data_analysis.risk_analyzer import RiskAnalyzer, NetworkAnalyzer


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for districts"""
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class TenderCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for tender categories"""
    queryset = TenderCategory.objects.all()
    serializer_class = TenderCategorySerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for organizations"""
    queryset = Organization.objects.select_related('district')
    serializer_class = OrganizationSerializer
    filterset_fields = ['organization_type', 'district', 'is_active']


class TenderViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for tenders"""
    queryset = Tender.objects.select_related(
        'buyer', 'winner', 'category', 'risk_score'
    ).prefetch_related('bids')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TenderDetailSerializer
        return TenderListSerializer
    
    filterset_fields = ['status', 'category', 'buyer__district']
    search_fields = ['title', 'tender_id', 'buyer__name']
    ordering_fields = ['publication_date', 'estimated_value', 'risk_score__total_risk_score']
    ordering = ['-risk_score__total_risk_score', '-publication_date']


class RiskScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for risk scores"""
    queryset = RiskScore.objects.select_related('tender')
    serializer_class = RiskScoreSerializer
    filterset_fields = ['risk_level', 'single_bid_flag', 'short_window_flag', 'repeated_pair_flag']
    ordering = ['-total_risk_score']


class AnalyticsSummaryView(APIView):
    """API endpoint for analytics summary"""
    
    def get(self, request):
        data = {
            'total_tenders': Tender.objects.count(),
            'total_organizations': Organization.objects.count(),
            'total_districts': District.objects.count(),
            'high_risk_tenders': RiskScore.objects.filter(
                risk_level__in=['high', 'critical']
            ).count(),
            'risk_distribution': dict(
                RiskScore.objects.values('risk_level').annotate(
                    count=Count('id')
                ).values_list('risk_level', 'count')
            ),
            'top_risk_flags': {
                'single_bid': RiskScore.objects.filter(single_bid_flag=True).count(),
                'short_window': RiskScore.objects.filter(short_window_flag=True).count(),
                'repeated_pair': RiskScore.objects.filter(repeated_pair_flag=True).count(),
            },
            'monthly_trends': []  # Placeholder for monthly trend data
        }
        
        serializer = AnalyticsSummarySerializer(data)
        return Response(serializer.data)


class DistrictRiskView(APIView):
    """API endpoint for district risk aggregation"""
    
    def get(self, request):
        district_risks = District.objects.annotate(
            total_tenders=Count('organization__bought_tenders'),
            high_risk_tenders=Count(
                'organization__bought_tenders__risk_score',
                filter=Q(organization__bought_tenders__risk_score__risk_level__in=['high', 'critical'])
            ),
            avg_risk_score=Avg('organization__bought_tenders__risk_score__total_risk_score')
        ).filter(total_tenders__gt=0)
        
        data = []
        for district in district_risks:
            risk_ratio = district.high_risk_tenders / district.total_tenders if district.total_tenders > 0 else 0
            data.append({
                'district_id': district.id,
                'district_name': district.name,
                'division': district.division,
                'total_tenders': district.total_tenders,
                'high_risk_tenders': district.high_risk_tenders,
                'avg_risk_score': district.avg_risk_score or 0,
                'risk_ratio': risk_ratio,
            })
        
        serializer = DistrictRiskSerializer(data, many=True)
        return Response(serializer.data)


class RunRiskAnalysisView(APIView):
    """API endpoint to run risk analysis"""
    
    def post(self, request):
        try:
            analyzer = RiskAnalyzer()
            results = analyzer.analyze_all_tenders()
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NetworkStatsView(APIView):
    """API endpoint for network statistics"""
    
    def get(self, request):
        try:
            network_analyzer = NetworkAnalyzer()
            stats = network_analyzer.get_network_stats()
            patterns = network_analyzer.find_suspicious_patterns()
            
            return Response({
                'network_stats': stats,
                'suspicious_patterns': patterns,
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExportTendersView(APIView):
    """API endpoint to export tender data"""
    
    def get(self, request):
        # Placeholder for CSV/Excel export functionality
        return Response({'message': 'Export functionality to be implemented'})


class ExportRisksView(APIView):
    """API endpoint to export risk data"""
    
    def get(self, request):
        # Placeholder for CSV/Excel export functionality
        return Response({'message': 'Export functionality to be implemented'})
