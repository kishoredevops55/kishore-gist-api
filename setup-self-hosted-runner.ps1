# Setup Self-Hosted GitHub Actions Runner on Windows
# Run this as Administrator in PowerShell

Write-Host "🏃 Setting up GitHub Actions Self-Hosted Runner" -ForegroundColor Green
Write-Host ""

# Configuration
$REPO = "kishoredevops55/eq-assessment"  # Change to your repo
$RUNNER_NAME = "local-windows-runner"
$RUNNER_WORK_DIR = "C:\actions-runner"

Write-Host "📋 Prerequisites Check" -ForegroundColor Yellow
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ Please run this script as Administrator" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Running as Administrator"

# Create runner directory
Write-Host ""
Write-Host "📁 Creating runner directory..." -ForegroundColor Yellow
if (-not (Test-Path $RUNNER_WORK_DIR)) {
    New-Item -ItemType Directory -Path $RUNNER_WORK_DIR | Out-Null
}
Set-Location $RUNNER_WORK_DIR
Write-Host "✅ Directory: $RUNNER_WORK_DIR"

# Download runner
Write-Host ""
Write-Host "⬇️  Downloading GitHub Actions Runner..." -ForegroundColor Yellow

$RUNNER_VERSION = "2.311.0"  # Update to latest version
$RUNNER_URL = "https://github.com/actions/runner/releases/download/v$RUNNER_VERSION/actions-runner-win-x64-$RUNNER_VERSION.zip"

if (-not (Test-Path "actions-runner-win-x64-$RUNNER_VERSION.zip")) {
    Invoke-WebRequest -Uri $RUNNER_URL -OutFile "actions-runner-win-x64-$RUNNER_VERSION.zip"
}

# Extract runner
if (-not (Test-Path "bin")) {
    Expand-Archive -Path "actions-runner-win-x64-$RUNNER_VERSION.zip" -DestinationPath . -Force
}
Write-Host "✅ Runner downloaded and extracted"

# Instructions for token
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "📝 NEXT STEPS - GET RUNNER TOKEN" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://github.com/$REPO/settings/actions/runners/new"
Write-Host ""
Write-Host "2. Copy the token from the page (it will look like: ABCD...XYZ)"
Write-Host ""
Write-Host "3. Run the configuration command:" -ForegroundColor Green
Write-Host ""
Write-Host "   .\config.cmd --url https://github.com/$REPO --token YOUR_TOKEN_HERE --name $RUNNER_NAME --work _work" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. When prompted:" -ForegroundColor Yellow
Write-Host "   - Runner name: $RUNNER_NAME"
Write-Host "   - Runner labels: [Press Enter for defaults]"
Write-Host "   - Runner work folder: [Press Enter for _work]"
Write-Host ""
Write-Host "5. Run the runner:" -ForegroundColor Green
Write-Host ""
Write-Host "   .\run.cmd" -ForegroundColor Cyan
Write-Host ""
Write-Host "   OR install as Windows Service:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   .\svc.sh install" -ForegroundColor Cyan
Write-Host "   .\svc.sh start" -ForegroundColor Cyan
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Open browser to runner setup page
Write-Host "Opening browser to get token..."
Start-Process "https://github.com/$REPO/settings/actions/runners/new"

Write-Host ""
Write-Host "📍 Current directory: $PWD"
Write-Host ""
Write-Host "Ready to configure? Run the config command above with your token!" -ForegroundColor Green
