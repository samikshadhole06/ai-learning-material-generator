"""
FastAPI Backend for AI Learning Material Generator
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os

# Import existing modules
import sys
sys.path.append('..')

from pdf_processor import extract_text_from_pdf
from text_processor import clean_text, extract_keywords, chunk_text
from embeddings import generate_embeddings
from vector_store import create_vector_store
from notes_generator import generate_notes
from quiz_generator import generate_quiz
from rag import ask_question

app = FastAPI(
    title="AI Learning Material Generator API",
    description="Transform PDFs into smart notes, quizzes, and get AI-powered answers",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (in production, use Redis or database)
documents = {}


# Request/Response Models
class ProcessResponse(BaseModel):
    doc_id: str
    num_characters: int
    num_chunks: int
    keywords: List[str]
    message: str


class NotesRequest(BaseModel):
    doc_id: str
    learning_level: str = "Intermediate"
    study_mode: str = "Quick Revision"


class QuizRequest(BaseModel):
    doc_id: str
    difficulty: str = "Medium"
    num_questions: int = 5


class QuestionRequest(BaseModel):
    doc_id: str
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[dict]


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": "AI Learning Material Generator API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/api/upload", response_model=ProcessResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file.
    Returns document ID and metadata.
    """
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Process PDF
        with open(tmp_path, 'rb') as f:
            raw_text = extract_text_from_pdf(f)
        
        if not raw_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF"
            )
        
        # Clean and process text
        cleaned_text = clean_text(raw_text)
        keywords = extract_keywords(cleaned_text)
        chunks = chunk_text(cleaned_text)
        
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Failed to create text chunks"
            )
        
        # Generate embeddings and create vector store
        embeddings = generate_embeddings(chunks)
        index = create_vector_store(embeddings)
        
        # Generate document ID
        doc_id = f"doc_{len(documents) + 1}"
        
        # Store document data
        documents[doc_id] = {
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'keywords': keywords,
            'chunks': chunks,
            'index': index,
            'filename': file.filename
        }
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return ProcessResponse(
            doc_id=doc_id,
            num_characters=len(cleaned_text),
            num_chunks=len(chunks),
            keywords=keywords,
            message="PDF processed successfully"
        )
        
    except Exception as e:
        if 'tmp_path' in locals():
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/api/generate-notes")
async def generate_notes_endpoint(request: NotesRequest):
    """Generate smart notes from uploaded document"""
    
    if request.doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        doc = documents[request.doc_id]
        context = "\n\n".join(doc['chunks'])
        
        notes = generate_notes(
            context,
            doc['keywords'],
            request.learning_level,
            request.study_mode
        )
        
        return {
            "notes": notes,
            "doc_id": request.doc_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating notes: {str(e)}")


@app.post("/api/generate-quiz")
async def generate_quiz_endpoint(request: QuizRequest):
    """Generate quiz from uploaded document"""
    
    if request.doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        doc = documents[request.doc_id]
        context = "\n\n".join(doc['chunks'])
        
        quiz = generate_quiz(
            context,
            request.difficulty,
            request.num_questions
        )
        
        return {
            "quiz": quiz,
            "doc_id": request.doc_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


@app.post("/api/ask-question", response_model=AnswerResponse)
async def ask_question_endpoint(request: QuestionRequest):
    """Ask a question about the uploaded document"""
    
    if request.doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        doc = documents[request.doc_id]
        
        answer, sources = ask_question(
            request.question,
            doc['index'],
            doc['chunks']
        )
        
        return AnswerResponse(
            answer=answer,
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")


@app.get("/api/documents")
async def list_documents():
    """List all uploaded documents"""
    return {
        "documents": [
            {
                "doc_id": doc_id,
                "filename": data['filename'],
                "num_chunks": len(data['chunks']),
                "num_keywords": len(data['keywords'])
            }
            for doc_id, data in documents.items()
        ]
    }


@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from memory"""
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    del documents[doc_id]
    
    return {"message": "Document deleted successfully", "doc_id": doc_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
