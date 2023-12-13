import requests
import json
from datetime import datetime
from dateutil import parser

from auto_integrate_cli.settings.default import (
    PIPELINE_CONCAT_DEFAULT,
    PIPELINE_CONDITION_DEFAULT,
    PIPELINE_NUMBER,
)

from auto_integrate_cli.file_handler.json_handler import JSONHandler


class Pipeline:
    """
    Pipeline
    Uses mapping to map data from api1 to api2 and generate pipeline.
    Applies appropriate transformations and conditions. GETs data from api1 and POSTs to api2.
    """

    def __init__(self, api1URL, api2URL, mapping, logger=None):
        self.api1URL = api1URL
        self.api2URL = api2URL
        self.mapping = mapping
        self.mapped_data = None
        self.logger = logger

    def map_data(self, num_of_records=None):
        """
        map_data

        This function maps uses the mapping to change api1 data to fields necessary for api2.
        Uses get_data_from_api method to get data from api1.

        Parameters:
            num_of_records (int): The number of items to get from api1

        Returns:
            dict: api1 data mapped to api2 fields
        """

        dataAPI1 = self.get_data_from_api(num_of_records)
        if self.logger:
            self.logger.append(
                f"Got {len(dataAPI1)} records from {self.api1URL}"
            )

        mapped_data = []

        if self.logger:
            self.logger.append(
                f"Mapping {len(dataAPI1)} records from {self.api1URL}"
            )
        for datum in dataAPI1:
            mapped_datum = {}
            for targetKey in self.mapping.keys():
                try:
                    sourceFields = self.mapping[targetKey]["source_fields"]
                except KeyError:
                    sourceFields = []

                # Check conditions, if applied, source fields will be conditionVal
                if "conditions" in self.mapping[targetKey]:
                    conditions = self.mapping[targetKey]["conditions"]
                    if conditions:
                        conditionVal = self.handleConditions(
                            conditions, sourceFields
                        )
                        if conditionVal != PIPELINE_CONDITION_DEFAULT:
                            sourceFields = [conditionVal]

                transformation = self.mapping[targetKey]["transformation"]

                if transformation == "toDateTime":
                    api1DateTimeFormat = self.mapping[targetKey][
                        "api1DateFormat"
                    ]
                    api2DateTimeFormat = self.mapping[targetKey][
                        "api2DateFormat"
                    ]
                    transformedValue = self.applyTransformation(
                        transformation,
                        sourceFields,
                        datum,
                        api1DateTimeFormat,
                        api2DateTimeFormat,
                    )
                else:
                    transformedValue = self.applyTransformation(
                        transformation, sourceFields, datum
                    )

                mapped_datum[targetKey] = transformedValue
            mapped_data.append(mapped_datum)
        self.mapped_data = mapped_data
        return self.mapped_data

    def applyTransformation(
        self,
        transformation,
        sourceFields,
        datum,
        api1DateTimeFormat=None,
        api2DateTimeFormat=None,
    ):
        """
        applyTransformation

        This function applies the transformation to the source fields and returns the transformed value.

        Parameters:
            transformation (str): The transformation to apply
            sourceFields (list): The source fields
            datum (dict): The datum
            api1DateTimeFormat (str): The API1 datetime format
            api2DateTimeFormat (str): The API2 datetime format

        Returns:
            any: transformed value

        """
        if transformation == "none":
            # No transformation
            transformedValue = datum[sourceFields[0]]
            return transformedValue

        elif transformation == "toInt":
            # Convert to int
            transformedValue = int(datum[sourceFields[0]])
            return transformedValue

        elif transformation == "toFloat":
            # Convert to float
            transformedValue = float(datum[sourceFields[0]])
            return transformedValue

        elif transformation == "toString":
            # Convert to string
            transformedValue = str(datum[sourceFields[0]])
            return transformedValue

        elif transformation == "toDateTime":
            # Convert to datetime
            sourceDateTimeFormat = api1DateTimeFormat
            targetDateTimeFormat = api2DateTimeFormat

            # Convert API1 date to datetime object
            dateString = datum[sourceFields[0]]
            # No conversion necessary if same date format
            if api1DateTimeFormat == api2DateTimeFormat:
                return str(dateString)

            # Convert to datetime object
            try:
                dateObject = datetime.strptime(
                    dateString, sourceDateTimeFormat
                )
            except ValueError as e:
                print(f"Error converting date string to datetime object: {e}")
                try:
                    if dateString[-1] == "Z":
                        dateObject = datetime.fromisoformat(
                            dateString.replace("Z", "+00:00")
                        )
                    else:
                        dateObject = datetime.fromisoformat(dateString)
                except ValueError as e:
                    print(
                        f"Error {e} converting as ISO: {dateString}, using dateutil parser"
                    )
                    dateObject = parser.isoparse(dateString)

            try:
                convertedDateObject = dateObject.strftime(targetDateTimeFormat)
                # print('Success converting datetime object to target format')
            except Exception as e:
                print(f"Error converting datetime object to string: {e}")
                convertedDateObject = str(dateObject)
            transformedValue = str(convertedDateObject)
            return transformedValue

        elif transformation == "toBool":
            # Convert to bool
            transformedValue = bool(datum[sourceFields[0]])
            return transformedValue

        elif transformation == "toObject":
            # Convert to object
            transformedValue = json.loads(datum[sourceFields[0]])
            return transformedValue

        elif transformation == "toList":
            # Convert to list
            transformedValue = [
                elem.strip() for elem in datum[sourceFields[0]].split(",")
            ]
            return transformedValue

        elif transformation == "toSubstr":
            # Grab source field from datum and substring it
            # todo: check substring conditions
            sourceField = sourceFields[0]
            transformedValue = datum[sourceField[:]]
            return transformedValue

        elif transformation == "toConcat":
            # Grab source fields from datum and concatenate them
            fieldsToConcat = []
            for field in sourceFields:
                fieldsToConcat.append(datum[field])
            transformedValue = PIPELINE_CONCAT_DEFAULT.join(fieldsToConcat)
            return transformedValue

    def handleConditions(self, conditions, sourceFields):
        """
        handleConditions

        This function handles the conditions and returns the appropriate value.
        If a condition applies, appropriate value will be returned, else PIPELINE_CONDITION_DEFAULT will be returned
        If more than one condition, we assume the last condition has highest priority

        Parameters:
            conditions (list): The conditions
            sourceFields (any): The source field

        Returns:
            any: The appropriate value or PIPELINE_CONDITION_DEFAULT
        """

        # Initialize returnVal to default
        # If a condition applies, returnVal will be changed appropriately, else default will be returned
        # If more than one condition, assuming last condition has highest priority
        returnVal = PIPELINE_CONDITION_DEFAULT

        for cond in conditions:
            condition = cond["condition"]
            fallback = cond["fallback"]

            if condition == "ifNull":
                if (
                    sourceFields is None
                    or sourceFields == "none"
                    or not sourceFields
                ):
                    returnVal = fallback
            elif condition == "ifEmpty":
                if (
                    sourceFields is None
                    or sourceFields == "none"
                    or sourceFields == ""
                    or not sourceFields
                ):
                    returnVal = fallback
            elif condition == "ifWrongFormat":
                returnVal = PIPELINE_CONDITION_DEFAULT
            elif condition == "isPrimary":
                try:
                    primary = fallback
                except TypeError:
                    primary = sourceFields[0]

                returnVal = primary

        return returnVal

    def get_data_from_api(self, num=None):
        """
        Get Data from API
        Returns an array of dictionaries from the API.

        Parameters:
            apiURL (str): The URL of the API
            num (int): The number of records to return

        Returns:
            list: The data from the API
        """
        try:
            response = requests.get(self.api1URL)

            if response.status_code == 200:
                data = response.json()
                # todo:handle nums with params to request instead of getting all the data
                if num is not None:
                    data = data[:num]

                return data
            else:
                if self.logger:
                    self.logger.append(
                        f"Error getting data from {self.api1URL}: {response.status_code}"
                    )
                print(
                    f"Error getting data from {self.api1URL}: {response.status_code}"
                )
        except Exception as e:
            if self.logger:
                self.logger.append(
                    f"Error getting data from {self.api1URL}: {e}"
                )
            print(f"Error getting data from {self.api1URL}: {e}")
            return None

    def generate_pipeline(self):
        """
        Generate Pipeline

        This function generates the pipeline.
        Uses GET requests to get the data from api1 and POST to api2.

        Parameters:
            mappedData (dict): The mapped data
            api2URL (str): The URL of the second API

        Returns:
            int: Number of records processed
        """
        if self.logger:
            self.logger.append(
                f"Generating pipeline for {len(self.mapped_data)} records from \n{self.api1URL} \nto \n{self.api2URL}"
            )

        for item in self.mapped_data:
            try:
                response = requests.post(self.api2URL, json=item)
                if response.status_code == 200 or response.status_code == 201:
                    if self.logger:
                        self.logger.append(f"POST OK: \n{item}")
                    print(f"POST to {self.api2URL}: OK")
                else:
                    if self.logger:
                        self.logger.append(
                            f"POST ERROR {response.status_code} \n{self.api2URL} \n{item}"
                        )
                    print(
                        f"POST to {self.api2URL}: ERROR {response.status_code}"
                    )
                    return 0
            except Exception as e:
                if self.logger:
                    self.logger.append(
                        f"POST ERROR {e} \n{self.api2URL} \n{item}"
                    )
                print(f"POST to {self.api2URL}: ERROR {e}")
                return 0


if __name__ == "__main__":
    # mapping_path = '../../demo/pipelineTest.json'
    mapping_path = "../../demo/mappingTestMock.json"

    jsonHandler = JSONHandler(mapping_path)
    dataSFURL = "https://651313e18e505cebc2e98c43.mockapi.io/DataSF"
    HubSpotURL = "https://651313e18e505cebc2e98c43.mockapi.io/HubspotCompany"
    studentsURL = "https://651313e18e505cebc2e98c43.mockapi.io/pupils"
    pupilsURL = "https://651313e18e505cebc2e98c43.mockapi.io/students"

    mapping = jsonHandler.read()
    mapping = mapping["mapped"]

    pipeline = Pipeline(studentsURL, pupilsURL, mapping)
    pipeline.map_data(PIPELINE_NUMBER)
    print(pipeline.mapped_data)
    # pipeline.generate_pipeline()
