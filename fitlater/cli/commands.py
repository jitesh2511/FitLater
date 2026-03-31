import pandas as pd
from fitlater.pipeline import (
    get_overview, 
    get_outliers, 
    get_correlation, 
    get_description,
    get_missing_diag,
    get_corr_diag,
    get_outliers_diag,
    get_distribution_diag,
    get_diagnostics
)

def load_dataset(session, args):
    if not args:
        print('Usage : load <filepath>\n')
        return
    
    path = args[0]

    try:
        session.df = pd.read_csv(path)
        session.file_path = path
        print('Dataset loaded successfully\n')
    except Exception as e:
        print(f'Failed to load file : {e}\n')

def overview_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_overview(session.df),'\n')

def correlation_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_correlation(session.df),'\n')

def outlier_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_outliers(session.df),'\n')

def describe_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_description(session.df),'\n')
    
def missing_diag_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_missing_diag(session.df),'\n')

def corr_diag_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_corr_diag(session.df),'\n')

def outlier_diag_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_outliers_diag(session.df),'\n')

def distribution_diag_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_distribution_diag(session.df),'\n')

def diagnostics_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_diagnostics(session.df),'\n')
