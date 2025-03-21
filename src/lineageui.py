from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class LineageApplication(App):
    CSS_PATH="lineageui.tcss"
    def compose(self)->ComposeResult:
        yield Header(name="DataOps Lineage Information")
        yield Footer()
    def on_mount(self):
        self.title = "DataOps Lineage Information"

if __name__ == "__main__":
    app = LineageApplication()
    app.run()