from .file_handler import FileHandler
import json

class JSONHandler(FileHandler):

    def __init__(self, file_path):
        """
        Initialize the JSONHandler class

        This function initializes the JSONHandler class with a file path.
        Gets the directory of the file from settings
        """
        super().__init__(file_path)

    def read(self):
        "Read python object from JSON file"
        with open(self.file_path) as f:
            return json.load(f)
        
    def write(self, data):
        "Write python object to JSON file"
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
        
    def append(self, data):
        "Append python object to JSON file"
        with open(self.file_path, 'a') as f:
            json.dump(data, f)
        
    def format(self):
        "Format JSON file"
        data = self.read()
        self.write(json.dumps(data, indent=4))