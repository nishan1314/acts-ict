from rest_framework import serializers
from .models import District, TenderCategory, Organization, Tender, TenderBid, RiskScore


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'division', 'code', 'created_at']


class TenderCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderCategory
        fields = ['id', 'name', 'description']


class OrganizationSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'organization_type', 'district', 'district_name',
            'registration_number', 'contact_email', 'is_active', 'created_at'
        ]


class RiskScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskScore
        fields = [
            'single_bid_flag', 'short_window_flag', 'repeated_pair_flag', 'high_value_flag',
            'single_bid_score', 'short_window_score', 'repeated_pair_score', 'network_risk_score',
            'total_risk_score', 'risk_level', 'analysis_date'
        ]


class TenderBidSerializer(serializers.ModelSerializer):
    bidder_name = serializers.CharField(source='bidder.name', read_only=True)
    
    class Meta:
        model = TenderBid
        fields = [
            'id', 'bidder', 'bidder_name', 'bid_amount', 'submission_date',
            'is_winner', 'technical_score', 'financial_score'
        ]


class TenderListSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.name', read_only=True)
    winner_name = serializers.CharField(source='winner.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    district_name = serializers.CharField(source='buyer.district.name', read_only=True)
    risk_score = RiskScoreSerializer(read_only=True)
    tender_window_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Tender
        fields = [
            'id', 'tender_id', 'title', 'buyer', 'buyer_name', 'winner', 'winner_name',
            'category', 'category_name', 'district_name', 'estimated_value', 'award_amount',
            'publication_date', 'submission_deadline', 'award_date', 'status',
            'tender_window_days', 'risk_score', 'created_at'
        ]


class TenderDetailSerializer(serializers.ModelSerializer):
    buyer = OrganizationSerializer(read_only=True)
    winner = OrganizationSerializer(read_only=True)
    category = TenderCategorySerializer(read_only=True)
    risk_score = RiskScoreSerializer(read_only=True)
    bids = TenderBidSerializer(many=True, read_only=True)
    tender_window_days = serializers.ReadOnlyField()
    is_short_window = serializers.ReadOnlyField()
    
    class Meta:
        model = Tender
        fields = [
            'id', 'tender_id', 'title', 'description', 'buyer', 'winner', 'category',
            'estimated_value', 'award_amount', 'currency', 'publication_date',
            'submission_deadline', 'opening_date', 'award_date', 'status',
            'tender_window_days', 'is_short_window', 'risk_score', 'bids',
            'created_at', 'updated_at'
        ]


class DistrictRiskSerializer(serializers.Serializer):
    """Serializer for district risk aggregation"""
    district_id = serializers.IntegerField()
    district_name = serializers.CharField()
    division = serializers.CharField()
    total_tenders = serializers.IntegerField()
    high_risk_tenders = serializers.IntegerField()
    avg_risk_score = serializers.FloatField()
    risk_ratio = serializers.FloatField()


class AnalyticsSummarySerializer(serializers.Serializer):
    """Serializer for analytics summary"""
    total_tenders = serializers.IntegerField()
    total_organizations = serializers.IntegerField()
    total_districts = serializers.IntegerField()
    high_risk_tenders = serializers.IntegerField()
    risk_distribution = serializers.DictField()
    top_risk_flags = serializers.DictField()
    monthly_trends = serializers.ListField()
