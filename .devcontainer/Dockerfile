FROM python:3.13-slim-trixie

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install base dependencies
RUN apt update && apt install -y --no-install-recommends \
    git \
    openssh-client \
    curl \
    ca-certificates \
    tree \
    xclip \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh
ENV PATH="/root/.local/bin/:$PATH"

# Workspace
RUN mkdir -p /workspaces
WORKDIR /workspaces
