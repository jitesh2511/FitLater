import os

from fitlater.config import (NAME, VERSION)

# Safe terminal width
try:
    WIDTH = os.get_terminal_size().columns
except OSError:
    WIDTH = 100


def _heading(title: str) -> str:
    return f"\n{title.center(WIDTH, '=')}\n"


def _section(title: str) -> str:
    line = "-" * len(title)
    return f"\n{line}\n{title}\n{line}\n"

def info() -> str:
    lines = []
    start = "\033[1m"
    end = "\033[0m"
    lines.append(f'\n\n{start}{NAME}')
    lines.append(f'v{VERSION}{end}')

    return '\n'.join(lines) + '\n'
