# Quick Push to GitHub Script
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository: https://github.com/madhubalan098/multi-doc-summarizer" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  You will be prompted for credentials:" -ForegroundColor Yellow
Write-Host "   Username: madhubalan098" -ForegroundColor White
Write-Host "   Password: Use your Personal Access Token (not your password)" -ForegroundColor White
Write-Host ""
Write-Host "Don't have a token? Get one here:" -ForegroundColor Cyan
Write-Host "https://github.com/settings/tokens/new" -ForegroundColor Green
Write-Host "(Select 'repo' scope, then copy the token)" -ForegroundColor Gray
Write-Host ""
Write-Host "Pushing..." -ForegroundColor Yellow

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ SUCCESS! Code is now on GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 View your repo at:" -ForegroundColor Cyan
    Write-Host "https://github.com/madhubalan098/multi-doc-summarizer" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Next: Deploy on Streamlit Cloud" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Go to: https://share.streamlit.io/" -ForegroundColor White
    Write-Host "2. Sign in with GitHub" -ForegroundColor White
    Write-Host "3. Click 'New app'" -ForegroundColor White
    Write-Host "4. Repository: madhubalan098/multi-doc-summarizer" -ForegroundColor White
    Write-Host "5. Branch: main" -ForegroundColor White
    Write-Host "6. Main file: app.py" -ForegroundColor White
    Write-Host "7. Click Deploy!" -ForegroundColor White
    Write-Host ""
    Write-Host "Your app will be live at:" -ForegroundColor Cyan
    Write-Host "https://madhubalan098-multi-doc-summarizer.streamlit.app" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Push failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run this command manually:" -ForegroundColor Yellow
    Write-Host "git push -u origin main" -ForegroundColor White
    Write-Host ""
}

Read-Host "Press Enter to exit"
