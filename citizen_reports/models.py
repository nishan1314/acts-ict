import hashlib
import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from dashboard.models import District, Tender, Organization


def upload_to_reports(instance, filename):
    """Generate upload path for report files"""
    ext = filename.split('.')[-1]
    timestamp = timezone.now().strftime('%Y/%m/%d')
    return f'reports/{timestamp}/{instance.id}_{filename}'


class CitizenReport(models.Model):
    """Citizen reports of corruption or irregularities"""
    REPORT_TYPES = [
        ('general', 'General Corruption Report'),
        ('tender', 'Tender-related Issue'),
        ('bribery', 'Bribery/Extortion'),
        ('misuse', 'Misuse of Public Resources'),
        ('nepotism', 'Nepotism/Favoritism'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('verified', 'Verified'),
        ('false_report', 'False Report'),
        ('resolved', 'Resolved'),
    ]
    
    # Basic Information
    report_id = models.CharField(max_length=20, unique=True, editable=False)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Location
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    specific_location = models.CharField(max_length=200, blank=True)
    
    # Related Entities (optional)
    related_tender = models.ForeignKey(
        Tender, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='citizen_reports'
    )
    related_organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citizen_reports'
    )
    
    # Reporter Information (optional/anonymous)
    reporter_name = models.CharField(max_length=100, blank=True)
    reporter_email = models.EmailField(blank=True)
    reporter_phone = models.CharField(max_length=20, blank=True)
    is_anonymous = models.BooleanField(default=True)
    
    # Status and Processing
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='submitted')
    admin_notes = models.TextField(blank=True)
    
    # Integrity and Transparency
    content_hash = models.CharField(max_length=64, editable=False)  # SHA-256
    submission_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['report_id']),
            models.Index(fields=['status']),
            models.Index(fields=['report_type']),
            models.Index(fields=['district']),
            models.Index(fields=['submitted_at']),
        ]
    
    def __str__(self):
        return f"{self.report_id}: {self.title[:50]}"
    
    def save(self, *args, **kwargs):
        # Generate report ID if not exists
        if not self.report_id:
            self.report_id = self.generate_report_id()
        
        # Generate content hash
        self.content_hash = self.generate_content_hash()
        
        super().save(*args, **kwargs)
    
    def generate_report_id(self):
        """Generate unique report ID"""
        timestamp = timezone.now().strftime('%Y%m%d')
        existing_count = CitizenReport.objects.filter(
            submitted_at__date=timezone.now().date()
        ).count()
        return f"CR{timestamp}{existing_count + 1:04d}"
    
    def generate_content_hash(self):
        """Generate SHA-256 hash of report content"""
        content = f"{self.title}|{self.description}|{self.district_id}|{self.report_type}"
        if self.related_tender_id:
            content += f"|{self.related_tender_id}"
        if self.related_organization_id:
            content += f"|{self.related_organization_id}"
        
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    @property
    def receipt_hash(self):
        """Public receipt hash for verification"""
        return self.content_hash


class ReportEvidence(models.Model):
    """Evidence files attached to citizen reports"""
    EVIDENCE_TYPES = [
        ('image', 'Image'),
        ('audio', 'Audio Recording'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]
    
    report = models.ForeignKey(
        CitizenReport, 
        on_delete=models.CASCADE, 
        related_name='evidence_files'
    )
    evidence_type = models.CharField(max_length=10, choices=EVIDENCE_TYPES)
    file = models.FileField(
        upload_to=upload_to_reports,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 
                                  'mp3', 'wav', 'mp4', 'avi', 'txt']
            )
        ]
    )
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # in bytes
    description = models.CharField(max_length=200, blank=True)
    
    # Integrity
    file_hash = models.CharField(max_length=64, editable=False)  # SHA-256 of file
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"{self.report.report_id} - {self.filename}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.filename = self.file.name
            self.file_size = self.file.size
            
            # Auto-detect evidence type based on file extension
            if not self.evidence_type or self.evidence_type == 'other':
                ext = self.filename.lower().split('.')[-1]
                if ext in ['jpg', 'jpeg', 'png', 'gif']:
                    self.evidence_type = 'image'
                elif ext in ['mp3', 'wav']:
                    self.evidence_type = 'audio'
                elif ext in ['mp4', 'avi']:
                    self.evidence_type = 'video'
                elif ext in ['pdf', 'doc', 'docx', 'txt']:
                    self.evidence_type = 'document'
            
            # Generate file hash
            self.file_hash = self.generate_file_hash()
        
        super().save(*args, **kwargs)
    
    def generate_file_hash(self):
        """Generate SHA-256 hash of the file content"""
        hash_sha256 = hashlib.sha256()
        
        # Reset file pointer to beginning
        self.file.seek(0)
        
        # Read file in chunks to handle large files
        for chunk in iter(lambda: self.file.read(4096), b""):
            hash_sha256.update(chunk)
        
        # Reset file pointer
        self.file.seek(0)
        
        return hash_sha256.hexdigest()


class IntegrityReceipt(models.Model):
    """Cryptographic receipts for report verification"""
    report = models.OneToOneField(
        CitizenReport, 
        on_delete=models.CASCADE, 
        related_name='integrity_receipt'
    )
    
    # Receipt Information
    receipt_id = models.CharField(max_length=20, unique=True, editable=False)
    content_hash = models.CharField(max_length=64)  # Same as report content_hash
    evidence_hashes = models.JSONField(default=list)  # List of evidence file hashes
    
    # Blockchain-style chaining (for demo purposes)
    previous_receipt_hash = models.CharField(max_length=64, blank=True)
    merkle_root = models.CharField(max_length=64, editable=False)
    
    # Timestamps
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"Receipt {self.receipt_id} for {self.report.report_id}"
    
    def save(self, *args, **kwargs):
        if not self.receipt_id:
            self.receipt_id = self.generate_receipt_id()
        
        # Set content hash from report
        self.content_hash = self.report.content_hash
        
        # Collect evidence hashes
        self.evidence_hashes = list(
            self.report.evidence_files.values_list('file_hash', flat=True)
        )
        
        # Generate merkle root
        self.merkle_root = self.generate_merkle_root()
        
        # Set previous receipt hash (blockchain-style chaining)
        if not self.previous_receipt_hash:
            last_receipt = IntegrityReceipt.objects.exclude(pk=self.pk).order_by('-generated_at').first()
            if last_receipt:
                self.previous_receipt_hash = last_receipt.merkle_root
        
        super().save(*args, **kwargs)
    
    def generate_receipt_id(self):
        """Generate unique receipt ID"""
        timestamp = timezone.now().strftime('%Y%m%d')
        existing_count = IntegrityReceipt.objects.filter(
            generated_at__date=timezone.now().date()
        ).count()
        return f"RC{timestamp}{existing_count + 1:04d}"
    
    def generate_merkle_root(self):
        """Generate Merkle root hash from content and evidence hashes"""
        all_hashes = [self.content_hash] + self.evidence_hashes
        if self.previous_receipt_hash:
            all_hashes.append(self.previous_receipt_hash)
        
        # Simple merkle root calculation (for demo)
        combined = ''.join(sorted(all_hashes))
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    def verify_integrity(self):
        """Verify the integrity of the receipt"""
        # Check if content hash matches report
        if self.content_hash != self.report.content_hash:
            return False, "Content hash mismatch"
        
        # Check if evidence hashes match
        current_evidence_hashes = list(
            self.report.evidence_files.values_list('file_hash', flat=True)
        )
        if set(self.evidence_hashes) != set(current_evidence_hashes):
            return False, "Evidence hash mismatch"
        
        # Verify merkle root
        expected_merkle = self.generate_merkle_root()
        if self.merkle_root != expected_merkle:
            return False, "Merkle root mismatch"
        
        return True, "Integrity verified"
