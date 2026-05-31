FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ENV DEBIAN_FRONTEND=noninteractive

# This container is intended for headless KiCad CLI checks/exports.
# Use native KiCad on the host for the GUI schematic and PCB editors.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        jq \
        make \
        python3 \
        python3-pip \
        kicad \
        kicad-symbols \
        kicad-footprints \
        kicad-templates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
