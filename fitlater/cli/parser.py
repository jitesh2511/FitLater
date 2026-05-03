"""
Simple command registry for the CLI.

Exposes the `COMMANDS` mapping which associates user-typed command names
to their handler callables. This mapping is imported by the CLI runner
to dispatch user input.
"""

from fitlater.cli.commands import (descriptive_command, load_dataset, 
                                   diagnostics_command,
                                   advisory_report_command)

COMMANDS = {
    'load':load_dataset,
    'descriptive':descriptive_command,
    'diagnostics':diagnostics_command,
    'advisory':advisory_report_command
}