import logging


class BaseMapper:
    """
    Base class for all mappers.
    """

    def __init__(self, api1, api2):
        """
        Initialize the BaseMapper class.

        This function initializes the BaseMapper class with two APIs.

        Parameters:
            api1: api1 from api_formatter
            api2: api2 from api_formatter

        Returns: None
        """
        logging.info("Initializing BaseMapper")
        self.api1 = api1
        self.api2 = api2

    def map(self):
        """
        Abstract method to map two APIs.
        """
        pass
