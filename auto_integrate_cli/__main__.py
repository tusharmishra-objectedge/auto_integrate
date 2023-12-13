import logging
import argparse
import os
<<<<<<< HEAD
import pytest
=======
>>>>>>> 1a1e82e (docs(app): add docs and enhanced logging)

from auto_integrate_cli.settings.default import DEFAULT_CWD, COVERAGE_THRESHOLD
from auto_integrate_cli.settings.log_config import setup_logging
from auto_integrate_cli.file_handler.json_handler import JSONHandler
from auto_integrate_cli.api_formatter.base import APIFormatter
<<<<<<< HEAD

from auto_integrate_cli.text_user_interface.textual_ui import VerificationApp

# Mappers
from auto_integrate_cli.mapper.mappings import map_autogen

# Pipeline
=======
from auto_integrate_cli.text_user_interface.textual_ui import VerificationApp
from auto_integrate_cli.mapper.mappings import map_autogen
>>>>>>> 1a1e82e (docs(app): add docs and enhanced logging)
from auto_integrate_cli.pipeline.pipeline import Pipeline

setup_logging()


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
    parser.add_argument(
        "--runTests",
        action="store_true",
        help="Run all unit tests",
        required=False,
    )

    return parser.parse_args()


def run_tests():
    test_path = "tests"
    pytest.main([test_path])


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
    test_path = "tests"

    if args.runTests:
        logging.info(f"Running tests at path: {test_path}.")
        print(f"Running tests at path: {test_path}.")
        run_tests()
        exit(0)

    # Read Inputs
    logging.info(f"Reading input file at path: {input_file}.")
    print(f"Reading input file at path: {input_file}.")
    file_handler = JSONHandler(input_file, output_file)
    inputs = file_handler.read()

    if not inputs.get("api1") or not inputs.get("api2"):
        logging.error("API1 or API2 is empty. Exiting.")
        return

    api1URL = inputs["api1"]["url"]
    api2URL = inputs["api2"]["url"]

    # Format APIs
    api_formatter = APIFormatter(inputs)

    apiDetailsDict = api_formatter.format()
    api1 = apiDetailsDict["api1"]
    api1Fields = apiDetailsDict["api1Fields"]
    api2 = apiDetailsDict["api2"]
    api2Fields = apiDetailsDict["api2Fields"]

    documentScraperOutput = {
        "api1": api1,
        "api1Fields": api1Fields,
        "api2": api2,
        "api2Fields": api2Fields,
    }

    documentScraperFilePath = (
        "demo/extractOutput/"
        + input_file.split("/")[-1].split(".")[0]
        + "ExtractOutput.json"
    )

    file_handler.output_file = documentScraperFilePath
    file_handler.write(documentScraperOutput)
    logging.info(
        "Wrote document scraper output to documentScraperAPITest.json"
    )

    file_handler.output_file = output_file

    # Mapping
    output_obj = map_autogen(api1, api2)
    logging.info(f"Writing output file at path: {output_file}.")
    file_handler.write(output_obj)

    mapping = output_obj["mapped"]

    # Coverage Stats
    api2FieldCount = len(api2Fields)
    coverageDict = {field: False for field in api2Fields}

    coverage = 0
    for field in mapping:
        if field in api2Fields:
            coverageDict[field] = True
            coverage += 1

    coverage = coverage / api2FieldCount
    print()
    print(f"Coverage: {coverage}")
    for field in coverageDict:
        print(f"{field}: {coverageDict[field]}")
    print()

    logging.info(f"Coverage Details: {coverageDict}")
    logging.info(f"Coverage: {coverage}")

    if coverage > COVERAGE_THRESHOLD:
        # Verify with user
        logging.info(
            f"Coverage is greater than {COVERAGE_THRESHOLD}. \
                Prompting User for verification."
        )

        verifyApp = VerificationApp(mapping)
        answers = verifyApp.run()

        correct = 0
        total = len(answers)

        for value in answers.values():
            if value:
                correct += 1

        print(
            f"\nYou verified {correct} out of {total} mappings as correct!\n"
        )
        logging.info(str(answers))
        logging.info(f"Verified {correct} out of {total} mappings as correct!")

        pipeline = Pipeline(api1URL, api2URL, mapping)
        pipeline.map_data(10)

        # Generate Pipeline
        if correct == total:
            logging.info("All mappings verified as correct!")
            print("Generating Pipeline...")
            pipeline = Pipeline(api1URL, api2URL, mapping)
            pipeline.map_data(10)

            pipeline.generate_pipeline()
        else:
            print(
                "Please verify all mappings as correct to generate pipeline."
            )


if __name__ == "__main__":
    main()
