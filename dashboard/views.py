from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg
from .models import Tender, RiskScore, Organization


def dashboard_view(request):
    """Main dashboard view with procurement analytics"""
    
    # Sample data for initial demo
    context = {
        'total_tenders': 1234,
        'high_risk_tenders': 156,
        'avg_risk_score': 3.2,
        'active_investigations': 23,
        'districts': [
            {'name': 'Dhaka', 'risk_score': 4.2, 'tender_count': 234},
            {'name': 'Chittagong', 'risk_score': 3.8, 'tender_count': 187},
            {'name': 'Sylhet', 'risk_score': 3.1, 'tender_count': 145},
            {'name': 'Rajshahi', 'risk_score': 2.9, 'tender_count': 123},
        ],
        'recent_tenders': [
            {
                'id': 1,
                'title': 'Road Construction Project',
                'organization': 'Roads and Highways Department',
                'amount': 50000000,
                'risk_score': 4.5,
                'date': '2024-01-15'
            },
            {
                'id': 2,
                'title': 'School Building Construction',
                'organization': 'Ministry of Education',
                'amount': 25000000,
                'risk_score': 2.1,
                'date': '2024-01-14'
            }
        ]
    }
    
    return render(request, 'dashboard/dashboard.html', context)


def tender_list_view(request):
    """List all tenders with filtering options"""
    
    # Sample tender data
    tenders = [
        {
            'id': 1,
            'title': 'Road Construction Project - Dhaka-Chittagong Highway',
            'organization': 'Roads and Highways Department',
            'amount': 50000000,
            'risk_score': 4.5,
            'status': 'Active',
            'date': '2024-01-15'
        },
        {
            'id': 2,
            'title': 'School Building Construction - Sylhet District',
            'organization': 'Ministry of Education',
            'amount': 25000000,
            'risk_score': 2.1,
            'status': 'Completed',
            'date': '2024-01-14'
        },
        {
            'id': 3,
            'title': 'Hospital Equipment Procurement',
            'organization': 'Ministry of Health',
            'amount': 15000000,
            'risk_score': 3.8,
            'status': 'Under Review',
            'date': '2024-01-13'
        }
    ]
    
    context = {
        'tenders': tenders,
        'total_count': len(tenders)
    }
    
    return render(request, 'dashboard/tender_list.html', context)


def tender_detail_view(request, tender_id):
    """Detailed view of a specific tender"""
    
    # Sample tender detail data
    tender = {
        'id': tender_id,
        'title': 'Road Construction Project - Dhaka-Chittagong Highway',
        'organization': 'Roads and Highways Department',
        'amount': 50000000,
        'risk_score': 4.5,
        'status': 'Active',
        'date': '2024-01-15',
        'description': 'Major highway construction project connecting Dhaka and Chittagong.',
        'risk_factors': [
            'Single bidder participation',
            'Unusually low bid amount',
            'Previous contractor issues'
        ],
        'bidders': [
            {'name': 'ABC Construction Ltd', 'bid_amount': 48000000},
            {'name': 'XYZ Builders', 'bid_amount': 52000000}
        ]
    }
    
    context = {'tender': tender}
    return render(request, 'dashboard/tender_detail.html', context)


def risk_analysis_view(request):
    """Risk analysis dashboard with charts and statistics"""
    
    # Sample risk analysis data
    context = {
        'risk_distribution': {
            'very_high': 15,
            'high': 45,
            'medium': 120,
            'low': 85,
            'very_low': 35
        },
        'risk_trends': [
            {'month': 'Jan', 'avg_risk': 3.2},
            {'month': 'Feb', 'avg_risk': 3.4},
            {'month': 'Mar', 'avg_risk': 3.1},
            {'month': 'Apr', 'avg_risk': 2.9},
            {'month': 'May', 'avg_risk': 3.3}
        ],
        'top_risk_organizations': [
            {'name': 'Roads and Highways Department', 'avg_risk': 4.2},
            {'name': 'Urban Development Authority', 'avg_risk': 3.8},
            {'name': 'Public Works Department', 'avg_risk': 3.5}
        ]
    }
    
    return render(request, 'dashboard/risk_analysis.html', context)


def api_tender_data(request):
    """API endpoint for tender data (JSON response)"""
    
    # Sample API data
    data = {
        'tenders': [
            {
                'id': 1,
                'title': 'Road Construction Project',
                'amount': 50000000,
                'risk_score': 4.5,
                'location': {'lat': 23.8103, 'lng': 90.4125}
            },
            {
                'id': 2,
                'title': 'School Building Construction',
                'amount': 25000000,
                'risk_score': 2.1,
                'location': {'lat': 24.8949, 'lng': 91.8687}
            }
        ]
    }
    
    return JsonResponse(data)


def api_risk_stats(request):
    """API endpoint for risk statistics"""
    
    data = {
        'total_tenders': 1234,
        'high_risk_count': 156,
        'average_risk_score': 3.2,
        'risk_distribution': {
            'very_high': 15,
            'high': 45,
            'medium': 120,
            'low': 85,
            'very_low': 35
        }
    }
    
    return JsonResponse(data)


def heatmap_view(request):
    """Heatmap view showing corruption risk by districts"""
    from .models import District, Tender, RiskScore
    
    # Get risk data by district
    districts = District.objects.all()
    heatmap_data = []
    
    for district in districts:
        # Count tenders in this district
        tender_count = Tender.objects.filter(
            buyer__district=district
        ).count()
        
        # Get average risk score for this district
        risk_scores = RiskScore.objects.filter(
            tender__buyer__district=district
        ).values_list('total_risk_score', flat=True)
        
        if risk_scores:
            avg_risk = sum(risk_scores) / len(risk_scores)
            risk_level = 'high' if avg_risk >= 7 else 'medium' if avg_risk >= 4 else 'low'
        else:
            avg_risk = 0
            risk_level = 'low'
        
        heatmap_data.append({
            'district': district,
            'tender_count': tender_count,
            'avg_risk_score': round(avg_risk, 2),
            'risk_level': risk_level
        })
    
    # Sort by risk score descending
    heatmap_data.sort(key=lambda x: x['avg_risk_score'], reverse=True)
    
    context = {
        'heatmap_data': heatmap_data,
        'total_districts': len(districts),
        'high_risk_districts': len([d for d in heatmap_data if d['risk_level'] == 'high']),
        'medium_risk_districts': len([d for d in heatmap_data if d['risk_level'] == 'medium']),
        'low_risk_districts': len([d for d in heatmap_data if d['risk_level'] == 'low']),
    }
    
    return render(request, 'dashboard/heatmap.html', context)
