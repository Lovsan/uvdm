"""
Test script for the license client.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.license_client import LicenseClient


def test_license_client():
    """Test the license client functionality."""
    print("=" * 60)
    print("Testing UVDM License Client")
    print("=" * 60)
    
    # Initialize client
    client = LicenseClient(server_url='http://localhost:5000')
    print(f"\nMachine ID: {client.machine_id}")
    
    # Check server status
    print("\n1. Checking server status...")
    if client.check_server_status():
        print("   ✓ Server is online and reachable")
    else:
        print("   ✗ Server is offline or unreachable")
        return
    
    # Test with a valid license key (you need to generate one first)
    print("\n2. Testing license verification...")
    test_license_key = "UVDM-51DC6745-79377B5B-595582A9-CC145BED"
    
    result = client.verify_license(test_license_key)
    if result.get('valid'):
        print(f"   ✓ License is valid")
        print(f"   - License Type: {result.get('license_type')}")
        print(f"   - Expiry Date: {result.get('expiry_date')}")
        print(f"   - Features: {result.get('features')}")
        if result.get('offline'):
            print(f"   - Mode: Offline (cache age: {result.get('cache_age_days')} days)")
        else:
            print(f"   - Mode: Online")
    else:
        print(f"   ✗ License verification failed: {result.get('error')}")
    
    # Test activation
    print("\n3. Testing license activation...")
    result = client.activate_license(test_license_key)
    if result.get('success'):
        print(f"   ✓ {result.get('message')}")
    else:
        print(f"   ✗ Activation failed: {result.get('error')}")
    
    # Test offline mode
    print("\n4. Testing offline mode...")
    result = client.verify_license(test_license_key, offline_mode=True)
    if result.get('valid'):
        print(f"   ✓ Cached license is valid")
        print(f"   - Cache Age: {result.get('cache_age_days', 0)} days")
    else:
        print(f"   ✗ No valid cached license")
    
    print("\n" + "=" * 60)
    print("Testing completed!")
    print("=" * 60)


if __name__ == '__main__':
    test_license_client()
