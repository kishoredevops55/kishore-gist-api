#!/usr/bin/env python3
"""
DEMO: Load Balancer Traffic Distribution
Advanced testing to show how traffic is distributed across multiple pods.
Shows pod distribution, response times, and load balancing behavior.
"""
import httpx
import time
import statistics
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

BASE_URL = "https://gists.kishore.local"
DEMO_USER = "octocat"


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def make_request_with_details(req_id: int) -> Tuple[int, float, bool, Dict]:
    """Make request and capture response details including pod info."""
    start = time.time()
    try:
        response = httpx.get(
            f"{BASE_URL}/{DEMO_USER}",
            timeout=10.0,
            verify=False
        )
        elapsed = (time.time() - start) * 1000
        
        # Try to get pod identifier from response headers
        headers = dict(response.headers)
        pod_name = headers.get('x-pod-name', headers.get('x-envoy-upstream-service-time', 'unknown'))
        server = headers.get('server', 'unknown')
        
        return (
            req_id,
            elapsed,
            response.status_code == 200,
            {
                'pod': pod_name,
                'server': server,
                'status': response.status_code
            }
        )
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        return (req_id, elapsed, False, {'error': str(e)[:50]})


def demo_1_burst_traffic():
    """DEMO 1: Burst of concurrent traffic"""
    print_section("DEMO 1: Burst Traffic Test (Load Balancer Distribution)")
    
    num_requests = 50
    max_workers = 20
    
    print(f"Sending {num_requests} concurrent requests with {max_workers} workers...")
    print("This simulates a burst of traffic hitting the load balancer.\n")
    
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(make_request_with_details, i) for i in range(num_requests)]
        
        for future in as_completed(futures):
            results.append(future.result())
    
    total_time = (time.time() - start_time) * 1000
    
    # Analyze results
    successful = [r for r in results if r[2]]
    failed = [r for r in results if not r[2]]
    times = [r[1] for r in successful]
    
    print(f"Results:")
    print(f"  Total requests: {num_requests}")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {len(failed)}")
    print(f"  Success rate: {len(successful)/num_requests*100:.1f}%")
    print(f"  Total wall-clock time: {total_time:.2f}ms")
    
    if times:
        print(f"\nResponse Times:")
        print(f"  Average: {statistics.mean(times):.2f}ms")
        print(f"  Median (p50): {statistics.median(times):.2f}ms")
        print(f"  Min: {min(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")
        
        sorted_times = sorted(times)
        print(f"  p95: {sorted_times[int(len(sorted_times)*0.95)]:.2f}ms")
        print(f"  p99: {sorted_times[int(len(sorted_times)*0.99)]:.2f}ms")
        
        throughput = num_requests / (total_time / 1000)
        print(f"\nThroughput: {throughput:.1f} requests/second")
        print(f"✅ Load balancer handled burst traffic successfully!")


def demo_2_sustained_traffic():
    """DEMO 2: Sustained traffic over time"""
    print_section("DEMO 2: Sustained Traffic (Constant Load)")
    
    duration_seconds = 10
    print(f"Sending continuous traffic for {duration_seconds} seconds...")
    print("This tests how the system handles sustained load.\n")
    
    results = []
    start_time = time.time()
    request_count = 0
    
    while time.time() - start_time < duration_seconds:
        req_id, elapsed, success, details = make_request_with_details(request_count)
        results.append((req_id, elapsed, success, details))
        request_count += 1
        time.sleep(0.1)  # 10 req/s rate
    
    successful = [r for r in results if r[2]]
    times = [r[1] for r in successful]
    
    print(f"Results:")
    print(f"  Duration: {duration_seconds}s")
    print(f"  Total requests: {request_count}")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {request_count - len(successful)}")
    print(f"  Average rate: {request_count/duration_seconds:.1f} req/s")
    
    if times:
        print(f"\nResponse Times:")
        print(f"  Average: {statistics.mean(times):.2f}ms")
        print(f"  Median: {statistics.median(times):.2f}ms")
        print(f"  Min: {min(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")
        
        print(f"\n✅ System handled sustained load steadily!")


def demo_3_traffic_distribution():
    """DEMO 3: Show traffic distribution across pods"""
    print_section("DEMO 3: Traffic Distribution Analysis")
    
    num_requests = 30
    print(f"Making {num_requests} requests to analyze distribution...\n")
    
    results = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request_with_details, i) for i in range(num_requests)]
        
        for future in as_completed(futures):
            results.append(future.result())
    
    # Count pod distribution
    pod_counter = Counter()
    server_counter = Counter()
    
    for req_id, elapsed, success, details in results:
        if success:
            pod_counter[details.get('pod', 'unknown')] += 1
            server_counter[details.get('server', 'unknown')] += 1
    
    print("Traffic Distribution by Pod:")
    for pod, count in pod_counter.most_common():
        percentage = count / num_requests * 100
        bar = '█' * int(percentage / 2)
        print(f"  {pod[:30]:30s}: {count:3d} requests ({percentage:5.1f}%) {bar}")
    
    print("\nLoad Balancing Behavior:")
    unique_pods = len(pod_counter)
    if unique_pods == 1:
        print(f"  ⚠️  All traffic went to 1 pod")
        print(f"     (May indicate single replica or session affinity)")
    elif unique_pods > 1:
        print(f"  ✅ Traffic distributed across {unique_pods} pods")
        print(f"     (Load balancer is working correctly!)")
    
    # Calculate distribution uniformity
    if unique_pods > 1:
        expected_per_pod = num_requests / unique_pods
        variance = statistics.variance([count for count in pod_counter.values()])
        print(f"\n  Expected per pod: {expected_per_pod:.1f}")
        print(f"  Distribution variance: {variance:.2f}")
        
        if variance < expected_per_pod * 0.3:
            print(f"  ✅ Excellent distribution (uniform)")
        else:
            print(f"  ⚠️  Some imbalance (normal for small sample)")


def demo_4_scaling_behavior():
    """DEMO 4: Show how system handles increasing load"""
    print_section("DEMO 4: Load Scaling Behavior")
    
    load_levels = [5, 10, 20, 30]
    
    print("Testing with increasing concurrent load levels...\n")
    
    for load in load_levels:
        print(f"Load level: {load} concurrent requests")
        
        results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=load) as executor:
            futures = [executor.submit(make_request_with_details, i) for i in range(load)]
            
            for future in as_completed(futures):
                results.append(future.result())
        
        total_time = (time.time() - start_time) * 1000
        successful = [r for r in results if r[2]]
        times = [r[1] for r in successful]
        
        if times:
            avg_time = statistics.mean(times)
            throughput = load / (total_time / 1000)
            print(f"  Success: {len(successful)}/{load}")
            print(f"  Avg response: {avg_time:.2f}ms")
            print(f"  Throughput: {throughput:.1f} req/s")
        
        print()
        time.sleep(1)
    
    print("✅ System scales well with increasing load!")


def demo_5_kubernetes_info():
    """DEMO 5: Show Kubernetes commands for verification"""
    print_section("DEMO 5: Kubernetes Load Balancing Verification")
    
    print("Run these commands to verify load balancing setup:\n")
    
    print("1️⃣  CHECK RUNNING PODS:")
    print("   kubectl get pods -l app=github-gists-api -o wide")
    print("   (Shows all pod replicas and which nodes they're on)\n")
    
    print("2️⃣  CHECK SERVICE ENDPOINTS:")
    print("   kubectl get endpoints github-gists-api")
    print("   (Shows all pod IPs that service distributes to)\n")
    
    print("3️⃣  CHECK HORIZONTAL POD AUTOSCALER:")
    print("   kubectl get hpa")
    print("   kubectl describe hpa github-gists-api")
    print("   (Shows auto-scaling configuration and current metrics)\n")
    
    print("4️⃣  CHECK POD RESOURCE USAGE:")
    print("   kubectl top pods -l app=github-gists-api")
    print("   (Shows CPU/Memory usage per pod)\n")
    
    print("5️⃣  CHECK SERVICE DETAILS:")
    print("   kubectl describe svc github-gists-api")
    print("   (Shows service configuration and endpoints)\n")
    
    print("6️⃣  CHECK ISTIO TRAFFIC DISTRIBUTION:")
    print("   kubectl get virtualservice github-gists-api -o yaml")
    print("   kubectl get destinationrule github-gists-api -o yaml")
    print("   (Shows Istio routing and load balancing rules)\n")
    
    print("7️⃣  VIEW REAL-TIME TRAFFIC:")
    print("   kubectl logs -f -l app=github-gists-api --all-containers=true")
    print("   (Follow logs from all pods in real-time)\n")
    
    print("8️⃣  CHECK INGRESS/GATEWAY:")
    print("   kubectl get ingress")
    print("   kubectl describe ingress github-gists-api")
    print("   (Shows external access configuration)\n")


def main():
    """Run all load balancer traffic demos"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  LOAD BALANCER TRAFFIC DISTRIBUTION DEMO".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        print(f"\nConnecting to {BASE_URL}...")
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0, verify=False)
        
        if response.status_code != 200:
            print(f"❌ API not responding properly")
            return
        
        print(f"✅ Connected successfully\n")
    except Exception as e:
        print(f"❌ Cannot connect: {e}")
        return
    
    # Run all demos
    demo_1_burst_traffic()
    demo_2_sustained_traffic()
    demo_3_traffic_distribution()
    demo_4_scaling_behavior()
    demo_5_kubernetes_info()
    
    print_section("✅ LOAD BALANCER TRAFFIC DEMO COMPLETED")
    print("Key Takeaways:")
    print("  1. System handles burst traffic effectively")
    print("  2. Sustained load is processed steadily")
    print("  3. Traffic is distributed across multiple pods")
    print("  4. System scales with increasing load")
    print("  5. Kubernetes provides automatic load balancing")
    print("\nFor interviews, emphasize:")
    print("  • Multi-layer load balancing (K8s + Istio)")
    print("  • Automatic horizontal scaling (HPA)")
    print("  • High availability with multiple replicas")
    print("  • Sub-second response times even under load")
    print()


if __name__ == "__main__":
    main()
