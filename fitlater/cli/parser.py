from fitlater.cli.commands import (descriptive_command, load_dataset, 
                                   diagnostics_command,
                                   advisory_report_command)

COMMANDS = {
    'load':load_dataset,
    'descriptive':descriptive_command,
    'diagnostics':diagnostics_command,
    'advisory':advisory_report_command
}