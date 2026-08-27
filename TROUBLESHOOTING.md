# Troubleshooting Guide

Common issues and their solutions for the AI Learning Material Generator.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Configuration Issues](#configuration-issues)
3. [Runtime Issues](#runtime-issues)
4. [PDF Processing Issues](#pdf-processing-issues)
5. [API Issues](#api-issues)
6. [Performance Issues](#performance-issues)

---

## Installation Issues

### Python Version Error
**Error**: `Python version 3.8 or higher required`

**Solution**:
```bash
# Check your Python version
python --version

# If too old, install Python 3.8+
# Windows: Download from python.org
# macOS: brew install python@3.11
# Linux: sudo apt install python3.11
```

### pip Not Found
**Error**: `pip: command not found`

**Solution**:
```bash
# Install pip
python -m ensurepip --upgrade

# Or use
python -m pip --version
```

### FAISS Installation Failed
**Error**: `Failed building wheel for faiss-cpu`

**Solution**:
```bash
# Try without cache
pip install faiss-cpu --no-cache-dir

# Or try conda
conda install -c conda-forge faiss-cpu

# Windows: Make sure Visual C++ redistributables are installed
```

### spaCy Model Download Failed
**Error**: `Can't find model 'en_core_web_sm'`

**Solution**:
```bash
# Download the model
python -m spacy download en_core_web_sm

# If behind proxy
python -m spacy download en_core_web_sm --proxy http://proxy:port

# If still fails, manual download
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0.tar.gz
```

---

## Configuration Issues

### GEMINI_API_KEY Not Found
**Error**: `GEMINI_API_KEY not found. Please add it to the .env file.`

**Solution**:
1. Ensure `.env` file exists in project root
2. Open `.env` and add:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Get key from: https://aistudio.google.com/app/apikey
4. Restart the application

**Verify**:
```bash
python check_config.py
```

### .env File Not Loading
**Error**: API key in `.env` but still not recognized

**Solution**:
```bash
# Check file location (must be in project root)
ls -la .env

# Check file encoding (should be UTF-8)
file .env

# Verify no extra spaces
cat .env

# Reload environment
python
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> import os
>>> print(os.getenv("GEMINI_API_KEY"))
```

### Virtual Environment Issues
**Error**: Packages installed but not found

**Solution**:
```bash
# Ensure venv is activated
# You should see (venv) in your prompt

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Verify correct Python
which python  # should point to venv/bin/python

# Reinstall if needed
pip install -r requirements.txt
```

---

## Runtime Issues

### Streamlit Won't Start
**Error**: `streamlit: command not found`

**Solution**:
```bash
# Ensure venv is activated
source venv/bin/activate

# Install streamlit
pip install streamlit

# Run with python -m
python -m streamlit run app.py
```

### Port Already in Use
**Error**: `Port 8501 is already in use`

**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8501 | xargs kill
```

### Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'X'`

**Solution**:
```bash
# Verify venv is activated
which python

# Reinstall dependencies
pip install -r requirements.txt

# If specific module missing
pip install <module-name>
```

### Session State Errors
**Error**: `KeyError: 'chunks'` or similar

**Solution**:
- Refresh the browser page
- Upload the PDF again
- Clear browser cache
- Restart Streamlit app

---

## PDF Processing Issues

### No Text Extracted from PDF
**Error**: `No readable text found in PDF`

**Causes**:
1. PDF contains only images (scanned document)
2. PDF is encrypted/password protected
3. PDF uses unsupported encoding

**Solutions**:
1. **For scanned PDFs**: Use OCR tool first
   ```bash
   # Install OCR tool
   pip install pdf2image pytesseract
   ```

2. **For encrypted PDFs**: Unlock first
   - Use online tools or Adobe Acrobat
   - Or try: `qpdf --decrypt input.pdf output.pdf`

3. **Try different PDF**: Test with a simple text-based PDF

**Verify PDF**:
```python
import fitz
doc = fitz.open("your_file.pdf")
print(doc[0].get_text())  # Should print text from first page
```

### PDF Processing Too Slow
**Issue**: Large PDF takes too long

**Solutions**:
1. Use smaller PDFs (< 50 pages)
2. Extract specific pages
3. Split large PDF into sections
4. Increase chunk size in `config.py`:
   ```python
   CHUNK_SIZE = 1000  # Larger chunks = fewer embeddings
   ```

### Corrupted PDF Error
**Error**: `Failed to process PDF`

**Solutions**:
1. Verify PDF is not corrupted:
   ```bash
   # Try opening in another PDF reader
   ```

2. Repair PDF:
   ```bash
   # Use online repair tools or
   qpdf --check input.pdf
   ```

3. Re-export PDF from source document

---

## API Issues

### Gemini API Authentication Failed
**Error**: `Invalid API key` or `Authentication failed`

**Solutions**:
1. Verify API key is correct
2. Check for extra spaces in `.env`
3. Ensure key starts with `AIza`
4. Generate new key: https://aistudio.google.com/app/apikey

**Test API**:
```bash
python test_gemini.py
```

### Rate Limit Exceeded
**Error**: `429 Too Many Requests` or `Quota exceeded`

**Solutions**:
1. Wait a few minutes before trying again
2. Check quota: https://aistudio.google.com/
3. Reduce frequency of requests
4. Use caching (upcoming feature)

### Gemini API Timeout
**Error**: `Request timeout` or no response

**Solutions**:
1. Check internet connection
2. Try again (temporary network issue)
3. Reduce context size (fewer chunks)
4. Check Gemini API status

### API Response Errors
**Error**: `Error generating response`

**Solutions**:
1. Check if prompt is too long
2. Verify content is appropriate
3. Try simpler request first
4. Check API quotas

---

## Performance Issues

### Slow Embedding Generation
**Issue**: Takes long time to process

**Solutions**:
1. Reduce chunk size (fewer chunks)
2. Use CPU efficiently:
   ```python
   # In embeddings.py, ensure:
   model.encode(..., show_progress_bar=False)
   ```
3. Consider GPU if available (change requirements.txt)

### High Memory Usage
**Issue**: Application uses too much RAM

**Solutions**:
1. Process smaller PDFs
2. Increase chunk size (fewer total chunks)
3. Clear session state after processing:
   ```python
   del st.session_state.raw_text  # If not needed
   ```
4. Close other applications

### Slow Vector Search
**Issue**: FAISS search takes long

**Solutions**:
1. Reduce TOP_K in `config.py`
2. For large datasets, use different FAISS index:
   ```python
   # In vector_store.py
   index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
   ```

---

## General Debugging

### Enable Debug Mode

**Check logs**:
```bash
streamlit run app.py --logger.level=debug
```

**Add print statements**:
```python
# In any file
print(f"Debug: variable = {variable}")
```

**Python debugger**:
```python
import pdb; pdb.set_trace()
```

### Verify All Components

```bash
# Run comprehensive check
python verify_setup.py

# Check configuration
python check_config.py

# Test all components
python test_all.py
```

### Reset Everything

```bash
# Delete virtual environment
rm -rf venv/

# Reinstall
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## Getting Help

### Before Asking for Help

1. ✅ Run `python verify_setup.py`
2. ✅ Run `python check_config.py`
3. ✅ Check error logs
4. ✅ Try with simple test PDF
5. ✅ Read relevant documentation

### Include in Bug Reports

1. Python version: `python --version`
2. OS and version
3. Error message (full traceback)
4. Steps to reproduce
5. What you've already tried
6. Output of `verify_setup.py`

### Useful Commands

```bash
# System info
python --version
pip list

# Package versions
pip show streamlit
pip show google-genai

# Environment check
python verify_setup.py
python check_config.py
python test_all.py
```

---

## Quick Fixes Checklist

When something doesn't work, try these in order:

1. ☐ Restart Streamlit app
2. ☐ Refresh browser page
3. ☐ Clear browser cache
4. ☐ Check API key in `.env`
5. ☐ Verify venv is activated
6. ☐ Run `python verify_setup.py`
7. ☐ Check internet connection
8. ☐ Try with different PDF
9. ☐ Restart computer
10. ☐ Reinstall dependencies

---

## Still Having Issues?

If you've tried everything:

1. Check project documentation:
   - `README.md` - Main documentation
   - `QUICKSTART.md` - Setup guide
   - `ARCHITECTURE.md` - System design

2. Verify example code:
   ```bash
   python test_gemini.py
   python test_all.py
   ```

3. Start fresh:
   - Create new virtual environment
   - Reinstall all dependencies
   - Use a simple test PDF

4. Check system requirements:
   - Python 3.8+
   - 4GB+ RAM available
   - Internet connection
   - Sufficient disk space

Remember: Most issues are environment-related. A clean reinstall usually fixes them! 🔧
