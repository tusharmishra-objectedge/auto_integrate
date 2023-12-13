from datetime import datetime


class LogHandler:
    def __init__(self, log_file):
        """
        Initialize the LogHandler class

        This function initializes the LogHandler class with a file path.
        Gets the directory of the file from settings.
        """
        self.log_file = log_file

    def createLogFile(self):
        with open(self.log_file, "w+") as f:
            f.write("Log File created at: ")
            f.write(str(datetime.now()))
            f.write("\n\n")

    def append(self, data):
        with open(self.log_file, "a+") as f:
            f.write("----------------------------------------\n")
            f.write(str(datetime.now()) + "\n")
            f.write(data)
            f.write("\n\n")
