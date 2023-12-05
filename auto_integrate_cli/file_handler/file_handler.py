class FileHandler:
    def __init__(self, input_file, output_file=None, logger=None):
        """
        Initialize the FileHandler class

        This function initializes the FileHandler class with a file path.
        Gets the directory of the file from settings
        """
        self.input_file = input_file
        self.output_file = output_file
        self.logger = logger

    def read(self):
        if self.logger:
            self.logger.append(f"Reading file at path: {self.input_file}")

        with open(self.input_file) as f:
            return f.read()

    def write(self, data):
        if self.logger:
            self.logger.append(f"Writing to file at path: {self.output_file}")
        with open(self.output_file, "w") as f:
            f.write(data)

    def append(self, data):
        if self.logger:
            self.logger.append(f"Appending to file at path: {self.output_file}")
        with open(self.output_file, "a") as f:
            f.write(data)
