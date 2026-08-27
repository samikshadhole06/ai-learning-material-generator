# 🌐 React + FastAPI Web Application

Modern full-stack web application for AI Learning Material Generator.

## 🏗️ Architecture

```
Frontend (React)  ←→  Backend (FastAPI)  ←→  AI Services (Gemini)
     :3000              :8000                    
```

**Frontend**: React + Vite (Modern UI)  
**Backend**: FastAPI (REST API)  
**AI**: Google Gemini API

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ and npm
- Gemini API key

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy environment file
# Add your GEMINI_API_KEY to backend/.env

# Start backend server
python main.py
```

Backend runs at: **http://localhost:8000**

### 2. Frontend Setup

```bash
# Navigate to frontend (in a NEW terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: **http://localhost:3000**

### 3. Configure API Key

Edit `backend/.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your key from: https://aistudio.google.com/app/apikey

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   └── (copy all .py files from root)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styles
│   │   ├── main.jsx        # Entry point
│   │   └── index.css       # Global styles
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
```

## 🌐 API Endpoints

### Upload PDF
```http
POST /api/upload
Content-Type: multipart/form-data

Response: {
  "doc_id": "doc_1",
  "num_characters": 15000,
  "num_chunks": 30,
  "keywords": ["machine", "learning", ...],
  "message": "PDF processed successfully"
}
```

### Generate Notes
```http
POST /api/generate-notes
Content-Type: application/json

{
  "doc_id": "doc_1",
  "learning_level": "Intermediate",
  "study_mode": "Quick Revision"
}

Response: {
  "notes": "# Study Notes\n\n...",
  "doc_id": "doc_1"
}
```

### Generate Quiz
```http
POST /api/generate-quiz
Content-Type: application/json

{
  "doc_id": "doc_1",
  "difficulty": "Medium",
  "num_questions": 5
}

Response: {
  "quiz": "# Quiz\n\nQuestion 1:\n...",
  "doc_id": "doc_1"
}
```

### Ask Question
```http
POST /api/ask-question
Content-Type: application/json

{
  "doc_id": "doc_1",
  "question": "What is machine learning?"
}

Response: {
  "answer": "Machine learning is...",
  "sources": [
    {"text": "...", "score": 0.85},
    ...
  ]
}
```

## 🎨 Features

### Modern UI
- ✨ Beautiful gradient design
- 📱 Fully responsive (mobile-friendly)
- 🎯 Intuitive tab navigation
- 🎨 Smooth animations
- 📊 Real-time statistics

### Functionality
- 📄 PDF upload and processing
- 📝 Smart notes generation
- 🧠 Quiz creation with adjustable settings
- 💬 AI-powered Q&A with source attribution
- 💾 Download notes and quizzes
- ⚙️ Customizable preferences

## 🔧 Development

### Backend Development
```bash
cd backend

# Run with auto-reload
uvicorn main:app --reload --port 8000

# Run tests
python test_all.py

# View API docs
# Open: http://localhost:8000/docs
```

### Frontend Development
```bash
cd frontend

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📦 Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
# Output: frontend/dist/
```

### Deploy Backend

**Option 1: Uvicorn (Simple)**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Option 2: Docker**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY backend/ .
COPY *.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Option 3: Cloud Platforms**
- **Railway**: Connect GitHub, auto-deploy
- **Render**: Web Service from Git
- **Heroku**: Git push deployment
- **AWS EC2**: Full control
- **Google Cloud Run**: Containerized apps

### Deploy Frontend

**Option 1: Vercel**
```bash
cd frontend
npm install -g vercel
vercel --prod
```

**Option 2: Netlify**
```bash
cd frontend
npm install -g netlify-cli
netlify deploy --prod
```

**Option 3: GitHub Pages**
```bash
cd frontend
npm run build
# Upload dist/ folder
```

## 🔒 Security

### Backend
- CORS configured for frontend origin
- File type validation
- Error handling
- Input sanitization

### Frontend
- XSS protection via React
- HTTPS in production
- Environment variables
- Secure API calls

### Environment Variables
```bash
# backend/.env
GEMINI_API_KEY=your_key_here

# frontend/.env (if needed)
VITE_API_URL=https://your-backend-url.com
```

## 🐛 Troubleshooting

### Backend Issues

**"Module not found"**
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**"Port already in use"**
```bash
# Use different port
uvicorn main:app --port 8001
```

**"CORS error"**
- Check backend/main.py CORS settings
- Ensure frontend URL is in allow_origins

### Frontend Issues

**"npm: command not found"**
- Install Node.js from: https://nodejs.org/

**"Can't connect to backend"**
- Ensure backend is running on port 8000
- Check vite.config.js proxy settings

**"Build fails"**
```bash
# Clean and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 🚀 Access the Application

Once both servers are running:

1. Open browser: **http://localhost:3000**
2. Upload a PDF file
3. Wait for processing
4. Use the features:
   - Generate notes
   - Create quizzes
   - Ask questions

## 📊 Performance

- PDF processing: ~10-30 seconds
- Notes generation: ~5-10 seconds
- Quiz generation: ~10-15 seconds
- Question answering: ~2-5 seconds

## 🎯 Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

## 📱 Mobile Responsive

The UI automatically adapts to:
- 📱 Mobile phones (< 768px)
- 📱 Tablets (768px - 1024px)
- 💻 Desktop (> 1024px)

## 🔄 API Documentation

Interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎓 Next Steps

1. ✅ Complete setup (backend + frontend)
2. 🔑 Add Gemini API key
3. 🚀 Start both servers
4. 📄 Upload a test PDF
5. 🎨 Customize UI (App.css)
6. 🌐 Deploy to production

## 💡 Tips

- Use small PDFs for testing (< 20 pages)
- Keep backend terminal open to see logs
- Clear browser cache if UI doesn't update
- Check browser console for frontend errors
- Check terminal for backend errors

## 📚 Documentation

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Vite**: https://vitejs.dev/
- **Axios**: https://axios-http.com/

## ✨ Features Coming Soon

- [ ] User authentication
- [ ] Save documents to database
- [ ] Multiple file formats (DOCX, TXT)
- [ ] Export to PDF
- [ ] Dark mode
- [ ] Progress indicators
- [ ] Batch processing

---

**Enjoy your modern web application!** 🎉

For issues, check the troubleshooting section or original documentation.
