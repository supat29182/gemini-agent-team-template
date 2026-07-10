#!/usr/bin/env python3
import os
import sys
import yaml
import argparse
import urllib.request
import urllib.error
import json

def parse_api_contract(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_endpoints(contract, base_url):
    print(f"🔍 Validating API Contract against {base_url} ...")
    paths = contract.get("paths", {})
    all_passed = True
    results = []

    for path, methods in paths.items():
        for method, details in methods.items():
            method_upper = method.upper()
            url = f"{base_url}{path}"
            expected_status = 200 # Default fallback
            
            # Extract expected status from responses
            responses = details.get("responses", {})
            if responses:
                # Find first 2xx or 3xx status code
                success_codes = [code for code in responses.keys() if str(code).startswith('2') or str(code).startswith('3')]
                if success_codes:
                    expected_status = int(success_codes[0])
            
            print(f"Testing {method_upper} {url} (Expected: {expected_status})...", end=" ")
            
            req = urllib.request.Request(url, method=method_upper)
            # Add default headers for JSON
            req.add_header('Accept', 'application/json')
            req.add_header('Content-Type', 'application/json')
            
            # Dummy payload if required (basic simulation)
            if method_upper in ['POST', 'PUT', 'PATCH']:
                req.data = json.dumps({}).encode('utf-8')
                
            try:
                response = urllib.request.urlopen(req, timeout=10)
                status = response.getcode()
            except urllib.error.HTTPError as e:
                status = e.code
            except urllib.error.URLError as e:
                status = 0 # Connection failed
                
            if status == expected_status or (status >= 200 and status < 400 and expected_status >= 200 and expected_status < 400):
                print("✅ PASSED")
                results.append((method_upper, path, "PASSED"))
            else:
                print(f"❌ FAILED (Got {status})")
                results.append((method_upper, path, f"FAILED: Expected {expected_status}, Got {status}"))
                all_passed = False
                
    return all_passed, results

def main():
    parser = argparse.ArgumentParser(description="Deterministic API Validator")
    parser.add_argument("--contract", required=True, help="Path to api_contract.yaml")
    parser.add_argument("--url", required=True, help="Base URL (e.g. http://localhost:3000)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.contract):
        print(f"Error: API Contract not found at {args.contract}")
        sys.exit(1)
        
    try:
        contract = parse_api_contract(args.contract)
    except Exception as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)
        
    all_passed, results = validate_endpoints(contract, args.url)
    
    print("\n--- Summary ---")
    for method, path, res in results:
        print(f"{method} {path}: {res}")
        
    if not all_passed:
        print("\n❌ API Validation Failed. Endpoints do not match the contract.")
        sys.exit(1)
    else:
        print("\n✅ API Validation Passed! All endpoints behave as expected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
