#!/bin/bash

# Setup script for AI Learning Material Generator

echo "🚀 Setting up AI Learning Material Generator..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Downloading spaCy language model..."
python -m spacy download en_core_web_sm

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please create .env file and add your GEMINI_API_KEY"
    echo "   Get your key from: https://aistudio.google.com/app/apikey"
else
    echo "✅ .env file found"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your GEMINI_API_KEY to .env file"
echo "2. Run: streamlit run app.py"
echo ""
