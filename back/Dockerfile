# Python is not part of the base image: uv installs the version in .python-version
FROM public.ecr.aws/docker/library/debian:trixie-slim AS base

ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
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

    
FROM base AS uv

# install curl
RUN apt-get update \
    && apt-get -y install curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# always use the Python that uv installs, never one that apt happens to pull in
ENV UV_PYTHON_PREFERENCE=only-managed \
    UV_LINK_MODE=copy



FROM uv AS vscode-devcontainer

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



FROM uv AS prod-build

# install Python to a fixed path, so that /app/.venv still works when both are copied into prod-base
ENV UV_PYTHON_INSTALL_DIR=/opt/python

# uv sync (installs the Python in .python-version first)
WORKDIR /app
COPY .python-version pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY README.md ./
COPY parimana ./parimana
RUN uv sync --locked --no-dev



FROM base AS prod-base

# install Python and parimana
ENV APP_PATH="/app" \
    PATH="/app/.venv/bin:$PATH" \
    FILE_STORAGE_ROOT_PATH="/var/parimana/repo"

COPY --from=prod-build /opt/python /opt/python
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
