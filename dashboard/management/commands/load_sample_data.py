"""
Management command to load sample data for ACTS demo
"""
import random
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import (
    District, TenderCategory, Organization, Tender, TenderBid, RiskScore
)
from data_analysis.risk_analyzer import RiskAnalyzer

fake = Faker()


class Command(BaseCommand):
    help = 'Load sample data for ACTS demo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tenders',
            type=int,
            default=100,
            help='Number of tenders to create (default: 100)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        self.stdout.write('Loading sample data...')
        
        # Load basic data
        self.load_districts()
        self.load_categories()
        self.load_organizations()
        
        # Load tenders and bids
        self.load_tenders(options['tenders'])
        
        # Run risk analysis
        self.stdout.write('Running risk analysis...')
        analyzer = RiskAnalyzer()
        results = analyzer.analyze_all_tenders()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded sample data:\n'
                f'- Districts: {District.objects.count()}\n'
                f'- Organizations: {Organization.objects.count()}\n'
                f'- Tenders: {Tender.objects.count()}\n'
                f'- Bids: {TenderBid.objects.count()}\n'
                f'- Risk Scores: {RiskScore.objects.count()}\n'
                f'- High Risk Tenders: {results["high_risk_found"]}'
            )
        )

    def clear_data(self):
        """Clear existing demo data"""
        RiskScore.objects.all().delete()
        TenderBid.objects.all().delete()
        Tender.objects.all().delete()
        Organization.objects.all().delete()
        TenderCategory.objects.all().delete()
        District.objects.all().delete()

    def load_districts(self):
        """Load Bangladesh districts"""
        districts_data = [
            # Dhaka Division
            ('Dhaka', 'Dhaka', 'DH-01'),
            ('Gazipur', 'Dhaka', 'DH-02'),
            ('Narayanganj', 'Dhaka', 'DH-03'),
            ('Tangail', 'Dhaka', 'DH-04'),
            ('Manikganj', 'Dhaka', 'DH-05'),
            ('Faridpur', 'Dhaka', 'DH-06'),
            ('Madaripur', 'Dhaka', 'DH-07'),
            ('Shariatpur', 'Dhaka', 'DH-08'),
            ('Gopalganj', 'Dhaka', 'DH-09'),
            ('Rajbari', 'Dhaka', 'DH-10'),
            ('Kishoreganj', 'Dhaka', 'DH-11'),
            ('Netrakona', 'Dhaka', 'DH-12'),
            ('Munshiganj', 'Dhaka', 'DH-13'),
            
            # Chittagong Division
            ('Chittagong', 'Chittagong', 'CH-01'),
            ('Coxs Bazar', 'Chittagong', 'CH-02'),
            ('Rangamati', 'Chittagong', 'CH-03'),
            ('Bandarban', 'Chittagong', 'CH-04'),
            ('Khagrachhari', 'Chittagong', 'CH-05'),
            ('Feni', 'Chittagong', 'CH-06'),
            ('Lakshmipur', 'Chittagong', 'CH-07'),
            ('Comilla', 'Chittagong', 'CH-08'),
            ('Noakhali', 'Chittagong', 'CH-09'),
            ('Brahmanbaria', 'Chittagong', 'CH-10'),
            ('Chandpur', 'Chittagong', 'CH-11'),
            
            # Rajshahi Division
            ('Rajshahi', 'Rajshahi', 'RA-01'),
            ('Pabna', 'Rajshahi', 'RA-02'),
            ('Sirajganj', 'Rajshahi', 'RA-03'),
            ('Bogra', 'Rajshahi', 'RA-04'),
            ('Joypurhat', 'Rajshahi', 'RA-05'),
            ('Naogaon', 'Rajshahi', 'RA-06'),
            ('Natore', 'Rajshahi', 'RA-07'),
            ('Chapainawabganj', 'Rajshahi', 'RA-08'),
            
            # Khulna Division
            ('Khulna', 'Khulna', 'KH-01'),
            ('Jessore', 'Khulna', 'KH-02'),
            ('Narail', 'Khulna', 'KH-03'),
            ('Magura', 'Khulna', 'KH-04'),
            ('Jhenaidah', 'Khulna', 'KH-05'),
            ('Kushtia', 'Khulna', 'KH-06'),
            ('Chuadanga', 'Khulna', 'KH-07'),
            ('Meherpur', 'Khulna', 'KH-08'),
            ('Satkhira', 'Khulna', 'KH-09'),
            ('Bagerhat', 'Khulna', 'KH-10'),
            
            # Barisal Division
            ('Barisal', 'Barisal', 'BA-01'),
            ('Patuakhali', 'Barisal', 'BA-02'),
            ('Barguna', 'Barisal', 'BA-03'),
            ('Bhola', 'Barisal', 'BA-04'),
            ('Jhalokati', 'Barisal', 'BA-05'),
            ('Pirojpur', 'Barisal', 'BA-06'),
            
            # Sylhet Division
            ('Sylhet', 'Sylhet', 'SY-01'),
            ('Moulvibazar', 'Sylhet', 'SY-02'),
            ('Habiganj', 'Sylhet', 'SY-03'),
            ('Sunamganj', 'Sylhet', 'SY-04'),
            
            # Rangpur Division
            ('Rangpur', 'Rangpur', 'RN-01'),
            ('Dinajpur', 'Rangpur', 'RN-02'),
            ('Thakurgaon', 'Rangpur', 'RN-03'),
            ('Panchagarh', 'Rangpur', 'RN-04'),
            ('Nilphamari', 'Rangpur', 'RN-05'),
            ('Lalmonirhat', 'Rangpur', 'RN-06'),
            ('Kurigram', 'Rangpur', 'RN-07'),
            ('Gaibandha', 'Rangpur', 'RN-08'),
            
            # Mymensingh Division
            ('Mymensingh', 'Mymensingh', 'MY-01'),
            ('Jamalpur', 'Mymensingh', 'MY-02'),
            ('Sherpur', 'Mymensingh', 'MY-03'),
            ('Netrakona', 'Mymensingh', 'MY-04'),
        ]
        
        for name, division, code in districts_data:
            District.objects.get_or_create(
                name=name,
                defaults={'division': division, 'code': code}
            )
        
        self.stdout.write(f'Loaded {len(districts_data)} districts')

    def load_categories(self):
        """Load tender categories"""
        categories = [
            ('Infrastructure', 'Roads, bridges, buildings, and utilities'),
            ('IT Services', 'Software development, hardware procurement, IT consulting'),
            ('Healthcare', 'Medical equipment, pharmaceuticals, hospital services'),
            ('Education', 'School construction, educational materials, training'),
            ('Transportation', 'Vehicles, logistics, public transport'),
            ('Energy', 'Power generation, renewable energy, grid infrastructure'),
            ('Water & Sanitation', 'Water supply systems, waste management'),
            ('Agriculture', 'Equipment, seeds, irrigation systems'),
            ('Security', 'Safety equipment, surveillance systems'),
            ('Consulting', 'Advisory services, feasibility studies'),
        ]
        
        for name, description in categories:
            TenderCategory.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
        
        self.stdout.write(f'Loaded {len(categories)} categories')

    def load_organizations(self):
        """Load government and supplier organizations"""
        districts = list(District.objects.all())
        categories = list(TenderCategory.objects.all())
        
        # Government buyers
        govt_types = [
            'Ministry', 'Department', 'Corporation', 'Council', 'Authority', 
            'Board', 'Commission', 'Agency', 'Office', 'Directorate'
        ]
        
        govt_names = [
            'Public Works', 'Health Services', 'Education', 'Transport', 'Water',
            'Power', 'Agriculture', 'Local Government', 'Urban Development',
            'Rural Development', 'Social Welfare', 'Youth & Sports',
            'Environment', 'ICT', 'Finance', 'Planning', 'Housing'
        ]
        
        # Create government buyers (2-3 per district)
        for district in districts:
            for i in range(random.randint(2, 3)):
                name = f"{random.choice(govt_names)} {random.choice(govt_types)}, {district.name}"
                
                Organization.objects.get_or_create(
                    name=name,
                    defaults={
                        'organization_type': 'buyer',
                        'district': district,
                        'registration_number': f"GOV-{district.code}-{i+1:03d}",
                        'contact_email': f"contact@{name.lower().replace(' ', '').replace(',', '')}.gov.bd",
                        'is_active': True,
                    }
                )
        
        # Create suppliers (5-10 per district)
        supplier_types = [
            'Construction Ltd.', 'Engineering Services', 'Trading Company', 
            'Technologies Ltd.', 'Solutions Ltd.', 'Enterprise', 'Corporation',
            'Industries', 'Contractors', 'Consultants'
        ]
        
        for district in districts:
            for i in range(random.randint(5, 10)):
                company_name = fake.company()
                name = f"{company_name} {random.choice(supplier_types)}"
                
                Organization.objects.get_or_create(
                    name=name,
                    defaults={
                        'organization_type': 'supplier',
                        'district': district,
                        'registration_number': f"SUP-{district.code}-{i+1:04d}",
                        'contact_email': fake.company_email(),
                        'contact_phone': fake.phone_number(),
                        'address': fake.address(),
                        'is_active': random.choice([True, True, True, False]),  # 25% chance inactive
                    }
                )
        
        self.stdout.write(f'Loaded {Organization.objects.count()} organizations')

    def load_tenders(self, num_tenders):
        """Load sample tenders with realistic corruption scenarios"""
        buyers = list(Organization.objects.filter(organization_type__in=['buyer', 'both']))
        suppliers = list(Organization.objects.filter(organization_type__in=['supplier', 'both'], is_active=True))
        categories = list(TenderCategory.objects.all())
        
        # Create some "preferred" supplier relationships for corruption scenarios
        preferred_pairs = []
        for buyer in random.sample(buyers, min(20, len(buyers))):
            # Each buyer has 1-3 preferred suppliers
            preferred_suppliers = random.sample(suppliers, random.randint(1, 3))
            for supplier in preferred_suppliers:
                preferred_pairs.append((buyer, supplier))
        
        for i in range(num_tenders):
            buyer = random.choice(buyers)
            category = random.choice(categories)
            
            # Generate tender dates
            publication_date = fake.date_time_between(start_date='-2y', end_date='now', tzinfo=timezone.get_current_timezone())
            
            # Corruption scenario: Some tenders have very short windows
            if random.random() < 0.15:  # 15% chance of short window
                days_to_deadline = random.randint(1, 6)  # 1-6 days (suspicious)
            else:
                days_to_deadline = random.randint(7, 45)  # Normal: 7-45 days
                
            submission_deadline = publication_date + timedelta(days=days_to_deadline)
            opening_date = submission_deadline + timedelta(days=random.randint(1, 3))
            
            # Award date (if tender is awarded)
            status = random.choices(
                ['published', 'closed', 'awarded', 'cancelled'],
                weights=[0.1, 0.2, 0.6, 0.1]
            )[0]
            
            award_date = None
            if status == 'awarded':
                award_date = opening_date + timedelta(days=random.randint(1, 14))
            
            # Estimated value (in BDT)
            estimated_value = Decimal(str(random.randint(100000, 50000000)))  # 100K to 50M BDT
            
            # Generate tender
            tender = Tender.objects.create(
                tender_id=f"TND-{publication_date.year}-{i+1:06d}",
                title=self.generate_tender_title(category),
                description=fake.text(max_nb_chars=500),
                category=category,
                buyer=buyer,
                estimated_value=estimated_value,
                publication_date=publication_date,
                submission_deadline=submission_deadline,
                opening_date=opening_date,
                award_date=award_date,
                status=status,
            )
            
            # Generate bids
            if status in ['closed', 'awarded']:
                self.generate_bids(tender, suppliers, preferred_pairs)
        
        self.stdout.write(f'Loaded {num_tenders} tenders')

    def generate_tender_title(self, category):
        """Generate realistic tender titles"""
        titles_by_category = {
            'Infrastructure': [
                'Construction of Rural Road Network',
                'Bridge Construction over Local River',
                'Government Office Building Construction',
                'School Building Renovation',
                'Hospital Infrastructure Development',
            ],
            'IT Services': [
                'Government Website Development',
                'Database Management System',
                'Computer Hardware Procurement',
                'Network Infrastructure Setup',
                'Software License Procurement',
            ],
            'Healthcare': [
                'Medical Equipment Supply',
                'Pharmaceutical Procurement',
                'Hospital Bed Procurement',
                'Ambulance Service Contract',
                'Medical Waste Management',
            ],
            'Education': [
                'School Furniture Supply',
                'Educational Book Printing',
                'Computer Lab Setup',
                'School Bus Service',
                'Teacher Training Program',
            ],
            'Transportation': [
                'Government Vehicle Procurement',
                'Public Bus Service Contract',
                'Traffic Management System',
                'Road Maintenance Service',
                'Fuel Supply Contract',
            ],
        }
        
        category_titles = titles_by_category.get(category.name, [
            f'{category.name} Service Contract',
            f'{category.name} Equipment Supply',
            f'{category.name} Development Project',
        ])
        
        base_title = random.choice(category_titles)
        location = random.choice(['District', 'Upazila', 'Municipality', 'Union'])
        
        return f"{base_title} - {location} Level"

    def generate_bids(self, tender, suppliers, preferred_pairs):
        """Generate bids for a tender with corruption scenarios"""
        buyer = tender.buyer
        
        # Check if this buyer has preferred suppliers
        preferred_suppliers = [supplier for b, supplier in preferred_pairs if b == buyer]
        
        # Corruption scenario probabilities
        single_bid_prob = 0.12  # 12% chance of single bid
        repeated_pair_prob = 0.25  # 25% chance of using preferred supplier
        
        # Determine number of bids
        if random.random() < single_bid_prob:
            num_bids = 1  # Single bid (red flag)
        elif random.random() < 0.3:
            num_bids = 2  # Two bids (still suspicious)
        else:
            num_bids = random.randint(3, 8)  # Normal competition
        
        # Select bidders
        bidders = []
        
        # If using preferred supplier scenario
        if preferred_suppliers and random.random() < repeated_pair_prob:
            # Preferred supplier gets to bid
            preferred = random.choice(preferred_suppliers)
            bidders.append(preferred)
            num_bids -= 1
        
        # Add random suppliers for remaining bids
        available_suppliers = [s for s in suppliers if s not in bidders and s.district_id in [tender.buyer.district_id, *random.choices(list(District.objects.values_list('id', flat=True)), k=3)]]
        additional_bidders = random.sample(
            available_suppliers, 
            min(num_bids, len(available_suppliers))
        )
        bidders.extend(additional_bidders)
        
        # Generate bid amounts
        base_amount = tender.estimated_value
        bids_data = []
        
        for j, bidder in enumerate(bidders):
            # Bid amount variation
            if bidder in preferred_suppliers:
                # Preferred suppliers might bid closer to estimate (less competitive)
                variation = random.uniform(0.95, 1.05)
            else:
                # Other suppliers bid more competitively
                variation = random.uniform(0.85, 1.1)
            
            bid_amount = base_amount * Decimal(str(variation))
            
            bids_data.append({
                'bidder': bidder,
                'amount': bid_amount,
                'is_preferred': bidder in preferred_suppliers
            })
        
        # Sort by bid amount and create TenderBid objects
        bids_data.sort(key=lambda x: x['amount'])
        
        winner = None
        for j, bid_data in enumerate(bids_data):
            is_winner = False
            
            if tender.status == 'awarded' and j == 0:  # Lowest bidder wins (normally)
                # But sometimes preferred supplier wins even if not lowest
                if bid_data['is_preferred'] and random.random() < 0.3:
                    is_winner = True
                elif not any(b['is_preferred'] for b in bids_data[:3]):  # No preferred in top 3
                    is_winner = True
                winner = bid_data['bidder']
            
            # Check if preferred supplier wins despite higher bid (corruption)
            elif tender.status == 'awarded' and bid_data['is_preferred'] and random.random() < 0.15:
                is_winner = True
                winner = bid_data['bidder']
            
            TenderBid.objects.create(
                tender=tender,
                bidder=bid_data['bidder'],
                bid_amount=bid_data['amount'],
                submission_date=tender.submission_deadline - timedelta(
                    hours=random.randint(1, 24 * max(1, (tender.submission_deadline - tender.publication_date).days))
                ),
                is_winner=is_winner,
                technical_score=random.randint(60, 95) if random.random() < 0.7 else None,
                financial_score=random.randint(60, 95) if random.random() < 0.7 else None,
            )
        
        # Set tender winner and award amount
        if winner and tender.status == 'awarded':
            tender.winner = winner
            winner_bid = TenderBid.objects.get(tender=tender, bidder=winner)
            tender.award_amount = winner_bid.bid_amount
            tender.save()
