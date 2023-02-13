import re
from pathlib import Path

from invoke import task, Context


@task()
def help(c: Context):
    c.run("invoke --list")


@task()
def help_make(c: Context):
    """Helper to generate the `make help` message"""
    with Path(__file__).parent.joinpath("Makefile").open() as f:
        makefile = f.read()

    target = ""
    description = ""
    targets = []
    for line in makefile.splitlines():
        if m := re.match(r"^## (.*)", line):
            description = m.group(1)
        elif m := re.match("^(.*?):", line):
            target = m.group(1)
            if description:
                targets.append([target, description])
        else:
            target = ""
            description = ""

    max_len = max(len(t[0]) for t in targets)

    print("Targets:\n")
    for targets, description in targets:
        print(f"{targets:<{max_len}}  {description}")
