from enum import Enum
from textual.screen import Screen
from textual.widgets import Input, ListView, ListItem, Header,Footer,Label
from textual.app import ComposeResult
from testdata import data


class SearchType(Enum):
    PIPELINE_TO_PIPELINE=0
    PIPELINE_TO_TABLE=1
    TABLE_TO_TABLE=2
    


class SearchScreen(Screen):
    def __init__(self, search_type: SearchType):
        super().__init__();
        self.screen_type = search_type
        
    def compose(self) -> ComposeResult:
    
        self.text_box = Input(placeholder="Search...")
        self.header= Header(name="Search")
        self.footer=Footer()
        self.list_view = ListView()
        yield self.header
        yield self.text_box
        yield self.list_view
        yield self.footer

    async def on_mount(self) -> None:
        self.text_box.focus()
        self.searchitems=data['City']
        await self.loadlistbox(self.searchitems)
    
    async def loadlistbox(self, searchitems):
            self.list_view.clear()
            for item in searchitems:
                self.list_view.append(ListItem(Label(item)))
                                  
    async def on_input_changed(self, message: Input.Changed) -> None:
        search_text = message.value
        print(search_text)
        # Perform search logic here and update list_view
        results = self.perform_search(search_text)
        self.update_list_view(results)

    def perform_search(self, search_text: str):
        # Dummy search logic, replace with actual search
        return [item for item in self.searchitems if search_text.lower() in item.lower()] 

    def update_list_view(self, results):
        self.list_view.clear()
        for result in results:
             self.list_view.append(ListItem(Label(result)))