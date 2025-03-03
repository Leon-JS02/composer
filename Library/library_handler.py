"""Class to manage Composer's audio library. 
Contains utilities to add/delete files, and change the library path."""

import json
import os

import shutil


class LibraryHandler:
    """Library Handler class. Objects"""

    def __init__(self, path: str = "Library/config.json"):
        self.config_path = path
        with open(self.config_path, 'r', encoding="UTF-8") as f:
            config = json.load(f)
        self.library_path = config['library_path']

    def add_to_library(self, file_path: str):
        """Adds a file of a given path to the audio library."""
        path = os.path.basename(file_path)
        if not self.validate_file_type(path) or self.exists_in_library(path):
            return False
        try:
            shutil.copy(file_path, self.library_path)
            return True
        except:
            return False

    def delete_from_library(self, file_name: str):
        """Removes a file of a given name from the audio library"""
        if not self.exists_in_library(file_name):
            return False
        try:
            file = os.path.join(self.library_path, file_name)
            os.remove(file)
            return True
        except:
            return False

    def set_library_path(self, path: str):
        """Sets the audio library path within the config.json file."""
        if (not os.path.exists(path)) or (not os.path.isdir(path)):
            return False
        try:
            with open(self.config_path, 'r', encoding="UTF-8") as f:
                config = json.load(f)

            config["library_path"] = path

            with open(self.config_path, "w", encoding="UTF-8") as f:
                json.dump(config, f, indent=4)

            self.library_path = path
            return True

        except:
            return False

    def get_library_path(self) -> str:
        """Returns library audio path."""
        return self.library_path

    def get_library_contents(self) -> list[str]:
        """Returns a list of file names from the audio library."""
        files = os.listdir(self.library_path)
        return files

    def exists_in_library(self, file_name: str) -> bool:
        """Returns True if a file name exists within the audio library."""
        path = os.path.join(self.library_path, file_name)
        return os.path.exists(path)

    def validate_file_type(self, file: str) -> bool:
        """Returns true if an audio file's extension is accepted."""
        extension = os.path.splitext(file)[-1].lower()
        return extension in [".mp3", ".flac", ".wav", ".m4a", ".ogg"]
