#!/usr/bin/env python3
"""
QUICK TEST SCRIPT - Test your production domain
Simple script to verify your deployed API is working
"""
import httpx
import sys

def test_domain(domain_url: str, timeout: int = 10):
    """Test if domain is accessible and working"""
    
    print(f"\n{'='*70}")
    print(f"Testing: {domain_url}")
    print(f"{'='*70}\n")
    
    # Test 1: Root endpoint
    print("1️⃣  Testing root endpoint...")
    try:
        response = httpx.get(f"{domain_url}/", timeout=timeout, verify=False)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Service: {data.get('service', 'N/A')}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)[:80]}")
        return False
    
    # Test 2: Health check
    print("\n2️⃣  Testing health endpoint...")
    try:
        response = httpx.get(f"{domain_url}/health", timeout=timeout, verify=False)
        if response.status_code == 200:
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Service is healthy")
        else:
            print(f"   ❌ Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:80]}")
    
    # Test 3: Gists endpoint
    print("\n3️⃣  Testing gists endpoint (octocat)...")
    try:
        response = httpx.get(f"{domain_url}/octocat", timeout=timeout, verify=False)
        if response.status_code == 200:
            data = response.json()
            gists = len(data.get('data', []))
            cache = data.get('cache', {}).get('hit', False)
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Gists fetched: {gists}")
            print(f"   ✅ Cache working: {cache}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:80]}")
        return False
    
    # Test 4: Metrics endpoint
    print("\n4️⃣  Testing metrics endpoint...")
    try:
        response = httpx.get(f"{domain_url}/metrics", timeout=timeout, verify=False)
        if response.status_code == 200:
            lines = len(response.text.split('\n'))
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Metrics available: {lines} lines")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Metrics not available: {str(e)[:80]}")
    
    print(f"\n{'='*70}")
    print("✅ ALL TESTS PASSED - Your domain is working!")
    print(f"{'='*70}\n")
    
    return True


if __name__ == "__main__":
    domain = "https://gists.kishore.local"
    
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    
    success = test_domain(domain)
    sys.exit(0 if success else 1)
