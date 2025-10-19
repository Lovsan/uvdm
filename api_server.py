"""
Simple API homeserver for license verification and management.
This server handles license validation for the UVDM application.
"""

from flask import Flask, request, jsonify
import json
import os
import hashlib
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)

# Configuration
LICENSE_FILE = os.path.join('data', 'licenses.json')
API_KEYS_FILE = os.path.join('data', 'api_keys.json')

# Ensure data directory exists
os.makedirs('data', exist_ok=True)


def load_licenses():
    """Load licenses from JSON file."""
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_licenses(licenses):
    """Save licenses to JSON file."""
    with open(LICENSE_FILE, 'w', encoding='utf-8') as f:
        json.dump(licenses, f, indent=2, ensure_ascii=False)


def load_api_keys():
    """Load API keys from JSON file."""
    if os.path.exists(API_KEYS_FILE):
        try:
            with open(API_KEYS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_api_keys(api_keys):
    """Save API keys to JSON file."""
    with open(API_KEYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(api_keys, f, indent=2, ensure_ascii=False)


def generate_license_key():
    """Generate a unique license key."""
    random_part = secrets.token_hex(16)
    return f"UVDM-{random_part[:8].upper()}-{random_part[8:16].upper()}-{random_part[16:24].upper()}-{random_part[24:].upper()}"


def hash_machine_id(machine_id):
    """Hash the machine ID for storage."""
    return hashlib.sha256(machine_id.encode()).hexdigest()


@app.route('/')
def index():
    """API root endpoint."""
    return jsonify({
        'name': 'UVDM License Server',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            '/api/license/verify': 'POST - Verify a license key',
            '/api/license/activate': 'POST - Activate a license key',
            '/api/license/deactivate': 'POST - Deactivate a license key',
            '/api/license/status': 'GET - Check license status',
            '/api/license/generate': 'POST - Generate a new license key (admin)',
        }
    })


@app.route('/api/license/verify', methods=['POST'])
def verify_license():
    """Verify if a license key is valid."""
    data = request.get_json()
    
    if not data or 'license_key' not in data:
        return jsonify({'valid': False, 'error': 'Missing license_key'}), 400
    
    license_key = data['license_key']
    machine_id = data.get('machine_id', '')
    
    licenses = load_licenses()
    
    if license_key not in licenses:
        return jsonify({
            'valid': False,
            'error': 'Invalid license key'
        }), 404
    
    license_info = licenses[license_key]
    
    # Check if license is expired
    if 'expiry_date' in license_info and license_info['expiry_date']:
        expiry_date = datetime.fromisoformat(license_info['expiry_date'])
        if datetime.now() > expiry_date:
            return jsonify({
                'valid': False,
                'error': 'License expired',
                'expiry_date': license_info['expiry_date']
            }), 403
    
    # Check if license is active
    if not license_info.get('active', False):
        return jsonify({
            'valid': False,
            'error': 'License is not active'
        }), 403
    
    # Check machine binding if present
    if machine_id and license_info.get('machine_id'):
        hashed_machine_id = hash_machine_id(machine_id)
        if license_info['machine_id'] != hashed_machine_id:
            return jsonify({
                'valid': False,
                'error': 'License is bound to a different machine'
            }), 403
    
    return jsonify({
        'valid': True,
        'license_type': license_info.get('license_type', 'standard'),
        'expiry_date': license_info.get('expiry_date'),
        'features': license_info.get('features', [])
    })


@app.route('/api/license/activate', methods=['POST'])
def activate_license():
    """Activate a license key for a specific machine."""
    data = request.get_json()
    
    if not data or 'license_key' not in data or 'machine_id' not in data:
        return jsonify({'success': False, 'error': 'Missing license_key or machine_id'}), 400
    
    license_key = data['license_key']
    machine_id = data['machine_id']
    
    licenses = load_licenses()
    
    if license_key not in licenses:
        return jsonify({
            'success': False,
            'error': 'Invalid license key'
        }), 404
    
    license_info = licenses[license_key]
    
    # Check if already bound to another machine
    if license_info.get('machine_id') and license_info['machine_id'] != hash_machine_id(machine_id):
        return jsonify({
            'success': False,
            'error': 'License already activated on another machine'
        }), 403
    
    # Activate the license
    licenses[license_key]['machine_id'] = hash_machine_id(machine_id)
    licenses[license_key]['active'] = True
    licenses[license_key]['activated_at'] = datetime.now().isoformat()
    
    save_licenses(licenses)
    
    return jsonify({
        'success': True,
        'message': 'License activated successfully',
        'license_type': license_info.get('license_type', 'standard'),
        'expiry_date': license_info.get('expiry_date')
    })


@app.route('/api/license/deactivate', methods=['POST'])
def deactivate_license():
    """Deactivate a license key."""
    data = request.get_json()
    
    if not data or 'license_key' not in data:
        return jsonify({'success': False, 'error': 'Missing license_key'}), 400
    
    license_key = data['license_key']
    machine_id = data.get('machine_id', '')
    
    licenses = load_licenses()
    
    if license_key not in licenses:
        return jsonify({
            'success': False,
            'error': 'Invalid license key'
        }), 404
    
    license_info = licenses[license_key]
    
    # Verify machine ID if provided
    if machine_id and license_info.get('machine_id'):
        hashed_machine_id = hash_machine_id(machine_id)
        if license_info['machine_id'] != hashed_machine_id:
            return jsonify({
                'success': False,
                'error': 'Cannot deactivate license from different machine'
            }), 403
    
    # Deactivate the license
    licenses[license_key]['active'] = False
    licenses[license_key]['deactivated_at'] = datetime.now().isoformat()
    
    save_licenses(licenses)
    
    return jsonify({
        'success': True,
        'message': 'License deactivated successfully'
    })


@app.route('/api/license/status', methods=['GET'])
def license_status():
    """Get status of all licenses (admin endpoint)."""
    licenses = load_licenses()
    
    status = {
        'total_licenses': len(licenses),
        'active_licenses': sum(1 for lic in licenses.values() if lic.get('active', False)),
        'expired_licenses': 0
    }
    
    # Count expired licenses
    now = datetime.now()
    for lic in licenses.values():
        if 'expiry_date' in lic and lic['expiry_date']:
            try:
                expiry_date = datetime.fromisoformat(lic['expiry_date'])
                if now > expiry_date:
                    status['expired_licenses'] += 1
            except (ValueError, TypeError):
                pass
    
    return jsonify(status)


@app.route('/api/license/generate', methods=['POST'])
def generate_license():
    """Generate a new license key (admin endpoint)."""
    data = request.get_json() or {}
    
    # Simple admin authentication (in production, use proper authentication)
    admin_key = data.get('admin_key', '')
    if admin_key != os.environ.get('UVDM_ADMIN_KEY', 'admin123'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    license_key = generate_license_key()
    
    # Set license parameters
    license_type = data.get('license_type', 'standard')
    duration_days = data.get('duration_days', 365)
    features = data.get('features', ['download', 'upload', 'playlist', 'batch'])
    
    expiry_date = None
    if duration_days > 0:
        expiry_date = (datetime.now() + timedelta(days=duration_days)).isoformat()
    
    licenses = load_licenses()
    
    licenses[license_key] = {
        'license_type': license_type,
        'created_at': datetime.now().isoformat(),
        'expiry_date': expiry_date,
        'active': False,
        'features': features,
        'machine_id': None
    }
    
    save_licenses(licenses)
    
    return jsonify({
        'success': True,
        'license_key': license_key,
        'license_type': license_type,
        'expiry_date': expiry_date,
        'features': features
    })


@app.route('/api/claim-trial', methods=['POST'])
def claim_trial():
    """
    Claim a free trial period (placeholder implementation).
    This endpoint is called by the client when a user claims their free trial.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Missing request data'}), 400
    
    duration_days = data.get('duration_days', 14)
    
    # Calculate expiration date
    expires_at = (datetime.now() + timedelta(days=duration_days)).isoformat()
    
    # In a real implementation, you would:
    # 1. Verify the user is not already on a trial
    # 2. Check user authentication
    # 3. Store trial information in database
    # 4. Send confirmation email
    
    return jsonify({
        'success': True,
        'message': 'Trial claimed successfully',
        'expires_at': expires_at,
        'duration_days': duration_days
    })


@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """
    Create a Stripe checkout session (placeholder implementation).
    Returns 501 Not Implemented if Stripe is not configured.
    """
    # Check if Stripe is configured
    stripe_key = os.environ.get('STRIPE_SECRET_KEY')
    
    if not stripe_key or stripe_key.startswith('sk_test_XXX'):
        return jsonify({
            'error': 'Stripe payment integration not configured',
            'message': 'Please configure Stripe API keys in config/payments.json or environment variables',
            'setup_instructions': {
                'step1': 'Create a Stripe account at https://stripe.com',
                'step2': 'Get your API keys from Stripe Dashboard',
                'step3': 'Set STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY environment variables',
                'step4': 'Restart the API server',
                'docs': 'See README.md for detailed setup instructions'
            }
        }), 501
    
    # If Stripe is configured, this is where you would:
    # 1. Import stripe library
    # 2. Create a checkout session
    # 3. Return the checkout URL
    
    return jsonify({
        'success': True,
        'checkout_url': 'https://checkout.stripe.com/placeholder',
        'message': 'Stripe integration active (placeholder response)'
    })


@app.route('/api/paypal/create-order', methods=['POST'])
def create_paypal_order():
    """
    Create a PayPal order (placeholder implementation).
    Returns 501 Not Implemented if PayPal is not configured.
    """
    # Check if PayPal is configured
    paypal_client_id = os.environ.get('PAYPAL_CLIENT_ID')
    
    if not paypal_client_id or paypal_client_id.startswith('XXX'):
        return jsonify({
            'error': 'PayPal payment integration not configured',
            'message': 'Please configure PayPal API credentials in config/payments.json or environment variables',
            'setup_instructions': {
                'step1': 'Create a PayPal Business account',
                'step2': 'Create an app in PayPal Developer Dashboard',
                'step3': 'Set PAYPAL_CLIENT_ID and PAYPAL_SECRET environment variables',
                'step4': 'Set PAYPAL_MODE to "sandbox" or "live"',
                'step5': 'Restart the API server',
                'docs': 'See README.md for detailed setup instructions'
            }
        }), 501
    
    # If PayPal is configured, this is where you would:
    # 1. Import PayPal SDK
    # 2. Create an order
    # 3. Return the approval URL
    
    return jsonify({
        'success': True,
        'approval_url': 'https://paypal.com/placeholder',
        'message': 'PayPal integration active (placeholder response)'
    })


@app.route('/api/trim', methods=['POST'])
def trim_video():
    """
    Trim a video (placeholder implementation).
    Returns 501 Not Implemented as this requires video processing infrastructure.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Missing request data'}), 400
    
    source = data.get('source')
    start = data.get('start')
    end = data.get('end')
    
    if not all([source, start is not None, end is not None]):
        return jsonify({'error': 'Missing required fields: source, start, end'}), 400
    
    # This is a placeholder. Real implementation would:
    # 1. Download/access the source video
    # 2. Use ffmpeg to trim the video
    # 3. Store the trimmed video
    # 4. Return a download URL or job ID
    
    return jsonify({
        'error': 'Server-side video trimming not implemented',
        'message': 'This is a placeholder endpoint. Server-side trimming requires additional infrastructure.',
        'suggestion': 'Use local trimming mode in the client for now',
        'implementation_notes': {
            'requirements': [
                'FFmpeg installed on server',
                'Storage for processed videos',
                'Queue system for video processing jobs',
                'CDN or file server for downloads'
            ],
            'todo': 'Implement video processing worker and storage backend'
        }
    }), 501


if __name__ == '__main__':
    # Run the server
    port = int(os.environ.get('UVDM_API_PORT', 5000))
    host = os.environ.get('UVDM_API_HOST', '0.0.0.0')
    debug = os.environ.get('UVDM_API_DEBUG', 'False').lower() == 'true'
    admin_key = os.environ.get('UVDM_ADMIN_KEY', 'admin123')
    
    print(f"Starting UVDM License Server on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    # Security warning
    if admin_key == 'admin123':
        print("\n" + "="*60)
        print("⚠️  SECURITY WARNING ⚠️")
        print("="*60)
        print("You are using the DEFAULT admin key 'admin123'")
        print("This is INSECURE and should ONLY be used for testing!")
        print("\nFor production, set a secure admin key:")
        print("  export UVDM_ADMIN_KEY=$(python -c \"import secrets; print(secrets.token_urlsafe(32))\")")
        print("="*60 + "\n")
    
    app.run(host=host, port=port, debug=debug)
