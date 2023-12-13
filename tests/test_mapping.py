from unittest.mock import patch
from auto_integrate_cli.mapper.mappings import map_autogen


class TestMappings:
    @patch("auto_integrate_cli.mapper.mappings.AutogenMapper")
    def test_autogen_map(self, mock_autogen_mapper):
        api1 = {"api1_key": "api1_value"}
        api2 = {"api2_key": "api2_value"}

        mock_instance = mock_autogen_mapper.return_value
        mock_instance.map.return_value = "autogen_result"

        result = map_autogen(api1, api2)

        mock_autogen_mapper.assert_called_once_with(api1, api2, None)

        mock_instance.map.assert_called_once()

        expected_result = {"type": "autogen", "mapped": "autogen_result"}
        assert result == expected_result
