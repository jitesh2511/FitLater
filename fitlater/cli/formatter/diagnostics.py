from fitlater.cli.formatter.base import (
    _heading,
    _section
)

def format_missing_diag(result:dict, heading=False):

    if not result['meta']['has_issue']:
        if heading:
            return '\nNo missing columns'
        else:
            return f'{_section('Missing')}\nNo missing columns\n'

    lines = []

    if heading:
        lines.append(_heading('Missing'))
    else:
        lines.append(_section('Missing'))

    data = result['data']

    for k,v in data.items():
        
        if (v['missing_percentage'] > 1e-12):
            lines.append(f'Feature : {k}')
            lines.append(f'Missing Percentage = {v['missing_percentage']}')
            lines.append(f'Severity : {v['severity']}')
            lines.append(f'Hint : {v['hint']}\n')
    
    
    return '\n'.join(lines) + '\n'

def format_corr_diag(result:dict, heading=False):

    if not result['meta']['has_issue']:
        if heading:
            return '\nNo correlated columns'
        else:
            return f'{_section('Correlation')}\nNo correlated columns\n'
    
    lines = []

    if heading:
        lines.append(_heading('Correlation'))
    else:
        lines.append(_section('Correlation'))

    data = result['data']

    for k,v in data.items():
        lines.append(f'Feature 1 : {v['feature_1']} \t Feature 2 : {v['feature_2']}')
        lines.append(f'Correlation = {v['correlation']}')
        lines.append(f'Severity : {v['severity']}')
        lines.append(f'Hint : {v['hint']}\n')
    
    return '\n'.join(lines) + '\n'

def format_outliers_diag(result:dict, heading=False):

    if not result['meta']['has_issue']:
        if heading:
            return '\nNo columns contain outliers'
        else:
            return f'{_section('Outliers')}\nNo columns contain outliers\n'
    
    lines = []

    if heading:
        lines.append(_heading('Outliers'))
    else:
        lines.append(_section('Outliers'))

    data = result['data']

    for k,v in data.items():
        if (v['outlier_percentage'] > 1e-12):
            lines.append(f'Feature : {k}')
            lines.append(f'Outlier Percentage = {v['outlier_percentage']}')
            lines.append(f'Severity : {v['severity']}')
            lines.append(f'Hint : {v['hint']}\n')
    
    return '\n'.join(lines) + '\n'

def format_distribution_diag(result:dict, heading=False):

    if not result['meta']['has_issue']:
        if heading:
            return '\nNo skewed columns'
        else:
            return f'{_section('Distribution')}\nNo skewed columns\n'
    
    lines = []

    if heading:
        lines.append(_heading('Distribution'))
    else:
        lines.append(_section('Distribution'))

    data = result['data']

    for k,v in data.items():
        lines.append(f'Feature : {k}')
        lines.append(f'Skew = {v['skew']}')
        lines.append(f'Severity : {v['severity']}')
        lines.append(f'Hint : {v['hint']}\n')
    
    return '\n'.join(lines) + '\n'


def format_diagnostics(missing, corr, outliers, distribution):

    lines = []

    lines.append(_heading('Diagnostics'))
    lines.append(format_missing_diag(missing))
    lines.append(format_corr_diag(corr))
    lines.append(format_outliers_diag(outliers))
    lines.append(format_distribution_diag(distribution))

    return '\n'.join(lines)