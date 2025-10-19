# Ultimate Video Download Manager (UVDM)

UVDM is a powerful and easy-to-use tool for downloading and managing videos from popular websites. Built with a feature-rich interface, it offers multiple video formats (MP3, MP4, AVI...), playlist downloads, batch downloads, and integrated history for seamless content organization.

## Key Features

- **Download videos in various formats**: Supports MP3, MP4, AVI, and more.
- **Clipboard Monitoring**: Detects supported video links automatically.
- **Playlist and Batch Download Support**: Download entire playlists or batch multiple links together.
- **Integrated Download History**: View downloaded videos with thumbnails, video details, and advanced sorting options.
- **Customizable Themes**: Personalize the look of the application with multiple themes.
- **Multi-threaded Downloads**: Faster downloads by utilizing multiple threads.
- **Manage Downloads**: Resume, rename, delete, or play downloads directly from the app.
- **Active Downloads Overview**: Monitor active downloads, network usage, and storage usage.
- **yt-dlp Integration**: Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp) for reliable and powerful downloading capabilities.
- **License Management System**: Optional API-based license verification and management for enterprise deployments.
- **Multi-Provider Payment System**: Support for Stripe, PayPal, Wise, and Cryptocurrency payments with comprehensive admin UI and webhook handling.

## Installation

To install UVDM, simply clone the repository and install the required dependencies:

```sh
git clone https://github.com/Lovsan/uvdm.git
cd uvdm
pip install -r requirements.txt
```

## Usage

To start UVDM, run the following command:

```sh
python main.py
```

Or use the convenience startup script:

```sh
# Linux/Mac
./start_uvdm.sh

# With API server
./start_uvdm.sh --with-api-server

# Windows
start_uvdm.bat

# With API server
start_uvdm.bat --with-api-server
```

Once the application launches, you can use the following features:

- **Paste Video URL**: UVDM will automatically detect video URLs from your clipboard.
- **Download Options**: Choose your desired format and quality before downloading.
- **Playlist Download**: Paste a playlist URL to download all the videos in it.
- **Batch Download**: Use the Batch Download feature to queue multiple links at once.

### Example

1. Launch UVDM. 
2. Copy a YouTube video URL to your clipboard.
3. The app will detect the link and prompt you to start downloading.
4. Click "Ok" "Download Later" or "Cancel"
5. The app will open new Download tab in new thread and starts the download process.
6. View your download progress in the "Active Downloads" tab.

## Screenshots



## Dependencies

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Python 3.7+
- Flask (for API server)
- Additional Python packages (listed in `requirements.txt`)

## API System and License Management

UVDM includes an optional API system for license verification and management. This is particularly useful for enterprise deployments or when you want to manage license distribution.

### Quick Start with API Server

1. Start the API server:
   ```sh
   python api_server.py
   ```

2. Generate a license (admin access):
   ```sh
   curl -X POST http://localhost:5000/api/license/generate \
     -H "Content-Type: application/json" \
     -d '{"admin_key": "admin123", "license_type": "standard", "duration_days": 365}'
   ```

3. Use the License Manager in UVDM:
   - Launch UVDM
   - Go to Help > License Manager
   - Enter your license key and activate it

For detailed API documentation, see [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md).

### Configuration

Edit `api_config.env` to configure the API server:

```env
UVDM_API_HOST=0.0.0.0
UVDM_API_PORT=5000
UVDM_ADMIN_KEY=your_secure_admin_key
UVDM_LICENSE_SERVER=http://localhost:5000
```

**Important**: Change the default admin key in production!

## Payment System (Multi-Provider Support)

UVDM now includes a comprehensive payment system that supports multiple payment providers including Stripe, PayPal, Wise, and Cryptocurrency payments. The system includes an admin interface for managing payment providers, webhook handlers for payment notifications, and a client-facing subscription page.

### Features

- **Multiple Payment Providers**: Support for Stripe, PayPal, Wise, and Cryptocurrency payments
- **Admin UI**: Comprehensive web-based admin interface for managing payment providers and webhooks
- **Webhook Support**: Secure webhook handling with signature verification for each provider
- **Database-backed Configuration**: SQLite database for storing provider credentials and webhook settings
- **Security**: Admin authentication, secret masking, and webhook signature verification
- **Test Mode**: Safe testing with mock payment sessions before going live

### Quick Start with Payment Server

1. **Start the payment-enabled API server**:
   ```sh
   python payment_api_server.py
   ```

2. **Initialize the payment database** (automatic on first run):
   ```sh
   python db/init_db.py
   ```

3. **Access the Admin UI**:
   - Open your browser to `http://localhost:5000/admin/payments`
   - Default admin key is `admin123` (change this in production!)

4. **Configure Payment Providers**:
   - Click "Add Provider" or edit existing providers
   - Add your API keys and credentials
   - Enable the provider
   - Configure webhook settings for each provider

5. **Access Client Subscription Page**:
   - Open `http://localhost:5000/static/subscription.html`
   - Users can select payment methods and initiate payments

### Payment Provider Configuration

#### Stripe

1. Sign up at [https://stripe.com](https://stripe.com)
2. Get API keys from [https://dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys)
3. In the admin UI, add provider with config:
   ```json
   {
     "api_key": "sk_test_...",
     "publishable_key": "pk_test_...",
     "test_mode": true
   }
   ```
4. Create webhook at [https://dashboard.stripe.com/webhooks](https://dashboard.stripe.com/webhooks)
5. Set webhook URL to `https://yourserver.com/api/webhooks/stripe`
6. Add webhook secret to webhook settings in admin UI

#### PayPal

1. Sign up at [https://developer.paypal.com](https://developer.paypal.com)
2. Create an app in the PayPal Developer Dashboard
3. Get Client ID and Secret from app settings
4. In the admin UI, add provider with config:
   ```json
   {
     "client_id": "your_client_id",
     "client_secret": "your_client_secret",
     "test_mode": true
   }
   ```

#### Wise (TransferWise)

1. Sign up at [https://wise.com](https://wise.com)
2. Generate API token from settings
3. In the admin UI, add provider with config:
   ```json
   {
     "api_token": "your_api_token",
     "test_mode": true
   }
   ```

#### Cryptocurrency

1. Set up cryptocurrency wallets (Bitcoin, Ethereum, etc.)
2. In the admin UI, add provider with config:
   ```json
   {
     "btc_address": "your_btc_address",
     "eth_address": "your_eth_address",
     "test_mode": true
   }
   ```

### Webhook Configuration

Webhooks allow payment providers to notify your server about payment events in real-time.

1. **Configure Webhook URL**: Set the webhook URL for each provider in the admin UI
   - Format: `https://yourserver.com/api/webhooks/{provider_key}`
   - Example: `https://yourserver.com/api/webhooks/stripe`

2. **Generate Webhook Secret**: Use the 🔑 button in the admin UI to generate a secure secret

3. **Enable Webhook**: Toggle the "Enabled" checkbox

4. **Test Webhook**: Use the "Test" button to send a test webhook to verify configuration

### API Endpoints

#### Admin Endpoints (require `X-Admin-Key` header)

- `GET /api/admin/payments` - List all payment providers
- `POST /api/admin/payments` - Create a new payment provider
- `PUT /api/admin/payments/:id` - Update a payment provider
- `DELETE /api/admin/payments/:id` - Delete a payment provider
- `GET /api/admin/payments/:id/webhooks` - List webhooks for a provider
- `POST /api/admin/payments/:id/webhooks` - Create webhook settings
- `PUT /api/admin/payments/:id/webhooks/:webhookId` - Update webhook settings
- `DELETE /api/admin/payments/:id/webhooks/:webhookId` - Delete webhook settings

#### Public Endpoints

- `POST /api/payments/:provider/create-session` - Create a payment session
- `POST /api/payments/:provider/confirm` - Confirm a payment
- `GET /api/payments/providers` - List enabled payment providers
- `POST /api/webhooks/:provider` - Receive webhook from payment provider

### Security Best Practices

1. **Set a Secure Admin Key**:
   ```sh
   export UVDM_ADMIN_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   ```

2. **Use HTTPS in Production**: Webhooks and API endpoints should use HTTPS

3. **Rotate Webhook Secrets Regularly**: Generate new secrets periodically

4. **Test Mode First**: Always test with test API keys before using production keys

5. **Monitor Webhook Logs**: Check server logs for webhook verification failures

6. **Restrict Admin Access**: Only expose admin endpoints to trusted networks

### Database Structure

The payment system uses SQLite with two main tables:

- **payment_providers**: Stores payment provider configurations
  - `id`, `provider_key`, `provider_name`, `config` (JSON), `enabled`, `created_at`, `updated_at`

- **webhook_settings**: Stores webhook configurations for each provider
  - `id`, `provider_id`, `webhook_url`, `webhook_secret`, `enabled`, `created_at`, `updated_at`

### Configuration Files

- `config/payments-db.example.json` - Database and provider configuration examples
- `db/migrations/20251019_create_payment_tables.sql` - Database schema migration

### Development Mode

By default, the system runs in development mode with:
- Default admin key `admin123` (shown with security warning)
- Mock payment sessions (no real charges)
- Test mode enabled for all providers

### Production Deployment

For production deployment:

1. Set secure environment variables:
   ```sh
   export UVDM_ADMIN_KEY="your_secure_random_key"
   export UVDM_API_HOST="0.0.0.0"
   export UVDM_API_PORT="5000"
   export UVDM_API_DEBUG="False"
   ```

2. Use a production WSGI server (e.g., Gunicorn):
   ```sh
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 payment_api_server:app
   ```

3. Set up reverse proxy (nginx, Apache) with HTTPS

4. Replace test API keys with production keys

5. Enable webhooks with proper secrets

For more details, see `config/payments-db.example.json`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve UVDM.

## Acknowledgments

- **yt-dlp**: The core downloading tool used by UVDM.
- **ffmpeg** A complete, cross-platform solution to record, convert and stream audio and video

## Links

- **GitHub Repository**: [Ultimate Video Download Manager](https://github.com/Lovsan/uvdm)
- **yt-dlp GitHub Repository**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)

Get started with UVDM and simplify your video downloading experience!
