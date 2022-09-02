from flask import Flask

from pagic.pagic import Pagic


def create_app():
    app = Flask(__name__)
    pagic = Pagic(app)
    pagic.scan_pages("demo.pages")
    return app


def main():
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
