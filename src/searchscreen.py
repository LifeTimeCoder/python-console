from textual import events,binding,on
from textual.app import App, ComposeResult
from textual.widgets import Input, ListView, ListItem, Label,Header,Footer
from textual.containers import Vertical
# from google.cloud import bigquery

class SearchScreen(App):
    """A Textual application with a search box and filtered list from BigQuery."""
    
    CSS = """
    Screen {
        align: center middle;
        layout: vertical;
    }
    Input {
    }
    ListView {
        height: 25;
        overflow: auto;
        padding-left: 1;
    }
    
    Vertical {
        width: 80%;
        align: center middle;
        layout: vertical;
        }
    """
    
    def __init__(self):
        super().__init__()
        self.source_data = []  # Store all cities for filtering
    
    def compose(self) -> ComposeResult:
        self.header=Header()
        self.footer=Footer()
        self.searchbox= Input(placeholder="Type to search...")
        self.searchlistview= ListView()
        yield self.header
        yield self.footer
        yield Vertical(
            self.searchbox, self.searchlistview
        )
    
    async def on_mount(self) -> None:
        """Runs when the app starts, loads cities from BigQuery."""
        self.source_data = await self.fetch_data()
        self.query_one(Input).BINDINGS.append(("down", "move foucs to list", "Move focus to list"))
        await self.update_list("")
        
    
    async def fetch_data(self):
        """Fetch city names from BigQuery and return as a list."""
        # client = bigquery.Client()
        # query = """
        # SELECT DISTINCT city 
        # FROM `bigquery-public-data.geo_us_boundaries.cities` 
        # WHERE city IS NOT NULL
        # ORDER BY city
        # LIMIT 100
        # """
        # query_job = client.query(query)
        # return [row.city for row in query_job.result()]
        return  ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington', 'Boston', 'El Paso', 'Nashville', 'Detroit', 'Oklahoma City','New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington', 'Boston', 'El Paso', 'Nashville', 'Detroit', 'Oklahoma City']
    
    async def update_list(self, filter_text: str):
        """Filters list based on input text."""
        self.searchlistview = self.query_one(ListView)
        self.searchlistview.clear()
        filtered_data = [datatiem for datatiem in self.source_data if filter_text.lower() in datatiem.lower()]
        for city in filtered_data:
            self.searchlistview.append(ListItem(Label(city)))
    
    async def on_input_changed(self, event: Input.Changed):
        """Filters the list as the user types."""
        await self.update_list(event.value)
    
    async def on_input_submitted(self, event: Input.Submitted):
        """Handles Enter key in input box."""
        if event.value.strip():
            self.exit(event.value.strip())  # Return selected city
    
    async def on_list_view_selected(self, event: ListView.Selected):
        """Handles Enter key in list view."""
        selected_item = event.item.query_one(Label).renderable
        self.exit(selected_item)  # Return selected city
        

    async def on_key(self, event: events.Key):
        """Handles down and up key events for swhtching focus between input and listview."""
        if self.searchbox.has_focus:
            if event.key == "down":
                if len(self.searchlistview.children)>0:
                    self.searchlistview.focus()
                    self.searchlistview.index=0
        if self.query_one(ListView).has_focus:
            if (event.key == "up"  and self.searchlistview.index==0):
                self.searchbox.focus()


if __name__ == "__main__":
    
    
    print("ffffffffffffffffffffffffffffffffffffffffffffffffffff")
    app = SearchScreen()
    selected_dataitem = app.run()
    print(f"Selected city: {selected_dataitem}")