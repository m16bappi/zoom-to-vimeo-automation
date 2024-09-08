import os
import csv


class UploadTracker:
    def __init__(self, csv_file_path='uploaded.csv'):
        self.csv_file_path = csv_file_path
        self.fieldnames = ['Meeting ID', 'Video Name', 'Meeting Host Time', 'Vimeo URL', 'Duration']

        # Initialize the CSV file if it doesn't exist
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

    def has_uploaded(self, meeting_id: int, start_time: str):
        """
        Check if a Zoom video has already been uploaded by looking at the CSV file.
        """
        if not os.path.isfile(self.csv_file_path):
            return False

        with open(self.csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Meeting ID'] == str(meeting_id) and row['Meeting Host Time'] == start_time:
                    return True
        return False

    def save_video_record(self, meeting_id, video_name, meeting_host_time, vimeo_url, duration):
        """
        Save the uploaded video's details to the CSV file.
        """
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow({
                'Meeting ID': meeting_id,
                'Video Name': video_name,
                'Meeting Host Time': meeting_host_time,
                'Vimeo URL': vimeo_url,
                'Duration': duration,
            })
