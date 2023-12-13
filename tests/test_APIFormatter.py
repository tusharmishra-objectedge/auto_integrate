import pytest
from unittest.mock import patch
from auto_integrate_cli.api_formatter.base import APIFormatter


@pytest.fixture
def sample_return_obj():
    return {
        "api1": {
            "type": "json_api",
            "url": "https://jsonplaceholder.typicode.com/todos/1",
        },
        "api2": {"type": "json_dict", "data": [{"key": "value"}]},
    }


@pytest.fixture
def sample_return_obj_with_doc_website():
    return {
        "api1": {"type": "none", "doc_website": "https://www.google.com"},
        "api2": {"type": "none", "doc_website": "https://www.google.com"},
    }


class TestAPIFormatter:
    @patch("requests.get")
    def test_get_json_api_successful(self, mock_get, sample_return_obj):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "userId": 1,
                "id": 1,
                "title": "delectus aut autem",
                "completed": False,
            }
        ]

        api_formatter = APIFormatter(sample_return_obj)
        result = api_formatter.get_json_api(url)
        assert result == {
            "userId": {"type": "int", "sample_value": 1},
            "id": {"type": "int", "sample_value": 1},
            "title": {"type": "str", "sample_value": "delectus aut autem"},
            "completed": {"type": "bool", "sample_value": False},
        }

    @patch("requests.get")
    def test_get_json_api_failure(self, mock_get, sample_return_obj):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        mock_get.return_value.status_code = 404

        api_formatter = APIFormatter(sample_return_obj)
        result = api_formatter.get_json_api(url)
        assert result == {}

    def test_get_json_dict(self, sample_return_obj):
        data = [{"key": "value"}]
        api_formatter = APIFormatter(sample_return_obj)
        result = api_formatter.get_json(data)
        assert result == {"key": {"type": "str", "sample_value": "value"}}

    @patch("auto_integrate_cli.api_formatter.base.extract")
    def test_extract(self, mock_extract, sample_return_obj_with_doc_website):
        mock_extract.return_value = {"autogen": "mapping"}

        api_formatter = APIFormatter(sample_return_obj_with_doc_website)
        result = api_formatter.format()

        expected_result = {
            "api1": {"autogen": "mapping"},
            "api1Fields": {},
            "api2": {"autogen": "mapping"},
            "api2Fields": {},
        }
        assert result == expected_result
