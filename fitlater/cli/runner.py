from fitlater.cli.parser import COMMANDS

def run_cli(session):
    
    print('Type \'help\' for help\n')

    while True:
        try:
            user_input = input(">> ").strip()

            if not user_input:
                continue

            if user_input == 'exit':
                print('Terminating...\n')
                break

            if user_input == 'help':
                print('Available Commands : ')
                for cmd in COMMANDS:
                    print(f'- {cmd}')
                print('- exit\n')
                continue

            parts = user_input.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd in COMMANDS:
                COMMANDS[cmd](session, args)
            else:
                print('Unknown Command\n')
        except (KeyboardInterrupt, EOFError) as e:
            print(f'{e}\n')
            break
        except Exception as e:
            print(f'Error : {e}\n')
