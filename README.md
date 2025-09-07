# ACTS - Accountability & Corruption Tracking System

![ACTS Logo](https://img.shields.io/badge/ACTS-Bangladesh%20Government-006A4E?style=for-the-badge&logo=shield)

A comprehensive AI-powered transparency platform for government procurement monitoring, citizen reporting, and corruption prevention in Bangladesh.

## 🇧🇩 Digital Bangladesh Initiative

ACTS (Accountability & Corruption Tracking System) is a cutting-edge digital platform designed to enhance transparency and accountability in government operations across Bangladesh. Built with modern web technologies and AI algorithms, it empowers citizens and strengthens governance.

## ✨ Features

### 🔍 Smart Detection
- **AI-Powered Analysis**: Advanced algorithms analyze procurement data to identify suspicious patterns
- **Risk Scoring**: Automated corruption risk assessment for tenders and contracts
- **Pattern Recognition**: Detection of unusual bidding behaviors and irregularities

### � Citizen Empowerment
- **Anonymous Reporting**: Secure platform for citizens to report corruption incidents
- **Blockchain Receipts**: SHA-256 encrypted receipts for report verification
- **Case Tracking**: Monitor the status of submitted reports
- **Whistleblower Protection**: Secure and anonymous reporting system

### � Analytics & Insights
- **Real-time Dashboards**: Interactive visualizations of corruption patterns
- **Geographic Mapping**: Heatmaps showing risk levels across Bangladesh districts
- **Trend Analysis**: Historical data analysis and forecasting
- **Risk Assessment Reports**: Comprehensive risk evaluations

### �️ Data Protection
- **Enterprise Security**: Bank-grade security for sensitive information
- **Privacy Protection**: Anonymized data processing
- **Secure Communications**: Encrypted data transmission

## 🚀 Technology Stack

- **Backend**: Django 4.2.7 (Python)
- **Database**: PostgreSQL with SQLite for development
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Analytics**: Pandas, NetworkX for data analysis
- **Visualization**: Chart.js, Leaflet for maps
- **Security**: SHA-256 encryption, Django security features
- **Typography**: Montserrat font family with Kalpurush for Bengali
- **Icons**: Font Awesome 6.4.0

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Installation

1. **Clone and Setup**
   ```cmd
   git clone <repository-url>
   cd ACTS
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```cmd
   createdb shuddho_map
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Load Sample Data**
   ```cmd
   python manage.py load_sample_data
   ```

4. **Run Development Server**
   ```cmd
   python manage.py runserver
   ```

5. **Access Application**
   - Dashboard: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/
   - API Docs: http://localhost:8000/api/docs/

## Project Structure

```
ACTS/
├── shuddho_map/           # Main Django project
├── dashboard/             # Dashboard app (tenders, risks, heatmaps)
├── citizen_reports/       # Citizen reporting system
├── data_analysis/         # Risk scoring and data processing
├── static/               # CSS, JS, images
├── templates/            # HTML templates
├── media/                # User uploads
├── sample_data/          # Demo procurement data
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md           # This file
```

## API Endpoints

### Dashboard API
- `GET /api/tenders/` - List all tenders with risk scores
- `GET /api/districts/risks/` - District-wise risk aggregation
- `GET /api/analytics/summary/` - Overall statistics

### Citizen Reports API
- `POST /api/reports/` - Submit new report
- `GET /api/reports/` - List all reports (public)
- `GET /api/receipts/{hash}/` - Verify integrity receipt

## Development

### Running Tests
```cmd
python manage.py test
```

### Code Style
```cmd
flake8 .
black .
```

### Database Migrations
```cmd
python manage.py makemigrations
python manage.py migrate
```

## Sample Data

The application includes sample Bangladesh procurement data with:
- 500+ tender records across all 64 districts
- Realistic buyer-supplier relationships
- Various risk scenarios for demonstration

## Demo Scenarios

1. **High-Risk Tender Detection**: Single bidder with short tender window
2. **Geographic Risk Clustering**: Districts with multiple suspicious patterns
3. **Citizen Report Verification**: Upload evidence and verify integrity receipt
4. **Network Analysis**: Visualize buyer-supplier relationship patterns

## Deployment Notes

This is a prototype for demonstration. For production deployment:
- Use environment variables for secrets
- Configure proper media storage (MinIO/S3)
- Set up SSL/HTTPS
- Configure production database
- Implement proper authentication/authorization
- Add rate limiting and security headers

## Contributing

This project was created for the PTIB Civic Tech Challenge 2025. Contributions welcome!

## License

Open source for civic technology advancement.

---

**Built for the PTIB Civic Tech Challenge 2025**  
*Empowering transparency through technology*
