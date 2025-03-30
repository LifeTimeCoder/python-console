from textual.app import App, ComposeResult
from textual.widgets import Tree, Header, Footer


class TreeApp(App):
   
    def compose(self) -> ComposeResult:
        self.header= Header(show_clock=True)
        yield self.header
        yield Footer()
        tree: Tree[str] = Tree("Dune")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
        yield tree
        
    def on_mount(self):
        self.title="DataOps Lineage Information - Pipeline View"

if __name__ == "__main__":
    app = TreeApp()
    app.run()
    