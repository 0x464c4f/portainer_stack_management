import sys
import os
from portainer_management import Portainer_Management

if __name__ == "__main__":
    # execute only if run as a script
    try:
        compose_filename = sys.argv[1]
        stack_name = sys.argv[2]
        api = Portainer_Management(os.environ['PORTAINER_USER'],os.environ['PORTAINER_PW'])
        api.create_or_update_stack_from_compose_file(compose_filename=compose_filename,stack_name=stack_name)
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <name_of_compose_file> <name_of_stack>")