import os


class FileHandler:
    def __init__(self, file_path):
        """
        Initialize the FileHandler class

        This function initializes the FileHandler class with a file path.
        Gets the directory of the file from settings
        """
        self.file_path = file_path

    def read(self):
        with open(self.file_path) as f:
            return f.read()
        
    def write(self, data):
        with open(self.file_path, 'w') as f:
            f.write(data)
    
    def append(self, data):
        with open(self.file_path, 'a') as f:
            f.write(data)
    