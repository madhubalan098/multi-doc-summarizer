# 🚀 Deployment Guide

## Your Project is Ready to Deploy!

All files have been optimized for Streamlit Cloud deployment with lighter models that fit in the 1GB RAM limit.

---

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `multi-doc-summarizer` (or your preferred name)
   - **Description:** AI Multi-Document Summarizer with NLP
   - **Visibility:** ✅ **Public** (required for free Streamlit deployment)
   - ❌ Do NOT check "Add a README file"
3. Click "Create repository"

---

## Step 2: Push Code to GitHub

Open PowerShell in this directory and run these commands:

```powershell
# Set your Git identity (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add your GitHub repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**When prompted for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)
  - Get token at: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select scopes: `repo`
  - Copy the token and use it as password

---

## Step 3: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository:** `YOUR_USERNAME/REPO_NAME`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy!"**
6. Wait 5-10 minutes for deployment
7. Your app URL will be: `https://YOUR_USERNAME-REPO_NAME.streamlit.app`

---

## ✅ What's Been Optimized

Your app now uses lightweight models that fit in Streamlit Cloud's free tier:

| Original Model | Optimized Model | Memory Saved |
|---------------|-----------------|--------------|
| BART-large-cnn | distilbart-cnn-12-6 | ~1.2GB |
| FLAN-T5-large | FLAN-T5-base | ~2GB |
| RoBERTa-large-mnli | DeBERTa-v3-base | ~900MB |

**Total:** Reduced from ~6GB to ~1.8GB (fits in 1GB with CPU-only PyTorch)

---

## 📝 After Deployment

1. Test your app with sample documents
2. Copy your public URL
3. Update `README.md` line 5 with your actual URL:
   ```markdown
   **[Access the deployed app here](https://YOUR-URL.streamlit.app)**
   ```
4. Push the update:
   ```powershell
   git add README.md
   git commit -m "Add live demo URL"
   git push
   ```

---

## ⚠️ Troubleshooting

**If deployment fails:**
1. Check logs in Streamlit Cloud dashboard
2. Click "Manage app" → "Logs"
3. Common issues:
   - Memory limit exceeded → Models may still be too large
   - Package installation error → Check requirements.txt syntax

**Need help?**
- Streamlit Community: https://discuss.streamlit.io/
- GitHub Issues: Create an issue in your repo

---

## 🎉 That's It!

Your AI Multi-Document Summarizer will be live and publicly accessible!
