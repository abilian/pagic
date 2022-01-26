"""Main module."""

from devtools import debug
from flask import Flask, request, g

from pagic.page import Route
from pagic.routing import url_for


class Pagic:
    app: Flask | None
    roots: list
    all_page_classes: list

    def __init__(self, app: Flask | None = None):
        self.roots = []
        self.all_page_classes = []
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        if "pagic" in app.extensions:
            raise RuntimeError("This extension is already registered on this Flask app.")

        self.app = app
        app.extensions["pagic"] = self

        app.before_request(self.before_request)
        app.context_processor(self.inject_extra_context)
        app.template_global("url_for")(url_for)

    def before_request(self):
        path = request.path
        debug(path)
        g.menus = {}

        for page_class in self.all_page_classes:
            menu_name = page_class.menu
            if not menu_name:
                continue

            if menu_name not in g.menus:
                g.menus[menu_name] = []

            endpoint = page_class.endpoint
            label = page_class.label
            url = url_for(endpoint)
            menu_item = {
                "label": label,
                "endpoint": endpoint,
                "url": url,
                "active": False,
            }
            g.menus[menu_name].append(menu_item)

    def inject_extra_context(self):
        return {
            "url_for": url_for,
            "pagic": self,
        }

    # TODO
    # def register_macros(app, path):
    #     scanner = venusian.Scanner()
    #     scanner.scan(importlib.import_module(path))
    #
    #     for macro in MACROS:
    #         app.template_global(macro.__name__)(macro)

    #
    # New registration API
    #
    def register_roots(self, roots):
        self.roots = roots
        for page_class in roots:
            self.register_page(page_class)

    def register_page(self, page_class, ancestors: list|None=None):
        self.all_page_classes.append(page_class)

        if ancestors is None:
            ancestors = []

        methods = ["GET", "POST"]
        route = Route(page_class)

        # if hasattr(page_class, "routes"):
        #     for _route in page_class.routes:
        #         self.app.add_url_rule(_route, page_class.name, route, methods=methods)
        #     return

        if page_class.path is None:
            page_class.path = page_class.name

        path_list = []
        for p in ancestors + [page_class]:
            if p.path:
                path_list.append(p.path)
        path = "/" + "/".join(path_list)
        self.app.add_url_rule(path, page_class.name, route, methods=methods)

        if hasattr(page_class, "children"):
            for child_class in page_class.children:
                self.register_page(child_class, ancestors + [page_class])

    #
    # Old API
    #
    # def register_pages(self, path=None):
    #     self.scan_pages(path)
    #
    #     for page_cls in Page.__all__pages__.values():
    #         print(f"Registering pags: {page_cls}")
    #         self.register_page(page_cls)
    #
    # def scan_pages(self, path):
    #     if not path:
    #         path = "tests"
    #     module = importlib.import_module(path)
    #     scanner = venusian.Scanner()
    #     scanner.scan(module)
    #
    # def register_page(self, cls):
    #     methods = ["GET", "POST"]
    #
    #     route = Route(cls)
    #     if hasattr(cls, "routes"):
    #         for _route in cls.routes:
    #             self.app.add_url_rule(_route, cls.name, route, methods=methods)
    #         return
    #
    #     if not hasattr(cls, "path"):
    #         cls.path = cls.name
    #
    #     self.app.add_url_rule(cls.path, cls.name, route, methods=methods)
