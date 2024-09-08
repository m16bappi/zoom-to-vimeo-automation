import base64
import requests
from datetime import timedelta, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import ConfigLoader, VimeoUploader, UploadTracker


class ZoomToVimeo:
    def __init__(self):
        self.tracker = UploadTracker()
        self.uploader = VimeoUploader('config/vimeo.json')

    def get_access_token(self, account: dict) -> str:
        """
        Retrieve the access token for the given Zoom account.
        """
        url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={account['account_id']}"
        basic_token = base64.b64encode(f"{account['client_id']}:{account['client_secret']}".encode('utf-8')).decode('utf-8')

        headers = {
            'Authorization': f'Basic {basic_token}',
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, headers=headers).json()

        if 'access_token' not in response:
            raise Exception(f"Failed to retrieve access token for account: {account['account_id']}")

        return response['access_token']

    def get_recordings(self, access_token: str) -> list:
        """
        Fetch Zoom recordings for the current user using the given access token.
        """
        url = 'https://api.zoom.us/v2/users/me/recordings'
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(url, headers=headers).json()

        if 'meetings' not in response:
            print(f"{datetime.now()} - No recordings found or API error: {response}")
            return []

        return response['meetings']

    def convert_duration(self, minutes) -> str:
        total_time = timedelta(minutes=minutes)
        hours, remainder = divmod(total_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def process_recordings(self, recordings: list, access_token: str):
        """
        Process each meeting's recordings and download the MP4 files.
        """
        for meeting in recordings:
            meeting_id = meeting.get('id')
            start_time = meeting.get('start_time')

            if self.tracker.has_uploaded(meeting_id, start_time):
                continue

            topic = meeting.get('topic')
            duration = self.convert_duration(meeting['duration'])

            # Extract MP4 download links
            download_links = [
                file['download_url'] for file in meeting.get('recording_files', [])
                if file.get('file_type') == 'MP4'
            ]

            for video_url in download_links:
                url = f"{video_url}?access_token={access_token}"
                print(f"{datetime.now()} - video processing: {topic}")
                vimeo_url = self.uploader.upload(url=url, video_name=topic, start_time=start_time)
                self.tracker.save_video_record(meeting_id, topic, start_time, vimeo_url, duration)

    def process_account(self, account: dict):
        access_token = self.get_access_token(account)
        recordings = self.get_recordings(access_token)
        self.process_recordings(recordings, access_token)

    def run(self):
        zoom_accounts = ConfigLoader('config/zoom.json').get('accounts', [])
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.process_account, account) for account in zoom_accounts]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f'{datetime.now()} - Error occurred: {e}')


if __name__ == '__main__':
    zoom_to_vimeo = ZoomToVimeo()
    zoom_to_vimeo.run()
