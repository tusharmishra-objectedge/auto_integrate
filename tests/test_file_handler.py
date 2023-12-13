import os
import pytest
from auto_integrate_cli.file_handler.file_handler import FileHandler


@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    return str(file_path)


class TestFileHandler:
    def test_read(self, temp_file):
        file_handler = FileHandler(input_file=temp_file)

        with open(temp_file, "w") as f:
            f.write("test")

        content = file_handler.read()
        assert content == "test"

    def test_write(self, temp_file):
        file_handler = FileHandler(input_file=temp_file, output_file=temp_file)

        file_handler.write("test")
        assert os.path.exists(temp_file)

        content = file_handler.read()
        assert content == "test"

    def test_append(self, temp_file):
        file_handler = FileHandler(input_file=temp_file, output_file=temp_file)

        file_handler.write("test")

        file_handler.append("testAgain")

        content = file_handler.read()

        assert content == "testtestAgain"
