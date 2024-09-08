# Zoom to Vimeo Uploader

This project automates the process of fetching Zoom meeting recordings and uploading them to Vimeo. It retrieves Zoom recordings using OAuth, processes each video, and uploads them to Vimeo using their API.

## Features
- **Zoom Integration**: Fetch Zoom recordings using OAuth 2.0 with account credentials.
- **Vimeo Integration**: Upload the downloaded Zoom recordings to Vimeo.
- **Concurrent Processing**: Handle multiple Zoom accounts and videos simultaneously using Python's `ThreadPoolExecutor`.
- **Tracking**: Prevent duplicate uploads by tracking already uploaded Zoom meetings.
- **Configurable**: Configure multiple Zoom accounts via a JSON file.

## Requirements

- Python 3.8+
- Vimeo account and API credentials
- Zoom account and OAuth app credentials
  
Here are the single commands to create a virtual environment, activate it, and install dependencies from `requirements.txt` for both **Windows** and **Linux/macOS**:

### **For Windows (PowerShell)**:

```bash
python -m venv venv; .\venv\Scripts\Activate; pip install -r requirements.txt
```

### **For Linux/macOS (Terminal)**:

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

These commands will set up the virtual environment, activate it, and install the necessary packages in one step.

## Project Structure

## Project Structure

```
.
├── config
│   ├── vimeo.json       # Vimeo API credentials
│   └── zoom.json        # Zoom account details
├── utils                # Utility module
│   ├── __init__.py      # Initializes utils module
│   ├── uploader.py      # Handles video uploads to Vimeo
│   ├── downloader.py    # Handles downloading Zoom recordings
│   ├── config_loader.py # Loads configuration from JSON files
│   └── tracker.py       # Tracks video uploads and prevents duplicates
├── main.py              # Main script to run the Zoom to Vimeo process
├── server.py            # Streamlit-based data viewer for uploaded records
├── requirements.txt     # List of dependencies required to run the project
└── README.md            # This README file
```

This structure provides the necessary components to run the project, including the required dependencies listed in `requirements.txt`.

## Configuration

### Zoom Account (`config/zoom.json`)
Add your Zoom OAuth credentials and account information in `config/zoom.json`. The JSON should have the following structure:

```json
{
    "accounts": [
        {
            "client_id": "your_zoom_client_id",
            "client_secret": "your_zoom_client_secret",
            "account_id": "your_zoom_account_id"
        }
    ]
}
```

### Vimeo Configuration (`config/vimeo.json`)
The Vimeo configuration should contain your Vimeo API credentials and upload settings:

```json
{
  "client_id": "",
  "client_secret": "",
  "access_token": ""
}
```

## How to Run

1. Ensure all configurations for Zoom and Vimeo are set up correctly.
2. Run the following command:

```bash
python main.py
```

This will start the process of fetching Zoom recordings, downloading them, and uploading them to Vimeo.

## Classes and Methods

### `ZoomToVimeo`
This is the main class that handles the flow from fetching Zoom recordings to uploading them to Vimeo.

- `get_access_token(account: dict)`: Retrieves the Zoom OAuth access token for the provided account.
- `get_recordings(access_token: str)`: Fetches the list of Zoom recordings.
- `convert_duration(minutes: int)`: Converts Zoom meeting duration (in minutes) into `HH:MM:SS` format.
- `process_recordings(recordings: list, access_token: str)`: Processes the recordings, downloading them and uploading to Vimeo.
- `process_account(account: dict)`: Manages the processing of recordings for each Zoom account.
- `run()`: Executes the program, processing recordings concurrently for multiple Zoom accounts.

## Customization

- **Add New Zoom Accounts**: Add new accounts to `zoom.json`.
- **Adjust Concurrency**: Modify `max_workers` in the `ThreadPoolExecutor` to adjust how many accounts are processed simultaneously.

# Zoom to Vimeo Uploaded Data Viewer

This `server.py` script is a Streamlit-based web app that loads and displays the uploaded Zoom to Vimeo video records from a CSV file. The application reads the CSV data, processes it, and provides a simple and interactive interface to preview the uploaded records.

## How to Run

1. Ensure your CSV file (`uploaded.csv`) is in the same directory as `server.py` or update the `FILE_PATH` variable with the correct file path.

2. Run the Streamlit app using the following command:

```bash
streamlit run server.py
```

3. The app will launch in your browser, displaying the Zoom to Vimeo video records.

## Example

Here is a sample layout of the app when displaying the data:

```text
+----------------------------------+-------------+--------------------------------+
|   Index  |  Meeting Host Time    |  Meeting ID |    Other columns (optional)    |
+----------------------------------+-------------+--------------------------------+
|     1    |  2023-09-06 10:00:00  |  1234567890 |    Additional Information      |
|     2    |  2023-08-30 09:30:00  |  0987654321 |    Additional Information      |
+----------------------------------+-------------+--------------------------------+
```

This simple web app allows you to quickly visualize and explore Zoom to Vimeo uploaded data records.

## License
This project is open-source and free to use under the [MIT License](LICENSE).
