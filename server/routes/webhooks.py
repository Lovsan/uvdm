"""
Webhook Routes

Flask routes for receiving webhooks from payment providers.
These are public endpoints that handle incoming webhook notifications.
"""

from flask import Blueprint, request, jsonify
from server.controllers.payment_controller import PaymentController
from server.models.payment_provider import PaymentProvider
from server.models.webhook_settings import WebhookSettings


# Create Blueprint
webhooks_bp = Blueprint('webhooks', __name__)


@webhooks_bp.route('/api/webhooks/<provider_key>', methods=['POST'])
def receive_webhook(provider_key):
    """
    Receive and process webhooks from payment providers.
    
    This endpoint validates the webhook signature and processes the event.
    """
    try:
        # Get provider
        provider = PaymentProvider.get_by_key(provider_key)
        
        if not provider:
            return jsonify({
                'success': False,
                'error': 'Unknown provider'
            }), 404
        
        if not provider.enabled:
            return jsonify({
                'success': False,
                'error': 'Provider is not enabled'
            }), 403
        
        # Get webhook settings for provider
        webhook_settings = WebhookSettings.get_by_provider(provider.id)
        
        # Find enabled webhook setting
        webhook_secret = None
        for webhook in webhook_settings:
            if webhook.enabled:
                webhook_secret = webhook.webhook_secret
                break
        
        # Get raw payload and headers
        payload = request.get_data()
        headers = dict(request.headers)
        
        # Verify webhook signature
        is_valid = PaymentController.verify_webhook(
            provider_key, 
            payload, 
            headers, 
            webhook_secret
        )
        
        if not is_valid:
            print(f"Webhook verification failed for provider: {provider_key}")
            return jsonify({
                'success': False,
                'error': 'Webhook signature verification failed'
            }), 400
        
        # Parse webhook payload
        try:
            webhook_data = request.get_json()
        except:
            webhook_data = {}
        
        # Log webhook receipt (in production, process the webhook properly)
        print(f"Webhook received from {provider_key}:")
        print(f"  Event type: {webhook_data.get('type', 'unknown')}")
        print(f"  Event ID: {webhook_data.get('id', 'unknown')}")
        
        # TODO: Process webhook based on event type
        # This would typically update order status, send notifications, etc.
        
        return jsonify({
            'success': True,
            'message': 'Webhook received and verified',
            'provider': provider_key
        }), 200
        
    except Exception as e:
        print(f"Webhook processing error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@webhooks_bp.route('/api/webhooks/<provider_key>/test', methods=['POST'])
def test_webhook(provider_key):
    """
    Test webhook endpoint for admin testing.
    
    This allows admins to send a test webhook to verify configuration.
    """
    try:
        provider = PaymentProvider.get_by_key(provider_key)
        
        if not provider:
            return jsonify({
                'success': False,
                'error': 'Unknown provider'
            }), 404
        
        # Get test payload
        test_data = request.get_json() or {}
        
        # Log test webhook
        print(f"Test webhook received for {provider_key}:")
        print(f"  Data: {test_data}")
        
        return jsonify({
            'success': True,
            'message': 'Test webhook received successfully',
            'provider': provider_key,
            'received_data': test_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# Payment Session Routes (Client-facing)
# ============================================================================

@webhooks_bp.route('/api/payments/<provider_key>/create-session', methods=['POST'])
def create_payment_session(provider_key):
    """
    Create a payment session/checkout for client.
    
    This is called from the frontend when user clicks a payment button.
    """
    try:
        data = request.get_json() or {}
        
        result = PaymentController.create_payment_session(
            provider_key=provider_key,
            amount=data.get('amount'),
            currency=data.get('currency'),
            metadata=data.get('metadata')
        )
        
        status_code = result.pop('status_code', 200)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@webhooks_bp.route('/api/payments/<provider_key>/confirm', methods=['POST'])
def confirm_payment(provider_key):
    """
    Confirm a payment after user completes checkout.
    
    This is called from the frontend after payment completion.
    """
    try:
        data = request.get_json() or {}
        
        result = PaymentController.confirm_payment(
            provider_key=provider_key,
            session_id=data.get('session_id'),
            payment_data=data.get('payment_data')
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@webhooks_bp.route('/api/payments/providers', methods=['GET'])
def get_available_providers():
    """
    Get list of enabled payment providers for client.
    
    Returns only enabled providers without sensitive config.
    """
    try:
        providers = PaymentProvider.get_enabled()
        
        # Return minimal info for clients
        provider_list = []
        for provider in providers:
            provider_list.append({
                'provider_key': provider.provider_key,
                'provider_name': provider.provider_name,
                'enabled': provider.enabled
            })
        
        return jsonify({
            'success': True,
            'providers': provider_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
