# Multi-Doc Summarizer - GitHub Push Script
# Run this script to push your code to GitHub

Write-Host "🚀 Multi-Doc Summarizer Deployment Helper" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is configured
$gitName = git config user.name
$gitEmail = git config user.email

if (-not $gitName) {
    Write-Host "⚙️  Git Configuration Needed" -ForegroundColor Yellow
    Write-Host ""
    $name = Read-Host "Enter your name"
    $email = Read-Host "Enter your email"
    
    git config user.name "$name"
    git config user.email "$email"
    Write-Host "✅ Git configured!" -ForegroundColor Green
    Write-Host ""
}

# Get GitHub repository URL
Write-Host "📦 GitHub Repository Setup" -ForegroundColor Yellow
Write-Host ""
Write-Host "First, create a NEW repository on GitHub:"
Write-Host "  1. Go to: https://github.com/new" -ForegroundColor Cyan
Write-Host "  2. Name it: multi-doc-summarizer (or any name)" -ForegroundColor Cyan
Write-Host "  3. Make it PUBLIC (required for free Streamlit)" -ForegroundColor Cyan
Write-Host "  4. Do NOT add README" -ForegroundColor Cyan
Write-Host "  5. Click 'Create repository'" -ForegroundColor Cyan
Write-Host ""

$username = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter your repository name"

$repoUrl = "https://github.com/$username/$repoName.git"

Write-Host ""
Write-Host "📤 Setting up remote repository..." -ForegroundColor Yellow

# Remove existing origin if any
git remote remove origin 2>$null

# Add new origin
git remote add origin $repoUrl

# Check if main branch exists, if not rename master to main
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    git branch -M main
}

Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  IMPORTANT: When prompted for password, use a Personal Access Token:" -ForegroundColor Red
Write-Host "   Get token at: https://github.com/settings/tokens" -ForegroundColor Cyan
Write-Host "   Click 'Generate new token (classic)' → Select 'repo' scope" -ForegroundColor Cyan
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ SUCCESS! Code pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://share.streamlit.io/" -ForegroundColor White
    Write-Host "  2. Sign in with GitHub" -ForegroundColor White
    Write-Host "  3. Click 'New app'" -ForegroundColor White
    Write-Host "  4. Select repository: $username/$repoName" -ForegroundColor White
    Write-Host "  5. Branch: main" -ForegroundColor White
    Write-Host "  6. Main file: app.py" -ForegroundColor White
    Write-Host "  7. Click 'Deploy!'" -ForegroundColor White
    Write-Host ""
    Write-Host "📱 Your app will be live at:" -ForegroundColor Cyan
    Write-Host "   https://$username-$repoName.streamlit.app" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Please check the error above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - Wrong username/repo name" -ForegroundColor White
    Write-Host "  - Invalid credentials (use Personal Access Token, not password)" -ForegroundColor White
    Write-Host "  - Repository doesn't exist on GitHub" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
