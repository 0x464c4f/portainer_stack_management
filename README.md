# Portainer Stack and Secret Management for Docker Swarm

## Description
This project is a collection of scripts that help to deploy/update Docker Swarm stacks through Portainer API's. 
It allows to: 
1. Create and update a Docker stack from a compose file as input 
2. Create or update Docker secrets to enable secret rotation
## Installation
1. The portainer username and password environment variables need to be defined first
    - "PORTAINER_URL"
    - "SWARM_ID"
    - "PORTAINER_USER"
    - "PORTAINER_PW"

2. Install package like this:

`pip install portainer-management --index-url https://__token__:<access_token>x@carm-infra.adfa.edu.au/app/gitlab/api/v4/projects/47/packages/pypi/simple --extra-index-url https://pypi.python.org/simple`


## API Usage

### Import library
`
from portainer_management import Portainer_Management
`

`
api = Portainer_Management(os.environ['portainer_username'],os.environ['portainer_pw'])
`

### Create/Update docker secret

`
api.create_or_update_docker_secret("super_secret","leeet")
`

### Create/Update Stack
`
api.create_or_update_stack_from_compose(compose_filename="docker-compose.yml",stack_name="test_stack")
`

