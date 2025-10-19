"""
Admin Payment Routes

Flask routes for managing payment providers and webhook settings.
These endpoints are protected by admin authentication.
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import os
from server.models.payment_provider import PaymentProvider
from server.models.webhook_settings import WebhookSettings


# Create Blueprint
admin_payments_bp = Blueprint('admin_payments', __name__)


def require_admin_auth(f):
    """
    Decorator to require admin authentication.
    
    Checks for ADMIN_API_KEY in the X-Admin-Key header.
    Set UVDM_ADMIN_KEY environment variable to enable authentication.
    If not set, authentication is disabled (for development).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_key = os.environ.get('UVDM_ADMIN_KEY')
        
        # If no admin key is configured, allow access (development mode)
        if not admin_key:
            return f(*args, **kwargs)
        
        # Check for admin key in header
        provided_key = request.headers.get('X-Admin-Key')
        
        if not provided_key or provided_key != admin_key:
            return jsonify({
                'error': 'Unauthorized. Admin authentication required.',
                'message': 'Set X-Admin-Key header with valid admin key.'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


# ============================================================================
# Payment Provider Routes
# ============================================================================

@admin_payments_bp.route('/api/admin/payments', methods=['GET'])
@require_admin_auth
def get_payment_providers():
    """Get all payment providers."""
    try:
        providers = PaymentProvider.get_all()
        include_secrets = request.args.get('include_secrets', 'false').lower() == 'true'
        
        return jsonify({
            'success': True,
            'providers': [p.to_dict(include_secrets=include_secrets) for p in providers]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_payments_bp.route('/api/admin/payments/<int:provider_id>', methods=['GET'])
@require_admin_auth
def get_payment_provider(provider_id):
    """Get a specific payment provider."""
    try:
        provider = PaymentProvider.get_by_id(provider_id)
        
        if not provider:
            return jsonify({
                'success': False,
                'error': 'Provider not found'
            }), 404
        
        include_secrets = request.args.get('include_secrets', 'false').lower() == 'true'
        
        return jsonify({
            'success': True,
            'provider': provider.to_dict(include_secrets=include_secrets)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_payments_bp.route('/api/admin/payments', methods=['POST'])
@require_admin_auth
def create_payment_provider():
    """Create a new payment provider."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Validate required fields
        if 'provider_key' not in data or 'provider_name' not in data:
            return jsonify({
                'success': False,
                'error': 'provider_key and provider_name are required'
            }), 400
        
        # Check if provider_key already exists
        existing = PaymentProvider.get_by_key(data['provider_key'])
        if existing:
            return jsonify({
                'success': False,
                'error': 'Provider with this key already exists'
            }), 409
        
        # Create provider
        provider = PaymentProvider(
            provider_key=data['provider_key'],
            provider_name=data['provider_name'],
            config=data.get('config', {}),
            enabled=data.get('enabled', False)
        )
        
        provider.save()
        
        return jsonify({
            'success': True,
            'provider': provider.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_payments_bp.route('/api/admin/payments/<int:provider_id>', methods=['PUT'])
@require_admin_auth
def update_payment_provider(provider_id):
    """Update an existing payment provider."""
    try:
        provider = PaymentProvider.get_by_id(provider_id)
        
        if not provider:
            return jsonify({
                'success': False,
                'error': 'Provider not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Update fields
        if 'provider_key' in data:
            # Check if new key conflicts with existing provider
            existing = PaymentProvider.get_by_key(data['provider_key'])
            if existing and existing.id != provider_id:
                return jsonify({
                    'success': False,
                    'error': 'Provider with this key already exists'
                }), 409
            provider.provider_key = data['provider_key']
        
        if 'provider_name' in data:
            provider.provider_name = data['provider_name']
        
        if 'config' in data:
            provider.config = data['config']
        
        if 'enabled' in data:
            provider.enabled = data['enabled']
        
        provider.save()
        
        return jsonify({
            'success': True,
            'provider': provider.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_payments_bp.route('/api/admin/payments/<int:provider_id>', methods=['DELETE'])
@require_admin_auth
def delete_payment_provider(provider_id):
    """Delete a payment provider."""
    try:
        provider = PaymentProvider.get_by_id(provider_id)
        
        if not provider:
            return jsonify({
                'success': False,
                'error': 'Provider not found'
            }), 404
        
        provider.delete()
        
        return jsonify({
            'success': True,
            'message': 'Provider deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# Webhook Settings Routes
# ============================================================================

@admin_payments_bp.route('/api/admin/payments/<int:provider_id>/webhooks', methods=['GET'])
@require_admin_auth
def get_provider_webhooks(provider_id):
    """Get all webhook settings for a provider."""
    try:
        provider = PaymentProvider.get_by_id(provider_id)
        
        if not provider:
            return jsonify({
                'success': False,
                'error': 'Provider not found'
            }), 404
        
        webhooks = WebhookSettings.get_by_provider(provider_id)
        include_secrets = request.args.get('include_secrets', 'false').lower() == 'true'
        
        return jsonify({
            'success': True,
            'webhooks': [w.to_dict(include_secrets=include_secrets) for w in webhooks]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_payments_bp.route('/api/admin/payments/<int:provider_id>/webhooks', methods=['POST'])
@require_admin_auth
def create_provider_webhook(provider_id):
    """Create a new webhook setting for a provider."""
    try:
        provider = PaymentProvider.get_by_id(provider_id)
        
        if not provider:
            return jsonify({
                'success': False,
                'error': 'Provider not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Generate secret if requested
        webhook_secret = data.get('webhook_secret')
        if data.get('generate_secret'):
            webhook_secret = WebhookSettings.generate_secret()
        
        # Create webhook settings
        webhook = WebhookSettings(
            provider_id=provider_id,
            webhook_url=data.get('webhook_url', ''),
            webhook_secret=webhook_secret,
            enabled=data.get('enabled', False)
        )
        
        webhook.save()
        
        return jsonify({
            'success': True,
            'webhook': webhook.to_dict(include_secrets=True)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_payments_bp.route('/api/admin/payments/<int:provider_id>/webhooks/<int:webhook_id>', methods=['PUT'])
@require_admin_auth
def update_provider_webhook(provider_id, webhook_id):
    """Update webhook settings."""
    try:
        webhook = WebhookSettings.get_by_id(webhook_id)
        
        if not webhook:
            return jsonify({
                'success': False,
                'error': 'Webhook not found'
            }), 404
        
        if webhook.provider_id != provider_id:
            return jsonify({
                'success': False,
                'error': 'Webhook does not belong to this provider'
            }), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Update fields
        if 'webhook_url' in data:
            webhook.webhook_url = data['webhook_url']
        
        if 'webhook_secret' in data:
            webhook.webhook_secret = data['webhook_secret']
        
        if data.get('generate_secret'):
            webhook.webhook_secret = WebhookSettings.generate_secret()
        
        if 'enabled' in data:
            webhook.enabled = data['enabled']
        
        webhook.save()
        
        return jsonify({
            'success': True,
            'webhook': webhook.to_dict(include_secrets=True)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_payments_bp.route('/api/admin/payments/<int:provider_id>/webhooks/<int:webhook_id>', methods=['DELETE'])
@require_admin_auth
def delete_provider_webhook(provider_id, webhook_id):
    """Delete webhook settings."""
    try:
        webhook = WebhookSettings.get_by_id(webhook_id)
        
        if not webhook:
            return jsonify({
                'success': False,
                'error': 'Webhook not found'
            }), 404
        
        if webhook.provider_id != provider_id:
            return jsonify({
                'success': False,
                'error': 'Webhook does not belong to this provider'
            }), 400
        
        webhook.delete()
        
        return jsonify({
            'success': True,
            'message': 'Webhook deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
