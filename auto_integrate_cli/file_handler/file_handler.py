class FileHandler:
    def __init__(self, input_file, output_file):
        """
        Initialize the FileHandler class

        This function initializes the FileHandler class with a file path.
        Gets the directory of the file from settings
        """
        self.input_file = input_file
        self.output_file = output_file

    def read(self):
        with open(self.input_file) as f:
            return f.read()

    def write(self, data):
        with open(self.output_file, "w") as f:
            f.write(data)

    def append(self, data):
        with open(self.output_file, "a") as f:
            f.write(data)
