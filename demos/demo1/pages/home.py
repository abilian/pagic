from pagic.page import Page


class HomePage(Page):
    name = "home"
    path = ""
    label = "Home"

    layout = "base.j2"
    template = "home.j2"
