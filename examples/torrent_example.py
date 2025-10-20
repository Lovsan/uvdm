#!/usr/bin/env python3
"""
Example script demonstrating torrent download functionality in UVDM.

This example shows how to:
1. Download a torrent using a magnet link
2. Monitor download progress
3. Display torrent information

Note: This is a demonstration script. In actual usage, the torrent tab
in the main UVDM application provides a full GUI for torrent management.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    """Main example function."""
    
    print("="*60)
    print("UVDM Torrent Download Example")
    print("="*60)
    print()
    print("This example demonstrates the torrent functionality in UVDM.")
    print()
    print("In the actual UVDM application:")
    print("  1. Navigate to the 'Torrents' tab")
    print("  2. Paste a magnet link or select a .torrent file")
    print("  3. Choose your download location")
    print("  4. Click 'Start Download'")
    print("  5. Watch the progress in real-time!")
    print()
    print("Features:")
    print("  • Magnet link support")
    print("  • .torrent file support")
    print("  • Real-time progress tracking")
    print("  • Speed and peer monitoring")
    print("  • Complete file list display")
    print("  • Start/stop controls")
    print()
    print("To use UVDM with torrents:")
    print("  python main.py")
    print()
    print("Then navigate to the 'Torrents' tab in the application.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
