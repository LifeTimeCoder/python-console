from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from screens import SearchScreen, SearchType





class LineageApplication(App):
    
    
    BINDINGS = [("p", "search_screen", "Pipelines")]
    CSS_PATH="lineageui.tcss"
    
    
    
    def compose(self)->ComposeResult:
        yield Header()
        yield Footer()
    def on_mount(self):
        self.title = "DataOps Lineage Information"
  
  
    def action_pipeline(self):
        self.screen
        
    def action_search_screen(self):
        self.push_screen(SearchScreen(SearchType.PIPELINE_TO_PIPELINE))
        
        
        
        
        
        
        
        
        
        
        
        
if __name__ == "__main__":
    app = LineageApplication()
    app.run()