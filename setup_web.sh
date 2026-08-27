#!/bin/bash

# Setup script for React + FastAPI Web Application

echo "🚀 Setting up AI Learning Material Generator Web App..."
echo ""

# ============================================
# BACKEND SETUP
# ============================================
echo "📦 Setting up Backend..."
echo ""

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm

# Copy Python modules from parent directory
echo "Copying Python modules..."
cp ../config.py .
cp ../pdf_processor.py .
cp ../text_processor.py .
cp ../embeddings.py .
cp ../vector_store.py .
cp ../notes_generator.py .
cp ../quiz_generator.py .
cp ../rag.py .
cp ../gemini_service.py .

# Check .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found in backend/"
    echo "📝 Please add your GEMINI_API_KEY to backend/.env"
else
    echo "✅ .env file found"
fi

cd ..

echo ""
echo "✅ Backend setup complete!"
echo ""

# ============================================
# FRONTEND SETUP
# ============================================
echo "📦 Setting up Frontend..."
echo ""

cd frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found!"
    echo "Please install Node.js from: https://nodejs.org/"
    exit 1
fi

echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"
echo ""

# Install npm dependencies
echo "Installing npm dependencies..."
npm install

cd ..

echo ""
echo "✅ Frontend setup complete!"
echo ""

# ============================================
# FINAL INSTRUCTIONS
# ============================================
echo "════════════════════════════════════════════════════════"
echo "✨ Setup Complete!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Add your GEMINI_API_KEY to backend/.env"
echo "   Get key from: https://aistudio.google.com/app/apikey"
echo ""
echo "2. Start the backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. Start the frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open browser: http://localhost:3000"
echo ""
echo "════════════════════════════════════════════════════════"
