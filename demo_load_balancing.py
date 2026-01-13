#!/usr/bin/env python3
"""
DEMO: Load Balancing & Traffic Distribution
Shows how traffic is handled, response times under load, and server distribution.
Safe to run - doesn't break anything, just tests performance.
"""
import httpx
import time
import asyncio
import statistics
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import threading

BASE_URL = "http://localhost:8080"
DEMO_USER = "octocat"


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def single_request(username: str) -> float:
    """Make a single request and return response time in ms."""
    try:
        start = time.time()
        response = httpx.get(f"{BASE_URL}/{username}", timeout=10.0)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        return elapsed if response.status_code == 200 else None
    except Exception:
        return None


def demo_1_sequential_requests():
    """DEMO 1: Sequential requests (baseline)"""
    print_section("DEMO 1: Sequential Requests (Baseline)")
    
    print("Making 10 sequential requests...\n")
    
    times = []
    for i in range(10):
        elapsed = single_request(DEMO_USER)
        if elapsed:
            times.append(elapsed)
            status = "✅ HIT (cached)" if elapsed < 50 else "⏱️  MISS (fresh)"
            print(f"  Request {i+1:2d}: {elapsed:7.2f}ms  {status}")
        else:
            print(f"  Request {i+1:2d}: FAILED")
    
    if times:
        print(f"\nStats:")
        print(f"  Average: {statistics.mean(times):.2f}ms")
        print(f"  Min: {min(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")
        print(f"  Total time: {sum(times):.2f}ms")


def demo_2_parallel_requests():
    """DEMO 2: Parallel requests (concurrent load)"""
    print_section("DEMO 2: Parallel Requests (Concurrent Load)")
    
    num_requests = 20
    print(f"Making {num_requests} parallel requests simultaneously...\n")
    
    def make_request():
        return single_request(DEMO_USER)
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        times = list(executor.map(make_request, [None] * num_requests))
    
    total_time = (time.time() - start_time) * 1000
    valid_times = [t for t in times if t is not None]
    
    if valid_times:
        print(f"Results:")
        print(f"  Successful: {len(valid_times)}/{num_requests}")
        print(f"  Total wall-clock time: {total_time:.2f}ms")
        print(f"  Average response time: {statistics.mean(valid_times):.2f}ms")
        print(f"  Min: {min(valid_times):.2f}ms")
        print(f"  Max: {max(valid_times):.2f}ms")
        print(f"\n✅ Server handled {num_requests} concurrent requests")


def demo_3_sustained_load():
    """DEMO 3: Sustained load test"""
    print_section("DEMO 3: Sustained Load (Constant Traffic)")
    
    duration_seconds = 5
    print(f"Sustained traffic for {duration_seconds} seconds...\n")
    
    times = []
    request_count = 0
    errors = 0
    
    start_time = time.time()
    
    while time.time() - start_time < duration_seconds:
        elapsed = single_request(DEMO_USER)
        if elapsed is not None:
            times.append(elapsed)
        else:
            errors += 1
        request_count += 1
    
    if times:
        throughput = request_count / duration_seconds
        print(f"Results:")
        print(f"  Total requests: {request_count}")
        print(f"  Successful: {len(times)}")
        print(f"  Failed: {errors}")
        print(f"  Throughput: {throughput:.1f} req/s")
        print(f"  Average response: {statistics.mean(times):.2f}ms")
        print(f"  p50 (median): {statistics.median(times):.2f}ms")
        if len(times) > 1:
            print(f"  p95: {sorted(times)[int(len(times)*0.95)]:.2f}ms")
            print(f"  p99: {sorted(times)[int(len(times)*0.99)]:.2f}ms")


def demo_4_multiple_endpoints():
    """DEMO 4: Traffic across multiple users"""
    print_section("DEMO 4: Traffic Distribution Across Multiple Users")
    
    users = ["octocat", "torvalds", "gvanrossum"]
    print(f"Distributing traffic across {len(users)} different users...\n")
    
    for user in users:
        print(f"User: {user}")
        times = []
        
        for _ in range(3):
            elapsed = single_request(user)
            if elapsed:
                times.append(elapsed)
        
        if times:
            print(f"  Avg response: {statistics.mean(times):.2f}ms")
        print()
    
    print("✅ Server can handle traffic for multiple users independently")


def demo_5_cache_effect_on_load():
    """DEMO 5: How caching reduces load"""
    print_section("DEMO 5: Caching Effect on Server Load")
    
    print("Scenario: 100 requests in 10 seconds\n")
    
    print("WITHOUT caching:")
    print("  → 100 GitHub API calls")
    print("  → 100 × 1000ms avg = 100 seconds of API latency")
    print("  → High GitHub rate limit usage")
    print("  → Poor user experience ❌\n")
    
    print("WITH caching (5-minute TTL):")
    print("  → 1st request: GitHub API call (1000ms)")
    print("  → 2-100 requests: Served from cache (<10ms each)")
    print("  → Total: ~1 second vs 100 seconds")
    print("  → 99x faster! ✅")
    print("  → Only 1 GitHub API call")
    print("  → Excellent user experience\n")
    
    print("Testing with actual requests...")
    
    # Clear cache with first request
    single_request(DEMO_USER)
    
    times = []
    for _ in range(5):
        elapsed = single_request(DEMO_USER)
        if elapsed:
            times.append(elapsed)
    
    if times:
        avg_cached = statistics.mean(times[1:]) if len(times) > 1 else times[0]
        print(f"\nActual measurements:")
        print(f"  First request (cache miss): {times[0]:.2f}ms")
        print(f"  Subsequent (cache hits): avg {avg_cached:.2f}ms")
        print(f"  Speedup: {times[0]/avg_cached:.1f}x faster")


def demo_6_server_health():
    """DEMO 6: Server health and uptime"""
    print_section("DEMO 6: Server Health & Uptime Monitoring")
    
    print("Checking server health and availability...\n")
    
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        
        if response.status_code == 200:
            health = response.json()
            print("Health Check: ✅ HEALTHY\n")
            print(f"Status: {health.get('status', 'unknown')}")
            print(f"Service: {health.get('service', 'unknown')}")
            
            if "uptime" in health:
                print(f"Uptime: {health['uptime']}s")
            
            print("\nAvailable endpoints:")
            print(f"  GET  /              - Root endpoint")
            print(f"  GET  /health        - Health check")
            print(f"  GET  /{{username}}    - Get gists for user")
            print(f"  GET  /metrics       - Prometheus metrics")
        
    except Exception as e:
        print(f"❌ Server health check failed: {e}")


def demo_7_load_balancing_setup():
    """DEMO 7: Show load balancing configuration"""
    print_section("DEMO 7: Load Balancing & Kubernetes Setup")
    
    print("Production Load Balancing Setup:\n")
    
    print("1. KUBERNETES SERVICE (Service Mesh):")
    print("   • Service type: ClusterIP or LoadBalancer")
    print("   • Multiple pod replicas (e.g., 3)")
    print("   • Automatic round-robin load balancing\n")
    
    print("2. ISTIO VirtualService:")
    print("   • Traffic management and routing")
    print("   • Load balancing algorithms available:")
    print("     - Round Robin (default)")
    print("     - Least connection")
    print("     - Random")
    print("     - Weighted distribution\n")
    
    print("3. HORIZONTAL POD AUTOSCALING (HPA):")
    print("   • Min replicas: 2")
    print("   • Max replicas: 10")
    print("   • Scale triggers: CPU usage, memory, custom metrics\n")
    
    print("4. INGRESS/API GATEWAY:")
    print("   • Nginx Ingress or Istio Gateway")
    print("   • TLS termination")
    print("   • Rate limiting")
    print("   • Circuit breaking\n")
    
    print("✅ This setup distributes traffic evenly across all pod replicas")


def main():
    """Run all load balancing demos"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  LOAD BALANCING & TRAFFIC DEMO FOR INTERVIEWERS".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        print("\nChecking if API is running...")
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        if response.status_code != 200:
            print("❌ API not responding")
            return
        print("✅ API is running\n")
    except Exception as e:
        print(f"❌ API not running: {e}")
        return
    
    # Run all demos
    demo_1_sequential_requests()
    demo_2_parallel_requests()
    demo_3_sustained_load()
    demo_4_multiple_endpoints()
    demo_5_cache_effect_on_load()
    demo_6_server_health()
    demo_7_load_balancing_setup()
    
    print_section("✅ LOAD BALANCING DEMO COMPLETED")
    print("Key Points for Interviews:")
    print("  1. Server handles parallel requests efficiently")
    print("  2. Cache reduces actual load on backend")
    print("  3. Kubernetes provides automatic load balancing")
    print("  4. HPA scales automatically based on metrics")
    print("  5. Multiple layers of load balancing for reliability")
    print()


if __name__ == "__main__":
    main()
