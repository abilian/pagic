from flask import Flask

from pagic.page import page, Page
from pagic.pagic import Pagic


@page
class HomePage(Page):
    name = "home"
    path = "/"
    label = "Home"

    layout = "base.j2"
    template = "home.j2"



def main():
    app = Flask(__name__)
    pagic = Pagic(app)
    pagic.register_roots([HomePage])
    app.run()


if __name__ == "__main__":
    main()
