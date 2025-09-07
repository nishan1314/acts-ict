from django.contrib import admin
from .models import District, TenderCategory, Organization, Tender, TenderBid, RiskScore


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', 'code')
    list_filter = ('division',)
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(TenderCategory)
class TenderCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_type', 'district', 'is_active')
    list_filter = ('organization_type', 'district', 'is_active')
    search_fields = ('name', 'registration_number')
    list_editable = ('is_active',)
    ordering = ('name',)


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ('tender_id', 'title', 'buyer', 'status', 'estimated_value', 'publication_date')
    list_filter = ('status', 'category', 'buyer__district')
    search_fields = ('tender_id', 'title', 'buyer__name')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    readonly_fields = ('tender_window_days', 'is_short_window')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tender_id', 'title', 'description', 'category', 'buyer')
        }),
        ('Financial', {
            'fields': ('estimated_value', 'award_amount', 'currency')
        }),
        ('Timeline', {
            'fields': ('publication_date', 'submission_deadline', 'opening_date', 'award_date')
        }),
        ('Status', {
            'fields': ('status', 'winner')
        }),
        ('Computed Fields', {
            'fields': ('tender_window_days', 'is_short_window'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TenderBid)
class TenderBidAdmin(admin.ModelAdmin):
    list_display = ('tender', 'bidder', 'bid_amount', 'is_winner', 'submission_date')
    list_filter = ('is_winner', 'tender__status')
    search_fields = ('tender__tender_id', 'bidder__name')
    ordering = ('-submission_date',)


@admin.register(RiskScore)
class RiskScoreAdmin(admin.ModelAdmin):
    list_display = ('tender', 'total_risk_score', 'risk_level', 'single_bid_flag', 'short_window_flag', 'repeated_pair_flag')
    list_filter = ('risk_level', 'single_bid_flag', 'short_window_flag', 'repeated_pair_flag')
    search_fields = ('tender__tender_id', 'tender__title')
    ordering = ('-total_risk_score',)
    readonly_fields = ('analysis_date',)
    
    fieldsets = (
        ('Tender', {
            'fields': ('tender',)
        }),
        ('Risk Flags', {
            'fields': ('single_bid_flag', 'short_window_flag', 'repeated_pair_flag', 'high_value_flag')
        }),
        ('Risk Scores', {
            'fields': ('single_bid_score', 'short_window_score', 'repeated_pair_score', 'network_risk_score')
        }),
        ('Overall Risk', {
            'fields': ('total_risk_score', 'risk_level')
        }),
        ('Analysis Metadata', {
            'fields': ('analysis_date', 'analysis_version'),
            'classes': ('collapse',)
        }),
    )
