import os
import pytest
import json
from auto_integrate_cli.file_handler.json_handler import JSONHandler


@pytest.fixture
def temp_json_file(tmp_path):
    file_path = tmp_path / "test_file.json"
    return str(file_path)


class TestJSONHandler:
    def test_read(self, temp_json_file):
        json_handler = JSONHandler(input_file=temp_json_file)

        with open(temp_json_file, "w") as f:
            json.dump({"key": "value"}, f)

        content = json_handler.read()
        assert content == {"key": "value"}

    def test_write(self, temp_json_file):
        json_handler = JSONHandler(
            input_file=temp_json_file, output_file=temp_json_file
        )

        json_handler.write({"key": "value"})
        assert os.path.exists(temp_json_file)

        content = json_handler.read()
        assert content == {"key": "value"}

    def test_format(self, temp_json_file):
        json_handler = JSONHandler(
            input_file=temp_json_file, output_file=temp_json_file
        )

        json_handler.write({"key": "value"})
        json_handler.format()

        content = json_handler.read()
        assert content == '{\n    "key": "value"\n}'
