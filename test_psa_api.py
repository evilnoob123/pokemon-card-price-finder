#!/usr/bin/env python3
"""
Test script to verify PSA API connectivity and response format.
"""

import requests
import json

def test_psa_api():
    """Test the PSA API with the provided certificate number and token."""
    
    # Test certificate number
    cert_number = "27790785"
    
    # PSA API Token (provided by user)
    psa_token = "F8eGWk5nCAKONQ4hKNvK6I6QXuBWQH4IQHWS0cOxsU0dGrgO7HlE2MxEQu8INI3BZJscCAVB3ukrTU1EUOZGSdntk8zae9sQHEsF0OsqYs11fZC1tUzyibskcPETsgyIgo4MoEa8qYe40qPeepyZqvNCT6f2VM1EKvo-DZOVr946iIM0BF693CsiNsm8O86ANJlUXBeN453b1LTTe-7h43oO5C8SbNAxBGm2dWQr4YYXrK9J9vUIyZIQ6Wm3pRVmNk2T8r9O7XWZru6AUlo6qlRf9lv6u9knt27PPzfV8X2GHckp"
    
    # PSA API URL
    psa_url = f"https://api.psacard.com/publicapi/cert/GetByCertNumber/{cert_number}"
    
    # Headers
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {psa_token}"
    }
    
    print(f"Testing PSA API...")
    print(f"URL: {psa_url}")
    print(f"Headers: {headers}")
    print("-" * 50)
    
    try:
        # Make the request
        response = requests.get(psa_url, headers=headers, timeout=10)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response JSON: {json.dumps(data, indent=2)}")
            except json.JSONDecodeError:
                print("Response is not valid JSON")
        
        return response.status_code == 200
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_psa_api()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
