# Project Architecture

## Overview

This is an AI-powered learning material generator that uses RAG (Retrieval-Augmented Generation) to create personalized study materials from PDF documents.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│                        (app.py)                              │
└────────────┬────────────────────────────────┬────────────────┘
             │                                │
             ▼                                ▼
┌────────────────────────┐      ┌────────────────────────────┐
│   PDF Processing       │      │   Gemini AI Service        │
│  (pdf_processor.py)    │      │  (gemini_service.py)       │
└───────────┬────────────┘      └───────────┬────────────────┘
            │                               │
            ▼                               │
┌────────────────────────┐                  │
│   Text Processing      │                  │
│  (text_processor.py)   │                  │
│  - Cleaning            │                  │
│  - Keyword Extraction  │                  │
│  - Chunking            │                  │
└───────────┬────────────┘                  │
            │                               │
            ▼                               │
┌────────────────────────┐                  │
│   Embeddings           │                  │
│  (embeddings.py)       │                  │
│  - Sentence Trans.     │                  │
└───────────┬────────────┘                  │
            │                               │
            ▼                               │
┌────────────────────────┐                  │
│   Vector Store         │                  │
│  (vector_store.py)     │◄─────────────────┤
│  - FAISS Index         │                  │
└───────────┬────────────┘                  │
            │                               │
            ▼                               │
┌────────────────────────────────────────────┼────────────────┐
│                RAG Pipeline                │                │
│                 (rag.py)                   │                │
│  ┌──────────┐  ┌──────────┐  ┌───────────┴──────────┐    │
│  │ Query    │→ │ Retrieve │→ │ Generate w/ Context  │    │
│  └──────────┘  └──────────┘  └──────────────────────┘    │
└───────────────────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────────────────────┐
│            Content Generators                              │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │    Notes     │  │     Quiz     │                       │
│  │ (notes_gen)  │  │  (quiz_gen)  │                       │
│  └──────────────┘  └──────────────┘                       │
└────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer (`app.py`)
- **Purpose**: User interface and orchestration
- **Framework**: Streamlit
- **Features**:
  - File upload handling
  - Session state management
  - Three main tabs: Notes, Quiz, Q&A
  - User preferences (learning level, study mode)

### 2. PDF Processing (`pdf_processor.py`)
- **Purpose**: Extract text from PDF files
- **Library**: PyMuPDF (fitz)
- **Functions**:
  - `extract_text_from_pdf()`: Extracts text from all pages
  - `clean_text()`: Removes extra whitespace and special characters

### 3. Text Processing (`text_processor.py`)
- **Purpose**: Prepare text for embedding and analysis
- **Library**: spaCy
- **Functions**:
  - `clean_text()`: Basic text cleaning
  - `extract_keywords()`: Extract important nouns/proper nouns
  - `chunk_text()`: Split text into overlapping chunks

**Chunking Strategy**:
- Default chunk size: 500 words
- Overlap: 100 words
- Prevents context loss at chunk boundaries

### 4. Embeddings (`embeddings.py`)
- **Purpose**: Convert text to numerical vectors
- **Model**: all-MiniLM-L6-v2 (Sentence Transformers)
- **Dimension**: 384-dimensional vectors
- **Functions**:
  - `generate_embeddings()`: Batch embed text chunks
  - `generate_query_embedding()`: Embed user questions

### 5. Vector Store (`vector_store.py`)
- **Purpose**: Store and search embeddings efficiently
- **Library**: FAISS (Facebook AI Similarity Search)
- **Index Type**: IndexFlatL2 (L2 distance)
- **Functions**:
  - `create_vector_store()`: Initialize FAISS index
  - `search_vector_store()`: Find top-K similar chunks

### 6. RAG System (`rag.py`)
- **Purpose**: Retrieval-Augmented Generation
- **Process**:
  1. Embed user question
  2. Search vector store for relevant chunks
  3. Combine retrieved chunks as context
  4. Generate answer using Gemini AI

### 7. Gemini AI Service (`gemini_service.py`)
- **Purpose**: Interface with Google Gemini API
- **Model**: gemini-2.0-flash-exp
- **Configuration**:
  - Temperature: 0.7 (balanced creativity)
  - Top-P: 0.95
  - Top-K: 40
  - Max tokens: 2048

### 8. Content Generators

#### Notes Generator (`notes_generator.py`)
- Creates summarized study notes
- Considers learning level and study mode
- Focuses on exam-relevant content

#### Quiz Generator (`quiz_generator.py`)
- Generates multiple-choice questions
- Adjustable difficulty
- Provides correct answers and explanations

## Data Flow

### Uploading and Processing
```
PDF Upload → Text Extraction → Text Cleaning → Keyword Extraction
                                              ↓
                                         Chunking
                                              ↓
                                   Generate Embeddings
                                              ↓
                                    Create FAISS Index
                                              ↓
                                  Store in Session State
```

### Generating Notes/Quiz
```
User Request → Combine Chunks → Construct Prompt → Gemini API → Response
```

### Answering Questions (RAG)
```
User Question → Embed Question → Search FAISS → Retrieve Top-K Chunks
                                                        ↓
                              Construct Prompt with Context
                                                        ↓
                                      Gemini API → Answer
```

## Configuration (`config.py`)

Central configuration file for:
- API keys (from .env)
- Model selection
- Chunking parameters
- RAG parameters

## Key Design Decisions

### 1. Why Overlapping Chunks?
- Prevents information loss at boundaries
- Improves context retrieval quality
- 100-word overlap provides continuity

### 2. Why FAISS?
- Fast similarity search
- Efficient memory usage
- No external database required
- Perfect for local deployment

### 3. Why Sentence Transformers?
- Pre-trained on semantic similarity
- Good balance of speed and quality
- Lightweight (< 100MB model)
- Works offline after download

### 4. Why RAG over Direct Generation?
- Grounds answers in uploaded material
- Reduces hallucination
- Provides source attribution
- More accurate for domain-specific content

### 5. Why Streamlit?
- Rapid prototyping
- Built-in session state
- Easy file upload handling
- Minimal frontend code

## Performance Considerations

### Processing Speed
- PDF extraction: ~1-2 seconds/page
- Embedding generation: ~0.5 seconds/chunk
- FAISS search: <100ms for 1000 vectors
- Gemini API: 2-5 seconds/request

### Memory Usage
- FAISS index: ~4MB per 1000 chunks
- Embeddings: ~1.5KB per chunk
- Model: ~100MB (sentence-transformers)

### Scalability Limits
- Recommended max PDF size: 50 pages
- Max chunks in memory: ~10,000
- FAISS can handle millions (with proper index type)

## Security Considerations

1. **API Key Management**
   - Stored in .env (not committed)
   - Loaded via python-dotenv
   - Never exposed in UI

2. **Input Validation**
   - PDF file type checking
   - Text extraction error handling
   - Empty content detection

3. **Rate Limiting**
   - Gemini API has built-in limits
   - No additional rate limiting implemented

## Error Handling

- Comprehensive try-catch blocks
- User-friendly error messages
- Graceful degradation
- Detailed error logging

## Future Improvements

1. **Multi-format Support**: DOCX, TXT, HTML
2. **Persistent Storage**: Save processed documents
3. **Advanced Chunking**: Semantic chunking
4. **Better Index**: FAISS IVF for larger datasets
5. **Caching**: Cache embeddings and responses
6. **Batch Processing**: Process multiple PDFs
7. **Export Options**: PDF, DOCX output formats
8. **Analytics**: Track usage and performance

## Dependencies

See `requirements.txt` for complete list.

Key dependencies:
- `streamlit`: Frontend framework
- `pymupdf`: PDF processing
- `sentence-transformers`: Embeddings
- `faiss-cpu`: Vector search
- `spacy`: NLP processing
- `google-genai`: Gemini AI API

## Testing

- `test_gemini.py`: API connectivity
- `test_all.py`: Comprehensive test suite
- `verify_setup.py`: Dependency verification
- `check_config.py`: Configuration validation
