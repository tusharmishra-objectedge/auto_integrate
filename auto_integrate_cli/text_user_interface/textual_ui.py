from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static
from auto_integrate_cli.file_handler.json_handler import JSONHandler

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)


class MappingDetail(Static):
    """A widget to display a mapping."""


class MappingVerification(Static):
    """A widget to display a mapping."""

    def __init__(self, mapping, verifyDict):
        self.mappingString = mapping
        self.verifyDict = verifyDict
        super().__init__()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button pressed events."""
        if event.button.id == "correctButton":
            if self.has_class("incorrectMap"):
                self.remove_class("incorrectMap")
            self.add_class("correctMap")
            buttonField = self.mappingString.split("  --   ")[0]
            self.verifyDict[buttonField] = True
        elif event.button.id == "incorrectButton":
            if self.has_class("correctMap"):
                self.remove_class("correctMap")
            self.add_class("incorrectMap")
            buttonField = self.mappingString.split("  --   ")[0]
            self.verifyDict[buttonField] = False

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Button("Correct", id="correctButton", variant="success")
        yield Button("Incorrect", id="incorrectButton", variant="error")
        yield MappingDetail(self.mappingString)


class VerificationApp(App):
    """Textual app to verify mappings"""

    def __init__(self, mapping):
        self.mapping = mapping
        self.verifyDict = {field: False for field in self.mapping}
        super().__init__()

    CSS_PATH = "verification.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "exit_app", "Exit App"),
    ]
    TITLE = "Mapping Verification"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        for key in self.mapping:
            condition = "No Condition"
            if "conditions" in self.mapping[key]:
                condition = self.mapping[key]["conditions"]
                # for cond in conditionList:
                #     condition += f"condition: {cond['condition']} fallback: {cond['fallback']}\n"

            mappingString = f"{key}  --   {self.mapping[key]['source_fields']}\nTransformation: {self.mapping[key]['transformation']}\nConditions: {condition}\n"
            temp = MappingVerification(mappingString, self.verifyDict)

            yield temp

        yield Button("Verify", id="verifyButton", variant="warning")

        yield Header()
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button pressed events."""
        if event.button.id == "verifyButton":
            self.exit(self.verifyDict)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_exit_app(self) -> None:
        """An action to exit the app."""
        self.exit(self.verifyDict)


if __name__ == "__main__":
    mappingPath = "../../demo/pipelineTest.json"
    mappingFile = JSONHandler(mappingPath, "output.txt")

    mapping = mappingFile.read()
    mapping = mapping["mapped"]

    app = VerificationApp(mapping)
    result = app.run()
    print(result)
