# Setup GitHub Token for API Rate Limit (5000 req/hour instead of 60)
# 
# Usage:
#   1. Create a GitHub Personal Access Token:
#      - Go to: https://github.com/settings/tokens
#      - Generate new token (classic)
#      - No scopes needed for public gists (or select 'gist' for private)
#
#   2. Run this script:
#      .\scripts\setup-github-token.ps1 -Token "your_token_here"
#
#   3. Restart deployment:
#      kubectl rollout restart deployment/github-gists-api -n production

param(
    [Parameter(Mandatory=$true)]
    [string]$Token,
    [string]$Namespace = "production"
)

Write-Host "Setting up GitHub Token..." -ForegroundColor Cyan

# Delete existing secret if exists
kubectl delete secret github-token -n $Namespace --ignore-not-found 2>$null

# Create new secret
kubectl create secret generic github-token `
    --from-literal=GITHUB_TOKEN=$Token `
    -n $Namespace

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Secret 'github-token' created in namespace '$Namespace'" -ForegroundColor Green
    
    # Restart deployment to pick up new secret
    Write-Host "Restarting deployment..." -ForegroundColor Yellow
    kubectl rollout restart deployment/github-gists-api -n $Namespace
    kubectl rollout status deployment/github-gists-api -n $Namespace --timeout=2m
    
    Write-Host ""
    Write-Host "[OK] GitHub token configured! You now have 5000 requests/hour" -ForegroundColor Green
    Write-Host ""
    Write-Host "Verify with:" -ForegroundColor Yellow
    Write-Host "  kubectl logs -n $Namespace -l app=github-gists-api --tail=5"
    Write-Host "  # Should show: 'GitHub token configured - 5000 requests/hour'"
} else {
    Write-Host "[ERROR] Failed to create secret" -ForegroundColor Red
    exit 1
}
