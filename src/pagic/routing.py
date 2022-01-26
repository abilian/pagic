import traceback
from functools import singledispatch

from flask import url_for as url_for_orig
from werkzeug.routing import BuildError

from pagic import Page


@singledispatch
def url_for(obj, _ns="", **kw) -> str:
    raise RuntimeError(f"Illegal argument for 'url_for': {obj} (type: {type(obj)})")


@url_for.register
def url_for_page(page: Page, _ns="", **kw):
    return page.url


@url_for.register
def url_for_str(name: str, _ns="", **kw):
    try:
        return url_for_orig(name, **kw)
    except BuildError as e:
        traceback.print_exc()
        return "#"
