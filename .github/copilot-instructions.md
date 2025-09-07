<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
- [x] Verify that the copilot-instructions.md file in the .github directory is created.

- [x] Clarify Project Requirements
	✅ Project: ACTS - Accountability & Corruption Tracking System prototype for Bangladesh
	✅ Tech Stack: Django backend, PostgreSQL database, Pandas/NetworkX for data analysis
	✅ Features: Procurement data analysis, risk scoring, citizen reporting, transparency logs

- [x] Scaffold the Project
	✅ Created Django project structure with all necessary components:
	- Main Django project (shuddho_map)
	- Dashboard app (tender analysis, risk scoring, heatmaps)
	- Citizen reports app (corruption reporting, integrity receipts)
	- Data analysis app (risk algorithms, network analysis)
	- Templates and static files structure
	- Database models for all features
	- API endpoints and serializers

- [x] Customize the Project
	✅ Implemented all ACTS features according to specifications:
	- Procurement data models with risk scoring
	- Bangladesh districts and organizations
	- Risk detection algorithms (single bid, short window, repeated pairs)
	- Citizen reporting with SHA-256 integrity receipts
	- Dashboard with statistics and visualizations
	- Management commands for sample data loading
	- Environment configuration

- [x] Install Required Extensions
	✅ No specific extensions required - using standard Django with web libraries

- [x] Compile the Project
	✅ Installed dependencies and set up database:
	- Created Python virtual environment
	- Installed Django, DRF, and all required packages
	- Set up SQLite database for demo
	- Created static files directory

- [x] Create and Run Task
	✅ Set up Django development server task running on http://localhost:8000

- [x] Launch the Project
	✅ Application is running successfully:
	- Django development server active
	- Web interface accessible
	- API endpoints available at /api/docs/
	- Admin panel at /admin/

- [x] Ensure Documentation is Complete
	✅ Created comprehensive README with setup instructions and project overview
	✅ Added setup.bat script for easy Windows installation
	✅ Documented all features and API endpoints
