from fitlater.cli.commands import (load_dataset, 
                                   overview_command, 
                                   correlation_command, 
                                   outlier_command, 
                                   describe_command,
                                   missing_diag_command,
                                   corr_diag_command,
                                   outlier_diag_command,
                                   distribution_diag_command,
                                   diagnostics_command)

COMMANDS = {
    'load':load_dataset,
    'overview':overview_command,
    'correlation':correlation_command,
    'outlier':outlier_command,
    'describe':describe_command,
    'missing_diags':missing_diag_command,
    'corr_diags':corr_diag_command,
    'outlier_diags':outlier_diag_command,
    'dist_diags':distribution_diag_command,
    'diagnostics':diagnostics_command
}