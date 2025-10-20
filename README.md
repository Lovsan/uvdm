# Ultimate Video Download Manager (UVDM)

UVDM is a powerful and easy-to-use tool for downloading and managing videos from popular websites. Built with a feature-rich interface, it offers multiple video formats (MP3, MP4, AVI...), playlist downloads, batch downloads, and integrated history for seamless content organization.

## Key Features

- **Download videos in various formats**: Supports MP3, MP4, AVI, and more.
- **Torrent Support**: Download torrents from public and private trackers with magnet links and .torrent files.
- **Clipboard Monitoring**: Detects supported video links automatically.
- **Playlist and Batch Download Support**: Download entire playlists or batch multiple links together.
- **Integrated Download History**: View downloaded videos with thumbnails, video details, and advanced sorting options.
- **Customizable Themes**: Personalize the look of the application with multiple themes.
- **Multi-threaded Downloads**: Faster downloads by utilizing multiple threads.
- **Manage Downloads**: Resume, rename, delete, or play downloads directly from the app.
- **Active Downloads Overview**: Monitor active downloads, network usage, and storage usage.
- **yt-dlp Integration**: Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp) for reliable and powerful downloading capabilities.
- **License Management System**: Optional API-based license verification and management for enterprise deployments.
- **Video Preview & Trimming**: Preview videos and trim them to your desired length with built-in FFmpeg integration.
- **2-Week Free Pro Trial**: First-time users can try Pro features for 2 weeks, no credit card required.
- **Multiple Payment Options**: Subscribe to Pro via Stripe or PayPal (when configured).
- **1000+ Supported Platforms**: Download from YouTube, Facebook, Instagram, TikTok, and 1000+ more sites.

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



## Torrent Support

UVDM now includes comprehensive torrent downloading capabilities powered by libtorrent.

### Features

- **Magnet Link Support**: Paste magnet links directly into UVDM
- **.torrent File Support**: Upload and download .torrent files
- **Public Tracker Support**: Download from public torrent sites
- **Private Tracker Support**: Configure authentication for private trackers
- **Real-time Information**: View seeds, peers, download/upload speeds
- **File Information**: See complete file lists with sizes before downloading
- **Progress Tracking**: Monitor download progress with detailed statistics

### Using Torrents

1. Launch UVDM and navigate to the "Torrents" tab
2. Enter a magnet link or browse for a .torrent file
3. Select your download location
4. Click "Start Download" to begin
5. Monitor progress with real-time statistics
6. View downloaded files in the specified output folder

### Torrent Information Display

The Torrents tab displays comprehensive information about your torrent:

- **Torrent Name**: The name of the content being downloaded
- **Total Size**: Combined size of all files in the torrent
- **File Count**: Number of files in the torrent
- **Creator**: Who created the torrent (if available)
- **Creation Date**: When the torrent was created
- **File List**: Detailed list of all files with individual sizes
- **Real-time Stats**: Seeds, peers, download/upload speeds
- **Download Progress**: Visual progress bar and percentage

### Technical Details

- **Library**: libtorrent 2.0.11+
- **Protocol**: BitTorrent protocol with DHT, PEX, and UPnP support
- **Session Management**: Efficient session handling with proper cleanup
- **Thread Safety**: Non-blocking downloads using Qt threading

## Dependencies

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [libtorrent](https://www.libtorrent.org/)
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

## Supported Platforms

UVDM supports downloading videos from 1000+ platforms through yt-dlp integration. Here are some of the most popular:

### Featured Platforms

- **YouTube**: Single videos, playlists, channels, multiple qualities (144p to 4K+), age-restricted content, subtitles
- **Facebook**: Public videos, Facebook Watch, live videos, multiple quality options
- **Instagram**: Post videos, Reels, IGTV, Stories (with authentication for private accounts)
- **TikTok**: Single videos, downloads without watermark (when possible), audio extraction
- **Adult Content Sites**: Various adult platforms with premium content support (18+, requires authentication)
- **And 1000+ More**: Twitter/X, Reddit, Vimeo, Dailymotion, Twitch, SoundCloud, and many more

### Viewing Platform Information

1. Launch UVDM
2. Navigate to the "About" tab or "Pro Features" tab
3. Click on any platform icon to see detailed support information
4. Use the "View Supported Sites" button to see the complete list of 1000+ supported extractors

## Free Trial & Pro Features

### 2-Week Free Trial

First-time users can try UVDM Pro features for 2 weeks, completely free with no credit card required!

**To claim your free trial:**

1. Launch UVDM
2. Navigate to the "Pro Features" tab
3. Click the "Claim Free Trial" button
4. Enjoy 14 days of Pro features!

**Pro Features Include:**

- 🚀 Faster download speeds with priority servers
- 📹 Advanced video editing and trimming tools
- 🎬 Batch processing up to 100 videos
- ☁️ Cloud storage integration
- 🔄 Automatic format conversion
- 📊 Detailed download analytics
- 🎯 Ad-free experience
- 💬 Priority customer support
- 🔓 Access to exclusive features

### Trial Details

- Trial information is stored locally using Qt Settings
- If the API server is configured, trial data is also synced to the server
- No credit card required for trial activation
- Full access to all Pro features during trial period
- Automatic notification when trial is about to expire

## Payment & Subscription

UVDM supports multiple payment methods for Pro subscriptions:

### Supported Payment Methods

- **Stripe**: Credit/debit cards, Apple Pay, Google Pay
- **PayPal**: PayPal balance, credit/debit cards

### Subscription Plans

- **Pro Monthly**: $9.99/month - All Pro features
- **Pro Yearly**: $99.99/year - Save 2 months (annual billing)

### Setting Up Payment Integration (For Administrators)

Payment integration requires configuration on the API server. Follow these steps:

#### 1. Configure Payment Keys

Create a `config/payments.json` file based on `config/payments.example.json`:

```bash
cp config/payments.example.json config/payments.json
```

Edit `config/payments.json` and add your API keys:

**For Stripe:**
```json
{
  "stripe": {
    "enabled": true,
    "publishable_key": "pk_live_YOUR_KEY",
    "secret_key": "sk_live_YOUR_KEY",
    "webhook_secret": "whsec_YOUR_SECRET"
  }
}
```

**For PayPal:**
```json
{
  "paypal": {
    "enabled": true,
    "mode": "live",
    "client_id": "YOUR_CLIENT_ID",
    "secret": "YOUR_SECRET"
  }
}
```

#### 2. Set Environment Variables (Alternative)

You can also configure payments using environment variables:

```bash
# Stripe
export STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_KEY
export STRIPE_SECRET_KEY=sk_live_YOUR_KEY
export STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET

# PayPal
export PAYPAL_CLIENT_ID=YOUR_CLIENT_ID
export PAYPAL_SECRET=YOUR_SECRET
export PAYPAL_MODE=live  # or 'sandbox' for testing
```

#### 3. Create Products and Plans

**Stripe Setup:**
1. Log in to [Stripe Dashboard](https://dashboard.stripe.com)
2. Create products: "UVDM Pro Monthly" and "UVDM Pro Yearly"
3. Create prices for each product
4. Copy the price IDs and add them to `config/payments.json`

**PayPal Setup:**
1. Log in to [PayPal Developer Dashboard](https://developer.paypal.com)
2. Create subscription plans
3. Copy the plan IDs and add them to `config/payments.json`

#### 4. Set Up Webhooks

**Stripe Webhooks:**
1. In Stripe Dashboard, go to Developers → Webhooks
2. Add endpoint: `https://your-domain.com/api/webhooks/stripe`
3. Select events: `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`
4. Copy the webhook signing secret to `config/payments.json`

**PayPal Webhooks:**
1. In PayPal Developer Dashboard, go to your app → Webhooks
2. Add webhook URL: `https://your-domain.com/api/webhooks/paypal`
3. Select events: `BILLING.SUBSCRIPTION.CREATED`, `BILLING.SUBSCRIPTION.UPDATED`, `BILLING.SUBSCRIPTION.CANCELLED`

#### 5. Restart the API Server

```bash
python api_server.py
```

### Testing Payment Integration

Use test mode before going live:

**Stripe Test Mode:**
- Use test API keys (pk_test_... and sk_test_...)
- Test with [Stripe test cards](https://stripe.com/docs/testing)

**PayPal Sandbox:**
- Set `"mode": "sandbox"` in config
- Use [PayPal Sandbox accounts](https://developer.paypal.com/docs/api-basics/sandbox/)

### Payment Placeholder Mode

If payment credentials are not configured, UVDM operates in "placeholder mode":
- Payment buttons are visible but show configuration instructions when clicked
- Users see helpful setup messages
- No actual payment processing occurs
- Perfect for development and testing

## Video Preview & Trimming

UVDM includes built-in video preview and trimming capabilities powered by FFmpeg.

### Features

- Preview videos in your system's default media player
- Trim videos to specific start and end times
- Two trimming modes: Local (fast) and Server-side (for URLs)
- Visual time selection with second precision
- Progress indicators for trimming operations
- Save trimmed videos with custom names

### Using Video Preview & Trim

1. Download a video using UVDM
2. Navigate to "Download History" tab
3. Right-click on a downloaded video
4. Select "Preview & Trim" from the context menu
5. In the preview dialog:
   - Click "▶ Play" to preview the full video
   - Set start and end times for trimming
   - Choose trimming mode (Local or Server-side)
   - Click "✂️ Trim Video" to create the trimmed version
   - Save the trimmed video to your desired location

### Trimming Modes

**Local Mode (Recommended):**
- Requires: Downloaded video file and FFmpeg installed
- Pros: Fast processing, no server required, works offline
- Uses: FFmpeg with copy codec for quick trimming

**Server-side Mode:**
- Requires: API server with video processing configured
- Pros: Works with video URLs, no local FFmpeg needed
- Note: This is currently a placeholder - server implementation required

### FFmpeg Installation

Video trimming requires FFmpeg to be installed:

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

### Server-side Trimming (For Administrators)

To enable server-side trimming, implement the `/api/trim` endpoint in `api_server.py`:

1. Install FFmpeg on the server
2. Set up video storage (local or cloud)
3. Implement video processing queue
4. Handle trim requests and return download URLs
5. Configure CDN or file server for video delivery

The endpoint specification is already defined in `api_server.py` as a placeholder.

**Important**: Change the default admin key in production!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve UVDM.

## Acknowledgments

- **yt-dlp**: The core downloading tool used by UVDM.
- **libtorrent**: High-performance BitTorrent implementation for torrent downloads.
- **ffmpeg**: A complete, cross-platform solution to record, convert and stream audio and video.

## Links

- **GitHub Repository**: [Ultimate Video Download Manager](https://github.com/Lovsan/uvdm)
- **yt-dlp GitHub Repository**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **libtorrent Website**: [libtorrent.org](https://www.libtorrent.org/)

Get started with UVDM and simplify your video downloading experience!
