FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Remove the stale Yarn APT repository whose GPG key is expired/invalid.
# This prevents apt-get update from failing inside devcontainer feature scripts.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt-get update
