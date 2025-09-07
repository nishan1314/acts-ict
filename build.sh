#!/usr/bin/env bash
# Build script for Render deployment

echo "🚀 Building ACTS - Accountability & Corruption Tracking System..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

echo "✅ Build completed successfully!"
echo "🇧🇩 ACTS is ready for deployment!"
