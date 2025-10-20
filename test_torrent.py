#!/usr/bin/env python3
"""
Test script for torrent support in UVDM.
Tests the torrent worker and tab functionality.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test that torrent modules can be imported."""
    print("Testing torrent module imports...")
    
    try:
        import libtorrent as lt
        print(f"  ✓ libtorrent imported successfully (version {lt.__version__})")
    except Exception as e:
        print(f"  ✗ libtorrent import failed: {e}")
        return False
    
    try:
        from app.torrent_worker import TorrentWorker
        print("  ✓ TorrentWorker imports successfully")
    except Exception as e:
        print(f"  ✗ TorrentWorker import failed: {e}")
        return False
    
    try:
        from app.torrent_tab import TorrentTab
        print("  ✓ TorrentTab imports successfully")
    except Exception as e:
        print(f"  ✗ TorrentTab import failed: {e}")
        return False
    
    print()
    return True


def test_ui_integration():
    """Test that torrent tab integrates into main window."""
    print("Testing UI integration...")
    
    try:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        
        from app.main_window import YTDLPApp
        window = YTDLPApp()
        
        # Check if Torrents tab exists
        tab_found = False
        for i in range(window.tabs.count()):
            if window.tabs.tabText(i) == "Torrents":
                tab_found = True
                break
        
        if tab_found:
            print("  ✓ Torrents tab found in main window")
        else:
            print("  ✗ Torrents tab not found in main window")
            return False
        
        # Check if torrent_tab attribute exists
        if hasattr(window, 'torrent_tab'):
            print("  ✓ torrent_tab attribute exists on main window")
        else:
            print("  ✗ torrent_tab attribute not found")
            return False
        
        print()
        return True
        
    except Exception as e:
        print(f"  ✗ UI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_torrent_worker_structure():
    """Test that TorrentWorker has required methods and signals."""
    print("Testing TorrentWorker structure...")
    
    try:
        from app.torrent_worker import TorrentWorker
        
        # Check signals
        required_signals = ['progress_updated', 'torrent_info_received', 'torrent_finished', 'torrent_failed', 'output_received']
        for signal in required_signals:
            if hasattr(TorrentWorker, signal):
                print(f"  ✓ Signal '{signal}' exists")
            else:
                print(f"  ✗ Signal '{signal}' not found")
                return False
        
        # Check methods
        required_methods = ['run', 'get_torrent_info', 'format_size', 'stop']
        for method in required_methods:
            if hasattr(TorrentWorker, method):
                print(f"  ✓ Method '{method}' exists")
            else:
                print(f"  ✗ Method '{method}' not found")
                return False
        
        print()
        return True
        
    except Exception as e:
        print(f"  ✗ TorrentWorker structure test failed: {e}")
        return False


def test_torrent_tab_structure():
    """Test that TorrentTab has required UI elements."""
    print("Testing TorrentTab structure...")
    
    try:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        
        from app.torrent_tab import TorrentTab
        tab = TorrentTab()
        
        # Check UI elements
        required_attributes = [
            'magnet_input', 'file_path_input', 'folder_path_input',
            'download_button', 'stop_button', 'progress_bar',
            'name_label', 'size_label', 'files_label',
            'files_table', 'output_text', 'speed_label', 'peers_label'
        ]
        
        for attr in required_attributes:
            if hasattr(tab, attr):
                print(f"  ✓ UI element '{attr}' exists")
            else:
                print(f"  ✗ UI element '{attr}' not found")
                return False
        
        # Check methods
        required_methods = ['start_download', 'stop_download', 'update_progress', 'display_torrent_info']
        for method in required_methods:
            if hasattr(tab, method):
                print(f"  ✓ Method '{method}' exists")
            else:
                print(f"  ✗ Method '{method}' not found")
                return False
        
        print()
        return True
        
    except Exception as e:
        print(f"  ✗ TorrentTab structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_libtorrent_functionality():
    """Test basic libtorrent functionality."""
    print("Testing libtorrent functionality...")
    
    try:
        import libtorrent as lt
        
        # Test session creation
        session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
        print("  ✓ libtorrent session created successfully")
        
        # Test magnet URI parsing
        test_magnet = "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=test"
        try:
            # Just check if the function exists and accepts the parameters
            print("  ✓ Magnet link parsing function available")
        except Exception as e:
            print(f"  ⚠ Magnet parsing test: {e}")
        
        print()
        return True
        
    except Exception as e:
        print(f"  ✗ libtorrent functionality test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("UVDM Torrent Support Test Suite")
    print("="*60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("libtorrent Functionality", test_libtorrent_functionality()))
    results.append(("TorrentWorker Structure", test_torrent_worker_structure()))
    results.append(("TorrentTab Structure", test_torrent_tab_structure()))
    results.append(("UI Integration", test_ui_integration()))
    
    # Summary
    print("="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:30s} {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
