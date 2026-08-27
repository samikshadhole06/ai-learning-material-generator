# 🚀 EASY START GUIDE - Use This!

## Your internet has connection issues. Let's use the SIMPLE Streamlit version instead!

### ✅ **3 SIMPLE STEPS**

#### **Step 1: Install Packages**

Open Command Prompt in your project folder and run:

```bash
pip install streamlit pymupdf sentence-transformers faiss-cpu spacy google-genai python-dotenv numpy
```

If this fails due to internet, try one at a time:
```bash
pip install streamlit
pip install pymupdf
pip install sentence-transformers
pip install faiss-cpu
pip install spacy
pip install google-genai
pip install python-dotenv
pip install numpy
```

#### **Step 2: Download spaCy Model**

```bash
python -m spacy download en_core_web_sm
```

If this fails, download manually:
1. Go to: https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0.tar.gz
2. Download the file
3. Install: `pip install en_core_web_sm-3.7.0.tar.gz`

#### **Step 3: Add API Key**

1. Open `.env` file in Notepad
2. Go to: https://aistudio.google.com/app/apikey
3. Get your API key
4. In `.env`, replace `your_gemini_api_key_here` with your actual key
5. Save

### 🎯 **RUN THE APP**

Simply run:
```bash
streamlit run app.py
```

Or double-click: **RUN_APP.bat**

The app will open automatically in your browser!

---

## ❌ **If Internet Keeps Failing**

Your internet connection is unstable. Try:

1. **Use mobile hotspot** instead of WiFi
2. **Turn off VPN** if you're using one
3. **Try different time** when internet is better
4. **Download packages manually**:
   - Go to: https://pypi.org/
   - Search for each package
   - Download .whl files
   - Install: `pip install package_name.whl`

---

## 💡 **Forget the Web App** (React + FastAPI)

The web app needs:
- ✅ Stable internet connection (you don't have)
- ✅ Node.js installation (you don't have)
- ✅ More complex setup

**Use Streamlit instead!** It's:
- ✅ One command to run
- ✅ Works without Node.js
- ✅ Same features
- ✅ Much simpler!

---

## 🆘 **Still Having Issues?**

Run this to check what's missing:
```bash
python verify_setup.py
```

This will tell you exactly what needs to be installed.

---

## ✅ **Quick Check**

Run these to see if packages are installed:
```bash
python -c "import streamlit; print('Streamlit OK')"
python -c "import fitz; print('PyMuPDF OK')"
python -c "import spacy; print('spaCy OK')"
python -c "import google.genai; print('Gemini OK')"
```

---

**TLDR:** Just run `streamlit run app.py` after installing packages and adding API key!
