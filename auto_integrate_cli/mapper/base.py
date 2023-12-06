class BaseMapper:
    def __init__(self, api1, api2, logger=None):
        self.api1 = api1
        self.api2 = api2
        self.logger = logger

    def map(self):
        pass
