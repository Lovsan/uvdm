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
- Additional Python packages (listed in `requirements.txt`)

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
