class UploadWorker(QObject):
    upload_finished = pyqtSignal(dict)
    upload_failed = pyqtSignal(str)

    def __init__(self, file_path, upload_site, settings_tab):
        super().__init__()
        self.file_path = file_path
        self.upload_site = upload_site
        self.settings_tab = settings_tab

    def run(self):
        try:
            # Placeholder implementation for uploading
            # In practice, this should use the API of the selected upload site
            time.sleep(2)  # Simulate upload delay

            # Assume upload is successful
            upload_info = {
                'filename': os.path.basename(self.file_path),
                'size': os.path.getsize(self.file_path),
                'duration': self.get_video_duration(),
                'site': self.upload_site,
                'status': 'Success',
                'path': self.file_path
            }
            # Save upload info to JSON
            self.save_upload_info(upload_info)
            self.upload_finished.emit(upload_info)
        except Exception as e:
            self.upload_failed.emit(f"Error during upload: {str(e)}")

    def get_video_duration(self):
        # Placeholder for getting video duration
        return 'Unknown'

    def save_upload_info(self, upload_info):
        json_file_path = os.path.join('data', 'uploads.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        data.append(upload_info)
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)



