FROM python:3.9

ARG PIP_TOKEN_PORTAINER

# Install portainer api client
RUN pip install portainer-management --index-url https://__token__:$PIP_TOKEN_PORTAINER@repo-url.url --extra-index-url https://pypi.python.org/simple