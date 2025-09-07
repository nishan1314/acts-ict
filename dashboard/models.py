from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class District(models.Model):
    """Bangladesh Districts for geographic mapping"""
    name = models.CharField(max_length=100, unique=True)
    division = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    # For future PostGIS integration
    # geometry = models.PolygonField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.division})"


class TenderCategory(models.Model):
    """Categories of government tenders"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Tender Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Organization(models.Model):
    """Government organizations and suppliers"""
    ORGANIZATION_TYPES = [
        ('buyer', 'Government Buyer'),
        ('supplier', 'Supplier/Contractor'),
        ('both', 'Both Buyer and Supplier'),
    ]
    
    name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=10, choices=ORGANIZATION_TYPES)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['organization_type']),
            models.Index(fields=['district']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_organization_type_display()})"


class Tender(models.Model):
    """Government procurement tenders"""
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('awarded', 'Awarded'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    tender_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.ForeignKey(TenderCategory, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name='bought_tenders'
    )
    
    # Financial Information
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2)
    award_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='BDT')
    
    # Timeline
    publication_date = models.DateTimeField()
    submission_deadline = models.DateTimeField()
    opening_date = models.DateTimeField()
    award_date = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    
    # Winner (if awarded)
    winner = models.ForeignKey(
        Organization, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='won_tenders'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publication_date']
        indexes = [
            models.Index(fields=['tender_id']),
            models.Index(fields=['status']),
            models.Index(fields=['publication_date']),
            models.Index(fields=['buyer']),
            models.Index(fields=['winner']),
        ]
    
    def __str__(self):
        return f"{self.tender_id}: {self.title[:50]}"
    
    @property
    def tender_window_days(self):
        """Calculate tender window in days"""
        if self.submission_deadline and self.publication_date:
            delta = self.submission_deadline - self.publication_date
            return delta.days
        return None
    
    @property
    def is_short_window(self):
        """Check if tender window is less than 7 days"""
        window = self.tender_window_days
        return window is not None and window < 7


class TenderBid(models.Model):
    """Bids submitted for tenders"""
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=15, decimal_places=2)
    submission_date = models.DateTimeField()
    is_winner = models.BooleanField(default=False)
    
    # Technical and financial scores (if available)
    technical_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    financial_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('tender', 'bidder')
        ordering = ['tender', 'bid_amount']
        indexes = [
            models.Index(fields=['tender']),
            models.Index(fields=['bidder']),
            models.Index(fields=['is_winner']),
        ]
    
    def __str__(self):
        status = " (WINNER)" if self.is_winner else ""
        return f"{self.tender.tender_id} - {self.bidder.name}: {self.bid_amount:,.2f}{status}"


class RiskScore(models.Model):
    """Risk scores computed for tenders"""
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]
    
    tender = models.OneToOneField(Tender, on_delete=models.CASCADE, related_name='risk_score')
    
    # Risk Flags
    single_bid_flag = models.BooleanField(default=False)
    short_window_flag = models.BooleanField(default=False)
    repeated_pair_flag = models.BooleanField(default=False)
    high_value_flag = models.BooleanField(default=False)
    
    # Risk Scores (0-100)
    single_bid_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    short_window_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    repeated_pair_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    network_risk_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Overall Risk
    total_risk_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='low')
    
    # Analysis metadata
    analysis_date = models.DateTimeField(auto_now=True)
    analysis_version = models.CharField(max_length=10, default='1.0')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_risk_score']
        indexes = [
            models.Index(fields=['risk_level']),
            models.Index(fields=['total_risk_score']),
            models.Index(fields=['analysis_date']),
        ]
    
    def __str__(self):
        return f"{self.tender.tender_id}: {self.total_risk_score}/100 ({self.get_risk_level_display()})"
    
    def save(self, *args, **kwargs):
        """Auto-calculate risk level based on total score"""
        if self.total_risk_score >= 80:
            self.risk_level = 'critical'
        elif self.total_risk_score >= 60:
            self.risk_level = 'high'
        elif self.total_risk_score >= 30:
            self.risk_level = 'medium'
        else:
            self.risk_level = 'low'
        super().save(*args, **kwargs)
