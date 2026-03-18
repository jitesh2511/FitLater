from fitlater.cli.runner import run_cli
from fitlater.state.session import Session
from fitlater.cli.formatter import info

try:
    print(info())

    session = Session()
    run_cli(session)
except KeyboardInterrupt:
    print('\nTerminated by user.')
except Exception as e:
    print(f'Error : {e}')