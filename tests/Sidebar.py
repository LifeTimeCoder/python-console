"""
A simple animated sidebar.

See comments for details.

"""

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Footer, Label, Header, RadioSet, RadioButton

TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."""


class Sidebar(Widget):
    DEFAULT_CSS = """
    Sidebar {
        width: 30;
        /* Needs to go in its own layer to sit above content */
        layer: sidebar; 
        /* Dock the sidebar to the appropriate side */
        dock: left;
        /* Offset x to be -100% to move it out of view by default */
        offset-x: -100%;

        background: $primary;
        border-right: vkey $background;    

        /* Enable animation */
        transition: offset 200ms;
        
        &.-visible {
            /* Set offset.x to 0 to make it visible when class is applied */
            offset-x: 0;
        }

        & > Vertical {
            margin: 1 2;
        }
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Label("Filters")
                with RadioSet(id="region_filters"):
                    yield RadioButton("op-eu-production")
            

class LineageApplication(App):
    """
    Test app to show our sidebar.
    """
    ENABLE_COMMAND_PALETTE= False
    DEFAULT_CSS = """
    Screen {    
        layers: sidebar;
    }

    """

    BINDINGS = [("s", "toggle_sidebar", "Toggle Sidebar")]

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True,name="LineageHeader",id="LineageHeader",)
        yield Sidebar()
        yield Label(TEXT)
        yield Footer()
        
        
    def on_mount(self) -> None:
        """Set the sidebar to be visible."""
        self.title = "Lineage"
    
    def action_toggle_sidebar(self) -> None:
        """Toggle the sidebar visibility."""
        self.show_sidebar = not self.show_sidebar

    def watch_show_sidebar(self, show_sidebar: bool) -> None:
        """Set or unset visible class when reactive changes."""
        self.query_one(Sidebar).set_class(show_sidebar, "-visible")


if __name__ == "__main__":
    app = LineageApplication()
    app.run()
