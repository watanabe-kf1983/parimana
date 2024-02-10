FROM python:3.11-slim as python-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

FROM python-base as poetry

# install curl
RUN apt-get update \
    && apt-get -y install curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry"

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${POETRY_HOME}/bin:$PATH"


FROM poetry as vscode-devcontainer

# install git sudo
RUN apt-get update \
    && apt-get -y install git sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add non-root user
ARG USERNAME=vscode
ARG USER_ID=1000
ARG GROUP_ID=$USER_ID

RUN groupadd --gid $GROUP_ID $USERNAME \
    && useradd -s /bin/bash --uid $USER_ID --gid $GROUP_ID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /home/$USERNAME/

FROM poetry as prod-build

# poetry install
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

COPY README.md ./
COPY parimana ./parimana
RUN poetry install --without dev


FROM python-base as prod

# install dockerize
ENV DOCKERIZE_VERSION v0.7.0
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# install chrome
RUN apt-get update \
  && apt-get install -y --no-install-recommends gnupg \
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends google-chrome-stable \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/

# install parimana
ENV APP_PATH="/app" \
    PATH="/app/.venv/bin:$PATH" \
    FILE_REPO_PATH="/var/parimana/repo"

COPY --from=prod-build ${APP_PATH} ${APP_PATH}
