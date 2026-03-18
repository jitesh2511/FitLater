from fitlater.cli.commands import (load_dataset, 
                                   overview_command, 
                                   correlation_command, 
                                   outlier_command, 
                                   result_command)

COMMANDS = {
    'load':load_dataset,
    'overview':overview_command,
    'correlation':correlation_command,
    'outlier':outlier_command,
    'result':result_command
}