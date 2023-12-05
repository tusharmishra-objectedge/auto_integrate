import argparse
import os
import requests

from auto_integrate_cli.settings.default import DEFAULT_CWD

from auto_integrate_cli.file_handler.json_handler import JSONHandler
from auto_integrate_cli.file_handler.log_handler import LogHandler
from auto_integrate_cli.api_formatter.base import APIFormatter

# Mappers
from auto_integrate_cli.mapper.mappings import mappings, map_autogen

# Pipeline
from auto_integrate_cli.pipeline.pipeline import Pipeline


def get_args():
    """
    Get command line arguments

    This function uses argparse to parse command line arguments and
    returns an argparse object.

    The arguments are for 2 api files, 2 formats, and 1 output file:
    -i: input file
    -o : output file

    Parameters:
        None

    Returns:
        argparse object: The parsed arguments from the command line
    """
    parser = argparse.ArgumentParser(
        description="API Formatter",
    )
    parser.add_argument(
        "-i", "--input-file", help="Input file", required=True, type=str
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="Output file",
        required=False,
        type=str,
        default="output.txt",
    )
    return parser.parse_args()


def main():
    """
    Main function

    This function is the main function of the script. It uses the
    argparse object to get the command line arguments. It then uses
    the APIFormatter class to format the API data and write it to
    the output file.

    Parameters:
        None

    Returns:
        None
    """
    args = get_args()
    input_file = os.path.join(DEFAULT_CWD, args.input_file)
    output_file = os.path.join(DEFAULT_CWD, args.output_file)

    # Logger
    logsPath = "logs"
    if not os.path.exists(logsPath):
        os.makedirs(logsPath)
    logger = LogHandler("logs/logs.txt")
    logger.createLogFile()

    print(f"\nReading input file at path: {input_file} ...\n")
    file_handler = JSONHandler(input_file, output_file, logger)
    inputs = file_handler.read()

    if not inputs["api1"] or not inputs["api2"]:
        print("API1 or API2 is empty. Exiting...")
        return


    api1URL = inputs["api1"]["url"]
    api2URL = inputs["api2"]["url"]

    api_formatter = APIFormatter(inputs, logger)

    api1, api2 = api_formatter.format()

    documentScraperOutput = {"api1": api1, "api2": api2}

    file_handler.output_file = "documentScraperOutput.json"
    file_handler.write(documentScraperOutput)
    print('Wrote document scraper output to documentScraperOutput.json')

    file_handler.output_file = output_file

    output_obj = map_autogen(api1, api2, logger)
    print(f"\nWriting output file at path: {output_file} ...\n")
    file_handler.write(output_obj)

    mapping = output_obj["mapped"]

    pipeline = Pipeline(api1URL, api2URL, mapping, logger)
    mapped_data = pipeline.map_data(10)
    for datum in mapped_data:
        print(datum)
    pipeline.generate_pipeline()


if __name__ == "__main__":
    main()
