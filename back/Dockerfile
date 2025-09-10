FROM public.ecr.aws/docker/library/python:3.11-slim AS python-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Chromium + Chromedriver
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      chromium \
      chromium-driver \
      # dependency for headless
      libnss3 libatk-bridge2.0-0 libxss1 libgtk-3-0 libasound2 \
      fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# locate chromedriver to PATH
RUN ln -sf /usr/lib/chromium/chromedriver /usr/local/bin/chromedriver || \
    ln -sf /usr/lib/chromium-browser/chromedriver /usr/local/bin/chromedriver

    
FROM python-base AS poetry

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



FROM poetry AS vscode-devcontainer

# install git sudo
RUN apt-get update \
    && apt-get -y install git sudo git-secrets \
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



FROM poetry AS prod-build

# poetry install
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

COPY README.md ./
COPY parimana ./parimana
RUN poetry install --without dev



FROM python-base AS prod-base

# install parimana
ENV APP_PATH="/app" \
    PATH="/app/.venv/bin:$PATH" \
    FILE_STORAGE_ROOT_PATH="/var/parimana/repo"

COPY --from=prod-build ${APP_PATH} ${APP_PATH}



FROM prod-base AS aws

# set selenium manager cache path for lambda
ENV SE_CACHE_PATH=/tmp/.cache/selenium



FROM prod-base AS compose

# install dockerize
ENV DOCKERIZE_VERSION=v0.7.0
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
