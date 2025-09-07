"""
Risk Analysis Engine for ACTS
Detects corruption red flags in procurement data
"""
import pandas as pd
import networkx as nx
from collections import defaultdict
from dashboard.models import Tender, TenderBid, RiskScore, Organization


class RiskAnalyzer:
    """Main risk analysis engine"""
    
    def __init__(self):
        self.risk_weights = {
            'single_bid': 40,
            'short_window': 25,
            'repeated_pair': 30,
            'network_risk': 5,
        }
    
    def analyze_all_tenders(self):
        """Analyze all tenders and update risk scores"""
        tenders = Tender.objects.all()
        results = {
            'total_analyzed': 0,
            'high_risk_found': 0,
            'flags_detected': defaultdict(int),
        }
        
        for tender in tenders:
            risk_score = self.analyze_tender(tender)
            
            results['total_analyzed'] += 1
            if risk_score.risk_level in ['high', 'critical']:
                results['high_risk_found'] += 1
            
            # Count flags
            if risk_score.single_bid_flag:
                results['flags_detected']['single_bid'] += 1
            if risk_score.short_window_flag:
                results['flags_detected']['short_window'] += 1
            if risk_score.repeated_pair_flag:
                results['flags_detected']['repeated_pair'] += 1
        
        return results
    
    def analyze_tender(self, tender):
        """Analyze a single tender for risk factors"""
        risk_score, created = RiskScore.objects.get_or_create(
            tender=tender,
            defaults={
                'analysis_version': '1.0'
            }
        )
        
        # Reset scores
        risk_score.single_bid_score = 0
        risk_score.short_window_score = 0
        risk_score.repeated_pair_score = 0
        risk_score.network_risk_score = 0
        
        # Reset flags
        risk_score.single_bid_flag = False
        risk_score.short_window_flag = False
        risk_score.repeated_pair_flag = False
        risk_score.high_value_flag = False
        
        # 1. Single Bid Analysis
        self._analyze_single_bid(tender, risk_score)
        
        # 2. Short Tender Window Analysis
        self._analyze_short_window(tender, risk_score)
        
        # 3. Repeated Buyer-Supplier Pairs
        self._analyze_repeated_pairs(tender, risk_score)
        
        # 4. Network Risk Analysis
        self._analyze_network_risk(tender, risk_score)
        
        # 5. High Value Flag
        self._analyze_high_value(tender, risk_score)
        
        # Calculate total risk score
        risk_score.total_risk_score = (
            risk_score.single_bid_score * self.risk_weights['single_bid'] // 100 +
            risk_score.short_window_score * self.risk_weights['short_window'] // 100 +
            risk_score.repeated_pair_score * self.risk_weights['repeated_pair'] // 100 +
            risk_score.network_risk_score * self.risk_weights['network_risk'] // 100
        )
        
        # Ensure score is within bounds
        risk_score.total_risk_score = min(100, max(0, risk_score.total_risk_score))
        
        risk_score.save()
        return risk_score
    
    def _analyze_single_bid(self, tender, risk_score):
        """Detect single-bid tenders"""
        bid_count = tender.bids.count()
        
        if bid_count == 0:
            # No bids recorded, but if there's a winner, assume single bid
            if tender.winner:
                risk_score.single_bid_flag = True
                risk_score.single_bid_score = 100
        elif bid_count == 1:
            risk_score.single_bid_flag = True
            risk_score.single_bid_score = 100
        elif bid_count == 2:
            # Two bids is still suspicious
            risk_score.single_bid_score = 60
        elif bid_count == 3:
            # Three bids, moderate risk
            risk_score.single_bid_score = 30
        else:
            # Four or more bids, low risk
            risk_score.single_bid_score = 0
    
    def _analyze_short_window(self, tender, risk_score):
        """Detect short tender windows"""
        if tender.tender_window_days is not None:
            days = tender.tender_window_days
            
            if days < 3:
                risk_score.short_window_flag = True
                risk_score.short_window_score = 100
            elif days < 7:
                risk_score.short_window_flag = True
                risk_score.short_window_score = 80
            elif days < 14:
                risk_score.short_window_score = 40
            elif days < 21:
                risk_score.short_window_score = 20
            else:
                risk_score.short_window_score = 0
    
    def _analyze_repeated_pairs(self, tender, risk_score):
        """Detect repeated buyer-supplier pairs"""
        if not tender.winner:
            return
        
        # Count how many times this buyer-supplier pair has occurred
        repeated_count = Tender.objects.filter(
            buyer=tender.buyer,
            winner=tender.winner,
            status='awarded'
        ).exclude(pk=tender.pk).count()
        
        if repeated_count >= 5:
            risk_score.repeated_pair_flag = True
            risk_score.repeated_pair_score = 100
        elif repeated_count >= 3:
            risk_score.repeated_pair_flag = True
            risk_score.repeated_pair_score = 80
        elif repeated_count >= 2:
            risk_score.repeated_pair_score = 60
        elif repeated_count == 1:
            risk_score.repeated_pair_score = 30
        else:
            risk_score.repeated_pair_score = 0
    
    def _analyze_network_risk(self, tender, risk_score):
        """Analyze network patterns for suspicious relationships"""
        if not tender.winner:
            return
        
        # Look for network patterns (simplified version)
        # This could be expanded with more sophisticated graph analysis
        
        # Check if the supplier wins unusually often
        supplier = tender.winner
        total_tenders = Tender.objects.filter(status='awarded').count()
        supplier_wins = Tender.objects.filter(winner=supplier, status='awarded').count()
        
        if total_tenders > 0:
            win_rate = supplier_wins / total_tenders
            
            if win_rate > 0.2:  # Wins more than 20% of all tenders
                risk_score.network_risk_score = 100
            elif win_rate > 0.1:  # Wins more than 10%
                risk_score.network_risk_score = 60
            elif win_rate > 0.05:  # Wins more than 5%
                risk_score.network_risk_score = 30
            else:
                risk_score.network_risk_score = 0
    
    def _analyze_high_value(self, tender, risk_score):
        """Flag high-value tenders for additional scrutiny"""
        # Calculate median tender value for comparison
        median_value = self._get_median_tender_value()
        
        if tender.estimated_value > median_value * 10:
            risk_score.high_value_flag = True
        elif tender.estimated_value > median_value * 5:
            risk_score.high_value_flag = True
    
    def _get_median_tender_value(self):
        """Calculate median tender value"""
        values = list(Tender.objects.values_list('estimated_value', flat=True))
        if not values:
            return 0
        
        values.sort()
        n = len(values)
        if n % 2 == 0:
            return (values[n//2 - 1] + values[n//2]) / 2
        else:
            return values[n//2]


class NetworkAnalyzer:
    """Analyze relationship networks between buyers and suppliers"""
    
    def __init__(self):
        self.graph = nx.Graph()
    
    def build_network(self):
        """Build network graph from tender data"""
        self.graph.clear()
        
        # Add nodes for organizations
        organizations = Organization.objects.all()
        for org in organizations:
            self.graph.add_node(
                org.id, 
                name=org.name, 
                type=org.organization_type,
                district=org.district.name
            )
        
        # Add edges for tender relationships
        awarded_tenders = Tender.objects.filter(
            status='awarded',
            winner__isnull=False
        ).select_related('buyer', 'winner')
        
        for tender in awarded_tenders:
            if self.graph.has_node(tender.buyer.id) and self.graph.has_node(tender.winner.id):
                if self.graph.has_edge(tender.buyer.id, tender.winner.id):
                    # Increment weight
                    self.graph[tender.buyer.id][tender.winner.id]['weight'] += 1
                    self.graph[tender.buyer.id][tender.winner.id]['tenders'].append(tender.id)
                else:
                    # Add new edge
                    self.graph.add_edge(
                        tender.buyer.id, 
                        tender.winner.id,
                        weight=1,
                        tenders=[tender.id]
                    )
    
    def find_suspicious_patterns(self):
        """Find suspicious patterns in the network"""
        self.build_network()
        
        patterns = {
            'highly_connected_suppliers': [],
            'exclusive_relationships': [],
            'cluster_analysis': {},
        }
        
        # Find highly connected suppliers
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            if node_data['type'] in ['supplier', 'both']:
                degree = self.graph.degree(node_id)
                if degree >= 5:  # Connected to 5+ buyers
                    patterns['highly_connected_suppliers'].append({
                        'organization_id': node_id,
                        'name': node_data['name'],
                        'connections': degree,
                    })
        
        # Find exclusive relationships (high weight edges)
        for edge in self.graph.edges(data=True):
            weight = edge[2]['weight']
            if weight >= 3:  # 3+ tenders between same pair
                buyer_name = self.graph.nodes[edge[0]]['name']
                supplier_name = self.graph.nodes[edge[1]]['name']
                patterns['exclusive_relationships'].append({
                    'buyer_id': edge[0],
                    'supplier_id': edge[1],
                    'buyer_name': buyer_name,
                    'supplier_name': supplier_name,
                    'tender_count': weight,
                })
        
        return patterns
    
    def get_network_stats(self):
        """Get overall network statistics"""
        if not self.graph.nodes():
            self.build_network()
        
        stats = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'connected_components': nx.number_connected_components(self.graph),
        }
        
        if stats['total_nodes'] > 0:
            # Average clustering coefficient
            stats['avg_clustering'] = nx.average_clustering(self.graph)
            
            # Most connected organizations
            degrees = dict(self.graph.degree())
            if degrees:
                max_degree_node = max(degrees, key=degrees.get)
                stats['most_connected'] = {
                    'organization_id': max_degree_node,
                    'name': self.graph.nodes[max_degree_node]['name'],
                    'connections': degrees[max_degree_node],
                }
        
        return stats


class DataImporter:
    """Import and process procurement data"""
    
    def import_from_csv(self, csv_file_path):
        """Import tender data from CSV file"""
        try:
            df = pd.read_csv(csv_file_path)
            return self._process_dataframe(df)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def import_from_dataframe(self, df):
        """Import tender data from pandas DataFrame"""
        return self._process_dataframe(df)
    
    def _process_dataframe(self, df):
        """Process DataFrame and create database records"""
        results = {
            'success': True,
            'imported_tenders': 0,
            'imported_organizations': 0,
            'imported_bids': 0,
            'errors': [],
        }
        
        try:
            # Process organizations first
            self._import_organizations(df, results)
            
            # Then process tenders
            self._import_tenders(df, results)
            
            # Finally process bids
            self._import_bids(df, results)
            
        except Exception as e:
            results['success'] = False
            results['errors'].append(str(e))
        
        return results
    
    def _import_organizations(self, df, results):
        """Import organizations from DataFrame"""
        # This is a simplified version - in practice, you'd need more sophisticated
        # organization matching and deduplication
        pass
    
    def _import_tenders(self, df, results):
        """Import tenders from DataFrame"""
        # This is a simplified version - you'd implement the actual CSV parsing
        # and tender creation logic here
        pass
    
    def _import_bids(self, df, results):
        """Import bids from DataFrame"""
        # This is a simplified version - you'd implement the actual bid
        # import logic here
        pass
