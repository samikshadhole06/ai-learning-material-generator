# 📚 AI-Powered Learning Material Generator

An intelligent study assistant that transforms PDFs into personalized learning materials using Google Gemini AI and RAG (Retrieval-Augmented Generation).

## Features

- **📝 Smart Notes Generator**: Generate concise, exam-oriented notes from PDFs
- **🧠 Quiz Generator**: Create multiple-choice questions with difficulty levels
- **💬 AI Study Assistant**: Ask questions and get answers grounded in your study material
- **🔍 Semantic Search**: Uses vector embeddings and FAISS for relevant context retrieval

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **NLP**: spaCy
- **PDF Processing**: PyMuPDF

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy model

```bash
python -m spacy download en_core_web_sm
```

### 5. Set up Gemini API Key

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a `.env` file in the project root
3. Add your API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

## Usage

### Run the application

```bash
streamlit run app.py
```

### Test Gemini API connection

```bash
python test_gemini.py
```

## Project Structure

```
├── app.py                  # Main Streamlit application
├── config.py               # Configuration and environment variables
├── gemini_service.py       # Gemini AI integration
├── pdf_processor.py        # PDF text extraction
├── text_processor.py       # Text cleaning and keyword extraction
├── embeddings.py           # Generate vector embeddings
├── vector_store.py         # FAISS vector database
├── notes_generator.py      # Smart notes generation
├── quiz_generator.py       # Quiz generation
├── rag.py                  # RAG-based question answering
├── test_gemini.py          # API connection test
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (not in git)
```

## How It Works

1. **Upload PDF**: User uploads study material in PDF format
2. **Text Extraction**: Extract text using PyMuPDF
3. **Text Processing**: Clean text and extract keywords using spaCy
4. **Chunking**: Split text into overlapping chunks
5. **Embeddings**: Convert chunks to vector embeddings
6. **Vector Store**: Store embeddings in FAISS index
7. **Features**:
   - **Notes**: Generate summarized notes with Gemini AI
   - **Quiz**: Create MCQs based on content
   - **Q&A**: Retrieve relevant chunks and answer questions

## Configuration

Edit `config.py` to customize:

- `EMBEDDING_MODEL`: Sentence transformer model
- `CHUNK_SIZE`: Text chunk size (default: 500 words)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 100 words)
- `TOP_K`: Number of relevant chunks to retrieve (default: 4)

## Learning Preferences

- **Learning Level**: Beginner, Intermediate, Advanced
- **Study Mode**: Quick Revision, Exam Preparation, Detailed Study
- **Quiz Difficulty**: Easy, Medium, Hard

## Troubleshooting

### spaCy model not found

```bash
python -m spacy download en_core_web_sm
```

### Gemini API errors

- Verify your API key is correct in `.env`
- Check you have API quota remaining
- Ensure you're using a valid model name

### FAISS installation issues

If `faiss-cpu` fails to install, try:

```bash
pip install faiss-cpu --no-cache-dir
```

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
