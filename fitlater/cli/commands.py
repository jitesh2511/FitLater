import pandas as pd
from fitlater.cli.formatter.descriptive import format_descriptive
from fitlater.pipeline import run_pipeline
from fitlater.cli.formatter.advisory import format_advice
from fitlater.cli.formatter.diagnostics import format_diagnostics


def load_dataset(session, args):
    if not args:
        print('Usage : load <filepath>\n')
        return
    
    path = args[0]

    if not path.endswith('.csv'):
        path += '.csv'

    try:
        session.df = pd.read_csv(path)
        session.result = run_pipeline(session.df)
        print('Dataset loaded successfully\n')
    except Exception as e:
        print(f'Failed to load file : {e}\n')

def descriptive_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return
    
    print(format_descriptive(session.result["descriptive"]), '\n')

def diagnostics_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return

    print(format_diagnostics(session.result["diagnostics"], args), '\n')


def advisory_report_command(session, args):
    if session.df is None:
        print('No dataset loaded\n')
        return

    print(format_advice(session.result["advisory"],args), '\n')