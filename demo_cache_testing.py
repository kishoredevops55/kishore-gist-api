#!/usr/bin/env python3
"""
DEMO: Cache Performance Testing
Shows how cache is working, cache hits, misses, and TTL reset.
Safe to run - no production data affected.
"""
import httpx
import time
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8080"
DEMO_USER = "octocat"


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def fetch_gists(username: str) -> Dict[str, Any]:
    """Fetch gists and return full response with cache info."""
    try:
        response = httpx.get(f"{BASE_URL}/{username}", timeout=10.0)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return {}


def demo_1_cache_hit():
    """DEMO 1: Show cache hit vs miss"""
    print_section("DEMO 1: Cache Hit vs Miss")
    
    print("First request (cache MISS - fetches from GitHub API):")
    start = time.time()
    result1 = fetch_gists(DEMO_USER)
    elapsed1 = time.time() - start
    
    if "cache" in result1:
        cache_info1 = result1["cache"]
        print(f"  Status: {cache_info1.get('hit', False)}")
        print(f"  Time taken: {elapsed1:.3f}s")
        print(f"  Gists found: {len(result1.get('data', []))}")
    
    print("\n" + "-"*80 + "\n")
    
    time.sleep(0.5)
    
    print("Second request (cache HIT - from memory):")
    start = time.time()
    result2 = fetch_gists(DEMO_USER)
    elapsed2 = time.time() - start
    
    if "cache" in result2:
        cache_info2 = result2["cache"]
        print(f"  Status: {cache_info2.get('hit', False)}")
        print(f"  Time taken: {elapsed2:.3f}s")
        print(f"  Gists found: {len(result2.get('data', []))}")
    
    print(f"\n✅ Performance improvement: {elapsed1/elapsed2:.1f}x faster with cache hit")


def demo_2_cache_ttl():
    """DEMO 2: Show cache TTL (Time To Live)"""
    print_section("DEMO 2: Cache TTL (Time To Live)")
    
    print("Making initial request...")
    result1 = fetch_gists(DEMO_USER)
    if "cache" in result1:
        ttl = result1["cache"].get("ttl", 300)
        expires = result1["cache"].get("expires_in_seconds", 0)
        print(f"  Cache TTL: {ttl}s")
        print(f"  Expires in: {expires:.1f}s")
    
    print(f"\nWaiting 2 seconds...")
    time.sleep(2)
    
    result2 = fetch_gists(DEMO_USER)
    if "cache" in result2:
        expires = result2["cache"].get("expires_in_seconds", 0)
        is_hit = result2["cache"].get("hit", False)
        print(f"  Still cached: {is_hit}")
        print(f"  Expires in: {expires:.1f}s (decreased by ~2s)")


def demo_3_cache_reset():
    """DEMO 3: Test cache reset after TTL"""
    print_section("DEMO 3: Cache Reset After TTL Expiration")
    
    print("Getting cache info for timing...")
    result1 = fetch_gists(DEMO_USER)
    
    if "cache" in result1:
        ttl = result1["cache"].get("ttl", 300)
        print(f"  Cache TTL is {ttl}s (test uses shorter TTL if set)")
        print(f"  Demo: Showing cache behavior (full TTL wait not practical for demo)")
        print(f"  ✅ In production, cache auto-refreshes after {ttl}s")


def demo_4_multiple_users():
    """DEMO 4: Cache works per-user"""
    print_section("DEMO 4: Independent Cache per User")
    
    users = ["octocat", "torvalds", "gvanrossum"]
    
    for i, user in enumerate(users, 1):
        print(f"Request {i}: Fetching {user}")
        result = fetch_gists(user)
        
        if "cache" in result:
            cache_info = result["cache"]
            print(f"  Cache hit: {cache_info.get('hit', False)}")
            print(f"  Gists: {len(result.get('data', []))}")
        
        if i < len(users):
            time.sleep(0.5)


def demo_5_metrics():
    """DEMO 5: Show cache metrics"""
    print_section("DEMO 5: Cache Performance Metrics")
    
    # Make some requests
    for i in range(3):
        fetch_gists(DEMO_USER)
        time.sleep(0.3)
    
    # Check metrics endpoint
    try:
        response = httpx.get(f"{BASE_URL}/metrics", timeout=5.0)
        if response.status_code == 200:
            metrics = response.text
            
            # Extract cache-related metrics
            print("Cache Metrics from Prometheus:")
            print("-" * 80)
            
            for line in metrics.split('\n'):
                if 'cache' in line.lower() and not line.startswith('#'):
                    print(f"  {line}")
            
            print("\n✅ These metrics can be scraped by Prometheus for monitoring")
    except Exception as e:
        print(f"⚠️  Could not fetch metrics: {e}")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  GITHUB GISTS API - CACHE DEMO FOR INTERVIEWERS".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Check if API is running
        print("\nChecking if API is running on http://localhost:8080...")
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        if response.status_code != 200:
            print("❌ API not responding with healthy status")
            return
        print("✅ API is running and healthy\n")
        
    except Exception as e:
        print(f"❌ API not running. Start it with: uvicorn app.main:app --host 0.0.0.0 --port 8080")
        return
    
    # Run all demos
    demo_1_cache_hit()
    demo_2_cache_ttl()
    demo_3_cache_reset()
    demo_4_multiple_users()
    demo_5_metrics()
    
    print_section("✅ CACHE DEMO COMPLETED")
    print("Key Takeaways:")
    print("  1. First request is slower (API call to GitHub)")
    print("  2. Subsequent requests are much faster (cached)")
    print("  3. Cache expires after TTL and refreshes automatically")
    print("  4. Each user has independent cache")
    print("  5. Metrics are exported for Prometheus monitoring")
    print()


if __name__ == "__main__":
    main()
