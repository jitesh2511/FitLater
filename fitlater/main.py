from fitlater.cli.runner import run_cli
from fitlater.state.session import Session
from fitlater.cli.formatter import info


def main():
    try:
        print(info())

        session = Session()
        run_cli(session)
    except KeyboardInterrupt:
        print('\nTerminated by user.')
    except Exception as e:
        print(f'Error : {e}')


if __name__ == '__main__':
    main()
