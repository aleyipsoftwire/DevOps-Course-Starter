FROM python:3.9-slim as base

# Set up poetry
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update \
    && apt-get install --no-install-recommends --assume-yes curl
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi

COPY todo_app /app/todo_app

EXPOSE 8000

FROM base as test

ENTRYPOINT poetry run pytest

FROM base as production

ENV FLASK_DEBUG=false
CMD poetry run gunicorn --bind 0.0.0.0 "todo_app.app:create_app()"

FROM base as development

ENV FLASK_DEBUG=true
CMD poetry run gunicorn --bind 0.0.0.0 "todo_app.app:create_app()"
