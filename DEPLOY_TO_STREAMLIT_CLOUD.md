# 🚀 Deploy to Streamlit Cloud

Your code is on GitHub! Now let's deploy it to Streamlit Cloud so it's accessible online.

## 📋 Prerequisites

✅ Code on GitHub: https://github.com/samikshadhole06/ai-learning-material-generator
✅ Gemini API key ready

## 🌐 Deploy Steps

### Step 1: Go to Streamlit Cloud

Visit: **https://share.streamlit.io/**

### Step 2: Sign In

- Click **"Sign in"**
- Use your **GitHub account** (samikshadhole06)
- Authorize Streamlit

### Step 3: Deploy New App

1. Click **"New app"**
2. Fill in:
   - **Repository:** `samikshadhole06/ai-learning-material-generator`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **"Advanced settings"**
4. Add **Secrets** (IMPORTANT!):
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
   Replace with your real API key!

5. Click **"Deploy"**

### Step 4: Wait

- Deployment takes 2-5 minutes
- You'll see logs as it installs dependencies
- When done, your app will be live!

---

## 🎯 Your App URL

After deployment, you'll get a URL like:
```
https://samikshadhole06-ai-learning-material-generator.streamlit.app
```

---

## ⚠️ Important Notes

### 1. PyTorch Issue

The app might fail during deployment because PyTorch (122MB) is large. 

**Solution:** Add this to your repository:

Create `packages.txt` file with:
```
python3-dev
```

And update `requirements.txt` to use CPU-only PyTorch:
```
torch --index-url https://download.pytorch.org/whl/cpu
```

### 2. Resource Limits

Streamlit Cloud free tier has:
- 1 GB RAM
- 1 CPU core
- 1 GB storage

Your app should work fine, but large PDFs may be slow.

---

## 🔧 If Deployment Fails

### Common Issues:

**1. Dependencies too large**
- Remove PyTorch temporarily
- App will work for PDF processing only
- Add back later if needed

**2. Missing API key**
- Make sure you added GEMINI_API_KEY in secrets
- No quotes around the key

**3. Requirements timeout**
- Try installing packages one by one
- Use lighter alternatives

---

## 📝 Quick Fix: Deploy Without PyTorch First

To ensure deployment works:

1. Edit `requirements.txt` - comment out torch:
   ```
   # torch>=2.2
   ```

2. Commit and push:
   ```bash
   git add requirements.txt
   git commit -m "Remove torch for deployment"
   git push
   ```

3. Try deploying again

The app will work for:
- ✅ PDF upload
- ✅ Text extraction  
- ✅ Keyword extraction
- ❌ Notes/Quiz (needs torch)

Add torch back later once deployed successfully!

---

## 🎉 After Successful Deployment

Your app will be live at:
```
https://[your-app-name].streamlit.app
```

Share this URL with anyone!

---

## 💡 Alternative: Deploy Web App

Instead of Streamlit, deploy the React+FastAPI version:

**Backend:** Deploy to Railway/Render
**Frontend:** Deploy to Vercel/Netlify

This gives you more control but is more complex.

---

## ✅ Recommended Path

1. **First:** Deploy Streamlit version (simpler)
2. **Test:** Make sure it works
3. **Later:** Add torch if needed
4. **Advanced:** Deploy React+FastAPI version

---

**Ready to deploy?** Go to https://share.streamlit.io/ and follow Step 2-3!
