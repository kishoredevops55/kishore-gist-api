# Load Test Script for GitHub Gists API via Istio Gateway
# Tests load balancing across 3 replicas with Istio mTLS

param(
    [int]$Requests = 100,
    [int]$Concurrent = 10,
    [string]$Host = "gists.kishore.local",
    [string]$Endpoint = "/octocat"
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Load Test: GitHub Gists API via Istio" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Total Requests: $Requests"
Write-Host "  Concurrent: $Concurrent"
Write-Host "  Host: $Host"
Write-Host "  Endpoint: $Endpoint"
Write-Host ""

# Check pods
Write-Host "Checking pod distribution..." -ForegroundColor Yellow
kubectl get pods -n production -o wide | Select-Object -First 5
Write-Host ""

# Simple load test using PowerShell jobs
Write-Host "Starting load test..." -ForegroundColor Green
Write-Host ""

$results = @{
    Success = 0
    Failed = 0
    TotalTime = 0
    Times = @()
}

$url = "https://${Host}${Endpoint}"
$batchSize = [math]::Ceiling($Requests / $Concurrent)

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

for ($batch = 0; $batch -lt $Concurrent; $batch++) {
    $jobs = @()
    
    for ($i = 0; $i -lt $batchSize -and (($batch * $batchSize) + $i) -lt $Requests; $i++) {
        $jobs += Start-Job -ScriptBlock {
            param($url)
            $sw = [System.Diagnostics.Stopwatch]::StartNew()
            try {
                $response = curl.exe -sk -w "%{http_code}" -o NUL $url 2>$null
                $sw.Stop()
                return @{ Success = ($response -eq "200"); Time = $sw.ElapsedMilliseconds }
            } catch {
                $sw.Stop()
                return @{ Success = $false; Time = $sw.ElapsedMilliseconds }
            }
        } -ArgumentList $url
    }
    
    # Wait for batch
    $jobs | Wait-Job | Out-Null
    
    foreach ($job in $jobs) {
        $result = Receive-Job $job
        if ($result.Success) {
            $results.Success++
        } else {
            $results.Failed++
        }
        $results.Times += $result.Time
        Remove-Job $job
    }
    
    # Progress
    $progress = [math]::Min(100, [math]::Round((($batch + 1) * $batchSize / $Requests) * 100))
    Write-Host "`rProgress: $progress% ($($results.Success + $results.Failed)/$Requests requests)" -NoNewline
}

$stopwatch.Stop()
Write-Host ""
Write-Host ""

# Calculate statistics
$avgTime = if ($results.Times.Count -gt 0) { ($results.Times | Measure-Object -Average).Average } else { 0 }
$minTime = if ($results.Times.Count -gt 0) { ($results.Times | Measure-Object -Minimum).Minimum } else { 0 }
$maxTime = if ($results.Times.Count -gt 0) { ($results.Times | Measure-Object -Maximum).Maximum } else { 0 }
$p95 = if ($results.Times.Count -gt 0) { ($results.Times | Sort-Object)[[math]::Floor($results.Times.Count * 0.95)] } else { 0 }
$rps = if ($stopwatch.Elapsed.TotalSeconds -gt 0) { [math]::Round($Requests / $stopwatch.Elapsed.TotalSeconds, 2) } else { 0 }

Write-Host "============================================" -ForegroundColor Green
Write-Host "Load Test Results" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Requests:" -ForegroundColor Yellow
Write-Host "  Total:      $Requests"
Write-Host "  Successful: $($results.Success)" -ForegroundColor Green
Write-Host "  Failed:     $($results.Failed)" -ForegroundColor $(if ($results.Failed -gt 0) { "Red" } else { "Green" })
Write-Host "  Success %:  $([math]::Round(($results.Success / $Requests) * 100, 2))%"
Write-Host ""
Write-Host "Timing:" -ForegroundColor Yellow
Write-Host "  Total Time: $([math]::Round($stopwatch.Elapsed.TotalSeconds, 2))s"
Write-Host "  Avg:        $([math]::Round($avgTime, 2))ms"
Write-Host "  Min:        $([math]::Round($minTime, 2))ms"
Write-Host "  Max:        $([math]::Round($maxTime, 2))ms"
Write-Host "  P95:        $([math]::Round($p95, 2))ms"
Write-Host ""
Write-Host "Throughput:" -ForegroundColor Yellow
Write-Host "  RPS:        $rps requests/second"
Write-Host ""

# Check load distribution across pods
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Load Distribution Across Pods" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Recent logs from each pod:" -ForegroundColor Yellow

$pods = kubectl get pods -n production -o jsonpath="{.items[*].metadata.name}" 2>$null
$podArray = $pods -split " "

foreach ($pod in $podArray) {
    if ($pod) {
        $logCount = (kubectl logs $pod -n production --tail=50 2>$null | Select-String "GET /octocat" | Measure-Object).Count
        Write-Host "  $pod : ~$logCount requests" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "Load balancing is working if requests are distributed across pods!" -ForegroundColor Green
Write-Host ""
