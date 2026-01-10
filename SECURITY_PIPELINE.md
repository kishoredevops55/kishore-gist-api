# 🔒 Complete Security & Deployment Pipeline

## ✅ What's Now Integrated

### 1. **Code Quality Scanning - SonarCloud** (Like Veracode)
- ✅ Static code analysis
- ✅ Security vulnerability detection
- ✅ Code coverage tracking
- ✅ Technical debt measurement
- ✅ **Free for open source projects**

### 2. **Container Security Scanning** (Like Twistlock/Prisma Cloud)
- ✅ **Trivy** - Comprehensive vulnerability scanner
- ✅ **Snyk** - Dependency and container scanning
- ✅ **Docker Scout** - DockerHub native scanner
- ✅ SBOM (Software Bill of Materials) generation
- ✅ GitHub Security tab integration

### 3. **DockerHub Integration**
- ✅ Automated push after security scans pass
- ✅ Multi-platform builds (amd64 + arm64)
- ✅ Tagged releases (sha, branch, latest)
- ✅ Private registry support with pull secrets

### 4. **Kubernetes Deployment**
- ✅ Pull OCI images from DockerHub
- ✅ ImagePullSecrets for private repos
- ✅ Rolling updates with zero downtime
- ✅ Health checks and readiness probes

### 5. **Prometheus Monitoring Enabled**
- ✅ `/metrics` endpoint added to API
- ✅ Request count, latency, active requests
- ✅ GitHub API call tracking
- ✅ ServiceMonitor for Prometheus Operator

---

## 🚀 Setup Guide (5 Minutes)

### Step 1: **Create Accounts** (All FREE!)

#### A. **SonarCloud** (Code Scanning)
1. Go to https://sonarcloud.io/
2. Sign in with GitHub
3. Import your repository: `kishoredevops55/eq-assessment`
4. Copy the token: https://sonarcloud.io/account/security
5. Add to GitHub Secrets: `SONAR_TOKEN`

#### B. **Snyk** (Container Scanning)
1. Go to https://app.snyk.io/signup
2. Sign up (free tier)
3. Get API token: https://app.snyk.io/account
4. Add to GitHub Secrets: `SNYK_TOKEN`

#### C. **DockerHub**
1. Go to https://hub.docker.com/
2. Sign up (free)
3. Create Access Token: Account Settings → Security → New Access Token
4. Add to GitHub Secrets:
   - `DOCKERHUB_USERNAME` = your username
   - `DOCKERHUB_TOKEN` = access token

---

### Step 2: **Add GitHub Secrets**

Go to: `https://github.com/kishoredevops55/eq-assessment/settings/secrets/actions`

Add these secrets:

```bash
# Code scanning
SONAR_TOKEN = "sqp_xxxxxxxxxxxxxxxxxxxxx"

# Container scanning
SNYK_TOKEN = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# DockerHub
DOCKERHUB_USERNAME = "your-dockerhub-username"
DOCKERHUB_TOKEN = "dckr_pat_xxxxxxxxxxxxx"

# Kubernetes (base64 encoded kubeconfig)
KUBECONFIG = "base64-encoded-kubeconfig-content"
```

**To encode kubeconfig**:
```powershell
# Windows PowerShell
$content = Get-Content ~/.kube/config -Raw
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))
```

---

### Step 3: **Update Kubernetes Deployment**

Edit `k8s/deployment.yaml` and replace:
```yaml
image: YOUR_DOCKERHUB_USERNAME/github-gists-api:latest
```

With your actual DockerHub username:
```yaml
image: kishoredevops55/github-gists-api:latest
```

---

### Step 4: **Push Changes**

```bash
cd d:\Kishore\eq-assessment

# Install new dependency
pip install prometheus-client==0.20.0

# Update requirements
pip freeze > requirements.txt

# Commit and push
git add .
git commit -m "feat: Add SonarCloud, Snyk, DockerHub, Prometheus monitoring"
git push origin main
```

---

## 📊 CI/CD Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CODE PUSH TO GITHUB                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. CI PIPELINE (.github/workflows/ci.yml)                       │
│                                                                  │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Lint & Test     │  │ Security     │  │ SonarCloud       │  │
│  │ - Flake8        │  │ - Bandit     │  │ - Code quality   │  │
│  │ - MyPy          │  │ - TruffleHog │  │ - Vulnerabilities│  │
│  │ - Pytest        │  │              │  │ - Coverage       │  │
│  └─────────────────┘  └──────────────┘  └──────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 3. BUILD DOCKER IMAGE                                    │  │
│  │    docker build -t github-gists-api:sha .                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 4. SECURITY SCANS (Before Push!)                         │  │
│  │    ✓ Trivy    - CVE scanning                             │  │
│  │    ✓ Snyk     - Dependency vulnerabilities               │  │
│  │    ✓ SBOM     - Software bill of materials               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ❌ If vulnerabilities found → FAIL (don't push)                │
│  ✅ If clean → Continue                                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 5. PUSH TO DOCKERHUB                                     │  │
│  │    docker push dockerhub.io/user/github-gists-api:sha    │  │
│  │    Tags: sha, branch, latest                             │  │
│  │    Platforms: linux/amd64, linux/arm64                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 6. DOCKER SCOUT SCAN (Post-push)                         │  │
│  │    Native DockerHub vulnerability scanning               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. CD PIPELINE (.github/workflows/cd.yml)                       │
│    (Triggers only if CI passes)                                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Create DockerHub Pull Secret in Kubernetes            │  │
│  │    kubectl create secret docker-registry dockerhub-secret│  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 2. Pull OCI Image from DockerHub                         │  │
│  │    Kubernetes pulls: dockerhub.io/user/github-gists-api  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 3. Deploy to Kubernetes (Rolling Update)                 │  │
│  │    - Zero downtime deployment                            │  │
│  │    - Health checks before switching traffic              │  │
│  │    - Automatic rollback on failure                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 4. Verify Metrics Endpoint                               │  │
│  │    curl http://service:8080/metrics                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. MONITORING (Automatic)                                       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Prometheus scrapes /metrics every 30s                    │  │
│  │  - http_requests_total                                   │  │
│  │  - http_request_duration_seconds                         │  │
│  │  - http_requests_active                                  │  │
│  │  - github_api_requests_total                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Grafana displays dashboards                              │  │
│  │  - Request rate per endpoint                             │  │
│  │  - p50/p95/p99 latencies                                 │  │
│  │  - Error rates                                           │  │
│  │  - Active connections                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Alerts trigger on:                                       │  │
│  │  - Error rate > 5%                                       │  │
│  │  - Latency p95 > 2s                                      │  │
│  │  - Pod crashes                                           │  │
│  │  - High memory usage                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Security Scanners Explained

### **1. SonarCloud** (Code Quality - Like Veracode)

**What it scans**:
- Security vulnerabilities (SQL injection, XSS, etc.)
- Code smells
- Bugs
- Technical debt
- Code coverage

**Example output**:
```
✅ Quality Gate: PASSED
📊 Coverage: 87%
🐛 Bugs: 0
🔒 Vulnerabilities: 0
💡 Code Smells: 3
```

**View results**: https://sonarcloud.io/dashboard?id=kishoredevops55_eq-assessment

---

### **2. Trivy** (Container Vulnerability Scanner)

**What it scans**:
- OS packages (apt, yum, apk)
- Application dependencies (pip, npm, etc.)
- CVE database (critical, high, medium, low)
- Misconfigurations

**Example output**:
```
Total: 15 (CRITICAL: 2, HIGH: 5, MEDIUM: 8, LOW: 0)

┌───────────────┬──────────────────┬──────────┬───────────────────┐
│   Library     │  Vulnerability   │ Severity │  Installed Version│
├───────────────┼──────────────────┼──────────┼───────────────────┤
│ urllib3       │ CVE-2023-45803   │ CRITICAL │ 1.26.5            │
│ requests      │ CVE-2023-32681   │ HIGH     │ 2.28.0            │
└───────────────┴──────────────────┴──────────┴───────────────────┘
```

---

### **3. Snyk** (Dependency & Container Scanner)

**What it scans**:
- Python dependencies
- Container base images
- Kubernetes manifests
- Infrastructure as Code (IaC)

**Example output**:
```
✓ Tested 45 dependencies for known issues
✗ Found 3 issues, 2 fixable

High severity vulnerability found in httpx
  Introduced through: httpx@0.23.0
  Fixed in: httpx@0.24.1
  Upgrade recommended
```

---

### **4. Docker Scout** (DockerHub Native)

**What it scans**:
- After image is pushed to DockerHub
- CVEs in layers
- Base image vulnerabilities
- Supply chain security

---

## 📈 Prometheus Metrics Available

After deployment, your API exposes these metrics at `http://your-api/metrics`:

```prometheus
# Request count by endpoint
http_requests_total{method="GET",endpoint="/octocat",status="200"} 1234

# Request latency histogram
http_request_duration_seconds_bucket{method="GET",endpoint="/octocat",le="0.1"} 987
http_request_duration_seconds_bucket{method="GET",endpoint="/octocat",le="0.5"} 1150

# Currently active requests
http_requests_active 3

# GitHub API calls
github_api_requests_total{status="200"} 856
github_api_requests_total{status="403"} 12  # Rate limits
github_api_requests_total{status="404"} 5   # User not found
```

---

## 🎯 Test Everything Locally

### **1. Test Metrics Endpoint**

```bash
# Rebuild with new code
docker build -t github-gists-api:test .

# Run locally
docker run -d -p 8080:8080 --name test-api github-gists-api:test

# Test metrics
curl http://localhost:8080/metrics
```

**Expected output**:
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/health",status="200"} 5.0

# HELP http_request_duration_seconds HTTP request latency
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{method="GET",endpoint="/health",le="0.005"} 5.0
```

### **2. Test Container Scanning Locally**

```bash
# Install Trivy
# Windows (via Chocolatey)
choco install trivy

# Scan your image
trivy image github-gists-api:test

# Scan with specific severity
trivy image --severity CRITICAL,HIGH github-gists-api:test
```

---

## 🏆 What You've Achieved

| Feature | Tool | Status |
|---------|------|--------|
| **Code Quality Scanning** | SonarCloud | ✅ |
| **Static Security Analysis** | Bandit, TruffleHog | ✅ |
| **Container CVE Scanning** | Trivy | ✅ |
| **Dependency Scanning** | Snyk | ✅ |
| **Post-Push Scanning** | Docker Scout | ✅ |
| **SBOM Generation** | Anchore | ✅ |
| **DockerHub Push** | Multi-platform | ✅ |
| **Kubernetes Pull** | ImagePullSecrets | ✅ |
| **Prometheus Metrics** | `/metrics` endpoint | ✅ |
| **Auto-Discovery** | ServiceMonitor | ✅ |

---

## 🎓 Interview Talking Points

### **Question**: "How do you ensure container security?"

**Your Answer**:
> "I implement **defense in depth** with multiple scanning layers:
> 1. **Pre-build**: Bandit scans Python code for security issues, TruffleHog checks for secrets
> 2. **Pre-push**: Trivy scans the built container for CVEs before pushing to registry
> 3. **Dependency check**: Snyk validates all Python packages against vulnerability database
> 4. **Post-push**: Docker Scout provides ongoing monitoring in DockerHub
> 5. **Runtime**: Kubernetes security contexts prevent privilege escalation
> 
> Images only reach production after passing all scans. I also generate SBOM for supply chain transparency."

### **Question**: "How do you monitor applications in Kubernetes?"

**Your Answer**:
> "I use the **Prometheus + Grafana** stack with:
> 1. **Custom metrics** exposed at `/metrics` endpoint tracking requests, latency, errors
> 2. **ServiceMonitor** CRD for automatic Prometheus discovery
> 3. **GitHub API metrics** to track rate limits and errors
> 4. **Grafana dashboards** showing p50/p95/p99 latencies, error rates, throughput
> 5. **Alerting** on SLO violations (p95 > 2s, error rate > 5%)
> 
> This provides real-time visibility into application health and performance."

---

## 🔗 Useful Links

- **SonarCloud Dashboard**: https://sonarcloud.io/projects
- **DockerHub Repo**: https://hub.docker.com/r/YOUR_USERNAME/github-gists-api
- **GitHub Security**: https://github.com/YOUR_USER/eq-assessment/security
- **Snyk Dashboard**: https://app.snyk.io/org/YOUR_ORG/projects

---

## ✅ Checklist

- [ ] Created SonarCloud account
- [ ] Created Snyk account
- [ ] Created DockerHub account
- [ ] Added all GitHub secrets
- [ ] Updated `k8s/deployment.yaml` with your DockerHub username
- [ ] Pushed changes to GitHub
- [ ] Verified CI pipeline passes
- [ ] Checked DockerHub for pushed image
- [ ] Deployed to Kubernetes
- [ ] Verified `/metrics` endpoint works
- [ ] Configured Prometheus scraping
- [ ] Imported Grafana dashboard

**When complete**: You have production-grade security scanning, container registry integration, and comprehensive monitoring! 🚀
