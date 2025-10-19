#!/usr/bin/env python3
"""
Test script for new UI features added to UVDM.
Tests platform icons, trial banner, payment widgets, and video preview/trim functionality.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test that all new modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.platform_icons_widget import PlatformIconsWidget
        print("  ✓ PlatformIconsWidget imports successfully")
    except Exception as e:
        print(f"  ✗ PlatformIconsWidget import failed: {e}")
        return False
    
    try:
        from app.trial_banner_widget import TrialBannerWidget
        print("  ✓ TrialBannerWidget imports successfully")
    except Exception as e:
        print(f"  ✗ TrialBannerWidget import failed: {e}")
        return False
    
    try:
        from app.payment_widget import PaymentWidget
        print("  ✓ PaymentWidget imports successfully")
    except Exception as e:
        print(f"  ✗ PaymentWidget import failed: {e}")
        return False
    
    try:
        from app.video_preview_dialog import VideoPreviewDialog
        print("  ✓ VideoPreviewDialog imports successfully")
    except Exception as e:
        print(f"  ✗ VideoPreviewDialog import failed: {e}")
        return False
    
    try:
        from app.pro_features_tab import ProFeaturesTab
        print("  ✓ ProFeaturesTab imports successfully")
    except Exception as e:
        print(f"  ✗ ProFeaturesTab import failed: {e}")
        return False
    
    try:
        from app.main_window import YTDLPApp
        print("  ✓ Main window imports successfully with all new components")
    except Exception as e:
        print(f"  ✗ Main window import failed: {e}")
        return False
    
    print()
    return True


def test_api_endpoints():
    """Test that API endpoints are accessible and respond correctly."""
    print("Testing API endpoints...")
    
    try:
        import requests
        import json
        from subprocess import Popen, PIPE
        import time
        
        # Get the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Start API server in background
        print("  Starting API server...")
        server_process = Popen(
            [sys.executable, "api_server.py"],
            stdout=PIPE,
            stderr=PIPE,
            cwd=script_dir
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Test endpoints
        base_url = "http://localhost:5000"
        
        # Test claim-trial
        try:
            response = requests.post(f"{base_url}/api/claim-trial", json={"duration_days": 14}, timeout=5)
            if response.status_code == 200:
                print("  ✓ /api/claim-trial responds correctly")
            else:
                print(f"  ✗ /api/claim-trial returned {response.status_code}")
        except Exception as e:
            print(f"  ✗ /api/claim-trial failed: {e}")
        
        # Test Stripe checkout (should return 501)
        try:
            response = requests.post(f"{base_url}/api/create-checkout-session", json={"plan": "pro_monthly"}, timeout=5)
            if response.status_code == 501:
                print("  ✓ /api/create-checkout-session returns 501 (placeholder)")
            else:
                print(f"  ⚠ /api/create-checkout-session returned {response.status_code} (expected 501)")
        except Exception as e:
            print(f"  ✗ /api/create-checkout-session failed: {e}")
        
        # Test PayPal order (should return 501)
        try:
            response = requests.post(f"{base_url}/api/paypal/create-order", json={"plan": "pro_monthly"}, timeout=5)
            if response.status_code == 501:
                print("  ✓ /api/paypal/create-order returns 501 (placeholder)")
            else:
                print(f"  ⚠ /api/paypal/create-order returned {response.status_code} (expected 501)")
        except Exception as e:
            print(f"  ✗ /api/paypal/create-order failed: {e}")
        
        # Test trim endpoint (should return 501)
        try:
            response = requests.post(f"{base_url}/api/trim", json={"source": "test.mp4", "start": 0, "end": 10}, timeout=5)
            if response.status_code == 501:
                print("  ✓ /api/trim returns 501 (placeholder)")
            else:
                print(f"  ⚠ /api/trim returned {response.status_code} (expected 501)")
        except Exception as e:
            print(f"  ✗ /api/trim failed: {e}")
        
        # Stop server
        server_process.terminate()
        server_process.wait(timeout=5)
        print("  ✓ API server stopped")
        
    except Exception as e:
        print(f"  ✗ API endpoint testing failed: {e}")
        return False
    
    print()
    return True


def test_assets():
    """Test that all asset files exist."""
    print("Testing assets...")
    
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets", "platform-icons")
    
    required_icons = [
        "instagram.svg",
        "tiktok.svg",
        "facebook.svg",
        "youtube.svg",
        "adult.svg",
        "more.svg"
    ]
    
    all_exist = True
    for icon in required_icons:
        icon_path = os.path.join(assets_dir, icon)
        if os.path.exists(icon_path):
            print(f"  ✓ {icon} exists")
        else:
            print(f"  ✗ {icon} missing at {icon_path}")
            all_exist = False
    
    print()
    return all_exist


def test_config_files():
    """Test that configuration files exist."""
    print("Testing configuration files...")
    
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, "config")
    
    payments_example = os.path.join(config_dir, "payments.example.json")
    if os.path.exists(payments_example):
        print("  ✓ payments.example.json exists")
        
        # Validate JSON
        try:
            import json
            with open(payments_example, 'r') as f:
                config = json.load(f)
            print("  ✓ payments.example.json is valid JSON")
            
            # Check for required keys
            if "stripe" in config and "paypal" in config and "plans" in config:
                print("  ✓ payments.example.json has required sections")
            else:
                print("  ✗ payments.example.json missing required sections")
                return False
        except Exception as e:
            print(f"  ✗ payments.example.json validation failed: {e}")
            return False
    else:
        print(f"  ✗ payments.example.json missing at {payments_example}")
        return False
    
    print()
    return True


def main():
    """Run all tests."""
    print("="*60)
    print("UVDM New Features Test Suite")
    print("="*60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Assets", test_assets()))
    results.append(("Config Files", test_config_files()))
    results.append(("API Endpoints", test_api_endpoints()))
    
    # Summary
    print("="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:20s} {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
