"""
Comprehensive test suite to verify all components work correctly.
"""

import sys

def test_gemini_api():
    """Test Gemini API connection."""
    print("\n=== Testing Gemini API ===")
    
    try:
        from gemini_service import generate_response
        
        response = generate_response(
            "Say 'Hello! API is working.' in exactly those words."
        )
        
        if response and len(response) > 0:
            print("✅ Gemini API is working")
            print(f"   Response: {response[:100]}...")
            return True
        else:
            print("❌ Gemini API returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {str(e)}")
        return False


def test_text_processor():
    """Test text processing functions."""
    print("\n=== Testing Text Processor ===")
    
    try:
        from text_processor import clean_text, extract_keywords, chunk_text
        
        # Test clean_text
        test_text = "This   is  a\ntest\n\ntext."
        cleaned = clean_text(test_text)
        assert "test text" in cleaned.lower()
        print("✅ clean_text() works")
        
        # Test extract_keywords
        sample_text = "Natural language processing is a field of artificial intelligence. NLP enables computers to understand human language."
        keywords = extract_keywords(sample_text)
        assert len(keywords) > 0
        print(f"✅ extract_keywords() works (found {len(keywords)} keywords)")
        
        # Test chunk_text
        chunks = chunk_text(sample_text, chunk_size=10, overlap=2)
        assert len(chunks) > 0
        print(f"✅ chunk_text() works (created {len(chunks)} chunks)")
        
        return True
        
    except Exception as e:
        print(f"❌ Text processor test failed: {str(e)}")
        return False


def test_embeddings():
    """Test embedding generation."""
    print("\n=== Testing Embeddings ===")
    
    try:
        from embeddings import generate_embeddings, generate_query_embedding
        
        test_chunks = [
            "Machine learning is a subset of AI.",
            "Deep learning uses neural networks."
        ]
        
        embeddings = generate_embeddings(test_chunks)
        assert embeddings.shape[0] == 2
        print(f"✅ generate_embeddings() works (shape: {embeddings.shape})")
        
        query_emb = generate_query_embedding("What is AI?")
        assert len(query_emb) > 0
        print(f"✅ generate_query_embedding() works (dimension: {len(query_emb)})")
        
        return True
        
    except Exception as e:
        print(f"❌ Embeddings test failed: {str(e)}")
        return False


def test_vector_store():
    """Test FAISS vector store."""
    print("\n=== Testing Vector Store ===")
    
    try:
        from embeddings import generate_embeddings, generate_query_embedding
        from vector_store import create_vector_store, search_vector_store
        
        test_chunks = [
            "Python is a programming language.",
            "Java is used for enterprise applications.",
            "JavaScript runs in web browsers."
        ]
        
        embeddings = generate_embeddings(test_chunks)
        index = create_vector_store(embeddings)
        print("✅ create_vector_store() works")
        
        query = "Tell me about Python"
        query_emb = generate_query_embedding(query)
        results = search_vector_store(index, query_emb, test_chunks, top_k=2)
        
        assert len(results) > 0
        assert "Python" in results[0]["text"]
        print(f"✅ search_vector_store() works (found {len(results)} results)")
        
        return True
        
    except Exception as e:
        print(f"❌ Vector store test failed: {str(e)}")
        return False


def test_generators():
    """Test notes and quiz generators."""
    print("\n=== Testing Generators ===")
    
    try:
        from notes_generator import generate_notes
        from quiz_generator import generate_quiz
        
        context = "Artificial Intelligence is the simulation of human intelligence by machines."
        keywords = ["artificial", "intelligence", "machine"]
        
        # Test notes generator
        notes = generate_notes(context, keywords, "Beginner", "Quick Revision")
        assert len(notes) > 0
        print("✅ generate_notes() works")
        
        # Test quiz generator
        quiz = generate_quiz(context, "Easy", 2)
        assert len(quiz) > 0
        print("✅ generate_quiz() works")
        
        return True
        
    except Exception as e:
        print(f"❌ Generators test failed: {str(e)}")
        return False


def test_rag():
    """Test RAG question answering."""
    print("\n=== Testing RAG ===")
    
    try:
        from embeddings import generate_embeddings
        from vector_store import create_vector_store
        from rag import ask_question
        
        chunks = [
            "Machine learning is a method of data analysis.",
            "Neural networks are inspired by biological neurons.",
            "Deep learning achieves high accuracy in image recognition."
        ]
        
        embeddings = generate_embeddings(chunks)
        index = create_vector_store(embeddings)
        
        question = "What is machine learning?"
        answer, sources = ask_question(question, index, chunks, top_k=2)
        
        assert len(answer) > 0
        assert len(sources) > 0
        print("✅ ask_question() works")
        print(f"   Retrieved {len(sources)} relevant chunks")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG test failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Running Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Text Processor", test_text_processor),
        ("Embeddings", test_embeddings),
        ("Vector Store", test_vector_store),
        ("Gemini API", test_gemini_api),
        ("Generators", test_generators),
        ("RAG System", test_rag),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ {name} test crashed: {str(e)}")
            results[name] = False
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your NLP project is ready to use.")
        print("Run: streamlit run app.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
