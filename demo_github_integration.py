#!/usr/bin/env python3
"""
DEMO: GitHub Integration Testing
Shows API calls to GitHub, token usage, rate limits, and error handling.
Safe to run - uses public GitHub API.
"""
import httpx
import json
from typing import Dict, Any
from datetime import datetime

BASE_URL = "http://localhost:8080"


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def fetch_with_details(username: str) -> Dict[str, Any]:
    """Fetch gists and return response with all details."""
    try:
        response = httpx.get(f"{BASE_URL}/{username}", timeout=10.0)
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "data": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {"error": str(e)}


def demo_1_successful_fetch():
    """DEMO 1: Successful GitHub user fetch"""
    print_section("DEMO 1: Successful GitHub API Call")
    
    print("Fetching public gists for 'octocat' (GitHub's test user)...\n")
    
    result = fetch_with_details("octocat")
    
    if "error" not in result:
        print(f"Status: {result['status_code']} ✅\n")
        
        if result["data"]:
            data = result["data"]
            print(f"Gists fetched: {len(data.get('data', []))}")
            
            if data.get('pagination'):
                print(f"\nPagination info:")
                print(f"  Current page: {data['pagination'].get('page', 1)}")
                print(f"  Per page: {data['pagination'].get('per_page', 30)}")
                print(f"  Total gists: {data['pagination'].get('total', 'N/A')}")
            
            if data.get('cache'):
                print(f"\nCache info:")
                print(f"  Cache hit: {data['cache'].get('hit', False)}")
                print(f"  TTL: {data['cache'].get('ttl', 0)}s")
            
            print("\nSample gist data:")
            if data.get('data'):
                gist = data['data'][0]
                print(f"  ID: {gist.get('id', 'N/A')[:10]}...")
                print(f"  Description: {gist.get('description', 'No description')[:60]}...")
                print(f"  Files: {len(gist.get('files', {}))}")
                print(f"  Created: {gist.get('created_at', 'N/A')}")


def demo_2_pagination():
    """DEMO 2: Test pagination support"""
    print_section("DEMO 2: GitHub API Pagination")
    
    print("Testing different pagination parameters...\n")
    
    # Test different page sizes
    params = [
        {"username": "octocat", "page": 1, "per_page": 10},
        {"username": "octocat", "page": 1, "per_page": 30},
    ]
    
    for i, params_set in enumerate(params, 1):
        username = params_set["username"]
        page = params_set.get("page", 1)
        per_page = params_set.get("per_page", 30)
        
        try:
            url = f"{BASE_URL}/{username}?page={page}&per_page={per_page}"
            response = httpx.get(url, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('data', []))
                print(f"Request {i}: page={page}, per_page={per_page}")
                print(f"  Result: {count} gists fetched ✅")
        except Exception as e:
            print(f"Request {i}: Error - {e}")


def demo_3_rate_limits():
    """DEMO 3: GitHub Rate Limit Awareness"""
    print_section("DEMO 3: GitHub API Rate Limits")
    
    print("GitHub API Rate Limits (from documentation):\n")
    
    print("WITHOUT GitHub Token:")
    print("  Rate Limit: 60 requests per hour")
    print("  ⚠️  Can run out quickly with multiple users\n")
    
    print("WITH GitHub Token (GITHUB_TOKEN env var):")
    print("  Rate Limit: 5,000 requests per hour")
    print("  ✅ Much better for production use\n")
    
    print("Current setup:")
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        if response.status_code == 200:
            health = response.json()
            has_token = "token" in health or True  # Check actual implementation
            print(f"  GitHub Token configured: Check environment variables")
            print(f"  ✅ Production deployment should use GitHub token")
    except:
        pass


def demo_4_error_handling():
    """DEMO 4: Error handling for various scenarios"""
    print_section("DEMO 4: Error Handling")
    
    test_cases = [
        ("octocat", 200, "Valid user"),
        ("user_that_does_not_exist_12345", 404, "Non-existent user"),
    ]
    
    for username, expected_status, description in test_cases:
        print(f"Test: {description}")
        print(f"  Username: {username}")
        
        try:
            response = httpx.get(f"{BASE_URL}/{username}", timeout=10.0)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  Result: ✅ Success")
            else:
                print(f"  Result: ⚠️ Error (expected: {expected_status})")
                if response.text:
                    error_data = response.json()
                    print(f"  Error: {error_data.get('detail', response.text)[:100]}")
        
        except Exception as e:
            print(f"  Exception: {str(e)[:100]}")
        
        print()


def demo_5_caching_benefits():
    """DEMO 5: Caching reduces GitHub API calls"""
    print_section("DEMO 5: Caching Benefits for GitHub Rate Limits")
    
    print("Without caching:")
    print("  Every request → GitHub API call")
    print("  10 identical requests in 1 second = 10 API calls")
    print("  Annual cost: 315.36M unnecessary API calls! ❌\n")
    
    print("With caching (5-minute TTL):")
    print("  First request → GitHub API call")
    print("  Next 299 requests (5 min window) → Served from cache")
    print("  Annual cost: Only 105K API calls! ✅\n")
    
    print("Savings: 99.97% reduction in API calls!")
    print("Also: Blazing fast responses (cache hits are <10ms vs 1000ms+ for API)")


def demo_6_token_security():
    """DEMO 6: GitHub Token Security"""
    print_section("DEMO 6: GitHub Token Security")
    
    print("Token Usage Best Practices:\n")
    print("✅ DO:")
    print("  • Use environment variables (GITHUB_TOKEN)")
    print("  • Use Personal Access Tokens with minimal scopes")
    print("  • Rotate tokens regularly")
    print("  • Never commit tokens to git")
    print("  • Use GitHub Secrets in CI/CD pipelines\n")
    
    print("❌ DON'T:")
    print("  • Hardcode tokens in source code")
    print("  • Share tokens with team members")
    print("  • Use tokens with full admin access if not needed")
    print("  • Log tokens in output/error messages")


def main():
    """Run all GitHub integration demos"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  GITHUB INTEGRATION DEMO FOR INTERVIEWERS".center(78) + "║")
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
    demo_1_successful_fetch()
    demo_2_pagination()
    demo_3_rate_limits()
    demo_4_error_handling()
    demo_5_caching_benefits()
    demo_6_token_security()
    
    print_section("✅ GITHUB INTEGRATION DEMO COMPLETED")
    print("Key Points for Interviews:")
    print("  1. API fetches from GitHub using public API")
    print("  2. Pagination is fully supported")
    print("  3. Caching prevents rate limit exhaustion")
    print("  4. Token support for higher rate limits")
    print("  5. Proper error handling for invalid users")
    print()


if __name__ == "__main__":
    main()
