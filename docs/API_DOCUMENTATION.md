# UVDM API System and Homeserver

This document describes the API system and homeserver for license verification in UVDM (Ultimate Video Download Manager).

## Overview

The UVDM API system consists of two main components:

1. **API Server (Homeserver)** - A Flask-based server that handles license verification, activation, and management
2. **License Client** - A Python module integrated into the UVDM application for communicating with the API server

## Features

- **License Generation**: Generate unique license keys with configurable expiration dates
- **License Activation**: Bind licenses to specific machines
- **License Verification**: Verify license validity and check expiration
- **Offline Mode**: Cache license validation for offline use (up to 7 days)
- **Machine Binding**: Prevent license sharing by binding to machine ID
- **Feature Flags**: Control which features are available for each license

## API Server

### Running the Server

```bash
# Basic usage
python api_server.py

# With custom configuration
export UVDM_API_PORT=8080
export UVDM_API_HOST=0.0.0.0
export UVDM_ADMIN_KEY=your_secure_key
python api_server.py

# Using the config file
source api_config.env
python api_server.py
```

### API Endpoints

#### 1. Root Endpoint
- **URL**: `/`
- **Method**: GET
- **Description**: Get API information and available endpoints
- **Response**: JSON with API details

#### 2. Verify License
- **URL**: `/api/license/verify`
- **Method**: POST
- **Body**:
  ```json
  {
    "license_key": "UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX",
    "machine_id": "optional_machine_id"
  }
  ```
- **Response**:
  ```json
  {
    "valid": true,
    "license_type": "standard",
    "expiry_date": "2025-10-19T00:00:00",
    "features": ["download", "upload", "playlist", "batch"]
  }
  ```

#### 3. Activate License
- **URL**: `/api/license/activate`
- **Method**: POST
- **Body**:
  ```json
  {
    "license_key": "UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX",
    "machine_id": "machine_identifier"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "License activated successfully",
    "license_type": "standard",
    "expiry_date": "2025-10-19T00:00:00"
  }
  ```

#### 4. Deactivate License
- **URL**: `/api/license/deactivate`
- **Method**: POST
- **Body**:
  ```json
  {
    "license_key": "UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX",
    "machine_id": "optional_machine_id"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "License deactivated successfully"
  }
  ```

#### 5. License Status (Admin)
- **URL**: `/api/license/status`
- **Method**: GET
- **Description**: Get statistics about all licenses
- **Response**:
  ```json
  {
    "total_licenses": 10,
    "active_licenses": 7,
    "expired_licenses": 2
  }
  ```

#### 6. Generate License (Admin)
- **URL**: `/api/license/generate`
- **Method**: POST
- **Body**:
  ```json
  {
    "admin_key": "your_admin_key",
    "license_type": "standard",
    "duration_days": 365,
    "features": ["download", "upload", "playlist", "batch"]
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "license_key": "UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX",
    "license_type": "standard",
    "expiry_date": "2025-10-19T00:00:00",
    "features": ["download", "upload", "playlist", "batch"]
  }
  ```

## License Client

### Usage in Application

```python
from app.license_client import LicenseClient

# Initialize the client
client = LicenseClient(server_url='http://localhost:5000')

# Verify a license
result = client.verify_license('UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX')
if result['valid']:
    print("License is valid!")
    print(f"License type: {result['license_type']}")
    print(f"Expires: {result['expiry_date']}")
else:
    print(f"License verification failed: {result['error']}")

# Activate a license
result = client.activate_license('UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX')
if result['success']:
    print("License activated successfully!")

# Check server status
if client.check_server_status():
    print("Server is online")
```

### Offline Mode

The license client automatically caches successful verifications for offline use. Cached licenses are valid for 7 days.

```python
# Force offline mode
result = client.verify_license('UVDM-XXX...', offline_mode=True)
if result['valid'] and result.get('offline'):
    print(f"Using cached license (age: {result['cache_age_days']} days)")
```

## Data Storage

The API server stores data in JSON files:

- `data/licenses.json` - License information
- `data/api_keys.json` - API keys (future use)
- `data/license_cache.json` - Client-side license cache

## Security Considerations

1. **Change the default admin key** in production (`UVDM_ADMIN_KEY`)
2. **Use HTTPS** for production deployments
3. **Implement rate limiting** to prevent abuse
4. **Regular backups** of license data
5. **Machine ID hashing** prevents exposure of system information

## Testing

You can test the API using curl:

```bash
# Generate a license (requires admin key)
curl -X POST http://localhost:5000/api/license/generate \
  -H "Content-Type: application/json" \
  -d '{"admin_key": "admin123", "license_type": "standard", "duration_days": 365}'

# Verify a license
curl -X POST http://localhost:5000/api/license/verify \
  -H "Content-Type: application/json" \
  -d '{"license_key": "UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX", "machine_id": "test-machine"}'

# Activate a license
curl -X POST http://localhost:5000/api/license/activate \
  -H "Content-Type: application/json" \
  -d '{"license_key": "UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX", "machine_id": "test-machine"}'
```

## Future Enhancements

- User authentication and authorization
- License usage analytics
- Multi-tier licensing (free, premium, enterprise)
- Automated license renewal
- Web-based admin dashboard
- Payment integration
- Email notifications for expiring licenses

## Troubleshooting

### Server won't start
- Check if port 5000 is already in use
- Verify Python and Flask are installed correctly
- Check file permissions on data directory

### License verification fails
- Ensure the API server is running
- Check network connectivity
- Verify the license key format
- Check server logs for errors

### Offline mode not working
- Ensure license was verified online at least once
- Check cache file exists in `data/license_cache.json`
- Cache is valid for only 7 days

## License

This API system is part of UVDM and follows the same MIT License.
