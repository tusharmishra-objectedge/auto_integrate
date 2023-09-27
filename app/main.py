import argparse
import os

from settings.default import DEFAULT_CWD

from file_handler.json_handler import JSONHandler
from api_formatter.base import APIFormatter

# Mappers
from mapper.mappings import mappings

def get_args():
    """
    Get command line arguments

    This function uses argparse to parse command line arguments and returns an argparse object.
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
        "-i",
        "--input-file",
        help="Input file",
        required=True,
        type=str
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="Output file",
        required=False,
        type=str,
        default="output.txt"
    )
    return parser.parse_args()


def main():
    """
    Main function

    This function is the main function of the script. It uses the argparse object to get the command line arguments.
    It then uses the APIFormatter class to format the API data and write it to the output file.

    Parameters:
        None

    Returns:
        None
    """
    args = get_args()
    input_file = os.path.join(DEFAULT_CWD, args.input_file)
    print(f"\nReading input file at path: {input_file} ...\n")
    file1 = JSONHandler(input_file)
    inputs = file1.read()
    # print(inputs)

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()

    print(f"\n API 1: {api1}\n")
    print(f"API 2: {api2}\n")

    # print("Mapping API 1 to API 2 ...\n")
    # print("Manual mapping ...\n")
    # print(f"L2R: \n {inputs['manual_map']['L2R']}\n")
    # print(f"R2L: \n {inputs['manual_map']['R2L']}\n")

    mappings(api1, api2, inputs['manual_map']['L2R'], inputs['manual_map']['R2L'])

    # api_formatter.write(args.output_file)


if __name__ == "__main__":
    main()