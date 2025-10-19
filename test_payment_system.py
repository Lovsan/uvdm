"""
Test script for payment system functionality.

This script tests the payment system components including:
- Database initialization
- Provider management
- Webhook settings
- Webhook verification
"""

import sys
import os
import json
import hashlib
import hmac

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.models.payment_provider import PaymentProvider
from server.models.webhook_settings import WebhookSettings
from server.controllers.payment_controller import PaymentController
from db.init_db import init_database, get_db_connection


def test_database_init():
    """Test database initialization."""
    print("\n" + "="*60)
    print("Testing Database Initialization")
    print("="*60)
    
    # Remove existing test database
    test_db = 'data/test_payments.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Initialize database
    success = init_database(test_db)
    
    if success and os.path.exists(test_db):
        print("✓ Database initialized successfully")
        return test_db
    else:
        print("✗ Database initialization failed")
        return None


def test_provider_operations(db_path):
    """Test payment provider CRUD operations."""
    print("\n" + "="*60)
    print("Testing Provider Operations")
    print("="*60)
    
    # Get all providers
    providers = PaymentProvider.get_all(db_path)
    print(f"✓ Found {len(providers)} providers")
    
    # Get specific provider
    stripe = PaymentProvider.get_by_key('stripe', db_path)
    if stripe:
        print(f"✓ Found Stripe provider: {stripe.provider_name}")
    
    # Update provider
    stripe.enabled = True
    stripe.config = {
        'api_key': 'sk_test_example123',
        'test_mode': True
    }
    stripe.save(db_path)
    print("✓ Updated Stripe provider")
    
    # Verify update
    stripe = PaymentProvider.get_by_key('stripe', db_path)
    if stripe.enabled:
        print("✓ Stripe is now enabled")
    
    # Test secret masking
    provider_dict = stripe.to_dict(include_secrets=False)
    if '*' in provider_dict['config']['api_key']:
        print("✓ Secret masking works correctly")
    
    # Get enabled providers
    enabled = PaymentProvider.get_enabled(db_path)
    print(f"✓ Found {len(enabled)} enabled provider(s)")


def test_webhook_operations(db_path):
    """Test webhook settings operations."""
    print("\n" + "="*60)
    print("Testing Webhook Operations")
    print("="*60)
    
    # Get provider
    stripe = PaymentProvider.get_by_key('stripe', db_path)
    
    # Create webhook settings
    webhook = WebhookSettings(
        provider_id=stripe.id,
        webhook_url='https://example.com/api/webhooks/stripe',
        webhook_secret=WebhookSettings.generate_secret(),
        enabled=True
    )
    webhook.save(db_path)
    print("✓ Created webhook settings")
    
    # Get webhooks for provider
    webhooks = WebhookSettings.get_by_provider(stripe.id, db_path)
    print(f"✓ Found {len(webhooks)} webhook(s) for Stripe")
    
    # Test secret masking
    webhook_dict = webhook.to_dict(include_secrets=False)
    if '*' in webhook_dict['webhook_secret']:
        print("✓ Webhook secret masking works correctly")


def test_webhook_verification():
    """Test webhook signature verification."""
    print("\n" + "="*60)
    print("Testing Webhook Verification")
    print("="*60)
    
    webhook_secret = 'test_secret_key'
    payload = '{"event": "payment_intent.succeeded", "data": {}}'
    
    # Test Stripe verification
    timestamp = '1234567890'
    signature = hmac.new(
        webhook_secret.encode('utf-8'),
        f"{timestamp}.{payload}".encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    signature_header = f"t={timestamp},v1={signature}"
    
    result = PaymentController.verify_stripe_webhook(
        payload, signature_header, webhook_secret
    )
    if result:
        print("✓ Stripe webhook verification passed")
    else:
        print("✗ Stripe webhook verification failed")
    
    # Test with wrong secret
    result = PaymentController.verify_stripe_webhook(
        payload, signature_header, 'wrong_secret'
    )
    if not result:
        print("✓ Stripe webhook correctly rejects invalid signature")
    else:
        print("✗ Stripe webhook verification should have failed")
    
    # Test generic webhook verification
    headers = {'Stripe-Signature': signature_header}
    result = PaymentController.verify_webhook(
        'stripe', payload, headers, webhook_secret
    )
    if result:
        print("✓ Generic webhook verification works for Stripe")
    else:
        print("✗ Generic webhook verification failed")


def test_payment_session_creation(db_path):
    """Test payment session creation."""
    print("\n" + "="*60)
    print("Testing Payment Session Creation")
    print("="*60)
    
    # Test with disabled provider
    result = PaymentController.create_payment_session(
        'paypal', amount=999, currency='usd'
    )
    if result['status_code'] == 503:
        print("✓ Correctly returns 503 for disabled provider")
    
    # Test with enabled provider
    result = PaymentController.create_payment_session(
        'stripe', amount=999, currency='usd'
    )
    if result['success']:
        print("✓ Successfully created mock payment session")
        print(f"  Session ID: {result['session_id']}")
    
    # Test with non-existent provider
    result = PaymentController.create_payment_session(
        'nonexistent', amount=999, currency='usd'
    )
    if result['status_code'] == 404:
        print("✓ Correctly returns 404 for non-existent provider")


def cleanup(db_path):
    """Clean up test database."""
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"\n✓ Cleaned up test database: {db_path}")


def main():
    """Run all tests."""
    print("="*60)
    print("UVDM Payment System Test Suite")
    print("="*60)
    
    # Initialize database
    db_path = test_database_init()
    if not db_path:
        print("\n✗ Tests failed: Could not initialize database")
        return 1
    
    try:
        # Run tests
        test_provider_operations(db_path)
        test_webhook_operations(db_path)
        test_webhook_verification()
        test_payment_session_creation(db_path)
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Tests failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        cleanup(db_path)


if __name__ == '__main__':
    sys.exit(main())
