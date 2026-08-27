# 🚀 Web App Quick Start

Get your React + FastAPI web application running in **3 simple steps**!

## ⚡ Super Quick Setup

### Windows:
```bash
# 1. Run automated setup
setup_web.bat

# 2. Add your API key to backend/.env
# Get from: https://aistudio.google.com/app/apikey

# 3. Start servers (2 separate terminals)
# Terminal 1:
start_backend.bat

# Terminal 2:
start_frontend.bat
```

### Linux/macOS:
```bash
# 1. Run automated setup
chmod +x setup_web.sh
./setup_web.sh

# 2. Add your API key to backend/.env
# Get from: https://aistudio.google.com/app/apikey

# 3. Start servers (2 separate terminals)
# Terminal 1:
./start_backend.sh

# Terminal 2:
./start_frontend.sh
```

## 🌐 Access the App

Open your browser and go to: **http://localhost:3000**

## 📋 What You Need

- **Python 3.8+** - For backend
- **Node.js 16+** - For frontend
- **Gemini API Key** - Get from https://aistudio.google.com/app/apikey

## 🎯 Using the Web App

1. **Open** http://localhost:3000 in your browser
2. **Upload** a PDF document
3. **Wait** for processing (~10-30 seconds)
4. **Use features**:
   - 📝 Smart Notes - Generate study notes
   - 🧠 Quiz - Create practice questions
   - 💬 Ask AI - Get answers from your PDF

## 🔧 Manual Setup (If Scripts Don't Work)

### Backend Setup:
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Copy Python files
cp ../config.py .
cp ../pdf_processor.py .
cp ../text_processor.py .
cp ../embeddings.py .
cp ../vector_store.py .
cp ../notes_generator.py .
cp ../quiz_generator.py .
cp ../rag.py .
cp ../gemini_service.py .

# Add API key to .env
python main.py
```

### Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

## ⚠️ Common Issues

### "Node.js not found"
Install from: https://nodejs.org/

### "Port 8000 already in use"
```bash
# Kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS:
lsof -ti:8000 | xargs kill
```

### "Port 3000 already in use"
The script will automatically use port 3001 or you can:
```bash
cd frontend
npm run dev -- --port 3001
```

### "CORS error in browser"
- Make sure backend is running on port 8000
- Check backend/main.py CORS settings

### "API key error"
- Ensure you've added your key to `backend/.env`
- Key should start with `AIza`
- No quotes needed around the key

## 📱 Features

✨ **Beautiful Modern UI**
- Gradient design
- Smooth animations
- Responsive layout

📄 **PDF Processing**
- Upload and analyze PDFs
- Extract keywords
- Create searchable chunks

📝 **Smart Notes**
- Exam-oriented summaries
- Customizable learning level
- Downloadable as Markdown

🧠 **Quiz Generator**
- Multiple choice questions
- Adjustable difficulty
- Includes explanations

💬 **AI Q&A**
- Ask anything about your PDF
- Get source references
- View relevance scores

## 🎨 Customization

Edit frontend styles:
- `frontend/src/App.css` - Component styles
- `frontend/src/index.css` - Global styles

Edit backend:
- `backend/main.py` - API endpoints
- `backend/.env` - Configuration

## 📊 What to Expect

**Backend Terminal** will show:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Frontend Terminal** will show:
```
VITE v5.0.8  ready in 1234 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

**Browser** will show:
- Modern gradient interface
- Upload PDF section
- Three feature tabs
- Sidebar with preferences

## 🎓 First Time Usage

1. Click "Choose PDF File"
2. Select a PDF (test with small file < 20 pages)
3. Wait for "PDF processed successfully!" alert
4. Try generating notes
5. Try creating a quiz
6. Try asking questions

## 💡 Pro Tips

- Use smaller PDFs for faster processing
- Adjust learning level in sidebar
- Download generated content
- Check "View Retrieved Material" in Q&A
- Keep both terminals open while using

## 🆘 Need Help?

1. **Check both terminals** for error messages
2. **Read** WEB_APP_README.md for detailed docs
3. **Verify** Python and Node.js are installed
4. **Confirm** API key is in backend/.env
5. **Try** restarting both servers

## ✅ Checklist

Before starting:
- ☐ Python 3.8+ installed
- ☐ Node.js 16+ installed
- ☐ Gemini API key obtained
- ☐ API key added to backend/.env
- ☐ Both terminals ready

## 🚀 You're Ready!

Your modern web application is set up. Enjoy creating smart learning materials! 📚

---

**Backend**: http://localhost:8000 (API)  
**Frontend**: http://localhost:3000 (Web UI)  
**API Docs**: http://localhost:8000/docs (Swagger)

For detailed documentation, see **WEB_APP_README.md**
