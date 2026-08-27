# 🚀 START HERE - AI Learning Material Generator

Welcome! This document will get you started in **5 minutes**.

## What Is This?

An AI-powered application that transforms your PDF study materials into:
- 📝 **Smart Notes**: Concise, exam-oriented summaries
- 🧠 **Quizzes**: MCQs with answers and explanations  
- 💬 **AI Assistant**: Ask questions, get answers from your documents

## Quick Start (3 Steps)

### Step 1: Setup (2 minutes)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Get API Key (2 minutes)

1. Visit: https://aistudio.google.com/app/apikey
2. Create/copy your API key
3. Open `.env` file
4. Replace `your_gemini_api_key_here` with your actual key
5. Save the file

### Step 3: Run (1 minute)

```bash
streamlit run app.py
```

That's it! The app opens in your browser at http://localhost:8501

## First Time Usage

1. **Upload a PDF** - Click "Browse files" button
2. **Wait** - App processes the PDF (~10-30 seconds)
3. **Use features** - Try all three tabs:
   - Generate notes
   - Create quiz
   - Ask questions

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Complete documentation |
| **QUICKSTART.md** | Detailed setup guide |
| **ARCHITECTURE.md** | How the system works |
| **TROUBLESHOOTING.md** | Fix common issues |
| **PROJECT_STATUS.md** | What's been done |

## 🧪 Verify Installation

```bash
# Check all dependencies
python verify_setup.py

# Check configuration
python check_config.py

# Test components
python test_all.py
```

## ⚠️ Common Issues

### "GEMINI_API_KEY not found"
→ Add your API key to `.env` file

### "spaCy model not found"
→ Run: `python -m spacy download en_core_web_sm`

### "Module not found"
→ Activate venv: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)

### Port already in use
→ Run: `streamlit run app.py --server.port 8502`

See **TROUBLESHOOTING.md** for more solutions.

## 📁 Project Files

**Core Application:**
- `app.py` - Main Streamlit UI
- `config.py` - Settings
- `gemini_service.py` - AI integration
- `pdf_processor.py` - PDF handling
- `text_processor.py` - Text processing
- `embeddings.py` - Vector embeddings
- `vector_store.py` - FAISS search
- `rag.py` - Q&A system
- `notes_generator.py` - Notes generation
- `quiz_generator.py` - Quiz generation

**Setup & Testing:**
- `setup.sh` / `setup.bat` - Automated setup
- `verify_setup.py` - Check dependencies
- `check_config.py` - Validate configuration
- `test_gemini.py` - Test API
- `test_all.py` - Test all components

**Configuration:**
- `.env` - API key (YOU NEED TO EDIT THIS!)
- `requirements.txt` - Python packages
- `.gitignore` - Git ignore rules

## 🎯 Features

### Smart Notes
- Generates concise study notes
- Adapts to learning level (Beginner/Intermediate/Advanced)
- Considers study mode (Quick Revision/Exam Prep/Detailed Study)
- Downloadable as Markdown

### Quiz Generator
- Creates MCQs with 4 options each
- Adjustable difficulty (Easy/Medium/Hard)
- 3-10 questions per quiz
- Shows correct answers and explanations
- Downloadable as Markdown

### AI Study Assistant
- Ask any question about your PDF
- Gets answers grounded in your document
- Shows source chunks used
- Displays relevance scores

## 🔧 Configuration

Edit `config.py` to customize:

```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Embedding model
CHUNK_SIZE = 500                       # Words per chunk
CHUNK_OVERLAP = 100                    # Overlap between chunks
TOP_K = 4                              # Chunks to retrieve
GEMINI_MODEL = "gemini-2.0-flash-exp" # AI model
```

## 💡 Tips

1. **PDF Quality**: Use text-based PDFs (not scanned images)
2. **File Size**: Smaller PDFs (< 50 pages) work best
3. **Preferences**: Adjust learning level and study mode in sidebar
4. **Questions**: Be specific when asking questions
5. **Downloads**: Save generated materials for offline use

## 🎓 Example Workflow

1. Upload: `machine_learning_textbook_chapter3.pdf`
2. Set preferences:
   - Learning Level: Intermediate
   - Study Mode: Exam Preparation
3. Generate notes → Download → Read
4. Generate quiz (Medium, 5 questions) → Download → Practice
5. Ask questions → Review answers

## 📊 Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.0 Flash
- **Embeddings**: Sentence Transformers
- **Vector DB**: FAISS
- **NLP**: spaCy
- **PDF**: PyMuPDF

## 🔐 Security

- ✅ API key stored in `.env` (not committed to git)
- ✅ `.gitignore` protects sensitive files
- ✅ Input validation on all uploads
- ✅ Error handling prevents crashes

## 🐛 Something Not Working?

1. Run diagnostics:
   ```bash
   python verify_setup.py
   python check_config.py
   ```

2. Check documentation:
   - **TROUBLESHOOTING.md** - Common issues
   - **QUICKSTART.md** - Setup details
   - **README.md** - Full guide

3. Quick fixes:
   - Restart app
   - Refresh browser
   - Check `.env` file
   - Verify venv is activated

## 📈 Next Steps

Once everything works:

1. ✨ Try with your own study materials
2. 🎨 Experiment with different settings
3. 📖 Read ARCHITECTURE.md to understand how it works
4. 🔧 Customize config.py for your needs
5. 🚀 Share with friends!

## ✅ Checklist

Before using the app, ensure:

- ☐ Python 3.8+ installed
- ☐ Dependencies installed (`requirements.txt`)
- ☐ spaCy model downloaded (`en_core_web_sm`)
- ☐ Gemini API key added to `.env`
- ☐ Virtual environment activated
- ☐ `verify_setup.py` passes all checks

## 🎉 Ready to Go!

You're all set! Run:

```bash
streamlit run app.py
```

Upload a PDF and start learning! 📚

---

**Need help?** Check **TROUBLESHOOTING.md** or **README.md**
**Want to understand the code?** Read **ARCHITECTURE.md**
**Quick reference?** See **QUICKSTART.md**

Happy learning! 🚀
