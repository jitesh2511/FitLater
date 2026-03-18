import pandas as pd
from fitlater.pipeline import (get_overview, get_outliers, get_correlation, get_results)

def load_dataset(session, args):
    if not args:
        print('Usage : load <filepath>\n')
        return
    
    path = args[0]

    try:
        session.df = pd.read_csv(path)
        session.file_path = path
        print('Dataset loaded sucessfully\n')
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

def result_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(get_results(session.df),'\n')
    
    