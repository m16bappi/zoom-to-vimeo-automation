import vimeo
import requests
import tempfile
from datetime import datetime
from .config_loader import ConfigLoader


class VimeoUploader:
    def __init__(self, config_path):
        self.config = ConfigLoader(config_path).config_data
        self.domain = 'https://vimeo.com'
        self.vimeo_client = vimeo.VimeoClient(
            token=self.config['access_token'],
            key=self.config['client_id'],
            secret=self.config['client_secret']
        )

    def upload(self, url, video_name: str, start_time: str):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=True) as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

                f.flush()
                print(f"{datetime.now()} - video uploading: {video_name}")
                uri: str = self.vimeo_client.upload(
                    f.name,
                    data={
                        'name': f"{video_name} - {start_time}",
                        'description': video_name,
                    }
                )
                link = f"{self.domain}/{uri.split('/').pop()}"
                print(f"{datetime.now()} - Video uploaded: {video_name} to link: {link}")
                return link
