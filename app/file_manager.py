
import os

def open_file(filepath):
    """Open a file using the default application."""
    if os.path.exists(filepath):
        os.startfile(filepath)

def save_file(filepath, content):
    """Save content to a specified file."""
    with open(filepath, 'w') as f:
        f.write(content)

def rename_file(old_name, new_name):
    """Rename a file."""
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
