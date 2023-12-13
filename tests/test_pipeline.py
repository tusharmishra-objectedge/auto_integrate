import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from auto_integrate_cli.pipeline.pipeline import Pipeline
from auto_integrate_cli.settings.default import PIPELINE_CONDITION_DEFAULT


@pytest.fixture
def sample_mapping():
    return {
        "target_field1": {
            "source_fields": ["source_field1"],
            "transformation": "none",
        },
        "target_field2": {
            "source_fields": ["source_field2"],
            "transformation": "toString",
        },
    }


class TestPipeline:
    api1_url = "http://example.com/api1"
    api2_url = "http://example.com/api2"
    pipeline = Pipeline(api1_url, api2_url, {})

    @patch("auto_integrate_cli.pipeline.pipeline.requests.get")
    def test_get_data_from_api(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ]
        mock_requests_get.return_value = mock_response

        # Act
        result = self.pipeline.get_data_from_api(num=2)

        # Assert
        assert result == [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ]
        mock_requests_get.assert_called_once_with(self.api1_url)

    @patch("auto_integrate_cli.pipeline.pipeline.requests.post")
    def test_generate_pipeline(self, mock_requests_post):
        self.pipeline.mapping = {
            "target_field": {
                "source_fields": ["source_field"],
                "transformation": "none",
            }
        }

        self.pipeline.mapped_data = [
            {"target_field": "value1"},
            {"target_field": "value2"},
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_post.return_value = mock_response

        # Act
        result = self.pipeline.generate_pipeline()

        # Assert
        assert result == 2
        expected_calls = [
            ((self.api2_url,), {"json": {"target_field": "value1"}}),
            ((self.api2_url,), {"json": {"target_field": "value2"}}),
        ]
        mock_requests_post.assert_has_calls(expected_calls, any_order=True)

    @patch.object(
        Pipeline,
        "get_data_from_api",
        return_value=[{"source_field1": "value1", "source_field2": "value2"}],
    )
    def test_map_data(self, mock_api_formatter_format, sample_mapping):
        # Arrange
        self.pipeline.mapping = sample_mapping

        # Act
        result = self.pipeline.map_data(num_of_records=2)

        # Assert
        assert result == [
            {"target_field1": "value1", "target_field2": "value2"}
        ]
        mock_api_formatter_format.assert_called_once()

    def test_handle_conditions_if_null(self):
        conditions = [{"condition": "ifNull", "fallback": "fallback_value"}]
        source_field = None

        result = self.pipeline.handleConditions(conditions, source_field)

        assert result == "fallback_value"

    def test_handle_conditions_if_null_with_value(self):
        conditions = [{"condition": "ifNull", "fallback": "fallback_value"}]
        source_field = "value"

        result = self.pipeline.handleConditions(conditions, source_field)

        assert result == PIPELINE_CONDITION_DEFAULT

    def test_handle_conditions_isEmpty(self):
        conditions = [{"condition": "ifEmpty", "fallback": "fallback_value"}]
        source_field = ""

        result = self.pipeline.handleConditions(conditions, source_field)

        assert result == "fallback_value"

    def test_handle_conditions_isEmpty_with_value(self):
        conditions = [{"condition": "ifEmpty", "fallback": "fallback_value"}]
        source_field = "value"

        result = self.pipeline.handleConditions(conditions, source_field)

        assert result == PIPELINE_CONDITION_DEFAULT

    def test_handle_conditions_isWrongFormat(self):
        conditions = [
            {"condition": "isWrongFormat", "fallback": "fallback_value"}
        ]
        source_field = "value"

        result = self.pipeline.handleConditions(conditions, source_field)

        assert result == PIPELINE_CONDITION_DEFAULT

    def test_handle_conditions_isPrimary(self):
        conditions = [{"condition": "isPrimary", "fallback": "fallback_value"}]
        source_field = "value"

        result = self.pipeline.handleConditions(conditions, source_field)

        assert result == "fallback_value"

    def test_applyTransformation_none(self):
        datum = {"source_field": "value"}
        transformation = "none"
        source_fields = ["source_field"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result == "value"

    def test_applyTransformation_toInt(self):
        datum = {"source_fields": "42"}
        transformation = "toInt"
        source_fields = ["source_fields"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result == 42

    def test_applyTransformation_toFloat(self):
        datum = {"source_fields": "42.3"}
        transformation = "toFloat"
        source_fields = ["source_fields"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result == 42.3

    def test_applyTransformation_toString(self):
        datum = {"source_fields": 42}
        transformation = "toString"
        source_fields = ["source_fields"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result == "42"

    @patch("auto_integrate_cli.pipeline.pipeline.datetime")
    @patch("auto_integrate_cli.pipeline.pipeline.parser")
    def test_applyTransformation_toDateTime_same_format(
        self, mock_parser, mock_datetime
    ):
        # Arrange
        pipeline_instance = Pipeline(
            "http://example.com/api1", "http://example.com/api2", {}
        )
        datum = {"source_fields": "2023-01-01T12:34:56.789Z"}
        transformation = "toDateTime"
        source_fields = ["source_fields"]

        API1_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        API2_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

        mock_datetime.strptime.return_value = datetime(
            2023, 1, 1, 12, 34, 56, 789000
        )

        # Act
        result = pipeline_instance.applyTransformation(
            transformation,
            source_fields,
            datum,
            API1_DATE_FORMAT,
            API2_DATE_FORMAT,
        )

        # Assert
        assert result == "2023-01-01T12:34:56.789Z"

    @patch("auto_integrate_cli.pipeline.pipeline.datetime")
    @patch("auto_integrate_cli.pipeline.pipeline.parser")
    def test_applyTransformation_toDateTime_different_format(
        self, mock_parser, mock_datetime
    ):
        # Arrange
        pipeline_instance = Pipeline(
            "http://example.com/api1", "http://example.com/api2", {}
        )
        datum = {"source_fields": "2023-01-01T12:34:56.789Z"}
        transformation = "toDateTime"
        source_fields = ["source_fields"]

        API1_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        API2_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

        mock_datetime.strptime.return_value = datetime(
            2023, 1, 1, 12, 34, 56, 789000
        )

        # Act
        result = pipeline_instance.applyTransformation(
            transformation,
            source_fields,
            datum,
            API1_DATE_FORMAT,
            API2_DATE_FORMAT,
        )

        # Assert
        assert result == "2023-01-01 12:34:56"

    def test_applyTransformation_toBool(self):
        datum = {"source_fields": "true"}
        transformation = "toBool"
        source_fields = ["source_fields"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result

    def test_applyTransformation_toObject(self):
        datum = {"source_fields": '{"key": "value"}'}
        transformation = "toObject"
        source_fields = ["source_fields"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result == {"key": "value"}

    def test_applyTransformation_toList(self):
        datum = {"source_fields": "value1, value2, value3"}
        transformation = "toList"
        source_fields = ["source_fields"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result == ["value1", "value2", "value3"]

    def test_applyTransformation_toSubstr(self):
        datum = {"source_fields": "value1"}
        transformation = "toSubstr"
        source_fields = ["source_fields"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result == "value1"

    def test_applyTransformation_toConcat(self):
        datum = {"source_fields": "value1", "sf2": "value2"}
        transformation = "toConcat"
        source_fields = ["source_fields", "sf2"]

        result = self.pipeline.applyTransformation(
            transformation, source_fields, datum
        )

        assert result == "value1 value2"
