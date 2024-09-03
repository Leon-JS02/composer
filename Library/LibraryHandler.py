import json
import os
import shutil


class LibraryHandler:
    def __init__(self):
        self.config_path = "Library/config.json"
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        self.library_path = config['library_path']

    def add_to_library(self, file_path):
        path = os.path.basename(file_path)
        if not self.validate_file_type(path) or self.exists_in_library(path):
            return False
        try:
            shutil.copy(file_path, self.library_path)
            return True
        except:
            return False

    def delete_from_library(self, file):
        if not self.exists_in_library(file):
            return False
        try:
            file = os.path.join(self.library_path, file)
            os.remove(file)
            return True
        except:
            return False

    def set_library_path(self, path):
        if (not os.path.exists(path)) or (not os.path.isdir(path)):
            return False
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            config["library_path"] = path

            with open(self.config_path, "w") as f:
                json.dump(config, f)

            self.library_path = path
            return True

        except:
            return False

    def get_library_path(self):
        return self.library_path

    def get_library_contents(self):
        files = os.listdir(self.library_path)
        return files

    def exists_in_library(self, file_name):
        path = os.path.join(self.library_path, file_name)
        return os.path.exists(path)

    def validate_file_type(self, file):
        extension = os.path.splitext(file)[-1].lower()
        return extension in [".mp3", ".flac", ".wav", ".m4a", ".ogg"]
