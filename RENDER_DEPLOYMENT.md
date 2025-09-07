# 🚀 ACTS Deployment Guide for Render

## Prerequisites Checklist ✅

✅ **Project Setup Complete**
- Django project configured with production settings
- WhiteNoise middleware for static files
- Environment variables configured with python-decouple
- Procfile created (`web: gunicorn shuddho_map.wsgi`)
- requirements.txt with all dependencies
- Static files collected

✅ **GitHub Repository Ready**
- Repository: https://github.com/nishan1314/acts-ict.git
- All files committed and pushed

## 🔗 Step-by-Step Render Deployment

### 1. **Create Render Account**
- Go to: https://render.com/
- Sign up with your GitHub account
- Verify your email address

### 2. **Create New Web Service**
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account if not already connected
3. Select repository: **`nishan1314/acts-ict`**
4. Click **"Connect"**

### 3. **Configure Deployment Settings**

#### Basic Settings:
- **Name**: `actsbd` (Bangladesh ACTS platform)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn shuddho_map.wsgi:application`

#### Advanced Settings:
- **Instance Type**: Free (for testing) or paid for production
- **Environment**: `Python 3.13` (or latest stable)

### 4. **Environment Variables** 
Add these in the Render dashboard under "Environment":

```
SECRET_KEY=your-super-secret-django-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=actsbd.onrender.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=acts_db
DB_USER=acts_user
DB_PASSWORD=your-db-password
DB_HOST=your-postgres-host
DB_PORT=5432
```

### 5. **Create PostgreSQL Database**
1. In Render dashboard: **"New +"** → **"PostgreSQL"**
2. **Name**: `acts-database`
3. **Region**: Same as your web service
4. **Plan**: Free or paid
5. After creation, copy connection details to environment variables

### 6. **Deploy Application**
1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Collect static files
   - Start the application

### 7. **Post-Deployment Setup**
After successful deployment, run these commands in Render's shell:

```bash
# Create database tables
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Load sample data
python manage.py load_sample_data
```

## 🔧 Environment Variables Explanation

| Variable | Purpose | Example |
|----------|---------|---------|
| `SECRET_KEY` | Django security key | Generate at: https://djecrety.ir/ |
| `DEBUG` | Production setting | `False` |
| `ALLOWED_HOSTS` | Allowed domains | `actsbd.onrender.com` |
| `DB_ENGINE` | Database type | `django.db.backends.postgresql` |
| `DB_NAME` | Database name | From Render PostgreSQL |
| `DB_USER` | Database user | From Render PostgreSQL |
| `DB_PASSWORD` | Database password | From Render PostgreSQL |
| `DB_HOST` | Database host | From Render PostgreSQL |
| `DB_PORT` | Database port | `5432` |

## 🌐 Custom Domain (Optional)

1. In your web service settings
2. Go to **"Settings"** → **"Custom Domains"**
3. Add your domain: `acts.gov.bd` (example)
4. Update DNS records as instructed

## 📊 Monitoring & Logs

- **Logs**: Available in Render dashboard
- **Metrics**: CPU, Memory usage tracking
- **Health Checks**: Automatic monitoring

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check requirements.txt for typos
   - Ensure all dependencies are listed

2. **Static Files Not Loading**
   - Verify WhiteNoise in MIDDLEWARE
   - Check STATIC_ROOT setting

3. **Database Connection Errors**
   - Verify environment variables
   - Check PostgreSQL service status

4. **500 Internal Server Error**
   - Check logs in Render dashboard
   - Verify SECRET_KEY is set
   - Ensure DEBUG=False

### Debug Commands:
```bash
# Check environment variables
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES)"

# Test database connection
python manage.py dbshell

# Collect static files manually
python manage.py collectstatic --noinput
```

## 🎯 Expected URLs After Deployment

- **Landing Page**: `https://actsbd.onrender.com/`
- **Dashboard**: `https://actsbd.onrender.com/dashboard/`
- **Admin Panel**: `https://actsbd.onrender.com/admin/`
- **API Docs**: `https://actsbd.onrender.com/api/docs/`
- **Citizen Reports**: `https://actsbd.onrender.com/reports/`

## 🇧🇩 Bangladesh Government Features Ready

✅ **Procurement Monitoring** - AI-powered tender analysis  
✅ **Risk Detection** - Corruption pattern identification  
✅ **Citizen Reporting** - Secure anonymous reporting  
✅ **District Heatmaps** - Geographic risk visualization  
✅ **Bengali Language** - Kalpurush font support  
✅ **Mobile Responsive** - Works on all devices  

## 🔐 Security Features

✅ **HTTPS** - Automatic SSL certificates  
✅ **Environment Variables** - Secure configuration  
✅ **WhiteNoise** - Static file serving  
✅ **CSRF Protection** - Built-in Django security  
✅ **SHA-256 Encryption** - Report integrity  

---

## 🚀 Quick Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Configure environment variables
- [ ] Create PostgreSQL database
- [ ] Deploy web service
- [ ] Run migrations
- [ ] Test application

**Your ACTS platform will be live at: `https://actsbd.onrender.com`**

🇧🇩 **Building Transparent Digital Bangladesh!**
