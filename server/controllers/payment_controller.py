"""
Payment Controller

This module handles payment-related business logic including webhook verification
for different payment providers (Stripe, PayPal, Wise, Crypto).
"""

import hashlib
import hmac
import json
from server.models.payment_provider import PaymentProvider
from server.models.webhook_settings import WebhookSettings


class PaymentController:
    """Controller for payment operations."""
    
    @staticmethod
    def verify_stripe_webhook(payload, signature_header, webhook_secret):
        """
        Verify Stripe webhook signature.
        
        Stripe sends a signature in the 'Stripe-Signature' header.
        Format: t=timestamp,v1=signature
        
        Args:
            payload: Raw webhook payload (bytes or string)
            signature_header: Value of Stripe-Signature header
            webhook_secret: Webhook secret from Stripe dashboard
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not webhook_secret or not signature_header:
            return False
        
        try:
            # Parse signature header
            sig_parts = {}
            for part in signature_header.split(','):
                key, value = part.split('=', 1)
                sig_parts[key] = value
            
            timestamp = sig_parts.get('t')
            signature = sig_parts.get('v1')
            
            if not timestamp or not signature:
                return False
            
            # Construct signed payload
            if isinstance(payload, str):
                payload = payload.encode('utf-8')
            
            signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
            
            # Compute expected signature
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                signed_payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures (constant time comparison)
            return hmac.compare_digest(expected_signature, signature)
            
        except Exception as e:
            print(f"Stripe webhook verification error: {e}")
            return False
    
    @staticmethod
    def verify_paypal_webhook(payload, signature_header, webhook_secret):
        """
        Verify PayPal webhook signature (mock implementation).
        
        Note: Real PayPal webhook verification requires certificate validation
        and more complex logic. This is a placeholder.
        
        Args:
            payload: Raw webhook payload
            signature_header: Signature header from PayPal
            webhook_secret: Webhook secret
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        # Mock verification - in production, implement proper PayPal verification
        # See: https://developer.paypal.com/docs/api-basics/notifications/webhooks/notification-messages/#link-verifysignature
        
        if not webhook_secret:
            return False
        
        # Placeholder: Always return True if secret is configured
        # TODO: Implement actual PayPal webhook signature verification
        return True
    
    @staticmethod
    def verify_wise_webhook(payload, signature_header, webhook_secret):
        """
        Verify Wise (TransferWise) webhook signature (mock implementation).
        
        Wise uses HMAC-SHA256 signature verification.
        
        Args:
            payload: Raw webhook payload
            signature_header: Signature header from Wise
            webhook_secret: Webhook secret
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not webhook_secret or not signature_header:
            return False
        
        try:
            # Wise typically uses X-Signature or X-Signature-SHA256 header
            if isinstance(payload, str):
                payload = payload.encode('utf-8')
            
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, signature_header)
            
        except Exception as e:
            print(f"Wise webhook verification error: {e}")
            return False
    
    @staticmethod
    def verify_crypto_webhook(payload, signature_header, webhook_secret):
        """
        Verify cryptocurrency webhook signature (mock implementation).
        
        Generic HMAC-SHA256 verification for crypto payment processors.
        
        Args:
            payload: Raw webhook payload
            signature_header: Signature header
            webhook_secret: Webhook secret
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not webhook_secret or not signature_header:
            return False
        
        try:
            if isinstance(payload, str):
                payload = payload.encode('utf-8')
            
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, signature_header)
            
        except Exception as e:
            print(f"Crypto webhook verification error: {e}")
            return False
    
    @staticmethod
    def verify_webhook(provider_key, payload, headers, webhook_secret):
        """
        Verify webhook based on provider.
        
        Args:
            provider_key: Payment provider key (stripe, paypal, wise, crypto)
            payload: Raw webhook payload
            headers: Request headers dict
            webhook_secret: Webhook secret for verification
            
        Returns:
            bool: True if verification succeeds or no secret configured, False if verification fails
        """
        # If no webhook secret configured, accept all webhooks but log it
        if not webhook_secret:
            print(f"Warning: No webhook secret configured for {provider_key}, accepting webhook without verification")
            return True
        
        # Route to appropriate verification method
        if provider_key == 'stripe':
            signature = headers.get('Stripe-Signature', '')
            return PaymentController.verify_stripe_webhook(payload, signature, webhook_secret)
        
        elif provider_key == 'paypal':
            signature = headers.get('PAYPAL-TRANSMISSION-SIG', '')
            return PaymentController.verify_paypal_webhook(payload, signature, webhook_secret)
        
        elif provider_key == 'wise':
            signature = headers.get('X-Signature-SHA256', headers.get('X-Signature', ''))
            return PaymentController.verify_wise_webhook(payload, signature, webhook_secret)
        
        elif provider_key == 'crypto':
            signature = headers.get('X-Webhook-Signature', '')
            return PaymentController.verify_crypto_webhook(payload, signature, webhook_secret)
        
        else:
            # Unknown provider
            print(f"Unknown provider: {provider_key}")
            return False
    
    @staticmethod
    def create_payment_session(provider_key, amount=None, currency=None, metadata=None):
        """
        Create a payment session/checkout for the given provider.
        
        This is a stub implementation that returns mock data.
        Real implementation would call provider APIs.
        
        Args:
            provider_key: Payment provider key
            amount: Payment amount
            currency: Payment currency
            metadata: Additional metadata
            
        Returns:
            dict: Session data or error information
        """
        provider = PaymentProvider.get_by_key(provider_key)
        
        if not provider:
            return {
                'success': False,
                'error': 'Provider not found',
                'status_code': 404
            }
        
        if not provider.enabled:
            return {
                'success': False,
                'error': 'Provider is not enabled',
                'status_code': 503
            }
        
        # Check if provider has configuration
        if not provider.config or not any(provider.config.values()):
            return {
                'success': False,
                'error': 'Provider not configured. Admin must add API keys in /admin/payments',
                'status_code': 501,
                'admin_url': '/admin/payments'
            }
        
        # Stub response - in production, call actual provider API
        return {
            'success': True,
            'provider': provider_key,
            'session_id': f'mock_session_{provider_key}_{hash(str(metadata))}',
            'checkout_url': f'https://mock-checkout.{provider_key}.com/session',
            'message': 'This is a mock payment session. Configure real API keys to enable live payments.',
            'test_mode': provider.config.get('test_mode', True)
        }
    
    @staticmethod
    def confirm_payment(provider_key, session_id, payment_data=None):
        """
        Confirm a payment after user completes checkout.
        
        This is a stub implementation.
        Real implementation would verify payment with provider API.
        
        Args:
            provider_key: Payment provider key
            session_id: Payment session ID
            payment_data: Additional payment confirmation data
            
        Returns:
            dict: Confirmation result
        """
        provider = PaymentProvider.get_by_key(provider_key)
        
        if not provider:
            return {
                'success': False,
                'error': 'Provider not found'
            }
        
        # Stub response
        return {
            'success': True,
            'provider': provider_key,
            'session_id': session_id,
            'status': 'completed',
            'message': 'Mock payment confirmation. Configure real API keys for actual payment processing.'
        }
