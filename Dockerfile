FROM mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim

# Build tools are installed once; regression execution needs no external network.
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 gcc g++ golang-go \
       php-cli ruby rustc nodejs npm default-jdk-headless ca-certificates \
    && npm install --global typescript@5.6.3 \
    && rm -rf /var/lib/apt/lists/*
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1 \
    DOTNET_NOLOGO=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /lab
USER 65532:65532
ENTRYPOINT ["python3", "tools/lab.py"]
CMD ["test", "--strict", "--output", "reports/container-regression.json"]

