import glob

import rich
from devtools import debug
from flask import Flask
from typer import Typer

from pagic.pagic import Pagic

cli = Typer()


@cli.command()
def serve(scandir: str = "pages"):
    """Run the development server."""
    debug(scandir)

    app = Flask(__name__)
    Pagic(app)

    Scanner(app, scandir)
    return
    # app.run()


@cli.command()
def hello():
    rich.print("Hello, world!")


class Scanner:
    def __init__(self, app, scandir):
        self.app = app
        self.scandir = scandir

    def scan(self):
        """Scan the `pages` directory."""
        rich.print(f"[green]Scanning {self.scandir} directory...[/green]")

        paths = glob.glob(f"{self.scandir}/**", recursive=True)
        for path in paths:
            if path.endswith(".py"):
                self.register_python_module(path)
            elif path.endswith(".html"):
                self.register_html_file(path)

    def register_python_module(self, path):
        route_path = path[len(self.scandir) :]
        debug(route_path)

        module_name = path[:-3].replace("/", ".")
        module = __import__(module_name)
        for name in module_name.split(".")[1:]:
            module = getattr(module, name)
        self.app.register_blueprint(module)

    def register_html_file(self, path):
        route_path = path[len(self.scandir) :]
        debug(route_path)

        # self.app.add_url_rule(route_path, route_path, lambda: render_file(path))


def render_file(path):
    with open(path) as f:
        return f.read()


if __name__ == "__main__":
    cli()
