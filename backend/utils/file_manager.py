import os
import time
from pathlib import Path
from typing import List


def cleanup_old_files(directory: Path, max_age_seconds: int = 3600) -> List[Path]:
    """
    Clean up files older than max_age_seconds in the specified directory.
    
    Args:
        directory: Directory to clean up
        max_age_seconds: Maximum age of files in seconds (default: 1 hour)
    
    Returns:
        List of deleted file paths
    """
    deleted_files = []
    
    if not directory.exists():
        return deleted_files
    
    current_time = time.time()
    
    for file_path in directory.iterdir():
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                    deleted_files.append(file_path)
                except OSError:
                    # If we can't delete the file, continue with the next
                    continue
    
    return deleted_files


def ensure_directory_exists(path: Path) -> Path:
    """
    Ensure that the specified directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists
    
    Returns:
        The directory path
    """
    path.mkdir(parents=True, exist_ok=True)
    return path