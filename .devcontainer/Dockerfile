FROM python:3.14-trixie

COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /uvx /bin/

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        curl \
        bash-completion \
        build-essential \
        sudo \
        openssh-client \
        default-jre-headless \
        graphviz \
        locales \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

ARG PLANTUML_VERSION=1.2025.2
RUN curl -fsSL -o /usr/local/lib/plantuml.jar \
        https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar \
    && printf '#!/bin/sh\nexec java -jar /usr/local/lib/plantuml.jar "$@"\n' > /usr/local/bin/plantuml \
    && chmod +x /usr/local/bin/plantuml

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

ENV UV_LINK_MODE=copy
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
