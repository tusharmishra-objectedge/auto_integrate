from .file_handler import FileHandler
import json


class JSONHandler(FileHandler):
    def __init__(self, input_file, output_file=None, logger=None):
        """
        Initialize the JSONHandler class

        This function initializes the JSONHandler class with a file path.
        Gets the directory of the file from settings
        """
        super().__init__(input_file, output_file, logger)

    def read(self):
        "Read python object from JSON file"
        if self.logger:
            self.logger.append(f"Reading JSON file at path: {self.input_file}")
        with open(self.input_file) as f:
            return json.load(f)

    def write(self, data):
        "Write python object to JSON file"
        if self.logger:
            self.logger.append(
                f"Writing JSON file at path: {self.output_file}"
            )
        with open(self.output_file, "w+") as f:
            json.dump(data, f, indent=4)
            f.write("\n")

    def append(self, data):
        if self.logger:
            self.logger.append(
                f"Appending JSON file at path: {self.output_file}"
            )
        "Append python object to JSON file"
        with open(self.output_file, "a") as f:
            json.dump(data, f)

    def format(self):
        "Format JSON file"
        if self.logger:
            self.logger.append(
                f"Formatting JSON file at path: {self.output_file}"
            )
        data = self.read()
        self.write(json.dumps(data, indent=4))
