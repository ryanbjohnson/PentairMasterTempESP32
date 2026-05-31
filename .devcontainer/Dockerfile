FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ENV DEBIAN_FRONTEND=noninteractive

# This container is intended for headless KiCad CLI checks/exports.
# Use native KiCad on the host for the GUI schematic and PCB editors.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        software-properties-common \
        jq \
        make \
        poppler-utils \
        python3 \
        python3-pip \
    && add-apt-repository -y ppa:kicad/kicad-8.0-releases \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        kicad \
        kicad-symbols \
        kicad-footprints \
        kicad-templates \
    && kicad-cli version | grep -E '^8\.' \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p \
        /home/vscode/.vscode-server/data/User/globalStorage/openai.chatgpt \
        /home/vscode/.codex \
    && chown -R vscode:vscode /home/vscode/.vscode-server /home/vscode/.codex
