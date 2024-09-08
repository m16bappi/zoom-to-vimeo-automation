import os
import requests

class FileDownloader:
    def __init__(self, download_dir="downloads"):
        """
        Initialize the FileDownloader with a default download directory.
        If the directory doesn't exist, it will be created.
        """
        self.download_dir = download_dir
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Ensure the download directory exists, create it if not."""
        os.makedirs(self.download_dir, exist_ok=True)

    def download(self, url: str, filename: str):
        """
        Download a file from the given URL and save it to the specified file name
        in the download directory.
        """
        file_path = os.path.join(self.download_dir, filename)

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return file_path 
