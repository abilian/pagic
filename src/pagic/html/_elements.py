"""HTML builder forked from xmlwitch.

There is still room for improvement.
"""

import keyword
from io import StringIO
from xml.sax.saxutils import escape, quoteattr

import defusedxml

from ._constants import html_tags

defusedxml.defuse_stdlib()


class _Element:
    tag: str

    def __init__(self, tag):
        self.tag = tag

    def __getattr__(self, key):
        if key in html_tags:
            return _Element(key)
        raise AttributeError(key)


def html():
    # return _Element("html")
    return Builder()


class Builder:
    def __init__(self):
        self._document = StringIO()

        self._encoding = "utf-8"
        self._indent = " "
        self._indentation = 0
        self._open_tag = None
        self._newline = ""

    def __getattr__(self, name):
        return Element(name, self)

    def __getitem__(self, name):
        return Element(name, self)

    def __str__(self):
        return self.__getvalue()

    def __getvalue(self) -> str:
        if self._open_tag:
            self._open_tag.close()

        return self._document.getvalue()

    def __del__(self):
        if self._open_tag:
            self._open_tag.close()

    def write(self, content: str):
        """Write raw content to the document."""
        self._document.write(content)
        self._newline = "\n"

    def write_escaped(self, content):
        """Write escaped content to the document."""
        self.write(escape(content))

    def write_indented(self, content):
        """Write indented content to the document."""
        self.write(f"{self._newline}{self._indent * self._indentation}{content}")

    def open_tag(self, element):
        self._open_tag = element

    def close_tag(self):
        """Close the currently open tag."""
        if self._open_tag:
            self._open_tag.close()

    def indent(self):
        self._indentation += 1

    def dedent(self):
        self._indentation -= 1


class Element:
    PYTHON_KWORD_MAP = {k + "_": k for k in keyword.kwlist}

    def __init__(self, name, builder):
        self.name = self._nameprep(name)
        self.content = ""
        self.builder = builder
        self.builder.close_tag()
        self.builder.write_indented(f"<{self.name}")
        self.builder._open_tag = self

    def close(self):
        if self.builder._open_tag is self:
            if self.content:
                self.builder.write(f">{self.content}</{self.name}>")
            else:
                self.builder.write(" />")
            self.builder._open_tag = None

    def __enter__(self):
        """Add a parent element to the document."""
        self.builder.write(f">{self.content}")
        self.builder.indent()
        self.builder._open_tag = None
        return self

    def __exit__(self, type, value, tb):
        """Add close tag to current parent element."""
        self.builder.close_tag()
        self.builder.dedent()
        self.builder.write_indented(f"</{self.name}>")

    def __call__(self, *args, **kargs):
        """Add content & attributes to the opened tag."""
        for attr, value in sorted(kargs.items()):
            self.builder.write(f" {self._nameprep(attr)}={quoteattr(value)}")
        for arg in args:
            self.content += escape(arg)
        return self

    def __del__(self):
        self.close()

    @classmethod
    def _nameprep(cls, name):
        """Undo keyword and colon mangling."""
        name = cls.PYTHON_KWORD_MAP.get(name, name)
        return name.replace("__", ":")
