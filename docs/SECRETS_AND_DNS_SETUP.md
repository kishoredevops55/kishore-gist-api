# 🔐 GitHub Secrets & DNS Setup Guide

## 📋 Required GitHub Repository Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### Add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `GRAFANA_ADMIN_USER` | `admin` | Grafana admin username |
| `GRAFANA_ADMIN_PASSWORD` | `YourSecurePassword123!` | Grafana admin password (use strong password) |
| `GH_API_TOKEN` | `ghp_xxxxxxxxxxxx` | GitHub Personal Access Token for API |

### How to Add Secrets:

1. Go to: `https://github.com/YOUR_USERNAME/eq-assessment/settings/secrets/actions`
2. Click **"New repository secret"**
3. Add each secret:

```
Name:  GRAFANA_ADMIN_USER
Value: admin
```

```
Name:  GRAFANA_ADMIN_PASSWORD
Value: YourSecureGrafanaPassword2024!
```

```
Name:  GH_API_TOKEN
Value: ghp_your_github_token_here
```

---

## 🌐 Windows Hosts File Configuration

### Step 1: Open Hosts File as Administrator

```powershell
# Run PowerShell as Administrator
notepad C:\Windows\System32\drivers\etc\hosts
```

### Step 2: Add DNS Entries

Add these lines at the end of the hosts file:

```
# GitHub Gists API - Local Kubernetes
172.18.255.200    gists.kishore.local
172.18.255.200    gists.local
172.18.255.200    kishoregrafana.local
```

> **Note:** If using port-forward instead of MetalLB, use `127.0.0.1`:
> ```
> 127.0.0.1    gists.kishore.local
> 127.0.0.1    gists.local
> 127.0.0.1    kishoregrafana.local
> ```

### Step 3: Get Actual LoadBalancer IP

```powershell
# Get the actual IP from your cluster
kubectl get svc istio-ingressgateway -n istio-system -o jsonpath="{.status.loadBalancer.ingress[0].ip}"
```

### Step 4: Flush DNS Cache

```powershell
ipconfig /flushdns
```

---

## 🔒 SSL/TLS Certificates

The CD pipeline automatically generates self-signed TLS certificates for:

| Domain | Secret Name | Namespace |
|--------|-------------|-----------|
| `gists.kishore.local` | `gists-tls-secret` | `istio-system` |
| `kishoregrafana.local` | `grafana-tls-secret` | `istio-system` |

### Certificate Details:
- **Validity:** 365 days
- **Key Size:** RSA 2048-bit
- **Extensions:** serverAuth, SAN (Subject Alternative Names)

### Verify Certificates:

```powershell
# Check gists API certificate
kubectl get secret gists-tls-secret -n istio-system

# Check Grafana certificate
kubectl get secret grafana-tls-secret -n istio-system

# View certificate details
kubectl get secret gists-tls-secret -n istio-system -o jsonpath="{.data.tls\.crt}" | 
  [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl get secret gists-tls-secret -n istio-system -o jsonpath="{.data.tls\.crt}"))) |
  openssl x509 -text -noout
```

---

## 🚀 Access URLs After Deployment

| Service | URL | Credentials |
|---------|-----|-------------|
| **Gists API** | https://gists.kishore.local | - |
| **Grafana** | https://kishoregrafana.local | From GitHub secrets |
| **Health Check** | https://gists.kishore.local/health | - |
| **Cache Stats** | https://gists.kishore.local/cache/stats | - |

---

## ✅ Verification Commands

```powershell
# Test Gists API
curl.exe -k https://gists.kishore.local/health

# Test Grafana
curl.exe -k https://kishoregrafana.local

# Check all services
kubectl get svc -n istio-system
kubectl get svc -n monitoring
kubectl get svc -n production

# Check secrets
kubectl get secrets -n istio-system | Select-String "tls"
kubectl get secrets -n monitoring | Select-String "grafana"
```

---

## 🔄 Pipeline Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     CD Pipeline Flow                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Build & Load Image                                          │
│         ↓                                                       │
│  2. Deploy Application (production namespace)                   │
│         ↓                                                       │
│  3. Setup GitHub Token Secret (GH_API_TOKEN)                    │
│         ↓                                                       │
│  4. Configure MetalLB LoadBalancer                              │
│         ↓                                                       │
│  5. Generate API TLS Certificate (gists-tls-secret)             │
│         ↓                                                       │
│  6. Configure Istio Gateway for API                             │
│         ↓                                                       │
│  7. Add Helm Repositories                                       │
│         ↓                                                       │
│  8. Create Monitoring Namespace                                 │
│         ↓                                                       │
│  9. Setup Grafana Credentials (GRAFANA_ADMIN_USER/PASSWORD)     │
│         ↓                                                       │
│  10. Generate Grafana TLS Certificate (grafana-tls-secret)      │
│         ↓                                                       │
│  11. Deploy Tempo (Tracing)                                     │
│         ↓                                                       │
│  12. Deploy Loki (Logs)                                         │
│         ↓                                                       │
│  13. Deploy Prometheus + Grafana                                │
│         ↓                                                       │
│  14. Deploy Synthetic Monitoring                                │
│         ↓                                                       │
│  15. Import Dashboards                                          │
│         ↓                                                       │
│  16. Configure Grafana Istio Gateway                            │
│         ↓                                                       │
│  ✅ COMPLETE - Both API and Monitoring deployed with HTTPS!     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Security Best Practices

1. **Never commit passwords** - Always use GitHub Secrets
2. **Rotate credentials regularly** - Update secrets periodically
3. **Use strong passwords** - Minimum 16 characters, mixed case, numbers, symbols
4. **Limit secret access** - Only grant necessary permissions
5. **Audit secret usage** - Review who accessed secrets

### Recommended Password Format:
```
Example: K!sh0re_Grafana_2024$Secure
- Length: 24+ characters
- Uppercase: K, G, S
- Lowercase: shore, rafana, ecure
- Numbers: 0, 2024
- Symbols: !, _, $
```

---

## 📝 Quick Setup Checklist

- [ ] Add `GRAFANA_ADMIN_USER` secret to GitHub
- [ ] Add `GRAFANA_ADMIN_PASSWORD` secret to GitHub
- [ ] Add `GH_API_TOKEN` secret to GitHub
- [ ] Update Windows hosts file with DNS entries
- [ ] Run CD pipeline (workflow_dispatch)
- [ ] Verify API at https://gists.kishore.local/health
- [ ] Login to Grafana at https://kishoregrafana.local
- [ ] Accept self-signed certificate warning in browser
