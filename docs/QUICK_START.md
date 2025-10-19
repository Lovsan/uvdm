# UVDM API Quick Start Guide

This guide will help you quickly set up and test the UVDM API system and license management.

## Prerequisites

- Python 3.7 or higher
- Flask installed (`pip install flask`)
- All dependencies from requirements.txt installed

## Step 1: Start the API Server

Open a terminal and run:

```bash
# Linux/Mac
cd /path/to/uvdm
python api_server.py

# Or with custom configuration
export UVDM_API_PORT=5000
export UVDM_ADMIN_KEY=my_secure_key
python api_server.py
```

Windows:
```cmd
cd C:\path\to\uvdm
python api_server.py
```

You should see:
```
Starting UVDM License Server on 0.0.0.0:5000
Debug mode: False
 * Running on http://0.0.0.0:5000
```

## Step 2: Generate a License Key

Open another terminal and generate a test license:

```bash
curl -X POST http://localhost:5000/api/license/generate \
  -H "Content-Type: application/json" \
  -d '{
    "admin_key": "admin123",
    "license_type": "premium",
    "duration_days": 365,
    "features": ["download", "upload", "playlist", "batch"]
  }'
```

Response:
```json
{
  "success": true,
  "license_key": "UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX",
  "license_type": "premium",
  "expiry_date": "2025-10-19T...",
  "features": ["download", "upload", "playlist", "batch"]
}
```

**Save this license key!** You'll need it in the next steps.

## Step 3: Test License Activation

Activate your license for your machine:

```bash
# Replace YOUR_LICENSE_KEY with the key from Step 2
curl -X POST http://localhost:5000/api/license/activate \
  -H "Content-Type: application/json" \
  -d '{
    "license_key": "YOUR_LICENSE_KEY",
    "machine_id": "my-test-machine"
  }'
```

Response:
```json
{
  "success": true,
  "message": "License activated successfully",
  "license_type": "premium",
  "expiry_date": "2025-10-19T..."
}
```

## Step 4: Verify the License

Verify your activated license:

```bash
curl -X POST http://localhost:5000/api/license/verify \
  -H "Content-Type: application/json" \
  -d '{
    "license_key": "YOUR_LICENSE_KEY",
    "machine_id": "my-test-machine"
  }'
```

Response:
```json
{
  "valid": true,
  "license_type": "premium",
  "expiry_date": "2025-10-19T...",
  "features": ["download", "upload", "playlist", "batch"]
}
```

## Step 5: Use the UVDM Application

Now start the UVDM application:

```bash
# Configure the license server URL (optional, defaults to localhost:5000)
export UVDM_LICENSE_SERVER=http://localhost:5000

# Start UVDM
python main.py
```

In the application:
1. Go to **Help** > **License Manager**
2. Enter your license key
3. Click **Activate License**
4. Click **Verify License** to confirm

The license status will be displayed in the dialog.

## Step 6: Test Offline Mode

1. Stop the API server (Ctrl+C)
2. In UVDM, go to **Help** > **License Manager**
3. Click **Verify License**

You should see the license is still valid, using cached data. The cache is valid for 7 days.

## Testing with Python Script

Run the included test script:

```bash
python test_license_client.py
```

This will test all license operations programmatically.

## Common Commands

### Check Server Status
```bash
curl http://localhost:5000/
```

### View License Statistics (Admin)
```bash
curl http://localhost:5000/api/license/status
```

### Deactivate a License
```bash
curl -X POST http://localhost:5000/api/license/deactivate \
  -H "Content-Type: application/json" \
  -d '{
    "license_key": "YOUR_LICENSE_KEY",
    "machine_id": "my-test-machine"
  }'
```

## Production Deployment

For production use:

1. **Change the admin key**:
   ```bash
   export UVDM_ADMIN_KEY=your_very_secure_random_key
   ```

2. **Use HTTPS**: Deploy behind a reverse proxy like nginx with SSL/TLS

3. **Secure the server**: Don't expose the API server directly to the internet

4. **Regular backups**: Backup `data/licenses.json` regularly

5. **Monitor logs**: Check `api_server.log` for issues

## Troubleshooting

### Server won't start
- Check if port 5000 is already in use
- Try a different port: `export UVDM_API_PORT=8080`

### License verification fails
- Ensure the API server is running
- Check the server URL is correct
- Verify network connectivity
- Check server logs for errors

### Application doesn't show license dialog
- Ensure you've pulled the latest code
- Check that all dependencies are installed
- Look for errors in the console

### Offline mode not working
- License must be verified online at least once
- Check if cache file exists: `data/license_cache.json`
- Cache is only valid for 7 days

## Need Help?

- Check the full API documentation: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
- Review the test script: `test_license_client.py`
- Check server logs: Look at console output or `api_server.log`

## Example: Complete Workflow

Here's a complete example from start to finish:

```bash
# Terminal 1: Start API server
python api_server.py

# Terminal 2: Generate and use license
# Generate license
LICENSE_KEY=$(curl -s -X POST http://localhost:5000/api/license/generate \
  -H "Content-Type: application/json" \
  -d '{"admin_key": "admin123", "license_type": "premium", "duration_days": 365}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['license_key'])")

echo "Generated license: $LICENSE_KEY"

# Activate license
curl -X POST http://localhost:5000/api/license/activate \
  -H "Content-Type: application/json" \
  -d "{\"license_key\": \"$LICENSE_KEY\", \"machine_id\": \"test-machine\"}"

# Verify license
curl -X POST http://localhost:5000/api/license/verify \
  -H "Content-Type: application/json" \
  -d "{\"license_key\": \"$LICENSE_KEY\", \"machine_id\": \"test-machine\"}"

# Terminal 3: Start UVDM with license server configured
export UVDM_LICENSE_SERVER=http://localhost:5000
python main.py
```

Now you can use the License Manager in the application with your generated license key!
