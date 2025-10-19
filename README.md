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
